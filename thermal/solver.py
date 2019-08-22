import numpy as np

class Solver:
    def __init__(self):
        self.matrix = None
        self.vector = None

    def assemble(self, domain, cell_size):
        size = len(domain.nodes)

        self.vector = np.zeros(size)
        self.matrix = np.zeros((size, size))

        self._assemble_vector(domain)
        self._assemble_matrix(domain, cell_size)

    def _assemble_vector(self, domain):
        for i in range(len(domain.nodes)):
            self.vector[i] = domain.nodes[i].temperature

    def _assemble_matrix(self, domain, cell_size):
        pass

    def solve(self, diff_frac_max):
        pass
