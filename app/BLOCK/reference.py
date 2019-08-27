#!/usr/bin/env python3

import math

BOLTZMANN_CONST = 5.670374419e-8 #W m^−2⋅K^−4

def main():
    T_a = 372.29
    T_i = 1500
    T_b_i = 300
    k = 1
    r_i = 10e-3
    r_a = 60e-3

    print(80*'=')
    print('Radiation reference case')
    print('T_a:  ', T_a)
    print('T_i:  ', T_i)
    print('T_b_i:', T_b_i)
    print('k:    ', k)
    print('r_i:  ', r_i)
    print('r_a:  ', r_a)
    print(80*'-')

    q_cond_1 = q_cond(k, T_i, T_a, r_i, r_a)
    q_rad_1 = q_rad(T_a, T_b_i)

    T_i_new = comb(k, T_i, T_a, r_i, r_a, T_b_i)

    print("q_cond_1:", q_cond_1)
    print("q_rad_1: ", q_rad_1)
    print("T_i_new: ", T_i_new)

    print(80*'=')

def q_cond(k, T_i, T_a, r_i, r_a):
    return -k*(T_a - T_i)/math.log(r_a/r_i)

def q_rad(T_w, T_b):
    return BOLTZMANN_CONST*(math.pow(T_w, 4) - math.pow(T_b, 4))

def comb(k, T_i, T_a, r_i, r_a, T_b_i):
    return T_i - (k*BOLTZMANN_CONST/math.log(r_a/r_i))*(math.pow(T_a, 4) - math.pow(T_b_i, 4))

if __name__ == '__main__':
    main()
