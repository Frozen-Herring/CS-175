'''
Created on May 21, 2017

@author: Justin Veyna
'''
try:
    from cPickle import Pickler, Unpickler
except ImportError:
    from pickle import Pickler, Unpickler

from random import randrange
from MazeGen import genMaze

def pickle_save(obj, file_name):
    f = open(file_name, "wb")
    if f != None:
        p = Pickler(f, protocol=2)
        p.dump(obj)
        f.close()

def pickle_load(file_name):
    f = open(file_name, "rb")
    obj = None
    if f != None:
        u = Unpickler(f)
        obj = u.load()
        f.close()
    return obj

class MazeSaveLoader:
    def __init__(self, x = 5, y = 5, rewardCount = 3):
        self.f = ""
        self.maze = None
        self.mazeSize = (x,y,1)
        self.rewardCount = rewardCount
        self.askLoadMaze()
        self.askSaveMaze()
    
    def getMaze(self):
        return self.maze
    
    def askSaveMaze(self):
        if self.f == "":
            self.f = raw_input("Enter a file name to save to: ")     
            if self.f == "":
                self.f = str(randrange(0,9999999999))
            self.f+="-maze.p"
            self._saveMaze()
    
    def _saveMaze(self):
        pickle_save(self.maze, self.f)
    
    def askLoadMaze(self):
        self.f = raw_input("Enter a file name to load from: ")
        if self.f == "":
            possibleMovement = "2D"
            self.maze = genMaze(self.mazeSize, possibleMovement, rewardCount = self.rewardCount)
        else:
            self.f+="-maze.p"
            self.maze = pickle_load(self.f)    
    
    def insertMaze(self, maze):
        self.maze = maze
    

if __name__ == "__main__":
    obj = ["hello", "world"]
    pickle_save(obj, "test1.p")
    obj = pickle_load("test1.p")
    print(obj)