#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 20.09.2025 11:33
@author: marcwelz
@project: mo25
"""
from helper_functions import read_float

liter_input: float = read_float(input("liters: "), 1.0)
density_input: float = read_float(input("density (kg/l): "), 1.0)

def liter_to_kg(l: float, d: float) -> float:
    return l * d

weight: float = liter_to_kg(liter_input, density_input)

print(weight)