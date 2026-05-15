#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 15.05.2026
@author: marcwelz
@project: mo25
"""
from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
import pandas as pd


class BaseTimingCalculator(ABC):

    @abstractmethod
    def compute_green_times(
        self,
        utilization_of_knots: dict[str, int],
        declared_phases: list[list[str]],
    ) -> list[int]: ...

    @abstractmethod
    def report(
        self,
        utilization_of_knots: dict[str, int],
        declared_phases: list[list[str]],
    ) -> pd.DataFrame: ...


@dataclass
class SignalTimingCalculator(BaseTimingCalculator):
    total_cycle_time: int
    intermediate_time_per_phase_change: int
    minimum_greentime: int
    time_requirement_per_car: int

    def _phase_traffic(
        self,
        utilization_of_knots: dict[str, int],
        declared_phases: list[list[str]],
    ) -> list[int]:
        return [max(utilization_of_knots[k] for k in phase) for phase in declared_phases]

    def _available_greentime(self, num_phases: int) -> float:
        return self.total_cycle_time - num_phases * self.intermediate_time_per_phase_change

    def _distribute(
        self,
        utilization_of_phases: list[int],
        total_available: float,
    ) -> list[int]:
        total: int = sum(utilization_of_phases)
        exact: list[float] = [q / total * total_available for q in utilization_of_phases]
        green_int: list[int] = [int(x) for x in exact]
        missing: int = int(total_available) - sum(green_int)
        order: list[int] = sorted(
            range(len(exact)), key=lambda i: exact[i] - green_int[i], reverse=True
        )
        for i in order[:missing]:
            green_int[i] += 1
        return [max(g, self.minimum_greentime) for g in green_int]

    def compute_green_times(
        self,
        utilization_of_knots: dict[str, int],
        declared_phases: list[list[str]],
    ) -> list[int]:
        utilization_of_phases: list[int] = self._phase_traffic(utilization_of_knots, declared_phases)
        total_available: float = self._available_greentime(len(declared_phases))
        return self._distribute(utilization_of_phases, total_available)

    def report(
        self,
        utilization_of_knots: dict[str, int],
        declared_phases: list[list[str]],
    ) -> pd.DataFrame:
        utilization_of_phases: list[int] = self._phase_traffic(utilization_of_knots, declared_phases)
        total_available: float = self._available_greentime(len(declared_phases))
        green_times: list[int] = self._distribute(utilization_of_phases, total_available)
        total_cycles_in_one_h: float = 3600 / self.total_cycle_time

        rows: list[dict] = []
        for knot, q_vorh in utilization_of_knots.items():
            phase_idx: int = next(i for i, grp in enumerate(declared_phases) if knot in grp)
            g: int = green_times[phase_idx]
            q_moegl: float = total_cycles_in_one_h * g / self.time_requirement_per_car
            rows.append({
                'Signalgruppe':    knot,
                'q_vorh [Fz/h]':  q_vorh,
                'Grünzeit [s]':    g,
                'q_mögl [Fz/h]':  round(q_moegl),
                'Auslastung [%]':  round(q_vorh / q_moegl * 100, 1),
            })

        return pd.DataFrame(rows)
