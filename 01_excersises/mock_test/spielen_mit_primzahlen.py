#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 05.12.2025 10:17
@author: marcwelz
@project: mo25
"""

# Source ChatGPT lol
def ist_primzahl(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True

def naechst_groesse_primzahl(m: int) -> int:
    if ist_primzahl(m):
        return m

    p: int = m
    while True:
        p += 1
        if ist_primzahl(p):
            return p

print(naechst_groesse_primzahl(8))