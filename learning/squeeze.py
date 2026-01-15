#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 14.01.2026 09:57
@author: marcwelz
@project: mo25
"""

b:list[list[int]] = [[100,100,100,100], [0,200,255,0], [127,128,129,0], [0,0,0,0]]

def squeeze(list_input: list[list[int]]) -> list[list[int]]:
    for g_index, item in enumerate(list_input):
        for index, i in enumerate(item):
            if i > 127:
                list_input[g_index][index] = 1
            elif i < 128:
                list_input[g_index][index] = 0

    return list_input

[print(*item, sep='') for item in squeeze(b)]

#print(*squeeze(b), sep='\n')