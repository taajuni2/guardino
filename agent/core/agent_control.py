from __future__ import annotations

import json
import platform
import socket
import threading
import time
import uuid
import logging
from typing import Dict, Any, Optional


from .events import Event, now_iso
try:
    from kafka import KafkaProducer, KafkaConsumer
    _KAFKA_AVAILABLE = True
except Exception:
    _KAFKA_AVAILABLE = False

log = logging.getLogger("agent.control")


class AgentControl:


    def __init__(
        self,
        *,
            broker: str,
            control_topic: str,
            config: Dict[str, Any],
            agent_id: str,
            heartbeat_interval: int = 20,
            stdout_fallback: bool = False,
    ) -> None:
        self.broker = broker
        self.control_topic = control_topic,
        self.config = config
        self.agent_id = agent_id,
        self.heartbeat_interval = heartbeat_interval,
        self._stop = threading.Event()
        self.stdout_fallback = stdout_fallback or not _KAFKA_AVAILABLE or not broker

        self._producer: None
        self._consumer = None


        if not self.stdout_fallback:
            self._producer = KafkaProducer(
                bootstrap_servers=[broker],
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )

            self._consumer = KafkaConsumer(
                self.control_topic,
                bootstrap_servers=[broker],
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                enable_auto_commit=True,
                group_id=self.agent_id,
            )

# ------------------- Controlling funktionen--------------------------------------#
    def _send(self, key: Optional[str], payload: Dict[str, Any]) -> None:
        if self.stdout_fallback:
            log.info(f"stdout_fallback was executed")
            print(json.dumps({"topic": self.control_topic, "key": key, "value": payload}, ensure_ascii=False))
            return
        assert self._producer is not None
        log.info(f"_send is executed")
        self._producer.send(self.control_topic, key=key, value=payload)
        log.info(f"Successfully send to {self.control_topic}")
        self._producer.flush()

    def _poll_ack(self, timeout_s: int = 8) -> Optional[Dict[str, Any]]:
        if self.stdout_fallback:
            return
        log.info(f"_poll_ack is executed")
        end = time.time() + timeout_s
        while time.time() < end:
            polled = self._consumer.poll(timeout_ms=500)
            for _tp, records in polled.items():
                for item in records:
                    val = item.value
                    if isinstance(val, dict) and val.get("type") == "register_ack":
                        log.info(f"Successfully polled {val}")
                        return val

        return None




# ------------------- Calls funktionen--------------------------------------#

    def register(self) -> Optional[str]:
        systeminfo = {
            "os": platform.system(),
            "os_version": platform.version(),
            "arch": platform.machine(),
            "python_version": platform.python_version(),
            "agent_version": self.config.get("agent_version", "1.0.0"),
            "nonce": str(uuid.uuid4()),

        }

        message = Event.build(
            agent_id=self.agent_id,
            type_="register",
            severity="info",
            paths=[],
            summary="Agent autoregistration",
            metadata=systeminfo,
            raw={"ts": now_iso()},
        ).to_dict()

        key = self.agent_id or "__register__"
        self._send(key, message)
        print(f"Heartbeat1 : {self.heartbeat_interval}")
        ack = self._poll_ack(timeout_s=int(self.config["heartbeat_interval_s"]))
        print(f"Heartbeat2 : {self.heartbeat_interval}")
        if ack:
            self.agent_id = ack.get("agent_id", self.agent_id)
            log.info(f"REGISTERED agent {self.agent_id}")
        return self.agent_id

    def start_heartbeat(self) -> None:
        def run():
            while not self._stop.is_set():
                payload = Event.build(
                    agent_id=self.agent_id,
                    type_="heartbeat",
                    severity="info",
                    paths=[],
                    summary="Agent heartbeat",
                    metadata={"health:": {"system_status:": "ok"}},
                    raw={"ts": now_iso()},
                ).to_dict()
                print(f"Heartbeat: {self.heartbeat_interval}")
                self._send(self.agent_id, payload)
                self._stop.wait(self.heartbeat_interval)
        threading.Thread(target=run, daemon=True).start()


    def stop_heartbeat(self) -> None:
        self._stop.set()
        try:
            if self._consumer:
                self._consumer.close()
            if self._producer:
                self._producer.close()
        except Exception:
            pass


