import math

class Cylinder:
    def __init__(self, r_i, r_a, conductivity = 1.0):
        self.r_i = r_i
        self.r_a = r_a
        self.conductivity = conductivity

    def temperature(self, T_i, T_a, r):
        return T_i + (T_a - T_i)*math.log(r/self.r_i)/math.log(self.r_a/self.r_i)

    def temperature_vec(self, T_i, T_a, r_vec):
        T = []

        for r in r_vec:
            T.append(self.temperature(T_i, T_a, r))

        return T

    def heat_flow(self, T_i, T_a):
        return self.conductivity*(T_a - T_i)/math.log(self.r_a/self.r_i)

if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt

    cyl = Cylinder(10e-3, 60e-3)
    r = np.linspace(10e-3, 60e-3, 100)
    T = cyl.temperature_vec(300, 1500, r)

    plt.plot(r, T)
    plt.show()
