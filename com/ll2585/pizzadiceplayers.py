from pizzadice import roll, rolledThreeShotguns
import random

class Player:
    def __init__(self):
        self.brains = 0
        self.name = "Me"
        self.brainsRolled = 0
        self.shotgunsRolled = 0
    
    def go(self, gameState, situation):
        self.reset()
        results = roll(self, situation) #first roll
        self.updateResults(results)
        self.goAgain(gameState, situation, results)
    
    def goAgain(self, gameState, situation, results):
        pass
        
    def brainsRolledThisTurn(self):
        return self.brainsRolled
    
    def shotgunsRolledThisTurn(self):
        return self.shotgunsRolled
    
    def updateResults(self, situation):
        rolledDice = situation['keptDice']
        if len(rolledDice) > 0:
            for d in rolledDice:
                if d[1] == "SHOTGUN":
                    self.shotgunsRolled += 1
                if d[1] == "BRAIN":
                    self.brainsRolled += 1
            self.brainsRolled += situation['brainsSaved']
            if self.shotgunsRolled >= 3:
                self.brainsRolled = 0
    
    def reset(self):
        self.brainsRolled = 0
        self.shotgunsRolled = 0
        
class Human(Player):
    def __init__(self):
        super(Human, self).__init__()
        
class Dumbbot(Player):
    def __init__(self):
        super(Dumbbot, self).__init__()
        self.name = "Dumb Bot"
        
    def goAgain(self, gameState, situation, results):
        reRoll = random.randint(0,1)
        while not(rolledThreeShotguns(results)) and reRoll == 1:
            results = roll(self, situation)
            self.updateResults(results)
            reRoll = random.randint(0,1)
        