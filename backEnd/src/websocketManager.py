from typing import Dict, List
from fastapi import WebSocket
from collections import defaultdict

class WebSocketManager:
    def __init__(self):
        self.active_lobbys : Dict[int, List[WebSocket]] = defaultdict(list)
    
    async def connect(self, lobby: int, websocket: WebSocket):
        await websocket.accept()
        self.active_lobbys[lobby].append(websocket)

    async def broadcast(self, lobby: int, message):
        connections = self.active_lobbys[lobby]
        for connection in connections:
            try:
                await connection.send_json(message)
            except:
                pass
        
    def disconnect(self, lobby: int, websocket: WebSocket):
        self.active_lobbys[lobby].remove(websocket)

