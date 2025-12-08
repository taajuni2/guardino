# schema/agent.py
from datetime import datetime
from typing import Any, List, Optional, Dict
from pydantic import BaseModel


class AgentBase(BaseModel):
    agent_id: str
    os: Optional[str] = None
    os_version: Optional[str] = None
    arch: Optional[str] = None
    python_version: Optional[str] = None
    agent_version: Optional[str] = None
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    last_heartbeat: Optional[datetime] = None
    meta: Optional[Dict[str, Any]] = None


class AgentOut(AgentBase):
    class Config:
        from_attributes = True  # SQLAlchemy → Pydantic


class EventOut(BaseModel):
    id: str
    ts: datetime
    agent_id: str
    event_type: str
    severity: Optional[str]
    summary: Optional[str]
    paths: Optional[List[str]]
    meta: Optional[Dict[str, Any]]
    raw: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True


class AgentLifecycleOut(BaseModel):
    id: str
    ts: datetime
    agent_id: str
    event_type: str
    meta: Optional[Dict[str, Any]]

class EventsGroupedOut(BaseModel):
    lifecycle: List[AgentLifecycleOut]
    events: List[EventOut]

    class Config:
        from_attributes = True
