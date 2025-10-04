#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 04.10.2025 10:40
@author: marcwelz
@project: mo25
"""
import random

a: int = 3
b: int = 50

randomIntNumbers: list[int] = []

for i in range(10):
    randomIntNumbers.append(random.randint(a, b))

print(randomIntNumbers)