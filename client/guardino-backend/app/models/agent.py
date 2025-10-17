from typing import Optional

from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class Agent(SQLModel, table=True):
    agent_id: Optional[int] = Field(primary_key=True, index=True)
    name: str
    ip_address: str
    os: str
    last_heartbeat: str
    status: str