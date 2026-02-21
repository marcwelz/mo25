#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 21.02.2026 11:03
@author: marcwelz
@project: mo25
"""
import time

wait_time: float = 0.5 # seconds

GREEN: str = "green"
YELLOW: str = "yellow"
RED: str = "red"

initial_traffic_lights: list[dict[str, str]] = [
    {
        "phase": 1,
        "color": RED,
    },
    {
        "phase": 1,
        "color": RED,
    },
    {
        "phase": 2,
        "color": RED,
    },
    {
        "phase": 2,
        "color": RED,
    },
    {
        "phase": 3,
        "color": RED,
    }
]

COLOR_CODE = {"green": "\033[92m", "yellow": "\033[93m", "red": "\033[91m"}

def print_traffic_light_status(tl):
    code = COLOR_CODE[tl["color"]]
    print(f"{code}{tl['color']}{code}")

def change_traffic_light_status(color: str) -> str:
    if color == "green":
        return YELLOW
    elif color == "yellow":
        return RED
    elif color == "red":
        return GREEN
    else:
        return color

def turn_traffic_lights_green(traffic_lights: list[dict[str, str]], greenphase_time: int) -> None:
    for traffic_light in traffic_lights:
        traffic_light['color'] = change_traffic_light_status(traffic_light.get('color'))
    time.sleep(greenphase_time)

def turn_traffic_lights_red(traffic_lights: list[dict[str, str]]) -> None:
    for traffic_light in traffic_lights:
        traffic_light['color'] = change_traffic_light_status(traffic_light.get('color'))
    time.sleep(wait_time)
    for traffic_light in traffic_lights:
        traffic_light['color'] = change_traffic_light_status(traffic_light.get('color'))

def cycle_traffic_lights(traffic_lights: list[dict[str, str]]) -> None:
    current_phase: int = 1

    while current_phase < 4:
        previous_phase: int = 3 if current_phase - 1 == 0 else current_phase - 1
        current_traffic_lights = [item for item in traffic_lights if item["phase"] == current_phase]
        past_traffic_lights = [item for item in traffic_lights if item["phase"] == previous_phase]
        turn_traffic_lights_red(past_traffic_lights)
        turn_traffic_lights_green(current_traffic_lights, 2)

        for traffic_light in traffic_lights:
            print_traffic_light_status(traffic_light)
        print('-----------')

        current_phase += 1

cycle_traffic_lights(initial_traffic_lights)

