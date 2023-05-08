from pygame import *
import ChessEngine
from random import randint
width = 640
height = 640
dimension = 8
squareSize = height // dimension
maxFps = 15
sources = {}
sounds = {}
boardImage = ""
def loadImages():
    global boardImage
    pieces = ["bB", "bK", "bN", "bp", "bQ", "bR", "wB", "wK", "wN", "wp", "wQ", "wR"]
    boardImage = transform.scale(image.load("sources/images/boards/walnut.png"), (width, height))
    for piece in pieces:
        sources[piece] = transform.scale(image.load("sources/images/pieces/" + piece + ".png"), (squareSize, squareSize))
def loadSounds():
    soundList = ["capture", "castle", "check", "move"]
    for sound in soundList:
        sounds[sound] = mixer.Sound("sources/sounds/" + sound + ".wav")
def main():
    init()
    screen = display.set_mode((width, height))
    display.set_caption("Chess")
    clock = time.Clock()
    screen.fill(Color("White"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    checkMate = gs.checkMate
    staleMate = gs.staleMate
    moveMade = False
    loadImages()
    loadSounds()
    id = str(randint(1, 1000000))
    log = open("gameLogs/gamelog_" + id + ".txt", "w")
    running = True
    squareSelected = ()
    playerClicks = []
    moveNumber = 1
    while running:
        for e in event.get():
            if (e.type == QUIT):
                running = False
            elif e.type == MOUSEBUTTONDOWN:
                location = mouse.get_pos()
                col = location[0]//squareSize
                row = location[1]//squareSize
                if (squareSelected == (row, col)) or (gs.board[row][col] == "  " and len(playerClicks) == 0):
                    squareSelected = ()
                    playerClicks = []
                else:
                    squareSelected = (row, col)
                    playerClicks.append(squareSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            inCheck, pins, checks = gs.checkForPinsAndChecks()
                            gs.getValidMoves()
                            checkMate = gs.checkMate
                            staleMate = gs.staleMate
                            with open("gameLogs/gamelog_" + id + ".txt", "a") as log:
                                log.write(move.getChessNotation(inCheck, checkMate, staleMate, gs.whiteToMove, moveNumber))
                                if gs.whiteToMove:
                                    moveNumber = moveNumber + 1
                            if inCheck:
                                mixer.Sound.play(sounds["check"])
                            else:
                                if move.pieceCaptured != "  ":
                                    mixer.Sound.play(sounds["capture"])
                                else:
                                    mixer.Sound.play(sounds["move"])
                            squareSelected =()
                            playerClicks = []
                    if not moveMade:
                            playerClicks = [squareSelected]
            elif e.type == KEYDOWN:
                if e.key == K_LEFT:
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        createGameState(screen, gs)
        clock.tick(maxFps)
        display.flip()

def createGameState(screen, gs):
    createBoard(screen)
    createPieces(screen, gs.board)

def createBoard(screen):
    screen.blit(boardImage, Rect(0, 0, 0, 0))

def createPieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != "  ":
                screen.blit(sources[piece], Rect(c*squareSize, r*squareSize, squareSize, squareSize))

if __name__ == "__main__":
    main()