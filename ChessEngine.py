import copy
class GameState():
    # initialize board state
    def __init__(self):
        # 2 dimensional array for reocrding state of board
        # first letter is b or w, representing if it is a white piece or not
        # second letter represents the piece
        # __ means empty square
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN","bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP","bP"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP","wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN","wR"]
        ]
        # initially its white's turn
        self.whiteTurn = True
        self.moveStack = []
        # record initial king locations
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

        self.isCheckMate = False
        self.isStaleMate = False

    # this function takes a move object and performs that move on the board
    def makeMove(self, move):
        # empty the previous square
        self.board[move.fromCoordinate[0]][move.fromCoordinate[1]] =  "__"
        # move the piece to new square
        self.board[move.toCoordinate[0]][move.toCoordinate[1]] = move.pieceToMove
        # record move in list so that it can be undo later on
        self.moveStack.append(move)
        # switch turn
        self.whiteTurn = not self.whiteTurn
        # update new coordinate for king location
        if move.pieceToMove == "bK":
            self.blackKingLocation = move.toCoordinate
        elif move.pieceToMove == "wK":
            self.whiteKingLocation = move.toCoordinate
        # if it was a pawn promotion move then make piece as queen.
        if move.isPawnPromotion:
            self.board[move.toCoordinate[0]][move.toCoordinate[1]] = move.pieceToMove[0] + "Q"

    # this function performs undo operation on a move
    def undoMove(self):
        # if a move exists which can be undo
        if self.moveStack:
            p = self.moveStack.pop()
            currentPiece = self.board[p.toCoordinate[0]][p.toCoordinate[1]]
            self.board[p.fromCoordinate[0]][p.fromCoordinate[1]] = currentPiece
            self.board[p.toCoordinate[0]][p.toCoordinate[1]] = p.pieceCaptured
            # switch turns back
            self.whiteTurn = not self.whiteTurn
            # update new king position coordinate
            if currentPiece == "bK":
                self.blackKingLocation = p.fromCoordinate
            elif currentPiece == "wK":
                self.whiteKingLocation = p.fromCoordinate
            # if move was a pawn promtion, then revert back
            if p.isPawnPromotion:
                self.board[p.fromCoordinate[0]][p.fromCoordinate[1]] = currentPiece[0] + "P"

    # this function returns all possible moves from a given square
    def getAllPossibleMoves(self):
        movesDict = dict()
        # loop over board
        for row in range(0, len(self.board)):
            for col in range(0, len(self.board)):
                if (self.board[row][col][0] == 'w' and self.whiteTurn) or (self.board[row][col][0] == 'b' and self.whiteTurn == False):
                    movesDict[(row, col)] = []
                    piece = self.board[row][col][1]
                    # piece is pawn /  shoinno, add pawn moves to the list
                    if piece == 'P':
                        self.getPawnMoves(movesDict, row, col)
                    # piece is Rook / Nouka, add rook moves to the list
                    elif piece == 'R':
                        self.getRookMoves(movesDict, row, col)
                    # piece is bishop / Hati, add bishop moves to the list
                    elif piece == 'B':
                        self.getBishopMoves(movesDict, row, col)
                    # Piece is Knight / Ghora, add knight moves to the list
                    elif piece == 'N':
                        self.getKnightMoves(movesDict, row, col)
                    # Piece is Queen / Rani, add queen moves to the list
                    elif piece == 'Q':
                        self.getQueenMoves(movesDict, row, col)
                    # Piece is King / Raja, add king moves to the list
                    elif piece == 'K':
                        self.getKingMoves(movesDict, row, col)
        return movesDict

    # get all possible squares a queen could move to from a given row and col
    def getQueenMoves(self, movesDict, row, col):
        #### Queen possible moves are just a combination of rook moves and bishop moves ###
        self.getBishopMoves(movesDict, row, col)
        self.getRookMoves(movesDict, row, col)

    # get all possible squares a King could move to from a given row and col
    def getKingMoves(self, movesDict, row, col):
        # potential 1 square paddings that can be done from a given square
        paddings = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        potentialMoves = []
        # create potential squares king could move to based on paddings
        for tup in paddings:
            potentialCoordinate = (row + tup[0], col + tup[1])
            if self.isValidTile(potentialCoordinate):
                potentialMoves.append(potentialCoordinate)
        # filter from the previous list if square is empty or has an enemy piece  that can be taken out
        enemyColor = 'b' if self.whiteTurn else 'w'
        for c in potentialMoves:
            if self.board[c[0]][c[1]] == "__":
                movesDict[(row, col)].append(Move((row, col), c, self.board))
            elif self.board[c[0]][c[1]][0] == enemyColor:
                movesDict[(row, col)].append(Move((row, col), c, self.board))
            else:
                pass

    # get all possible squares a knight could move to from a given row and col
    def getKnightMoves(self, movesDict, row, col):
        # 2 and a half movements that can be done
        paddings = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        potentialMoves = []
        # create potential squares knight could move to based on paddings
        for tup in paddings:
            potentialCoordinate = (row + tup[0], col + tup[1])
            if self.isValidTile(potentialCoordinate):
                potentialMoves.append(potentialCoordinate)

        enemyColor = 'b' if self.whiteTurn else 'w'
        # filter from the previous list if square is empty or has an enemy piece  that can be taken out
        for c in potentialMoves:
            if self.board[c[0]][c[1]] == "__":
                movesDict[(row, col)].append(Move((row, col), c, self.board))
            elif self.board[c[0]][c[1]][0] == enemyColor:
                movesDict[(row, col)].append(Move((row, col), c, self.board))
            else:
                pass

    # get all possible squares a bishop could move to fram a given row and col
    def getBishopMoves(self, movesDict, row, col):
        enemyColor = 'b' if self.whiteTurn else 'w'
        # top right until invalid tile or tile has opponent's pieces and can be taken out
        newRow = row - 1
        newCol = col + 1
        while self.isValidTile((newRow, newCol)):
            if self.board[newRow][newCol] == "__":
                movesDict[(row, col)].append(Move((row, col), (newRow, newCol), self.board))
            elif self.board[newRow][newCol][0] == enemyColor:
                movesDict[(row, col)].append(Move((row, col), (newRow, newCol), self.board))
                break
            else:
                break
            newRow -= 1
            newCol += 1
        # top left until invalid tile or tile has opponent's pieces and can be taken out
        newRow = row - 1
        newCol = col - 1
        while self.isValidTile((newRow, newCol)):
            if self.board[newRow][newCol] == "__":
                movesDict[(row, col)].append(Move((row, col), (newRow, newCol), self.board))
            elif self.board[newRow][newCol][0] == enemyColor:
                movesDict[(row, col)].append(Move((row, col), (newRow, newCol), self.board))
                break
            else:
                break
            newRow -= 1
            newCol -= 1

        # bottom right until invalid tile or tile has opponent's pieces and can be taken out
        newRow = row + 1
        newCol = col + 1
        while self.isValidTile((newRow, newCol)):
            if self.board[newRow][newCol] == "__":
                movesDict[(row, col)].append(Move((row, col), (newRow, newCol), self.board))
            elif self.board[newRow][newCol][0] == enemyColor:
                movesDict[(row, col)].append(Move((row, col), (newRow, newCol), self.board))
                break
            else:
                break
            newRow += 1
            newCol += 1

        # bottom left until invalid tile or tile has opponent's pieces and can be taken out
        newRow = row + 1
        newCol = col - 1
        while self.isValidTile((newRow, newCol)):
            if self.board[newRow][newCol] == "__":
                movesDict[(row, col)].append(Move((row, col), (newRow, newCol), self.board))
            elif self.board[newRow][newCol][0] == enemyColor:
                movesDict[( row, col)].append(Move((row, col), (newRow, newCol), self.board))
                break
            else:
                break
            newRow += 1
            newCol -= 1

    # get all possible squares a pawn could move to fram a given row and col
    def getRookMoves(self, movesDict, row, col):
        enemyColor = 'b' if self.whiteTurn else 'w'
        # go down until invalid tile or tile has opponent's pieces and can be taken out
        newRow = row + 1
        while self.isValidTile((newRow, col)):
            if self.board[newRow][col] == "__":
                movesDict[(row, col)].append(Move((row, col), (newRow, col), self.board))
            elif self.board[newRow][col][0] == enemyColor:
                movesDict[(row, col)].append(Move((row, col), (newRow, col), self.board))
                break
            else:
                break
            newRow +=1

        # go up until invalid tile or tile has opponent's pieces and can be taken out
        newRow = row - 1
        while self.isValidTile((newRow, col)):
            if self.board[newRow][col] == "__":
                movesDict[(row, col)].append(Move((row, col), (newRow, col), self.board))
            elif self.board[newRow][col][0] == enemyColor:
                movesDict[(row, col)].append(Move((row, col), (newRow, col), self.board))
                break
            else:
                break
            newRow -=1


        # go right until invalid tile or tile has opponent's pieces and can be taken out
        newCol = col + 1
        while self.isValidTile((row, newCol)):
            if self.board[row][newCol] == "__":
                movesDict[(row, col)].append(Move((row, col), (row, newCol), self.board))
            elif self.board[row][newCol][0] == enemyColor:
                movesDict[(row, col)].append(Move((row, col), (row, newCol), self.board))
                break
            else:
                break
            newCol +=1

        # go left until invalid tile or tile has opponent's pieces and can be taken out
        newCol = col - 1
        while self.isValidTile((row, newCol)):
            if self.board[row][newCol] == "__":
                movesDict[(row, col)].append(Move((row, col), (row, newCol), self.board))
            elif self.board[row][newCol][0] == enemyColor:
                movesDict[(row, col)].append(Move((row, col), (row, newCol), self.board))
                break
            else:
                break
            newCol -=1

        #print(movesDict.get((row, col), None))


    # get all possible squares a pawn could move to fram a given row and col
    def getPawnMoves(self, movesDict, row, col):
        # if its whites turn
        if self.whiteTurn:
            # get potential coordinate the pawn could move to
            potentialCoordinates = [x for x in [(row-1, col)] if self.isValidTile(x)]
            potentialFirstMoveCoordinates = [x for x in [(row-2, col)] if self.isValidTile(x)]
            potentialCaptureCoordinates = [x for x in [(row-1, col+1), (row-1, col-1)] if self.isValidTile(x)]
            # loop over potential coordinate
            for c in potentialCoordinates:
                # if coordinate is empty
                if self.board[c[0]][c[1]] == "__":
                    movesDict[(row, col)].append(Move((row, col), c, self.board))
                    for c in potentialFirstMoveCoordinates:
                        if self.board[c[0]][c[1]] == "__" and row == 6:
                            movesDict[(row, col)].append(Move((row, col), c, self.board))
            # if coordinate has opponent piece and can be captured
            for c in potentialCaptureCoordinates:
                if self.board[c[0]][c[1]][0] == "b":
                    movesDict[(row, col)].append(Move((row, col), c, self.board))
        else: # if its whites turn
            # get potential coordinate the pawn could move to
            potentialCoordinates = [x for x in [(row + 1, col)] if self.isValidTile(x)]
            potentialFirstMoveCoordinates = [x for x in [(row + 2, col)] if self.isValidTile(x)]
            potentialCaptureCoordinates = [x for x in [(row + 1, col + 1), (row + 1, col - 1)] if self.isValidTile(x)]
            # loop over potential coordinate
            for c in potentialCoordinates:
                # if coordinate is empty
                if self.board[c[0]][c[1]] == "__":
                    movesDict[(row, col)].append(Move((row, col), c, self.board))
                    for c in potentialFirstMoveCoordinates:
                        if self.board[c[0]][c[1]] == "__" and row == 1:
                            movesDict[(row, col)].append(Move((row, col), c, self.board))
            # if coordinate has opponent piece and can be captured
            for c in potentialCaptureCoordinates:
                if self.board[c[0]][c[1]][0] == "w":
                    movesDict[(row, col)].append(Move((row, col), c, self.board))

        #print(movesDict.get((row, col), None))

    # this fucntion returns all valid moves possible from a given point i the game
    def getValidMoves(self, shuffled=False):
        # get all possible moves
        allPossibleMoves = self.getAllPossibleMoves()
        realIsWhiteTurn = self.whiteTurn
        # loop over all possible moves
        for k, moves in allPossibleMoves.items():
            mmm = copy.deepcopy(moves)
            for i in range(0, len(mmm)):
                # make the move temporarily
                self.makeMove(mmm[i])
                # get opponent's possible moves
                opponentMoves = self.getAllPossibleMoves()
                # loop over opponent's possible moves
                for m, opponentMovesList in opponentMoves.items():
                    for j in range(0, len(opponentMovesList)):
                        # check if move threatens player's king
                        if realIsWhiteTurn:
                            if opponentMovesList[j].toCoordinate[0] ==  self.whiteKingLocation[0] and opponentMovesList[j].toCoordinate[1] == self.whiteKingLocation[1]:
                                # if it does threaten king, then remove move from valid move set
                                try:
                                    moves.remove(mmm[i])
                                except:
                                    pass
                                    #print(mmm[i])
                                #moves.pop(i)
                        else:
                            if opponentMovesList[j].toCoordinate[0] ==  self.blackKingLocation[0] and opponentMovesList[j].toCoordinate[1] == self.blackKingLocation[1]:
                                #moves.remove(moves[i])
                                # if it does threaten king, then remove move from valid move set
                                try:
                                    #moves.pop(i)
                                    moves.remove(mmm[i])
                                except:
                                    pass
                                    #print(mmm[i])
                # undo the original move which was temporarily made.
                self.undoMove()
        if shuffled == True:
            return {x for v in allPossibleMoves.values() for x in v}
        return allPossibleMoves

    # return if a player is in check right now
    def isInCheck(self):
        if self.whiteTurn:
            self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    # is the square under attack or not
    def squareUnderAttack(self, row, col):
        self.whiteTurn = not self.whiteTurn
        opponentMoves = self.getAllPossibleMoves()
        self.whiteTurn = not self.whiteTurn
        for k, moves in opponentMoves.items():
            for i in range(0, len(moves)):
                if moves[i].toCoordinate[0] == row and moves[i].toCoordinate[1] == col:
                    return True
        return False

    # is the square a valid piece on the board
    def isValidTile(self, coordinate):
        if coordinate[0] >=0 and coordinate[0] <= 7 and coordinate[1] >=0 and coordinate[1] <= 7:
            return True
        else:
            return False



# This class models each individual move in the game
class Move():
    def __init__(self, fromCoordinate, toCoordinate, board):
        # the coordinate from which piece was moved
        self.fromCoordinate =  fromCoordinate
        # the coordinate to which piece was moved
        self.toCoordinate = toCoordinate
        # which piece was moved
        self.pieceToMove = board[self.fromCoordinate[0]][self.fromCoordinate[1]]
        # which piece was captured
        self.pieceCaptured = board[self.toCoordinate[0]][self.toCoordinate[1]]
        # Is it a pawn promotion move
        self.isPawnPromotion = False
        if (self.pieceToMove == "wP" and self.toCoordinate[0] == 0) or (self.pieceToMove == "bP" and self.toCoordinate[0] == 7):
            self.isPawnPromotion = True
        # Hash function for the move
        self.moveHash = self.fromCoordinate[0] * 1000 + self.fromCoordinate[1] * 100 + self.toCoordinate[0] * 10 + self.toCoordinate[1]

    # for debug purposes - output move object as string
    def __str__(self):
        output = ""
        for name, var in vars(self).items():

            output += str(name) + " : " + str(var) + "; "
        return output

    # for hash purposes - so that move objects can be put in sets
    def __hash__(self):
        return self.moveHash

    __repr__ = __str__

    # check if 2 distinct move objects are the same or not
    def __eq__(self, other):
        if self.fromCoordinate == other.fromCoordinate and self.toCoordinate == other.toCoordinate and self.pieceToMove == other.pieceToMove and self.pieceCaptured == other.pieceCaptured and self.isPawnPromotion == other.isPawnPromotion:
            return True
        else:
            return False