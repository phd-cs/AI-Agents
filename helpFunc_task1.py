import math
import Lab1_Agents_Task1_World as World
from random import randrange
import numpy as np

# connect to the server
import time

robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))


## help funtions :
Energi_Counter = 0  
Energi_Timer = 0
def Timer(f):
    count = 0
    while count < f * 5000:
        count = count + 1

def avoid_walls(val):
    #wall in leftside
    if World.getSensorReading("ultraSonicSensorLeft") < 0.9 and World.getSensorReading("ultraSonicSensorRight") == float('inf'):
        var = 'L' 
        World.STOP()
        World.setMotorSpeeds(dict(speedRight = -3, speedLeft = -3))
        Timer(val)
        World.STOP()
        World.setMotorSpeeds(dict(speedRight = 2, speedLeft = 4))
        Timer(val)
        findAndColEnergi()

    #wall in rightside
    elif World.getSensorReading("ultraSonicSensorLeft") == float('inf') and World.getSensorReading("ultraSonicSensorRight") < 0.9:
        var = 'R' 
        World.STOP()
        World.setMotorSpeeds(dict(speedRight = -3, speedLeft = -3))
        Timer(val)
        World.STOP()
        World.setMotorSpeeds(dict(speedRight = 4, speedLeft = 2))
        Timer(val)
        findAndColEnergi()

    #wall in Corner
    elif World.getSensorReading("ultraSonicSensorLeft") < 0.9 and World.getSensorReading("ultraSonicSensorRight") < 0.9:
        var = 'C' 
        World.STOP()
        World.setMotorSpeeds(dict(speedLeft=-3, speedRight=-3))
        Timer(val)
        World.STOP()
        World.setMotorSpeeds(dict(speedLeft=2, speedRight=-2))
        Timer(val)
        findAndColEnergi()

    #wall in leftside
    elif World.getSensorReading("ultraSonicSensorLeft") < 0.9:
        var = 'L' 
        World.STOP()
        World.setMotorSpeeds(dict(speedLeft=-3, speedRight=-3))
        Timer(val)
        World.STOP()
        World.setMotorSpeeds(dict(speedLeft=4, speedRight=2))
        Timer(val)
        findAndColEnergi()

    #wall in rightside
    elif World.getSensorReading("ultraSonicSensorRight") < 0.9:
        var = 'R' 
        World.STOP()
        World.setMotorSpeeds(dict(speedLeft=-3, speedRight=-3))
        Timer(val)
        World.STOP()
        World.setMotorSpeeds(dict(speedLeft=2, speedRight=4))
        Timer(val)
        findAndColEnergi()

    #no walls
    elif World.getSensorReading("ultraSonicSensorLeft") == float('inf') and World.getSensorReading("ultraSonicSensorRight") == float('inf'):
        var = 'N' 

    else:
        var = 'U'
        Timer(val)
        findAndColEnergi()

    return var

def findAndColEnergi():
    energi = World.collectNearestBlock()
    if energi == 'Energy collected :)':
        global Energi_Counter
        global Energi_Timer

        Energi_Counter = Energi_Counter + 1
        Energi_Timer = time.process_time() 

        while Energi_Counter >= 12:
            World.STOP()

def findAndCol(val):
    distance = World.getSensorReading("energySensor").distance
    direction = World.getSensorReading("energySensor").direction

    while direction < 0 and math.fabs(direction) > 0.11:
        World.STOP()
        World.setMotorSpeeds(dict(speedRight = 4, speedLeft = 2))
        distance = World.getSensorReading("energySensor").distance
        direction = World.getSensorReading("energySensor").direction

        avoid_walls(val)
        findAndColEnergi()

    while direction > 0 and math.fabs(direction) > 0.11:
        World.STOP()
        World.setMotorSpeeds(dict(speedRight = 2, speedLeft = 4))
        distance = World.getSensorReading("energySensor").distance
        direction = World.getSensorReading("energySensor").direction

        avoid_walls(val)
        findAndColEnergi()

    while direction == 0:
        distance = World.getSensorReading("energySensor").distance
        direction = World.getSensorReading("energySensor").direction
        avoid_walls(val)
        World.setMotorSpeeds(dict(speedRight = 1, speedLeft = 1))
        findAndColEnergi()

    World.setMotorSpeeds(dict(speedRight = 1, speedLeft = 1))
    findAndColEnergi()
    avoid_walls(val)