# detection.py
import os, math
from collections import Counter

def _entropy(data: bytes) -> float:
    if not data:
        return 0.0
    total = len(data)
    counts = Counter(data)
    return -sum((c/total) * math.log2(c/total) for c in counts.values())

def entropy_spike(path: str,
                  abs_threshold: float = 7.5,
                  min_size_bytes: int = 4096,
                  sample_each: int = 8192) -> tuple[bool, dict]:
    """
    Minimal-PoC: Liest nur Head+Tail (je sample_each Bytes) und triggert,
    wenn Entropie >= abs_threshold.
    """
    try:
        if not os.path.isfile(path):
            return False, {"reason": "not a regular file"}

        size = os.path.getsize(path)
        if size < min_size_bytes:
            return False, {"reason": f"too small ({size}B)"}

        with open(path, "rb") as f:
            head = f.read(sample_each)
            if size > sample_each:
                f.seek(max(0, size - sample_each))
                tail = f.read(sample_each)
            else:
                tail = b""

        data = head + tail
        H = _entropy(data)
        is_spike = H >= abs_threshold
        details = {
            "entropy": round(H, 3),
            "bytes_sampled": len(data),
            "threshold": abs_threshold,
            "reason": "entropy threshold reached!" if is_spike else "below entropy threshold",
        }
        return is_spike, details

    except Exception as e:
        return False, {"reason": f"exception: {e}"}

