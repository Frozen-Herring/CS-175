'''
Created on Jun 3, 2017

@author: Shintomo
'''
import MazeGen
import WorldSim
import AgentModule
from scipy.optimize import minimize


class Optimizer:
    def __init__(self, agent, world):
        self.agent=agent
        self.world=world
        

def getAnalytics(Agent):
    pass

def runOptimizer(maze):
    #n, alpha, gamma
    x = [1,.5,.5]
    bounds = [(1,20),(0,1.0),(0,1.0)]
    agent = AgentModule.Agent(world)
    toCall =  lambda: runNEpidsodes(agent, 250, eps = .2) #count eps and end at found best path
    #TODO: just compare best reward/////////out dated: ->add agent.compareBestPath(bestPath) to check if agent has achieved desired path

def callBack(vals):
    #actual just make the callback agent.reset
    #reset agent
    #save vals to agent class
    pass


if __name__ == '__main__':
    pass