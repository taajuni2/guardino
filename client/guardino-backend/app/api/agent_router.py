from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..api.deps import get_db_session, get_current_user
from ..models.agent import Agent
from ..schemas.agent import AgentOut

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)

@router.get("/all" , response_model=List[AgentOut])
async def list_agents(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(Agent))
    agents = result.scalars().all()
    return agents