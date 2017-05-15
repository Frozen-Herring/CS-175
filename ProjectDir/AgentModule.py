import MalmoPython as Malmo
from _collections import defaultdict
import random

qTable_DEFAULT = 0

class Agent:
    def __init__(self, world, start=(0,0,0), n=1, alpha=0.3, gamma=1.0):

        self.start = start #starting square
        
        self.world = world # keep a reference to the world... TODO: evaluate whether or not this is a good idea
        
        self.n = n #num of states back to update in the qTable
        self.alpha = alpha #learning rate
        self.gamma = gamma #discount factor
        self.moveHistory = [start] # [coodinate]... list of the indices of blocks we traversed so far...
        self.actionHistory = []
        self.rewardHistory = []
        
        self.rewardSum = 0; # int... the sum of all the rewards gotten so far from currentPath
        self.ourAgent = Malmo.AgentHost()
        
        self.hitLava = False # bool... we set this to true when we hit lava
        self.qTable = defaultdict(lambda: defaultdict(lambda: qTable_DEFAULT)) #qTable[state][action][projectedReward]

    def get_current_state(self):
        #todo key made of inventory location and zombie location(???)
        return None
    
    
    def makePath(self, N):#not sure if we need this? or should this just b e run
        ''' (self, int) -> None
        Continually call makeMove N times, or until we hit lava, or until remainingRewards is empty '''
        
        count = 0
        while count < N and not self.hitLava:
            self.makeMove()
            count += 1

    def makeMove(self,testing = False):
        ''' (self, [int], '''
        if not testing:
            possibleMoves = ['movenorth 1', 'movesouth 1', 'moveeast 1', 'movewest 1']
            moveToTake = self.chooseMove(possibleMoves)
            directionAction = self.world.getDirectionActionForMove(self.moveHistory[-1], moveToTake)
            self.ourAgent.sendCommand(directionAction)
            self.update(moveToTake)

    def chooseMove(self, possibleMoves):
        ''' (self, [int] -> int... use expectedRewardDict and blockReward and a RNG to choose a move'''
        for move in possibleMoves:
            expectedReward = self.world.expectedRewardDict[move]
            blockReward = self.world.blockRewardDict[move]
            # TODO: use expectedReward and blockReward to choose a move

    def choose_action(self, possibleMoves, eps):
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
        
    def update_q_table(self, T, nextState):
        #must be called every action BEFORE the next state is appended to moveHistory
        for i in range(-1, -(len(self.actionHistory)+1)+self.n):
            #for the past n state/action pairs
            G = self.rewardHistory[-1]
            G = self.gamma ** -(i+1) * self._optimal_value(nextState)
            G-= self.qTable[self.moveHistory[-1]][self.actionHistory[-1]]
            G*= self.alpha
            self.q_table[self.moveHistory[-1]][self.actionHistory[-1]] += G
    
    def _optimal_value(self, state):
        for _, stateQTable in self.qTable.items():
            return max( [(value, action) for action, value in stateQTable.items()])
                
    
    
    ########################################################################################################
    #-----------------------------------------Depreciated Code---------------------------------------------#
    ########################################################################################################
    
    
    def update(self, moveToTake):
        ''' (self, int) -> None... updates moveHistory and rewardSum with the consequence of taking the move'''
        self.moveHistory.append(moveToTake) # add the move we took to moveHistory
        # TODO: update rewardSum... possibly something like "self.rewardSum += self.world.blockRewardDict[moveToTake] + self.world.qTableDict[moveToTake]
        # TODO: update self.world.expectedBlockRewardDict by distributing our rewardSum through all blocks in self.moveHistory
        # TODO: if we hit lava, set self.hitLava to true
        # TODO: if we hit a reward block, remrove it from self.remainingRewards... "if self.world.blocks[moveToMake] == 'emerald_block": self.remainingRewards.remove(moveToMake)



