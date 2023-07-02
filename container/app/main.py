from typing import TypedDict, NotRequired
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from faker import Faker

app = FastAPI()


def get_random_name():
    faker = Faker()
    return faker.unique.first_name()


class Connection(TypedDict):
    user_name: str
    channel_name: str
    channel_password: NotRequired[str]


class ConnectionManager:
    def __init__(self):
        self.connections: Connection = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections[websocket] = {}
        self.connections[websocket]["user_name"] = get_random_name()
        self.connections[websocket]["channel_name"] = "1"
        text = f">> {self.connections[websocket]['user_name']} connected"
        await manager.send_to_user(text, websocket)
        await manager.send_to_channel(text, websocket)

    async def disconnect(self, websocket: WebSocket):
        text = f">> {self.connections[websocket]['user_name']} disconnected"
        await manager.send_to_channel(text, websocket)
        del self.connections[websocket]

    async def send_to_user(self, text: str, websocket: WebSocket):
        await websocket.send_text(text)

    async def send_to_channel(self, text: str, websocket: WebSocket):
        from_channel_name = self.connections[websocket]["channel_name"]
        for connection in self.connections:
            to_channel_name = self.connections[connection]["channel_name"]
            if from_channel_name is to_channel_name and connection is not websocket:
                await connection.send_text(text)


manager = ConnectionManager()


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            received_text = await websocket.receive_text()
            if received_text.startswith("/a"):
                text = f"-> {manager.connections[websocket]['user_name']} {received_text.split(' ', 1)[1]}"
                await manager.send_to_user(text, websocket)
                await manager.send_to_channel(text, websocket)
            elif received_text.startswith("/c"):
                channel_name = received_text.split()[1]
                await manager.send_to_channel(
                    f">> {manager.connections[websocket]['user_name']} leaves this channel",
                    websocket,
                )
                manager.connections[websocket]["channel_name"] = channel_name
                await manager.send_to_user(
                    f">> Channel changed to {channel_name}", websocket
                )
                await manager.send_to_channel(
                    f">> {manager.connections[websocket]['user_name']} joined this channel",
                    websocket,
                )
            elif received_text.startswith("/s"):
                for connection in manager.connections:
                    await manager.send_to_user(
                        f"{manager.connections[connection]['user_name']} @{manager.connections[connection]['channel_name']}",
                        websocket,
                    )
            elif received_text.startswith("/"):
                help_text = [
                    "/a <text> action something",
                    "/c <channel name> to change the channel",
                    "/s to show who's online",
                ]
                for text in help_text:
                    await manager.send_to_user(text, websocket)
            else:
                await manager.send_to_user(received_text, websocket)
                await manager.send_to_channel(
                    f"<{manager.connections[websocket]['user_name']}> {received_text}",
                    websocket,
                )
    except WebSocketDisconnect:
        await manager.disconnect(websocket)


app.mount("/", StaticFiles(directory="static", html=True), name="static")
