# app/services/kafka_consumer.py
from __future__ import annotations

import asyncio
import json
import logging
from aiokafka import AIOKafkaConsumer
from ..core.config import settings
from ..core.database import SessionLocal
from ..services.agent_service import (
    handle_register,
    handle_heartbeat,
    handle_generic_event,
)

log = logging.getLogger("backend.kafka.consumer")


async def consume_agent_messages(stop_event: asyncio.Event | None = None):
    print("Starting Kafka consumer for agent messages...")
    consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC_AGENT_EVENTS,
        settings.KAFKA_TOPIC_AGENT_LIFECYCLE,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP,
        group_id=settings.KAFKA_GROUP_ID,
        enable_auto_commit=False,
        value_deserializer=lambda v: v.decode("utf-8"),
    )
    await consumer.start()
    try:
        while True:
            if stop_event and stop_event.is_set():
                break

            msgs = await consumer.getmany(timeout_ms=1000, max_records=50)
            for _tp, batch in msgs.items():
                for msg in batch:
                    try:
                        payload = json.loads(msg.value)
                    except json.JSONDecodeError:
                        log.warning("Could not decode message: %r", msg.value)
                        continue

                    msg_type = payload.get("type")
                    agent_id = payload.get("agent_id")

                    async with SessionLocal() as db:
                        try:
                            if msg_type == "register":
                                print("Handling register message")
                                await handle_register(db, payload)
                            elif msg_type == "heartbeat":
                                print("Handling register message")
                                await handle_heartbeat(db, payload)
                            else:
                                await handle_generic_event(db, payload)

                            # WICHTIG: async commit
                            await db.commit()
                            await consumer.commit()
                        except Exception:
                            log.exception("Error processing message from agent %s", agent_id)
                            await db.rollback()

                    # Offset erst nach erfolgreicher Verarbeitung committen


            await asyncio.sleep(0.1)
    finally:
        await consumer.stop()
