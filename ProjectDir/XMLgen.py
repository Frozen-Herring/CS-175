import MazeGen
import MalmoPython
import SaveLoader as sl
from CoordinateUtils import rewardDict, malmoGroundY, raiseBy, agentStart

class XmlGen:
    def __init__(self, maze = None):
        self.height = malmoGroundY
        self.raiseBy = raiseBy
        self.agentStart = agentStart

        if maze == None:
            maze = sl.MazeSaveLoader().getMaze()

        self.maze = maze
        self.mazeXSize = self.maze.x
        self.mazeYSize = self.maze.z
        self.mazeZSize = self.maze.y



    def generateXML(self):
        # USE THIS TO SET UP WITH MODIFICATIONS
        initialXML = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

      <About>
        <Summary>Lars 175</Summary>
      </About>

      <ModSettings>
        <MsPerTick>20</MsPerTick>
      </ModSettings>

      <ServerSection>
          <ServerInitialConditions>
                <Time>
                    <StartTime>6000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <Weather>clear</Weather>
                <AllowSpawning>false</AllowSpawning>
          </ServerInitialConditions>
        <ServerHandlers>
          <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1"/>
          <ServerQuitFromTimeUp timeLimitMs="1000000"/>
          <ServerQuitWhenAnyAgentFinishes/>
        </ServerHandlers>
      </ServerSection>

      <AgentSection mode="Survival">
        <Name>Lars</Name>
        <AgentStart>
          <Placement x="0.5" y="227" z="0.5" pitch="30" yaw="0"/>
        </AgentStart>
        <AgentHandlers>
            <RewardForCollectingItem>REWARD_DICT_GOES_HERE
            </RewardForCollectingItem>
          <ObservationFromFullStats/>
          <VideoProducer want_depth="false">
              <Width>640</Width>
              <Height>480</Height>
          </VideoProducer>
          <DiscreteMovementCommands>
              <ModifierList type="deny-list">
                <command>attack</command>
              </ModifierList>
          </DiscreteMovementCommands>
          <AbsoluteMovementCommands/>
          <ChatCommands/>
           <MissionQuitCommands/>
          <RewardForTouchingBlockType>
            <Block reward="-100.0" type="lava" behaviour="onceOnly"/>
          </RewardForTouchingBlockType>
          <RewardForSendingCommand reward="-1"/>
          <AgentQuitFromTouchingBlockType>
              <Block type="lava" />
          </AgentQuitFromTouchingBlockType>
        </AgentHandlers>
      </AgentSection>

    </Mission>'''

        rewardDictXmlString = ""
        sorted(rewardDict.keys())
        for key, value in sorted(rewardDict.items()):
            rewardDictXmlString += "\n<Item type=\"{}\" reward=\"{}\"/>".format(key, value)
        initialXML = initialXML.replace("REWARD_DICT_GOES_HERE", rewardDictXmlString)

        # Set up Misscion class
        missionSpecs = MalmoPython.MissionSpec(initialXML, True)

        # Describe Mission
        missionSpecs.setSummary("LARS Project 175")

        # Timer??
        # missionSpecs.timeLimitInSeconds(100)

        # Day Light parameteers, defualt 1000, morning not allowing time to pass
        missionSpecs.setTimeOfDay(13200, False)

        # For Future use, set a entrance or exit state to be recorded
        missionSpecs.startAt(self.agentStart[0], self.agentStart[1], self.agentStart[2])  # - float x, float y, float z, float tolerance

        mazeValue = self.maze.maze

        # Draw world in XML
        missionSpecs.drawCuboid(-10, self.height, -10, self.mazeXSize + 10, self.mazeYSize + self.height + 10, self.mazeZSize + 10, 'obsidian')
        missionSpecs.drawCuboid(-9, self.height, -9, self.mazeXSize + 9, self.mazeYSize + self.height + 9, self.mazeZSize + 9, 'air')
        missionSpecs.drawCuboid(-9, self.height, -9, self.mazeXSize + 9, self.height, self.mazeZSize + 9, 'lava')

        rewardDictCopy = dict()
        for key in rewardDict:
            rewardDictCopy[key] = rewardDict[key]

        # Draw Maze/Items
        for xVal in range(len(mazeValue)):
            x = xVal
            for zVal in range(len(mazeValue[xVal])):
                z = zVal
                for yVal in range(len(mazeValue[xVal][zVal])):
                    y = yVal
                    if str(mazeValue[x][z][y]) == "lava":
                        missionSpecs.drawBlock(x, (y + self.height), z, str(mazeValue[x][z][y]))
                    else:
                        missionSpecs.drawBlock(x, (y + self.height + self.raiseBy), z, str(mazeValue[x][z][y]))

                        if str(mazeValue[x][z][y]) == "lapis_block":
                            missionSpecs.drawItem(x, (y + self.height + self.raiseBy + 2), z, rewardDictCopy.popitem()[0])
        # Observations
        missionSpecs.observeFullInventory()  # Full item inventory of the player included in the observations
        missionSpecs.observeRecentCommands()  # list of commands acted upon since the last timestep
        # missionSpecs.observeDistance# (float x, float y, float z, const std::string & name) For use once an end in place


        # Rewards
        # rewardForReachingPosition(float x, float y, float, z, float amount, float tolerance) # to be included when end is implemented


        # Settings
        missionSpecs.removeAllCommandHandlers()
        missionSpecs.allowAllDiscreteMovementCommands()
        missionSpecs.allowAllAbsoluteMovementCommands()
        missionSpecs.allowAllChatCommands()
        missionSpecs.requestVideo(960, 540)
        missionSpecs.setViewpoint(1)
        missionSpecs.allowAllInventoryCommands()

        return missionSpecs.getAsXML(True)


if __name__ == '__main__':
    xmlGen = XmlGen()
    print xmlGen.generateXML()




