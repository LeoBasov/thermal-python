import matplotlib.pyplot as plt
import numpy as np
import sys

class Visualizer:
    def __init__(self):
        pass

    def plot(self, domain, cell_size):
        max = self.find_max(domain)
        matrix = np.zeros((max[0] + 1, max[1] + 1))

        for node in domain.nodes:
            matrix[node.pos[0]][node.pos[1]] = node.temperature

        plt.imshow(np.transpose(matrix), cmap='jet', origin='lower', interpolation='none')
        plt.xlabel('z-coord * ' + str(cell_size) + ' m')
        plt.ylabel('r-coord * ' + str(cell_size) + ' m')
        plt.colorbar()
        plt.show()

    def find_max(self, domain):
        max = [-sys.float_info.max, -sys.float_info.max]

        for node in domain.nodes:
            if node.pos[0] > max[0]:
                max[0] = node.pos[0]

            if node.pos[1] > max[1]:
                max[1] = node.pos[1]

        return max

    def find_min(self, domain):
        min = [sys.float_info.max, sys.float_info.max]

        for node in domain.nodes:
            if node.pos[0] < min[0]:
                min[0] = node.pos[0]

            if node.pos[1] < min[1]:
                min[1] = node.pos[1]

        return min

    def plot_inter_r(self, domain, cell_size):
        min = self.find_min(domain)
        max = self.find_max(domain)

        values = []
        r_coord = []

        for r in range(min[1], max[1] + 1):
            loc = []

            for node in domain.nodes:
                if node.pos[1] == r:
                    loc.append(node.temperature)

            values.append(np.mean(loc))
            r_coord.append(cell_size*r)

        plt.plot(r_coord, values)
        plt.xlabel('r-coord')
        plt.ylabel('Temperature [K]')
        plt.show()

    def plot_inter_z(self, domain, cell_size):
        min = self.find_min(domain)
        max = self.find_max(domain)

        values = []
        z_coord = []

        for z in range(min[0], max[0] + 1):
            loc = []

            for node in domain.nodes:
                if node.pos[0] == z:
                    loc.append(node.temperature)

            values.append(np.mean(loc))
            z_coord.append(cell_size*z)

        plt.plot(z_coord, values)
        plt.xlabel('z-coord')
        plt.ylabel('Temperature [K]')
        plt.show()
