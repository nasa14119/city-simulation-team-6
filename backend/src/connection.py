from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder

from observer import Observer, manager


class Connection(Observer):
    def __init__(self, ws: WebSocket):
        self.ws = ws
        manager.attachObserver(self)
        self.events = []

    async def send(self):
        if not self.events:
            return
        events = self.events[:]
        self.events = []
        for event in events:
            await self.ws.send_json(jsonable_encoder(event))

    def notify(self, event, payload):
        self.events.append({"event": event, "payload": payload})

    def disconect(self):
        manager.detattachObserver(self)
