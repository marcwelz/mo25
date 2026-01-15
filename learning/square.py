#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 14.01.2026 10:29
@author: marcwelz
@project: mo25
"""

def draw_square(width: int) -> str:
    tmp_str: str = ''
    for x in range(5):
        for y in range(width):
            if x == 0 or x == width - 1:
                tmp_str +='*'
            elif y == 0 or y == width -1:
                tmp_str +='*'
            else:
                tmp_str +=' '
        tmp_str += '\n'
    return tmp_str

print(draw_square(5))

