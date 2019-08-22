import matplotlib.pyplot as plt
import numpy as np
import sys

class Visualizer:
    def __init__(self):
        pass

    def plot(self, domain):
        max = self.find_max(domain)
        matrix = np.zeros((max[0] + 1, max[1] + 1))

        for node in domain.nodes:
            matrix[node.pos[0]][node.pos[1]] = node.temperature

        plt.imshow(np.transpose(matrix), cmap='plasma', origin='lower')
        plt.colorbar()
        plt.show()

    def find_max(self, domain):
        max = [-sys.float_info.max, -sys.float_info.max]

        for node in domain.nodes:
            if node.pos[0] > max[0]:
                max[0] = node.pos[0]

            if node.pos[1] > max[1]:
                max[1] = node.pos[0]

        return max
