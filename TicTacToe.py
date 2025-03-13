# THIS IS A GAME OF TIC TAC TOE YOU CAN PLAY AGAINST THE COMPUTER OR ANOTHER PLAYER #

# AUTHOR: Florian Germann
# LAST CHANGED: 2025-02-16
# LAST CHANGED BY: Piet Kreuzmann

#######################################################################################

import random

#-------------------------------------------------------------------------------------

#empty Playfield creation
arr_playfield = [["1", "2", "3"],
                 ["4", "5", "6"],
                 ["7", "8", "9"]]

def printPlayfield():
    print("\n")
    print(" " + arr_playfield[0][0] + " | " + arr_playfield[0][1] + " | " + arr_playfield[0][2])
    print("---+---+---")
    print(" " + arr_playfield[1][0] + " | " + arr_playfield[1][1] + " | " + arr_playfield[1][2])
    print("---+---+---")
    print(" " + arr_playfield[2][0] + " | " + arr_playfield[2][1] + " | " + arr_playfield[2][2])
    print("\n")

#Merker Variablen Deklaration
gameEnded = False
playerOneTurn = True
userInput = 1
moveCount = 0
gameStatus = 0
computerOpponent = False
botDifficulty = 0

#pool of legal moves for the bot
def getLegalMoves():
    legalMoves = []  
    for i in range(1, 10):  
        if not(arr_playfield[findPlayedRow(i)][findPlayedColumn(i)] == "X" or arr_playfield[findPlayedRow(i)][findPlayedColumn(i)] == "O"):
            legalMoves.append(i)
    return legalMoves  

#Funktion zur Inputüberprüfung
def isInputValid(input):
    if (input > 0) and (input < 10):
        if not(arr_playfield[findPlayedRow(input)][findPlayedColumn(input)] == "X" or arr_playfield[findPlayedRow(input)][findPlayedColumn(input)] == "O"):
            return True
        else:
            print("Entered Space is already taken")
            return False
    else:
        print("Entered Charakter was invalid")
        return False

#Funktion zum Herausfinden der Zeile
def findPlayedRow(input):
    if input <= 3:
        return 0
    elif input <= 6:
        return 1
    elif input <= 9:
        return 2
    else:
        return None
    
#Funktion zum Herausfinden der Spalte
def findPlayedColumn(input):
    row = findPlayedRow(input) 
    column = input - (row * 3 + 1)
    return column

#check for game ending
def checkPlayerWon(player):
    # Überprüfung von Spalten
    for col in range(3):
        if arr_playfield[0][col] == player and arr_playfield[1][col] == player and arr_playfield[2][col] == player:
            return 1

    # Überprüfung von Zeilen
    for row in range(3):
        if arr_playfield[row][0] == player and arr_playfield[row][1] == player and arr_playfield[row][2] == player:
            return 1

    # Überprüfung der Hauptdiagonale
    if arr_playfield[0][0] == player and arr_playfield[1][1] == player and arr_playfield[2][2] == player:
        return 1

    # Überprüfung der Gegendiagonale
    if arr_playfield[0][2] == player and arr_playfield[1][1] == player and arr_playfield[2][0] == player:
        return 1

    # Unentschieden prüfen
    if moveCount == 9:
        return 2

    return 0

def canBotWin():
    for move in getLegalMoves():
        row = findPlayedRow(move)
        column = findPlayedColumn(move)

        arr_playfield[row][column] = "O"
        if checkPlayerWon("O") == 1:
            arr_playfield[row][column] = str(move)  # revert the move
            return move
        arr_playfield[row][column] = str(move)  # revert the move
    return None

def canBotBlock():
    for move in getLegalMoves():
        row = findPlayedRow(move)
        column = findPlayedColumn(move)

        arr_playfield[row][column] = "X"
        if checkPlayerWon("X") == 1:
            arr_playfield[row][column] = str(move)  # revert the move
            return move
        arr_playfield[row][column] = str(move)  # revert the move
    return None

#easy bot - this bot will just place its sign randomly
def easyBot():
    global userInput
    legalMoves = getLegalMoves()
    randomMove = random.choice(legalMoves)
    arr_playfield[findPlayedRow(randomMove)][findPlayedColumn(randomMove)] = "O"
    printPlayfield()
    userInput = randomMove

#medium bot - this bot will try to win itself if possible, otherwise it will just place its sign randomly
def mediumBot():
    global userInput
    if canBotWin() != None:
        arr_playfield[findPlayedRow(canBotWin())][findPlayedColumn(canBotWin())] = "O"
        printPlayfield()
        userInput = canBotWin()
    else:
        easyBot()

def hardBot():
    global userInput

    # 1. Prüfen, ob der Bot direkt gewinnen kann
    winMove = canBotWin()
    if winMove is not None:
        row, col = findPlayedRow(winMove), findPlayedColumn(winMove)
        arr_playfield[row][col] = "O"
        #printPlayfield()
        userInput = winMove
        return

    # 2. Prüfen, ob der Bot den Spieler blockieren muss
    blockMove = canBotBlock()
    if blockMove is not None:
        row, col = findPlayedRow(blockMove), findPlayedColumn(blockMove)
        arr_playfield[row][col] = "O"
        #printPlayfield()
        userInput = blockMove
        return

    # 3. Falls kein direkter Gewinn oder Block möglich ist → Minimax verwenden
    bestMove = None
    bestScore = float('-inf')

    for move in getLegalMoves():
        row = findPlayedRow(move)
        column = findPlayedColumn(move)

        arr_playfield[row][column] = "O"  # Testweise den Zug setzen
        #printPlayfield()
        score = minimax(False)  # Minimax für den Gegner aufrufen
        arr_playfield[row][column] = str(move)  # Zug zurücksetzen

        if score > bestScore:
            bestScore = score
            bestMove = move

    if bestMove is not None:
        row = findPlayedRow(bestMove)
        column = findPlayedColumn(bestMove)
        arr_playfield[row][column] = "O"
        #printPlayfield()
        userInput = bestMove

def minimax(isMaximizing):
    winner_X = checkPlayerWon("X")
    winner_O = checkPlayerWon("O")

    if winner_O == 1:  # Bot gewinnt
        return 1
    elif winner_X == 1:  # Spieler gewinnt
        return -1
    elif len(getLegalMoves()) == 0:  # Unentschieden
        return 0

    if isMaximizing:
        bestScore = float('-inf')
        for move in getLegalMoves():
            row = findPlayedRow(move)
            column = findPlayedColumn(move)

            arr_playfield[row][column] = "O"
            score = minimax(False)
            arr_playfield[row][column] = str(move)  # Zug zurücksetzen

            bestScore = max(score, bestScore)
        return bestScore

    else:
        bestScore = float('inf')
        for move in getLegalMoves():
            row = findPlayedRow(move)
            column = findPlayedColumn(move)

            arr_playfield[row][column] = "X"
            score = minimax(True)
            arr_playfield[row][column] = str(move)  # Zug zurücksetzen

            bestScore = min(score, bestScore)
        return bestScore
    
def startQuestionaire():
    global computerOpponent
    global botDifficulty

    # Spielstart
    print("Welcome to TicTacToe")
    print("Do you want to play TicTacToe alone? (y/n)")

    while True:
        userinput = input()
        if userinput == "y":
            print("You will play against the computer")
            computerOpponent = True
            break
        elif userinput == "n":
            print("You will play against another player")
            computerOpponent = False
            break
        else:
            print("Please enter a valid input")

    if computerOpponent:
        print("Should the Bot be easy medium or hard? (e/m/h)")
        while True:
            userinput = input()
            if userinput == "e":
                print("Bot is easy")
                botDifficulty = 0
                break
            elif userinput == "m":
                print("Bot is medium")
                botDifficulty = 1
                break
            elif userinput == "h":
                print("Bot is hard")
                botDifficulty = 2
                break
            else:
                print("Please enter a valid input")

    print("The Game will start now")
    print("Player 1 starts the game")

    printPlayfield()

#-------------------------------------------------------------------------------------

startQuestionaire()

while not gameEnded:
    # Zug Spieler 1
    if playerOneTurn:
        print("Player 1, please Enter the desired Space for your X to be placed")

        # Nutzerinput setzen und überprüfen
        try:
            userInput = int(input())
        except:
            print("Please Enter a Number")

        while isInputValid(userInput) == False:
            try:
                userInput = int(input())
            except:
                print("Please Enter a Number")

        # Setzen des Spielzeichens
        arr_playfield[findPlayedRow(userInput)][findPlayedColumn(userInput)] = "X"

        # Ausgabe Spielfeld
        printPlayfield()

        # Prüfen, ob ein Spieler gewonnen hat
        gameStatus = checkPlayerWon("X") if not playerOneTurn else checkPlayerWon("O")
        match gameStatus:
            case 1:
                print("Player 1 Won")
                gameEnded = True
                break
            case 2:
                print("Draw")
                gameEnded = True
                break

        playerOneTurn = False

    # Zug Spieler 2
    else:
        if computerOpponent:
            print("Bot is thinking")
            # Botzug
            if botDifficulty == 0:
                easyBot()
            elif botDifficulty == 1:
                mediumBot()
            elif botDifficulty == 2:
                hardBot()
        else:
            print("Player 2, please Enter the desired Space for your O to be placed")

            # Nutzerinput setzen und überprüfen
            try:
                userInput = int(input())
            except:
                print("Please Enter a Number")

            while isInputValid(userInput) == False:
                try:
                    userInput = int(input())
                except:
                    print("Please Enter a Number")

            # Setzen des Spielzeichens
            arr_playfield[findPlayedRow(userInput)][findPlayedColumn(userInput)] = "O"

        # Ausgabe Spielfeld
        printPlayfield()
        # Prüfen, ob ein Spieler gewonnen hat
        gameStatus = checkPlayerWon("X") if playerOneTurn else checkPlayerWon("O")
        match gameStatus:
            case 1:
                if computerOpponent:
                    print("Bot Won")
                else:
                    print("Player 2 Won")
                gameEnded = True
                break
            case 2:
                print("Draw")
                gameEnded = True
                break

        playerOneTurn = True

    moveCount += 1
