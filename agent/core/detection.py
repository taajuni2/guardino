# core/detection.py
import logging
import os, math
from collections import Counter

log = logging.getLogger("agent.detection")

def _entropy(data: bytes) -> float:
    if not data:
        return 0.0
    total = len(data)
    counts = Counter(data)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


def entropy_spike(path: str,
                  abs_threshold: float = 7.5,
                  min_size_bytes: int = 4096,
                  sample_each: int = 8192) -> tuple[bool, dict]:
    """
    Prüft, ob eine Datei aufgrund hoher Entropie verdächtig ist.
    Liest Head+Tail (je sample_each Bytes) und berechnet Shannon-Entropie.
    """
    try:
        log.debug("Entriopy_spike reached")
        st = os.stat(path)
        if not os.path.isfile(path) or st.st_size < min_size_bytes:
            return False, {"reason": "too small or not a regular file"}

        with open(path, 'rb') as f:
            head = f.read(sample_each)
            if st.st_size > sample_each * 2:
                f.seek(-sample_each, os.SEEK_END)
                tail = f.read(sample_each)
            else:
                tail = b""
        data = head + tail
        H = _entropy(data)
        is_spike = H >= abs_threshold
        log.info(f"Spike: {is_spike}")
        details = {
            "entropy": round(H, 3),
            "bytes_sampled": len(data),
            "threshold": abs_threshold,
            "reason": "entropy threshold reached!" if is_spike else "below entropy threshold",
        }
        return is_spike, details
    except Exception as e:
        return False, {"reason": f"exception: {e}"}
