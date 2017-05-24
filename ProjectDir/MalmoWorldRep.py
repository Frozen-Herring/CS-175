import json
import time

class WorldRep:
    def __init__(self, agentHost, worldState = None, rewards = {}):
        '''Define a world state'''
        self.sortedRewards = sorted(rewards.keys())
        self.agentHost = agentHost
        self.worldState = worldState
        self.obs = None
        self.QAgentLoc = (0.5, 227, 0.5)
        self.rewardList = [0 for _ in rewards.keys()]
        self.totalRewards = 0
        self.lastReward = 0


    def newEpisode(self, worldState): #Agent Calls this
        '''Clear all attributes and get new world state'''
        self.worldState = worldState
        self.obs = json.loads(worldState.observations[-1].text)
        self.QAgentLoc = (self.obs[u'XPos'], self.obs[u'YPos'])
        self.rewardList = None
        self.totalRewards = 0
        self.lastReward = 0


    def _updateWorldRep(self, worldState):
        '''Update attributes that may have changed'''
        self.worldState = worldState
        self.obs = json.loads(worldState.observations[-1].text)
        self.QAgentLoc = (self.obs[u'XPos'], self.obs[u'YPos'])
        self._updateAllRewards()

    def _updateAllRewards(self): #getreward from move
        self.rewardList = self._createRewardList()
        self.lastReward = self.worldState.rewards[-1].getValue() - self.totalRewards #ehhhhhh probably
        self.totalRewards = self.worldState.rewards[-1].getValue()

    def _getInventoryItemsAsSet(self):
        rewardSet = set()
        for i in range(9):
            invKey = 'InventorySlot{}_item'.format(str(i))
            if invKey in self.obs:
                rewardSet.add(self.obs[invKey])
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
        time.sleep(.5)
        self._updateWorldRep(self.agentHost.peekWorldState())
        return self.lastReward
