#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 20.09.2025 10:34
@author: marcwelz
@project: mo25
"""
import sys

velocity: float = float(sys.argv[1])
friction: float = 0.3
gravity_acceleration: float = 9.81

def calculate_break_distance(v: float, f: float, g: float) -> float:
    return ((v ** 2) / 2) / (f * g)

break_distance: float = calculate_break_distance(velocity, friction, gravity_acceleration)

print(break_distance)