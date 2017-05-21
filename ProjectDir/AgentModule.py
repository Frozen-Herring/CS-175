import MalmoPython as Malmo
from _collections import defaultdict
import random
import CoordinateUtils


qTable_DEFAULT = 0
'''
##################################################################
#--------------------------todo----------------------------------#
##################################################################

1:Use QLearning library?
2:makeMove function (incomplete)
    -chose move
    -make move
    -update q table
3:Add run episode (or make this a separate module?????)
    -make moves until max moves or "dead"

##################################################################
#--------------------------\todo---------------------------------#
##################################################################
'''

def createQTable():
    innerDef = lambda: qTable_DEFAULT
    outerDef = lambda: defaultdict(innerDef)
    return defaultdict(outerDef) #qTable[state][action][projectedReward]

class Agent:
    def __init__(self, world, start=(0,0,0), n=1, alpha=0.3, gamma=1.0, moveCap = 100):

        self.start = start #starting square
        
        self.world = world # keep a reference to the world... TODO: evaluate whether or not this is a good idea
        self.ourAgent = Malmo.AgentHost()
        self.moveCap = moveCap
        
        '''Q Learning'''
        self.n = n #num of states back to update in the qTable
        self.alpha = alpha #learning rate
        self.gamma = gamma #discount factor
        self.qTable = createQTable()
        '''end Q Learning'''
        
        '''episodic variables'''
        self.moveCount = 0
        self.moveHistory = [start] # [locs]... list of the locs we traversed so far...
        self.actionHistory = []
        self.rewardHistory = []
        self.rewardsLooted = [0 for _ in range(len(world.getRewardList()))]
        '''end episodic variables'''
    
    def new_episode(self):
        self.moveHistory = [self.start]
        self.actionHistory = []
        self.rewardHistory = []
        self.rewardsLooted = [0 for _ in range(len(self.world.getRewardList()))]
        self.moveCount = 0
        self.world.newEpisode()
        
    def getCurrentState(self):
        #returns (curLoc, itemsLooted)
        return (self.moveHistory[-1], tuple(self.rewardsLooted))
    
    def isAlive(self):
        return self.moveCap > self.moveCount and not self.world.onDangerBlock() 
    
    def getRawardTotal(self):
        return sum(self.rewardHistory)
    
    def makeMove(self, eps = .5):
        possibleMoves = CoordinateUtils.movement2D #hard-coded 2D movement
        moveToTake = self.chooseAction(possibleMoves, eps)
        self.moveHistory.append(CoordinateUtils.sumCoordinates(moveToTake, self.moveHistory[-1]))
        
        reward = self.world.moveAgent(moveToTake)
        self.rewardHistory.append(reward)
        self.updateQTable()
        
        self.moveCount += 1

    def chooseAction(self, possibleMoves, eps, testing = False):
        if testing:
            #todo: return random move in possibleMoves
            rand = random.randrange(len(possibleMoves))
            return possibleMoves[rand]
        else:
            rnd = random.random()
            if rnd < eps:
                a = random.randint(0, len(possibleMoves) - 1)
                return possibleMoves[a]
            else:
                return self._bestMove(possibleMoves)
    

    ########################################################################################################
    #-----------------------------------------QTable Code--------------------------------------------------#
    ########################################################################################################
    
    def updateQTable(self):
        n = self.moveCount if self.moveCount < self.n else self.n
        print range(-n, 0)
        for i in range(-n, 0):
            #for the past n state/action pairs
            G = self.rewardHistory[-1]
            G += self.gamma ** -(i+1) * self._optimalValue(self.moveHistory[-1])
            G-= self.qTable[self.moveHistory[-1]][self.actionHistory[-1]]
            G*= self.alpha
            print G
            self.q_table[self.moveHistory[-1]][self.actionHistory[-1]] += G
    
    def _optimalValue(self, state):
        possible = [value for _, value in self.qTable[state].items()]
        if len(possible) == 0:
            return 0
        else:
            return max(possible)
    
    def _bestMove(self, possibleMoves):
        posBest = []
        bestReward = -10000
        for i, action in enumerate(possibleMoves):
            if self.qTable[self.moveHistory[-1]][action] > bestReward:
                bestReward = self.qTable[self.moveHistory[-1]][action]
                posBest = [i]
            elif self.qTable[self.moveHistory[-1]][action] == bestReward:
                posBest.append(i)
        a = random.randint(0, len(posBest) - 1)
        return possibleMoves[posBest[a]]
    
    ########################################################################################################
    #-----------------------------------------Depreciated Code---------------------------------------------#
    ########################################################################################################
    
    
    
        
    
    
    
    """
    def update(self, moveToTake):
        ''' (self, int) -> None... updates moveHistory and rewardSum with the consequence of taking the move'''
        self.moveHistory.append(moveToTake) # add the move we took to moveHistory
        # TODO: update rewardSum... possibly something like "self.rewardSum += self.world.blockRewardDict[moveToTake] + self.world.qTableDict[moveToTake]
        # TODO: update self.world.expectedBlockRewardDict by distributing our rewardSum through all blocks in self.moveHistory
        # TODO: if we hit lava, set self.hitLava to true
        # TODO: if we hit a reward block, remrove it from self.remainingRewards... "if self.world.blocks[moveToMake] == 'emerald_block": self.remainingRewards.remove(moveToMake)

    def makePath(self, N):#not sure if we need this? or should this just be run
    ''' (self, int) -> None
        Continually call makeMove N times, or until we hit lava, or until remainingRewards is empty '''
        
    count = 0
    while count < N and not self.hitLava:
        self.makeMove()
        count += 1
        
    
    
    def chooseMove(self, possibleMoves):
        ''' (self, [int] -> int... use expectedRewardDict and blockReward and a RNG to choose a move'''
        for move in possibleMoves:
            expectedReward = self.world.expectedRewardDict[move]
            blockReward = self.world.blockRewardDict[move]
            # TODO: use expectedReward and blockReward to choose a move
    """
    


