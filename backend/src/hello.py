from time import sleep

from observer import Events, MakeProducer


def main():
    produce = MakeProducer()
    while True:
        produce.send(Events.HELLO, "Hello")
        sleep(1)
