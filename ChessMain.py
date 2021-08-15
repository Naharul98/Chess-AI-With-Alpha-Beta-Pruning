import pygame as p
from Chess import ChessEngine
from Chess import AI
from multiprocessing import Process
from multiprocessing import Queue
# board dimension
WIDTH = 512
HEIGHT = 512

#DIMENSION = 8
#SQUARE_SIZE = HEIGHT//DIMENSION
MAX_FPS = 30
average = []

IMAGES = dict()


# loads images onto the images dictionary
def loadImages():
    pieceCode = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]

    for piece_code in pieceCode:
        IMAGES[piece_code] = p.transform.scale(p.image.load("images/" + piece_code + ".png"), (HEIGHT//8, HEIGHT//8))

# run this function to start the game
def main():
    ### initialization ###
    p.init()
    p.display.set_caption("Chess by Shariar")
    loadImages()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill("white")
    gameState = ChessEngine.GameState()
    running = True

    # get all valid moves
    validMoves = gameState.getValidMoves()
    previousSelection = None

    # role parameters
    whiteIsAI = False
    blackIsAI = True
    # boolean variables
    AIThinking = False
    process = None
    undo = False
    while running:
        for e in p.event.get():
            # if user chooses to quit
            if e.type == p.QUIT:
                running = not running
            # handle mouse click events
            elif e.type == p.MOUSEBUTTONDOWN:
                # if human turn
                if isHumanTurn(whiteIsAI, blackIsAI, gameState) == True:
                    positionClicked = p.mouse.get_pos()
                    #row, column of where it was clicked
                    coordinateClicked = (positionClicked[1]//(HEIGHT//8),positionClicked[0]//(HEIGHT//8))
                    # already chose a piece for movement
                    if previousSelection != None:
                        # piece moved in same spot
                        if previousSelection == coordinateClicked:
                            previousSelection = None
                        else: # piece moved to a different location
                            move = ChessEngine.Move(previousSelection, coordinateClicked, gameState.board)
                            # if square to move is a valid one
                            if validMoves.get(previousSelection, None) != None:
                                for i in range(0, len(validMoves[previousSelection])):
                                    if move == validMoves[previousSelection][i]:
                                        # make the move
                                        gameState.makeMove(validMoves[previousSelection][i])
                                        # refresh valid moves
                                        validMoves = gameState.getValidMoves()
                                        undo = False
                                        break
                                '''
                                if move in validMoves[previousSelection]:
                                    gameState.makeMove(move)
                                    validMoves = gameState.getValidMoves()
                                '''
                            previousSelection = None
                    else:
                        if gameState.board[coordinateClicked[0]][coordinateClicked[1]] != "__":
                            previousSelection = coordinateClicked
            # handle keyboard events
            elif e.type == p.KEYDOWN:
                # undo event
                if e.key == p.K_z:
                    # undo move
                    gameState.undoMove()
                    # refresh valid moves
                    validMoves = gameState.getValidMoves()
                    # stop AI thought process as move is being undo
                    if AIThinking:
                        process.terminate()
                        AIThinking = False
                    undo = True
                # board reset event
                if e.key == p.K_r:
                    # reset all variables to initial value
                    gameState = ChessEngine.GameState()
                    validMoves = gameState.getValidMoves()
                    previousSelection = None
                    if AIThinking:
                        process.terminate()
                        AIThinking = False
                    process = None
                    undo = False


        # if AI turn
        if isGameOver(validMoves) == False and isHumanTurn(whiteIsAI, blackIsAI, gameState) == False and undo == False:
            # start ai thought process
            if AIThinking == False:
                AIThinking = True
                print("Thinking")
                q = Queue()
                # start a new process for finding out the best move according to chosen algo
                process = Process(target=AI.findBestMiniMaxMove, args=(validMoves, gameState, q))
                process.start()
            # if process has finished
            if process.is_alive() == False:
                print("done")
                #minimaxMove = AI.findBestMiniMaxMove(validMoves, gameState)
                # get the resulting move output by the algoritm
                minimaxMove = q.get()
                # not been able to find the best move for some reason
                if minimaxMove[0] is None:
                    print("picking random move")
                    randomMove = AI.findRandomMove(validMoves, gameState)
                    gameState.makeMove(randomMove)
                else:
                    # make the move
                    gameState.makeMove(minimaxMove[0])
                    average.append(minimaxMove[1])
                # print average number of states explored for experimental purposes
                print("average = ")
                print(sum(average)/len(average))
                validMoves = gameState.getValidMoves()
                previousSelection = None
                AIThinking = False

        # draw board
        drawBoard(screen, gameState, previousSelection, validMoves)
        # if game over, show game over text
        if isGameOver(validMoves) == True:
            if gameState.whiteTurn:
                showWinningText("Black Wins! Press R to reset the game", screen)
            else:
                showWinningText("White Wins! Press R to reset the game", screen)
        clock.tick(MAX_FPS)
        p.display.flip()

# this function checks if it is currently human turn
def isHumanTurn(whiteIsAI, blackIsAI, gameState):
    if (whiteIsAI == False and gameState.whiteTurn == True) or (blackIsAI == False and gameState.whiteTurn == False):
        return True
    else:
        return False

# this function checks if it is currently game over
def isGameOver(validMoves):
    for k, v in validMoves.items():
        if len(v) > 0:
            return False
    return True

# this function displays text when a player has won
def showWinningText(text, screen):
    font = p.font.SysFont("Calibri", 32, True, True)
    txt = font.render(text, 0, p.Color("Black"))
    txtLocation  = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - txt.get_width()/2, HEIGHT/2 - txt.get_height()/2)
    screen.blit(txt, txtLocation)



## this function draws squares on the board
def drawBoard(screen, gameState, selection, validMoves):
    # draw tiles
    isWhite = True
    for row in range(0, 8):
        isWhite = not isWhite
        for col in range(0, 8):
            rectangle = p.Rect(col * (HEIGHT // 8), row * (HEIGHT // 8), (HEIGHT // 8), (HEIGHT // 8))
            if isWhite:
                p.draw.rect(screen, p.Color("grey"), rectangle)
            else:
                p.draw.rect(screen, p.Color("white"), rectangle)
            isWhite = not isWhite
    # draw potential moves
    if selection:
        if (gameState.whiteTurn and gameState.board[selection[0]][selection[1]][0] == 'w') or (gameState.whiteTurn == False and gameState.board[selection[0]][selection[1]][0] == 'b'):
            drawPotentialMoves(screen, selection, validMoves)
    # draw pieces in current game state
    drawPieces(screen, gameState.board)



# This function highlights squares of possible moves when a user clicks a pirce
def drawPotentialMoves(screen, selection, validMoves):
    # draw selected cell
    selectedRow = selection[0]
    selectedcol = selection[1]
    rectangle = p.Rect(selectedcol * (HEIGHT // 8), selectedRow * (HEIGHT // 8), (HEIGHT // 8), (HEIGHT // 8))

    p.draw.rect(screen, p.Color("light blue"), rectangle)

    # draw blue outline in squares which are of possible moves for the piece.
    for move in validMoves.get(selection, []):
        row = move.toCoordinate[0]
        col = move.toCoordinate[1]
        rectangle = p.Rect(col * (HEIGHT // 8), row * (HEIGHT // 8), (HEIGHT // 8), (HEIGHT // 8))
        p.draw.rect(screen, p.Color("lightslateblue"), rectangle, 5)



## draw pieces on the board
def drawPieces(screen, board):
    for row in range(0, 8):
        for col in range(0, 8):
            if board[row][col] != "__":
                rectangle = p.Rect(col * (HEIGHT // 8), row * (HEIGHT // 8), (HEIGHT // 8), (HEIGHT // 8))
                screen.blit(IMAGES.get(board[row][col]), rectangle)




if __name__ == "__main__":
    main()