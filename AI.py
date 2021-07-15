import random
from Chess import ChessMain
from itertools import chain
from Chess import ChessEngine
from Chess import AI
scoreDict = dict()
scoreDict["K"] = 0
scoreDict["Q"] = 10
scoreDict["R"] = 5
scoreDict["B"] = 3
scoreDict["N"] = 3
scoreDict["P"] = 1
#center is good
knightPositionRewards = [
            [1, 1, 1, 1, 1, 1, 1,1],
            [1, 2, 2, 2, 2, 2, 2,1],
            [1, 2, 3, 3, 3, 3, 2,1],
            [1, 2, 3, 4, 4, 3, 2,1],
            [1, 2, 3, 4, 4, 3, 2,1],
            [1, 2, 3, 3, 3, 3, 2,1],
            [1, 2, 2, 2, 2, 2, 2,1],
            [1, 1, 1, 1, 1, 1, 1,1],
        ]
# diagonal is good
bishopPositionRewards = [
            [4, 3, 2, 1, 1, 2, 3,4],
            [3, 4, 5, 2, 2, 3, 4,3],
            [2, 3, 4, 3, 3, 4, 3,2],
            [1, 2, 3, 4, 4, 3, 2,1],
            [1, 2, 3, 4, 4, 3, 2,1],
            [2, 3, 4, 3, 3, 4, 3,1],
            [3, 4, 3, 2, 2, 3, 4,3],
            [4, 3, 2, 1, 1, 2, 3,4],
        ]
# 5,1 is 4 because its a god position to infiltrate and capture rook on the other sie
# will try to centralize the queen
queenPositionRewards = [
            [1, 1, 1, 3, 1, 1, 1,1],
            [1, 2, 3, 3, 3, 1, 1,1],
            [1, 4, 3, 3, 3, 4, 2,1],
            [1, 2, 3, 3, 3, 2, 2,1],
            [1, 2, 3, 3, 3, 2, 2,1],
            [1, 4, 3, 3, 3, 4, 2,1],
            [1, 1, 2, 3, 3, 1, 1,1],
            [1, 1, 1, 3, 1, 1, 1,1],
        ]

# 2nd row is good because if you reach there, can put a lot of pressure on pawns
# centralizing rook in back row is generally good
# keep off the edges
rookPositionRewards = [
            [4, 3, 4, 4, 4, 4, 3,4],
            [4, 4, 4, 4, 4, 4, 4,4],
            [1, 1, 2, 3, 3, 2, 1,1],
            [1, 2, 3, 4, 4, 3, 2,1],
            [1, 2, 3, 4, 4, 3, 2,1],
            [1, 1, 2, 2, 2, 2, 1,1],
            [4, 4, 4, 4, 4, 4, 4,4],
            [4, 3, 4, 4, 4, 4, 3,4],
        ]
# pawn in opponents territory desirable as chance for pawn promotion
# centralized pawn is good.
# pawn in row 6 middle is 0 because it is desirable for pawn to advance and dominate the middle of the board
whitePawnRewards = [
            [8, 8, 8, 8, 8, 8, 8,8],
            [8, 8, 8, 8, 8, 8, 8,8],
            [5, 6, 6, 7, 7, 6, 6,5],
            [2, 3, 3, 5, 5, 3, 3,2],
            [1, 2, 3, 4, 4, 3, 2,1],
            [1, 1, 2, 3, 3, 2, 1,1],
            [1, 1, 1, 0, 0, 1, 1,1],
            [0, 0, 0, 0, 0, 0, 0,0],
        ]

blackPawnRewards = list(reversed(whitePawnRewards))

checkmateScore = 1000
max_depth = 2

def findRandomMove(validMoves, gameState):
    m = []
    for k, v in validMoves.items():
        if len(v) > 0:
            m = m + v
    #print(m)
    return m[random.randint(0, len(m) - 1)]

def findBestMiniMaxMove(validMoves, gameState, q):
    global nxtMove
    global count
    count = 0
    nxtMove = None
    v = {x for v in validMoves.values() for x in v}
    #print(v)
    #findMiniMaxMove(validMoves, gameState, max_depth, gameState.whiteTurn)
    findNegaMaxMove(v, gameState, max_depth, 1 if gameState.whiteTurn else -1)
    print(count)
    q.put(nxtMove)
    #return nxtMove


def findMiniMaxMove(validMoves, gameState, depth, whiteTurn):
    global nxtMove
    if depth == 0:
        return calculateBoardScore(gameState, validMoves)
    # to maximize
    if whiteTurn:
        maxSoFar = float('-inf')
        for k, v in validMoves.items():
            for move in v:
                gameState.makeMove(move)
                nextMoves = gameState.getValidMoves()
                s = findMiniMaxMove(nextMoves, gameState, depth-1, not whiteTurn)

                if s > maxSoFar:
                    maxSoFar = max(maxSoFar, s)
                    if depth == max_depth:
                        nxtMove = move

                gameState.undoMove()
        return maxSoFar

    else: # to minimize
        minSoFar = float('inf')
        for k, v in validMoves.items():
            for move in v:
                gameState.makeMove(move)
                nextMoves = gameState.getValidMoves()
                s = findMiniMaxMove(nextMoves, gameState, depth - 1, not whiteTurn)
                if s < minSoFar:
                    minSoFar = min(s, minSoFar)
                    if depth == max_depth:
                        nxtMove = move
                gameState.undoMove()
        return minSoFar
'''
# 1 if whites turn, -1 if black
def findNegaMaxMove(validMoves, gameState, depth, turn, alpha=False, beta=False):
    global nxtMove
    if depth == 0:
        return turn * calculateBoardScore(gameState, validMoves)

    #maxScore = -checkmateScore
    maxScore = float('-inf')
    #for k, v in validMoves.items():
    for move in validMoves:
        gameState.makeMove(move)
        nextMoves = gameState.getValidMoves(shuffled=True)
        s = -findNegaMaxMove(nextMoves, gameState, depth - 1, -turn)
        if s > maxScore:
            maxScore = s
            if max_depth == depth:
                nxtMove = move
        gameState.undoMove()
    return maxScore
'''
# 1 if whites turn, -1 if black
# alpha = current max, beta = min...in recursive call, alpha becomes opponents new min -> hence the -alpha. Beta becomes opponents max
def findNegaMaxMove(validMoves, gameState, depth, turn, alpha=float("-inf"), beta=float("inf")):
    global nxtMove
    global count
    count = count + 1
    if depth == 0:
        return turn * calculateBoardScore(gameState, validMoves)

    #move ordering
    maxScore = float('-inf')
    for move in validMoves:
        gameState.makeMove(move)
        nextMoves = gameState.getValidMoves(shuffled=True)
        s = -findNegaMaxMove(nextMoves, gameState, depth - 1, -turn, -beta, -alpha)
        if s > maxScore:
            maxScore = s
            if max_depth == depth:
                nxtMove = move
                debug = ""
                debug += str(move.toCoordinate) + " " + move.pieceToMove
                print(debug)
        gameState.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

def calculateBoardScore(gameState, validMoves):
    if len(validMoves) == 0:
        if gameState.whiteTurn == True:
            return -checkmateScore
        else:
            return checkmateScore
    score = 0
    for row in range(0, len(gameState.board)):
        for col in range(0, len(gameState.board)):
            if gameState.board[row][col] != "__":
                positionScore = 0
                if gameState.board[row][col][1] != "K":
                    if gameState.board[row][col] == "wP":
                        positionScore = whitePawnRewards[row][col]
                    elif gameState.board[row][col] == "bP":
                        positionScore = blackPawnRewards[row][col]
                    elif gameState.board[row][col][1] == "R":
                        positionScore = rookPositionRewards[row][col]
                    elif gameState.board[row][col][1] == "B":
                        positionScore = bishopPositionRewards[row][col]
                    elif gameState.board[row][col][1] == "Q":
                        positionScore = queenPositionRewards[row][col]
                    elif gameState.board[row][col][1] == "N":
                        positionScore = knightPositionRewards[row][col]
                    else:
                        positionScore = 0
                if gameState.board[row][col][0] == "w":
                    score = score + (scoreDict[gameState.board[row][col][1]] + (positionScore * 0.01))
                elif gameState.board[row][col][0] == "b":
                    score = score - (scoreDict[gameState.board[row][col][1]] + (positionScore * 0.01))
    return score

'''
def calculateBoardScore(gameState):
    score = 0
    for row in range(0, len(gameState.board)):
        for col in range(0, len(gameState.board)):
            if gameState.board[row][col][0] == "w":
                score = score + scoreDict[gameState.board[row][col][1]]
            elif gameState.board[row][col][0] == "b":
                score = score - scoreDict[gameState.board[row][col][1]]
    return score
'''