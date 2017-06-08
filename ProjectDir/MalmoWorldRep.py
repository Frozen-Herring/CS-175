import json
import time
from CoordinateUtils import rewardDict

class WorldRep:
    def __init__(self, agentHost, maze, worldState = None):
        '''Define a world state'''
        self.maze = maze
        self.sortedRewards = sorted(rewardDict.keys())[0:self.maze.rewardCount]
        self.agentHost = agentHost
        self.worldState = worldState
        self.obs = None
        self.QAgentLoc = (0.5, 227, 0.5)
        self.rewardList = [0 for _ in rewardDict.keys()]
        self.totalRewards = 0
        self.lastReward = 0
        self.endBlock = (maze.endBlock[0]+.5, maze.endBlock[1]+.5)
        self.inventoryItemsAsSet = set()
        self.finishMazeReward = 10


    def newEpisode(self): #Agent Calls this
        '''Clear all attributes and get new world state'''
        self.obs = json.loads(self.worldState.observations[-1].text)
        self.QAgentLoc = (self.obs[u'XPos'], self.obs[u'ZPos'])
        self.rewardList = [0 for _ in self.sortedRewards]
        self.totalRewards = 0
        self.lastReward = 0
        self.inventoryItemsAsSet = set()


    def _updateWorldRep(self, worldState):
        '''Update attributes that may have changed'''
        self.worldState = worldState
        self.obs = json.loads(worldState.observations[-1].text)
        self.QAgentLoc = (self.obs[u'XPos'], self.obs[u'ZPos'])
        self._updateAllRewards()

    def _updateAllRewards(self): #getreward from move
        self.rewardList = self._createRewardList()
        self.lastReward = self.worldState.rewards[-1].getValue() - self.totalRewards #ehhhhhh probably
        if self.finishedMaze():
            self.lastReward = self.finishMazeReward
        self.totalRewards = self.worldState.rewards[-1].getValue()

    def _getInventoryItemsAsSet(self):
        rewardSet = set()
        for i in range(9):
            invKey = 'InventorySlot_{}_item'.format(str(i))
            if invKey in self.obs:
                rewardSet.add(self.obs[invKey])
        self.inventoryItemsAsSet = rewardSet
        return rewardSet

    def _createRewardList(self):
        inventoryItems = self._getInventoryItemsAsSet()
        rewardList = []

        for key in self.sortedRewards:
            if key in inventoryItems:
                rewardList.append(1)
            else:
                rewardList.append(0)
        return rewardList

    def _getMoveCommandFromCoordTuple(self, moveCoordinates):
        '''Convert Agent Motion to malmo commands'''
        d = {(-1, 0, 0): "movewest 1",
             (1, 0, 0): "moveeast 1",
             (0, -1, 0): "movenorth 1",
             (0, 1, 0): "movesouth 1"}
        return d[moveCoordinates]

    def onDangerBlock(self): #Agent Calls this
        '''For contingency reasons, will never be true while the world is being updated'''
        return False

    def getRewardList(self): #Agent Calls this
        return self.rewardList

    def moveAgent(self, move = tuple()): #Agent Calls this
        '''Enacts the qAgents command and returns the reward from that command'''
        malmoMove = self._getMoveCommandFromCoordTuple(move)
        self.agentHost.sendCommand(malmoMove)
        time.sleep(.1)
        self._updateWorldRep(self.agentHost.peekWorldState())
        return self.lastReward

    def finishedMaze(self):
        # print "agent is on end block: " + str(self.endBlock == self.QAgentLoc) + "... " + str(self.endBlock) + "==" + str(self.QAgentLoc)
        # print " - agent has all rewards:" + str(sum(self.rewardList) == len(self.rewardList)) + "... " + str(sum(self.rewardList)) + "==" + str(len(self.rewardList))
        # print " returning: " + str(self.endBlock == self.QAgentLoc and sum(self.rewardList) == len(self.rewardList))
        # if the agent is on the end block AND we have collected all the rewards, we finished the maze
        return self.endBlock == self.QAgentLoc and sum(self.rewardList) == len(self.rewardList)



