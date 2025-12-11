
from ..services.websockets import websocket_manager
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect


router = APIRouter(prefix="", tags=["ws"])

@router.websocket("/")
async def events_ws(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
    except Exception:
        websocket_manager.disconnect(websocket)