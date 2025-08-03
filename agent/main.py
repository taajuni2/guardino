from core.blacklist import PathBlacklist
from core import monitor
import yaml

def load_config(config_path="config/agent_config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def dummy_detection(file_path):
    print(f"🔍 Verdächtige Änderung erkannt an: {file_path}")
    # TODO: Hier später Entropieprüfung oder andere Erkennung aufrufen

def main():
    config = load_config()

    watch_dirs = config.get("watch_directories", [])
    blacklist_paths = config.get("blacklist_paths", [])

    blacklist = PathBlacklist(blacklist_paths)

    clean_watch_dirs = [d for d in watch_dirs if not blacklist.is_blacklisted(d)]

    if not clean_watch_dirs:
        print("❌ Keine gültigen Watch-Verzeichnisse. Agent beendet.")
        return

    print("🚀 Starte Überwachung...")
    monitor.start_monitoring(clean_watch_dirs, blacklist, dummy_detection)

if __name__ == "__main__":
    main()
