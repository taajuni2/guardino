# app/models.py
from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from ..core.database import Base
import uuid
from datetime import datetime, timezone


def now_utc():
    return datetime.now(timezone.utc)

class Agent(Base):
    __tablename__ = "agents"

    agent_id = Column(String, primary_key=True)
    os = Column(String, nullable=True)
    os_version = Column(String, nullable=True)
    arch = Column(String, nullable=True)
    python_version = Column(String, nullable=True)
    agent_version = Column(String, nullable=True)
    first_seen = Column(DateTime(timezone=True), default=now_utc)
    last_seen = Column(DateTime(timezone=True), default=now_utc)
    last_heartbeat = Column(DateTime(timezone=True), default=now_utc)
    meta = Column(JSONB, nullable=True)

    lifecycle_entries = relationship("AgentLifecycle", back_populates="agent")
    events = relationship("Event", back_populates="agent")


class AgentLifecycle(Base):
    __tablename__ = "agent_lifecycle"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ts = Column(DateTime(timezone=True), default=now_utc, nullable=False)
    summary = Column(String, nullable=True)
    severity = Column(String, nullable=True)

    agent_id = Column(String, ForeignKey("agents.agent_id"), nullable=False)
    event_type = Column(String, nullable=False)  # register | heartbeat
    meta = Column(JSONB, nullable=True)

    agent = relationship("Agent", back_populates="lifecycle_entries")


class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ts = Column(DateTime(timezone=True), default=now_utc, nullable=False)
    agent_id = Column(String, ForeignKey("agents.agent_id"), nullable=False)
    event_type = Column(String, nullable=False)
    severity = Column(String, nullable=True)
    summary = Column(String, nullable=True)
    paths = Column(JSONB, nullable=True)
    meta = Column(JSONB, nullable=True)

    agent = relationship("Agent", back_populates="events")
