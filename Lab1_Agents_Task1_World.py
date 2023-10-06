import vrep, math, time, random

# stop the robot
def STOP():
    setMotorSpeeds(dict(speedLeft=0, speedRight=0))    

# get some information from one of the sensors
def getSensorReading(sensor):
    def getObstacleDist(sensorHandler_):
        # Get raw sensor readings using API
        rawSR = vrep.simxReadProximitySensor(robot.clientID, sensorHandler_, vrep.simx_opmode_oneshot_wait)
        #print(rawSR)
        # Calculate Euclidean distance
        if rawSR[1]: # if true, obstacle is within detection range, return distance to obstacle
            return math.sqrt(rawSR[2][0]*rawSR[2][0] + rawSR[2][1]*rawSR[2][1] + rawSR[2][2]*rawSR[2][2])
        else: # if false, obstacle out of detection range, return inf.
            return float('inf')
    if sensor=="ultraSonicSensorLeft":
        return getObstacleDist(robot.ultraSonicSensorLeft)
    elif sensor=="ultraSonicSensorRight":
        return getObstacleDist(robot.ultraSonicSensorRight)
    elif sensor=="energySensor":
        blockHandle,blockName,distance,direction = findEnergyBlocks()[0]
        return EasyDict(distance=distance,direction=direction)
    print ("Unknown sensor:",sensor)
    return None

# set speeds for robot wheels
def setMotorSpeeds(motorSpeed):
    try:
        vrep.simxPauseCommunication(robot.clientID,True)
        vrep.simxSetJointTargetVelocity(robot.clientID, robot.leftMotorHandle, motorSpeed.get('speedLeft',0), vrep.simx_opmode_oneshot )
        vrep.simxSetJointTargetVelocity(robot.clientID, robot.rightMotorHandle, motorSpeed.get('speedRight',0), vrep.simx_opmode_oneshot )
    finally:
        vrep.simxPauseCommunication(robot.clientID,False)

# execute an action for a given time, then stop the robot and return control
def execute(motorSpeed,simulationTime,clockTime):
    startTimeSim = getSimulationTime()
    startTimeClock = time.time()
    setMotorSpeeds(motorSpeed)
    while True:
        if simulationTime>0 and getSimulationTime()>startTimeSim+simulationTime: break
        if clockTime>0 and time.time()>startTimeClock+clockTime: break
        time.sleep(0.1)
    STOP()

# which direction robot is facing?
def robotDirection():
    retCode, robotOrientation = vrep.simxGetObjectOrientation(robot.clientID, robot.pioneerRobotHandle, -1, vrep.simx_opmode_oneshot_wait)
    direction = math.pi/2 - robotOrientation[2]
    return normaliseAngle(direction)

# time is useful
def getSimulationTime():
    vrep.simxGetPingTime(robot.clientID)
    return vrep.simxGetLastCmdTime(robot.clientID)-connectionTime

################################################################################
################################################################################
# Helper functions below... not all that interesting...                        #
################################################################################
################################################################################

class EasyDict(dict):
    def __init__(self, *args, **kwargs):
        super(EasyDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

# a function to initialise connection to the server... hides a lot of uninteresting technical details.
def init():
    global robot
    global blockHandleArray, connectionTime
    print('Program started')
    vrep.simxFinish(-1) # just in case, close all opened connections
    int_portNb = 19999 # define port_nr
    clientID = vrep.simxStart('127.0.0.1', int_portNb, True, True, 5000, 5) # connect to server
    if clientID != -1:
        print('Connected to remote API server')
        res,objs = vrep.simxGetObjects(clientID,vrep.sim_handle_all,vrep.simx_opmode_oneshot_wait) # get all objects in the scene
        if res == vrep.simx_return_ok: # Remote function call succeeded
            print('Number of objects in the scene: ',len(objs))# print number of object in the scene
            ret_lm,  leftMotorHandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_leftMotor', vrep.simx_opmode_oneshot_wait)
            ret_rm,  rightMotorHandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor', vrep.simx_opmode_oneshot_wait)
            ret_pr,  pioneerRobotHandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx', vrep.simx_opmode_oneshot_wait)
            ret_sl,  ultraSonicSensorLeft = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_ultrasonicSensor3',vrep.simx_opmode_oneshot_wait)
            ret_sr,  ultraSonicSensorRight = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_ultrasonicSensor5',vrep.simx_opmode_oneshot_wait)
            blockHandleArray = []
            for i_block in range(12):
                blockName = 'ConcretBlock#'+str(i_block)
                retCode, handle = vrep.simxGetObjectHandle(clientID, blockName, vrep.simx_opmode_oneshot_wait)
                assert retCode==0, retCode
                if i_block>6:
                    rand_loc = [random.random()*6-1.5, random.random()*7-2.5, 0.0537] # x[-1.5,4.5] y[-2.5,-4.5]
                    vrep.simxSetObjectPosition(clientID, handle, -1, rand_loc, vrep.simx_opmode_oneshot_wait)
                retCode,position = vrep.simxGetObjectPosition(clientID, handle, -1, vrep.simx_opmode_oneshot_wait)
                assert retCode==0, retCode
                blockHandleArray.append([handle,i_block,position])
            robot = EasyDict(clientID=clientID,
                             leftMotorHandle=leftMotorHandle,
                             rightMotorHandle=rightMotorHandle,
                             pioneerRobotHandle=pioneerRobotHandle,
                             ultraSonicSensorLeft=ultraSonicSensorLeft,
                             ultraSonicSensorRight=ultraSonicSensorRight,
                             energySensor=None)
            connectionTime = vrep.simxGetLastCmdTime(robot.clientID)
            return robot
        else:
            print('Remote API function call returned with error code: ',res)
        vrep.simxFinish(clientID) # close all opened connections
    else:
        print('Failed connecting to remote API server')
        print('Program finished')
    return {}

# helper function
def findEnergyBlocks():
    res = []
    retCode, robotPos = vrep.simxGetObjectPosition(robot.clientID, robot.pioneerRobotHandle, -1, vrep.simx_opmode_oneshot_wait)
    robotdirection = robotDirection()
    for blockHandle,blockName,blockPosition in blockHandleArray:
        # retCode, relativePos = vrep.simxGetObjectPosition(robot.clientID, blockHandle, robot.pioneerRobotHandle, vrep.simx_opmode_oneshot_wait)
        # relativePos = [ robotPos[0]-blockPosition[0], robotPos[1]-blockPosition[1] ]
        relativePos = [ blockPosition[0]-robotPos[0], blockPosition[1]-robotPos[1] ]
        distance = math.sqrt(relativePos[0]**2 + relativePos[1]**2) # compute Euclidean distance (in 2-D)
        absDirection = math.atan2(relativePos[0],relativePos[1])
        direction = normaliseAngle(absDirection - robotdirection)
        res.append((blockHandle,blockName,distance,direction))
    res.sort(key=lambda xx:xx[2])
    return res
# helper function
def collectNearestBlock():
    blockHandle,blockName,distance,direction = findEnergyBlocks()[0]
    if distance <= 0.5:
        vrep.simxSetObjectPosition(robot.clientID, blockHandle, -1, [1000,1000,-2], vrep.simx_opmode_oneshot)
        blockHandleArray[blockName][-1] = [1000,1000,-2]
        return('Energy collected :)')
    return('No blocks nearby :(')

def normaliseAngle(direction):
    while direction>math.pi: direction -= 2*math.pi
    while direction<-math.pi: direction += 2*math.pi
    assert -math.pi<=direction<=math.pi, direction
    return direction
