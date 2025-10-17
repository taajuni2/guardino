from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

class FileMonitorHandler(FileSystemEventHandler):
    def __init__(self, blacklist, detection_callback):
        self.blacklist = blacklist
        self.detection_callback = detection_callback

    def on_modified(self, event):
        if not event.is_directory and not self.blacklist.is_blacklisted(event.src_path):
            self.detection_callback(event.src_path)

    def on_created(self, event):
        if not event.is_directory and not self.blacklist.is_blacklisted(event.src_path):
            self.detection_callback(event.src_path)

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
