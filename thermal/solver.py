import numpy as np
import math
from .domain import Type
from .domain import SideType
import sys
from .rad_solver import calc_T

BOLTZMANN_CONST = 5.670374419e-8 #W m^−2⋅K^−4

class Solver:
    def __init__(self):
        self.matrix = None
        self.vector = None
        self.vector_add = None

        self.vector_rad = None
        self.vector_rad_index_pairs = None
        self.vector_background_temp_4 = None

        self.cell_size = None

    def assemble(self, domain, cell_size):
        self._assemble_vector(domain)
        self._assemble_matrix(domain, cell_size)
        self._assemble_vector_add(domain, cell_size)
        self._assemble_vector_rad(domain, cell_size)

        self.cell_size = cell_size

    def _assemble_vector(self, domain):
        self.vector = np.zeros(len(domain.nodes))

        for i in range(len(domain.nodes)):
            self.vector[i] = domain.nodes[i].temperature

    def _assemble_matrix(self, domain, cell_size):
        size = len(domain.nodes)
        self.matrix = np.zeros((size, size))

        for row in range(size):
            print("ROW {}/{}".format(row + 1, size), end="\r", flush=True)

            node = domain.nodes[row]
            pos = node.pos

            if node.type == Type.INSIDE:
                r_i = node.pos[1]*cell_size

                node_zp_r = domain.find_node((node.pos[0] + 1, node.pos[1]))
                node_zm_r = domain.find_node((node.pos[0] - 1, node.pos[1]))
                node_z_rp = domain.find_node((node.pos[0], node.pos[1] + 1))
                node_z_rm = domain.find_node((node.pos[0], node.pos[1] - 1))

                k_zp_r = node_zp_r[1].conductivity
                k_zm_r = node_zm_r[1].conductivity
                k_z_rp = node_z_rp[1].conductivity
                k_z_rm = node_z_rm[1].conductivity

                k = 0.25*(k_zp_r + k_zm_r) + 0.25*(k_z_rp + k_z_rm)

                self.matrix[row][node_zp_r[0]] = 0.25 + (k_zp_r - k_zm_r)/(16.0*k)
                self.matrix[row][node_zm_r[0]] = 0.25 - (k_zp_r - k_zm_r)/(16.0*k)
                self.matrix[row][node_z_rp[0]] = 0.25 + (k_z_rp - k_z_rm)/(16.0*k) + cell_size/(8.0*r_i)
                self.matrix[row][node_z_rm[0]] = 0.25 - (k_z_rp - k_z_rm)/(16.0*k) - cell_size/(8.0*r_i)

            elif node.type == Type.NEUMANN:
                if node.side_type == SideType.UP:
                    node_z_rm = domain.find_node((node.pos[0], node.pos[1] - 1))
                    self.matrix[row][node_z_rm[0]] = 1.0

                elif node.side_type == SideType.DOWN:
                    node_z_rp = domain.find_node((node.pos[0], node.pos[1] + 1))
                    self.matrix[row][node_z_rp[0]] = 1.0

                elif node.side_type == SideType.LEFT:
                    node_zp_r = domain.find_node((node.pos[0] + 1, node.pos[1]))
                    self.matrix[row][node_zp_r[0]] = 1.0

                elif node.side_type == SideType.RIGHT:
                    node_zm_r = domain.find_node((node.pos[0] - 1, node.pos[1]))
                    self.matrix[row][node_zm_r[0]] = 1.0

            elif node.type == Type.DIRICHLET:
                self.matrix[row][row] = 1.0

            elif node.type == Type.CONNECTION:
                r_i = node.pos[1]*cell_size

                node_zp_r = domain.find_node((node.pos[0] + 1, node.pos[1]))
                node_zm_r = domain.find_node((node.pos[0] - 1, node.pos[1]))
                node_z_rp = domain.find_node((node.pos[0], node.pos[1] + 1))
                node_z_rm = domain.find_node((node.pos[0], node.pos[1] - 1))

                if node_z_rp == None or node_z_rm == None:
                    self.matrix[row][node_zp_r[0]] = 0.5
                    self.matrix[row][node_zm_r[0]] = 0.5

                elif node_zp_r == None or node_zm_r == None:
                    self.matrix[row][node_z_rp[0]] = 0.5
                    self.matrix[row][node_z_rm[0]] = 0.5

                else:
                    k_zp_r = node_zp_r[1].conductivity
                    k_zm_r = node_zm_r[1].conductivity
                    k_z_rp = node_z_rp[1].conductivity
                    k_z_rm = node_z_rm[1].conductivity

                    k = 0.25*(k_zp_r + k_zm_r) + 0.25*(k_z_rp + k_z_rm)

                    self.matrix[row][node_zp_r[0]] = 0.25 + (k_zp_r - k_zm_r)/(16.0*k)
                    self.matrix[row][node_zm_r[0]] = 0.25 - (k_zp_r - k_zm_r)/(16.0*k)
                    self.matrix[row][node_z_rp[0]] = 0.25 + (k_z_rp - k_z_rm)/(16.0*k) + cell_size/(8.0*r_i)
                    self.matrix[row][node_z_rm[0]] = 0.25 - (k_z_rp - k_z_rm)/(16.0*k) - cell_size/(8.0*r_i)

        print("")

    def _assemble_vector_add(self, domain, cell_size):
        self.vector_add = np.zeros(len(domain.nodes))

        for i in range(len(domain.nodes)):
            if domain.nodes[i].type == Type.NEUMANN:
                self.vector_add[i] = domain.nodes[i].narmal_derivative*cell_size

    def _assemble_vector_rad(self, domain, cell_size):
        self.vector_rad = np.zeros(len(domain.nodes))
        self.vector_rad_index_pairs = [[False, 0, 0] for _ in range(len(domain.nodes))]
        self.vector_background_temp_4 = len(domain.nodes)*[None]

        for i in range(len(domain.nodes)):
            if domain.nodes[i].type == Type.BLACK_BODY:
                node = domain.nodes[i]

                node_zp_r = domain.find_node((node.pos[0] + 1, node.pos[1]))
                node_zm_r = domain.find_node((node.pos[0] - 1, node.pos[1]))
                node_z_rp = domain.find_node((node.pos[0], node.pos[1] + 1))
                node_z_rm = domain.find_node((node.pos[0], node.pos[1] - 1))

                self.vector_background_temp_4[i] = math.pow(domain.nodes[i].background_temp, 4)
                self.vector_rad_index_pairs[i][0] = True
                self.vector_rad_index_pairs[i][2] = domain.nodes[i].conductivity

                if domain.nodes[i].side_type == SideType.RIGHT:
                    self.vector_rad_index_pairs[i][1] = node_zm_r[0]
                elif domain.nodes[i].side_type == SideType.UP:
                    self.vector_rad_index_pairs[i][1] = node_z_rm[0]
                elif domain.nodes[i].side_type == SideType.LEFT:
                    self.vector_rad_index_pairs[i][1] = node_zp_r[0]
                elif domain.nodes[i].side_type == SideType.DOWN:
                    self.vector_rad_index_pairs[i][1] = node_z_rp[0]

    def solve(self, diff_frac_max, rad_frac):
        itter = 0
        diff_abs_old = sys.float_info.max

        while True:
            itter += 1

            self._get_rad_values(rad_frac)

            new_vector = np.matmul(self.matrix, self.vector) + self.vector_add + self.vector_rad
            diffs = abs(new_vector - self.vector)
            min_vec = 1 if min(self.vector) == 0.0 else min(self.vector)
            diff_abs = max(diffs)/min_vec
            self.vector = new_vector

            print("ITTERATION: {:5d}, MAX DIFF: {:5.5}".format(itter, diff_abs), end="\r", flush=True)

            if diff_abs < diff_frac_max:
                print("")
                break
            else:
                diff_abs_old = diff_abs

    def _get_rad_values(self, rad_frac):
        for i in range(len(self.vector_rad_index_pairs)):
            if self.vector_rad_index_pairs[i][0]:
                q = self.vector_rad_index_pairs[i][2]/(BOLTZMANN_CONST*self.cell_size )
                c = self.vector_background_temp_4[i] + q*self.vector[self.vector_rad_index_pairs[i][1]]
                T = calc_T(q, c)

                self.vector_rad[i] = T

    def get_results(self, domain):
        for i in range(len(domain.nodes)):
            domain.nodes[i].temperature = self.vector[i]
