import math
from collections import Counter

def calculate_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counter = Counter(data)
    total = len(data)
    entropy = -sum((count / total) * math.log2(count / total) for count in counter.values())
    return entropy

def is_suspicious_file(path: str, entropy_threshold: float = 7.5, allowed_extensions=None) -> (bool, str):
    if allowed_extensions and not any(path.endswith(ext) for ext in allowed_extensions):
        return False, "Extension not monitored"

    try:
        with open(path, "rb") as f:
            data = f.read(2048)  # Nur ersten 2KB prüfen
            entropy = calculate_entropy(data)

            if entropy > entropy_threshold:
                return True, f"High entropy detected ({entropy:.2f})"
            else:
                return False, f"Entropy OK ({entropy:.2f})"
    except Exception as e:
        return False, f"Could not read file: {e}"
