'''
Created on May 17, 2017

@author: Justin Veyna
'''
import MazeGen
import CoordinateUtils



emptyBlockReward, normalBlockReward, dangerBlockReward, rewardBlockReward = None, -1, -500, 100
blockList = [CoordinateUtils.emptyBlock, CoordinateUtils.normalBlock, CoordinateUtils.dangerBlock, CoordinateUtils.rewardBlock]
rewardList = [emptyBlockReward, normalBlockReward, dangerBlockReward, rewardBlockReward]


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
        self.agentLoc = spawnLoc
    
    def getRewardList(self):
        return self.worldMaze.rewardBlocks
    
    def getLoc(self):
        return self.agentLoc
    
    def getTile(self, loc = None):
        if loc == None:
            loc = self.agentLoc
        if not MazeGen.inMaze(self.worldMaze.mazeSize, loc):#all tiles outside of maze are dangerBlocks
            return CoordinateUtils.dangerBlock
        return self.worldMaze[loc]
    
    def moveAgent(self, directionToMove):
        '''returns reward here of new state'''
        self.agentLoc = CoordinateUtils.sumCoordinates(directionToMove, self.agentLoc)
        return self._getReward()
    
    def _getReward(self):
        tile = self.getTile()
        if tile == CoordinateUtils.rewardBlock:#if it's a rewardBlock then turn it normal (can't be taken more than once)
            self.worldMaze.set(self.agentLoc, CoordinateUtils.normalBlock, weak = False)    
        return self.rewardDict[tile]
        
    def onDangerBlock(self):
        return self.getTile() == CoordinateUtils.dangerBlock
    
        
        