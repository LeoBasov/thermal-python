"""
"""

from enum import Enum

class Domain:
    def __init__(self):
        self.blocks = []
        self.nodes = []

    def add_block(self, min, max):
        self.check(min, max)

        id = len(self.blocks)
        block = Block(id, min, max)

        side1 = Side((max[0], min[1]), max)
        side2 = Side(max, (min[0], max[1]))
        side3 = Side((min[0], max[1]), min)
        side4 = Side(min, (max[0], min[1]))

        block.set_sides(side1, side2, side3, side4)

        self.blocks.append(block)

        return id

    def check(self, min, max):
        if min[0] < 0 or min[1] < 0:
            raise Exception('Domain', 'min[0]', min[0], 'min[1]', min[1])
        elif max[0] <= min[0] or max[1] <= min[1]:
            raise Exception('Domain', 'min[0]', min[0], 'min[1]', min[1], 'max[0]', max[0], 'max[1]', max[1])

class Node:
    def __init__(self):
        self.id = None
        self.pos_x = None
        self.pos_y = None
        self.type = None

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
    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.type = None
        self.value = None
        self.connection = None
