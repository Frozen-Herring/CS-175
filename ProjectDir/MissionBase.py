import MalmoPython
import os
import sys
import time
from XMLgen import XmlGen
from AgentModule import Agent as QAgent
from MalmoWorldRep import WorldRep
from SaveLoader import MazeSaveLoader as msl
from CoordinateUtils import rewardDict, agentStart
"""
==================
Stuff to change:
set start location as var,
in this and xmlgen
fix world Rep
==================
"""

class MissionBase:
    def __init__(self, maze):
        self.maze = maze

    def agentRun(self, agentHost, qAgent, world):
        world.worldState = agentHost.peekWorldState() # wait until valid observation
        # sys.stdout.write("\nwait for obs")
        while world.worldState.is_mission_running and all(e.text == '{}' for e in world.worldState.observations):
            world.worldState = agentHost.peekWorldState()

            # sys.stdout.write(".")
            # sys.stdout.flush()
        # sys.stdout.write("\n")
        # sys.stdout.flush()

        qAgent.new_episode() #TODO: what is this?

        while world.worldState.is_mission_running:
            #Make move
            qAgent.makeMove()
            world.worldState = agentHost.peekWorldState()
            if world.finishedMaze(): #TODO: doesn't work???
                agentHost.sendCommand("chat /kill")
                agentHost.sendCommand("chat I finished the maze!")
                print "finished mission"

    def startMission(self, agentHost, mission, missionRec):
        try:
            agentHost.startMission(mission, missionRec)
        except RuntimeError as e:
            print "Error starting mission:", e

        print "\nStarting New Mission..."
        worldState = agentHost.peekWorldState()
        while not worldState.has_mission_begun:
            time.sleep(0.1)
            worldState = agentHost.getWorldState()
            for error in worldState.errors:
                print "Error:", error.text


    def setup(self):
        xmlGen = XmlGen(self.maze)
        worldXML = xmlGen.generateXML()
        sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
        mission = MalmoPython.MissionSpec(worldXML, True)
        missionRec = MalmoPython.MissionRecordSpec()
        agentHost = MalmoPython.AgentHost()
        return (agentHost, mission, missionRec)


    def main(self):
        CURRENT_MAZE_NAME = "some maze"
        BEST_POSSIBLE_SCORE = -999

        agentHost, mission, missionRec = self.setup()
        world = WorldRep(agentHost, self.maze)
        qAgent = QAgent(world, start = agentStart)
        agentHost.sendCommand("chat /difficulty 3")
        agentHost.sendCommand("chat oh boy I sure hope there's no lava around here")

        while (not (world.finishedMaze() and qAgent.bestScoreSoFar >= BEST_POSSIBLE_SCORE)): #TODO: doesn't work???
            self.startMission(agentHost, mission, missionRec)
            self.agentRun(agentHost, qAgent, world)

        print ("optimal path (best possible score) found in: " + str(qAgent.episodeCount) + " episodes. Stopping Agent.")
        self.updateRecordStats(CURRENT_MAZE_NAME, qAgent.episodeCount, qAgent.totalMoveCount)


    def updateRecordStats(self, currentMazeName, episodesTaken, totalMovesTaken):
        with open("best_run_stats.csv", "r+") as f:
            data = f.read()
            data += "\n" + str(currentMazeName) + "\t" + str(episodesTaken) + "\t" + str(totalMovesTaken)
            f.seek(0)
            f.write(data)
            f.truncate()


#----CONNECT/SET UP AGENT AND RUN MISSION-----
if __name__ == "__main__":
    maze = msl().getMaze()
    # maze = msl(x=2,y=5,rewardCount=2,lavaPercent=.2).getMaze()
    missionBase = MissionBase(maze)
    missionBase.main()



