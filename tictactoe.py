"""
Tic Tac Toe Player
"""

import math
import copy

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
    x_count = 0
    o_count = 0

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == X:
                x_count += 1
            elif board[i][j] == O:
                o_count += 1

    if x_count > o_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for i in range(len(board[0])):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception('Invalid Action!')

    i, j = action

    copyb = copy.deepcopy(board)
    copyb[i][j] = player(board)

    return copyb


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
# row winner
    for i in range(len(board)):
        if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] is not EMPTY:
            return board[i][0]

# columns winner
    for j in range(len(board)):
        if board[0][j] == board[1][j] and board[1][j] == board[2][j] and board[0][j] is not EMPTY:
            return board[0][j]

# diagonal winners
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == O:
        return -1
    elif winner(board) == X:
        return 1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.

    X = max, O = Min
    """

    def max_value(board):

        move = ()
        if terminal(board):
            return utility(board), move
        else:
            v = -math.inf
            for action in actions(board):
                minvalue = min_value(result(board, action))[0]
                if minvalue > v:
                    v = minvalue
                    move = action
            return v, move

    def min_value(board):

        move = ()
        if terminal(board):
            return utility(board), move
        else:
            v = math.inf
            for action in actions(board):
                maxvalue = max_value(result(board, action))[0]
                if maxvalue < v:
                    v = maxvalue
                    move = action
            return v, move

    if terminal(board):
        return None

    if player(board) == X:
        return max_value(board)[1]

    else:
        return min_value(board)[1]
