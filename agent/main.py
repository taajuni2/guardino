from core.blacklist import PathBlacklist
from core import monitor
import logging
from utils.utils import load_config, setup_logging

config = load_config("config/agent_config.yaml")
log = setup_logging("INFO")
log = logging.getLogger("agent.main")

def dummy_detection(file_path):
    print(f"🔍 Verdächtige Änderung erkannt an: {file_path}")
    # TODO: Hier später Entropieprüfung oder andere Erkennung aufrufen

def emit_event(evt: dict):
    if isinstance(evt, str):
        print(f"[ALERT] entropy_spike -> {evt}")
        return
    print(f"[ALERT] {evt['type']} {evt['event_type']} -> {evt['path']} | {evt['details']}")

def main():
    config = load_config("config/agent_config.yaml")

    watch_dirs = config.get("watch_directories", [])
    blacklist_paths = config.get("blacklist_paths", [])

    blacklist = PathBlacklist(blacklist_paths)

    clean_watch_dirs = [d for d in watch_dirs if not blacklist.is_blacklisted(d)]

    if not clean_watch_dirs:
        print("Keine gültigen Watch-Verzeichnisse. Agent beendet.")
        return

    print(" Starte Überwachung...")
    log.info("monitoring started")
    monitor.start_monitoring(clean_watch_dirs, blacklist, emit_event)

if __name__ == "__main__":
    main()
