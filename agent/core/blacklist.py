import os
import logging

log = logging.getLogger("agent.blacklist")

class PathBlacklist:
    def __init__(self, blacklist):
        self.blacklist = set(os.path.abspath(p) for p in blacklist)

    def is_blacklisted(self, path):
        abs_path = os.path.abspath(path)
        return any(abs_path.startswith(b) for b in self.blacklist)