#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 20.02.2026 10:12
@author: marcwelz
@project: mo25
"""
import random

x: dict[str, list[str]] = {
    'ZRH': ['LX333', 'LX122', 'LX187'],
    'BSL': ['LX433', 'LX722'],
    'AMS': ['LX933'],
}
y: dict[str, str] = {
    'Zuerich': 'ZRH',
    'Basel': 'BSL',
    'Amsterdam': 'AMS',
}

def calculate_num_sceduled_flights(
        airport_codes_and_flightnumber: dict[str, list[str]],
        airport_names_and_codes: dict[str, str]
    ) -> int:

    random_airport_code: str = random.choice(list(airport_names_and_codes.values()))

    if random_airport_code in airport_codes_and_flightnumber:
        return len(airport_codes_and_flightnumber[random_airport_code])
    return 0

print(calculate_num_sceduled_flights(x, y))