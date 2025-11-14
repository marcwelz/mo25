#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 14.11.2025 14:08
@author: marcwelz
@project: mo25
"""
import math

"""
trail: list[tuple[float, float]] = \
    [(142.492, 208.536),
    (142.658, 207.060),
    (143.522, 205.978),
    (145.009, 205.546)]
"""

trail_list: list[tuple[float, float]] = [(1, 1), (2, 1), (1, 2), (1, 1)]

def path_length(trail: list[tuple[float, float]]) -> float:
    total_length: float = 0

    for index in range(1, len(trail) - 1):
        total_length += math.sqrt(
            ((trail[index][0] - trail[index - 1][0]) ** 2) + ((trail[index][1] - trail[index - 1][1]) ** 2))

    return total_length

print(path_length(trail_list))