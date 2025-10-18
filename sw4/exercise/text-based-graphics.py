#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 18.10.2025 11:06
@author: marcwelz
@project: mo25
"""

t: str = '*'

amount_input: int = int(input('Enter amount: '))

range_max_top: int = (amount_input // 2) + 1

for x in range(1, range_max_top):
    print(t * x)

for x in range(range_max_top, 0, -1):
    print(x * t)
