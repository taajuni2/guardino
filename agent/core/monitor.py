from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .detection import entropy_spike
from .pattern_detector import PatternDetector
import time
import os
import logging


log = logging.getLogger("agent.monitor")

class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, blacklist, detection_callback, cooldown_seconds: int = 5, mass_create_window_s: int = 10, mass_create_threshold: int = 50):
        self.blacklist = blacklist
        self.detection_callback = detection_callback
        self.cooldown_seconds = cooldown_seconds
        self._last_alert_ts = {}
        self.mass_create = PatternDetector(window_s=mass_create_window_s, threshold=mass_create_threshold, per_dir=True)

    def _check_and_emit(self, path: str, kind: str):
        try:
            if self.blacklist and self.blacklist.is_blacklisted(path):
                return

            now = time.time()
            last = self._last_alert_ts.get(path, 0)
            if (now - last) < self.cooldown_seconds:
                return
            suspicious, details = entropy_spike(path)
            if suspicious:
                self._last_alert_ts[path] = now
                evt = {
                    "type": "mass_create",
                    "event_type": kind,
                    "path": path,
                    "details": details,
                }
                # <<< HIER: Callback erhält ein Dict, nicht das Event-Objekt >>>
                self.detection_callback(evt)
        except Exception:
            log.exception("entropy check failed for %s", path)


    def on_modified(self, event):
        if not event.is_directory:
            self._check_and_emit(event.src_path, "modified")


    def _rate_limited(self, key: str, now: float) -> bool:
        last = self._last_alert_ts.get(key, 0.0)
        if now - last < self.cooldown_seconds:
            return True
        self._last_alert_ts[key] = now
        return False

    def on_created(self, event):
        if event.is_directory:
            return
        path = os.path.abspath(event.src_path)
        if self.blacklist.is_blacklisted(path):
            return

        now = time.time()
        # (1) Detector „füttern“
        triggered = self.mass_create.push_event(path, now=now)
        if not triggered:
            return

        # (2) Details holen und ggf. gedrosselt melden
        det = self.mass_create.details(path, now=now)
        k = det["key"]
        if self._rate_limited(k, now):
            return
        log.info("STEP IN ON CREATED IS REACHED")
        # (3) Event emittieren
        evt = {
            "type": "entropy_spike",
            "event_type": "mass_create",
            "path": k,
            "details": "KEINE",
        }

        self.detection_callback(evt)

def start_monitoring(paths, blacklist, detection_callback, cooldown_seconds=5, mass_create_window_s=10, mass_create_threshold=50):
    observer = Observer()
    event_handler = FileMonitorHandler(blacklist, detection_callback, cooldown_seconds=cooldown_seconds, mass_create_window_s=mass_create_window_s, mass_create_threshold=mass_create_threshold)
    for path in paths:
        if not blacklist.is_blacklisted(path) and os.path.exists(path):
            observer.schedule(event_handler, path, recursive=True)

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
