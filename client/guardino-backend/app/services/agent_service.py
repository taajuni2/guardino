# app/services/agent_service.py
from datetime import datetime, timezone
import uuid
from sqlalchemy import select
from .. import models

def _now():
    return datetime.now(timezone.utc)


async def handle_register(db, msg: dict):
    agent_id = msg["agent_id"]
    meta = msg.get("metadata") or {}
    now = _now()

    # Agent holen (ASYNC!)
    result = await db.execute(
        select(models.Agent).where(models.Agent.agent_id == agent_id)
    )
    agent = result.scalars().first()

    if agent is None:
        agent = models.Agent(
            agent_id=agent_id,
            os=meta.get("os"),
            os_version=meta.get("os_version"),
            arch=meta.get("arch"),
            python_version=meta.get("python_version"),
            agent_version=meta.get("agent_version"),
            first_seen=now,
            last_seen=now,
            last_heartbeat=now,
            meta=meta,  # Spalte heißt bei uns meta
        )
        db.add(agent)
    else:
        agent.os = meta.get("os") or agent.os
        agent.os_version = meta.get("os_version") or agent.os_version
        agent.arch = meta.get("arch") or agent.arch
        agent.python_version = meta.get("python_version") or agent.python_version
        agent.agent_version = meta.get("agent_version") or agent.agent_version
        agent.last_seen = now
        agent.last_heartbeat = now
        agent.meta = meta or agent.meta

    # Lifecycle-Eintrag mitschreiben
    lifecycle = models.AgentLifecycle(
        id=uuid.UUID(msg["id"]) if msg.get("id") else uuid.uuid4(),
        ts=now,
        agent_id=agent_id,
        event_type="register",
        meta=meta,
    )
    db.add(lifecycle)
    # commit macht der Consumer


async def handle_heartbeat(db, msg: dict):
    agent_id = msg["agent_id"]
    now = _now()

    # Agent laden (ASYNC!)
    result = await db.execute(
        select(models.Agent).where(models.Agent.agent_id == agent_id)
    )
    agent = result.scalars().first()

    if not agent:
        # hier nur loggen/printen und KEIN lifecycle-Insert,
        # damit der FK nicht mehr knallt
        print(f"[WARN] Heartbeat von unbekanntem Agent empfangen: {agent_id} :: {msg}")
        return

    # wenn Agent existiert → updaten
    agent.last_seen = now
    agent.last_heartbeat = now

    lifecycle = models.AgentLifecycle(
        id=uuid.UUID(msg["id"]) if msg.get("id") else uuid.uuid4(),
        ts=now,
        agent_id=agent_id,
        event_type="heartbeat",
        summary="Heartbeat received",
        meta=msg.get("metadata") or {},
    )
    db.add(lifecycle)
    # commit macht der Consumer


async def handle_generic_event(db, msg: dict):
    now = _now()
    evt = models.Event(
        id=uuid.UUID(msg["id"]) if msg.get("id") else uuid.uuid4(),
        ts=msg.get("ts", now),
        agent_id=msg["agent_id"],
        event_type=msg.get("type"),
        severity=msg.get("severity"),
        summary=msg.get("summary"),
        paths=msg.get("paths") or [],
        meta=msg.get("metadata") or {},
        raw=msg.get("raw") or {},
    )
    db.add(evt)
    # commit macht der Consumer
