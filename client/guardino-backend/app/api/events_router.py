# app/api/events_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..api.deps import get_db_session
from ..models.agent import AgentLifecycle, Event
from ..schemas.agent import AgentLifecycleOut, EventsGroupedOut, EventOut

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/lifecycle", response_model=list[AgentLifecycleOut])
async def list_lifecycle_events(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(
        select(AgentLifecycle).order_by(AgentLifecycle.ts.desc())
    )
    return result.scalars().all()


@router.get("/all", response_model=list[EventOut])
async def list_all_events(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(
        select(Event).order_by(Event.ts.desc())
    )
    return result.scalars().all()


@router.get("/grouped", response_model=EventsGroupedOut)
async def list_grouped_events(db: AsyncSession = Depends(get_db_session)):
    lifecycle_q = await db.execute(
        select(AgentLifecycle).order_by(AgentLifecycle.ts.desc())
    )
    events_q = await db.execute(
        select(Event).order_by(Event.ts.desc())
    )

    return EventsGroupedOut(
        lifecycle=lifecycle_q.scalars().all(),
        events=events_q.scalars().all(),
    )
