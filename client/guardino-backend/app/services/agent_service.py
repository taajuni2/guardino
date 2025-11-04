# app/services/agent_service.py
from datetime import datetime, timezone
from sqlalchemy.exc import NoResultFound
from ..models.agent import Agent, Event, AgentLifecycle


def _now():
    return datetime.now(timezone.utc)

def handle_register(db, msg: dict):
    agent_id = msg["agent_id"]
    meta = msg.get("metadata", {})
    ts = msg.get("timestamp") or msg.get("raw", {}).get("ts") or _now().isoformat()

    # Agent upsert
    agent = db.get(Agent, agent_id)
    if agent is None:
        agent = Agent(
            agent_id=agent_id,
            os=meta.get("os"),
            os_version=meta.get("os_version"),
            arch=meta.get("arch"),
            python_version=meta.get("python_version"),
            agent_version=meta.get("agent_version"),
            first_seen=_now(),
            last_seen=_now(),
            last_heartbeat=_now(),
            metadata=meta,
        )
        db.add(agent)
    else:
        # Update bekannte Felder
        agent.os = meta.get("os") or agent.os
        agent.os_version = meta.get("os_version") or agent.os_version
        agent.arch = meta.get("arch") or agent.arch
        agent.python_version = meta.get("python_version") or agent.python_version
        agent.agent_version = meta.get("agent_version") or agent.agent_version
        agent.last_seen = _now()
        agent.last_heartbeat = _now()
        agent.meta = meta or agent.metadata

    # Lifecycle-Eintrag
    lifecycle = AgentLifecycle(
        id=msg.get("id"),
        ts=_now(),
        agent_id=agent_id,
        event_type="register",
        meta=meta,
    )
    db.add(lifecycle)



def handle_heartbeat(db, msg: dict):
    agent_id = msg["agent_id"]
    agent = db.get(Agent, agent_id)
    if agent:
        agent.last_seen = _now()
        agent.last_heartbeat = _now()
        db.add(AgentLifecycle(
            id=msg.get("id"),
            ts=_now(),
            agent_id=agent_id,
            event_type="heartbeat",
            meta=msg.get("metadata") or {},
        ))


def handle_generic_event(db, msg: dict):
    evt = Event(
        id=msg.get("id"),
        ts=msg.get("timestamp", _now()),
        agent_id=msg["agent_id"],
        event_type=msg.get("type"),
        severity=msg.get("severity"),
        summary=msg.get("summary"),
        paths=msg.get("paths") or [],
        meta=msg.get("metadata") or {},
        raw=msg.get("raw") or {},
    )
    db.add(evt)
