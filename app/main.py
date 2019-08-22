#!/usr/bin/env python3

import sys

sys.path.append('../.')

import thermal.domain

def main():
    print(80*'=')
    print('Thermal test')

    doain = thermal.domain.Domain()

    doain.add_block((0, 0), (1, 1))
    #doain.add_block((-1, 0), (1, 1))
    #doain.add_block((0, 0), (0, 1))

    print(80*'=')

if __name__ == '__main__':
    main()
