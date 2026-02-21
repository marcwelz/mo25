#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 11.10.2025 10:23
@author: marcwelz
@project: mo25
"""

maximum_takeoff_mass: int = 1280 # kg

weight_empty_aircraft: float = float(input("Enter the empty mass of the aircraft (kg): "))
weight_passenger_front: float = float(input("Enter the weight of the pilot/passenger in the front seats (kg): "))
weight_passenger_rear: float = float(input("Enter the weight of the passengers in the rear: (kg): "))
weight_baggage_compartment: float = float(input("Enter the weight of the baggage compartment: (kg): "))
weight_baggage_tube: float = float(input("Enter the weight of the baggage tube: (kg): "))
weight_usable_fuel: float = float(input("Enter the weight of the usable fuel: (kg): "))

total_weight: int = int(
    weight_empty_aircraft +
    weight_passenger_front +
    weight_passenger_rear +
    weight_baggage_compartment +
    weight_baggage_tube +
    weight_usable_fuel
)

if total_weight <= maximum_takeoff_mass:
    print("The aircraft is allowed for taking off!")
else:
    print("The aircraft is too heavy to take off!")


