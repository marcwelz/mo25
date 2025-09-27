#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 20.09.2025 11:33
@author: marcwelz
@project: mo25
"""
from typing import Final
from helper_functions import read_float

DEFAULT_VALUE: Final[float] = 1.0

liter_input: float = read_float(input("liters: "), DEFAULT_VALUE)
density_input: float = read_float(input("density (kg/l): "), DEFAULT_VALUE)

def liter_to_kg(l: float, d: float) -> float:
    return l * d

weight: float = liter_to_kg(liter_input, density_input)

print(weight)