#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 08.05.2026 11:23
@author: marcwelz
@project: mo25
"""
import os

path: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

entries = os.listdir(path)

#easy
for entry in entries:
    full_path = os.path.join(path, entry)
    if os.path.isfile(full_path):
        print(f'\U0001F4C4 {entry}')
    else:
        print(f'\U0001F4C1 {entry}')

#extended
for root, dirs, files in os.walk(path):
    level = root.replace(path, '').count(os.sep)
    indent = '  ' * level
    print(f'{indent}\U0001F4C1 {os.path.basename(root)}/')
    for file in files:
        print(f'{indent}  \U0001F4C4 {file}')