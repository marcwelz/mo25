#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 09.05.2026 10:18
@author: marcwelz
@project: mo25
"""

import time
from dataclasses import dataclass, field
import sumo_interface as intf

# ---------------------------------------------------------------------------
# Signal-Logik (aus p3/traffic_light.py)
# ---------------------------------------------------------------------------
STAGES: dict[int, str] = {
    0: "green",
    1: "yellow",
    2: "red",
}

PHASE_DURATION: dict[str, int] = {
    "green":  5,
    "yellow": 2,
    "red":    6,
}

@dataclass
class Signal:
    current_color: str
    green_phase: int
    red_phase: int
    yellow_phase: int

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

@dataclass()
class SignalPhase:
    signal_groups: list[tuple[list[int], SignalGroup]]
    current_stage: STAGES
    green_time: int
    #todo intergreen_times: int


# ---------------------------------------------------------------------------
# Simulation
# ---------------------------------------------------------------------------

# traffic_light Farben → SUMO Signal-Zustände
COLOR_MAP: dict[str, str] = {
    "green":  "GREEN",
    "yellow": "AMBER",
    "red":    "RED",
}

period_time = 30          # Simulationsdauer in Sekunden
simStepsPerSecond = 10    # Schritte pro Sekunde (jeder Schritt = 0.1 s)
simTimeSteps = range(period_time * simStepsPerSecond)  # range(300)

filename = "EinfacheKreuzung.sumocfg"
v = intf.SumoInterface(filename)

sg1: tuple[list[int], SignalGroup] = \
    ([7, 8, 9, 10], SignalGroup(current_color="green", green_phase=5, yellow_phase=2, red_phase=6))
sg2: tuple[list[int], SignalGroup] = \
    ([1,2,3], SignalGroup(current_color="red", green_phase=5, yellow_phase=2, red_phase=6))
sg3: tuple[list[int], SignalGroup] = \
    ([5, 6], SignalGroup(current_color="red", green_phase=5, yellow_phase=2, red_phase=6))
sg4: tuple[list[int], SignalGroup] = \
    ([11,12], SignalGroup(current_color="red", green_phase=5, yellow_phase=2, red_phase=6))
sg5: tuple[list[int], SignalGroup] = \
    ([4], SignalGroup(current_color="red", green_phase=5, yellow_phase=2, red_phase=6))
sg6: tuple[list[int], SignalGroup] = \
    ([13], SignalGroup(current_color="red", green_phase=5, yellow_phase=2, red_phase=6))

signal_groups: list[tuple[list[int], SignalGroup]] = [
    sg1, sg2, sg3, sg4, sg5, sg6
]


ss1: SignalPhase = SignalPhase([sg1], 'GREEN', 5)
ss2: SignalPhase = SignalPhase([sg2, sg5], 'RED', 5)
ss3: SignalPhase = SignalPhase([sg3, sg5], 'RED', 5)
ss4: SignalPhase = SignalPhase([sg4, sg6], 'RED', 5)

signal_phases: list[SignalPhase] = [
    ss1, ss2, ss3, ss4
]

for phase in signal_phases:
    for head_ids, group in phase.signal_groups:
        v.setSignalHeadState(head_ids, COLOR_MAP[group.current_color])

for i in simTimeSteps:
    t = i / simStepsPerSecond  # Simulationszeit in Sekunden (0.0 … 29.9)
    v.runSingleStep(t)

    if i % simStepsPerSecond == 0:
        t_sec = i // simStepsPerSecond
        for head_ids, group in signal_groups:
            group.update(t_sec)
            for head_id in head_ids:
                v.setSignalHeadState(head_id, COLOR_MAP[group.current_color])

    time.sleep(0.07)

v.close()
