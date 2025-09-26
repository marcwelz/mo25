#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 26.09.2025 10:04
@author: marcwelz
@project: mo25
"""

# noch nicht relevant
for x in range(3):
    print('.' * (x + 1))

# datentypen
# beschreibt den typ des werts einer variable wir das umgekehrte e in der Mathematik
# das "=" heisst nicht gleich sondern assignement, man weist einer variablen einen wert zu
# wenn es gleich bedeuten sollte, benutzt man zwei Gleichzeichen also ==
# variablen können jeden möglichen namen haben, ideal ist jedoch ein aussagekräftiger Variablennamen
text: str = "hallo" # string speichert Text
fullNumber: int = 3 # int speichert nur ganze Zahlen
decimalNumber: float = 3.2 # Float speichert Kommazahlen

# int + int = int, int - int = int, int * int = int, int / int = float -> Andere Domaine
# was passiert wenn man es vermisch -> dann wird es automatisch umgewandelt
fullNumber = 3 / 2 # hier wird von int auf float umgewandelt
print(fullNumber)

inputVariable: str = input() # input ist standardmässig immer ein string

user_input: str = input('gib mir eine zahl')
user_input: int = int(user_input) # wandelt den input zu einer nummer um

print(user_input + 1) # gibt den user input + 1 aus. WICHTIG: user_input hat seinen wert nicht verändert

xy: int = user_input + 1 # hier wird das +1 in eine neue variable gespeichert