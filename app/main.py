#!/usr/bin/env python3

import sys

sys.path.append('../.')

import thermal.domain

def main():
    print(80*'=')
    print('Thermal test')

    doain = thermal.domain.Domain()

    #set blocks
    housing_1 = doain.add_block((0, 50), (100, 60), conductivity = 1, density = 1, heat_capacity = 1)
    housing_2 = doain.add_block((100, 50), (200, 60), conductivity = 1, density = 1, heat_capacity = 1)

    emitter = doain.add_block((100, 40), (200, 50), conductivity = 1, density = 1, heat_capacity = 1)

    orifice1 = doain.add_block((200, 50), (210, 60), conductivity = 1, density = 1, heat_capacity = 1)
    orifice2 = doain.add_block((200, 40), (210, 50), conductivity = 1, density = 1, heat_capacity = 1)
    orifice3 = doain.add_block((200, 30), (210, 40), conductivity = 1, density = 1, heat_capacity = 1)

    #set sides housing_1
    doain.set_side(housing_1, 0, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(housing_2, 2))
    doain.set_side(housing_1, 1, thermal.domain.Type.NEUMANN, value = 0.0)
    doain.set_side(housing_1, 2, thermal.domain.Type.DIRICHLET, value = 300)
    doain.set_side(housing_1, 3, thermal.domain.Type.NEUMANN, value = 1.0)

    #set sides housing_2
    doain.set_side(housing_2, 0, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(orifice1, 2))
    doain.set_side(housing_2, 1, thermal.domain.Type.NEUMANN, value = 0.0)
    doain.set_side(housing_2, 2, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(housing_1, 0))
    doain.set_side(housing_2, 3, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(emitter, 1))

    #set sides emitter
    doain.set_side(emitter, 0, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(orifice2, 2))
    doain.set_side(emitter, 1, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(housing_2, 3))
    doain.set_side(emitter, 2, thermal.domain.Type.NEUMANN, value = 1.0)
    doain.set_side(emitter, 3, thermal.domain.Type.NEUMANN, value = 1.0)

    #set sides orifice1
    doain.set_side(orifice1, 0, thermal.domain.Type.NEUMANN, value = 0.0)
    doain.set_side(orifice1, 1, thermal.domain.Type.NEUMANN, value = 0.0)
    doain.set_side(orifice1, 2, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(housing_2, 0))
    doain.set_side(orifice1, 3, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(orifice2, 1))

    #set sides orifice2
    doain.set_side(orifice2, 0, thermal.domain.Type.NEUMANN, value = 0.0)
    doain.set_side(orifice2, 1, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(orifice1, 3))
    doain.set_side(orifice2, 2, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(emitter, 0))
    doain.set_side(orifice2, 3, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(orifice3, 1))

    #set sides orifice3
    doain.set_side(orifice3, 0, thermal.domain.Type.NEUMANN, value = 0.0)
    doain.set_side(orifice3, 1, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(orifice2, 3))
    doain.set_side(orifice3, 2, thermal.domain.Type.NEUMANN, value = 1.0)
    doain.set_side(orifice3, 3, thermal.domain.Type.NEUMANN, value = 1.0)

    doain.assemble_nodes()

    for node in doain.nodes:
        print(node.temperature)

    print(80*'=')

if __name__ == '__main__':
    main()
