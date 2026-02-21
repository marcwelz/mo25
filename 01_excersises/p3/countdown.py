#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 18.10.2025 10:40
@author: marcwelz
@project: mo25
"""

user_countdown = int(input("Enter a number to count downwards: "))

for x in range(user_countdown, -1, -1):
    print(x)

print('---------')

while user_countdown >= 0:
    print(user_countdown)
    user_countdown -= 1

