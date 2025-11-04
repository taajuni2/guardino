import os
import time
import json
import logging
import asyncio
import threading

from core.blacklist import PathBlacklist
from core import monitor
from core.agent_control import AgentControl
from utils.utils import load_config, setup_logging, get_or_create_agent_id

from transport.producer import KafkaEventProducer


def main():
    # -------------------------------------------------
    # 1. Config laden
    # -------------------------------------------------
    config_path = os.getenv("AGENT_CONFIG", "config/agent_config.yaml")
    config = load_config(config_path)

    # -------------------------------------------------
    # 2. Logger setup
    # -------------------------------------------------
    setup_logging(config.get("log_level", "INFO"))
    log = logging.getLogger("agent.main")

    # -------------------------------------------------
    # 3. Werte aus Config holen
    # -------------------------------------------------
    mass_window = int(config.get("mass_create_window_s", 10))
    mass_threshold = int(config.get("mass_create_threshold", 50))
    cooldown = int(config.get("cooldown_seconds", 5))

    entropy_thr = float(config.get("entropy_abs_threshold", 7.5))
    entropy_min_size = int(config.get("entropy_min_size_bytes", 4096))
    entropy_sample_each = int(config.get("entropy_sample_each", 8192))

    kafka_cfg = config.get("kafka", {})
    topics = kafka_cfg.get("topics", {})
    broker = kafka_cfg.get("broker", "localhost:9092")
    events_topic = topics.get("events", "agent-events")
    control_topic = topics.get("control", "agent-lifecycle")

    agent_id = get_or_create_agent_id(config_path)
    heartbeat_interval = int(config.get("heartbeat_interval_s", 20))
    log.debug("heartbeat_interval_s = %s", heartbeat_interval)

    # -------------------------------------------------
    # 4. Async Event Loop im Hintergrund-Thread
    #    (damit wir aiokafka in synchronem Code nutzen können)
    # -------------------------------------------------
    loop = asyncio.new_event_loop()

    def loop_runner():
        asyncio.set_event_loop(loop)
        loop.run_forever()

    loop_thread = threading.Thread(target=loop_runner, daemon=True)
    loop_thread.start()

    # -------------------------------------------------
    # 5. Kafka Producer Instanz
    # -------------------------------------------------
    producer = KafkaEventProducer(
        broker=broker,
        topic=events_topic,
        log=log,
    )

    # Producer im Hintergrundloop starten
    asyncio.run_coroutine_threadsafe(producer.start(), loop)

    # -------------------------------------------------
    # 6. emit_event Funktion bauen
    #    Diese wird von monitor.start_monitoring() aufgerufen.
    #    Sie ist sync, aber schiebt Events async in den Producer.
    # -------------------------------------------------
    def emit_event(evt: dict):
        """
        Versucht Event an Kafka zu senden.
        Fallback: stdout, wenn Kafka nicht bereit ist oder send_event False liefert.
        """
        fut = asyncio.run_coroutine_threadsafe(producer.send_event(evt), loop)
        try:
            ok = fut.result(timeout=2)
            if not ok:
                # Kafka nicht ready oder Sendefehler
                log.debug("STDOUT fallback (Kafka send failed or producer not started): %s", evt)
                print(json.dumps(evt, ensure_ascii=False))
        except Exception as e:
            # harter Fehler beim Senden
            log.warning("Kafka send exception (%s), fallback stdout", e)
            print(json.dumps(evt, ensure_ascii=False))

    # -------------------------------------------------
    # 7. AgentControl (Heartbeat, Registrierung)
    # -------------------------------------------------
    agent_control = AgentControl(
        broker=broker,
        control_topic=control_topic,
        config=config,
        agent_id=agent_id,
        heartbeat_interval=heartbeat_interval,
        stdout_fallback=bool(os.environ.get("STDOUT_ONLY", "0") == "1"),
    )

    # Registrierung jetzt nur noch "ich bin da", kein ack erwartet
    agent_control.register()
    log.info("MAIN running as agent_id=%s", agent_id)

    # Heartbeat starten
   # agent_control.start_heartbeat()
   # agent_control.start_heartbeat()

    # -------------------------------------------------
    # 8. Watch Directories + Blacklist
    # -------------------------------------------------
    watch_dirs = [os.path.expanduser(p) for p in config.get("watch_directories", [])]
    blacklist_paths = [os.path.expanduser(p) for p in config.get("blacklist_paths", [])]

    blacklist = PathBlacklist(blacklist_paths)

    clean_watch_dirs = [
        d for d in watch_dirs
        if os.path.exists(d) and not blacklist.is_blacklisted(d)
    ]

    if not clean_watch_dirs:
        log.error("Keine gültigen Watch-Verzeichnisse. Agent beendet.")
        agent_control.stop_heartbeat()

        # Producer stoppen und Loop beenden
        asyncio.run_coroutine_threadsafe(producer.stop(), loop).result(timeout=2)
        loop.call_soon_threadsafe(loop.stop)
        loop_thread.join(timeout=2)
        return

    log.info("Agent ID: %s", agent_id)
    log.info("Mass entropy threshold: %s", entropy_thr)
    log.info("Mass create threshold: %s", mass_threshold)
    log.info("Watching dirs: %s", clean_watch_dirs)

    # -------------------------------------------------
    # 9. Monitoring starten (dein File-/Ransomware-Detector)
    # -------------------------------------------------
    monitor.start_monitoring(
        clean_watch_dirs,
        blacklist,
        emit_event,  # <- jetzt geht alles über KafkaEventProducer
        cooldown_seconds=cooldown,
        mass_create_window_s=mass_window,
        mass_create_threshold=mass_threshold,
        agent_id=agent_id,
        entropy_abs_threshold=entropy_thr,
        entropy_min_size_bytes=entropy_min_size,
        entropy_sample_each=entropy_sample_each,
    )

    # -------------------------------------------------
    # 10. Idle Loop bis CTRL+C
    # -------------------------------------------------
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        log.info("Shutdown requested, cleaning up...")
        agent_control.stop_heartbeat()

        # Kafka Producer schließen
        try:
            asyncio.run_coroutine_threadsafe(producer.stop(), loop).result(timeout=2)
        except Exception as e:
            log.debug("Error stopping producer: %s", e)

        # Async Loop beenden
        loop.call_soon_threadsafe(loop.stop)
        loop_thread.join(timeout=2)


if __name__ == "__main__":
    main()
