'''
Created on May 20, 2017

@author: Shintomo
'''
import MazeGen
import WorldSim
import AgentModule
import SaveLoader as sl
from random import randrange
from scipy.optimize import minimize
from CoordinateUtils import sumCoordinates
TEST = True

def testRunEpisode(agent, eps = .5, verbose = False):
    while agent.isAlive() or sumCoordinates(agent.moveHistory[-1], (1,1,1)) == agent.world.worldMaze.mazeSize: #TODO: add terminal block check
        agent.makeMove(eps = eps, verbose = verbose)

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
    f = raw_input("Enter a file name to load from: ")
    if f == "":
        x=7
        y=7
        z=1
        mazeSize = (x,y,z)
        possibleMovement = "2D"
        rewardCount = 3
        maze = MazeGen.genMaze(mazeSize, possibleMovement, rewardCount = rewardCount)
    else:
        f+="-maze.p"
        maze = sl.pickle_load(f)
    maze.prettyPrint()

    if TEST:
        world = WorldSim.WorldSim(maze)
        agent = AgentModule.Agent(world)
        runNEpidsodes(agent, 50000, .2, verbose=False)
        print "Best: "
        PrintBestPath(agent)
        print agent.qTable
    if f != "":
        f = raw_input("Enter a file name to save to: ")
        if f == "":
            f = str(randrange(0,9999999999))
        f+="-maze.p"
        maze = sl.pickle_save(maze, f)



