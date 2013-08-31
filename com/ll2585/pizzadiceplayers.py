import random


class Player:
    def __init__(self, name):
        self.brains = 0
        self.type = "GENERIC"
        self.name = name
    
    def updateName(self):
        self.name = "%s - %s" %(self.name, self.type)
    
    def chooseToRollAgain(self, gameState, situation):
        pass
        
class Human(Player):
    def __init__(self, name):
        super(Human, self).__init__(name)
        
    def chooseToRollAgain(self, gameState, situation):
        print("rolled %s" %(situation['rolledDice']))
        result = input("Roll again (Y/N)?: ")
        while result != "Y" and result != "N":
            result = input("Roll again (Y/N)?: ")
        return True if result == "Y" else False
        
class Dumbbot(Player):
    def __init__(self, name):
        super(Dumbbot, self).__init__(name)
        self.type = "Dumb Bot"
        self.updateName()

    def chooseToRollAgain(self, gameState, situation):
        if situation['brainsRolled'] == 0: return True
        reRoll = random.randint(0,1)
        return reRoll == 1
        
class ScaredBot(Player):
    def __init__(self, name, stopAt = 2):
        super(ScaredBot, self).__init__(name)
        self.type = "Scared Bot"
        self.updateName()
        self.stopAt = stopAt

    def chooseToRollAgain(self, gameState, situation):
        shotGunsRolled = 0
        for d in situation['keptDice']:
            if d[1] == "SHOTGUN":
                shotGunsRolled+=1
        return shotGunsRolled < self.stopAt
    
class RollsUntilInTheLeadBot(Player):
    """This bot's strategy is to keep rolling for brains until they are in the lead (plus an optional number of points). This is a high risk strategy, because if the opponent gets an early lead then this bot will take greater and greater risks to get in the lead in a single turn.

    However, once in the lead, this bot will just use Zombie_MinNumShotgunsThenStops's strategy."""
    def __init__(self, name, buffer=0, stopAt = 2):
        super(RollsUntilInTheLeadBot, self).__init__(name)
        self.type = "Greedy Bot"
        self.updateName()
        self.buffer = buffer
        self.alternateStrat = ScaredBot(name + "_alt", stopAt)

    def chooseToRollAgain(self, gameState, situation):
        maxScore = 0
        name = ""
        for key in gameState['scores']:
            if gameState['scores'][key] > maxScore:
                maxScore = gameState['scores'][key]
                name = key
        if name != self.name and maxScore >= gameState['scores'][self.name] +situation['brainsRolled']+ self.buffer:
            return True
        else:
            return self.alternateStrat.chooseToRollAgain(gameState, situation)
        
        
class MonteCarloBot(Player):
    """This bot does several experimental dice rolls with the current cup, and re-rolls if the chance of 3 shotguns is less than "riskiness".
    The bot doesn't care how many brains it has rolled or what the relative scores are, it just looks at the chance of death for the next roll given the current cup."""
    def __init__(self, name, riskiness=50, numExperiments=100):
        super(MonteCarloBot, self).__init__(name)
        self.type = "MonteCarlo Bot"
        self.updateName()
        self.riskiness = riskiness
        self.numExperiments = numExperiments

    def chooseToRollAgain(self, gameState, situation):
        from pizzadice import shotgunsRolled
        shotguns = shotgunsRolled(situation)
        while True:
            # run experiments
            deaths = 0
            for i in range(self.numExperiments):
                if shotguns + self.simulatedRollShotguns(situation) >= 3:
                    deaths += 1

            # roll if percentage of deaths < riskiness%
            if deaths / float(self.numExperiments) * 100 < self.riskiness:
                return True
            else:
                return False

    def simulatedRollShotguns(self, situation):
        import copy
        """Calculates the number of shotguns rolled with the current cup and rolled brains. (Rolled brains is only used in the rare case that we run out of dice.)"""
        shotguns = 0
        cup = copy.copy(situation['cup'])
        rolledBrains = situation['brainsRolled']
        keptDice = copy.copy(situation['keptDice'])

        # "ran out of dice", so put the rolled brains back into the cup
        if len(cup) < 3:
            newKept = []
            for d in keptDice:
                if d[1] == "BRAIN":
                    cup.append(d[0])
                else:
                    newKept.append(d)
            keptDice = newKept

        # add new dice to hand from cup until there are 3 dice in the hand
        hand = copy.copy(situation['hand'])
        while len(hand) < 3:
            hand.append(cup.pop())
            
        from pizzadice import rollDice
        # roll the dice
        results = rollDice(hand)

        # count the shotguns and remove them from the hand
        for d in results:
            if d[1] == "SHOTGUN":
                shotguns += 1

        return shotguns