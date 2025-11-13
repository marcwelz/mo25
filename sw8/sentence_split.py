#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 13.11.2025 14:07
@author: marcwelz
@project: mo25
"""

text: str = 'Hallo ich bin marc. das ist ein satz. ich mag züge.'

sentence_list: list[str] = text.split('.')
del sentence_list[-1]

word_amount: int = 0

for sentence in sentence_list:
    wordsList: list[str] = sentence.split()
    for word in wordsList:
        word_amount += 1

print(word_amount / len(sentence_list))