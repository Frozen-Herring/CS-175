import MalmoPython as Malmo


class Agent:
    def __init__(self, world):
        self.world = world # keep a reference to the world... TODO: evaluate whether or not this is a good idea
        self.currentPath = [] # [int]... list of the indices of blocks we traversed so far... #TODO: We might need to pass the agent's starting position and put it into currentPath
        self.rewardSum = 0; # int... the sum of all the rewards gotten so far from currentPath
        self.remainingRewards = [] # [int]... list of the reward blocks which have not been visited yet
        self.ourAgent = Malmo.AgentHost()

        self.hitLava = False # bool... we set this to true when we hit lava

    def makePath(self, N):
        ''' (self, int) -> None
        Continually call makeMove N times, or until we hit lava, or until remainingRewards is empty '''
        count = 0
        while count < N and not self.hitLava:
            self.makeMove()
            count += 1

    def makeMove(self):
        ''' (self, [int], '''
        possibleMoves = ['movenorth 1', 'movesouth 1', 'moveeast 1', 'movewest 1']
        moveToTake = self.chooseMove(possibleMoves)
        directionAction = self.world.getDirectionActionForMove(self.currentPath[-1], moveToTake)
        self.ourAgent.sendCommand(directionAction)
        self.update(moveToTake)

    def chooseMove(self, possibleMoves):
        ''' (self, [int] -> int... use expectedRewardDict and blockReward and a RNG to choose a move'''
        for move in possibleMoves:
            expectedReward = self.world.expectedRewardDict[move]
            blockReward = self.world.blockRewardDict[move]
            # TODO: use expectedReward and blockReward to choose a move

    def update(self, moveToTake):
        ''' (self, int) -> None... updates currentPath and rewardSum with the consequence of taking the move'''
        self.currentPath.append(moveToTake) # add the move we took to currentPath
        # TODO: update rewardSum... possibly something like "self.rewardSum += self.world.blockRewardDict[moveToTake] + self.world.qTableDict[moveToTake]
        # TODO: update self.world.expectedBlockRewardDict by distributing our rewardSum through all blocks in self.currentPath
        # TODO: if we hit lava, set self.hitLava to true
        # TODO: if we hit a reward block, remrove it from self.remainingRewards... "if self.world.blocks[moveToMake] == 'emerald_block": self.remainingRewards.remove(moveToMake)



