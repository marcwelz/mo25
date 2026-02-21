#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 05.12.2025 10:14
@author: marcwelz
@project: mo25
"""

x: str = ''

for i in range(1, 100):
    x += str(i)
    if not i == 99:
        x += ','

print(x)