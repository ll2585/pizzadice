from pizzadice import roll
import random

class Player:
    def __init__(self, name):
        self.brains = 0
        self.type = "GENERIC"
        self.name = name
    
    def updateName(self):
        self.name = "%s - %s" %(self.name, self.type)
    
    def chooseToRollAgain(self, gameState, situation, results):
        pass
        
    def rollAgain(self, gameState, situation):
        return self.chooseToRollAgain(gameState, situation)
        
class Human(Player):
    def __init__(self, name):
        super(Human, self).__init__(name)
        
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
            return self.alternateStrat.rollAgain(gameState, situation)
        