from typing import TypedDict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from faker import Faker

app = FastAPI()


def get_random_name():
    faker = Faker()
    return faker.unique.first_name()


class Connection(TypedDict):
    websocket: WebSocket
    name: str
    channel: str


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[Connection] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[websocket] = get_random_name()
        text = f">> {self.active_connections[websocket]} connected"
        await manager.send_personal_message(text, websocket)
        await manager.send_channel_broadcast(text, websocket)

    async def disconnect(self, websocket: WebSocket):
        text = f">> {self.active_connections[websocket]} disconnected"
        await manager.send_channel_broadcast(text, websocket)
        del self.active_connections[websocket]

    async def send_personal_message(self, text: str, websocket: WebSocket):
        await websocket.send_text(text)

    async def send_server_broadcast(self, text: str):
        for connection in self.active_connections:
            await connection.send_text(text)

    async def send_channel_broadcast(self, text: str, websocket: WebSocket):
        for connection in self.active_connections:
            if connection is not websocket:
                await connection.send_text(text)


manager = ConnectionManager()


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            text = await websocket.receive_text()
            if text.startswith("/"):
                text = f"{manager.active_connections}"
                await manager.send_personal_message(text, websocket)
            else:
                await manager.send_personal_message(text, websocket)
                await manager.send_channel_broadcast(
                    f"<{manager.active_connections[websocket]}> {text}", websocket
                )
    except WebSocketDisconnect:
        await manager.disconnect(websocket)


app.mount("/", StaticFiles(directory="static", html=True), name="static")
