#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 20.09.2025 11:28
@author: marcwelz
@project: mo25
"""
from typing import Optional

def read_float(prompt: str, default: Optional[float] = None) -> float:
    if default is None:
        default = 10
    try:
        return float(prompt)
    except ValueError:
        print(f"invalid input, us default value {default}")
        return default

def read_int(prompt: str, default: Optional[int] = None) -> int:
    if default is None:
        default = 10
    try:
        return int(prompt)
    except ValueError:
        print(f"invalid input, us default value {default}")
        return default