from typing import Optional

from sqlmodel import SQLModel, Field

class Heartbeat(SQLModel, table=True):
    hb_id: Optional[int] = Field(primary_key=True, index=True)
    agent_id: Optional[int] = Field(default=None, foreign_key="agent.agent_id")
    timestamp: str