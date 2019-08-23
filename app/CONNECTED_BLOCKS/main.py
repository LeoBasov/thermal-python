#!/usr/bin/env python3

import sys

sys.path.append('../../.')

import thermal.domain
import thermal.visualizer
import thermal.solver

def main():
    print(80*'=')
    print('Thermal test')

    CELL_SIZE = 0.001
    DIFF_MAX = 1.0e-4

    domain = thermal.domain.Domain()
    sover = thermal.solver.Solver()
    visualizer = thermal.visualizer.Visualizer()

    #set blocks
    block1 = domain.add_block((0, 10), (50, 60), conductivity = 10, density = 1, heat_capacity = 1)
    block2 = domain.add_block((0, 60), (50, 110), conductivity = 1, density = 1, heat_capacity = 1)

    #set sides block1
    domain.set_side(block1, 0, thermal.domain.Type.NEUMANN, value = 0.0)
    domain.set_side(block1, 1, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(block2, 3))
    domain.set_side(block1, 2, thermal.domain.Type.NEUMANN, value = 0.0)
    domain.set_side(block1, 3, thermal.domain.Type.DIRICHLET, value = 100.0)

    #set sides block2
    domain.set_side(block2, 0, thermal.domain.Type.NEUMANN, value = 0.0)
    domain.set_side(block2, 1, thermal.domain.Type.DIRICHLET, value = 10000)
    domain.set_side(block2, 2, thermal.domain.Type.NEUMANN, value = 0.0)
    domain.set_side(block2, 3, thermal.domain.Type.CONNECTION, connection = thermal.domain.Connection(block1, 0))


    print(80*'-')
    print('ASSEMBLING NODES')
    domain.assemble_nodes()

    print(80*'-')
    print('ASSEMBLING NUMERICS')
    sover.assemble(domain, CELL_SIZE)
    print('SOLVING NUMERICS')
    sover.solve(DIFF_MAX)
    sover.get_results(domain)

    visualizer.plot(domain, CELL_SIZE)
    visualizer.plot_inter_r(domain, CELL_SIZE)
    visualizer.plot_inter_z(domain, CELL_SIZE)

    print(80*'=')

if __name__ == '__main__':
    main()
