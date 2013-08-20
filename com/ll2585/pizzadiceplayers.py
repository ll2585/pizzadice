from pizzadice import roll

class Player:
    def __init__(self):
        self.brains = 0
        self.name = "Me"
    
    def go(self, gameState):
        roll()
        
class Human(Player):
    def __init__(self):
        super(Human, self).__init__()
        
class Dumbbot(Player):
    def __init__(self):
        super(Dumbbot, self).__init__()