#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 14.01.2026 10:13
@author: marcwelz
@project: mo25
"""

for x in range (2, 10):
    for y in range (1, 10):
        print(1, x, y, x, sep='')

print('----')

[[print(1, x, y, x, sep='') for y in range (1, 10)] for x in range (2, 10)]