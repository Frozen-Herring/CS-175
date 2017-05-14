import MalmoPython
import os
import sys
import time
from XMLgen import generateXML

worldXML = generateXML((25,25,25))

#--------SET UP MALMO INTERFACE-------
def startMission(agent_host, xml):
    my_mission = MalmoPython.MissionSpec(xml, True)
    my_mission_record = MalmoPython.MissionRecordSpec()
    agent_host.startMission( my_mission, my_mission_record )
    world_state = agent_host.peekWorldState()
    while not world_state.has_mission_begun:
        time.sleep(0.1)
        world_state = agent_host.peekWorldState()
        for error in world_state.errors:
            print "Error:",error.text
        if len(world_state.errors) > 0:
            exit(1)
#------------------------------------------

#----------OUR MISSION CODE----------------
def runOurMission(agent_host):
    agent_host.sendCommand('tp 1 7 1')
    #agent_host.sendCommand('setworldspawn 1 6 1')
    '''
    for x in xrange(3):
        for z in xrange(3):
            teleport_x = x * 2 + 1
            teleport_z = z * 2 + 1
            tp_command = "tp " + str(teleport_x)+ " 4 " + str(teleport_z) # command string is x y z, appears this map uses 4 as base
            print "Sending command: " + tp_command
            agent_host.sendCommand(tp_command)
            time.sleep(2) # TIME BETWEEN MOVES
    '''
    agent_host.sendCommand("quit")
# ------------------------------------------

#----CONNECT/SET UP AGENT AND RUN MISSION-----
if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
    agent_host = MalmoPython.AgentHost()

    try:
        agent_host.parse( sys.argv )
    except RuntimeError as e:
        print 'ERROR:',e
        print agent_host.getUsage()
        exit(1)
    if agent_host.receivedArgument("help"):
        print agent_host.getUsage()
        exit(0)

    startMission(agent_host, worldXML)
    world_state = agent_host.peekWorldState()
    #-----------------------------------------


    #----------------RUN MISSION--------------
    #Currently is teleport around with no purpose

    runOurMission(agent_host)

    #-------------------------------------------

    #------END MISSION AND CHECK REWARDS--------

    while world_state.is_mission_running:
        world_state = agent_host.peekWorldState()

    print "Mission over."

    '''
    world_state = agent_host.getWorldState()
    if Mission Ran :
        Calculate Final Rewards
    if not sucessful:
        print "Error Messgae"
        exit(1)
    '''

    print "Test successful"
    exit(0)

