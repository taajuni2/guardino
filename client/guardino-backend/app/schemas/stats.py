#  schemas/stats.py
from typing import Dict
from pydantic import BaseModel


class AgentStats(BaseModel):
    total_agents: int
    online_agents: int
    offline_agents: int


class ThreatStats(BaseModel):
    total_alerts: int
    alerts_last_24h: int
    alerts_by_severity: Dict[str, int]


class StatsResponse(BaseModel):
    agents: AgentStats
    threats: ThreatStats
