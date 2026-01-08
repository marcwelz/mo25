#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 19.12.2025 10:07
@author: marcwelz
@project: mo25
"""
import json

plane_data = open('plane_data.txt')
plane_spec = json.load(plane_data)
plane_data.close()

front_seats: float = plane_spec['Front seats']
rear_seats: float = plane_spec['Rear seats']
sdt_baggage_compartment:float = plane_spec['Std baggage compartment']
baggage_tube: float = plane_spec['Baggage tube']
usable_fuel: float = plane_spec['Usable fuel']
empty_distance: float = plane_spec['Empty distance']
maximum_weight: float = plane_spec['Maximum Weight']
empty_moment: float = plane_spec['Empty Moment']

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

total_moment: float = float(empty_moment +
    front_seats * weight_passenger_front +
    rear_seats * weight_passenger_rear +
    sdt_baggage_compartment * weight_baggage_compartment +
    baggage_tube * weight_baggage_tube +
    usable_fuel * weight_usable_fuel)

center_of_gravity: float = total_moment / total_weight

is_CoG_Ok: bool = center_of_gravity >= 2.4 and center_of_gravity <= 2.53

if total_weight <= maximum_weight and is_CoG_Ok:
    print("The aircraft is allowed for taking off!")
else:
    print("The aircraft is too heavy to take off!")

