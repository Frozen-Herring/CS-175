class World:
    def __init__(self):
        self.blocks = [] # list of block type strings... ["air", "diamond_block", "emerald_block"]
        self.qTableDict = dict() # key = block index, value = reward score calculated by the monte carlo thing
        self.blockRewardDict = dict() # key = block type, value = reward value... {lava:-100, normal:-1, rewardBlock:+10}
        self.blocksPerRow = 21 # TODO: make sure this corresponds to the size of the world defined in the mission xml
        self.totalRows = 0 # TODO: make sure this corresponds to the size of the world defined in the mission xml

    def getPossibleMoves(self, startingIndex):
        ''' (self, int) -> [int]
        output: list of block indices which are valid moves
        '''
        possibleMoves = []
        eastWestNorthSouthIndexList = [startingIndex+1, startingIndex-1, startingIndex-self.blocksPerRow, startingIndex+self.blocksPerRow]
        for index in eastWestNorthSouthIndexList:
            if index <= len(self.blocks-1) and self.blocks[index] in set("lava", "diamond_block", "emerald_block"): # TODO: make sure that these block types are correct
                possibleMoves.append(index)
        return possibleMoves

    def getDirectionActionForMove(self, startingBlock, adjacentBlock):
        action_trans = { -self.blocksPerRow: 'movenorth 1', self.blocksPerRow: 'movesouth 1', -1: 'movewest 1', 1: 'moveeast 1'}
        return action_trans[adjacentBlock - startingBlock]
