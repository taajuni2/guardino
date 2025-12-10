
from ..services.websockets import websocker_manager
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect


router = APIRouter(prefix="", tags=["ws"])

@router.websocket("/")
async def events_ws(websocket: WebSocket):
    await websocker_manager.connect(websocket)
    try:
        while True:
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        websocker_manager.disconnect(websocket)
    except Exception:
        websocker_manager.disconnect(websocket)