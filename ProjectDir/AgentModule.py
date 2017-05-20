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


class Agent:
    def __init__(self, world, start=(0,0,0), n=1, alpha=0.3, gamma=1.0):

        self.start = start #starting square
        
        self.world = world # keep a reference to the world... TODO: evaluate whether or not this is a good idea
        
        '''Q Learning constants'''
        self.n = n #num of states back to update in the qTable
        self.alpha = alpha #learning rate
        self.gamma = gamma #discount factor
        '''end Q Learning constants'''
        self.moveHistory = [start] # [locs]... list of the locs we traversed so far...
        self.actionHistory = []
        self.rewardHistory = []
        self.rewardsLooted = [0 for _ in range(world.getRewardList())]
        
        self.rewardSum = 0; # int... the sum of all the rewards gotten so far from currentPath
        self.ourAgent = Malmo.AgentHost()
        
        self.hitLava = False # bool... we set this to true when we hit lava
        self.qTable = defaultdict(lambda: defaultdict(lambda: qTable_DEFAULT)) #qTable[state][action][projectedReward]

    def getCurrentState(self):
        #returns (curLoc, itemsLooted)
        return (self.moveHistory[-1], tuple(self.rewardsLooted))
    

    def makeMove(self,testing = True, eps = .5):
        ''' (self, [int], 
        MISSING A LOT
        '''
        if testing:
            possibleMoves = CoordinateUtils.movement2D #hard-coded 2D movement
            moveToTake = self.chooseAction(possibleMoves, eps)
            reward = self.world.moveAgent(moveToTake)
            self.update(reward)
        if not testing:
            possibleMoves = None
            self.world.moveAgent()


    def chooseAction(self, possibleMoves, eps, testing = True):
        if testing:
            #todo: return random move in possibleMoves
            pass
        else:
            rnd = random.random()
            if rnd < eps:
                a = random.randint(0, len(possibleMoves) - 1)
                return possibleMoves[a]
            else:
                posBest = []
                bestReward = -10000
                for i, action in enumerate(possibleMoves):
                    if self.qTable[self.moveHistory[-1]][action] > bestReward:
                        bestReward = self.qTable[self.moveHistory[-1]][action]
                        posBest = [i]
                    elif self.qTable[self.moveHistory[-1]][action] == bestReward:
                        posBest += [i]
                a = random.randint(0, len(posBest) - 1)
                return possibleMoves[posBest[a]]
    
    def update(self, reward):
        pass#todo: qLearning

    ########################################################################################################
    #-----------------------------------------Depreciated Code---------------------------------------------#
    ########################################################################################################
    
    
    
        
    ########################################################################################################
    #-----------------------------------------QTable Code--------------------------------------------------#
    ########################################################################################################
    """
    def updateQTable(self, T, nextState):
        #must be called every action BEFORE the next state is appended to moveHistory
        for i in range(-1, -(len(self.actionHistory)+1)+self.n):
            #for the past n state/action pairs
            G = self.rewardHistory[-1]
            G = self.gamma ** -(i+1) * self._optimalValue(nextState)
            G-= self.qTable[self.moveHistory[-1]][self.actionHistory[-1]]
            G*= self.alpha
            self.q_table[self.moveHistory[-1]][self.actionHistory[-1]] += G
    
    def _optimalValue(self, state):
        for _, stateQTable in self.qTable.items():
            return max( [(value, action) for action, value in stateQTable.items()])
    """
    
    
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
    


