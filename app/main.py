#!/usr/bin/env python3

import sys

sys.path.append('../.')

import thermal.domain

def main():
    print(80*'=')
    print('Thermal test')

    doain = thermal.domain.Domain()

    print(80*'=')

if __name__ == '__main__':
    main()
