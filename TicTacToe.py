# THIS IS A GAME OF TIC TAC TOE YOU CAN PLAY AGAINST THE COMPUTER OR ANOTHER PLAYER #

# AUTHOR: Florian Germann
# LAST CHANGED: 2025-02-16
# LAST CHANGED BY: Piet Kreuzmann

#######################################################################################

import random

#-------------------------------------------------------------------------------------

#empty Playfield creation
arr_playfield = [["1","2","3"],
                 ["4","5","6"],
                 ["7","8","9"]]

#Merker Variablen Deklaration
gameEnded = False
playerOneTurn = True
userInput = 0
moveCount = 0
gameStatus = 0
computerOpponent = False
botDifficulty = 0

#pool of legal moves for the bot
def getLegalMoves():
    legalMoves = []
    for i in range(1,10):
        if not(arr_playfield[findPlayedRow(i)][findPlayedColumn(i)] == "X" or arr_playfield[findPlayedRow(i)][findPlayedColumn(i)] == "O"):
            legalMoves.append(i)
    return legalMoves

#Funktion zur Inputüberprüfung
def isInputValid(input):
    if (input > 0) and (input < 10):

        if not(arr_playfield[findPlayedRow(input)][findPlayedColumn(input)] == "X" or arr_playfield[findPlayedRow(input)][findPlayedColumn(input)] == "O") :
            return True
        else : 
            print("Entered Space is already taken")
            return False

    else :

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
        return 
    
#Funktion zum Herausfinden der Spalte
def findPlayedColumn(input):

    row = findPlayedRow(input) 
    column = input - (row * 3 + 1)
    return column

#check for game ending
def checkPlayerWon():
    #check column
    for i in range(0,3):
        if arr_playfield[i][findPlayedColumn(userInput)] != arr_playfield[findPlayedRow(userInput)][findPlayedColumn(userInput)]:
            break
        if i == 2:
            return 1

    #check line
    for i in range(0,3):
        if arr_playfield[findPlayedRow(userInput)][i] != arr_playfield[findPlayedRow(userInput)][findPlayedColumn(userInput)]:
            break
        if i == 2:
            return 1

    #check diagonal
    if findPlayedRow(userInput) == findPlayedColumn(userInput):
        for i in range(0,3):
            if arr_playfield[i][i] != arr_playfield[findPlayedRow(userInput)][findPlayedColumn(userInput)]:
                break
            if i == 2:
                return 1

    #check antidiagonal
    if findPlayedRow(userInput) + findPlayedColumn(userInput) == 2:
        for i in range(0,3):
            if arr_playfield[i][2-i] != arr_playfield[findPlayedRow(userInput)][findPlayedColumn(userInput)]:
                break
            if i == 2:
                return 1

    #check draw
    if moveCount == 9:
        return 2

    return 0

def canBotWin():
    for move in getLegalMoves():
        row = findPlayedRow(move)
        column = findPlayedColumn(move)
        arr_playfield[row][column] = "O"
        if checkPlayerWon() == 1:
            arr_playfield[row][column] = str(move)  # revert the move
            return move
        arr_playfield[row][column] = str(move)  # revert the move
    return None


#easy bot - this bot will just place its sign randomly
def easyBot():
    legalMoves = getLegalMoves()
    randomMove = random.choice(legalMoves)
    arr_playfield[findPlayedRow(randomMove)][findPlayedColumn(randomMove)] = "O"
    
#medium bot - this bot will try to win itself if possible, otherwise it will just place its sign randomly
def mediumBot():
    print("medium")

#hard bot - this bot will try to win itself if possible, otherwise block the player from winning, otherwise it will just place its sign randomly
def hardBot():
    print("hard")

def startQuestionaire():
    global computerOpponent
    global botDifficulty

    #Spielstart
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


    if(computerOpponent):
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


    print( arr_playfield[0] , '\n' , arr_playfield[1] , '\n' , arr_playfield[2])


#-------------------------------------------------------------------------------------

startQuestionaire()


while not gameEnded :

    #Zug Spieler 1
    if playerOneTurn : 

        print("Player 1, please Enter the desired Space for your X to be placed")

        #Nutzerinput setzen und überprüfen
        try:
            userInput = int(input())
        except:
            print("Please Enter a Number")

        while isInputValid(userInput) == False:
            try:
                userInput = int(input())
            except:
                print("Please Enter a Number")


        #Setzen des Spielzeichens
        arr_playfield[findPlayedRow(userInput)][findPlayedColumn(userInput)] = "X"

        #Ausgabe Spielfeld
        print( arr_playfield[0] , '\n' , arr_playfield[1] , '\n' , arr_playfield[2])


        #prüfen, ob ein Spieler gewonnen hat
        gameStatus = checkPlayerWon()
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

    #Zug Spieler 2
    else :
        if(computerOpponent):
            print("Bot is thinking")
            #Botzug
            if botDifficulty == 0:
                easyBot()
            elif botDifficulty == 1:
                mediumBot()
            elif botDifficulty == 2:
                hardBot()


        else:

            print("Player 2, please Enter the desired Space for your O to be placed")


            #Nutzerinput setzen und überprüfen
            try:
                userInput = int(input())
            except:
                print("Please Enter a Number")

            while isInputValid(userInput) == False:
                try:
                    userInput = int(input())
                except:
                    print("Please Enter a Number")


            #Setzen des Spielzeichens
            arr_playfield[findPlayedRow(userInput)][findPlayedColumn(userInput)] = "O"


        #Ausgabe Spielfeld
        print( arr_playfield[0] , '\n' , arr_playfield[1] , '\n' , arr_playfield[2])


        #prüfen, ob ein Spieler gewonnen hat
        gameStatus = checkPlayerWon()
        match gameStatus:
            case 1: 
                print("Player 2 Won")
                gameEnded = True
                break
            case 2:
                print("Draw")
                gameEnded = True
                break

        playerOneTurn = True

        
    moveCount += 1