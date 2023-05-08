# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

import numpy as np
import random
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!
MAX_DEPTH = 2

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
            return SpawnAction(HexPos(3, 3))
        
        else: #from second step
            match self._color:
                case PlayerColor.RED:
                    # return SpawnAction(HexPos(3, 3))
                    #action tuple: (new board after a selected action, action is spawn or spread, (optional if action is spread, this is the pos where it starts spreading), vector is spot when spawning or direction when spreading)
                    actiontuple = get_action(self)
                    # print(actiontuple)
                    
                    # choose to spawn
                    if actiontuple[0] == "spawn":
                        spawnspot = actiontuple[1]
                        return SpawnAction(HexPos(spawnspot[0], spawnspot[1]))
                    # choose to spread
                    if actiontuple[0] == "spread":
                        spreadspot = actiontuple[1]
                        spreaddir = actiontuple[2]
                        return SpreadAction(HexPos(spreadspot[0], spreadspot[1]), HexDir(spreaddir))
                
                case PlayerColor.BLUE:
                    # return SpawnAction(HexPos(3, 3))
                    #action tuple: (new board after a selected action, action is spawn or spread, (optional if action is spread, this is the pos where it starts spreading), vector is spot when spawning or direction when spreading)
                    actiontuple = get_action(self)
                    # print(actiontuple)
                    
                    # choose to spawn
                    if actiontuple[0] == "spawn":
                        spawnspot = actiontuple[1]
                        return SpawnAction(HexPos(spawnspot[0], spawnspot[1]))
                    # choose to spread
                    if actiontuple[0] == "spread":
                        spreadspot = actiontuple[1]
                        spreaddir = actiontuple[2]
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
                    else:
                        self._board[newpos] = (color, 1 + newpower)
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                pass
        
        #print(self._board)
    
def get_action(self):
    boardcopy = self._board.copy() # it is a copy of the board dict
    color = self._color
    opponentcolor = None
    
    map = list(boardcopy.items())
    
    if color == PlayerColor.RED:
        opponentcolor = PlayerColor.BLUE
    else:
        opponentcolor = PlayerColor.RED
    
    for set in map:
            thispos = set[0]
            if set[1][0] == color:
                for dir in DIRECTION_LIST:
                    newpos = change_position(array_add(thispos, dir))
                    if boardcopy[newpos][0] == opponentcolor:
                        return ("spread", thispos, dir)
    
    if calc_totalpower(boardcopy) == 49:
        newmap = list()
        for set in map:
            if set[1][0] == color:
                newmap.append(set)
        randomchoice = random.choice(newmap)
        randompos = randomchoice[0]
        randomdircode = random.randint(0, 5)
        randomdir = DIRECTION_LIST[randomdircode]
        return ("spread", randompos, randomdir)
    
    else:
        newmap = list()
        for set in map:
            if set[1][0] == None:
                newmap.append(set)
    # print(newmap)
    
    randomchoice = random.choice(newmap)
    return ("spawn", randomchoice[0])
    
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