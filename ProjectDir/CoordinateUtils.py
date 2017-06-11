'''
Created on May 17, 2017

@author: Justin Veyna
'''

'''
############################################################################################################
#----------------------------------------------------------------------------------------------------------#
#----------------------------------------------Todo--------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------#
############################################################################################################
'''


'''
############################################################################################################
#----------------------------------------------------------------------------------------------------------#
#----------------------------------------------Constants---------------------------------------------------#
#----------------------------------------------------------------------------------------------------------#
############################################################################################################
'''
emptyBlock = "air"
normalBlock = "stone"
dangerBlock = "lava"
rewardBlock = "lapis_block"
terminalBlock = "emerald_block"

malmoGroundY = 226
lavaDepth = 7
raiseBy = 2
agentStart = (.5, malmoGroundY+raiseBy+1, .5)
agentStart2 = (0,0,0)

#rewardDict = {"coal": 10, "iron_ingot": 20, "gold_ingot": 30, "lapis_ore": 40, "emerald_ore": 50, "diamond": 60, "potato": 70}
rewardDict = {"coal": 10, "iron_ingot": 10, "gold_ingot": 10, "lapis_ore": 10, "emerald_ore": 10, "diamond": 10, "potato": 10}

movement1D = [(1,0,0),(-1,0,0)] #right, left
movement2D = [(1,0,0),(0,1,0),(-1,0,0),(0,-1,0)] #right, up, left, down #top-down

#Coordinate(AKA: mazeSize or location) is of format: (int),(int, int), or (int, int, int) for 1, 2, or 3 dimensions
#possibleMovement is a string that describes what types of movement actions the agent can make.
    #ie: "1D", "2D top-down"
    #not implemented yet: "2D side-view", "3D climb", "3D jump"

possibleMovementDict = {"1D": movement1D, "2D": movement2D}

MOVECAP = 300


'''
############################################################################################################
#----------------------------------------------------------------------------------------------------------#
#------------------------------------------Coordinate Functions--------------------------------------------#
#----------------------------------------------------------------------------------------------------------#
############################################################################################################
'''

#for the malmo-maze coordinate conversions do we have to add/ subtract 1 to the height?
def mazeToMalCoord(mazeCoord):
    #convert maze coordinates to malmo coordinates
    x,y,z = mazeCoord
    mazeCoord = (x,z,y)
    return sumCoordinates(mazeCoord, agentStart)

def malToMazeCoord(malCoord):
    #convert malmo coordinates to maze coordinates
    x,y,z = subCoordinates(malCoord, agentStart)
    return (int(x), int(z), int(y))

def seperateCoordinate(coordinate, default):
    if len(coordinate) == 1:
        x = coordinate[0]
        y,z = (default,default)
    elif len(coordinate) == 2:
        x,y = coordinate
        z=default
    elif len(coordinate) == 3:
        x,y,z = coordinate
    else:
        raise BaseException #TypeError("Wrong number of dimentions" + coordinate + "is not of length (1,2,3)")
    return x,y,z

def sumCoordinates(coord1, coord2, default = 0):
    return opCoordinates(coord1, coord2, "add", default)

def subCoordinates(coord1, coord2, default = 0):
    return opCoordinates(coord1, coord2, "sub", default)

def disCoordinates(coord1, coord2, default = 0):
    return opCoordinates(coord1, coord2, "dis", default)

def opCoordinates(coord1, coord2, op, default):
    assert len(coord1) == 3
    assert len(coord2) == 3
    x1,y1,z1 = seperateCoordinate(coord1, default)
    x2,y2,z2 = seperateCoordinate(coord2, default)
    if op == "add":
        return (x1+x2, y1+y2, z1+z2)
    elif op == "sub":
        return (x1-x2, y1-y2, z1-z2)
    elif op == "dis":
        return (x1-x2)**2+(y1-y2)**2+(z1-z2)**2
        