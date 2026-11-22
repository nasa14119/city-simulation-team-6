import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from config import CONFIG
from connection import Connection


def server():
    app = FastAPI()

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    @app.websocket("/ws")
    async def webSocket(websocket: WebSocket):
        await websocket.accept()
        con = Connection(websocket)
        try:
            await con.send()
        except WebSocketDisconnect:
            con.disconect()

    conf = uvicorn.Config(app, host="0.0.0.0", port=CONFIG["PORT"], log_level="info")
    server = uvicorn.Server(conf)
    server.run()
