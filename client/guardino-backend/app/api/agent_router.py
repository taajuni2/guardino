from typing import List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..api.deps import get_db_session, get_current_user
from ..models.agent import Agent
from ..schemas.agent import AgentOut
from ..services.websockets import agents_manager

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)

@router.get("/all" , response_model=List[AgentOut])
async def list_agents(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(select(Agent))
    agents = result.scalars().all()
    return agents


@router.websocket("/ws")
async def agents_ws(websocket: WebSocket):
    await agents_manager.connect(websocket)
    try:
        while True:
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        agents_manager.disconnect(websocket)
    except Exception as e:
        print(f"Error in Websocket: {e}")
        agents_manager.disconnect(websocket)