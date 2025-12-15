# core/blacklist.py
import os
import logging

log = logging.getLogger("agent.blacklist")

class PathBlacklist:
    def __init__(self, blacklist):
        # Normalisiere und erweitere ~
        self.blacklist = set(os.path.abspath(os.path.expanduser(p)) for p in blacklist)

    def is_blacklisted(self, path: str) -> bool:
        try:
            abs_path = os.path.abspath(os.path.expanduser(path))
            return any(abs_path.startswith(b) for b in self.blacklist)
        except Exception:
            return False