from typing import Optional

from pydantic import BaseModel
from sqlmodel import SQLModel, Field

class RamsomwareEvent(SQLModel, table=True):
    re_id: Optional[int] = Field(primary_key=True, index=True)
    agent_id: Optional[int] = Field(default=None, foreign_key="agent.agent_id")
    event_type: str
    file_path: str
    detected_at: str
    status: str