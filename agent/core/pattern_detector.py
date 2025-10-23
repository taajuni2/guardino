# monitor_churn.py (sehr klein)
import time
from collections import deque, defaultdict

class PatternDetector:
    def __init__(self, window_s=10, threshold=50, per_dir=True):
        self.window_s = window_s      # Zeitfenster in Sekunden
        self.threshold = threshold    # Anzahl Events im Fenster
        self.per_dir = per_dir
        # maps: key -> deque of timestamps
        self.events = defaultdict(deque)

    def _key_for(self, path):
        return path if not self.per_dir else __import__("os").path.dirname(path)

    def push_event(self, path):
        k = self._key_for(path)
        now = time.time()
        dq = self.events[k]
        dq.append(now)
        # trim old
        cutoff = now - self.window_s
        while dq and dq[0] < cutoff:
            dq.popleft()
        return len(dq) >= self.threshold

    def details(self, path):
        k = self._key_for(path)
        return {"count_in_window": len(self.events[k]), "window_s": self.window_s}


# patternDetector = PatternDetector(window_s=10, threshold=50)  # Beispielwerte
#
# # in on_created/on_modified:
# if churn.push_event(event.src_path):
#     emit_event({
#         "type": "mass_change",
#         "path": event.src_path,
#         "details": churn.details(event.src_path)
#     })