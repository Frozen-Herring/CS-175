import json
import time

class WorldRep:
    def __init__(self, agentHost, worldState = None):
        '''Define a world state'''
        self.worldState = worldState
        self.agentHost = agentHost
        self.obs = None
        self.QAgentLoc = None
        self.rewardList = None
        self.lastReward = None


    def newEpisode(self, worldState): #Agent Calls this
        '''Clear all attributes and get new world state'''
        self.worldState = worldState
        self.obs = json.loads(worldState.observations[-1].text)
        self.QAgentLoc = (self.obs[u'XPos'], self.obs[u'YPos'])
        self.rewardList = None
        self.lastReward = None


    def _updateWorldState(self, worldState):
        '''Update attributes that may have changed'''
        self.self.worldState = worldState
        self.obs = json.loads(worldState.observations[-1].text)
        self.QAgentLoc = (self.obs[u'XPos'], self.obs[u'YPos'])
        self.rewardList = self.updateLastReward()
        self.lastReward = self.updateRewardList()

    def _updateLastReward(self): #getreward from move
        pass

    def _getInventoryItemsAsSet(self):
        rewardSet = set()
        for i in range(9):
            invKey = 'InventorySlot{}_item'.format(str(i))
            if invKey in self.obs:
                rewardSet.append(self.obvs[invKey])
        return rewardSet

    def createRewardList(self, rewardDict):
        inventoryItems = self._getInventoryItemsAsSet()
        rewardList = []

        for key in sorted(rewardDict.keys()):
            if key in inventoryItems:
                rewardList.append(1)
            else:
                rewardList.append(0)
        return rewardList

    def _updateRewardList(self): ################DEREKS STUFF
        pass

    def _getMoveCommandFromCoordTuple(moveCoordinates):
        '''Convert Agent Motion to malmo commands'''
        d = {(-1, 0, 0): "movewest 1",
             (1, 0, 0): "moveeast 1",
             (0, -1, 0): "movenorth 1",
             (0, 1, 0): "movesouth 1"}
        return d[moveCoordinates]

    def onDangerBlock(self): #Agent Calls this
        '''For contingency's sack, will never be true while the world is being updated'''
        return False

    def getRewardList(self): #Agent Calls this
        '''Put the structure and values here'''
        return self.rewardList

    def moveAgent(self, move = tuple()): #Agent Calls this
        '''Enacts the qAgents command and returns the reward from that command'''
        malmoMove = self._getMoveCommandFromCoordTuple(move)
        self.agentHost.sendCommand(malmoMove)
        time.sleep(0.1)
        self.updateLastReward()
        return self.lastReward