#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 05.12.2025 10:04
@author: marcwelz
@project: mo25
"""

arr: list[int] = [23,13,2,33,25,12,29]

def best_bath_dat(tmp_arr: list[int]) -> str:
    days: list[str] = ['mo', 'di', 'mi', 'do', 'fr', 'sa', 'so']

    max_tmp: int = 0
    max_index: int = 0

    for index, x in enumerate(tmp_arr):
        if x > max_tmp:
            max_tmp = x
            max_index = index

    return days[max_index]

print(best_bath_dat(arr))