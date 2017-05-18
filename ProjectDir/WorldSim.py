'''
Created on May 17, 2017

@author: Justin Veyna
'''
import MazeGen


emptyBlockReward, normalBlockReward, dangerBlockReward, rewardBlockReward = None, -1, -500, 100
blockList = [MazeGen.emptyBlock, MazeGen.normalBlock, MazeGen.dangerBlock, MazeGen.rewardBlock]
rewardList = [emptyBlockReward, normalBlockReward, dangerBlockReward, rewardBlockReward]

REWARDDICT = dict(zip(blockList,rewardList))
print REWARDDICT
class WorldSim():
    '''
    classdocs
    '''

    def __init__(self, worldMap, spawnLoc = (0,0,0)):
        '''
        worldMap: Maze class pre-gererated by MazeGen
        '''
        self.worldMap = worldMap
        self.agentLoc = spawnLoc
        self.rewardsRemaining = set(worldMap.rewardBlocks)
    
    def moveAgent(self, newLoc):
        '''returns reward here of new state'''
        self.agentLoc = newLoc
        if MazeGen.inMaze(self.worldMap.mazeSize, newLoc):
            return REWARDDICT[self.worldMap(newLoc)]
        else:
            return  REWARDDICT[MazeGen.dangerBlock]
    
    def getReward(self):
        '''return the reward of the action???? or  block the user is standing on'''
    
        
        