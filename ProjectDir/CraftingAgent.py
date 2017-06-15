import MalmoPython as Malmo
from collections import defaultdict, deque
from numpy import random as nprandom
from random import choice


class CraftAgent:
    #ACTIONS = CRAFT THING, WAIT
    #STATES = CONTENTS OF INVENTORY


    def __init__(self, world, alpha=0.3, gamma=1, n=1):

        """Constructing an RL agent.

        Args
            alpha:  <float>  learning rate      (default = 0.3)
            gamma:  <float>  value decay rate   (default = 1)
            n:      <int>    number of back steps to update (default = 1)
        """

        self.epsilon = 0.25  # chance of taking a random action instead of the best
        self.world = world
        self.qTable = self.createQTable()
        self.n, self.alpha, self.gamma = n, alpha, gamma
        self.inventory = world.inventoryItemsAsSet
        self.numItems = 0
        self.ourAgent = Malmo.AgentHost()
        self.actions = ["craft thing", "craft thingy", "craft thingamajig", "wait"]

        self.recipes = {'thing': set('cheese', 'pickle'), 'thingy': set('cheese', 'pickle', 'ham'),'thingamajig': set('cheese', 'anitfreeze', 'russian mafia')}
        self.rewards = {'thing': 10, 'thingy': 20, 'thingamjig': 100, 'bad': -20} #maybe move to malmo?

    def createQTable(self):
        outerDef = lambda: defaultdict(int) #action : Reward
        return defaultdict(outerDef) # state : action


    def update_q_table(self, tau, S, A, R, T, oldState):
        """Performs relevant updates for state tau.

        Args
            tau: <int>  state index to update
            S:   <dequqe>   states queue
            A:   <dequqe>   actions queue
            R:   <dequqe>   rewards queue
            T:   <int>      terminating state index
        """
        curr_s, curr_a, curr_r = S.popleft(), A.popleft(), R.popleft()
        G = sum([self.gamma ** i * R[i] for i in range(len(S))])
        if tau + self.n < T:
            G += self.gamma ** self.n * self.q_table[S[-1]][A[-1]]

        old_q = self.q_table[curr_s][curr_a]
        self.q_table[curr_s][curr_a] = old_q + self.alpha * (G - old_q)

    def chooseAction(self, currState, possActs, eps): #possible actions is list
        """Chooses an action according to eps-greedy policy. """

        if currState not in self.q_table:
            self.q_table[currState] = {}

        for action in possActs:
            if action not in self.q_table[currState]:
                self.q_table[currState][action] = 0

        if nprandom.random_sample() < eps:
            return choice(possActs)

        else:
            bestActions = []
            bestVal = float("-inf")
            possible_actions = set(possActs)

            for action, value in self.qTable[currState].items():
                if (value > bestVal) and action in (possible_actions):
                    bestVal = value
                    bestActions = [action]

                elif (value == bestVal) and action in (possible_actions):
                    bestActions.append(action)

            if len(bestActions) != 0: #May not need because
                return choice(bestActions)

            else:
                return choice(possible_actions)


    def isValidCraft(self):
        pass

    def possibleActions(self): #maybe????/
        pass

    def takeAction(self):
        pass

    def checkInventory(self):
        return self.world.inventoryItemsAsSet()