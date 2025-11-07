#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 25.10.2025 10:23
@author: marcwelz
@project: mo25
"""

all_dominos:list = []

for i in range(1, 7):
    for k in range(i, 7):
        domino: list = [i, k]
        all_dominos.append(domino)

print(*all_dominos, sep="\n")