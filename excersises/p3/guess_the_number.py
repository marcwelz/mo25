#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 18.10.2025 10:48
@author: marcwelz
@project: mo25
"""

import random

rdm_number: int = random.randint(1, 10)

user_guess_number: int = 0

while user_guess_number != rdm_number:
    user_guess_number = int(input("Guess the number from 1 to 10: "))
    if user_guess_number == rdm_number:
        print("You guessed right!")

    elif user_guess_number > rdm_number:
        print("You guess too high")

    else: print("You guess too low")
