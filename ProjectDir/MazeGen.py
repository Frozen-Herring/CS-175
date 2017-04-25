'''
Created on Apr 24, 2017

@author: Justin Veyna
'''

from random import random
emptyBlock = "air"
normalBlock = "stone"
dangerBlock = "lava"
rewardBlock = "emerald"

movement1D = [(1,0,0),(-1,0,0)] #right, left
movement2D = [(1,0,0),(0,1,0),(-1,0,0),(0,-1,0)] #right, up, left, down #top-down

#Coordinate(AKA: mazeSize or location) is of format: (int),(int, int), or (int, int, int) for 1, 2, or 3 dimensions
#possibleMovement is a string that describes what types of movement actions the agent can make.
    #ie: "1D", "2D top-down"
    #not implemented yet: "2D side-view", "3D climb", "3D jump"

possibleMovementDict = {"1D": movement1D, "2D": movement2D}

def inMaze(mazeSize, location):
    #takes in 
    max_x,max_y,max_z = seperateCoordinate(mazeSize, 1)
    x, y, z = seperateCoordinate(location, 0)
    return x>=0 and y>=0 and z>=0 and x<max_x and y<max_y and z<max_z
    
def movementBlocked(mazeSize, location, movement=None):
    return False

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
    return _opCoordinates(coord1, coord2, "add", default)

def subCoordinates(coord1, coord2, default = 0):
    return _opCoordinates(coord1, coord2, "sub", default)

def disCoordinates(coord1, coord2, default = 0):
    return _opCoordinates(coord1, coord2, "dis", default)

def _opCoordinates(coord1, coord2, op, default):
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
        
        
        
        

def possibleMoves(mazeSize, location, possibleMovement, currentPath=[]):
    ret = set()
    if possibleMovement == "2D top-down" or possibleMovement == "1D" or possibleMovement == "2D":
        for movement in possibleMovementDict[possibleMovement]:
            move = sumCoordinates(location, movement)
            if inMaze(mazeSize, move):
                ret.add(move)
    else:
        raise BaseException #possibleMovement+"is not implemented yet"
    #print location, "->", ret
    return ret


def genPath(mazeSize, startBlock, endBlock, possibleMovement):
    
    currentPath = [startBlock]
    
    while currentPath[-1] != endBlock:
        posMoves = possibleMoves(mazeSize, currentPath[-1], possibleMovement, currentPath)
        move = _pickMove(posMoves, currentPath, endBlock)
        currentPath.append(move)
    return currentPath

def _pickMove(posMoves, currentPath, endBlock, impetus=1.5, momentum = .1, backtrackAversion = .3, backtrackCap = 500):
    #pick the next move somewhat randomly based on the impetus and momentum
    #score each block and regularize to create percents for each move
    '''
    impetus: How likely the path creator is to go towards the goal
    momentum: How unlikely the AI is to turn
    backtrackAversion: How unlikely the AI is to backtrack. Stonger for more recently visited tiles .
    '''
    scores = dict()
    #momentum pre-calculations
    lastMovement = None
    if len(currentPath) > 1:
        lastMovement = subCoordinates(currentPath[-1], currentPath[-2])
        momentumFavoredMove = sumCoordinates(currentPath[-1], lastMovement)
    #backtrackAversion pre-calculations
    reversedPath = currentPath[:]
    reversedPath.reverse()
    
    currentDistance = disCoordinates(currentPath[-1], endBlock)
    total = 0.0
    for move in posMoves:
        score = 100.0
        newDistance = disCoordinates(move, endBlock)
        if newDistance < currentDistance:
            score*=impetus
        if lastMovement != None and move != momentumFavoredMove:
            score*=momentum
        if move in currentPath[(-1*backtrackCap):]:
            timePast = reversedPath.index(move)
            score*=(1-backtrackAversion)#**timePast #todo odd behavior
        scores[move] = score
        '''
        if score != 0:
            print score
        '''
        total+=score
    #print "total", total
    randNum = random()
    for move in posMoves:
        newScore = scores[move]/total
        scores[move]= newScore
        randNum-=newScore
        if randNum <= 0:
            return move
    return posMoves[-1]#safety net if total does not add up to 1
        
        

def evalPath():
    #evaluate how good the maze is
    return 0
    
    
def genMaze(mazeSize, rewardCount=3, possibleMovement=movement2D):
    x,y,z = seperateCoordinate(mazeSize, 1)
    startBlock = (0,0,0)#hard coded for now
    endBlock = (x-1,y-1,0)#hard coded for now
    pass
    
    
    
    
    

if __name__ == '__main__':
    x=20
    y=50
    z=1
    print "x:", x, "y:",y, "z:",z
    mazeSize = (x,y,z)
    startBlock = (0,0,0)
    endBlock = (x-1,y-1,0)
    possibleMovement = "2D"
    p =  genPath(mazeSize, startBlock, endBlock, possibleMovement)
    setP = set(p)
    print "path", p
    print "num", len(p)
    print "num unique", len(set(p))
    print "num tiles", x*y
    toPrint = ""
    for i in range(x):
        for j in range(y):
            if (i,j,0) in setP:
                toPrint+="X"
            else:
                toPrint+=" "
            toPrint+=" "
        toPrint+="\n"
    print toPrint
    
'''
This gave passable results    
impetus=1.5, momentum = 1, backtrackAversion = 0 #mostly centeralized movement towards goal
impetus=1.5, momentum = .1, backtrackAversion = 0 #branch heavy linear paths
'''
                