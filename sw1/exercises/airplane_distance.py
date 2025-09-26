#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 20.09.2025 10:44
@author: marcwelz
@project: mo25
"""
import math
from typing import TypedDict

from helper_functions import read_int

class AirplaneLocation(TypedDict, total=True):
    x_position: int
    y_position: int

default_value: int = 2

position_x_plane_1: int = read_int(input("x position airplane 1: "), default_value)
position_y_plane_1: int = read_int(input("y position airplane 1: "), default_value)
position_x_plane_2: int = read_int(input("x position airplane 2: "), default_value)
position_y_plane_2: int = read_int(input("y position airplane 2: "), default_value)

position_airplane1: AirplaneLocation = {"x_position": position_x_plane_1, "y_position": position_y_plane_1}
position_airplane2: AirplaneLocation = {"x_position": position_x_plane_2, "y_position": position_y_plane_2}

def calculate_distance(plane1: AirplaneLocation, plane2: AirplaneLocation) -> float:
    square_difference_x: float = (plane2['x_position'] - plane1['x_position']) ** 2
    square_difference_y: float = (plane2['y_position'] - plane1['y_position']) ** 2

    return math.sqrt(square_difference_x + square_difference_y)

distance: float = calculate_distance(position_airplane1, position_airplane2)
print(distance)

