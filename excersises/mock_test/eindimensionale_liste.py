#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 05.12.2025 10:11
@author: marcwelz
@project: mo25
"""

arr: list[float] = [33.3, 12.5, 10.75, 44, 65.5]

def get_durchschnitt(x: list[float]) -> float:
    return sum(x) / len(x)

def get_nearest_index_false(x:list[float]) -> int:
    avg:float = get_durchschnitt(x)
    h: float = 0
    h_index: int = 0
    for index, i in enumerate(x):
        if (i % avg) > h:
            h = i % avg
            h_index = index

    return h_index

def get_nearest_index_correct(x: list[float]) -> int:
    avg = get_durchschnitt(x)
    nearest_index = 0
    smallest_diff = abs(x[0] - avg)

    for index, value in enumerate(x):
        diff = abs(value - avg)
        if diff < smallest_diff:
            smallest_diff = diff
            nearest_index = index

    return nearest_index

print(get_durchschnitt(arr))
print(get_nearest_index_false(arr))
print(get_nearest_index_correct(arr))