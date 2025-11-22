#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 22.11.2025 10:43
@author: marcwelz
@project: mo25
"""
import random
from turtledemo.penrose import start

width_board: int = 10
height_board: int = 15

alphabet:list[str] = []
for i in range(ord('a'), ord('z') + 1):
    alphabet.append(chr(i))

def init_battle_board() -> list[list[str]]:
    board: list[list[str]] = []
    for i in range(height_board + 1):
        board.append([])

    for index, row in enumerate(board):
        for i in range(width_board + 1):
            if(index == 0 and i > 0):
                board[index].append(alphabet[i - 1].upper())
            elif(i == 0 and index > 0):
                board[index].append(index)
            else: board[index].append('O')

    return board

def init_battle_ships(board: list[list[str]], battleships_count: int = 1) -> list[list[str]]:
    for x in range(battleships_count):
        random_x_position: int = random.randint(1, width_board - 1)
        random_y_position: int = random.randint(1, height_board - 1)

        board[random_y_position][random_x_position] = '[]'

        if (random_y_position + 1) < height_board:
            board[random_y_position + 1][random_x_position] = '[]'
        if (random_y_position + 2) < height_board:
            board[random_y_position + 2][random_x_position] = '[]'

        random_x_position = random.randint(1, width_board - 1)
        random_y_position = random.randint(1, height_board - 1)

        board[random_y_position][random_x_position] = '[]'

        if (random_x_position + 1) < width_board:
            board[random_y_position][random_x_position + 1] = '[]'
        if (random_x_position + 2) < width_board:
            board[random_y_position][random_x_position + 2] = '[]'

    return board

def check_if_battleship_hits(board: list[list[str]], guess: list[int]) -> bool:
    return board[guess[0]][guess[1]] == '[]'

battle_board: list[list[str]] = init_battle_board()
user_battle_board: list[list[str]] = init_battle_board()

battle_board = init_battle_ships(battle_board, 3)

game_circles: int = 0
correct_guesses: int = 0

for row in battle_board:
    print(*row)

while game_circles <= 10:
    user_input = input(str(game_circles + 1) + ". Try: Guess position: ")
    coordinates: list[int] = []
    coordinates_input: list[str] = user_input.split(',')
    coordinates.append(int(coordinates_input[1]))
    coordinates.append((alphabet.index(coordinates_input[0].lower())) + 1)

    if check_if_battleship_hits(battle_board, coordinates):
        print('You hit!')
        correct_guesses += 1
        user_battle_board[coordinates[0]][coordinates[1]] = '[X]'
        battle_board[coordinates[0]][coordinates[1]] = '[X]'
    else:
        print('You miss!')
        user_battle_board[coordinates[0]][coordinates[1]] = 'X'
        battle_board[coordinates[0]][coordinates[1]] = 'X'

    print(*user_battle_board, sep="\n")
    game_circles += 1

print(f'You had {correct_guesses} correct guesses!')
print(*battle_board, sep="\n")
