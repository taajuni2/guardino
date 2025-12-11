# app/services/agent_service.py
from datetime import datetime, timezone
import uuid
from sqlalchemy import select
from ..models.agent import Agent, AgentLifecycle, Event
from ..schemas.agent import EventOut, AgentOut
from ..services.websockets import websocket_manager

def _now():
    return datetime.now(timezone.utc)


async def handle_register(db, msg: dict):
    agent_id = msg["agent_id"]
    meta = msg.get("meta") or {}
    now = _now()

    # Agent holen (ASYNC!)
    result = await db.execute(
        select(Agent).where(Agent.agent_id == agent_id)
    )
    agent = result.scalars().first()

    if agent is None:
        agent = Agent(
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
    evt = AgentLifecycle(
        id=uuid.UUID(msg["id"]) if msg.get("id") else uuid.uuid4(),
        ts=now,
        agent_id=agent_id,
        event_type="register",
        meta=meta,
    )
    db.add(evt)
    ws_agent = AgentOut.model_validate(agent)
    print(f"HANDLE REGISTER MODEL DUMP {agent}")
    await websocket_manager.broadcast_json({
        "type": "agent_register",
        "data": ws_agent.model_dump(mode="json")
    # commit macht der Consume
    })



async def handle_heartbeat(db, msg: dict):
    agent_id = msg["agent_id"]
    now = _now()

    # Agent laden (ASYNC!)
    result = await db.execute(
        select(Agent).where(Agent.agent_id == agent_id)
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

    evt = AgentLifecycle(
        id=uuid.UUID(msg["id"]) if msg.get("id") else uuid.uuid4(),
        ts=now,
        agent_id=agent_id,
        event_type="heartbeat",
        summary="Heartbeat received",
        severity="info",
        meta=msg.get("meta") or {},
    )
    db.add(evt)
    # commit macht der Consumer
    ws_event = AgentOut.model_validate(evt)
    await websocket_manager.broadcast_json({
        "type": "agent_heartbeat",
        "data": ws_event.model_dump()
})




async def handle_generic_event(db, msg: dict):
    now = _now()
    evt = Event(
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
    ws_event = EventOut.model_validate(evt)
    await websocket_manager.broadcast_json({
        "type": "event_new",
        "data": ws_event.model_dump()
    })
    # commit macht der Consumer
