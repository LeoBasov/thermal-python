import numpy as np

class Solver:
    def __init__(self):
        self.matrix = None
        self.vector = None

    def assemble(self, domain, cell_size):
        self._assemble_vector(domain)
        self._assemble_matrix(domain, cell_size)

    def _assemble_vector(self, domain):
        self.vector = np.zeros(len(domain.nodes))

        for i in range(len(domain.nodes)):
            self.vector[i] = domain.nodes[i].temperature

    def _assemble_matrix(self, domain, cell_size):
        size = len(domain.nodes)
        self.matrix = np.zeros((size, size))

        for i in range(size):
            node = domain.nodes[i]

    def solve(self, diff_frac_max):
        itter = 0

        while True:
            itter += 1
            new_vector = np.matmul(self.matrix, self.vector)
            diffs = abs(new_vector - self.vector)
            self.vector = new_vector

            print("ITTERATION: {:5d}, MAX DIFF: {:5.5}".format(itter, max(diffs)), end="\r", flush=True)

            if max(diffs) < diff_frac_max:
                print("")
                break
