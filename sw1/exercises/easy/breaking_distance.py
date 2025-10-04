#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 04.10.2025 10:52
@author: marcwelz
@project: mo25
"""

friction: float = 0.3
gravity_acceleration: float = 9.81

velocity: float = float(input("Enter velocity: "))

break_distance: float = ((velocity ** 2) / 2) / (friction * gravity_acceleration)

print(break_distance)