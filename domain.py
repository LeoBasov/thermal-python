"""
"""

from enum import Enum

class Domain:
    def __init__(self):
        self.blocks = []
        self.node_blocks = []

class Type(Enum):
    INSIDE = 0
    CONNECTION = 1
    DIRICHLET = 2
    NEUMANN = 3

class Block:
    """
    Block class
    Sides are always counted strating from the far right, counter clock wise.

    """

    def __init__(self, id, min, max):
        self.id = id
        self.min = min
        self.max = max
        self.sides = (None, None, None, None)

    def set_sides(self, side1, side2, side3, side4):
        self.sides = (side1, side2, side3, side4)

class Connection:
    def __init__(self, block_id, side_id):
        self.block_id = block_id
        self.side_id = side_id

class Side:
    def __init__(self, id, type, value = None):
        self.id = id
        self.type = type
        self.value = value
        self.connections = []
