import random

RED = "RED"
GREEN = "GREEN"
YELLOW = "YELLOW"
BRAIN = "BRAIN"
SHOTGUN = "SHOTGUN"
FEET = "FEET"

class Player:
    def __init__(self):
        self.brains = 0
        
        
def rollDice(color):
    side = random.randint(1,6)
    if color == RED:
        return BRAIN if side == 1 else SHOTGUN if side < 5 else FEET
    if color == YELLOW:
        return BRAIN if side < 3 else SHOTGUN if side < 5 else FEET
    if color == GREEN:
        return BRAIN if side < 4 else SHOTGUN if side < 5 else FEET
    

def runGame():
    cup = [GREEN, GREEN, GREEN, GREEN, GREEN, GREEN,  YELLOW, YELLOW, YELLOW, YELLOW, RED, RED, RED]
    hand = []
    random.shuffle(cup)
    hand.append(cup.pop())
    hand.append(cup.pop())
    hand.append(cup.pop())
    for c in hand:
        print (rollDice(c))
    

if __name__ == '__main__':
    runGame()