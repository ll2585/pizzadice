import random, pizzadiceplayers
RED = "RED"
GREEN = "GREEN"
YELLOW = "YELLOW"
BRAIN = "BRAIN"
SHOTGUN = "SHOTGUN"
FEET = "FEET"
LOGGING = True


def runGame(playerList):
    scores = dict([(i, 0) for i in range(len(playerList))])
    CUP = [GREEN]*6+  [YELLOW] * 4 + [RED]*3
    
    gameState = {'players': playerList,
                 'scores': scores,
                 'round': 0}
    #play 1 round
    while True:
        playerIndex = 0
        for player in playerList:
            CURCUP = list(CUP)
            random.shuffle(CURCUP)
            hand = []
            keptDice = []
            curSituation = {'cup': CURCUP,
                            'hand': hand,
                            'keptDice': keptDice,
                            'brainsSaved': 0
                            }
            player.go(gameState, curSituation) #loop for this guys turn; returns when he is done
            NUMBRAINS = player.brainsRolledThisTurn()
            NUMBLASTS = player.shotgunsRolledThisTurn()
            if NUMBLASTS < 3:
                gameState['scores'][playerIndex] += NUMBRAINS
            playerIndex += 1
            
#returns a situation
def roll(player, situation):
    keptDice = situation['keptDice']
    hand = situation['hand']
    cup = situation['cup']
    brainsSaved = situation['brainsSaved']
    random.shuffle(cup)
    while len(hand) < 3:
        #insert code to deal with no more cups but whatever for now
        hand.append(cup.pop())
    if LOGGING:
        print("The hand is %s" %(hand))
    rolledDice = rollDice(hand)
    hand = []
    for d in rolledDice:
        if d[1] != "FEET":
            keptDice.append(d)
        else:
            hand.append(d[0])
    #if LOGGING:
        #print("rolled %s" %(rolledDice))
    return {'cup': cup, 'hand': hand, 'keptDice': keptDice, 'brainsSaved': brainsSaved}
    
def rollDice(hand):
    rolls = []
    for die in hand:
        color = die
        side = random.randint(1,6)
        result = ()
        if color == RED:
            result = (color, BRAIN) if side == 1 else (color, SHOTGUN) if side < 5 else (color, FEET)
        if color == YELLOW:
            result = (color, BRAIN) if side < 3 else (color, SHOTGUN) if side < 5 else (color, FEET)
        if color == GREEN:
            result = (color, BRAIN) if side < 4 else (color, SHOTGUN) if side < 5 else (color, FEET)
        rolls.append(result)
    return rolls
    

def rolledThreeShotguns(situation):
    shotguns = 0
    if len(situation['keptDice']) > 0:
        for d in situation['keptDice']:
            if d[1] == "SHOTGUN":
                shotguns += 1
    return shotguns == 3
    

if __name__ == '__main__':
    human = pizzadiceplayers.Human()
    dumbbot = pizzadiceplayers.Dumbbot()
    dumbbot2 = pizzadiceplayers.Dumbbot()
    players = [dumbbot2, dumbbot]
    runGame(players)