# core/pattern_detector.py
from __future__ import annotations
import time
from collections import deque, defaultdict
import os


class PatternDetector:
    """
    Erkennt Massen-Events in einem gleitenden Zeitfenster.
    - per_dir=True: pro Basisverzeichnis bündeln (dirname(path))
    - window_s: Fensterbreite in Sekunden
    - threshold: ab wie vielen Events im Fenster ein Alarm ausgelöst wird
    """
    def __init__(self, window_s: int = 10, threshold: int = 50, per_dir: bool = True):
        self.window_s = window_s
        self.threshold = threshold
        self.per_dir = per_dir
        self.events = defaultdict(deque) # key -> deque[timestamps]
        self.paths = defaultdict(deque) # key -> deque[paths]

    def key_for(self, path: str) -> str:
        return os.path.dirname(path) if self.per_dir else "__all__"

    def _prune(self, q: deque, now: float):
        cutoff = now - self.window_s
        while q and q[0] < cutoff:
            q.popleft()

    def add_event(self, path: str, now: float | None = None):
        now = now or time.time()
        k = self.key_for(path)
        self.events[k].append(now)
        self.paths[k].append(path)
        self._prune(self.events[k], now)
        # paths deck gleich lang halten
        while len(self.paths[k]) > len(self.events[k]):
            self.paths[k].popleft()

    def count(self, path: str, now: float | None = None) -> int:
        now = now or time.time()
        k = self.key_for(path)
        q = self.events[k]
        self._prune(q, now)
        return len(q)

    def recent_paths(self, path: str, now: float | None = None, max_items: int = 100) -> list[str]:
        now = now or time.time()
        k = self.key_for(path)
        q = self.events[k]
        self._prune(q, now)
        # n jüngste Pfade (bis Fensterlänge)
        return list(self.paths[k])[-max_items:]

    def details(self, path: str, now: float | None = None) -> dict:
        now = now or time.time()
        k = self.key_for(path)
        q = self.events[k]
        self._prune(q, now)
        return {
            "key": k,
            "count_in_window": len(q),
            "window_s": self.window_s,
            "threshold": self.threshold,
            "first_ts": q[0] if q else None,
            "last_ts": q[-1] if q else None,
    }