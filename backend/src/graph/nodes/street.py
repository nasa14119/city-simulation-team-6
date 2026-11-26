from typing import cast

from .node_base import Direction, NodeBase, NodeTypes

DIRECTIONS = {
    ">": Direction.Right,
    "<": Direction.Left,
    "∧": Direction.Up,
    "∨": Direction.Down,
}

OPPOSITES = {
    Direction.Right: Direction.Left,
    Direction.Left: Direction.Right,
    Direction.Down: Direction.Up,
    Direction.Up: Direction.Down,
}

BLOCKED_PENALTY = lambda s=None: 20


class Street(NodeBase):
    def __init__(self, cors, direction):
        super().__init__(cors)
        self.direction: Direction = DIRECTIONS[direction]
        self.vehicles = []
        self.conections: dict[Direction, Street] = {}
        self.isBlocked = False
        self.weight = 1

    def calc_weight(self):
        hasVehicle = 0 if self.isFree() else 1
        penalty = 0 if not self.isBlocked else BLOCKED_PENALTY()
        self.weight = 1 + hasVehicle + penalty
        if self.canContinue():
            self.weight += self.next_in_direction().calc_weight()
        return self.weight

    def next_in_direction(self):
        return self.conections[self.direction]

    def connect(self, con: "Street"):
        self.conections[con.direction] = con

    def canContinue(self):
        return self.direction in self.conections

    def canTransit(self):
        return not self.isBlocked and self.isFree()

    def isFree(self):
        return not self.vehicles

    def leave(self, vehicle):
        self.vehicles = [v for v in self.vehicles if vehicle != v]

    def connect_graph(self, graph) -> None:
        pending = self.grab_surrounding_directionated(graph, filter=self.type)
        opposite = OPPOSITES[self.direction]
        for key, node in pending.items():
            node = cast(Street, node)
            if not node:
                continue
            if key == opposite and node.direction == self.direction:
                continue
            if node:
                self.conections[key] = node

    @property
    def type(self):
        return NodeTypes.STREET
