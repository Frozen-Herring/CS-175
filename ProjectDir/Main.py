'''
Created on May 20, 2017

@author: Shintomo
'''
import MazeGen
import WorldSim
import AgentModule

TEST = True

def testRunEpisode(agent):
    while agent.isAlive():
        agent.makeMove()

def printAgentHistory(agent):
    for move,reward in zip(agent.moveHistory[1:], agent.rewardHistory):
        print "Move: {}, Tile: {}, Reward: {}".format(move, agent.world._getTile(move), reward)


if __name__ == '__main__':
    x=20
    y=50
    z=1
    mazeSize = (x,y,z)
    possibleMovement = "2D"

    lavaPercent = 1.0
    rewardCount = 5

    maze = MazeGen.genMaze(mazeSize, possibleMovement)
    #maze.prettyPrint()
    
    if TEST:
        world = WorldSim.WorldSim(maze)
        agent = AgentModule.Agent(world)
        testRunEpisode(agent)
        printAgentHistory(agent)

        
        
    