# core/monitor.py
from __future__ import annotations

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .detection import entropy_spike
from .pattern_detector import PatternDetector
from .events import Event
import time
import os
import json
import logging
from typing import Callable, Dict, List

log = logging.getLogger("agent.monitor")


class FileMonitorHandler(FileSystemEventHandler):
    """
    Vereinheitlicht die Erkennung und das Emittieren von Events:
    - Mass Creation: via PatternDetector im gleitenden Zeitfenster
    - Entropy Spike: via detection.entropy_spike()
    - Einheitliche Event-Struktur, Rate-Limiting, Blacklist-Check
    """


    def __init__(
            self,
            blacklist,
            detection_callback: Callable[[dict], None],
            cooldown_seconds: int = 5,
            mass_create_window_s: int = 10,
            mass_create_threshold: int = 50,
            agent_id: str | None = None,
            entropy_abs_threshold: float = 7.5,
            entropy_min_size_bytes: int = 4096,
            entropy_sample_each: int = 8192,
            per_dir_mass: bool = True,
    ):
        self.blacklist = blacklist
        self.detection_callback = detection_callback
        self.cooldown_seconds = cooldown_seconds
        self.agent_id = agent_id or os.getenv("AGENT_ID", "agent-unknown")


        # Mass-Creation Detector
        self.mass_detector = PatternDetector(
        window_s=mass_create_window_s,
        threshold=mass_create_threshold,
        per_dir=per_dir_mass,
    )

        # Entropy-Parameter
        self.entropy_abs_threshold = entropy_abs_threshold
        self.entropy_min_size_bytes = entropy_min_size_bytes
        self.entropy_sample_each = entropy_sample_each

        # Rate-Limiting (pro Schlüssel)
        self._last_alert_ts: Dict[str, float] = {}


    # --------------------------
    # Filesystem Hooks
    # --------------------------
    def on_created(self, event):
        if event.is_directory:
            return
        path = event.src_path
        if self._is_blacklisted(path):
            return

    # 1) Mass Creation Pfad füttern
        now = time.time()
        self.mass_detector.add_event(path, now=now)

    # Prüfen, ob Schwellwert erreicht
        count = self.mass_detector.count(path, now=now)
        if count >= self.mass_detector.threshold:
            key = f"mass:{self.mass_detector._key_for(path)}"
            if not self._rate_limited(key, now):
                details = self.mass_detector.details(path, now=now)
                sev = "warning" if count < (self.mass_detector.threshold * 2) else "critical"
                ev = Event.build(
                    agent_id=self.agent_id,
                    type_="mass_creation",
                    severity=sev,
                    summary=f"Mass file creation detected: {details['count_in_window']} files in {details['window_s']}s",
                    paths=self._limit_paths(self.mass_detector.recent_paths(path, now=now)),
                    metadata={
                        "key": details["key"],
                        "count_in_window": details["count_in_window"],
                        "window_s": details["window_s"],
                        "threshold": details["threshold"],
                        "first_ts": details["first_ts"],
                        "last_ts": details["last_ts"],
                    },
                    raw={"sample_paths": self.mass_detector.recent_paths(path, now=now, max_items=200)},
                )
                self._emit(ev)

        # 2) Für on_created direkt auch Entropie prüfen (frühe Erkennung)
        self._check_entropy_and_emit(path)

    def _check_entropy_and_emit(self, path: str):
        now = time.time()
        ok, details = entropy_spike(
            path,
            abs_threshold=self.entropy_abs_threshold,
            min_size_bytes=self.entropy_min_size_bytes,
            sample_each=self.entropy_sample_each,
        )
        if not ok:
            return

        dir_key = os.path.dirname(path) or "/"
        key = f"entropy:{dir_key}"
        if self._rate_limited(key, now):
            return

        entropy_val = details.get("entropy", 0.0)
        sev = "warning" if entropy_val < (self.entropy_abs_threshold + 0.8) else "critical"
        ev = Event.build(
            agent_id=self.agent_id,
            type_="entropy_spike",
            severity=sev,
            summary=f"Entropy spike detected (H={entropy_val}) at {path}",
            paths=[path],
            metadata={
                "entropy": entropy_val,
                "threshold": details.get("threshold", self.entropy_abs_threshold),
                "bytes_sampled": details.get("bytes_sampled"),
            },
            raw={"reason": details.get("reason")},
        )
        self._emit(ev)
    def _emit(self, event_obj: Event):
        """
        Zentraler Emitter-Hook: einheitliches JSON, Logging, Callback.
        Den eigentlichen Versand (Kafka/REST) übernimmt detection_callback (z. B. main.emit_event).
        """
        try:
            event = event_obj.to_dict()
        # Blacklist final auf paths anwenden (Defensivprogrammierung)
            event["paths"] = [p for p in event.get("paths", []) if not self._is_blacklisted(p)]
            log.info(
            "Emitting event id=%s type=%s severity=%s paths=%d",
            event["id"], event["type"], event["severity"], len(event["paths"][0]),
            )
            self.detection_callback(event)
        except Exception as e:
            log.exception("Emit failed: %s; event=%s", e, json.dumps(event_obj.to_dict(), ensure_ascii=False))

    def _limit_paths(self, paths: List[str], max_items: int = 20) -> List[str]:
        return [p for p in paths if not self._is_blacklisted(p)][:max_items]


    def _is_blacklisted(self, path: str) -> bool:
        try:
            return self.blacklist.is_blacklisted(path)
        except Exception:
            return False

    def _rate_limited(self, key: str, now: float) -> bool:
        last = self._last_alert_ts.get(key, 0.0)
        if now - last < self.cooldown_seconds:
            return True
        self._last_alert_ts[key] = now
        return False

def start_monitoring(
    paths: List[str],
    blacklist,
    detection_callback: Callable[[dict], None],
    cooldown_seconds: int = 5,
    mass_create_window_s: int = 10,
    mass_create_threshold: int = 50,
    agent_id: str | None = None,
    entropy_abs_threshold: float = 7.5,
    entropy_min_size_bytes: int = 4096,
    entropy_sample_each: int = 8192,
):

    observer = Observer()
    event_handler = FileMonitorHandler(
        blacklist=blacklist,
        detection_callback=detection_callback,
        cooldown_seconds=cooldown_seconds,
        mass_create_window_s=mass_create_window_s,
        mass_create_threshold=mass_create_threshold,
        agent_id=agent_id,
        entropy_abs_threshold=entropy_abs_threshold,
        entropy_min_size_bytes=entropy_min_size_bytes,
        entropy_sample_each=entropy_sample_each,
    )

    for path in paths:
        if not os.path.exists(path):
            log.warning("Skipping non-existing path: %s", path)
            continue
        if blacklist.is_blacklisted(path):
            log.warning("Skipping blacklisted path: %s", path)
            continue
        observer.schedule(event_handler, path, recursive=True)

    observer.start()
    log.info("File monitoring started on: %s", paths)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()