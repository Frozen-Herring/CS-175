'''
Created on May 20, 2017

@author: Shintomo
'''
import MazeGen
import WorldSim
import AgentModule
from SaveLoader  import MazeSaveLoader
from random import randrange
from CoordinateUtils import MOVECAP
TEST = True
def testRunEpisode(agent, eps = .5, verbose = False):
    i = 0
    while (agent.isAlive() or agent.moveHistory[-1] == agent.world.worldMaze.endBlock) and i < MOVECAP:
        agent.makeMove(eps = eps, verbose = verbose)
        i+=1

def runNEpidsodes(agent, n, eps = .5, verbose = False):
    for i in range(n):
        if i%1000==0:
            print(i)
        testRunEpisode(agent, eps)
        if verbose:
            printAgentHistory(agent)
        agent.new_episode()
        

def PrintBestPath(agent):
    testRunEpisode(agent, eps = 0)
    print(agent.moveHistory)


def printAgentHistory(agent):
    for move,reward in zip(agent.moveHistory[1:], agent.rewardHistory):
        print "Move: {}, Tile: {}, Reward: {}".format(move, agent.world._getTile(move), reward)

if __name__ == '__main__':   
    maze = MazeSaveLoader().getMaze()
    maze.prettyPrint()

    if TEST:
        world = WorldSim.WorldSim(maze)
        agent = AgentModule.Agent(world)
        runNEpidsodes(agent, 50000, .2, verbose=False)
        print "Best: "
        PrintBestPath(agent)
        print agent.qTable
    



