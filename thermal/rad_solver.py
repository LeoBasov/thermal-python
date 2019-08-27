import math


def calc_T(q, c):
    T = 0.50000*math.sqrt(
    (3.4943*c)/math.pow((1.7321*math.sqrt(256*math.pow(c, 3) + 27*math.pow(q, 4)) + 9*math.pow(q, 2)), (1/3))
    #- 0.38157*(1.7321*math.sqrt(256*c^3 + 27*q^4) + 9*q^2)^(1/3)
    #+ (2*q)/math.sqrt(
    #0.38157*(1.7321*math.sqrt(256*c^3 + 27*q^4) + 9*q^2)^(1/3)
    #- (3.4943*c)/(1.7321*math.sqrt(256*c^3 + 27*q^4) + 9*q^2)^(1/3)
    #)
    )
    """- 0.50000*math.sqrt(
    0.38157*(1.7321*math.sqrt(256*c^3 + 27*q^4) + 9*q^2)^(1/3)
    - (3.4943*c)/(1.7321*math.sqrt(256*c^3 + 27*q^4) + 9*q^2)^(1/3)
    )"""

    return T

if __name__ == '__main__':
    BOLTZMANN_CONST = 5.670374419e-8
    dr = 0.0001
    k = 2000
    T_i = 1500
    T_b = 300

    q = k/(BOLTZMANN_CONST*dr)
    c = math.pow(T_b, 4) + q*T_i

    T = calc_T(q, c)

    print(T)
