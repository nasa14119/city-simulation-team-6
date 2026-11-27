from collections.abc import Callable

from .building import Building
from .node_base import Direction, Empty, NodeBase
from .street import DIRECTIONS, Street

NodeFactory = Callable[[tuple[int, int]], NodeBase]
__all__ = ["Building", "Direction", "Empty", "NodeBase", "Street"]


def node_factory(type: str) -> NodeFactory:
    if type in DIRECTIONS:
        return lambda cors: Street(cors, type)
    if type == "#":
        return lambda cors: Empty(cors)
    if type == "B":
        return lambda cors: Building(cors)
    raise TypeError("No case was match")
