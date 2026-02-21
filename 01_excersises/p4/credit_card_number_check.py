#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 01.11.2025 10:10
@author: marcwelz
@project: mo25
"""

credit_card_number_input:str = input("Enter the credit card number: XXXX XXXX XXXX XXXX")

def check_if_credit_card_number_is_valid(credit_card_number:str) -> bool:
    if len(credit_card_number) != 19:
        return False

    chars:list[str] = list(credit_card_number)

    for index, char in enumerate(chars):
        if index == 4 or index == 9 or index == 14 or index == 19:
            if char != ' ':
                return False
        else:
            if not char.isdigit():
                return False

    sum_total: int = 0
    for section in credit_card_number.split(' '):
        for number in section:
            sum_total += int(number)

    return sum_total % 10 == 0

print(check_if_credit_card_number_is_valid(credit_card_number_input))