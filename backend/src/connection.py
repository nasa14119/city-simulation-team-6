from asyncio import Queue

from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder

from observer import Observer, manager


class Connection(Observer):
    def __init__(self, ws: WebSocket):
        self.ws = ws
        manager.attachObserver(self)
        self.events = Queue()

    async def send(self):
        while True:
            event = await self.events.get()
            await self.ws.send_json(jsonable_encoder(event))

    def notify(self, event, payload):
        self.events.put_nowait({"event": event, "payload": payload})

    def disconect(self):
        manager.detattachObserver(self)
