#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 09.05.2026 10:18
@author: marcwelz
@project: mo25
"""
from __future__ import annotations
import threading
import time
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import sumo_interface as intf
from signal_timing import SignalTimingCalculator

# Config

SUMO_CONFIG:str = "EinfacheKreuzung.sumocfg"
SIMULATION_DURATION:int = 120 # [s]
STEPS_PER_SECOND:int = 10 # same step length as in .sumocfg

YELLOW_DURATION:int = 2 # [s]
RED_CLEARANCE:int = 4 # [s]

# singal calculations
CYCLE_TIME:int = 60 # calculation time [s]
INTERMEDIATE_TIME:int = YELLOW_DURATION + RED_CLEARANCE # 6 s
MIN_GREEN_TIME:int = 6 # minimal greent time [s]
TIME_PER_CAR:int = 2 # const: time for car to pass [s/Fz]

UTILIZATION_OF_KNOTS: dict[str, int] = {
    'K1': 300, # South
    'K2': 300, # North
    'K3': 600, # East
    'K4': 600, # West
}
KNOT_PHASES: list[list[str]] = [['K1'], ['K2'], ['K3'], ['K4']]

# add id of signal heads
SIGNAL_GROUPS: list[list[int]] = [
    [7, 8, 9, 10], # sg0
    [1, 2, 3], # sg1
    [5, 6], # sg2
    [11, 12], # sg3
    [4], # sg4
    [13], # sg5 persons
]

# same greentinme
PHASE_DEFINITIONS: list[list[int]] = [
    [0], # Phase 1
    [1, 4], # Phase 2
    [2, 4], # Phase 3
    [3, 5], # Phase 4
]

# Engine

@dataclass
class SignalGroup:
    head_ids: list[int]
    yellow_phase: int
    red_phase: int

@dataclass
class SignalPhase:
    name: str
    active_groups: list[SignalGroup]
    green_time: int = field(default=0)

class BaseController(ABC):
    @abstractmethod
    def step(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...


class TrafficController(BaseController):
    _STAGES: tuple[str, ...] = ("green", "yellow", "red")
    _COLOR_MAP: dict[str, str] = {"green": "GREEN", "yellow": "AMBER", "red": "RED"}

    def __init__(
        self,
        interface: intf.SumoInterface,
        all_groups: list[SignalGroup],
        phases: list[SignalPhase],
    ) -> None:
        self._v: intf.SumoInterface = interface
        self._all_groups: list[SignalGroup] = all_groups
        self._phases: list[SignalPhase] = phases
        self._phase_idx: int = 0
        self._stage_idx: int = 0
        self._timer: int = 0
        self._apply()

    def _stage_duration(self) -> int:
        phase: SignalPhase = self._phases[self._phase_idx]
        stage: str = self._STAGES[self._stage_idx]
        if stage == "green":
            return phase.green_time
        rep: SignalGroup = phase.active_groups[0]
        return rep.yellow_phase if stage == "yellow" else rep.red_phase

    def _apply(self) -> None:
        sumo_color: str = self._COLOR_MAP[self._STAGES[self._stage_idx]]
        active_ids: set[int] = {id(g) for g in self._phases[self._phase_idx].active_groups}
        for group in self._all_groups:
            color: str = sumo_color if id(group) in active_ids else "RED"
            for head_id in group.head_ids:
                self._v.setSignalHeadState(head_id, color)

    def step(self) -> None:
        if self._timer >= self._stage_duration():
            self._timer = 0
            self._stage_idx += 1
            if self._stage_idx >= len(self._STAGES):
                self._stage_idx = 0
                self._phase_idx = (self._phase_idx + 1) % len(self._phases)
            self._apply()
        self._timer += 1

    def close(self) -> None:
        self._v.close()


@dataclass
class Simulation:
    interface: intf.SumoInterface
    controller: TrafficController
    period_time: int
    steps_per_second: int

    def _run(self) -> None:
        for i in range(self.period_time * self.steps_per_second):
            self.interface.runSingleStep(i / self.steps_per_second)
            if i % self.steps_per_second == 0:
                self.controller.step()
            time.sleep(1 / self.steps_per_second)

    def activate(self) -> None:
        t: threading.Thread = threading.Thread(target=self._run)
        t.start()
        t.join()
        self.controller.close()


# Execute

groups: list[SignalGroup] = [
    SignalGroup(heads, yellow_phase=YELLOW_DURATION, red_phase=RED_CLEARANCE)
    for heads in SIGNAL_GROUPS
]

calculator: SignalTimingCalculator = SignalTimingCalculator(
    total_cycle_time=CYCLE_TIME,
    intermediate_time_per_phase_change=INTERMEDIATE_TIME,
    minimum_greentime=MIN_GREEN_TIME,
    time_requirement_per_car=TIME_PER_CAR,
)
green_times: list[int] = calculator.compute_green_times(UTILIZATION_OF_KNOTS, KNOT_PHASES)
print(calculator.report(UTILIZATION_OF_KNOTS, KNOT_PHASES).to_string(index=False))

signal_phases: list[SignalPhase] = []
for index, sg_indices in enumerate(PHASE_DEFINITIONS):
    active: list[SignalGroup] = [groups[j] for j in sg_indices]
    signal_phases.append(SignalPhase(f"P{index + 1}", active, green_time=green_times[index]))

v: intf.SumoInterface = intf.SumoInterface(SUMO_CONFIG)

Simulation(
    interface=v,
    controller=TrafficController(v, groups, signal_phases),
    period_time=SIMULATION_DURATION,
    steps_per_second=STEPS_PER_SECOND,
).activate()
