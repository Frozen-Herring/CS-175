import MalmoPython
import os
import sys
import time
from XMLgen import XmlGen
from AgentModule import Agent as QAgent
from MalmoWorldRep import WorldRep

"""
==================
Stuff to change:
set start location as var,
in this and xmlgen
fix world Rep
==================
"""

class MissionBase:
    def __init__(self):
        self.endBlock = None

    def agentRun(self, agentHost, qAgent, world):
        world.worldState = agentHost.peekWorldState() # wait until valid observation
        # sys.stdout.write("\nwait for obs")
        while world.worldState.is_mission_running and all(e.text == '{}' for e in world.worldState.observations):
            world.worldState = agentHost.peekWorldState()

            # sys.stdout.write(".")
            # sys.stdout.flush()
        # sys.stdout.write("\n")
        # sys.stdout.flush()

        qAgent.new_episode()

        while world.worldState.is_mission_running:
            #Make move
            qAgent.makeMove(0.02, False)
            world.worldState = agentHost.peekWorldState()
            #world.updateWorldRep(world.worldState) --- make move in agent, calls make move in world rep, which updates itself.

        #------------------

        return

    def startMission(self, agentHost, mission, missionRec):
        try:
            agentHost.startMission(mission, missionRec)
        except RuntimeError as e:
            print "Error starting mission:", e

        print "\nStarting New Mission..."
        worldState = agentHost.peekWorldState()
        while not worldState.has_mission_begun:
            # sys.stdout.write(".")
            time.sleep(0.1)
            worldState = agentHost.getWorldState()
            for error in worldState.errors:
                print "Error:", error.text


    def setup(self, mazeSize = (10, 10, 10), rewards = {"apple":50}):
        xmlGen = XmlGen()
        worldXML = xmlGen.generateXML(mazeSize, rewards)
        self.endBlock = xmlGen.endBlock
        sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
        mission = MalmoPython.MissionSpec(worldXML, True)
        missionRec = MalmoPython.MissionRecordSpec()
        agentHost = MalmoPython.AgentHost()
        return (agentHost, mission, missionRec)


    def main(self):

        rewards = {"coal": 10, "iron_ingot": 20, "gold_ingot": 30, "lapis_ore": 40, "emerald_ore": 50, "diamond": 60, "potato": 70}
        mazeSize = (10,10,10)

        agentHost, mission, missionRec = self.setup(mazeSize, rewards)
        world = WorldRep(agentHost, self.endBlock, rewards = rewards)
        qAgent = QAgent(world, start = (.5, 227,.5))

        #finalReward = 0
        maxMoves = 10000;
        for i in range(maxMoves):
            self.startMission(agentHost, mission, missionRec)
            self.agentRun(agentHost, qAgent, world)
            time.sleep(.1)

        #print 'Final Rewards: ', finalReward
        time.sleep(0.5) # (let the Mod reset)
        print "Mission Complete"



#----CONNECT/SET UP AGENT AND RUN MISSION-----
if __name__ == "__main__":
    missionBase = MissionBase()
    missionBase.main()



