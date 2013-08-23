import random, pizzadiceplayers, sys
RED = "RED"
GREEN = "GREEN"
YELLOW = "YELLOW"
BRAIN = "BRAIN"
SHOTGUN = "SHOTGUN"
FEET = "FEET"
SHOTGUNDEATH = 3
LOGGING = True

#0 = A has 12, B has 13, A doesnt get a chance
#1 = A has 12, B has 13, A gets one chance
#2 = A has 12, B has 13, A gets a chance, and then B gets last chance
#3 = A has 12, B has 13, A gets a chance, B gets a chance, then A then B until someone dies
RULESET = 2


def runGame(playerList):
    scores = dict([(player.name, 0) for player in playerList])
    canStillRoll = [True] * len(playerList)
    CUP = [GREEN]*6+  [YELLOW] * 4 + [RED]*3
    
    gameState = {'players': playerList,
                 'scores': scores,
                 'round': 0}
    #play 1 round
    gameOver = False
    lastRound = False
    LEADER = None
    LEADERSCORE = 0
    while True:
        playerIndex = 0
        for player in playerList:
            if(lastRound and LEADER == player):
                canStillRoll[playerIndex] = False
                break
            if canStillRoll[playerIndex]:
                CURCUP = list(CUP)
                random.shuffle(CURCUP)
                hand = []
                keptDice = []
                curSituation = {'cup': CURCUP,
                                'hand': hand,
                                'keptDice': keptDice,
                                'brainsRolled': 0
                                }
                #player.go(gameState, curSituation) #loop for this guys turn; returns when he is done
                print("%s is starting" %(player.name))
                results = roll(player, curSituation)
                #check to see if we died first turn
                if not(shotgunsRolled(results) >= SHOTGUNDEATH):
                    #if not, see if the player wants to roll again and do so until either he stops or he dies
                    while(player.rollAgain(gameState, results) and not(shotgunsRolled(results) >= SHOTGUNDEATH)):
                        print("%s is going again" %(player.name))
                        results = roll(player, results)
                        
                #tabulation of scores; if he didnt die add score
                if not(shotgunsRolled(results) >= SHOTGUNDEATH):
                    brainsRolled = results['brainsRolled']
                    gameState['scores'][player.name] += brainsRolled
                else:
                    brainsRolled = 0

                NUMBRAINS = brainsRolled
                NUMBLASTS = shotgunsRolled(results)
                if LOGGING:
                    print("%s finished rolling with %s brains and %s blasts" %(player.name, NUMBRAINS, NUMBLASTS))
                    print("The scores are: %s" %(gameState['scores']))
                    
                if gameState['scores'][player.name] > LEADERSCORE:
                    LEADER = player
                    LEADERSCORE = gameState['scores'][player.name]
                    if LOGGING:
                        print("%s takes the lead with %s brains!" %(player.name, gameState['scores'][player.name]))
                        
            if lastRound:
                if RULESET != 3 or shotgunsRolled(results) >= SHOTGUNDEATH or (RULESET == 3 and player != LEADER):
                    print("%s is eliminated"%(player.name))
                    canStillRoll[playerIndex] = False
                
            if gameState['scores'][player.name] >= 13: 
                print("SHOWDOWN")
                if RULESET == 0:
                    lastRound = True
                    for i in range(0, playerIndex+1):
                        canStillRoll[i] = False
                if RULESET == 1:
                    lastRound = True
                    canStillRoll[playerIndex] = False
                if RULESET == 2 or RULESET == 3:
                    lastRound = True

                
            playerIndex += 1
            
        gameOver = gameIsOver(canStillRoll)
        if gameOver:
            print("Game over!")
            print("%s wins!" %(LEADER.name))
            break
        
def gameIsOver(canStillRoll):
    for i in canStillRoll:
        if i: return False
    return True
            
    
#returns a situation
def roll(player, situation):
    keptDice = situation['keptDice']
    hand = situation['hand']
    cup = situation['cup']
    brainsRolled = situation['brainsRolled']
    if shotgunsRolled(situation) >= SHOTGUNDEATH:
        sys.exit(0)

    if(len(cup) < 3):
        if LOGGING:
            pass
            #print("out of dice!")
        newKept = []
        for d in keptDice:
            if d[1] == BRAIN:
                cup.append(d[0])
            else:
                newKept.append(d)
        keptDice = newKept
    random.shuffle(cup)
    while len(hand) < 3:
        hand.append(cup.pop())
    if LOGGING:
        pass
        #print("The hand is %s" %(hand))
    rolledDice = rollDice(hand)
    hand = []
    for d in rolledDice:
        if d[1] != FEET:
            if d[1] == BRAIN:
                brainsRolled += 1
            keptDice.append(d)
        else:
            hand.append(d[0])
    if LOGGING:
        pass
        print("rolled %s" %(rolledDice))
        #print("now the cup is %s" %(cup))
        #print("and the hand is %s, the kept dice are %s" %(hand, keptDice))
    return {'cup': cup, 'hand': hand, 'keptDice': keptDice, 'brainsRolled': brainsRolled}
    

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

def shotgunsRolled(situation):
    shotguns = 0
    if len(situation['keptDice']) > 0:
        for d in situation['keptDice']:
            if d[1] == SHOTGUN:
                shotguns += 1
    return shotguns


if __name__ == '__main__':
    human = pizzadiceplayers.Human("Luke")
    dumbbot = pizzadiceplayers.Dumbbot("Alan")
    dumbbot2 = pizzadiceplayers.Dumbbot("Bob")
    dumbbot3 = pizzadiceplayers.Dumbbot("Charlie")
    rollbot = pizzadiceplayers.RollsUntilInTheLeadBot("Dean")
    scaredBot = pizzadiceplayers.ScaredBot("Edgar")
    players = [dumbbot, dumbbot2, dumbbot3, rollbot, scaredBot]
    runGame(players)