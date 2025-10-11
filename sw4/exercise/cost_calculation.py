#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 11.10.2025 10:31
@author: marcwelz
@project: mo25
"""

"""
    This exercise does not work. The exercise itself is faulty
"""

# Constants

a1_material_base_price_per_unit: int = 335
a2_material_base_price_per_unit: int = 1520
b1_material_base_price_per_unit: int = 865

machine_a_base_price: int = 25000
machine_b_base_price: int = 40000

specialist_a_hourly_rate: int = 150
specialist_b_hourly_rate: int = 175
project_manager_hourly_rate: int = 200

project_manager_hours_per_month: int = 42
project_manager_cost_range: range = range(8, 13)  # in percent

# Inputs

project_budget_input: int = int(input("Enter the budget for the project (in CHF): "))
project_machine_type_input: str = input("Enter the machine type (A or B): ").upper()
project_length_months_input: int = int(input("Enter the duration of the project (in months): "))

# functions

def convert_from_hours_to_work_month(input_hours: int) -> int:
    return int(input_hours * 42 * 4)

def calculate_selected_machine_specialist_total_cost() -> int:
    if project_machine_type_input == "A":
        return convert_from_hours_to_work_month(specialist_a_hourly_rate) * project_length_months_input
    else:
        return convert_from_hours_to_work_month(specialist_b_hourly_rate) * project_length_months_input

def calculate_material_cost() -> int:
    if project_machine_type_input == "A":
        return 159 * b1_material_base_price_per_unit
    else:
        return (47 * a1_material_base_price_per_unit) + (119 * a2_material_base_price_per_unit)

def calculate_selected_machine_cost() -> int:
    if project_machine_type_input == "A":
        return machine_b_base_price
    else:
        return machine_a_base_price

# Calculations

selected_machine_specialist_total_cost: int = calculate_selected_machine_specialist_total_cost()

specialist_working_hours_total: int = project_length_months_input * 42

project_manager_labour_cost_total: int = int(
    project_manager_hourly_rate * project_manager_hours_per_month * project_length_months_input)

project_manager_labour_cost_percentage_to_specialist: int = round(100 / selected_machine_specialist_total_cost * project_manager_labour_cost_total)

total_labour_cost: int = selected_machine_specialist_total_cost + project_manager_labour_cost_total

selected_material_cost: int = calculate_material_cost()

selected_machine_cost: int = calculate_selected_machine_cost()

total_costs: int = selected_machine_cost + selected_material_cost + total_labour_cost

# outputs and checks

if total_costs > (project_budget_input / 4):
    print("Error: Total costs exceed the project budget!")

if project_manager_labour_cost_percentage_to_specialist not in project_manager_cost_range:
    print("Error: Project manager labour cost is not within the allowed range!")

print(
    "Machine Cost: " + str(selected_machine_cost) + "\n"
    "Material Cost: " + str(selected_material_cost) + "\n"
    "Total Labour Cost: " + str(total_labour_cost) + "\n"
    "Working Hours of Specialist: " + str(specialist_working_hours_total) + "\n"
    "Project Manager Labour Cost in Percentage: " + str(project_manager_labour_cost_percentage_to_specialist) + "%"
)
