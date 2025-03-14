# THIS IS A GAME OF TIC TAC TOE YOU CAN PLAY AGAINST THE COMPUTER OR ANOTHER PLAYER #

# AUTHOR: Florian Germann
# LAST CHANGED: 2025-02-16
# LAST CHANGED BY: Piet Kreuzmann

#######################################################################################

import random
import time

#-------------------------------------------------------------------------------------

#empty Playfield creation
arr_playfield = [["1", "2", "3"],
                 ["4", "5", "6"],
                 ["7", "8", "9"]]

# ANSI Escape Codes for colors
RED = "\033[91m"  # Rotes X
BLUE = "\033[94m"  # Blaues O
RESET = "\033[0m"  # Zurück zur Standardfarbe

def printPlayfield():
    print("\n")
    for row in arr_playfield:
        print(" " + 
              (RED + row[0] + RESET if row[0] == "X" else BLUE + row[0] + RESET if row[0] == "O" else row[0]) + " | " +
              (RED + row[1] + RESET if row[1] == "X" else BLUE + row[1] + RESET if row[1] == "O" else row[1]) + " | " +
              (RED + row[2] + RESET if row[2] == "X" else BLUE + row[2] + RESET if row[2] == "O" else row[2]))
        if row != arr_playfield[-1]:
            print("---+---+---")
    print("\n")

# Marker variable declaration
gameEnded = False
playerOneTurn = True
userInput = 1
moveCount = 0
gameStatus = 0
computerOpponent = False
botDifficulty = 0
playerWantsToPlay = True

# Pool of legal moves for the bot
def getLegalMoves():
    legalMoves = []  
    for i in range(1, 10):  
        if not(arr_playfield[findPlayedRow(i)][findPlayedColumn(i)] == "X" or arr_playfield[findPlayedRow(i)][findPlayedColumn(i)] == "O"):
            legalMoves.append(i)
    return legalMoves  

# Function to validate input
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

# Function to determine the row
def findPlayedRow(input):
    if input <= 3:
        return 0
    elif input <= 6:
        return 1
    elif input <= 9:
        return 2
    else:
        return None
    
# Function to determine the column
def findPlayedColumn(input):
    row = findPlayedRow(input) 
    column = input - (row * 3 + 1)
    return column

# Check for game ending
def checkPlayerWon(player):
    # Check columns
    for col in range(3):
        if arr_playfield[0][col] == player and arr_playfield[1][col] == player and arr_playfield[2][col] == player:
            return 1

    # Check rows
    for row in range(3):
        if arr_playfield[row][0] == player and arr_playfield[row][1] == player and arr_playfield[row][2] == player:
            return 1

    # Check main diagonal
    if arr_playfield[0][0] == player and arr_playfield[1][1] == player and arr_playfield[2][2] == player:
        return 1

    # Check counter-diagonal
    if arr_playfield[0][2] == player and arr_playfield[1][1] == player and arr_playfield[2][0] == player:
        return 1

    # Check for a draw
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

        arr_playfield[row][column] ="X"
        if checkPlayerWon("X") == 1:
            arr_playfield[row][column] = str(move)  # revert the move
            return move
        arr_playfield[row][column] = str(move)  # revert the move
    return None

# Easy bot - this bot will just place its sign randomly
def easyBot():
    global userInput

    time.sleep(1)  # Delay for 1 second

    legalMoves = getLegalMoves()
    randomMove = random.choice(legalMoves)
    arr_playfield[findPlayedRow(randomMove)][findPlayedColumn(randomMove)] = "O"
    printPlayfield()
    userInput = randomMove

# Medium bot - this bot will try to win itself if possible, otherwise it will just place its sign randomly
def mediumBot():
    global userInput

    time.sleep(1)  # Delay for 1 second

    if canBotWin() != None:
        arr_playfield[findPlayedRow(canBotWin())][findPlayedColumn(canBotWin())] = "O"
        printPlayfield()
        userInput = canBotWin()
    else:
        easyBot()

# Hard bot - this bot will try to win, block the player, or use minimax if necessary
def hardBot():
    global userInput

    time.sleep(1)  # Delay for 1 second

     # 1. Check if the bot can win directly
    winMove = canBotWin()
    if winMove is not None:
        row, col = findPlayedRow(winMove), findPlayedColumn(winMove)
        arr_playfield[row][col] = "O"
        userInput = winMove
        return

    # 2. Check if the bot needs to block the player
    blockMove = canBotBlock()
    if blockMove is not None:
        row, col = findPlayedRow(blockMove), findPlayedColumn(blockMove)
        arr_playfield[row][col] = "O"
        userInput = blockMove
        return

    # 3. If no immediate win or block is possible → use Minimax
    bestMove = None
    bestScore = float('-inf')

    for move in getLegalMoves():
        row = findPlayedRow(move)
        column = findPlayedColumn(move)

        arr_playfield[row][column] = "O" # Test placing move
        score = minimax(False)  # Call Minimax for opponent
        arr_playfield[row][column] = str(move)  # Reset move

        if score > bestScore:
            bestScore = score
            bestMove = move

    if bestMove is not None:
        row = findPlayedRow(bestMove)
        column = findPlayedColumn(bestMove)
        arr_playfield[row][column] = "O"
        userInput = bestMove

# Minimax algorithm for optimal bot moves
def minimax(isMaximizing):
    winner_X = checkPlayerWon("X")
    winner_O = checkPlayerWon("O")

    if winner_O == 1:  # Bot wins
        return 1
    elif winner_X == 1:  # Player wins
        return -1
    elif len(getLegalMoves()) == 0:  # Draw
        return 0

    if isMaximizing:
        bestScore = float('-inf')
        for move in getLegalMoves():
            row = findPlayedRow(move)
            column = findPlayedColumn(move)

            arr_playfield[row][column] = "O"
            score = minimax(False)
            arr_playfield[row][column] = str(move)  # Reset move

            bestScore = max(score, bestScore)
        return bestScore

    else:
        bestScore = float('inf')
        for move in getLegalMoves():
            row = findPlayedRow(move)
            column = findPlayedColumn(move)

            arr_playfield[row][column] = "X"
            score = minimax(True)
            arr_playfield[row][column] = str(move)  # Reset move

            bestScore = min(score, bestScore)
        return bestScore
    
# Start questionnaire for game mode selection   
def startQuestionaire():
    global computerOpponent
    global botDifficulty

    # Game start
    print("Welcome to TicTacToe")

    # Reset the playfield and check if the player wants to play again
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

while playerWantsToPlay:

    startQuestionaire()

    while not gameEnded:
         # Player 1's turn
        if playerOneTurn:
            print("Player 1, please Enter the desired Space for your X to be placed")

             # Set and validate user input
            try:
                userInput = int(input())
            except:
                print("Please Enter a Number")

            while isInputValid(userInput) == False:
                try:
                    userInput = int(input())
                except:
                    print("Please Enter a Number")

           # Set the game piece
            arr_playfield[findPlayedRow(userInput)][findPlayedColumn(userInput)] = "X"
            moveCount += 1

            # Display the playfield
            printPlayfield()

            # Check if a player has won
            gameStatus = checkPlayerWon("X")
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

         # Player 2's turn
        else:
            if computerOpponent:
                print("Bot is thinking")
                time.sleep(1)  # Delay for 1 second
                # Bot move
                if botDifficulty == 0:
                    easyBot()
                elif botDifficulty == 1:
                    mediumBot()
                elif botDifficulty == 2:
                    hardBot()
                moveCount += 1
            else:
                print("Player 2, please Enter the desired Space for your O to be placed")

                # Set and validate user input
                try:
                    userInput = int(input())
                except:
                    print("Please Enter a Number")

                while isInputValid(userInput) == False:
                    try:
                        userInput = int(input())
                    except:
                        print("Please Enter a Number")

                # Set the game piece
                arr_playfield[findPlayedRow(userInput)][findPlayedColumn(userInput)] = "O"
                moveCount += 1

            # Ausgabe Spielfeld
            printPlayfield()
             # Check if a player has won
            gameStatus = checkPlayerWon("O")
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



#--------------------------------------------------------------------------------
# Ask if the player wants to restart the game

    print("Do you want to play again? (y/n)")

    while True:
        userinput = input()
        if userinput == "y":
            gameEnded = False
            playerOneTurn = True
            moveCount = 0
            arr_playfield = [["1", "2", "3"],
                             ["4", "5", "6"],
                             ["7", "8", "9"]]  # reset the playfield
            break
        elif userinput == "n":
            playerWantsToPlay = False
            break
        else:
            print("Please enter a valid input")

