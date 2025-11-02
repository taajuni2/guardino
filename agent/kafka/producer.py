# agent/kafka/kafka_producer.py
import asyncio
import yaml
import json
import logging
from aiokafka import AIOKafkaProducer

logger = logging.getLogger("agent.producer")

def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

config = load_config()
KAFKA_BROKER = config["kafka"]["broker"]
TOPIC_EVENTS = config["kafka"]["topics"]["events"]


async def send_event(event: dict):
    """
    Sendet ein Event an Kafka (async).
    """
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        acks="all",
    )

    await producer.start()
    try:
        await producer.send_and_wait(TOPIC_EVENTS, event)
        logger.info(f"✅ Event sent to Kafka: {event}")
    except Exception as e:
        logger.error(f"❌ Kafka send failed: {e}")
    finally:
        await producer.stop()


# Test
if __name__ == "__main__":
    test_event = {
        "agent_id": "agent-001",
        "path": "/etc/passwd",
        "action": "modified",
        "timestamp": "2025-11-02T14:30:00Z",
    }
    asyncio.run(send_event(test_event))
