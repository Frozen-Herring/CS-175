import MalmoPython
import os
import sys
import time
import json
import random
from XMLgen import generateXML

worldXML = generateXML((25,25,25), {"coal":10, "iron_ingot":20, "gold_ingot":30, "lapis_ore":40, "emerald_ore":50, "diamond":60, "potato":70}) #maze size x y z

#--------SET UP MALMO INTERFACE-------
def startMission(agentHost, xml):
    mission = MalmoPython.MissionSpec(xml, True)
    missionRecord = MalmoPython.MissionRecordSpec() # Need to set up
    agentHost.startMission( mission, missionRecord )
    worldState = agentHost.peekWorldState()
    while not worldState.has_mission_begun:
        time.sleep(0.1)
        worldState = agentHost.peekWorldState()
        for error in worldState.errors:
            print "Error:",error.text
        if len(worldState.errors) > 0:
            exit(1)
#------------------------------------------


#-----------AGENENT RUN-------------------- Suggest moving this to agent
actions = ["movenorth 1", "movesouth 1", "movewest 1", "moveeast 1"]

def run(agentHost):
    """run the agent on the world"""

    totalReward = 0
    currentRewards = 0

    previousState = None #may need?
    previousAction = None

    # wait for a valid observation
    worldState = agentHost.peekWorldState()
    while worldState.is_mission_running and all(e.text == '{}' for e in worldState.observations):
        worldState = agentHost.peekWorldState()

    if not worldState.is_mission_running:
        return 0  # mission already ended

    obs = json.loads(worldState.observations[-1].text)
    print obs
    prevX = obs[u'XPos']
    prevZ = obs[u'ZPos']
    print 'Initial position:', prevX, ',', prevZ

    #totalReward += agentHost.sendCommand() #should be total reward plus whatever the last action got?  Maybe want to do rewards based on item collected not inventory

    #Take actions ----

    time.sleep(1)
    agentHost.sendCommand('movenorth 1')
    print 'move'
    time.sleep(1)

    print 'Waiting for data...',
    while worldState.is_mission_running:
        while True:
            worldState = agentHost.peekWorldState()
            if not worldState.is_mission_running:
                print 'mission ended.'
                break

        worldState = agentHost.getWorldState()
        for err in worldState.errors:
            print err

        current_r = sum(r.getValue() for r in worldState.rewards)


#-----------AGENENT RUN--------------------

#----------OUR MISSION CODE----------------
'''
def runOurMission(agentHost):
    TESTING STUFF
    #agentHost.sendCommand('tp 0 227 0')
    time.sleep(1)
    loc = 0
    for i in range(10):

        agentHost.sendCommand('movenorth 1')
        print 'move'
        time.sleep(1)
        """
        agentHost.sendCommand('tp ' + str(loc) + ' 227 ' +str(loc))
        loc+=1
        print loc, " moved\n"
        time.sleep(1)
        """

    #agentHost.sendCommand('setworldspawn 1 6 1')
    
    for x in xrange(3):
        for z in xrange(3):
            teleport_x = x * 2 + 1
            teleport_z = z * 2 + 1
            tp_command = "tp " + str(teleport_x)+ " 4 " + str(teleport_z) # command string is x y z, appears this map uses 4 as base
            print "Sending command: " + tp_command
            agentHost.sendCommand(tp_command)
            time.sleep(2) # TIME BETWEEN MOVES
    
    agentHost.sendCommand("quit")
'''
# ------------------------------------------

#----CONNECT/SET UP AGENT AND RUN MISSION-----
if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
    agentHost = MalmoPython.AgentHost()

    try:
        agentHost.parse( sys.argv )
    except RuntimeError as e:
        print 'ERROR:',e
        print agentHost.getUsage()
        exit(1)
    if agentHost.receivedArgument("help"):
        print agentHost.getUsage()
        exit(0)

    startMission(agentHost, worldXML)
    worldState = agentHost.peekWorldState()
    #-----------------------------------------


    #----------------RUN MISSION--------------
    #Currently is moving north around with no purpose
    #runOurMission(agentHost)
    maxRetry = 3
    maxMoves = 3
    finalRewards = []
    for i in range(maxMoves):
        print "Mission starting",
        world_state = agentHost.getWorldState()
        while not world_state.has_mission_begun:
            print "."
            time.sleep(0.1)
            world_state = agentHost.getWorldState()
            for error in world_state.errors:
                print "Error:", error.text
        print

        # -- run the agent in the world -- #
        run(agentHost) #save rewards at some poitn

        print 'Final reward:',  finalRewards
        #finalRewards += what ever last rewards were

        # -- clean up -- #
        time.sleep(0.5)  # (let the Mod reset)

    print "Done."

    print
    print "Final rewards for all ", maxMoves, ' runs:'
    print finalRewards

    #-------------------------------------------

    #------END MISSION AND CHECK REWARDS--------
    """
    while worldState.is_mission_running:
        worldState = agentHost.peekWorldState()

    print "Mission over."

    '''
    worldState = agentHost.getWorldState()
    if Mission Ran :
        Calculate Final Rewards
    if not sucessful:
        print "Error Messgae"
        exit(1)
    '''

    print "Test successful"
    exit(0)
    """