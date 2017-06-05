'''
Created on Jun 3, 2017

@author: Shintomo
'''
import MazeGen
import WorldSim
import AgentModule
from scipy.optimize import minimize
from Main import runNEpidsodes
from CoordinateUtils import MOVECAP
from SaveLoader import MazeSaveLoader

def genBins():
    ret = []
    for i in range(1,21):
        for j in range(1,21):
            j /= 20.0
            for k in range(1,21):
                k /= 20.0
                ret.append((i,j,k))
                

class Optimizer:
    def __init__(self, maze):
        world=WorldSim.WorldSim(maze)
        self.maxEps = 100000
        self.eps = .1
        self.agent = AgentModule.Agent(world)
        self.optimal = None
        
    
    def runOptimizerContinuos_BROKEN(self):
        #n, alpha, gamma
        x = [2,.5,.5]
        bounds = ((1,20),(0,1.0),(0,1.0))
        toCall =  lambda vals: self.runToOptimal( vals)
        method="TNC"
        scale = (.001, 5000000, 5000000)
        self.optimal = minimize(fun = toCall, x0 = x, method = method, bounds = bounds, callback = self.callBack, options = {"maxiter":1000, "disp":True, "scale":scale})
    
    def runOptimizer(self):
        keys = genBins()
        scores = []
        lowest_val = self.maxEps
        best_vals = None
        
        for vals in keys:
            scores.append(self.runToOptimal(vals))
        i = max(zip())
    
    def assignVals(self, vals):
        n, alpha, gamma = vals
        self.agent.n = int(n)
        self.agent.alpha = alpha
        self.agent.gamma = gamma    
    
    def runToOptimal(self, vals, verbose = True):
        self.agent.completeReset()
        self.assignVals(vals)
        
        
        
        while self.agent.bestScoreSoFar < self.idealScore and self.agent.episodeCount < self.maxEps:
            i=0
            while (self.agent.isAlive() or self.agent.moveHistory[-1] == self.agent.world.worldMaze.endBlock) and i < MOVECAP:
                self.agent.makeMove(eps = self.eps, verbose = False)
                i+=1
            self.agent.new_episode(verbose = False)
        if verbose:
            print(vals)
            print("Num eps:", self.agent.episodeCount)
            print("Score:", self.agent.bestScoreSoFar)
            
        return self.agent.episodeCount

    def callBack(self, vals):
        pass
    
    def findBestScore(self):
        self.idealScore=-60
        pass
    
    def getAnalytics(self):
        pass
    
if __name__ == '__main__':
    msl = MazeSaveLoader()
    maze = msl.getMaze()
    optmzr = Optimizer(maze)
    optmzr.findBestScore()
    optmzr.runOptimizer()
    print(optmzr.optimal)
    print(msl.f)

'''
##################################################################
#--------------------------finds---------------------------------#
##################################################################

eps of .1 worked MARGINALLY better than eps .2
eps of .1 worked MARGINALLY better then eps .05
'''