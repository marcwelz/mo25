#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 25.10.2025 10:32
@author: marcwelz
@project: mo25
"""

board:list = []

for i in range(1, 16):
    row:list = []
    for k in range(1, 16):
        row.append('x')

    if i == 1:
        row[1] = '*'
        row[0] = '*'
    elif i == 15:
        row[-1] = '*'
        row[-2] = '*'
    else:
        row[i] = '*'
        row[i-1] = '*'
        row[i-2] = '*'

    board.append(row)

for row in board:
    print(*row)
print(*board, sep="\n")