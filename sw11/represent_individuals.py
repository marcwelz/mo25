#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 08.05.2026 11:02
@author: marcwelz
@project: mo25
"""
from dataclasses import dataclass
import random

@dataclass
class Person:
    originalIndex: int
    height: float

    def __lt__(self, other: "Person") -> bool:
        return self.height < other.height

person_list: list[Person] = []

[person_list.append(Person(i, round(random.uniform(165, 185),2))) for i in range(1, 101)]

def quicksort(lst: list[Person]) -> list[Person]:
    if len(lst) <= 1:
        return lst

    pivot = lst[len(lst) // 2]
    left = [p for p in lst if p < pivot]
    middle = [p for p in lst if p.height == pivot.height]
    right = [p for p in lst if pivot < p]

    return quicksort(left) + middle + quicksort(right)


sorted_list = quicksort(person_list)

print(f"{'Rank':<6} {'Original Index':<16} {'Height (cm)'}")
print("-" * 36)
for rank, person in enumerate(sorted_list, start=1):
    print(f"{rank:<6} {person.originalIndex:<16} {person.height:.2f}")



