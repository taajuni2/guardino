# main.py
import os
import json
import logging
from core.blacklist import PathBlacklist
from core import monitor
from utils.utils import load_config, setup_logging


def emit_event(evt: dict):
    """Hier später: Kafka/REST; aktuell stdout."""
    print(json.dumps(evt, ensure_ascii=False))


def main():
# Konfiguration laden
    config_path = os.getenv("AGENT_CONFIG", "config/agent_config.yaml")
    config = load_config(config_path)

    logger = setup_logging(config.get("log_level", "INFO"))
    log = logging.getLogger("agent.main")

    # Blacklist & Watch-Dirs
    watch_dirs = [os.path.expanduser(p) for p in config.get("watch_directories", [])]
    blacklist_paths = [os.path.expanduser(p) for p in config.get("blacklist_paths", [])]

    blacklist = PathBlacklist(blacklist_paths)
    clean_watch_dirs = [d for d in watch_dirs if os.path.exists(d) and not blacklist.is_blacklisted(d)]
    if not clean_watch_dirs:
        log.error("Keine gültigen Watch-Verzeichnisse. Agent beendet.")
        return

    # Parameter (können in YAML ergänzt werden)
    agent_id = os.getenv("AGENT_ID", config.get("agent_id", "agent-01"))
    mass_window = int(config.get("mass_create_window_s", 10))
    mass_threshold = int(config.get("mass_create_threshold", 50))
    cooldown = int(config.get("cooldown_seconds", 5))
    entropy_thr = float(config.get("entropy_abs_threshold", 7.5))
    entropy_min_size = int(config.get("entropy_min_size_bytes", 4096))
    entropy_sample_each = int(config.get("entropy_sample_each", 8192))
    log.info(f"Agent ID: {agent_id}")
    log.info(f"Mass entropy threshold: {entropy_thr}")
    log.info(f"Mass create threshold: {mass_threshold}")
    log.info("Monitoring of: %s started", clean_watch_dirs)
    monitor.start_monitoring(
        clean_watch_dirs,
        blacklist,
        emit_event,
        cooldown_seconds=cooldown,
        mass_create_window_s=mass_window,
        mass_create_threshold=mass_threshold,
        agent_id=agent_id,
        entropy_abs_threshold=entropy_thr,
        entropy_min_size_bytes=entropy_min_size,
        entropy_sample_each=entropy_sample_each,
)


if __name__ == "__main__":
    main()