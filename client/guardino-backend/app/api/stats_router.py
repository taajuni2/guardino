# api/stats_router.py
from fastapi import APIRouter, Depends
from ..core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.stats_service import get_agent_stats, get_threat_stats
from ..schemas.stats import AgentStats, ThreatStats, StatsResponse

router = APIRouter(
    prefix="/stats",
    tags=["stats"],
)

@router.get("/health")
async def health():
    return {"status": "ok"}




@router.get("/total", response_model=StatsResponse)
async def get_stats(db: AsyncSession = Depends(get_db)):
    agent_raw = await get_agent_stats(db)
    threat_raw = await get_threat_stats(db)

    return StatsResponse(
        agents=AgentStats(**agent_raw),
        threats=ThreatStats(**threat_raw),
    )