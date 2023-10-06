import math
import Lab1_Agents_Task1_World as World
from random import randrange
import numpy as np

# connect to the server
import time

from helpFunc_task1 import Energi_Timer, findAndCol

robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))


def random_agent():
    while robot: # main Control loop
        speed_motor = dict(speedRight = randrange(-4,4), speedLeft = randrange(-4,4))
        World.execute(speed_motor, 10000, -1)
        World.collectNearestBlock()

def fix_agent():
    while robot:
        simulationTime = World.getSimulationTime()

        if simulationTime < 15000:
            _speed_motor = dict(speedLeft = -1, speedRight = -2)
        if simulationTime < 10000:
            speed_motor_ = dict(speedLeft = 1, speedRight = 2)
        if simulationTime < 5000:
            speed_motor = dict(speedLeft = 10, speedRight = 10)

        World.execute(speed_motor, simulationTime, 3)
        World.collectNearestBlock()
        World.execute(speed_motor_, simulationTime, 3)
        World.collectNearestBlock()
        World.execute(_speed_motor, simulationTime, 3)
        World.collectNearestBlock()

def reflex_agent():
    while robot:
        findAndCol(1000)

def memory_agent():
    while robot:
        if (time.process_time() - Energi_Timer) > 5:
            findAndCol(2000)
        else:
            findAndCol(1000)


reflex_agent()