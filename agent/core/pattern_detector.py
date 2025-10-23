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
        self.events = defaultdict(lambda: deque())     # key -> deque[timestamps]

    def _key_for(self, path: str) -> str:
        return os.path.dirname(path) if self.per_dir else os.path.abspath(path)

    def _prune(self, q: deque, now: float):
        """Alte Timestamps aus dem Fenster entfernen."""
        border = now - self.window_s
        while q and q[0] < border:
            q.popleft()

    def push_event(self, path: str, now: float | None = None) -> bool:
        """
        Fügt ein Event hinzu und gibt True zurück, wenn threshold im Fenster erreicht/überschritten wurde.
        """
        now = now or time.time()
        k = self._key_for(path)
        q = self.events[k]
        self._prune(q, now)
        q.append(now)
        return len(q) >= self.threshold

    def count(self, path: str, now: float | None = None) -> int:
        now = now or time.time()
        k = self._key_for(path)
        q = self.events[k]
        self._prune(q, now)
        return len(q)

    def details(self, path: str, now: float | None = None) -> dict:
        now = now or time.time()
        k = self._key_for(path)
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