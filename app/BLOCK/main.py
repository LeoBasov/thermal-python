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
    DIFF_MAX = 1e-4

    domain = thermal.domain.Domain()
    sover = thermal.solver.Solver()
    visualizer = thermal.visualizer.Visualizer()

    #set blocks
    block = domain.add_block((0, 10), (100, 100), conductivity = 1, density = 1, heat_capacity = 1)

    #set sides housing_1
    domain.set_side(block, 0, thermal.domain.Type.DIRICHLET, value = 10000.0)
    domain.set_side(block, 1, thermal.domain.Type.DIRICHLET, value = 0.0)
    domain.set_side(block, 2, thermal.domain.Type.DIRICHLET, value = 10000)
    domain.set_side(block, 3, thermal.domain.Type.DIRICHLET, value = 0.0)

    print(80*'-')
    print('ASSEMBLING NODES')
    domain.assemble_nodes()

    print(80*'-')
    print('ASSEMBLING NUMERICS')
    sover.assemble(domain, CELL_SIZE)
    print('SOLVING NUMERICS')
    sover.solve(DIFF_MAX)
    sover.get_results(domain)

    visualizer.plot(domain)

    print(80*'=')

if __name__ == '__main__':
    main()
