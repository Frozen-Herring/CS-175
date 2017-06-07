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
    for i in range(5,21,3):
        for j in range(1,6):
            j /= 5.0
            for k in range(1,6):
                k /= 5.0
                ret.append((i,j,k))
    return ret
                

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
    
    def runOptimizer(self, verbose=True):
        resultsAsString = ""
        keys = genBins()
        scores = []
        lowestVal = self.maxEps
        bestVals = None
        header = "avg. episodes\tn\talpha\tgamma\tentire val list"
        resultsAsString += header
        if verbose: print header
        for vals in keys:
            avgValList = []
            for i in range(2):
                avgValList.append(self.runToOptimal(vals))
            val = float(sum(avgValList))/len(avgValList)
            currentLine = str(val) + "\t" + str(vals[0]) + "\t" + str(vals[1]) + "\t" + str(vals[2]) + "\t" + str(avgValList)
            resultsAsString += "\n" + currentLine
            if verbose: print currentLine
            if val<lowestVal:
                lowestVal = val
                bestVals = vals
            scores.append((vals, val))
        self.optimal = (lowestVal, bestVals)
        with open("agentOptimizerResults.csv", "w") as f:
            f.write(resultsAsString)
        print(scores)
    
    def assignVals(self, vals):
        n, alpha, gamma = vals
        self.agent.n = int(n)
        self.agent.alpha = alpha
        self.agent.gamma = gamma    
    
    def runToOptimal(self, vals, verbose = False):
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


    def derekRunOptimizer(self):
        keys = genBins()
        scores = []
        lowestVal = self.maxEps
        bestVals = None
        print "avg. episodes\tn\talpha\tgamma\tentire episode list"
        for vals in keys:
            avgValList = []
            for i in range(100):
                avgValList.append(self.runUntilMazeSolved(vals, verbose=False))
            val = float(sum(avgValList))/len(avgValList)
            print str(val) + "\t" + str(vals[0]) + "\t" + str(vals[1]) + "\t" + str(vals[2]) + "\t" + str(avgValList)
            if val<lowestVal:
                lowestVal = val
                bestVals = vals
            scores.append((vals, val))
        self.optimal = (lowestVal, bestVals)
        print(scores)

    def runUntilMazeSolved(self, vals, verbose=True):
        self.agent.completeReset()
        self.assignVals(vals)

        while not self.agent.world.finishedMaze():
            i = 0
            self.agent.new_episode(verbose=False)
            while i < MOVECAP and self.agent.isAlive() and not self.agent.world.finishedMaze():
                self.agent.makeMove(eps=self.eps, verbose=False)
                i += 1
        if verbose: print str(vals) + ":\n - episodes: " + str(self.agent.episodeCount) + "\n - score: " + str(self.agent.bestScoreSoFar)
        return self.agent.episodeCount


    
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