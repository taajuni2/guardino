from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .detection import entropy_spike
import time
import os
import logging


log = logging.getLogger("agent.monitor")

class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, blacklist, detection_callback):
        self.blacklist = blacklist
        self.detection_callback = detection_callback

    def _check(self, path: str, kind: str):
        if self.blacklist and self.blacklist.is_blacklisted(path):
            return
        suspicious, details = entropy_spike(path)
        if suspicious:
            log.warning("Entropy spike: %s | %s", path, details)
            self.detection_callback({
                "type": "entropy_spike",
                "path": path,
                "event_type": kind,
                "details": details
            })

    def on_modified(self, event):
        if not event.is_directory and not self.blacklist.is_blacklisted(event.src_path):
            log.info("%s is blacklisted" % event.src_path)
            self.detection_callback(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self._check(event.src_path, "created")

def start_monitoring(paths, blacklist, detection_callback):
    observer = Observer()

    for path in paths:
        if not blacklist.is_blacklisted(path) and os.path.exists(path):
            event_handler = FileMonitorHandler(blacklist, detection_callback)
            observer.schedule(event_handler, path, recursive=True)

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
