
from ..services.websockets import events_manager
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect


router = APIRouter(prefix="", tags=["ws"])

@router.websocket("/ws")
async def events_ws(websocket: WebSocket):
    await events_manager.connect(websocket)
    try:
        while True:
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        events_manager.disconnect(websocket)
    except Exception:
        events_manager.disconnect(websocket)