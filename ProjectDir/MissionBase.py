import MalmoPython
import os
import sys
import time
import json
import random
from XMLGen import generateXML

def agentRun(agentHost):
    totalReward = 0 #
    currentReward = 0

    worldState = agentHost.peekWorldState() # wait until valid observation
    sys.stdout.write("\nwait for obs")
    while worldState.is_mission_running and all(e.text == '{}' for e in worldState.observations):
        worldState = agentHost.peekWorldState()
        sys.stdout.write(".")
        sys.stdout.flush()

    if not worldState.is_mission_running:
        return 0

    obs = json.loads(worldState.observations[-1].text)  #Yay, observation
    print "\n", obs,
    prevX = obs[u'XPos']
    prevZ = obs[u'ZPos']
    print '\nInitial position:', prevX, ',', prevZ

    #Make arbitray move
    actionSet = ["movenorth 1", "movesouth 1", "movewest 1", "moveeast 1"]
    time.sleep(1)
    #move = "tp .5 227 .5"#random.choice(actionSet)
    move = random.choice(actionSet)
    agentHost.sendCommand(move)
    #time.sleep(2)
    #agentHost.sendCommand("moveeast 1")
    print '\nmoved ', move
    time.sleep(1)
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

def setup(mazeSize = (10, 10, 10), rewards = {}):
    worldXML = generateXML(mazeSize, rewards)  # maze size x y z  ALSO PASS ITEM DICT
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
    mission = MalmoPython.MissionSpec(worldXML, True)
    mission.allowAllAbsoluteMovementCommands() #-------------------DELETE THIS FOR TESSTING ONLY
    missionRec = MalmoPython.MissionRecordSpec()
    agentHost = MalmoPython.AgentHost()

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

    return agentHost


def main():
    agentHost = setup()

    #finalReward = 0
    maxMoves = 3

    agentRun(agentHost)


    for i in range(maxMoves):
        agentRun(agentHost)


    #print 'Final Rewards: ', finalReward
    time.sleep(0.5) # (let the Mod reset)
    print "Mission Complete"



#----CONNECT/SET UP AGENT AND RUN MISSION-----
if __name__ == "__main__":
    main()



#-------------------------------------------
