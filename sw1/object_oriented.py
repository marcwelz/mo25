#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 28.02.2026 10:19
@author: marcwelz
@project: mo25
"""
from dataclasses import dataclass

@dataclass
class TrafficLight:
    status: str
    phase: int


tl1 = TrafficLight('green', 1)
tl2 = TrafficLight('green', 1)
tl3 = TrafficLight('red', 2)

print(tl1)