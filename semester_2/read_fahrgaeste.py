#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 10.04.2026 11:17
@author: marcwelz
@project: mo25
"""

import pandas as pd

passanger_data = pd.read_json("fahrgaeste.json")

average_wait_time_per_line = passanger_data.groupby("linie")["wartezeit"].mean()

print(average_wait_time_per_line)

b = passanger_data['wartezeit'] > 4

print(b)

longest_wait_time = passanger_data[b]

print(longest_wait_time['name'])