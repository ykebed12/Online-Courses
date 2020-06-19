"""
Tic Tac Toe Player
"""
from copy import deepcopy
import math


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    play = 0
    for row in board:
        for cell in row:
            if cell == X:
                play += 1
            elif cell == O:
                play -= 1

    return X if play == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    a = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell is EMPTY:
                a.append((i,j))
    
    return a


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board[action[0]][action[1]] = player(board)
    return board

def transform(cell):
    """
    this function is used to calculate the winner of a board
    """
    if cell == X:
        return 1
    elif cell == O:
        return -1
    else:
        return 0

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    d1 = 0
    d2 = 0
    rows = [0, 0, 0]
    cols = [0, 0, 0]

    for j, row in enumerate(board):
        for i, cell in enumerate(row):
            
            cell_val = transform(cell)

            # First diagonal
            if i==j:
                d1 += cell_val
            
            # Rows
            rows[j] += cell_val

            # Columns
            cols[i] += cell_val

            # Second diagonal
            if i+j == 2:
                d2 += cell_val

    win = rows + cols + [d1,d2]

    if max(win) == 3:
        return X
    elif min(win) == -3:
        return O    
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    d1 = 0
    d2 = 0
    rows = [0, 0, 0]
    cols = [0, 0, 0]
    space = 0

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            
            cell_val = transform(cell)

            if cell == None:
                space += 1

            # First diagonal
            if i==j:
                d1 += cell_val
            
            # Rows
            rows[i] += cell_val

            # Columns
            cols[j] += cell_val

            # Second diagonal
            if i+j == 2:
                d2 += cell_val

    win = rows + cols + [d1,d2]

    return True if max(win) == 3 or min(win) == -3 or space == 0 else False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise
    given a terminal board.
    """
    who_wins = winner(board)
    if who_wins == X:
        return 1
    elif who_wins == O:
        return -1
    else:
        return 0


def actual_value(pc_player, board):
    utility_val = utility(board)
    if pc_player == X:
        return -utility_val
    else:
        return utility_val

def max_val(board):
    if terminal(board):
        return utility(board)
    v = -2
    
    for action in actions(board):
        b = deepcopy(board)
        v = max(v, min_val(result(b, action)))
        if v == 1:
            return 1
    return v

def min_val(board):
    if terminal(board):
        return utility(board)
    v = 2
    
    for action in actions(board):
        b = deepcopy(board)
        v = min(v, max_val(result(b, action)))
        if v == -1:
            return -1
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    
    result_action = None
    pc = player(board)
    value = 2 if pc == O else -2

    for action in actions(board):
        b = deepcopy(board)
        next_board = result(b, action)
        
        
        if pc == X:
            v = min_val(next_board)
            result_action, value = (action, v) if v > value else (result_action, value)
        else:
            v = max_val(next_board)
            result_action, value = (action, v) if v < value else (result_action, value)

    return result_action
