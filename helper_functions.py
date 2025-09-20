#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 20.09.2025 11:28
@author: marcwelz
@project: mo25
"""

def read_float(prompt: str, default: float) -> float:
    try:
        return float(input(prompt))
    except ValueError:
        print(f"invalid input, us default value {default}")
        return default