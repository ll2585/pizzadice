import random, pizzadiceplayers
RED = "RED"
GREEN = "GREEN"
YELLOW = "YELLOW"
BRAIN = "BRAIN"
SHOTGUN = "SHOTGUN"
FEET = "FEET"

def rollDice(color):
    side = random.randint(1,6)
    if color == RED:
        return BRAIN if side == 1 else SHOTGUN if side < 5 else FEET
    if color == YELLOW:
        return BRAIN if side < 3 else SHOTGUN if side < 5 else FEET
    if color == GREEN:
        return BRAIN if side < 4 else SHOTGUN if side < 5 else FEET
    

def runGame(playerList):
    global CURPLAYER, BASECUP, CURCUP, CURHAND, NUMBLASTS, NUMBRAINS, BRAINDICE
    scores = dict([(player.name, 0) for player in playerList])
    CUP = [GREEN]*6+  [YELLOW] * 4 + [RED]*3
    
    gameState = {'players': playerList,
                 'scores': scores,
                 'round': 0}
    #play 1 round
    while True:
        for player in playerList:
            CURPLAYER = player
            CURCUP = list(CUP)
            random.shuffle(CURCUP)
            hand = []
            NUMBLASTS = 0
            NUMBRAINS = 0
            BRAINDICE = []
            player.go(gameState) #loop for this guys turn
            if NUMBLASTS < 3:
                gameState[scores][player.name] += 
            
            
def roll():
    
    print("1")
    

if __name__ == '__main__':
    human = pizzadiceplayers.Human()
    dumbbot = pizzadiceplayers.Dumbbot()
    players = [human, dumbbot]
    runGame(players)