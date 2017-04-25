def genereateBlockDrawingDecoratorStringGivenListOfBlockLists(listOfBlockLists, y):
    returnString = ""
    z = 0
    for list in listOfBlockLists:
        x = 0
        for block in list:
            returnString += "<DrawBlock {0}, {1}, {2}, {3}>\n".format(str(x), str(y), str(z), block)
            x += 1
        z += 1
    return returnString

def generateMissionXML(listOfBlockLists, yElevation):
    drawingDecoratorString = genereateBlockDrawingDecoratorStringGivenListOfBlockLists(listOfBlockLists, yElevation)
    return ""

if __name__ == "__main__": # put any test cases for the worldbuildingutils here
    print(genereateBlockDrawingDecoratorStringGivenListOfBlockLists([["lava", "lava", "lava"], ["dirt", "dirt", "dirt"], ["stone", "dirt", "lava"]]))

