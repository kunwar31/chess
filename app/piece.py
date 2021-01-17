from copy import deepcopy
from .moves import get_left_moves, get_right_moves, get_forward_moves, get_backward_moves,\
    get_backward_left_diagonal_moves, get_backward_right_diagonal_moves, get_forward_left_diagonal_moves, \
    get_forward_right_diagonal_moves


class Piece:
    """
    Abstract class for a chess piece
    """
    def __init__(self, position, color=None, name='E'):
        self.color = color
        self.name = name
        self.position = position
        self.history = []

    def __repr__(self):
        if self.color is not None:
            return f"{self.color}:{self.name}"
        return f" {self.name} "

    def get_moves(self, board):
        # Gets moves without considering king check
        # TODO - config based moves
        raise NotImplementedError

    def get_legal_moves(self, board):
        # TODO - King castles
        # TODO - Pawn - en passant

        legal_moves = set()

        moves = self.get_moves(board)
        king_pos = board.king[self.color].position
        attacked_positions = board.get_attacked_positions(self.color)

        # check if king in check and if we can block/take
        if board.king_in_check[self.color]:
            for piece, attacked_path in attacked_positions.items():
                if king_pos in attacked_path:
                    # Check if can block
                    possible_blocks = moves.intersection(attacked_path)
                    blocks = set()
                    for block in possible_blocks:
                        board_copy = deepcopy(board)
                        board_copy.move_piece(self.position, block)
                        if king_pos not in piece.get_legal_moves(board_copy):
                            blocks.add(block)

                    if len(blocks) > 0:
                        legal_moves.update(blocks)

                    # Check if can take
                    legal_moves.update(moves.intersection({piece.position}))

            return legal_moves

        # check for pins
        for piece, attacked_path in attacked_positions.items():
            if self.position in attacked_path:
                board_copy = deepcopy(board)
                board_copy.set_piece(Pieces.E(position=self.position))
                piece_moves = piece.get_legal_moves(board_copy)
                if board_copy.king[self.color].position in piece_moves:
                    return set()

        legal_moves.update(moves)

        return legal_moves

    def get_attacked_positions(self, board):
        # Returns positions where king cannot move
        return self.get_moves(board)

    def move(self, position):
        self.history.append(self.position)
        self.position = position


class Knight(Piece):
    def __init__(self, position, color='W'):
        super(Knight, self).__init__(position=position, color=color,  name='N')

    def get_moves(self, board):
        moves = []
        forward_backward_moves = []
        forward_backward_moves.extend(get_forward_moves(self.position, 2, self.color, board, is_not_knight=False))
        forward_backward_moves.extend(get_backward_moves(self.position, 2, self.color, board, is_not_knight=False))
        for position in forward_backward_moves:
            moves.extend(get_left_moves(position, 1, self.color, board))
            moves.extend(get_right_moves(position, 1, self.color, board))

        left_right_moves = []
        left_right_moves.extend(get_left_moves(self.position, 2, self.color, board, is_not_knight=False))
        left_right_moves.extend(get_right_moves(self.position, 2, self.color, board, is_not_knight=False))
        for position in left_right_moves:
            moves.extend(get_forward_moves(position, 1, self.color, board))
            moves.extend(get_backward_moves(position, 1, self.color, board))

        return set(moves)


class Rook(Piece):
    def __init__(self, position, color='W'):
        super(Rook, self).__init__(position=position, color=color,  name='R')

    def get_moves(self, board):
        moves = []

        moves.extend(get_forward_moves(self.position, 8, self.color, board))
        moves.extend(get_backward_moves(self.position, 8, self.color, board))
        moves.extend(get_left_moves(self.position, 8, self.color, board))
        moves.extend(get_right_moves(self.position, 8, self.color, board))

        return set(moves)


class Pawn(Piece):
    def __init__(self, position, color='W'):
        super(Pawn, self).__init__(position=position, color=color,  name='P')

    def get_moves(self, board):
        # Pawn moves:
        #   Forward 1 step
        #   Forward 2 step when at 2nd/7th rank
        #   Moves diagonally

        moves = []

        # 1 step fwd
        moves.extend(get_forward_moves(self.position, 1, self.color, board))

        # 1 step fwd diagonal
        moves.extend(get_forward_right_diagonal_moves(self.position, 1, self.color, board))
        moves.extend(get_forward_left_diagonal_moves(self.position, 1, self.color, board))

        # 2 step fwd
        if (self.color == 'W' and self.position.rank == 2) or (self.color == 'B' and self.position.rank == 7):
            moves.extend(get_forward_moves(self.position, 2, self.color, board))

        return set(moves)

    def get_attacked_positions(self, board):
        positions = []
        positions.extend(get_forward_right_diagonal_moves(self.position, 1, self.color, board, is_for_attack=True))
        positions.extend(get_forward_left_diagonal_moves(self.position, 1, self.color, board, is_for_attack=True))
        return set(positions)


class Bishop(Piece):
    def __init__(self, position, color='W'):
        super(Bishop, self).__init__(position=position, color=color,  name='B')

    def get_moves(self, board):
        moves = []

        moves.extend(get_forward_right_diagonal_moves(self.position, 8, self.color, board))
        moves.extend(get_forward_left_diagonal_moves(self.position, 8, self.color, board))
        moves.extend(get_backward_right_diagonal_moves(self.position, 8, self.color, board))
        moves.extend(get_backward_left_diagonal_moves(self.position, 8, self.color, board))

        return set(moves)


class Queen(Piece):
    def __init__(self, position, color='W'):
        super(Queen, self).__init__(position=position, color=color,  name='Q')

    def get_moves(self, board):
        moves = []

        moves.extend(get_forward_moves(self.position, 8, self.color, board))
        moves.extend(get_backward_moves(self.position, 8, self.color, board))
        moves.extend(get_left_moves(self.position, 8, self.color, board))
        moves.extend(get_right_moves(self.position, 8, self.color, board))
        moves.extend(get_forward_right_diagonal_moves(self.position, 8, self.color, board))
        moves.extend(get_forward_left_diagonal_moves(self.position, 8, self.color, board))
        moves.extend(get_backward_right_diagonal_moves(self.position, 8, self.color, board))
        moves.extend(get_backward_left_diagonal_moves(self.position, 8, self.color, board))

        return set(moves)


class King(Piece):
    def __init__(self, position, color='W'):
        super(King, self).__init__(position=position, color=color,  name='K')

    def get_moves(self, board):
        moves = []

        moves.extend(get_forward_moves(self.position, 1, self.color, board))
        moves.extend(get_backward_moves(self.position, 1, self.color, board))
        moves.extend(get_left_moves(self.position, 1, self.color, board))
        moves.extend(get_right_moves(self.position, 1, self.color, board))
        moves.extend(get_forward_right_diagonal_moves(self.position, 1, self.color, board))
        moves.extend(get_forward_left_diagonal_moves(self.position, 1, self.color, board))
        moves.extend(get_backward_right_diagonal_moves(self.position, 1, self.color, board))
        moves.extend(get_backward_left_diagonal_moves(self.position, 1, self.color, board))

        moves = set(moves)
        attacked_positions = board.get_attacked_positions(self.color)

        # King cannot move into a check
        for piece, attacked_path in attacked_positions.items():
            moves = moves - attacked_path
        return moves

    def get_legal_moves(self, board):
        return self.get_moves(board)

    def is_in_check(self, board):
        attacked_positions = board.get_attacked_positions(self.color)

        for piece, attacked_path in attacked_positions.items():
            if self.position in attacked_path:
                board.king_in_check[self.color] = True
                return True

        board.king_in_check[self.color] = False
        return False

    def get_attacked_positions(self, board):
        moves = []

        moves.extend(get_forward_moves(self.position, 1, self.color, board))
        moves.extend(get_backward_moves(self.position, 1, self.color, board))
        moves.extend(get_left_moves(self.position, 1, self.color, board))
        moves.extend(get_right_moves(self.position, 1, self.color, board))
        moves.extend(get_forward_right_diagonal_moves(self.position, 1, self.color, board))
        moves.extend(get_forward_left_diagonal_moves(self.position, 1, self.color, board))
        moves.extend(get_backward_right_diagonal_moves(self.position, 1, self.color, board))
        moves.extend(get_backward_left_diagonal_moves(self.position, 1, self.color, board))

        return set(moves)


class Pieces:
    P = Pawn
    N = Knight
    R = Rook
    B = Bishop
    Q = Queen
    K = King
    E = Piece
