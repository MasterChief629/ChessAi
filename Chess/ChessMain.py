"""
Handles user input
display gamestate
"""

#Import the nessicary files and libraries
import pygame as p
import ChessEngine
import ChessAi

#define the board display parameters
WIDTH = HEIGHT = 800
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

#load the pieces from the images folder
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("ChessAi/Chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    State = ChessEngine.GameState()

    #get the initial moves selected
    validMoves = State.getValidMoves()
    moveMade = False

    #decide who is a player and who is an AI
    playerOne = False #Represents a human playing white if true, or an Ai playing white if false
    playerTwo = False #same as prior but for black

    #actually load the images
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    while running:
        humanTurn = (State.whiteToMove and playerOne) or (not State.whiteToMove and playerTwo)
        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            #allow a person to click pieces to move them
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE

                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []

                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)

                    #if two valid squares are clicked then make the move
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], State.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                State.makeMove(validMoves[i])
                                moveMade = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]

            #keypress ultilization
            elif e.type == p.KEYDOWN:
                #undo a move
                if e.key == p.K_z:
                    State.undoMove()
                    moveMade = True
                #reset the board
                if e.key == p.K_r:
                    State = ChessEngine.GameState()
                    validMoves = State.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    gameOver = False

        #AI implementation
        if not gameOver and not humanTurn:
            AIMove = ChessAi.findBestMinMax(State, validMoves)
            if AIMove == None:
                AIMove = ChessAi.findRandomMove(validMoves)
            State.makeMove(AIMove)
            moveMade = True
        #change the player
        if moveMade:
            validMoves = State.getValidMoves()
            moveMade = False
        drawGameState(screen, State, validMoves, sqSelected)

        #have the end game texts
        if State.checkmate:
            gameOver = True
            if State.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif State.stalemate:
            gameOver = True
            drawText(screen, 'Stalemate')

        clock.tick(MAX_FPS)
        p.display.flip()



"""graphics of game state"""
def drawGameState(screen, State, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, State, validMoves, sqSelected)
    drawPieces(screen, State.board)

#highlights the square of the last move's end location as well as the possible locations that a piece could be moved
def highlightSquares(screen, State, validMoves, sqSelected):

    #highlights the end location of the last move
    if len(State.moveLog) > 0:
        lastMove = State.moveLog[-1]
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(120)
        s.fill(p.Color('green'))
        screen.blit(s, (lastMove.startCol * SQ_SIZE, lastMove.startRow * SQ_SIZE))
        screen.blit(s, (lastMove.endCol * SQ_SIZE, lastMove.endRow * SQ_SIZE))

    #highlights the possible move locations
    if sqSelected != ():
        r, c = sqSelected
        if State.board[r][c][0] == ('w' if State.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('purple'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('blue'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))

#actual display of the board
def drawBoard(screen):
    colors = [p.Color("Tan"), p.Color("Brown")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

#displays each of the pieces as the size of the square
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

#displays the text at the end of the game depending on how it ended
def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 50, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0,0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('White'))
    screen.blit(textObject, textLocation.move(2,2))


main()