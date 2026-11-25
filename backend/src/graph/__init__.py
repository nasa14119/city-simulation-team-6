from pathlib import Path
from typing import cast

import numpy as np
from nodes import Direction, NodeBase, node_factory
from nodes.node_base import NodeTypes

MAP_PATH = Path(__file__).parent / "map.txt"


class Graph:
    def __init__(self, path) -> None:
        self.graph = self.read_map_file(path)
        self.__connect_graph()

    def read_map_file(self, path):
        with open(path, "r") as file:
            line = file.readline().strip()
            row, column = [int(num) for num in line.split(" ")]
            graph = np.empty((row, column), dtype=NodeBase)
            for j in range(row):
                line = file.readline().strip()
                for i, ch in enumerate(line):
                    curr = node_factory(ch)
                    graph[j][i] = curr((j, i))
        return graph

    def __connect_graph(self):
        graph = self.graph
        for cors, node in np.ndenumerate(graph):
            node = cast(NodeBase, node)
            node.connect_graph(graph)
        print(
            graph[0][3].grab_surrounding_directionated(
                graph, filters=[NodeTypes.STREET, NodeTypes.EMPTY]
            )
        )


graph = Graph(MAP_PATH)
