# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

import numpy as np
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!
MAX_DEPTH = 1

UP = (1,- 1)
UPLEFT = (0, -1)
UPRIGHT = (1, 0)
DOWN = (-1, 1)
DOWNLEFT = (-1, 0)
DOWNRIGHT = (0, 1)
LEFT = (-1, -1)
RIGHT = (1, 1)
    
DIRECTION_LIST = [UP, UPLEFT, UPRIGHT, DOWN, DOWNLEFT, DOWNRIGHT]

class Agent:
    EMPTY = True
    
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        self._board = {} #empty board
        
        for i in range(7):
            for j in range(7):
                pos = (i, j)
                self._board[pos] = (None, 0) # player, power
        
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        if self.EMPTY: #first step
            match self._color:
                case PlayerColor.RED:
                    return SpawnAction(HexPos(3, 3))
                case PlayerColor.BLUE:
                    # This is going to be invalid... BLUE never spawned!
                    # return SpreadAction(HexPos(3, 3), HexDir.Up)
                    return SpawnAction(HexPos(3, 3))
        
        else: #from second step
            match self._color:
                case PlayerColor.RED:
                    #action tuple: (new board after a selected action, action is spawn or spread, (optional if action is spread, this is the pos where it starts spreading), vector is spot when spawning or direction when spreading)
                    actiontuple = get_action(self)
                    # print(score, actiontuple)
                    
                    # choose to spawn
                    if actiontuple[1] == "spawn":
                        spawnspot = actiontuple[2]
                        return SpawnAction(HexPos(spawnspot[0], spawnspot[1]))
                    # choose to spread
                    if actiontuple[1] == "spread":
                        spreadspot = actiontuple[2]
                        spreaddir = actiontuple[3]
                        return SpreadAction(HexPos(spreadspot[0], spreadspot[1]), HexDir(spreaddir))
                
                case PlayerColor.BLUE:
                    #action tuple: (new board after a selected action, action is spawn or spread, (optional if action is spread, this is the pos where it starts spreading), vector is spot when spawning or direction when spreading)
                    actiontuple = get_action(self)
                    # print(score, actiontuple)
                    
                    # choose to spawn
                    if actiontuple[1] == "spawn":
                        spawnspot = actiontuple[2]
                        return SpawnAction(HexPos(spawnspot[0], spawnspot[1]))
                    # choose to spread
                    if actiontuple[1] == "spread":
                        spreadspot = actiontuple[2]
                        spreaddir = actiontuple[3]
                        return SpreadAction(HexPos(spreadspot[0], spreadspot[1]), HexDir(spreaddir))
                    # return SpawnAction(HexPos(4, 4))
    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                pos = tuple([int(i) for i in str(cell).split("-")])
                self._board[pos] = (color, 1)
                self.EMPTY = False # dict already updated not empty
                print(f"Testing: {color} SPAWN at {cell}")
                pass
            case SpreadAction(cell, direction):
                pos = tuple([int(i) for i in str(cell).split("-")])
                power = self._board[pos][-1]
                dir = get_direction(str(direction))
                self._board[pos] = (None, 0)
                for i in range(power):
                    newpos = change_position(array_add(pos,array_mul(dir,i+1)))
                    newpower = self._board[newpos][-1]
                    if newpower == 6:
                        self._board[newpos] = (None, 0)
                        # print(self._board)
                    else:
                        self._board[newpos] = (color, 1 + newpower)
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                pass
        #print(self._board)
    
def get_action(self):
    boardcopy = self._board.copy() # it is a copy of the board dict
    # evaluation score, new board after a selected action, action is spawn or spread, vector is spot when spawning or direction when spreading
    score, actiontuple = minimax(boardcopy, MAX_DEPTH, True, self._color, self)
    return actiontuple

    
def change_position(pointA):
    return (pointA[0] % 7, pointA[1] % 7)

def array_add (A, B):
    return np.add(np.array(A),np.array(B))

def array_mul (A, B):
    return np.array(A) * B

def get_direction(direction):
    if direction == "[↘]":
        return (0, 1)
    if direction == "[↓]":
        return (-1, 1)
    if direction == "[↙]":
        return (-1, 0)
    if direction == "[↖]":
        return (0, -1)
    if direction == "[↑]":
        return (1, -1)
    if direction == "[↗]":
        return (1, 0)

def evalutation(board, color, self):
    # find power
    mypower = calc_mypower(board, color)
    totalpower = calc_totalpower(board)
    opponentpower = totalpower - mypower
    # print(mypower)
    # print(opponentpower)
    
    #find points
    mypoints = calc_mypoints(board, color)
    totalpoints = calc_totalpoints(board)
    opponentpoints = totalpoints - mypoints
    # print(mypoints)
    # print(opponentpoints)
    
    #current version is the sum of the difference of power and points
    value = 0.5*(mypower - opponentpower) + 0.5*(mypoints - opponentpoints)
    # value = mypower - opponentpower
    if color == self._color:
        return value
    else:
        return -value
    # value = mypower - opponentpower
# calculate power for a single color
def calc_mypower(board, color):
    board_list = list(board.items())
    sum = 0
    for set in board_list:
        if color == set[1][0]:
            sum += set[1][1]
    return sum

def calc_totalpower(board):
    board_list = list(board.items())
    sum = 0
    for set in board_list:
        sum += set[1][1]
    return sum

def calc_mypoints(board, color):
    board_list = list(board.items())
    sum = 0
    for set in board_list:
        if set[1][0] == color:
            sum += 1
    return sum

def calc_totalpoints(board):
    board_list = list(board.items())
    sum = 0
    for set in board_list:
        if set[1][0] != None:
            sum += 1
    return sum

best_child = None

def minimax(board, depth, maximizing_player, color, self):
    # print("this is a new attempt:")
    if depth == 0:
        return evalutation(board, color, self), []
    
    # set up the children for current board
    children = []
    
    # considering spawns
    # set:[(pos.r, pos.q), (color, power)]
    for set in list(board.items()):
        # we can make a spawn if nobody occupied this spot
        if set[1][0] == None and calc_totalpower(board) != 49:
            thispos = set[0]
            tempboard = board.copy()
            tempboard[thispos] = (color, 1)
            # temptuple contains three elements: (a new board, spawn/spread, spawn spot/direction vectror)
            temptuple = (tempboard, "spawn", thispos)
            children.append(temptuple)

    # considering spreads
    for set in list(board.items()):
        # correct color means this is my point
        if set[1][0] == color:
            thispos = set[0]
            thispower = set[1][1]
            
            # loop six directions and powers to set up new points after spread
            for dir in DIRECTION_LIST:
                for power in range(thispower):
                    tempboard = board.copy()
                    tempboard[thispos] = (None, 0)
                    newpos = change_position(array_add(thispos, array_mul(dir, power + 1)))
                    newpower = tempboard[newpos][1]
                    if newpower == 6:
                        tempboard[newpos] = (None, 0)
                    else:
                        tempboard[newpos] = (color, 1 + newpower)
                    # temptuple contains three elements: (a new board, spawn/spread, spawn spot/direction vectror)
                    temptuple = (tempboard, "spread", thispos, dir)
                    children.append(temptuple)
                    
    if maximizing_player:
        best_value = float('-inf')
        for child in children:
            # print(child[1], child[2])
            value, a = minimax(child[0], depth-1, False, color, self)
            if value > best_value:
                best_value = max(best_value, value)
                best_child = child
        return best_value, best_child

    else: # minimizing player
        best_value = float('inf')
        for child in children:
            # print(child[1], child[2])
            if color == PlayerColor.RED:
                value, a = minimax(child[0], depth-1, True, PlayerColor.BLUE, self)
                if value < best_value:
                    best_value = min(best_value, value)
                    best_child = child
            else:
                value, a = minimax(child[0], depth-1, True, PlayerColor.RED, self)
                if value < best_value:
                    best_value = min(best_value, value)
                    best_child = child
        # print(best_child)
        return best_value, best_child

# def MinimaxCutoff(state, depth, maximizingPlayer, evaluation, alpha, beta):
#     if depth == 0 or state.isWin() or state.isLose():
#         return evaluation(state), None

#     if maximizingPlayer:
#         bestScore = float('-inf')
#         for action in state.getLegalActions():
#             successor = state.generateSuccessor(action)
#             score, _ = MinimaxCutoff(successor, depth - 1, False, evaluation, alpha, beta)
#             if score > bestScore:
#                 bestScore, bestAction = score, action
#             if bestScore > beta:
#                 return bestScore, bestAction
#             alpha = max(alpha, bestScore)
#         return bestScore, bestAction

#     else:
#         bestScore = float('inf')
#         for action in state.getLegalActions():
#             successor = state.generateSuccessor(action)
#             score, _ = MinimaxCutoff(successor, depth - 1, True, evaluation, alpha, beta)
#             if score < bestScore:
#                 bestScore, bestAction = score, action
#             if bestScore < alpha:
#                 return bestScore, bestAction
#             beta = min(beta, bestScore)
#         return bestScore, bestAction
