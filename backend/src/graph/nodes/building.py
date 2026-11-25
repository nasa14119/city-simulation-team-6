import numpy as np
from numpy._typing import NDArray

from .node_base import NodeBase, NodeTypes
from .street import Street


class Building(NodeBase):
    def __init__(self, cors) -> None:
        super().__init__(cors)
        self.door: Street | None = None

    def connect_graph(self, graph: NDArray[np.object_]):
        self.pick_random_door(graph)

    def pick_random_door(self, graph: NDArray[np.object_]):
        options = self.grab_surrounding(graph)
        options = [opt for opt in options if opt.type == NodeTypes.STREET]
        if not options:
            raise IndexError("No street arround building")
        self.add_door(np.random.choice(options))

    def add_door(self, door: Street):
        self.door = door

    @property
    def type(self):
        return NodeTypes.BUILDING
