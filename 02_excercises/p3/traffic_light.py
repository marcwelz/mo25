#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 06.04.2026 21:53
@author: marcwelz
@project: mo25
"""

import time
import threading
from dataclasses import dataclass

@dataclass
class Signal:
    current_color: str
    green_phase: int
    red_phase: int
    yellow_phase: int

@dataclass
class SignalHead(Signal):
    def print_color(self) -> None:
        print(self.current_color)

@dataclass
class SignalCountdown(Signal):
    def interstage(self, from_stage: str, to_stage: str) -> None:
        print(f"  Phasenwechsel: {from_stage} → {to_stage}")
        self.current_color = to_stage

    def _simulate(self) -> None:
        past_phase_ticks: int = 0
        while True:
            if self.current_color == "green":
                print(f"green:  {self.green_phase - past_phase_ticks} sec remaining")
                if self.green_phase <= past_phase_ticks:
                    self.interstage("green", "yellow")
                    past_phase_ticks = 0
            elif self.current_color == "yellow":
                print(f"yellow: {self.yellow_phase - past_phase_ticks} sec remaining")
                if self.yellow_phase <= past_phase_ticks:
                    self.interstage("yellow", "red")
                    past_phase_ticks = 0
            elif self.current_color == "red":
                print(f"red:    {self.red_phase - past_phase_ticks} sec remaining")
                if self.red_phase <= past_phase_ticks:
                    self.interstage("red", "green")
                    past_phase_ticks = 0
            past_phase_ticks += 1
            time.sleep(1)

    def _user_input(self) -> None:
        valid_phases: list[str] = ["green", "yellow", "red"]
        while True:
            new_phase: str = input("Neue Phase eingeben (green/yellow/red): ").strip().lower()
            if new_phase in valid_phases:
                self.interstage(self.current_color, new_phase)
            else:
                print(f"  Ungültige Phase: '{new_phase}'")

    def activate(self) -> None:
        t_sim: threading.Thread = threading.Thread(target=self._simulate, daemon=True)
        t_input: threading.Thread = threading.Thread(target=self._user_input, daemon=True)
        t_sim.start()
        t_input.start()
        t_sim.join()


signal: SignalCountdown = SignalCountdown("green", green_phase=5, red_phase=6, yellow_phase=2)
signal.activate()