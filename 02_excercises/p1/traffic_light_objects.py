#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 28.02.2026 11:24
@author: marcwelz
@project: mo25
"""
from dataclasses import dataclass
from enum import Enum

class Status(Enum):
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"

@dataclass
class TrafficLight:
    status: Status

@dataclass
class SignalGroup:
    traffic_lights: list[TrafficLight]

@dataclass
class TrafficLightControl:
    signal_groups: list[SignalGroup]

    def run(self):
        print("Traffic Light Control")

tl1 = TrafficLight(Status.RED)
tl2 = TrafficLight(Status.RED)
tl3 = TrafficLight(Status.GREEN)
tl4 = TrafficLight(Status.GREEN)
tl5 = TrafficLight(Status.GREEN)
tl6 = TrafficLight(Status.YELLOW)
tl7 = TrafficLight(Status.YELLOW)

sg1 = SignalGroup([tl1, tl2])
sg2 = SignalGroup([tl3, tl4, tl5])
sg3 = SignalGroup([tl6, tl7])

traffic_light_control = TrafficLightControl([sg1, sg2, sg3])
traffic_light_control.run()

