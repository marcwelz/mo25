#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 21.11.2025 09:59
@author: marcwelz
@project: mo25
"""
from io import TextIOWrapper

fruits: list[str] = ['apple', 'banana', 'orange', 'strawberry']

f: TextIOWrapper = open("greetings.txt", "w")

f.write("Hello, world!" + '\n')

for fruit in fruits:
    f.write(fruit + '\n')

f.close()