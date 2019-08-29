import sys

sys.path.append('../../.')

import thermal.domain
import thermal.solver
from cylinder_analytic import Cylinder
import numpy as np

def execute():
    radial_out_hot()

def radial_out_hot():
    RAD_FRAC = 0.01
    CELL_SIZE = 1e-3
    DIFF_MAX = 1.0e-5
    OUTTER_TEMP = 1500
    INNER_TEMP = 300

    domain = thermal.domain.Domain()
    sover = thermal.solver.Solver()
    cylinder = Cylinder(10*CELL_SIZE, 60*CELL_SIZE)

    #set blocks
    block = domain.add_block((0, 10), (50, 60), conductivity = 1, density = 1, heat_capacity = 1)

    #set sides housing_1
    domain.set_side(block, 0, thermal.domain.Type.NEUMANN, value = 0.)
    domain.set_side(block, 1, thermal.domain.Type.DIRICHLET, value = OUTTER_TEMP)
    domain.set_side(block, 2, thermal.domain.Type.NEUMANN, value = 0.0)
    domain.set_side(block, 3, thermal.domain.Type.DIRICHLET, value = INNER_TEMP)

    print(80*'-')
    print('ASSEMBLING NODES')
    domain.assemble_nodes()

    print(80*'-')
    print('ASSEMBLING NUMERICS')
    sover.assemble(domain, CELL_SIZE)
    print('SOLVING NUMERICS')
    sover.solve(DIFF_MAX, RAD_FRAC)
    sover.get_results(domain)

    (r_coord, values) = inter_r(domain, CELL_SIZE)
    ref = cylinder.temperature_vec(INNER_TEMP, OUTTER_TEMP, r_coord)

def find_max(domain):
    max = [-sys.float_info.max, -sys.float_info.max]

    for node in domain.nodes:
        if node.pos[0] > max[0]:
            max[0] = node.pos[0]

        if node.pos[1] > max[1]:
            max[1] = node.pos[1]

    return max

def find_min(domain):
    min = [sys.float_info.max, sys.float_info.max]

    for node in domain.nodes:
        if node.pos[0] < min[0]:
            min[0] = node.pos[0]

        if node.pos[1] < min[1]:
            min[1] = node.pos[1]

    return min

def inter_r(domain, cell_size):
    min = find_min(domain)
    max = find_max(domain)

    values = []
    r_coord = []

    for r in range(min[1], max[1] + 1):
        loc = []

        for node in domain.nodes:
            if node.pos[1] == r:
                loc.append(node.temperature)

        values.append(np.mean(loc))
        r_coord.append(cell_size*r)

    return (r_coord, values)
