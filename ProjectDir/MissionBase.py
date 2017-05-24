import MalmoPython
import os
import sys
import time
from XMLgen import generateXML
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


def agentRun(agentHost, qAgent, world):
    worldState = agentHost.peekWorldState() # wait until valid observation
    # sys.stdout.write("\nwait for obs")
    while worldState.is_mission_running and all(e.text == '{}' for e in worldState.observations):
        worldState = agentHost.peekWorldState()
        # sys.stdout.write(".")
        # sys.stdout.flush()
    # sys.stdout.write("\n")
    # sys.stdout.flush()

    if not worldState.is_mission_running:
        print "Mission quit"
        return 0

    world.newEpisode(worldState)

    while worldState.is_mission_running:
        #Make move
        qAgent.makeMove()
        worldState = agentHost.peekWorldState()
        #world.updateWorldRep(worldState) --- make move in agent, calls make move in world rep, which updates itself.

    #------------------

    return

def startMission(agentHost, mission, missionRec):
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


def setup(mazeSize = (10, 10, 10), rewards = {"apple":50}):
    worldXML = generateXML(mazeSize, rewards)
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
    mission = MalmoPython.MissionSpec(worldXML, True)
    missionRec = MalmoPython.MissionRecordSpec()
    agentHost = MalmoPython.AgentHost()
    return (agentHost, mission, missionRec)


def main():

    rewards = {"coal": 10, "iron_ingot": 20, "gold_ingot": 30, "lapis_ore": 40, "emerald_ore": 50, "diamond": 60, "potato": 70}
    mazeSize = (10,10,10)

    agentHost, mission, missionRec = setup(mazeSize, rewards)
    world = WorldRep(agentHost, rewards = rewards)
    qAgent = QAgent(world, start = (.5, 227,.5))

    #finalReward = 0
    maxMoves = 100;
    for i in range(maxMoves):
        startMission(agentHost, mission, missionRec)
        agentRun(agentHost, qAgent, world)
        time.sleep(.5)

    #print 'Final Rewards: ', finalReward
    time.sleep(0.5) # (let the Mod reset)
    print "Mission Complete"



#----CONNECT/SET UP AGENT AND RUN MISSION-----
if __name__ == "__main__":
    main()



