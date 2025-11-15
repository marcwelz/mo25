#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 15.11.2025 10:06
@author: marcwelz
@project: mo25
"""

my_string: str = 'hallo,max,tschau'

names_list: list[str] = my_string.split(',')
my_string_2: str = ','.join(names_list)

print(names_list, my_string_2)