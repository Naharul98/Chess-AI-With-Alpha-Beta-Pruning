import pygame as p
from Chess import ChessEngine
from Chess import AI
from multiprocessing import Process
from multiprocessing import Queue
WIDTH = 512
HEIGHT = 512

#DIMENSION = 8
#SQUARE_SIZE = HEIGHT//DIMENSION
MAX_FPS = 30


IMAGES = dict()
# currently selected chess piece


def loadImages():
    pieceCode = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]

    for piece_code in pieceCode:
        IMAGES[piece_code] = p.transform.scale(p.image.load("images/" + piece_code + ".png"), (HEIGHT//8, HEIGHT//8))


def main():
    ### initialization ###
    p.init()
    p.display.set_caption("Chess by Nahid")
    loadImages()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill("white")
    gameState = ChessEngine.GameState()
    running = True
    ### initialization ###

    validMoves = gameState.getValidMoves()
    previousSelection = None

    whiteIsAI = False
    blackIsAI = True

    AIThinking = False
    process = None
    undo = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = not running
            elif e.type == p.MOUSEBUTTONDOWN:
                if isHumanTurn(whiteIsAI, blackIsAI, gameState) == True:
                    positionClicked = p.mouse.get_pos()
                    #row, column
                    coordinateClicked = (positionClicked[1]//(HEIGHT//8),positionClicked[0]//(HEIGHT//8))
                    if previousSelection != None:
                        if previousSelection == coordinateClicked:
                            previousSelection = None
                        else:
                            move = ChessEngine.Move(previousSelection, coordinateClicked, gameState.board)
                            if validMoves.get(previousSelection, None) != None:
                                for i in range(0, len(validMoves[previousSelection])):
                                    if move == validMoves[previousSelection][i]:
                                        gameState.makeMove(validMoves[previousSelection][i])
                                        validMoves = gameState.getValidMoves()
                                        undo = False
                                        break
                                '''
                                if move in validMoves[previousSelection]:
                                    gameState.makeMove(move)
                                    validMoves = gameState.getValidMoves()
                                '''
                            previousSelection = None
                            #drawBoard(screen, gameState, previousSelection, validMoves)
                            #clock.tick(MAX_FPS)
                            #p.display.flip()
                    else:
                        if gameState.board[coordinateClicked[0]][coordinateClicked[1]] != "__":
                            previousSelection = coordinateClicked
            # Undo
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gameState.undoMove()
                    validMoves = gameState.getValidMoves()
                    if AIThinking:
                        process.terminate()
                        AIThinking = False
                    undo = True
                if e.key == p.K_r:
                    gameState = ChessEngine.GameState()
                    validMoves = gameState.getValidMoves()
                    previousSelection = None
                    if AIThinking:
                        process.terminate()
                        AIThinking = False
                    process = None
                    undo = False



        if isGameOver(validMoves) == False and isHumanTurn(whiteIsAI, blackIsAI, gameState) == False and undo == False:
            if AIThinking == False:
                AIThinking = True
                print("Thinking")
                q = Queue()
                process = Process(target=AI.findBestMiniMaxMove, args=(validMoves, gameState, q))
                process.start()
            if process.is_alive() == False:
                print("done")
                #minimaxMove = AI.findBestMiniMaxMove(validMoves, gameState)
                minimaxMove = q.get()
                if minimaxMove is None:
                    print("picking random move")
                    randomMove = AI.findRandomMove(validMoves, gameState)
                    gameState.makeMove(randomMove)
                else:
                    gameState.makeMove(minimaxMove)
                validMoves = gameState.getValidMoves()
                previousSelection = None
                AIThinking = False


        drawBoard(screen, gameState, previousSelection, validMoves)
        if isGameOver(validMoves) == True:
            if gameState.whiteTurn:
                showWinningText("Black Wins! Press R to reset the game", screen)
            else:
                showWinningText("White Wins! Press R to reset the game", screen)
        clock.tick(MAX_FPS)
        p.display.flip()

def isHumanTurn(whiteIsAI, blackIsAI, gameState):
    if (whiteIsAI == False and gameState.whiteTurn == True) or (blackIsAI == False and gameState.whiteTurn == False):
        return True
    else:
        return False


def isGameOver(validMoves):
    for k, v in validMoves.items():
        if len(v) > 0:
            return False
    return True

def showWinningText(text, screen):
    font = p.font.SysFont("Calibri", 32, True, True)
    txt = font.render(text, 0, p.Color("Black"))
    txtLocation  = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - txt.get_width()/2, HEIGHT/2 - txt.get_height()/2)
    screen.blit(txt, txtLocation)



## draw squares
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




def drawPotentialMoves(screen, selection, validMoves):
    # draw selected cell
    selectedRow = selection[0]
    selectedcol = selection[1]
    rectangle = p.Rect(selectedcol * (HEIGHT // 8), selectedRow * (HEIGHT // 8), (HEIGHT // 8), (HEIGHT // 8))
    p.draw.rect(screen, p.Color("light blue"), rectangle)

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