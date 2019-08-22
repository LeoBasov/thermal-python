import numpy as np
from .domain import Type
from .domain import SideType

class Solver:
    def __init__(self):
        self.matrix = None
        self.vector = None
        self.vector_add = None

    def assemble(self, domain, cell_size):
        self._assemble_vector(domain)
        self._assemble_matrix(domain, cell_size)
        self._assemble_vector_add(domain, cell_size)

    def _assemble_vector(self, domain):
        self.vector = np.zeros(len(domain.nodes))

        for i in range(len(domain.nodes)):
            self.vector[i] = domain.nodes[i].temperature

    def _assemble_matrix(self, domain, cell_size):
        size = len(domain.nodes)
        self.matrix = np.zeros((size, size))

        for row in range(size):
            node = domain.nodes[row]
            pos = node.pos

            if node.type == Type.INSIDE:
                r_i = node.pos[1]*cell_size

                node_zp_r = domain.find_node((node.pos[0] + 1, node.pos[1]))
                node_zm_r = domain.find_node((node.pos[0] - 1, node.pos[1]))
                node_z_rp = domain.find_node((node.pos[0], node.pos[1] + 1))
                node_z_rm = domain.find_node((node.pos[0], node.pos[1] - 1))

                self.matrix[row][node_zp_r[0]] = 0.25
                self.matrix[row][node_zm_r[0]] = 0.25
                self.matrix[row][node_z_rp[0]] = 0.25 + cell_size/(8.0*r_i)
                self.matrix[row][node_z_rm[0]] = 0.25 - cell_size/(8.0*r_i)

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

    def _assemble_vector_add(self, domain, cell_size):
        self.vector_add = np.zeros(len(domain.nodes))

        for i in range(len(domain.nodes)):
            if domain.nodes[i].type == Type.NEUMANN:
                self.vector_add[i] = domain.nodes[i].normder*cell_size

    def solve(self, diff_frac_max):
        itter = 0

        while True:
            itter += 1
            new_vector = np.matmul(self.matrix, self.vector) + self.vector_add
            diffs = abs(new_vector - self.vector)
            diff_abs = max(diffs)/min(self.vector)
            self.vector = new_vector

            print("ITTERATION: {:5d}, MAX DIFF: {:5.5}".format(itter, diff_abs), end="\r", flush=True)

            if diff_abs < diff_frac_max:
                print("")
                break

    def get_results(self, domain):
        for i in range(len(domain.nodes)):
            domain.nodes[i].temperature = self.vector[i]
