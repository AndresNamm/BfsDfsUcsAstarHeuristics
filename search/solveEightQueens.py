import random
import copy
from optparse import OptionParser
from datetime import *
import random

import util

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]

        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board
        i = 0
        cnt=0
        while cnt<=110:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            i += 1
            if currentNumberOfAttacks < newNumberOfAttacks:
                break
            elif currentNumberOfAttacks == newNumberOfAttacks:
                if currentNumberOfAttacks == 0:
                    break
                else:
                    cnt+=1
            else:
                cnt=-40
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray
        self.attacks = [0 for i in range(8)]
        self.currentNrOfAttacks = 0
    @staticmethod

    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray
          
    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s 

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999. 
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks, 
        the Column and Row of the new queen  
        For exmaple: 
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        mainBoard = copy.deepcopy(self.squareArray)
        n = 8


        nrow,ncol=[-1,-1]
        equal=[]
        min=self.getNumberOfAttacks()
        for column in range(n):
            self.squareArray=[[]]
            self.squareArray = copy.deepcopy(mainBoard)
            # Empties all the values in column
            for i in range(n):
                self.squareArray[i][column] = 0
            # Tests out attackNumber with all the different movements
            for row in range(n):
                self.squareArray[row][column]=1
                val = self.getNumberOfAttacks()
                self.squareArray[row][column]=0
                if val < min:
                    nrow=row
                    ncol=column
                    min=val
                if val == min:
                    equal.append([row,column])

        if nrow == -1:
            if len(equal)!=0:
                random.seed(datetime.now())
                index = random.randint(1,len(equal)-1)
                #index=len(equal)%2
                nrow=equal[index][0]
                ncol=equal[index][1]

        newBoard=mainBoard.copy()
        if nrow !=-1:
            for i in range(n):
                newBoard[i][ncol]=0
            newBoard[nrow][ncol]=1
        nBoard = Board(newBoard)
        return (nBoard,min,nrow,ncol)


    def getPositions(self):
        positions = []
        n=8
        # Get Positions
        for column in range(n):
            for row in range(n):
                if self.squareArray[row][column] == 1:
                    positions.append(row)
                    break



        return(positions)


    def getNumberOfAttacks(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """

        positions = self.getPositions()
        # Get number of attacks per queen
        sum = 0
        for i in range(len(positions)):
            self.attacks[i]=self.chekDir((positions[i],i))
            sum += self.attacks[i]
        self.currentNrOfAttacks=sum
        return sum

    def checkLimits(self, row, col):
        max=7
        min=0
        if row> max or col >max or col < min or row<min:
            return False
        return True

    def chekDir(self,pos):
        row,col=pos
        directions = [(1,1),(-1,1),(0,1)]
        attack = 0

        for i in directions:
            drow,dcol=i
            nrow = drow + row
            ncol = dcol + col
            while self.checkLimits(nrow,ncol):
                if self.squareArray[nrow][ncol]==1:
                    attack+=1
                nrow+=drow
                ncol+=dcol
        return attack



if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
