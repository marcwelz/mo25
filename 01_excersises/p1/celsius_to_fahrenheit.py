#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 20.09.2025 10:41
@author: marcwelz
@project: mo25
"""
from typing import Final

from helper_functions import read_float

CELSIUS_DEFAULT: Final[float] = 20.0

celsius: float = read_float(input("celsius: "), CELSIUS_DEFAULT)

def celsius_to_fahrenheit(c: float) -> float:
    return (c * 9/5) + 32

fahrenheit: float = celsius_to_fahrenheit(celsius)

print(fahrenheit)