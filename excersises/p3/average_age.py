#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 18.10.2025 10:59
@author: marcwelz
@project: mo25
"""

amount_person_in_group: int = int(input('Amount of person in group: '))

age_total_of_group: int = 0

for x in range(amount_person_in_group):
    age_total_of_group += int(input(f'Age of person {x + 1} in group: '))

print('average age', round(age_total_of_group/amount_person_in_group))