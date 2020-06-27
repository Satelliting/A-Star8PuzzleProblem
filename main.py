# Course: CS4242
# Student Name: Jordan Allen
# Student ID: 000719555
# Assignment #: #2
# Due Date: 06/27/2020
# Signature: ________________
# Grade: ____________________

from pprint import pprint
from time import sleep
import tkinter as tk
import random


# Handles The GUI Functionality
class MainGUI:
    def __init__(self, randomPuzzle, goalPuzzle):

        # GUI Main Section
        self.master = tk.Tk()
        self.master.title('8 Square Solution')

        # Random Square Title Labels
        tk.Label(self.master, text="Random", width=10, justify='center').grid(row=0,column=0)
        tk.Label(self.master, text="8 Square", width=10, justify='center').grid(row=1,column=0)

        # Random Square Labels
        self.rLabel1 = tk.Label(self.master, text=randomPuzzle[0][0]).grid(row=0, column=1)
        self.rLabel2 = tk.Label(self.master, text=randomPuzzle[0][1]).grid(row=0, column=2)
        self.rLabel3 = tk.Label(self.master, text=randomPuzzle[0][2]).grid(row=0, column=3)
        self.rLabel4 = tk.Label(self.master, text=randomPuzzle[1][0]).grid(row=1, column=1)
        self.rLabel5 = tk.Label(self.master, text=randomPuzzle[1][1]).grid(row=1, column=2)
        self.rLabel6 = tk.Label(self.master, text=randomPuzzle[1][2]).grid(row=1, column=3)
        self.rLabel7 = tk.Label(self.master, text=randomPuzzle[2][0]).grid(row=2, column=1)
        self.rLabel8 = tk.Label(self.master, text=randomPuzzle[2][1]).grid(row=2, column=2)
        self.rLabel9 = tk.Label(self.master, text=randomPuzzle[2][2]).grid(row=2, column=3)

        # Goal Square Title Labels
        tk.Label(self.master, text="Goal", width=10, justify='center').grid(row=0,column=4)
        tk.Label(self.master, text="8 Square", width=10, justify='center').grid(row=1,column=4)


        # Goal Square Labels
        self.gLabel1 = tk.Label(self.master, text=goalPuzzle[0][0]).grid(row=0, column=5)
        self.gLabel2 = tk.Label(self.master, text=goalPuzzle[0][1]).grid(row=0, column=6)
        self.gLabel3 = tk.Label(self.master, text=goalPuzzle[0][2]).grid(row=0, column=7)
        self.gLabel4 = tk.Label(self.master, text=goalPuzzle[1][0]).grid(row=1, column=5)
        self.gLabel5 = tk.Label(self.master, text=goalPuzzle[1][1]).grid(row=1, column=6)
        self.gLabel6 = tk.Label(self.master, text=goalPuzzle[1][2]).grid(row=1, column=7)
        self.gLabel7 = tk.Label(self.master, text=goalPuzzle[2][0]).grid(row=2, column=5)
        self.gLabel8 = tk.Label(self.master, text=goalPuzzle[2][1]).grid(row=2, column=6)
        self.gLabel9 = tk.Label(self.master, text=goalPuzzle[2][2]).grid(row=2, column=7)

        # GUI Solve Section
        self.solveButton = tk.Button(self.master, text='Solve Grid', command=lambda: main(self), state='active')
        self.solveButton.grid(row=3, column=0, sticky='nsew', columnspan=4)
        self.solveLabel  = tk.Label(self.master, text="", justify='left')
        self.solveLabel.grid(row=3,column=4, sticky='nsew', columnspan=4)

        # GUI Mainloop
        tk.mainloop()

# Handles The aStarNode Functionality (State, Child States)
class aStarNode:
    def __init__(self, a, b, f):
        self.a = a # Data Value (Heuristic Value)
        self.b = b # Level Value (Heuristic Value)
        self.f = f # 'F' Value (Heuristic Value)

    # Find All Possible Child States
    def findChildren(self):
        # Find The Empty Space Location
        x, y = self.find(self.a, '_')

        # Set Of All Possible Moves
        possibleMoves = [
            [x, y - 1], # Move Up
            [x, y + 1], # Move Down
            [x - 1, y], # Move Left
            [x + 1, y]  # Move Right
        ]

        # All Possible Child Nodes
        childNodes = []

        # Iterating Over All Possible Moves
        for move in possibleMoves:
            childState = self.checkMove(self.a, x, y, move[0], move[1])

            # Checks if Child is Not From Out of Limits
            if childState is not None:
                childNode = aStarNode(childState, self.b + 1, 0)
                childNodes.append(childNode)
        return childNodes

    def checkMove(self, puzzle, x1, y1, x2, y2):
        # Checks If Moving Blank To New Space Is In Bounds
        if x2 >= 0 and x2 < len(self.a) and y2 >= 0 and y2 < len(self.a):
            # Create A Temporary Puzzle (Future Potential Child State)
            tempPuzzle1 = []
            # Copy Current Active Puzzle
            tempPuzzle1 = self.copy(puzzle)

            # Start Manipulating Child State Puzzle
            tempPuzzle2 = tempPuzzle1[x2][y2]
            tempPuzzle1[x2][y2] = tempPuzzle1[x1][y1]
            tempPuzzle1[x1][y1] = tempPuzzle2

            return tempPuzzle1
        # If Space Is Not In Bounds
        else:
            return None

    # Creates A Copy of The Current Puzzle
    def copy(self, currentPuzzle):
        # Instatiates The Puzzle's Copy
        copyPuzzle = []

        # Iterates Over currentPuzzle Rows
        for row in currentPuzzle:
            # Instatiates currentPuzzle Row
            copyRowValues = []

            # Iterates over currentPuzzle Rows' Values
            for column in row:
                copyRowValues.append(column)
            copyPuzzle.append(copyRowValues)

        # Returns The Copy Puzzle
        return copyPuzzle

    # Find The Location of The Blank Space
    def find(self, currentPuzzle, blankSpace):
        # Iterates Over currentPuzzle Rows
        for row in range(0, len(self.a)):
            # Iterates over currentPuzzle Rows' Values
            for column in range(0, len(self.a)):
                # Checks If Location == Blank Space
                if currentPuzzle[row][column] == blankSpace:
                    # Returns Location of Blank Space
                    return row, column

# Handles The Puzzle Functionality
class Puzzle:
    def __init__(self, master):
        # Passing the GUI To The Puzzle Class (Possible Use)
        self.gui = master

        # Creates The Open & Closed Lists For Tracking Child States
        self.openList = []
        self.closedList = []


    # Find The F Value From H + G (Heuristic Value)
    def findF(self, start, goal):
        return self.findH(start.a, goal) + start.b

    # Finds The H Value (Heuristic Value)
    def findH(self, start, goal):
        # Instatiates hValue (Heuristic Value)
        hValue = 0

        # Iterates Over Rows
        for row in range(0, 3):
            # Iterates Over Rows's Values
            for column in range(0, 3):
                # Checks If Values != The Goal Placement
                if start[row][column] != goal[row][column] and start[row][column] != '_':
                    # If They Don't Equal Goal Placement, They Increase H Value
                    hValue += 1
        return hValue


    # Start Main Function
    def solvePuzzle(self):

        # Creates The First aStarNode
        theNode = aStarNode(randomPuzzle, 0, 0)

        # Goes Off To Find F Value (Heuristic Value)
        theNode.f = self.findF(theNode, goalPuzzle)

        # Puts Starting aStarNode In openList (Open List / Closed List Concept)
        self.openList.append(theNode)

        # Handles Initial GUI Functionality Changes
        puzzleChanges = 0
        self.gui.solveButton['state'] = 'disabled'

        # While Searching For Route From Current State To Goal State
        while True:
            # Keeps currentNode the Most Active aStarNode (State -> Child States)
            currentNode = self.openList[0]

            print(f"\nCurrent aStarNode #{puzzleChanges}:")
            for i in range(len(currentNode.a)):
                print(currentNode.a[i])

            # Checks If currentState EQUALS goalState
            if self.findH(currentNode.a, goalPuzzle) == 0:
                self.gui.solveLabel['text']   = f"Steps To Solve: {puzzleChanges}"
                self.gui.solveButton['state'] = 'active'

                print(f"Took {puzzleChanges} Changes To Reach The Goal Puzzle Node (State)")
                break

            for x in currentNode.findChildren():
                x.f = self.findF(x, goalPuzzle)
                self.openList.append(x)
            self.closedList.append(currentNode)

            del self.openList[0]

            # Sorts The Open List Using The Heuristic 'F Value'
            self.openList.sort(key = lambda x:x.f, reverse=False)

            # Handles GUI Changing Functionality
            puzzleChanges += 1
            self.gui.solveLabel['text']   = f"Steps To Solve: {puzzleChanges}"
            sleep(1) # <--- For Decoration Essentially (Should Be Removed For Functionality)



# This is the assignment #2 randomPuzzle & goalPuzzle State
randomPuzzle = [
    ['_', 1, 2],
    [8, 6, 3],
    [7, 5, 4]
]

goalPuzzle = [
    [1, 2, 3],
    [8, '_', 4],
    [7, 6, 5]
]



# Main Functionality
def main(masterGUI=None):
    print("Starting Random Puzzle:")
    for i in range(len(randomPuzzle)):
        print(randomPuzzle[i])


    print("Goal Puzzle Puzzle:")
    for i in range(len(goalPuzzle)):
        print(goalPuzzle[i])

    print("Starting To A* Search...")

    thePuzzle = Puzzle(masterGUI)
    thePuzzle.solvePuzzle()


# Calls MainGUI
masterGUI = MainGUI(randomPuzzle, goalPuzzle)

# Used When Not Using GUI
#main()
