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

class Agent:
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
        match self._color:
            case PlayerColor.RED:
                return SpawnAction(HexPos(3, 3))
            case PlayerColor.BLUE:
                # This is going to be invalid... BLUE never spawned!
                return SpreadAction(HexPos(3, 3), HexDir.Up)

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                pos = tuple([int(i) for i in str(cell).split("-")])
                self._board[pos] = (color, 1)
                print(f"Testing: {color} SPAWN at {cell}")
                pass
            case SpreadAction(cell, direction):
                pos = tuple([int(i) for i in str(cell).split("-")])
                power = self._board[pos][-1]
                for i in power:
                    newpos = change_position(array_add(pos,array_mul(direction,i)))
                    newpower = self._board[newpos][-1]
                    self._board[newpos] = (color, 1 + newpower)
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                pass
        print(self._board)
        #get_action(self)
    
def get_action(self):
    board = self._board.copy
    print(board)
    
def change_position(pointA):
    return (pointA[0] % 7, pointA[1] % 7)

def array_add (A, B):
    return np.add(np.array(A),np.array(B))

def array_mul (A, B):
    return np.array(A) * B

# def minimax(node, depth, maximizing_player, scores, children):
#     if depth == 0 or node not in children:
#         return scores[node]

#     if maximizing_player:
#         best_value = float('-inf')
#         for child in children[node]:
#             value = minimax(child, depth-1, False, scores, children)
#             best_value = max(best_value, value)
#         return best_value

#     else: # minimizing player
#         best_value = float('inf')
#         for child in children[node]:
#             value = minimax(child, depth-1, True, scores, children)
#             best_value = min(best_value, value)
#         return best_value

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

# def Greedy(state, evaluationFunction):
#     bestScore = float('-inf')
#     bestAction = None
#     for action in state.getLegalActions():
#         successor = state.generateSuccessor(action)
#         score = evaluationFunction(successor)
#         if score > bestScore:
#             bestScore, bestAction = score, action
#     return bestAction