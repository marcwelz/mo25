#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 18.10.2025 10:33
@author: marcwelz
@project: mo25
"""

import random

user_action: int = int(input('1: Rock, 2: Paper, 3: Scissor: '))

computer_action: int = random.randint(1, 3)

print("computer chose: ", computer_action)

if user_action == computer_action:
    print("It's a tie!")

elif user_action == 1:
    if computer_action == 2:
        print("Computer wins!")
    elif computer_action == 3:
        print("User wins!")

elif user_action == 2:
    if computer_action == 1:
        print("User wins!")
    elif computer_action == 3:
        print("Computer wins!")

else:
    if computer_action == 1:
        print("Computer wins!")
    elif computer_action == 2:
        print("User wins!")