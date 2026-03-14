#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 14.03.2026 10:30
@author: marcwelz
@project: mo25
"""
from dataclasses import dataclass
import time

@dataclass
class Signal:
    current_color: str
    green_phase: int
    red_phase: int
    yellow_phase: int

@dataclass
class SignalHead(Signal):
    def print_color(self):
        print(self.current_color)

@dataclass
class SignalCountdown(Signal):
    """
    def print_countdown(self):
        if self.current_color == "green":
            print(self.green_phase)
        elif self.current_color == "red":
            print(self.red_phase)
        elif self.current_color == "yellow":
            print(self.yellow_phase)
    """

    def activate(self):
        past_phase_ticks: int = 0
        while True:
            # self.print_countdown()
            if self.current_color == "green":
                print("green: ", self.green_phase - past_phase_ticks, "sec remaining")
                if self.green_phase <= past_phase_ticks:
                    self.current_color = "yellow"
                    past_phase_ticks = 0
            elif self.current_color == "yellow":
                print("yellow: ", self.yellow_phase - past_phase_ticks, "sec remaining")
                if self.yellow_phase <= past_phase_ticks:
                    self.current_color = "red"
                    past_phase_ticks = 0
            elif self.current_color == "red":
                print("red: ", self.red_phase - past_phase_ticks, "sec remaining")
                if self.red_phase <= past_phase_ticks:
                    self.current_color = "green"
                    past_phase_ticks = 0

            past_phase_ticks += 1
            time.sleep(1)

#signal = Signal('green', 5, 2, 6)
signal_countdown = SignalCountdown('green', 5, 6, 2)

signal_countdown.activate()
