import MalmoPython
import os
import sys
import time
import json
import random
from XMLGen import generateXML

def agentRun(agentHost):
    totalReward = 0
    currentReward = 0

    worldState = agentHost.peekWorldState() # wait until valid observation
    sys.stdout.write("\nwait for obs")
    while worldState.is_mission_running and all(e.text == '{}' for e in worldState.observations):
        worldState = agentHost.peekWorldState()
        sys.stdout.write(".")
        sys.stdout.flush()

    if not worldState.is_mission_running:
        print "Mission quit"
        return 0

    while worldState.is_mission_running:
        obs = json.loads(worldState.observations[-1].text)
        print "\n", obs,
        prevX = obs[u'XPos']
        prevZ = obs[u'ZPos']
        print '\nInitial position:', prevX, ',', prevZ

        #Make arbitray move
        actionSet = ["movenorth 1", "movesouth 1", "movewest 1", "moveeast 1"]
        time.sleep(1)
        move = random.choice(actionSet)
        agentHost.sendCommand(move)
        print '\nmoved ', move
        time.sleep(.5)
        worldState = agentHost.peekWorldState()
    #------------------


    #totalReward += currentReward

    # main loop to run Q stuff
    """
    while worldState.is_mission_running:
        print 'Waiting for data...',
        while True:
            world_state = agentHost.peekWorldState()
            if not worldState.is_mission_running:
                print 'mission ended.'
                break
            if len(world_state.rewards) > 0 and not all(e.text == '{}' for e in world_state.observations):
                obs = json.loads(world_state.observations[-1].text)
                currX = obs[u'XPos']
                currZ = obs[u'ZPos']

            print 'New position from observation:', currX, ',', currZ, 'after action:', move,

            
            world_state = agentHost.peektWorldState() #Change to peek? Even needed?
            for err in world_state.errors:
                print err
            currentReward = sum(r.getValue() for r in world_state.rewards)
            
            #Do more moves and stuff.... Dunno Q learning checks and effects go here.
        """


    return currentReward

def startMission(agentHost, mission, missionRec):
    try:
        agentHost.startMission(mission, missionRec)
    except RuntimeError as e:
        print "Error starting mission:", e

    print "Waiting for the mission to start"
    worldState = agentHost.peekWorldState()
    while not worldState.has_mission_begun:
        sys.stdout.write(".")
        time.sleep(0.1)
        worldState = agentHost.getWorldState()
        for error in worldState.errors:
            print "Error:", error.text

    print "Waiting for the mission to start"
    worldState = agentHost.peekWorldState()
    while not worldState.has_mission_begun:
        sys.stdout.write(".")
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

    #finalReward = 0
    maxMoves = 3
    for i in range(maxMoves):
        startMission(agentHost, mission, missionRec)
        agentRun(agentHost)
        time.sleep(.5)

    #print 'Final Rewards: ', finalReward
    time.sleep(0.5) # (let the Mod reset)
    print "Mission Complete"



#----CONNECT/SET UP AGENT AND RUN MISSION-----
if __name__ == "__main__":
    main()



