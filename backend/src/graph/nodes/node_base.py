from abc import ABC, abstractmethod
from enum import Enum

import numpy as np
from numpy.typing import NDArray


class Direction(Enum):
    Left = "left"
    Right = "right"
    Up = "up"
    Down = "down"


class NodeTypes(Enum):
    EMPTY = "empty"
    STREET = "street"
    BUILDING = "building"


class NodeBase(ABC):
    def __init__(self, cors: tuple[int, int]):
        self._cors = cors

    @property
    def cors(self) -> tuple[int, int]:
        return self._cors

    @property
    @abstractmethod
    def type(self) -> NodeTypes:
        pass

    @abstractmethod
    def connect_graph(self, graph: NDArray[np.object_]) -> None:
        pass

    def grab_surrounding(self, graph: NDArray[np.object_]):
        options = []
        y, x = self.cors
        if x > 0:
            options.append(graph[y][x - 1])
        if x < graph.shape[1] - 1:
            options.append(graph[y][x + 1])
        if y > 0:
            options.append(graph[y - 1][x])
        if y < graph.shape[0] - 1:
            options.append(graph[y + 1][x])
        return options

    def grab_surrounding_directionated(
        self,
        graph: NDArray[np.object_],
        filter: None | NodeTypes = None,
        filters: None | list[NodeTypes] = None,
    ):
        options: dict[Direction, None | NodeBase] = {
            Direction.Left: None,
            Direction.Right: None,
            Direction.Up: None,
            Direction.Down: None,
        }
        y, x = self.cors
        if x > 0:
            options[Direction.Left] = graph[y][x - 1]
        if x < graph.shape[1] - 1:
            options[Direction.Right] = graph[y][x + 1]
        if y > 0:
            options[Direction.Up] = graph[y - 1][x]
        if y < graph.shape[0] - 1:
            options[Direction.Down] = graph[y + 1][x]
        if filter:
            for key, value in options.items():
                if value and value.type != filter:
                    options[key] = None
        if not filters:
            filters = []
        if filters:
            for key, value in options.items():
                if value and value.type not in filters:
                    options[key] = None
        return options


class Empty(NodeBase):
    @property
    def type(self):
        return NodeTypes.EMPTY

    def connect_graph(self, graph: NDArray[np.object_]) -> None:
        return super().connect_graph(graph)
