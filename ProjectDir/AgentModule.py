import MalmoPython as Malmo
from _collections import defaultdict
import random
import CoordinateUtils
from itertools import product as itproduct
import Tkinter as tk

qTable_DEFAULT = 0
'''
##################################################################
#--------------------------todo----------------------------------#
##################################################################

##################################################################
#--------------------------\todo---------------------------------#
##################################################################
'''

def createQTable():
    innerDef = lambda: qTable_DEFAULT
    outerDef = lambda: defaultdict(innerDef)
    return defaultdict(outerDef) #qTable[state][action][projectedReward]

class Agent:
    def __init__(self, world, start=(0,0,0), n=7, alpha=.6, gamma=.8, moveCap = 100):

        self.start = start #starting square
        
        self.world = world # keep a reference to the world... TODO: evaluate whether or not this is a good idea
        self.ourAgent = Malmo.AgentHost()
        self.moveCap = moveCap
        
        '''Q Learning'''
        self.n = n #num of states back to update in the qTable
        self.alpha = alpha #learning rate
        self.gamma = gamma #discount factor
        self.qTable = createQTable()
        '''draw'''
        scale = 40
        self.scale = scale
        root = tk.Tk()
        root.wm_title("Q-table")
        canvas = tk.Canvas(root, width=self.world.maze.x*scale, height=self.world.maze.y*scale, borderwidth=0, highlightthickness=0, bg="black")
        canvas.grid()
        root.update()
        self.canvas = canvas
        self.root = root
        '''end draw'''
        '''end Q Learning'''
        
        '''episodic variables'''
        self.moveCount = 0
        self.moveHistory = [start] # [locs]... list of the locs we traversed so far...
        self.actionHistory = []
        self.rewardHistory = []
        '''end episodic variables'''

        '''Analytics'''
        self.episodeCount = 0
        self.totalMoveCount = 0
        self.bestScoreSoFar = -999
        self.bestPathSoFar = []

        self.movesPerEpisode = []
        self.rewardScorePerEpisode = []
        self.rewardsCollectedPerEpisode = []
        '''End Analytics'''

    def updateAnalyticsBeforeNewEpisode(self, printInfo=False):
        self.episodeCount += 1

        if self.episodeCount > 1:
            # update move trackers
            self.totalMoveCount += self.moveCount
            self.movesPerEpisode.append(self.moveCount)

            # update reward trackers
            rewardSum = sum(self.rewardHistory)
            self.rewardScorePerEpisode.append(rewardSum)
            self.rewardsCollectedPerEpisode.append(sum(self.world.rewardList))
            if rewardSum > self.bestScoreSoFar:
                self.bestScoreSoFar = rewardSum
                self.bestPathSoFar = self.moveHistory

            if printInfo:
                print "analytics:"
                print " - total moves: " + str(self.totalMoveCount)
                print " - total episodes: " + str(self.episodeCount)
                print " - best score so far: " + str(self.bestScoreSoFar)
                print " - best path so far: " + str(self.bestPathSoFar)
                print " - moves per episode: " + str(self.movesPerEpisode)
                print " - reward score per episode " + str(self.rewardScorePerEpisode)
                print " - rewards collected per epsiode: " + str(self.rewardsCollectedPerEpisode)

    def clearAnalytics(self):
        self.episodeCount = 0
        self.totalMoveCount = 0
        self.bestScoreSoFar = -999
        self.bestPathSoFar = []

        self.movesPerEpisode = []
        self.rewardScorePerEpisode = []
        self.rewardsCollectedPerEpisode = []

    def new_episode(self, verbose = False, saveFile= False):
        self.updateAnalyticsBeforeNewEpisode(verbose)
        if saveFile:
            with open("analytics.csv", "w") as f:
                f.write("episode #\tmoves #\treward score\trewards collected")
                for i in range(self.episodeCount-1):
                    f.write("\n" + str(i) + "\t" + str(self.movesPerEpisode[i]) + "\t" + str(self.rewardScorePerEpisode[i]) + "\t" + str(self.rewardsCollectedPerEpisode[i]))
                    f.flush()
        self.moveHistory = [self.start]
        self.actionHistory = []
        self.rewardHistory = []
        self.moveCount = 0
        self.world.newEpisode()#TODO: interects with world

    def completeReset(self):
        self.new_episode()
        self.clearAnalytics()
        self.qTable = createQTable()

    def getCurrentState(self):
        #returns (curLoc, itemsLooted)
        return (tuple(self.world.rewardList), self.moveHistory[-1])
    
    def isAlive(self):
        if self.world.finishedMaze():
            return False
        return self.moveCap > self.moveCount and not self.world.onDangerBlock()
    
    def getRawardTotal(self):
        return sum(self.rewardHistory)
    
    def makeMove(self, eps = .1, verbose = False, learningType = True):
        self._draw()
        old_state = (tuple(self.world.rewardList), self.moveHistory[-1])
        possibleMoves = CoordinateUtils.movement2D #hard-coded 2D movement
        moveToTake = self.chooseAction(possibleMoves, eps)
        self.actionHistory.append(moveToTake)
        self.moveHistory.append(CoordinateUtils.sumCoordinates(moveToTake, self.moveHistory[-1]))
        
        reward = self.world.moveAgent(moveToTake)#TODO: interects with world

        self.rewardHistory.append(reward)
        self.moveCount += 1
        self.updateQTable(old_state)
        if learningType == True:#add lava punishment to all with q-learning
            if reward < -50: #TODO: ATTENTION HARD CODED: to check for lava
                for rl in self.allRewardStates():
                    old_state = (tuple(rl), self.moveHistory[-2])
                    self.updateQTable(old_state)
        if verbose:
            self.printStatus()
        
        

    def chooseAction(self, possibleMoves, eps, testing = False):
        if testing:
            rand = random.randrange(len(possibleMoves))
            return possibleMoves[rand]
        else:
            rnd = random.random()
            if rnd < eps:
                a = random.randint(0, len(possibleMoves) - 1)
                return possibleMoves[a]
            else:
                cur_state = (tuple(self.world.rewardList), self.moveHistory[-1])
                return self._bestMove(possibleMoves, cur_state)

    def allRewardStates(self, excludeCurrent = True):
        ret =[tuple(x) for x in itproduct([0,1], repeat = len(self.world.rewardList))]
        if excludeCurrent:
            ret.remove(tuple(self.world.rewardList))
        return ret
        

    def printStatus(self):
        print "make move..."
        print " - self.actionHistory = " + str(self.actionHistory)
        print " - self.rewardHistory = " + str(self.rewardHistory)
        print " - self.rewardsLooted = " + str(self.world.rewardList)
        #TODO: commented out due to inconsistancies with worldsim
        #print " - self.world.totalRewards = " + str(self.world.totalRewards)
        #print " - self.world.lastReward = " + str(self.world.lastReward)


    ########################################################################################################
    #-----------------------------------------QTable Code--------------------------------------------------#
    ########################################################################################################
    
    def updateQTable(self, old_state):
        n = self.moveCount if self.moveCount < self.n else self.n
        cur_state = (tuple(self.world.rewardList), self.moveHistory[-1])
        for i in range(-n, 0):
            #for the past n state/action pairs
            G = self.rewardHistory[-1]
            G += self.gamma ** -(i+1) * self._optimalValue(cur_state)
            G-= self.qTable[old_state][self.actionHistory[-1]]
            G*= self.alpha
            self.qTable[old_state][self.actionHistory[-1]] += G
    
    def _optimalValue(self, state):
        possible = [value for _, value in self.qTable[state].items()]
        if len(possible) == 0:
            return 0
        else:
            return max(possible)
    
    def _bestMove(self, possibleMoves, state):
        posBest = []
        bestReward = -10000
        for i, action in enumerate(possibleMoves):
            if self.qTable[state][action] > bestReward:
                bestReward = self.qTable[state][action]
                posBest = [i]
            elif self.qTable[state][action] == bestReward:
                posBest.append(i)
        a = random.randint(0, len(posBest) - 1)
        return possibleMoves[posBest[a]]
    def _draw(self):
        world_x = self.world.maze.x
        world_y = self.world.maze.y
        scale = self.scale
        curr_x, curr_y, _ = self.moveHistory[-1]
        self.canvas.delete("all")
        action_inset = 0.1
        action_radius = 0.1
        curr_radius = 0.2
        #action_positions = [ ( 0.5, 1-action_inset ), ( 0.5, action_inset ), ( 1-action_inset, 0.5 ), ( action_inset, 0.5 ) ]
        #action_positions = [ ( 1-action_inset, 0.5 ), ( 0.5, 1-action_inset ), ( action_inset, 0.5 ), ( 0.5, action_inset ) ]
        #action_positions = [ ( 0.5, 1-action_inset ), ( 1-action_inset, 0.5 ), ( 0.5, action_inset ), ( action_inset, 0.5 ) ]
        #action_positions = [ ( 0.5, action_inset ), ( 1-action_inset, 0.5 ), ( 0.5, 1-action_inset ), ( action_inset, 0.5 ) ]
        #action_positions = [ ( 0.5, action_inset ), ( action_inset, 0.5 ), ( 0.5, 1-action_inset ), ( 1-action_inset, 0.5 ) ]
        #action_positions = [ ( 0.5, 1-action_inset ), ( action_inset, 0.5 ), ( 0.5, action_inset ), ( 1-action_inset, 0.5 ) ]
        #action_positions = [ ( action_inset, 0.5 ), ( 0.5, 1-action_inset ), ( 1-action_inset, 0.5 ), ( 0.5, action_inset ) ]close?
        action_positions = [ ( action_inset, 0.5 ), ( 0.5, action_inset ), ( 1-action_inset, 0.5 ), ( 0.5, 1-action_inset ) ]
        # (NSWE to match action order)
        min_value = -10
        max_value = 10
        for x in range(world_x):
            for y in range(world_y):
                stateCoord = (x,y,0)
                s = (tuple(self.world.rewardList),stateCoord)
                self.canvas.create_rectangle( (world_x-1-x)*scale, (world_y-1-y)*scale, (world_x-1-x+1)*scale, (world_y-1-y+1)*scale, outline="#fff", fill="#000")
                for aInd in range(4):
                    action = CoordinateUtils.movement2D[aInd]
                    if not s in self.qTable:
                        continue
                    value = self.qTable[s][action]
                    color = 255 * ( value - min_value ) / ( max_value - min_value ) # map value to 0-255
                    color = max( min( color, 255 ), 0 ) # ensure within [0,255]
                    color_string = '#%02x%02x%02x' % (255-color, color, 0)
                    self.canvas.create_oval( (world_x - 1 - x + action_positions[aInd][0] - action_radius ) *scale,
                                             (world_y - 1 - y + action_positions[aInd][1] - action_radius ) *scale,
                                             (world_x - 1 - x + action_positions[aInd][0] + action_radius ) *scale,
                                             (world_y - 1 - y + action_positions[aInd][1] + action_radius ) *scale, 
                                             outline=color_string, fill=color_string )
        if curr_x is not None and curr_y is not None:
            self.canvas.create_oval( (world_x - 1 - curr_x + 0.5 - curr_radius ) * scale, 
                                     (world_y - 1 - curr_y + 0.5 - curr_radius ) * scale, 
                                     (world_x - 1 - curr_x + 0.5 + curr_radius ) * scale, 
                                     (world_y - 1 - curr_y + 0.5 + curr_radius ) * scale, 
                                     outline="#fff", fill="#fff" )
        self.root.update()

