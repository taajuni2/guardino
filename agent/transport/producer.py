# agent/kafka/kafka_producer.py
from __future__ import annotations
from pathlib import Path
import json
import logging
import asyncio
from aiokafka import AIOKafkaProducer

logger = logging.getLogger("agent.producer")


class KafkaEventProducer:
    """
    Wrapper um AIOKafkaProducer.

    - async start()  -> stellt Verbindung zu Kafka her
    - async stop()   -> schließt Verbindung sauber
    - async send_event(event_dict) -> sendet ein Event ans Topic

    Diese Klasse macht KEIN eigenes Config-Loading.
    Du gibst broker, topic und optional logger von außen rein.
    """
    def __init__(self, broker: str, topic: str, log: logging.Logger | None = None):
        self._broker = broker
        self._topic = topic
        self.security_protocol="SSL",
        self.ssl_cafile="../certs/ca.crt",
        self._log = log or logger
        self._producer: AIOKafkaProducer | None = None

    async def start(self):
        """
        Initialisiert die Kafka-Verbindung einmal.
        Muss vor send_event() aufgerufen werden.
        """
        print("HALLOOOOOOO OVELLLLOOOOOO STARRTTTTTT")
        try:
            if self._producer is not None:
                return  # schon gestartet
            base_dir = Path(__file__).resolve().parent.parent.parent  # -> .../guardino
            ca_file = base_dir / "certs" / "ca.crt"

            self._log.info("Using CA file at: %s (exists=%s)", ca_file, ca_file.exists())
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self._broker,
                security_protocol="SSL",
                ssl_cafile=ca_file,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                acks="all",
            )
            await self._producer.start()
            logger.info("Producer gestartet")
            self._log.info("✅ Kafka producer connected to %s", self._broker)
        except Exception as e:
            logger.log("FEHLER AUFGETRETTEN %e ", e)
            self._producer = None
    async def stop(self):
        """
        Schließt die Verbindung wieder sauber.
        """
        if self._producer is not None:
            try:
                await self._producer.stop()
                self._log.info("🛑 Kafka producer stopped")
            finally:
                self._producer = None

    async def send_event(self, event: dict) -> bool:
        """
        Sendet ein einzelnes Event ins Topic.
        Gibt True zurück bei Erfolg, False bei Fehler.
        """
        if self._producer is None:
            # wurde start() vergessen oder Kafka nicht erreichbar?
            self._log.warning("Producer not started, can't send. Event=%s", event)
            return False

        try:
            await self._producer.send_and_wait(self._topic, event)
            self._log.debug("📤 Event -> Kafka topic '%s': %s", self._topic, event)
            return True
        except Exception as e:
            self._log.error("❌ Kafka send failed: %s", e)
            return False
