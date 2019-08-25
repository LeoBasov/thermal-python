"""
"""

import sys
from enum import Enum

class Domain:
    def __init__(self):
        self.blocks = []
        self.nodes = []

    def add_block(self, min, max, conductivity, density, heat_capacity):
        self.check(min, max)

        id = len(self.blocks)
        block = Block(id, min, max, conductivity, density, heat_capacity)

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

    def set_side(self, block_id, side_id, type, value = None, connection = None):
        self.blocks[block_id].sides[side_id].type = type
        self.blocks[block_id].sides[side_id].value = value
        self.blocks[block_id].sides[side_id].connection = connection

    def assemble_nodes(self):
        for block in self.blocks:
            for z in range(block.min[0], block.max[0] + 1):
                for r in range(block.min[1], block.max[1] + 1):
                    pos = (z, r)
                    conductivity = block.conductivity
                    density = block.density
                    heat_capacity = block.heat_capacity

                    type = None
                    side_type = None
                    temperature = None
                    narmal_derivative = None
                    background_temp = None

                    if z == block.max[0]:
                        side_type = SideType.RIGHT
                        (type, temperature, narmal_derivative, background_temp) = self._get_values(block.sides[0])
                    elif r == block.max[1]:
                        side_type = SideType.UP
                        (type, temperature, narmal_derivative, background_temp) = self._get_values(block.sides[1])
                    elif z == block.min[0]:
                        side_type = SideType.LEFT
                        (type, temperature, narmal_derivative, background_temp) = self._get_values(block.sides[2])
                    elif r == block.min[1]:
                        side_type = SideType.DOWN
                        (type, temperature, narmal_derivative, background_temp) = self._get_values(block.sides[3])
                    else:
                        type = Type.INSIDE

                    if type != Type.CONNECTION or not self._nodes_exists(pos):
                        node = Node(type, pos, temperature, conductivity, density, heat_capacity, side_type, narmal_derivative, background_temp)

                        self.nodes.append(node)

        self._set_temperatures()

    def find_node(self, pos):
        for i in range(len(self.nodes)):
            if self.nodes[i].pos == pos:
                return (i, self.nodes[i])

    def _get_values(self, side):
        type = side.type
        temp = None
        narmal_derivative = None
        background_temp = None

        if type == Type.DIRICHLET:
            temp = side.value
        elif type == Type.NEUMANN:
            narmal_derivative = side.value
        elif type == Type.BLACK_BODY:
            background_temp = side.value

        return (type, temp, narmal_derivative, background_temp)

    def _nodes_exists(self, pos):
        for node in self.nodes:
            if node.pos == pos:
                return True

        return False

    def _set_temperatures(self):
        max = -sys.float_info.max
        min =  sys.float_info.max
        temperature = None

        for node in self.nodes:
            if node.type == Type.DIRICHLET:
                if node.temperature > max:
                    max = node.temperature

                if node.temperature < min:
                    min = node.temperature

        temperature = 0.5*(min + max)

        for node in self.nodes:
            if node.type != Type.DIRICHLET:
                 node.temperature = temperature

class Node:
    def __init__(self, type, pos, temperature, conductivity, density, heat_capacity, side_type, narmal_derivative, background_temp):
        self.type = type
        self.pos = pos
        self.temperature = temperature
        self.conductivity = conductivity
        self.density = density
        self.heat_capacity = heat_capacity

        self.side_type = side_type
        self.narmal_derivative = narmal_derivative #dT/dn
        self.background_temp = background_temp

class Type(Enum):
    INSIDE = 0
    CONNECTION = 1
    DIRICHLET = 2
    NEUMANN = 3
    BLACK_BODY = 4

class SideType(Enum):
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3

class Block:
    """
    Block class
    Sides are always counted strating from the far right, counter clock wise.

    """

    def __init__(self, id, min, max, conductivity, density, heat_capacity):
        self.id = id
        self.min = min
        self.max = max
        self.sides = (None, None, None, None)
        self.conductivity = conductivity
        self.density = density
        self.heat_capacity = heat_capacity

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
