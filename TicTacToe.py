#empty Playfield creation
arr_playfield = [["1","2","3"],
                 ["4","5","6"],
                 ["7","8","9"]]

#Merker Variablen Deklaration
onePlayerWon = False
playerOneTurn = True
userInput = 0


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


#-------------------------------------------------------------------------------------

while not onePlayerWon :
    #Ausgabe Spielfeld
    print( arr_playfield[0] , '\n' , arr_playfield[1] , '\n' , arr_playfield[2])

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

        playerOneTurn = False

    #Zug Spieler 2
    else :
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

        playerOneTurn = True