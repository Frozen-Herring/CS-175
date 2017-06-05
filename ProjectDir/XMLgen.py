import MazeGen
import MalmoPython
import SaveLoader as sl
from random import randrange

# Stuff to do.
""""
change skin? 
Timer?
change sleep times
change tick time

"""

class XmlGen:
    def __init__(self, f = '', load = False, save = False):
        self.height = 226
        self.endBlock = None
        self.load = load
        self.save = save
        self.f = f

    def createMaze(self, mazeSize, rewardCount):
        if self.load:
            maze = sl.pickle_load(self.f)
            maze.prettyPrint()

        else:
            possibleMovement = "2D"
            maze = MazeGen.genMaze(mazeSize, possibleMovement, rewardCount)

        if self.save:
                if self.f == "":
                    self.f = str(randrange(0, 9999999999))
                    self.f += "-maze.p"
                mazeSaved = sl.pickle_save(maze, self.f)

        return maze


    def generateXML(self, mazeSize, rewardDict):
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
        for key, value in rewardDict.items():
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
        missionSpecs.startAt(0.5, 229, 0.5)  # - float x, float y, float z, float tolerance

        #CREATE THE MAZE
        maze = self.createMaze(mazeSize, rewardCount=len(rewardDict))

        mazeValue = maze.maze

        # Draw world in XML
        missionSpecs.drawBlock(-1, 227, -1, 'glowstone')  # Start block

        missionSpecs.drawBlock(-1, 227, mazeSize[2] + 1, 'glowstone')  # Start block
        missionSpecs.drawBlock(mazeSize[0] + 1, 227, mazeSize[2] + 1, 'glowstone')  # Start block
        missionSpecs.drawBlock(mazeSize[0] + 1, 227, -1, 'glowstone')  # Start block

        missionSpecs.drawCuboid(-10, self.height, -10, mazeSize[0] + 10, mazeSize[1] + self.height + 10, mazeSize[2] + 10, 'obsidian')
        missionSpecs.drawCuboid(-9, self.height, -9, mazeSize[0] + 9, mazeSize[1] + self.height + 9, mazeSize[2] + 9, 'air')
        missionSpecs.drawCuboid(-9, self.height, -9, mazeSize[0] + 9, self.height, mazeSize[2] + 9, 'lava')

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
                        missionSpecs.drawBlock(x, (y + self.height)+2, z, str(mazeValue[x][z][y]))
                        if str(mazeValue[x][z][y]) == "lapis_block":
                            missionSpecs.drawItem(x, (y + self.height + 4), z, rewardDictCopy.popitem()[0])

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
        # missionSpecs.allowAllChatCommands()
        missionSpecs.requestVideo(960, 540)
        missionSpecs.setViewpoint(1)
        missionSpecs.allowAllInventoryCommands()

        self.endBlock = maze.endBlock

        return missionSpecs.getAsXML(True)


if __name__ == '__main__':
    xmlGen = XmlGen()
    print xmlGen.generateXML((25, 25, 25), {"coal": 10, "iron_ingot": 20, "gold_ingot": 30, "lapis_ore": 40, "emerald_ore": 50,
                                     "diamond": 60, "potato": 70})




