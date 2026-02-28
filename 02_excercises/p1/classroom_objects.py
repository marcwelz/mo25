#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 28.02.2026 11:15
@author: marcwelz
@project: mo25
"""
import datetime
from dataclasses import dataclass


@dataclass
class Table:
    area: int

@dataclass
class Student:
    name: str

@dataclass
class Teacher:
    name: str

@dataclass
class Blackboard:
    lastCleaned: datetime

@dataclass
class Classroom:
    tables: list[Table]
    presentStudents: list[Student]
    presentTeacher: Teacher
    blackboard: Blackboard
    subject: str

table1: Table = Table(40)
table2: Table = Table(35)

student1: Student = Student("John")
student2: Student = Student("Marc")
student3: Student = Student("Max")

teacher: Teacher = Teacher("Herr Scherrer")

blackboard: Blackboard = Blackboard(datetime.datetime(2026, 2, 28))

classroom: Classroom = Classroom(
    [table1, table2],
    [student1, student2, student3],
    teacher,
    blackboard,
    'programming'
)

print(classroom)
