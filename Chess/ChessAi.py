"""
Allows for different AI algorithms to be implemented for the opponent
"""
import random

#set up heuristics for the algorithms to use
pieceScores = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 3}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3


#very basic AI that just chooses a random valid move
#not currently beingused
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


#Two move depth non-recursive greedy
#also not currently being used
def findGreedyMove(State, validMoves):
    turnMultiplier = 1 if State.whiteToMove else -1
    opponentMinMaxScore = -CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        State.makeMove(playerMove)
        opponentsMoves = State.getValidMoves()
        if State.stalemate:
            opponentMaxScore = STALEMATE
        elif State.checkmate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentMove in opponentsMoves:
                State.makeMove(opponentMove)
                State.getValidMoves()
                if State.checkmate:
                    score = CHECKMATE
                elif State.stalemate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreBoard(State.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                State.undoMove()
        if  opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        State.undoMove()
    return bestPlayerMove


#first recursive helper
def findBestMinMax(State, validMoves):
    global nextMove
    nextMove = None
    findRecursiveGreedyMove(State, validMoves, DEPTH, State.whiteToMove)
    return nextMove


#recursive greedy algorithm that allows for different depths to be picked
def findRecursiveGreedyMove(State, validMoves, depth, whiteToMove):
    random.shuffle(validMoves)
    global nextMove
    
    #base case, returns the score of each end move
    if depth == 0:
        return scoreBoard(State)
    #checks the weights and pins/checks for all of white's moves
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            State.makeMove(move)
            nextMoves = State.getValidMoves()

            savedInCheck = State.inCheck
            savedPins = State.pins[:]
            savedChecks = State.checks[:]

            score = findRecursiveGreedyMove(State, nextMoves, depth - 1, False)

            State.inCheck = savedInCheck
            State.pins = savedPins
            State.checks = savedChecks

            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            State.undoMove()
        return maxScore
    #checks the weights and pins/checks for all of black's moves
    else:
        minScore = CHECKMATE
        for move in validMoves:
            State.makeMove(move)
            nextMoves = State.getValidMoves()

            savedInCheck = State.inCheck
            savedPins = State.pins[:]
            savedChecks = State.checks[:]

            score = findRecursiveGreedyMove(State, nextMoves, depth - 1, True)

            State.inCheck = savedInCheck
            State.pins = savedPins
            State.checks = savedChecks

            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            State.undoMove()
        return minScore


#original scoreboard used for the nonrecursive greedy
#def scoreBoard(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScores[square[1]]
            elif square[0] == 'b':
                score -= pieceScores[square[1]]
    
    return score


#positive score is good for white, negative is good for black
def scoreBoard(State):
    if State.checkmate:
        if State.whiteToMove:
            return -CHECKMATE #black win
        else:
            return CHECKMATE #white win
    elif State.stalemate:
        return STALEMATE
    
    score = 0
    for row in State.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScores[square[1]]
            elif square[0] == 'b':
                score -= pieceScores[square[1]]
    
    return score