#!/usr/bin/env python3

import sys

sys.path.append('../../.')

import thermal.domain
import thermal.visualizer
import thermal.solver

def main():
    print(80*'=')
    print('Thermal test')

    RAD_FRAC = 0.0001
    CELL_SIZE = 0.0001
    DIFF_MAX = 1e-4

    domain = thermal.domain.Domain()
    sover = thermal.solver.Solver()
    visualizer = thermal.visualizer.Visualizer()

    #set blocks
    housing_1 = domain.add_block((0, 50), (100, 60), conductivity = 205, density = 1, heat_capacity = 1)
    housing_2 = domain.add_block((100, 50), (400, 60), conductivity = 205, density = 1, heat_capacity = 1)

    emitter = domain.add_block((100, 20), (400, 50), conductivity = 50, density = 1, heat_capacity = 1)

    orifice1 = domain.add_block((400, 50), (410, 60), conductivity = 205, density = 1, heat_capacity = 1)
    orifice2 = domain.add_block((400, 20), (410, 50), conductivity = 205, density = 1, heat_capacity = 1)
    orifice3 = domain.add_block((400, 10), (410, 20), conductivity = 205, density = 1, heat_capacity = 1)

    #set sides housing_1
    domain.set_side(housing_1, 0, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(housing_2, 2))
    domain.set_side(housing_1, 1, thermal.domain.Type.BLACK_BODY, value = 4.0)
    domain.set_side(housing_1, 2, thermal.domain.Type.DIRICHLET, value = 300)
    domain.set_side(housing_1, 3, thermal.domain.Type.BLACK_BODY, value = 500.0)

    #set sides housing_2
    domain.set_side(housing_2, 0, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(orifice1, 2))
    domain.set_side(housing_2, 1, thermal.domain.Type.BLACK_BODY, value = 4.0)
    domain.set_side(housing_2, 2, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(housing_1, 0))
    domain.set_side(housing_2, 3, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(emitter, 1))

    #set sides emitter
    domain.set_side(emitter, 0, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(orifice2, 2))
    domain.set_side(emitter, 1, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(housing_2, 3))
    domain.set_side(emitter, 2, thermal.domain.Type.BLACK_BODY, value = 500.0)
    domain.set_side(emitter, 3, thermal.domain.Type.DIRICHLET, value = 1500.0)

    #set sides orifice1
    domain.set_side(orifice1, 0, thermal.domain.Type.BLACK_BODY, value = 4.0)
    domain.set_side(orifice1, 1, thermal.domain.Type.BLACK_BODY, value = 4.0)
    domain.set_side(orifice1, 2, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(housing_2, 0))
    domain.set_side(orifice1, 3, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(orifice2, 1))

    #set sides orifice2
    domain.set_side(orifice2, 0, thermal.domain.Type.BLACK_BODY, value = 4.0)
    domain.set_side(orifice2, 1, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(orifice1, 3))
    domain.set_side(orifice2, 2, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(emitter, 0))
    domain.set_side(orifice2, 3, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(orifice3, 1))

    #set sides orifice3
    domain.set_side(orifice3, 0, thermal.domain.Type.BLACK_BODY, value = 4.0)
    domain.set_side(orifice3, 1, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(orifice2, 3))
    domain.set_side(orifice3, 2, thermal.domain.Type.BLACK_BODY, value = 1500.0)
    domain.set_side(orifice3, 3, thermal.domain.Type.BLACK_BODY, value = 1500.0)

    print(80*'-')
    print('ASSEMBLING NODES')
    domain.assemble_nodes()

    print(80*'-')
    print('ASSEMBLING NUMERICS')
    sover.assemble(domain, CELL_SIZE)
    print('SOLVING NUMERICS')
    sover.solve(DIFF_MAX, RAD_FRAC)
    sover.get_results(domain)

    visualizer.plot(domain, CELL_SIZE)

    print(80*'=')

if __name__ == '__main__':
    main()
