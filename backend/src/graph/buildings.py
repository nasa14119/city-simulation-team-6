from typing import cast

import numpy as np
from numpy.typing import ArrayLike

from .nodes import Building, Street


class SelectionErrorBuilding(Exception):
    def __init__(self, cause, buildings: list[Building]):
        super().__init__(f"Error trying to get path: {cause}")
        self.buildings = buildings


rng = np.random.default_rng()


class Buildings:
    def __init__(self):
        self.buildings: list[Building] = []

    def add_building(self, building: Building):
        self.buildings.append(building)

    def get_path(self) -> tuple[Street, Street]:
        """Get two random buildings streets to get to"""
        if len(self.buildings) < 2:
            raise SelectionErrorBuilding(
                "Not enogh buildings to select from", self.buildings
            )
        choices = rng.choice(cast(ArrayLike, self.buildings), size=2, replace=False)
        choices = [cast(Building, b) for b in choices]
        doors = [b.door for b in choices if b.door]
        if len(doors) < 2:
            raise SelectionErrorBuilding("Not all doors are set of buildings", choices)
        return (doors[0], doors[1])
