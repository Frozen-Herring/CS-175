import MazeGen

def generateXML(mazeSize):
    '''Takes a three tuple or iterabele'''
    WIDTH = 860
    HEIGHT = 480

    maze = MazeGen.genMaze(mazeSize)
    mazeValue = maze.maze

    def genItems():
        items = ""

        items += '<DrawBlock x="' + str(0) + '" y="' + str(4) + '" ' + 'z="' + str(0) + '" type="' + str('dirt') + '"/>' #Start block

        for xVal in range(len(mazeValue)):
            x = xVal
            for zVal in range(len(mazeValue[xVal])):
                z = zVal
                for yVal in range(len(mazeValue[xVal][zVal])):
                    y = yVal
                    items += '<DrawBlock x="' + str(x) + '" y="' + str(y + 3) + '" '+ 'z="' + str(z) + '" type="' + str(mazeValue[x][z][y]) +'"/>'
                    #items += '<DrawItem x="' + str(x) + '" y="' + str(y + 3) + '" '+ 'z="' + str(z+6) + '" type="apple"/>'

        return items

    worldXML = '''<?xml version="1.0" encoding="UTF-8" ?>
        <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <About>
                <Summary>Testing Base -- CHANGE THIS</Summary>
            </About>
            <ServerSection>
                <ServerInitialConditions>
                    <Time>
                        <StartTime>1000</StartTime>
                        <AllowPassageOfTime>false</AllowPassageOfTime>
                    </Time>
                    <Weather>clear</Weather>
                </ServerInitialConditions>
                <ServerHandlers>
                    <FlatWorldGenerator generatorString="3;;1;" forceReset="true" destroyAfterUse="true"/>
                    <DrawingDecorator>''' + genItems() + '''</DrawingDecorator>
                    <ServerQuitWhenAnyAgentFinishes />
                </ServerHandlers>
            </ServerSection>
            <AgentSection mode="Survival">
                <Name>ChickenChicken</Name>
                <AgentStart>
                    <Placement x="0" y="4" z="0"/>
                    <Inventory/>
                </AgentStart>
                <AgentHandlers>
                    <ContinuousMovementCommands turnSpeedDegs="360"/>
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

    return worldXML
