import MazeGen
import MalmoPython

#Stuff to do.
""""
Clean up rewards
set view point behind
change skin? 
Timer?
change sleep times

"""

HEIGHT = 226
itemRewards = {"apple":25, "carrot":50, "emerald":70, "diamond":100}

def generateXML(mazeSize, rewards):
    global HEIGHT

    #USE THIS TO SET UP WITH MODIFICATIONS
    initialXML = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://ProjectMalmo.microsoft.com Mission.xsd">

  <About>
    <Summary>LARS Project 175</Summary>
  </About>
  
  <ModSettings>
    <MsPerTick>20</MsPerTick>
  </ModSettings>

  <ServerSection>
    <ServerInitialConditions>
      <Time>
        <StartTime>13200</StartTime>
        <AllowPassageOfTime>false</AllowPassageOfTime>
      </Time>
      <Weather>clear</Weather>
      <AllowSpawning>false</AllowSpawning>																
    </ServerInitialConditions>
    <ServerHandlers>
      <FlatWorldGenerator destroyAfterUse="true" forceReset="false" generatorString="3;7,220*1,5*3,2;3;,biome_1" seed=""/>
      <ServerQuitWhenAnyAgentFinishes description=""/>
    </ServerHandlers>
  </ServerSection>
									   
  <AgentSection mode="Survival">
    <Name>Lars</Name>
    <AgentStart>
       <Placement x="0.5" y="227" z="0.5" pitch="30" yaw="0"/>
    </AgentStart>
    <AgentHandlers>	 
      <ObservationFromRecentCommands/>
      <ObservationFromFullStats/>
      <ObservationFromFullInventory/>
      <ContinuousMovementCommands turnSpeedDegs="180"/>
      <VideoProducer want_depth="false">
          <Width>640</Width>
          <Height>480</Height>
      </VideoProducer>
      <DiscreteMovementCommands>
          <ModifierList type="deny-list">
            <command>attack</command>
          </ModifierList>
      </DiscreteMovementCommands>
      <RewardForTouchingBlockType>
        <Block reward="-100.0" type="lava" behaviour="onceOnly"/>
      </RewardForTouchingBlockType>
      <RewardForSendingCommand reward="-1"/>
	<InventoryCommands/>	  
    </AgentHandlers>
  </AgentSection>
				 
</Mission>'''




    #Set up Misscion class
    missionSpecs = MalmoPython.MissionSpec(initialXML, True)

    #Describe Mission
    missionSpecs.setSummary("LARS Project 175")

    #/setworldspawn 0 227 0

    #Timer??
    #missionSpecs.timeLimitInSeconds(100)

    #Day Light parameteers, defualt 1000, morning not allowing time to pass
    missionSpecs.setTimeOfDay(13200 ,False)

    #For Future use, set a entrance or exit state to be recorded
    missionSpecs.startAt(0.5, 227, 0.5) #- float x, float y, float z, float tolerance
    maze = MazeGen.genMaze(mazeSize)
    mazeValue = maze.maze


    #Draw world in XML
    missionSpecs.drawBlock(-1,227,-1,'glowstone')#Start block

    missionSpecs.drawBlock(-1, 227, mazeSize[2]+1, 'glowstone')  # Start block
    missionSpecs.drawBlock(mazeSize[0]+1, 227,mazeSize[2]+1, 'glowstone')  # Start block
    missionSpecs.drawBlock(mazeSize[0]+1, 227, -1, 'glowstone')  # Start block

    missionSpecs.drawCuboid(-10, HEIGHT, -10, mazeSize[0]+10, mazeSize[1]+HEIGHT+1, mazeSize[2]+10, 'obsidian')
    missionSpecs.drawCuboid(-9, HEIGHT, -9, mazeSize[0]+9, mazeSize[1]+HEIGHT, mazeSize[2]+9, 'air')
    missionSpecs.drawCuboid(-9, HEIGHT, -9, mazeSize[0] + 9, HEIGHT, mazeSize[2] + 9, 'lava')


    #Draw Maze/Items
    for xVal in range(len(mazeValue)):

        x = xVal
        for zVal in range(len(mazeValue[xVal])):
            z = zVal
            for yVal in range(len(mazeValue[xVal][zVal])):
                y = yVal
                missionSpecs.drawBlock(x,(y + HEIGHT),z, str(mazeValue[x][z][y]))
                if str(mazeValue[x][z][y]) == "lapis_block":
                    missionSpecs.drawItem(x, (y + HEIGHT + 2), z, "apple")
                    pass

    #Observations
    missionSpecs.observeFullInventory()  #Full item inventory of the player included in the observations
    missionSpecs.observeRecentCommands() # list of commands acted upon since the last timestep
    #missionSpecs.observeDistance# (float x, float y, float z, const std::string & name) For use once an end in place


    #Rewards
    #rewardForReachingPosition(float x, float y, float, z, float amount, float tolerance) # to be included when end is implemented
    #Change to reward for touching block?????


    #Settings
    missionSpecs.removeAllCommandHandlers()
    missionSpecs.allowAllDiscreteMovementCommands()
    missionSpecs.requestVideo(520, 440)
    missionSpecs.setViewpoint(1)
    missionSpecs.allowAllInventoryCommands()

    return missionSpecs.getAsXML(True)

print generateXML((25,25,25), {})




