#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 22.05.2026 10:56
@author: marcwelz
@project: mo25
"""

def is_save_password(pw:str) -> bool:
    if len(pw) < 8:
        return False
    if not any(c.isupper() for c in pw):
        return False
    if not any(c.isdigit() for c in pw):
        return False
    if any(c.isspace() for c in pw):
        return False
    return True

