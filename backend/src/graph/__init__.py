from pathlib import Path
from typing import cast

import numpy as np

from .buildings import Buildings
from .nodes import NodeBase, node_factory

MAP_PATH = Path(__file__).parent / "map.txt"


class Graph:
    def __init__(self, path) -> None:
        self.graph = self.read_map_file(path)
        self.buildings = Buildings()
        self.__connect_graph()

    def read_map_file(self, path):
        with open(path, "r") as file:
            line = file.readline().strip()
            row, column = [int(num) for num in line.split(" ")]
            graph = np.empty((row, column), dtype=NodeBase)
            for j in range(row):
                line = file.readline().strip()
                for i, ch in enumerate(line):
                    Node = node_factory(ch)
                    node = Node((j, i))
                    graph[j][i] = node
        return graph

    def __connect_graph(self):
        graph = self.graph
        for node in graph.flat:
            node = cast(NodeBase, node)
            node.connect_graph(self)


graph = Graph(MAP_PATH)
