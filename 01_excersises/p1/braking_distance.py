#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 20.09.2025 10:34
@author: marcwelz
@project: mo25
"""
import sys
from typing import Final

from helper_functions import read_float

FRICTION: Final[float] = 0.3
GRAVITY_ACCELERATION: Final[float] = 9.81

velocity: float = read_float(sys.argv[1])

def calculate_break_distance(v: float, f: float, g: float) -> float:
    return ((v ** 2) / 2) / (f * g)

break_distance: float = calculate_break_distance(velocity, FRICTION, GRAVITY_ACCELERATION)

print(break_distance)