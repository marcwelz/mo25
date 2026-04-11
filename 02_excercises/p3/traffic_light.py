#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 06.04.2026 21:53
@author: marcwelz
@project: mo25
"""

import time
import threading
from dataclasses import dataclass, field

STAGES: dict[int, str] = {
    0: "green",
    1: "yellow",
    2: "red",
}

PHASE_DURATION: dict[str, int] = {
    "green": 5,
    "yellow": 2,
    "red": 6,
}

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
class SignalGroup(Signal):
    _stage: int = field(default=0, init=False)
    _ticks_in_stage: int = field(default=0, init=False)

    def current_stage(self) -> int:
        return self._stage

    def interstage(self, from_stage: int, to_stage: int) -> None:
        print(f"  Phasenwechsel: Stage {from_stage} ({STAGES[from_stage]}) → Stage {to_stage} ({STAGES[to_stage]})")
        self._stage = to_stage
        self.current_color = STAGES[to_stage]
        self._ticks_in_stage = 0

    def update(self, t: int) -> None:
        color: str = STAGES[self._stage]
        duration: int = PHASE_DURATION[color]
        remaining: int = duration - self._ticks_in_stage
        print(f"  t={t:03d} | Stage {self._stage} ({color}) | {remaining} sec remaining")

        if self._ticks_in_stage >= duration:
            next_stage: int = (self._stage + 1) % len(STAGES)
            self.interstage(self._stage, next_stage)
        else:
            self._ticks_in_stage += 1

@dataclass
class Simulation:
    signal_group: SignalGroup
    duration: int = 60

    def _run(self) -> None:
        for t in range(self.duration):
            self.signal_group.update(t)
            time.sleep(1)
        print("Simulation beendet.")

    def _user_input(self) -> None:
        while True:
            raw: str = input("Neue Phasennummer eingeben (0=green, 1=yellow, 2=red): ").strip()
            try:
                new_stage: int = int(raw)
                if new_stage in STAGES:
                    self.signal_group.interstage(self.signal_group.current_stage(), new_stage)
                else:
                    print(f"  Ungültige Stage: {new_stage}. Gültig: {list(STAGES.keys())}")
            except ValueError:
                print("  Bitte eine Zahl eingeben.")

    def activate(self) -> None:
        t_sim: threading.Thread = threading.Thread(target=self._run)
        t_input: threading.Thread = threading.Thread(target=self._user_input, daemon=True)
        t_sim.start()
        t_input.start()
        t_sim.join()


if __name__ == "__main__":
    group: SignalGroup = SignalGroup(current_color="green", green_phase=5, red_phase=6, yellow_phase=2)
    sim: Simulation = Simulation(signal_group=group, duration=60)
    sim.activate()