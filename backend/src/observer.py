from abc import ABC, ABCMeta, abstractmethod
from enum import Enum


class Events(Enum):
    MAP_UPDATE = "MAP_UPDATE"
    HELLO = "HELLO"


class EventListener(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def notify(self, payload):
        pass


class Observer(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def notify(self, event: Events, payload):
        pass


class Manager:
    def __init__(self):
        self.listeners = {}
        self.observers = []
        for event in Events:
            self.listeners[event] = []

    def update(self, event: Events, payload):
        for li in self.listeners[event]:
            li.notify(payload)

        for ob in self.observers:
            ob.notify(event, payload)

    def on(self, event: Events, listener: EventListener):
        self.listeners[event].append(listener)

    def removeListener(self, event: Events, listener):
        self.listeners[event] = list(
            filter(lambda li: li != listener, self.listeners[event])
        )

    def attachObserver(self, ob: Observer):
        self.observers.append(ob)

    def detattachObserver(self, observer: Observer):
        self.observers = list(filter(lambda ob: ob != observer, self.observers))


class Producer:
    def __init__(self, manager: Manager):
        self.manager = manager

    def send(self, event: Events, payload):
        self.manager.update(event, payload)


manager = Manager()


def MakeProducer() -> Producer:
    return Producer(manager)
