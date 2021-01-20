from .board import Board
from functools import lru_cache
import time
import numpy as np
from multiprocessing.pool import Pool


def get_all_legal_moves(board, player):
    for position, piece in board.board.items():
        if piece.color == player:
            legal_moves = piece.get_legal_moves(board)
            if len(legal_moves) > 0:
                yield piece, legal_moves


def get_score(board, player):
    score = 0
    for position, piece in board.board.items():
        if piece.color == player:
            piece_score = piece.score
            score += piece_score
    return score


def get_score_difference(board, player):
    score = 0
    opponent_score = 0
    for position, piece in board.board.items():
        if piece.color == player:
            piece_score = piece.score
            score += piece_score
        else:
            piece_score = piece.score
            opponent_score += piece_score
    return score - opponent_score


def alphabeta_minimax(args):
    piece, move_position, board, player, current_player, start_time, max_time, depth, max_depth, min_depth,\
    alpha, beta = args

    if start_time == 0:
        start_time = time.time()

    if (time.time() - start_time >= max_time and depth >= min_depth) or depth >= max_depth:
        return get_score_difference(board, player)

    board_copy = board.copy()
    piece_copy = piece.copy()
    board_copy.move_piece(piece_copy.position, move_position)

    current_player = 'W' if current_player is 'B' else 'B'

    if current_player == player:
        value = -1000000000

        legal_moves = get_all_legal_moves(board_copy, current_player)

        for new_piece, legal_moves in legal_moves:
            for move in legal_moves:
                value = max(value, alphabeta_minimax((new_piece, move, board_copy, player,
                                                      current_player, start_time, max_time, depth+1, max_depth, min_depth,
                                                      alpha, beta)))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            if alpha >= beta:
                break
        return value
    else:
        value = 1000000000

        legal_moves = get_all_legal_moves(board_copy, current_player)

        for new_piece, legal_moves in legal_moves:
            for move in legal_moves:
                value = min(value, alphabeta_minimax((new_piece, move, board_copy, player,
                                                      current_player, start_time, max_time, depth+1, max_depth, min_depth,
                                                      alpha, beta)))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            if beta <= alpha:
                break
        return value


def minimax(args):
    piece, move_position, board, player, current_player, depth, max_depth = args
    if depth >= max_depth:
        return get_score_difference(board, player)

    board_copy = board.copy()
    piece_copy = piece.copy()
    board_copy.move_piece(piece_copy.position, move_position)

    if current_player == player:
        value = -1000000000

        current_player = 'W' if current_player is 'B' else 'B'
        legal_moves = get_all_legal_moves(board_copy, current_player)

        for new_piece, legal_moves in legal_moves:
            for move in legal_moves:
                value = max(value, minimax((new_piece, move, board_copy, player, current_player, depth + 1, max_depth)))
        return value
    else:
        value = 1000000000

        current_player = 'W' if current_player is 'B' else 'B'
        legal_moves = get_all_legal_moves(board_copy, current_player)

        for new_piece, legal_moves in legal_moves:
            for move in legal_moves:
                value = min(value, minimax((new_piece, move, board_copy, player, current_player, depth + 1, max_depth)))
        return value


def _get_score(args):
    piece, move_position, board, player, current_player, depth, max_depth = args
    if depth >= max_depth:
        return get_score_difference(board, player)

    piece_copy = piece.copy()
    best_score = -100000
    board_copy = board.copy()
    board_copy.move_piece(piece_copy.position, move_position)

    if current_player == 'W':
        new_current_player = 'B'
    else:
        new_current_player = 'W'

    legal_moves = get_all_legal_moves(board_copy, new_current_player)

    for new_piece, legal_moves in legal_moves:
        for move in legal_moves:

            new_score = _get_score((new_piece, move, board_copy.copy(), player, new_current_player,
                                              depth + 1, max_depth))
            if new_score > best_score:
                best_score = new_score

    return best_score


class ChessGame:
    def __init__(self, board, player_1='W', player_2='B'):
        self.board = board
        self.player_1 = player_1
        self.player_2 = player_2
        self.max_depth = 10
        self.cache = {}
        self.pool = Pool(100)

    def get_best_move(self, board, player, max_time, max_depth, min_depth):
        board_copy = board.copy()

        all_args = []

        for piece, legal_moves in get_all_legal_moves(board_copy, player):
            for move in legal_moves:
                all_args.append((piece, move, board_copy, player, player, 0, max_time, 0, max_depth, min_depth,
                                 -1000000000,
                                 1000000000))

        counter = 0

        all_node_scores = {}

        for new_score in self.pool.imap(alphabeta_minimax, all_args):
            all_node_scores[(all_args[counter][0], all_args[counter][1])] = new_score
            counter += 1

        best_score = max(all_node_scores.values())
        best_nodes = [node for node, score in all_node_scores.items() if score == best_score]
        print(all_node_scores)
        best_node = best_nodes[np.random.choice(range(len(best_nodes)), 1)[0]]
        print(best_node, best_score)
        return best_node, best_score

    def play(self, board, max_time=5, max_depth=50, min_depth=3):
        current_player = 'W'
        board.view_board()
        print()

        while True:
            (piece, move_position), _ = self.get_best_move(board, current_player, max_time, max_depth, min_depth)
            if piece is None:
                break
            board.move_piece(piece.position, move_position)

            print(f"{current_player} Moves {piece} to {move_position}")
            board.view_board()
            print()

            if current_player == 'W':
                current_player = 'B'
            else:
                current_player = 'W'




