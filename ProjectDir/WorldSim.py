'''
Created on May 17, 2017

@author: Justin Veyna
'''
import MazeGen

import CoordinateUtils



emptyBlockReward, normalBlockReward, dangerBlockReward, rewardBlockReward, terminalBlockReward= None, -1, -500, 100, 0
blockList = [CoordinateUtils.emptyBlock, CoordinateUtils.normalBlock, CoordinateUtils.dangerBlock, CoordinateUtils.rewardBlock, CoordinateUtils.terminalBlock]
rewardList = [emptyBlockReward, normalBlockReward, dangerBlockReward, rewardBlockReward, terminalBlockReward]
rewardForFinishingMazeWithAllItems = 100


class WorldSim():
    '''
    classdocs
    '''

    def __init__(self, worldMaze, spawnLoc = (0,0,0)):
        '''
        worldMaze: Maze class pre-gererated by MazeGen
        '''
        self.rewardDict = dict(zip(blockList,rewardList))
        self.worldMaze = worldMaze
        self.spawnLoc = spawnLoc
        self.agentLoc = spawnLoc
        self.rewardList = [0 for _ in self.worldMaze.rewardBlocks]
        self.totalRewards = 0
    
    def getRewardList(self):
        return self.worldMaze.rewardBlocks
    
    def getLoc(self):
        return self.agentLoc
    
    def newEpisode(self):
        self.agentLoc = self.spawnLoc
        self.rewardList = [0 for _ in self.worldMaze.rewardBlocks]
        for rewardBlock in self.worldMaze.rewardBlocks:
            self.worldMaze.set(rewardBlock, CoordinateUtils.rewardBlock, weak = False)
    
    def moveAgent(self, directionToMove):
        '''returns reward here of new state'''
        self.agentLoc = CoordinateUtils.sumCoordinates(directionToMove, self.agentLoc)
        return self._getReward()
    
    def onDangerBlock(self):
        return self._getTile() == CoordinateUtils.dangerBlock
    
    def _getTile(self, loc = None):
        if loc == None:
            loc = self.agentLoc
        if not MazeGen.inMaze(self.worldMaze.mazeSize, loc):#all tiles outside of maze are dangerBlocks
            return CoordinateUtils.dangerBlock
        return self.worldMaze[loc]
    
    def _getReward(self):
        if self.agentLoc in self.worldMaze.rewardBlocks:
            a = self.worldMaze.rewardBlocks.index(self.agentLoc)
            self.rewardList[a] = 1
        tile = self._getTile()
        if tile == CoordinateUtils.rewardBlock:#if it's a rewardBlock then turn it normal (can't be taken more than once)
            self.worldMaze.set(self.agentLoc, CoordinateUtils.normalBlock, weak = False)
        #print "tile: {}, reward: {}".format(tile, self.rewardDict[tile])
        if self.finishedMaze():
            reward = rewardForFinishingMazeWithAllItems
        else:
            reward = self.rewardDict[tile]
        self.totalRewards+=reward
        return reward

    def finishedMaze(self):
        return self.worldMaze.endBlock == self.agentLoc and sum(self.rewardList) == len(self.rewardList)
        

    
        
        