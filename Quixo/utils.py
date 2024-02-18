import random
from game import Game, Move
from copy import deepcopy


def simulate_move(board, player, from_pos, move):
    from_pos = [from_pos[1], from_pos[0]]

    piece = player

    if move == Move.LEFT:
        for i in range(from_pos[1], 0, -1):
            board[(from_pos[0], i)] = board[(from_pos[0], i - 1)]
        board[(from_pos[0], 0)] = piece

    elif move == Move.RIGHT:
        for i in range(from_pos[1], board.shape[1] - 1, 1):
            board[(from_pos[0], i)] = board[(from_pos[0], i + 1)]
        board[(from_pos[0], board.shape[1] - 1)] = piece
        
    elif move == Move.TOP:
        for i in range(from_pos[0], 0, -1):
            board[(i, from_pos[1])] = board[(i - 1, from_pos[1])]
        board[(0, from_pos[1])] = piece
        
    elif move == Move.BOTTOM:
        for i in range(from_pos[0], board.shape[0] - 1, 1):
            board[(i, from_pos[1])] = board[(i + 1, from_pos[1])]
        board[(board.shape[0] - 1, from_pos[1])] = piece

    return board


def valid_random_move(game : Game):
        state = game.get_board()
        valid_cell = False
        while not valid_cell:
            x = random.randint(0, 4)
            if x == 0 or x == 4:
                y = random.randint(0, 4)
            else:
                y = random.choice([0, 4])
            from_pos = (x, y)
            if state[y][x] != (1 - game.get_current_player()):
                valid_cell = True

        available_moves= [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
        if x == 0:
            available_moves.remove(Move.LEFT)
        elif x == 4:
            available_moves.remove(Move.RIGHT)
        if y == 0:
            available_moves.remove(Move.TOP)
        elif y == 4:
            available_moves.remove(Move.BOTTOM)
        move = random.choice(available_moves)

        return from_pos, move


def generate_all_moves():
    population = list()
    for x in range(5):
        for y in range(5):
            if x == 0 or x == 4 or y == 0 or y == 4:
                available_moves= [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
                if x == 0:
                    available_moves.remove(Move.LEFT)
                elif x == 4:
                    available_moves.remove(Move.RIGHT)
                if y == 0:
                    available_moves.remove(Move.TOP)
                elif y == 4:
                    available_moves.remove(Move.BOTTOM)
                for m in available_moves:
                    population.append(((x, y), m))
    return population


def get_all_valid_moves(board, player):
    valid_moves = list()
    moves = generate_all_moves()
    for possible_move in moves:
        if board[possible_move[0][1]][possible_move[0][0]] != (1 - player):
            valid_moves.append(possible_move)
    return valid_moves
