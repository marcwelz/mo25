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
    phase: int

@dataclass
class SignalGroup:
    traffic_lights: list[TrafficLight]

@dataclass
class TrafficLightControl:
    signal_groups: list[SignalGroup]

    def run(self):
        print("Traffic Light Control")
