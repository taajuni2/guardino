# main.py
import os
import time
import json
import logging
from core.blacklist import PathBlacklist
from core import monitor
from core.agent_control import AgentControl
from utils.utils import load_config, setup_logging


def emit_event(evt: dict):
    """Hier später: Kafka/REST; aktuell stdout."""
    print(json.dumps(evt, ensure_ascii=False))


def main():
#Load config
    config_path = os.getenv("AGENT_CONFIG", "config/agent_config.yaml")
    config = load_config(config_path)

#Logger setup
    logger = setup_logging(config.get("log_level", "INFO"))
    log = logging.getLogger("agent.main")




#Load Parameters
    mass_window = int(config.get("mass_create_window_s", 10))
    mass_threshold = int(config.get("mass_create_threshold", 50))
    cooldown = int(config.get("cooldown_seconds", 5))
    entropy_thr = float(config.get("entropy_abs_threshold", 7.5))
    entropy_min_size = int(config.get("entropy_min_size_bytes", 4096))
    entropy_sample_each = int(config.get("entropy_sample_each", 8192))
    topics = config.get("kafka", {}).get("topics", {})
    broker = config.get("kafka", {}).get("broker", {})
    control_topic = topics.get("control", "agent-control")


    print("DEBUG heartbeat_interval_s =", config.get("heartbeat_interval_s"))


# Heartbeat und Autoregistration vorbereiten
    agent_id = config.get("agent_id", "agent-default-01")
    heartbeat_interval = int(config.get("heartbeat_interval_s", 20))
    agent_control = AgentControl(
        broker=broker,
        control_topic=control_topic,
        config=config,
        agent_id=agent_id,
        heartbeat_interval=heartbeat_interval,
        stdout_fallback=bool(os.environ.get("STDOUT_ONLY", "0") == "1"),
    )

    assigned_agent_id = agent_control.register()
    if assigned_agent_id:
        config["agent_id"] = assigned_agent_id
        log.info("Registered as agent_id=%s", assigned_agent_id)
    else:
        log.warning("No register_ack call received. Proceeding with agent_id=%s", agent_id)

    agent_control.start_heartbeat()
# Blacklist und Watch-Dirs hohlen
    watch_dirs = [os.path.expanduser(p) for p in config.get("watch_directories", [])]
    blacklist_paths = [os.path.expanduser(p) for p in config.get("blacklist_paths", [])]

    blacklist = PathBlacklist(blacklist_paths)
    clean_watch_dirs = [d for d in watch_dirs if os.path.exists(d) and not blacklist.is_blacklisted(d)]
    if not clean_watch_dirs:
        log.error("Keine gültigen Watch-Verzeichnisse. Agent beendet.")
        return

    # Parameter (können in YAML-File ergänzt werden)

    log.info(f"Agent ID: {agent_id}")
    log.info(f"Mass entropy threshold: {entropy_thr}")
    log.info(f"Mass create threshold: {mass_threshold}")
    monitor.start_monitoring(
        clean_watch_dirs,
        blacklist,
        emit_event,
        cooldown_seconds=cooldown,
        mass_create_window_s=mass_window,
        mass_create_threshold=mass_threshold,
        agent_id=agent_id, # agent ID muss noch dynamisch erstellt werden
        entropy_abs_threshold=entropy_thr,
        entropy_min_size_bytes=entropy_min_size,
        entropy_sample_each=entropy_sample_each,
)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        agent_control.stop_heartbeat()

if __name__ == "__main__":
    main()