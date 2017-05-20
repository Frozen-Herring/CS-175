'''
Created on May 20, 2017

@author: Shintomo
'''
import MazeGen
import WorldSim

TEST = True

def testRunEpisode(Agent):

if __name__ == '__main__':
    x=20
    y=50
    z=1
    mazeSize = (x,y,z)
    possibleMovement = "2D"

    lavaPercent = 1.0
    rewardCount = 5

    maze = MazeGen.genMaze(mazeSize, possibleMovement)
    maze.prettyPrint()
    
    if TEST:
        world = WorldSim.WorldSim(maze)
        
        
    