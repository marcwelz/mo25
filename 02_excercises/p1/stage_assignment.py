#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 07.03.2026 10:16
@author: marcwelz
@project: mo25
"""
from dataclasses import dataclass

stageAssignment: list[list[bool]] = [
    [True, False],
    [False, True],
]

@dataclass
class SignalGroup:
    is_active: bool = False

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

@dataclass
class StageController:
    signal_groups: list[SignalGroup]
    stageAssignment: list[list[bool]]

    def interstage(self, to_stage: int) -> None:
        for gruppenIndex, group in enumerate(self.signal_groups):
            isActive: bool = self.stageAssignment[gruppenIndex][to_stage]
            if isActive:
                group.activate()
            else:
                group.deactivate()

signal_group1 = SignalGroup(stageAssignment[0][0])
signal_group2 = SignalGroup(stageAssignment[1][0])

stage_controller = StageController([signal_group1, signal_group2], stageAssignment=stageAssignment)

for index, stage_asg in enumerate(stageAssignment):
    stage_controller.interstage(index)
    print(stage_controller.signal_groups)


