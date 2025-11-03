from __future__ import annotations

import asyncio
from aiokafka import AIOKafkaConsumer
from ..core.config import settings
from ..core.database import SessionLocal
# from app.schemas.file_event import FileEventIn  # später von dir
# from app.models.file_event import FileEvent    # später von dir

async def consume_file_events(stop_event: asyncio.Event | None = None):
    consumer = AIOKafkaConsumer(
        settings.KAFKA_TOPIC_AGENT_EVENTS,
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
                    raw_value = msg.value  # <- später in Pydantic parsen
                    # Beispiel: in DB schreiben
                    print(f"Kafka event vom backend {raw_value}")
                    async with SessionLocal() as db:
                        # deine Business-Logik hier
                        # await db.execute(...)
                        # await db.commit()
                        pass

                    await consumer.commit()
            await asyncio.sleep(0.1)
    finally:
        await consumer.stop()
