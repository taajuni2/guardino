# app/api/events_router.py
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..api.deps import get_db_session
from ..models.agent import AgentLifecycle, Event
from ..schemas.agent import AgentLifecycleOut, EventsGroupedOut, EventOut
from ..services.websockets import events_manager

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/lifecycle", response_model=list[AgentLifecycleOut])
async def list_lifecycle_events(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(
        select(AgentLifecycle).order_by(AgentLifecycle.ts.desc())
    )
    rows = result.scalars().all()

    return [
        AgentLifecycleOut.model_validate(row, from_attributes=True)
        for row in rows
    ]


@router.get("/all", response_model=list[EventOut])
async def list_all_events(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(
        select(Event).order_by(Event.ts.desc())
    )
    rows = result.scalars().all()

    return [
        EventOut.model_validate(row, from_attributes=True)
        for row in rows
    ]


@router.get("/grouped", response_model=EventsGroupedOut)
async def list_grouped_events(db: AsyncSession = Depends(get_db_session)):
    lifecycle_q = await db.execute(
        select(AgentLifecycle).order_by(AgentLifecycle.ts.desc())
    )
    events_q = await db.execute(
        select(Event).order_by(Event.ts.desc())
    )

    lifecycle_rows = lifecycle_q.scalars().all()
    event_rows = events_q.scalars().all()

    lifecycle_out = [
        AgentLifecycleOut.model_validate(row, from_attributes=True)
        for row in lifecycle_rows
    ]
    events_out = [
        EventOut.model_validate(row, from_attributes=True)
        for row in event_rows
    ]

    return EventsGroupedOut(
        lifecycle=lifecycle_out,
        events=events_out,
    )


