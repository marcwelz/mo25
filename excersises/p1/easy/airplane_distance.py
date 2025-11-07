#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 04.10.2025 10:48
@author: marcwelz
@project: mo25
"""
import math

x1: int = int(input('x pos airplane 1'))
y1: int = int(input('y pos airplane 1'))
x2: int = int(input('x pos airplane 2'))
y2: int = int(input('y pos airplane 2'))

sqrt_difference_x: float = (x1-x2) ** 2
sqrt_difference_y: float = (y1-y2) ** 2

distance: float = math.sqrt(sqrt_difference_x + sqrt_difference_y)

print(distance)