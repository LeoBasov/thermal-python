"""
"""

from enum import Enum

class Block:
    """
    Block class
    Sides are always counted strating from the far right, counter clock wise.

    """

    def __init__(self, id):
        self.id = id
        self.sides = (None, None, None, None)

    def set_sides(self, side1, side2, side3, side4):
        self.sides = (side1, side2, side3, side4)

class BCType(Enum):
    CONNECTION = 0
    DIRICHLET = 1
    NEUMANN = 2

class Connection:
    def __init__(self, block_id, side_id):
        self.block_id = block_id
        self.side_id = side_id

class Side:
    def __init__(self, id, type, value = None):
        self.id = id
        self.type = None
        self.value = None
        self.connections = []
