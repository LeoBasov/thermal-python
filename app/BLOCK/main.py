#!/usr/bin/env python3

import sys

sys.path.append('../../.')

import thermal.domain
import thermal.visualizer
import thermal.solver

def main():
    print(80*'=')
    print('Thermal test')

    RAD_FRAC = 0.01
    CELL_SIZE = 1e-3
    DIFF_MAX = 1.0e-6

    domain = thermal.domain.Domain()
    sover = thermal.solver.Solver()
    visualizer = thermal.visualizer.Visualizer()

    #set blocks
    block = domain.add_block((0, 10), (50, 60), conductivity = 1, density = 1, heat_capacity = 1)

    #set sides housing_1
    domain.set_side(block, 0, thermal.domain.Type.NEUMANN, value = 0.)
    domain.set_side(block, 1, thermal.domain.Type.BLACK_BODY, value = 300.0)
    domain.set_side(block, 2, thermal.domain.Type.NEUMANN, value = 0.0)
    domain.set_side(block, 3, thermal.domain.Type.DIRICHLET, value = 1500.0)

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
    visualizer.plot_inter_r(domain, CELL_SIZE)
    visualizer.plot_inter_z(domain, CELL_SIZE)

    print(80*'=')

if __name__ == '__main__':
    main()
