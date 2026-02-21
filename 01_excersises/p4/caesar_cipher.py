#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 25.10.2025 11:17
@author: marcwelz
@project: mo25
"""

alphabet:list[str] = []
for i in range(ord('a'), ord('z') + 1):
    alphabet.append(chr(i))
alphabet_length: int = len(alphabet)

def encrypt(text: str) -> str:
    chars:list[str] = list(text.lower())
    new_chars:list[str] = []

    for char in chars:
        if char in alphabet:
            index_of_char = alphabet.index(char)
            new_chars.append(alphabet[(index_of_char - 3) % alphabet_length])
        else:
            new_chars.append(char)

    return ''.join(new_chars)

def decrypt(text: str) -> str:
    chars:list[str] = list(text)
    new_chars:list[str] = []

    for char in chars:
        if char in alphabet:
            index_of_char = alphabet.index(char)
            new_chars.append(alphabet[(index_of_char + 3) % alphabet_length])
        else:
            new_chars.append(char)


    return ''.join(new_chars)

user_input: str = input("Enter your message: ")

encripted_message: str = encrypt(user_input)

print(encripted_message)
print(decrypt(encripted_message))