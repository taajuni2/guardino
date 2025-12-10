# services/websockets.py
from typing import List
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_json(self, message: dict):
        print("Broadcast Json happend")
        dead = []
        for ws in self.active_connections:
            try:
                await ws.send_json(message)
                print(f"Successfully to send message to websocket {message}" )
            except WebSocketDisconnect:
                print("Failed to send message to websocket")
                dead.append(ws)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)


agents_manager = ConnectionManager()
events_manager = ConnectionManager()
