#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 09.05.2026 10:17
@author: marcwelz
@project: mo25
"""
import sys
import traci
import traci.constants


class SumoInterface:
    def __init__(self, SumoNetworkFileName):
        sumoFolder = "C:/Program Files (x86)/Eclipse/Sumo/"
        tools = sumoFolder + "tools/"

        sys.path.append(tools)

        sumoBinary = sumoFolder + "bin/sumo-gui.exe"
        sumoCmd = [sumoBinary, "-c", SumoNetworkFileName, "--start", "--step-length", "0.1"]

        traci.start(sumoCmd, label="new_connection4")
        traci.gui.setSchema('View #0', 'real world')

        self.sim = traci

        # LSA Parameter
        lsaID = "J1"

        self.sumoCmd = sumoCmd
        self.lsaID = lsaID

        self.tr = traci

    def runSingleStep(self, t):
        sim = self.sim
        sim.simulationStep()

    def setSignalHeadState(self, sh_id, color):

        tlsID = self.lsaID
        tr = self.tr

        if color == "GREEN":
            c = 'g'
        elif color == "RED":
            c = 'r'
        elif color == "AMBER":
            c = 'y'
        elif color == "RED_AMBER":
            c = 'y'
        else:
            raise Exception("Color not found")

        currentColors = tr.trafficlight.getRedYellowGreenState(tlsID)
        colors = currentColors
        colorsL = list(colors)
        k = sh_id - 1
        colorsL[k] = c
        colors = ''.join(colorsL)
        tr.trafficlight.setRedYellowGreenState(tlsID, colors)

    def setCounterNumber(self, number):

        print(number)

    def close(self):
        sim = self.sim
        sim.close()