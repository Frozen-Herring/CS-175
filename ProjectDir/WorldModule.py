class World:
    def __init__(self):
        self.blocks = [] # list of block type strings... ["air", "diamond_block", "emerald_block"]
        self.expectedRewardDict = dict() # key = block index, value = reward score calculated by the monte carlo thing
        self.blockRewardDict = dict() # key = block type, value = reward value... {lava:-100, normal:-1, rewardBlock:+10}

    def getPossibleMoves(self, startingIndex):
        ''' (self, int) -> [int]
        output: list of block indices which are valid moves
        '''
