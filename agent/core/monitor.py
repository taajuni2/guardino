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

    def _check_and_emit(self, path: str, kind: str):
        try:
            if self.blacklist and self.blacklist.is_blacklisted(path):
                return
            suspicious, details = entropy_spike(path)
            if suspicious:
                evt = {
                    "type": "entropy_spike",
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
            log.info("%s on modified", event.src_path)
            self._check_and_emit(event.src_path, "modified")

    def on_created(self, event):
        if not event.is_directory:
            log.info("%s is on created" % event.src_path)
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
