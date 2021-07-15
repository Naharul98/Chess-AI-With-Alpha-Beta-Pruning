import copy
class GameState():
    def __init__(self):
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

        self.whiteTurn = True
        self.moveStack = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

        # TODO
        self.isCheckMate = False
        self.isStaleMate = False

    def makeMove(self, move):
        self.board[move.fromCoordinate[0]][move.fromCoordinate[1]] =  "__"
        self.board[move.toCoordinate[0]][move.toCoordinate[1]] = move.pieceToMove
        self.moveStack.append(move)
        self.whiteTurn = not self.whiteTurn

        if move.pieceToMove == "bK":
            self.blackKingLocation = move.toCoordinate
        elif move.pieceToMove == "wK":
            self.whiteKingLocation = move.toCoordinate

        if move.isPawnPromotion:
            self.board[move.toCoordinate[0]][move.toCoordinate[1]] = move.pieceToMove[0] + "Q"

    def undoMove(self):
        if self.moveStack:
            p = self.moveStack.pop()
            currentPiece = self.board[p.toCoordinate[0]][p.toCoordinate[1]]
            self.board[p.fromCoordinate[0]][p.fromCoordinate[1]] = currentPiece
            self.board[p.toCoordinate[0]][p.toCoordinate[1]] = p.pieceCaptured
            self.whiteTurn = not self.whiteTurn

            if currentPiece == "bK":
                self.blackKingLocation = p.fromCoordinate
            elif currentPiece == "wK":
                self.whiteKingLocation = p.fromCoordinate

            if p.isPawnPromotion:
                self.board[p.fromCoordinate[0]][p.fromCoordinate[1]] = currentPiece[0] + "P"

    def getAllPossibleMoves(self):
        movesDict = dict()
        for row in range(0, len(self.board)):
            for col in range(0, len(self.board)):
                if (self.board[row][col][0] == 'w' and self.whiteTurn) or (self.board[row][col][0] == 'b' and self.whiteTurn == False):
                    movesDict[(row, col)] = []
                    piece = self.board[row][col][1]
                    # piece is pawn /  shoinno
                    if piece == 'P':
                        self.getPawnMoves(movesDict, row, col)
                    # piece is Rook / Nouka
                    elif piece == 'R':
                        self.getRookMoves(movesDict, row, col)
                    # piece is bishop / Hati
                    elif piece == 'B':
                        self.getBishopMoves(movesDict, row, col)
                    # Piece is Knight / Ghora
                    elif piece == 'N':
                        self.getKnightMoves(movesDict, row, col)
                    # Piece is Queen / Rani
                    elif piece == 'Q':
                        self.getQueenMoves(movesDict, row, col)
                    # Piece is King / Raja
                    elif piece == 'K':
                        self.getKingMoves(movesDict, row, col)
        return movesDict

    def getQueenMoves(self, movesDict, row, col):
        self.getBishopMoves(movesDict, row, col)
        self.getRookMoves(movesDict, row, col)

    def getKingMoves(self, movesDict, row, col):
        paddings = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        potentialMoves = []
        for tup in paddings:
            potentialCoordinate = (row + tup[0], col + tup[1])
            if self.isValidTile(potentialCoordinate):
                potentialMoves.append(potentialCoordinate)

        enemyColor = 'b' if self.whiteTurn else 'w'
        for c in potentialMoves:
            if self.board[c[0]][c[1]] == "__":
                movesDict[(row, col)].append(Move((row, col), c, self.board))
            elif self.board[c[0]][c[1]][0] == enemyColor:
                movesDict[(row, col)].append(Move((row, col), c, self.board))
            else:
                pass

    def getKnightMoves(self, movesDict, row, col):
        paddings = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        potentialMoves = []
        for tup in paddings:
            potentialCoordinate = (row + tup[0], col + tup[1])
            if self.isValidTile(potentialCoordinate):
                potentialMoves.append(potentialCoordinate)

        enemyColor = 'b' if self.whiteTurn else 'w'
        for c in potentialMoves:
            if self.board[c[0]][c[1]] == "__":
                movesDict[(row, col)].append(Move((row, col), c, self.board))
            elif self.board[c[0]][c[1]][0] == enemyColor:
                movesDict[(row, col)].append(Move((row, col), c, self.board))
            else:
                pass



    def getBishopMoves(self, movesDict, row, col):
        enemyColor = 'b' if self.whiteTurn else 'w'
        # top right
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
        # top left
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

        # bottom right
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

        # bottom left
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

    def getRookMoves(self, movesDict, row, col):
        enemyColor = 'b' if self.whiteTurn else 'w'
        # go down
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

        # go up
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


        # go right
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

        # go left
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



    def getPawnMoves(self, movesDict, row, col):
        if self.whiteTurn:
            potentialCoordinates = [x for x in [(row-1, col)] if self.isValidTile(x)]
            potentialFirstMoveCoordinates = [x for x in [(row-2, col)] if self.isValidTile(x)]
            potentialCaptureCoordinates = [x for x in [(row-1, col+1), (row-1, col-1)] if self.isValidTile(x)]

            for c in potentialCoordinates:
                if self.board[c[0]][c[1]] == "__":
                    movesDict[(row, col)].append(Move((row, col), c, self.board))
                    for c in potentialFirstMoveCoordinates:
                        if self.board[c[0]][c[1]] == "__" and row == 6:
                            movesDict[(row, col)].append(Move((row, col), c, self.board))

            for c in potentialCaptureCoordinates:
                if self.board[c[0]][c[1]][0] == "b":
                    movesDict[(row, col)].append(Move((row, col), c, self.board))
        else:
            potentialCoordinates = [x for x in [(row + 1, col)] if self.isValidTile(x)]
            potentialFirstMoveCoordinates = [x for x in [(row + 2, col)] if self.isValidTile(x)]
            potentialCaptureCoordinates = [x for x in [(row + 1, col + 1), (row + 1, col - 1)] if self.isValidTile(x)]
            for c in potentialCoordinates:
                if self.board[c[0]][c[1]] == "__":
                    movesDict[(row, col)].append(Move((row, col), c, self.board))
                    for c in potentialFirstMoveCoordinates:
                        if self.board[c[0]][c[1]] == "__" and row == 1:
                            movesDict[(row, col)].append(Move((row, col), c, self.board))

            for c in potentialCaptureCoordinates:
                if self.board[c[0]][c[1]][0] == "w":
                    movesDict[(row, col)].append(Move((row, col), c, self.board))

        #print(movesDict.get((row, col), None))


    def getValidMoves(self, shuffled=False):
        # get all possible moves
        allPossibleMoves = self.getAllPossibleMoves()
        realIsWhiteTurn = self.whiteTurn

        for k, moves in allPossibleMoves.items():
            mmm = copy.deepcopy(moves)
            for i in range(0, len(mmm)):
                self.makeMove(mmm[i])
                opponentMoves = self.getAllPossibleMoves()
                for m, opponentMovesList in opponentMoves.items():
                    for j in range(0, len(opponentMovesList)):
                        if realIsWhiteTurn:
                            if opponentMovesList[j].toCoordinate[0] ==  self.whiteKingLocation[0] and opponentMovesList[j].toCoordinate[1] == self.whiteKingLocation[1]:
                                try:
                                    moves.remove(mmm[i])
                                except:
                                    pass
                                    #print(mmm[i])
                                #moves.pop(i)
                        else:
                            if opponentMovesList[j].toCoordinate[0] ==  self.blackKingLocation[0] and opponentMovesList[j].toCoordinate[1] == self.blackKingLocation[1]:
                                #moves.remove(moves[i])
                                try:
                                    #moves.pop(i)
                                    moves.remove(mmm[i])
                                except:
                                    pass
                                    #print(mmm[i])

                self.undoMove()
        if shuffled == True:
            return {x for v in allPossibleMoves.values() for x in v}
        return allPossibleMoves

    def isInCheck(self):
        if self.whiteTurn:
            self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, row, col):
        self.whiteTurn = not self.whiteTurn
        opponentMoves = self.getAllPossibleMoves()
        self.whiteTurn = not self.whiteTurn
        for k, moves in opponentMoves.items():
            for i in range(0, len(moves)):
                if moves[i].toCoordinate[0] == row and moves[i].toCoordinate[1] == col:
                    return True
        return False


    def isValidTile(self, coordinate):
        if coordinate[0] >=0 and coordinate[0] <= 7 and coordinate[1] >=0 and coordinate[1] <= 7:
            return True
        else:
            return False




class Move():
    def __init__(self, fromCoordinate, toCoordinate, board):
        self.fromCoordinate =  fromCoordinate
        self.toCoordinate = toCoordinate
        self.pieceToMove = board[self.fromCoordinate[0]][self.fromCoordinate[1]]
        self.pieceCaptured = board[self.toCoordinate[0]][self.toCoordinate[1]]
        self.isPawnPromotion = False
        if (self.pieceToMove == "wP" and self.toCoordinate[0] == 0) or (self.pieceToMove == "bP" and self.toCoordinate[0] == 7):
            self.isPawnPromotion = True

        self.moveHash = self.fromCoordinate[0] * 1000 + self.fromCoordinate[1] * 100 + self.toCoordinate[0] * 10 + self.toCoordinate[1]

    def __str__(self):
        output = ""
        for name, var in vars(self).items():

            output += str(name) + " : " + str(var) + "; "
        return output

    def __hash__(self):
        return self.moveHash

    __repr__ = __str__

    def __eq__(self, other):
        if self.fromCoordinate == other.fromCoordinate and self.toCoordinate == other.toCoordinate and self.pieceToMove == other.pieceToMove and self.pieceCaptured == other.pieceCaptured and self.isPawnPromotion == other.isPawnPromotion:
            return True
        else:
            return False