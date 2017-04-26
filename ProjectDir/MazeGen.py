'''
Created on Apr 24, 2017

@author: Justin Veyna
'''
'''
PLEASE READ:
File still needs to be cleaned up a lot documentation wise and there are a lot of general use functions that can surely be put in another file.
DO NOT EDIT for now
'''

from random import random, shuffle

'''
############################################################################################################
#----------------------------------------------------------------------------------------------------------#
#----------------------------------------------Constants---------------------------------------------------#
#----------------------------------------------------------------------------------------------------------#
############################################################################################################
'''
emptyBlock = " "#"air"#todo 
normalBlock = "X"#"stone"
dangerBlock = "."#"lava"#todo
rewardBlock = "O"#"emerald"

movement1D = [(1,0,0),(-1,0,0)] #right, left
movement2D = [(1,0,0),(0,1,0),(-1,0,0),(0,-1,0)] #right, up, left, down #top-down

#Coordinate(AKA: mazeSize or location) is of format: (int),(int, int), or (int, int, int) for 1, 2, or 3 dimensions
#possibleMovement is a string that describes what types of movement actions the agent can make.
    #ie: "1D", "2D top-down"
    #not implemented yet: "2D side-view", "3D climb", "3D jump"

possibleMovementDict = {"1D": movement1D, "2D": movement2D}
'''
############################################################################################################
#----------------------------------------------------------------------------------------------------------#
#------------------------------------------Coordinate Functions--------------------------------------------#
#----------------------------------------------------------------------------------------------------------#
############################################################################################################
'''
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
        
        
'''
############################################################################################################
#----------------------------------------------------------------------------------------------------------#
#-------------------------------------------Path Generation------------------------------------------------#
#----------------------------------------------------------------------------------------------------------#
############################################################################################################
'''        
        

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
        
        
'''
############################################################################################################
#----------------------------------------------------------------------------------------------------------#
#--------------------------------------------Maze Generation-----------------------------------------------#
#----------------------------------------------------------------------------------------------------------#
############################################################################################################
'''  
class Maze():
    def __init__(self, mazeSize, lavaPercent=.5, rewardCount=5):
        self.lavaPercent = lavaPercent
        self.rewardCount = rewardCount
        self.x, self.y, self.z = mazeSize
        self.maze=[]
        for _ in range(self.x):
            l1=[]
            for _ in range(self.y):
                l2=[]
                for _ in range(self.z):
                    l2.append(None)
                l1.append(l2)
            self.maze.append(l1)
                    

    def __getitem__(self, key):
        x,y,z = key
        return self.maze[x][y][z]
    
    def __setitem__(self, key, value):
        x,y,z = key
        self.maze[x][y][z] = value
    
    def set(self, location, blockType, weak=True):
        if self[location] == None or not weak:
            self[location] = blockType
    
    def fill_maze(self, pSet):
        for x in range(self.x):
            for y in range(self.y):
                for z in range(self.z):
                    self._dictateBlock((x,y,z), pSet)
        self._addRewards(pSet)
        self._fillAir()
                    
    def _dictateBlock(self, location, pSet):
        x,y,z = location
        if location in pSet:
            #if part of path
            for a in range(z+1):
                self.set((x,y,a), normalBlock)
        elif z==0:
            if random() <= self.lavaPercent:
                self.set(location, dangerBlock)
            else:
                self.set(location, normalBlock)
    
    def _addRewards(self, pSet):
        pathBlocks = list(pSet)
        shuffle(pathBlocks)
        for i in range(self.rewardCount):
            self.set(pathBlocks[i], rewardBlock, False)
    
    def _fillAir(self):
        for x in range(self.x):
            for y in range(self.y):
                for z in range(self.z):
                    self.set((x,y,z), emptyBlock)
    
    def prettyPrint(self):
        #2D ONLY
        toPrint=""
        for x in self.maze:
            for y in x:
                for z in y:
                    if z != None:
                        toPrint+=z[0]
                    else:
                        toPrint+="_"
                toPrint+=" "
            toPrint+="\n"
        print toPrint
        
    
def genMaze(mazeSize, lavaPercent=1.0, rewardCount=5, possibleMovement="2D"):
    x,y,z = seperateCoordinate(mazeSize, 1)
    startBlock = (0,0,0)#hard coded for now
    endBlock = (x-1,y-1,0)#hard coded for now
    
    p =  genPath(mazeSize, startBlock, endBlock, possibleMovement)
    pSet = set(p)
    
    maze = Maze(mazeSize, lavaPercent, rewardCount)
    maze.fill_maze(pSet)
    return maze
    
    

'''
############################################################################################################
#----------------------------------------------------------------------------------------------------------#
#--------------------------------------------Post Analytics------------------------------------------------#
#----------------------------------------------------------------------------------------------------------#
############################################################################################################
'''  

def evalPath():
    #evaluate how good the maze is
    return 0

def pathDetails(p):
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

def test_maze():
    mazeSize =(5,5,1)
    maze = Maze(mazeSize)
    maze.prettyPrint()
    print (0,0,0), maze[(0,0,0)]
    maze.set((0,0,0), normalBlock)
    print (0,0,0), maze[(0,0,0)]
    print (1,0,0), maze[(1,0,0)]
    maze.set((1,0,0), dangerBlock)
    print (1,0,0), maze[(1,0,0)]
    #maze.fill_maze(pSet)
    maze.prettyPrint()
    
if __name__ == '__main__':
    #maze specific constants
    x=20
    y=50
    z=1
    print "x:", x, "y:",y, "z:",z
    mazeSize = (x,y,z)

    possibleMovement = "2D"
    
    
    #Path Generation Test Code
    #startBlock = (0,0,0)
    #endBlock = (x-1,y-1,0)
    #p =  genPath(mazeSize, startBlock, endBlock, possibleMovement)
    #pathDetails(p)
    
    #Maze Generation Test Code
    #test_maze()
    lavaPercent = 1.0
    rewardCount = 5
    maze = genMaze(mazeSize, possibleMovement)
    maze.prettyPrint()



'''
FINDINGS:

This gave passable results
impetus=1.5, momentum = 1, backtrackAversion = 0 #mostly centeralized movement towards goal
impetus=1.5, momentum = .1, backtrackAversion = 0 #branch heavy linear paths
impetus=1.5, momentum = .1, backtrackAversion = .3, backtrackCap = 500 # mostly same as above
'''
                