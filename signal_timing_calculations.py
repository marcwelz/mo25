#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 08.01.2026 11:44
@author: marcwelz
@project: mo25
"""

# -------- Parameters --------
# enter your values below

intermediate_time_per_phase_change: int = 6 #seconds
total_cycle_time: int = 45 #seconds
time_requirement_per_car: int = 2 #seconds
utilization_of_knots: dict[str, int] = {'K1': 400, 'K2': 200, 'K3': 250, 'K4': 420} #traffic per hour
declaired_phases: list[list[str]] = [['K1', 'K4'], ['K2'], ['K3']] #declaration of phases

# -------- Variables --------

greentime_of_phases: list[float] #max traffix per hour
possible_utilization_of_phases: list[float] #max traffix per hour
total_utilization_of_phases: list[float] #in %
utilization_of_phases: list[int]

# -------- Functions --------

def determining_traffic_performance_volume_per_phase(phases: list[list[str]]) -> list[int]:
    determined_traffic_volume: list[int] = []
    for phase in phases:
        tmp_arr_traffic_per_phase: list[int] = []
        for knot in phase:
            tmp_arr_traffic_per_phase.append(utilization_of_knots[knot])

        determined_traffic_volume.append(max(tmp_arr_traffic_per_phase))

    return determined_traffic_volume

def calculate_phase_greentime(_total_utilization: int, _total_available_greentime: float, _utilization_of_phases: list[int]) -> list[float]:
    exact = [q / _total_utilization * _total_available_greentime for q in _utilization_of_phases]
    green_int = [int(x) for x in exact]
    missing = int(_total_available_greentime) - sum(green_int)
    order = sorted(range(len(exact)), key=lambda i: exact[i] - green_int[i], reverse=True)
    for i in order[:missing]:
        green_int[i] += 1

    return green_int


def calculate_possible_utilization_of_phases(_utilization_of_phases: list[int], _total_cycles_in_one_h: float, _greentime_of_phases: list[float], _time_requirement_per_car: int) -> list[float]:
    tmp_arr: list[float] = []
    for index, current_phase in enumerate(_utilization_of_phases):
        tmp_arr.append(_total_cycles_in_one_h * greentime_of_phases[index] / _time_requirement_per_car)

    return tmp_arr

def calculate_total_utilization_of_phases(_utilization_of_knots: dict[str, int], _declaired_phases: list[list[str]], _possible_utilization_of_phases: list[float]) -> list[float]:
    tmp_arr: list[float] = []
    for knot, value in _utilization_of_knots.items():
        i = next(i for i, group in enumerate(_declaired_phases) if knot in group)
        tmp_arr.append(value / _possible_utilization_of_phases[i])

    return tmp_arr

# -------- Calculations --------

total_cycles_in_one_h: float = 3600 / total_cycle_time
utilization_of_phases = determining_traffic_performance_volume_per_phase(declaired_phases)

total_utilization: int = sum(utilization_of_phases)
total_available_greentime: float = total_cycle_time - (len(utilization_of_phases) * intermediate_time_per_phase_change)
greentime_of_phases = calculate_phase_greentime(total_utilization, total_available_greentime, utilization_of_phases)
possible_utilization_of_phases = calculate_possible_utilization_of_phases(utilization_of_phases, total_cycles_in_one_h, greentime_of_phases, time_requirement_per_car)
total_utilization_of_phases = calculate_total_utilization_of_phases(utilization_of_knots, declaired_phases, possible_utilization_of_phases)

if not int(sum(greentime_of_phases)) == int(total_available_greentime):
    print('greentime of phases do not math with available greentime')

# display table (source chatgpt)
# can be ignored

rows = []
for index, knot_key in enumerate(utilization_of_knots):
    i = next(i for i, group in enumerate(declaired_phases) if knot_key in group)

    q_vorh = utilization_of_knots[knot_key]
    g = greentime_of_phases[i]
    q_moegl = possible_utilization_of_phases[i]
    auslast = total_utilization_of_phases[index]

    cycles_txt = f"{total_cycles_in_one_h:g}".rstrip(".")
    g_txt = f"{g:.0f}"
    formula = f"{cycles_txt} * {g_txt} / {time_requirement_per_car} = {q_moegl:.0f} Fz/h"

    rows.append([
        knot_key,
        f"{q_vorh} Fz/h",
        formula,
        f"{auslast*100:.0f}%"
    ])

headers = ["Signalgruppe", "q_vorh", "q_moegl", "Auslastung"]

col_widths = [len(h) for h in headers]
for r in rows:
    for j, cell in enumerate(r):
        col_widths[j] = max(col_widths[j], len(cell))

def hline(left: str, mid: str, right: str) -> str:
    return left + mid.join("─" * (w + 2) for w in col_widths) + right

def fmt_row(cells: list[str]) -> str:
    out = "│"
    for j, cell in enumerate(cells):
        right_align = (j != 0)
        content = cell.rjust(col_widths[j]) if right_align else cell.ljust(col_widths[j])
        out += f" {content} │"
    return out

print(hline("┌", "┬", "┐"))
print(fmt_row(headers))
print(hline("├", "┼", "┤"))
for r in rows:
    print(fmt_row(r))
print(hline("└", "┴", "┘"))