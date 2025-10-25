#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 25.10.2025 10:06
@author: marcwelz
@project: mo25
"""

def e1():
    my_list: list = []

    for j in range(10):
        my_row: list = []
        for i in range(10):
            my_row.append(0)

        my_list.append(my_row)

    my_list[1][1] = 2
    my_list[1][2] = 2

    print(*my_list, sep="\n")

def e2_1() -> None:
    mylist: list = [[0] * 10] * 10

    mylist[0][3] = 1

    print(*mylist, sep="\n")

def e2_2() -> None:
    mylist: list = []

    for i in range(10):
        my_row = [0] * 10
        mylist.append(my_row)

    mylist[1][1] = 2

    print(*mylist, sep="\n")

e2_2()