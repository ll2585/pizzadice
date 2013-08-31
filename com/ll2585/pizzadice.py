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
RULESET = 3


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
                                'brainsRolled': 0,
                                'rolledDice': None
                                }
                #player.go(gameState, curSituation) #loop for this guys turn; returns when he is done
                if LOGGING:
                    print("%s is starting" %(player.name))
                results = roll(player, curSituation)
                #check to see if we died first turn
                if not(shotgunsRolled(results) >= SHOTGUNDEATH):
                    #if not, see if the player wants to roll again and do so until either he stops or he dies
                    while(not(shotgunsRolled(results) >= SHOTGUNDEATH) and player.chooseToRollAgain(gameState, results) ):
                        if LOGGING:
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
                    if LOGGING:
                        print("%s is eliminated"%(player.name))
                    canStillRoll[playerIndex] = False
                
            if gameState['scores'][player.name] >= 13: 
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
            if LOGGING:
                print("Game over!")
                print("%s wins!" %(LEADER.name))
            return gameState
        
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
    return {'cup': cup, 'hand': hand, 'keptDice': keptDice, 'brainsRolled': brainsRolled, 'rolledDice': rolledDice}
    

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


def runTournament(players, numGames):
    """A tournament is one or more games of Zombie Dice. The bots are re-used between games, so they can remember previous games.
    zombies is a list of zombie bot objects. numGames is an int of how many games to run."""
    global TOURNAMENT_STATE
    TOURNAMENT_STATE = {'gameNumber': 0,
                        'wins': dict([(zombie.name, 0) for zombie in players]),
                        'ties': dict([(zombie.name, 0) for zombie in players])}

    print('Tournament of %s games started...' % (numGames))

    for TOURNAMENT_STATE['gameNumber'] in range(numGames):
        random.shuffle(players) # randomize the order
        endState = runGame(players) # use the same zombie objects so they can remember previous games.
        
        #print ("End score: %s" %(endState['scores']))
        if endState is None:
            sys.exit('Error when running game.')

        ranking = sorted(endState['scores'].items(), key=lambda x: x[1], reverse=True)
        highestScore = ranking[0][1]
        winners = [x[0] for x in ranking if x[1] == highestScore]
        if len(winners) == 1:
            TOURNAMENT_STATE['wins'][ranking[0][0]] += 1
        elif len(winners) > 1:
            for score in endState['scores'].items():
                if score[1] == highestScore:
                    TOURNAMENT_STATE['ties'][score[0]] += 1

    TOURNAMENT_STATE['gameNumber'] += 1 # increment to show all games are finished

    # print out the tournament results in neatly-formatted columns.
    print('Tournament results:')
    maxNameLength = max([len(zombie.name) for zombie in players])

    winsRanking = sorted(TOURNAMENT_STATE['wins'].items(), key=lambda x: x[1], reverse=True)
    print('Wins:')
    for winnerName, winnerScore in winsRanking:
        print('    %s %s' % (winnerName.rjust(maxNameLength), str(winnerScore).rjust(len(str(numGames)))))

    tiesRanking = sorted(TOURNAMENT_STATE['ties'].items(), key=lambda x: x[1], reverse=True)
    print('Ties:')
    for tiedName, tiedScore in tiesRanking:
        print('    %s %s' % (tiedName.rjust(maxNameLength), str(tiedScore).rjust(len(str(numGames)))))



if __name__ == '__main__':
    human = pizzadiceplayers.Human("Luke")
    mcbot = pizzadiceplayers.MonteCarloBot("Alan")
    dumbbot2 = pizzadiceplayers.Dumbbot("Bob")
    dumbbot3 = pizzadiceplayers.Dumbbot("Charlie")
    rollbot = pizzadiceplayers.RollsUntilInTheLeadBot("Dean")
    scaredBot = pizzadiceplayers.ScaredBot("Edgar")
    players = [mcbot, dumbbot2, dumbbot3, rollbot, scaredBot]
    LOGGING = False
    runTournament(players, 1000)
