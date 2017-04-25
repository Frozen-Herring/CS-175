import MalmoPython
import os
import sys
import time

#-----------RANDOM WORLD GEN--------------
WIDTH=860
HEIGHT=480

def genItems():
    items = ""
    for x in xrange(10):
        for z in xrange(10):
            items += '<DrawBlock x="' + str(x * 1000) + '" y="3" z="' + str(z * 1000) + '" type="redstone_block"/>'
            items += '<DrawItem x="' + str(x * 1000) + '" y="10" z="' + str(z * 1000) + '" type="emerald"/>'
    return items

worldXML = '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary>Teleportastic</Summary>
        </About>

        <ServerSection>
            <ServerInitialConditions>
                <Time>
                    <StartTime>1000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime> <!-- Keep steady daylight to make image parsing simple -->
                </Time>
                <Weather>clear</Weather> <!-- Keep steady weather to make image parsing simple -->
            </ServerInitialConditions>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;;1;" forceReset="true" destroyAfterUse="true"/>
                <DrawingDecorator>''' + genItems() + '''</DrawingDecorator>
                <ServerQuitWhenAnyAgentFinishes />
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>Brundlefly</Name>
            <AgentStart>
                <Placement x="-100.5" y="4" z="400.5" yaw="0" pitch="90"/>  <!-- Look down at the ground -->
                <Inventory/>
            </AgentStart>
            <AgentHandlers>
                <ObservationFromFullInventory/>
                <AbsoluteMovementCommands/>
                <MissionQuitCommands/>
                <RewardForCollectingItem>
                    <Item type="emerald" reward="1"/>
                </RewardForCollectingItem>
                <VideoProducer>
                    <Width>''' + str(WIDTH) + '''</Width>
                    <Height>''' + str(HEIGHT) + '''</Height>
                </VideoProducer>
            </AgentHandlers>
        </AgentSection>

    </Mission>'''

#------------------------------------


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
    for x in xrange(10):
        for z in xrange(10):
            teleport_x = x * 2 + 1
            teleport_z = z * 2 + 1
            tp_command = "tp " + str(teleport_x)+ " 4 " + str(teleport_z) # command string is x y z, appears this map uses 4 as base
            print "Sending command: " + tp_command
            agent_host.sendCommand(tp_command)
            time.sleep(10) # TIME BETWEEN MOVES
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

    agent_host.sendCommand("quit")
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

