'''
Created on May 20, 2017

@author: Shintomo
'''
import MazeGen
import WorldSim
import AgentModule

TEST = True

def testRunEpisode(agent, eps = .5):
    while agent.isAlive():
        agent.makeMove(eps = eps)

def runNEpidsodes(agent, n, eps = .5, verbose = False):
    for i in range(n):
        print i
        testRunEpisode(agent, eps)
        if verbose:
            printAgentHistory(agent)
        agent.new_episode()
        



def printAgentHistory(agent):
    for move,reward in zip(agent.moveHistory[1:], agent.rewardHistory):
        print "Move: {}, Tile: {}, Reward: {}".format(move, agent.world._getTile(move), reward)

def PrintBestPath(agent):
    testRunEpisode(agent, eps = 0)
    printAgentHistory(agent)

if __name__ == '__main__':
    x=3
    y=3
    z=1
    mazeSize = (x,y,z)
    possibleMovement = "2D"

    lavaPercent = 1.0
    rewardCount = 1
    moveCap = 5

    maze = MazeGen.genMaze(mazeSize, possibleMovement, rewardCount = 2)
    maze.prettyPrint()
    
    if TEST:
        world = WorldSim.WorldSim(maze)
        agent = AgentModule.Agent(world)
        runNEpidsodes(agent, 3, .2, verbose=True)
        print "Best: "
        PrintBestPath(agent)
        print agent.qTable

        
        
    