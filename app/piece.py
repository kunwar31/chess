from .position import Position
from .moves import get_left_moves, get_right_moves, get_forward_moves, get_backward_moves,\
    get_backward_left_diagonal_moves, get_backward_right_diagonal_moves, get_forward_left_diagonal_moves, \
    get_forward_right_diagonal_moves


class Piece:
    """
    Abstract class for a chess piece
    """
    def __init__(self, position, color=None, name='E', icon='.', score=0):
        self.color = color
        self.name = name
        self.position = position
        # self.history = []
        self.score = score
        self.icon = icon

    def __hash__(self):
        return f"{self.position.__hash__()}{self.name}{self.color}".__hash__()

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def copy(self):
        return type(self)(position=Position(rank=self.position.rank,
                                            file=self.position.file),
                          color=self.color)

    def __repr__(self):
        return f" {self.icon} "

    def get_moves(self, board):
        # Gets moves without considering king check
        # TODO - config based moves
        raise NotImplementedError

    def get_legal_moves(self, board):
        # TODO - King castles
        # TODO - Pawn - en passant
        # TODO - Pawn to 8th rank promotes

        legal_moves = set()

        moves = self.get_moves(board) - {self.position}
        king_pos = board.king[self.color].position
        attacked_positions = board.get_attacked_positions(self.color)
        king_in_check = board.king[self.color].is_in_check(board)

        # check for pins
        for piece, attacked_path in attacked_positions.items():
            if self.position in attacked_path:
                if not king_in_check:
                    board_copy = board.copy()
                    del board_copy.board[self.position]
                    if board_copy.king[self.color].is_in_check(board_copy):
                        return set()

        # check if king in check and if we can block/take
        if king_in_check:
            for piece, attacked_path in attacked_positions.items():
                if king_pos in attacked_path:
                    # Check if can block
                    possible_blocks = moves.intersection(attacked_path)
                    blocks = set()
                    for block in possible_blocks:
                        board_copy = board.copy()
                        board_copy.move_piece(self.position, block)
                        if not board_copy.king[self.color].is_in_check(board_copy):
                            blocks.add(block)

                    if len(blocks) > 0:
                        legal_moves.update(blocks)

                    # Check if can take
                    legal_moves.update(moves.intersection({piece.position}))

            return legal_moves

        legal_moves.update(moves)

        return legal_moves

    def get_attacked_positions(self, board):
        # Returns positions where king cannot move
        return self.get_moves(board)

    def move(self, position):
        # self.history.append(self.position)
        self.position = position


class Knight(Piece):
    def __init__(self, position, color='W'):
        if color == 'W':
            icon = '♘'
        else:
            icon = '♞'
        super(Knight, self).__init__(position=position, color=color, name='N', icon=icon, score=3)

    def get_moves(self, board):
        moves = set()
        forward_backward_moves = []
        forward_backward_moves.extend(get_forward_moves(self.position, 2, self.color, board, is_not_knight=False))
        forward_backward_moves.extend(get_backward_moves(self.position, 2, self.color, board, is_not_knight=False))
        for position in forward_backward_moves:
            moves.update(get_left_moves(position, 1, self.color, board))
            moves.update(get_right_moves(position, 1, self.color, board))

        left_right_moves = []
        left_right_moves.extend(get_left_moves(self.position, 2, self.color, board, is_not_knight=False))
        left_right_moves.extend(get_right_moves(self.position, 2, self.color, board, is_not_knight=False))
        for position in left_right_moves:
            moves.update(get_forward_moves(position, 1, self.color, board))
            moves.update(get_backward_moves(position, 1, self.color, board))

        return moves


class Rook(Piece):
    def __init__(self, position, color='W'):
        if color == 'W':
            icon = '♖'
        else:
            icon = '♜'
        super(Rook, self).__init__(position=position, color=color, name='R', icon=icon, score=5)

    def get_moves(self, board):
        moves = set()

        moves.update(get_forward_moves(self.position, 8, self.color, board))
        moves.update(get_backward_moves(self.position, 8, self.color, board))
        moves.update(get_left_moves(self.position, 8, self.color, board))
        moves.update(get_right_moves(self.position, 8, self.color, board))

        return moves


class Pawn(Piece):
    def __init__(self, position, color='W'):
        if color == 'W':
            icon = '♙'
        else:
            icon = '♟'
        super(Pawn, self).__init__(position=position, color=color, name='P', icon=icon, score=1)

    def get_moves(self, board):
        # Pawn moves:
        #   Forward 1 step
        #   Forward 2 step when at 2nd/7th rank
        #   Moves diagonally

        moves = set()

        # 1 step fwd
        moves.update(get_forward_moves(self.position, 1, self.color, board, is_pawn=True))

        # 1 step fwd diagonal
        moves.update(get_forward_right_diagonal_moves(self.position, 1, self.color, board))
        moves.update(get_forward_left_diagonal_moves(self.position, 1, self.color, board))

        # 2 step fwd
        if (self.color == 'W' and self.position.rank == 2) or (self.color == 'B' and self.position.rank == 7):
            moves.update(get_forward_moves(self.position, 2, self.color, board, is_pawn=True))

        return moves

    def get_attacked_positions(self, board):
        positions = set()
        positions.update(get_forward_right_diagonal_moves(self.position, 1, self.color, board, is_for_attack=True))
        positions.update(get_forward_left_diagonal_moves(self.position, 1, self.color, board, is_for_attack=True))
        return positions


class Bishop(Piece):
    def __init__(self, position, color='W'):
        if color == 'W':
            icon = '♗'
        else:
            icon = '♝'
        super(Bishop, self).__init__(position=position, color=color, name='B', icon=icon, score=3)

    def get_moves(self, board):
        moves = set()

        moves.update(get_forward_right_diagonal_moves(self.position, 8, self.color, board))
        moves.update(get_forward_left_diagonal_moves(self.position, 8, self.color, board))
        moves.update(get_backward_right_diagonal_moves(self.position, 8, self.color, board))
        moves.update(get_backward_left_diagonal_moves(self.position, 8, self.color, board))

        return moves


class Queen(Piece):
    def __init__(self, position, color='W'):
        if color == 'W':
            icon = '♕'
        else:
            icon = '♛'
        super(Queen, self).__init__(position=position, color=color, name='Q', icon=icon, score=9)

    def get_moves(self, board):
        moves = set()

        moves.update(get_forward_moves(self.position, 8, self.color, board))
        moves.update(get_backward_moves(self.position, 8, self.color, board))
        moves.update(get_left_moves(self.position, 8, self.color, board))
        moves.update(get_right_moves(self.position, 8, self.color, board))
        moves.update(get_forward_right_diagonal_moves(self.position, 8, self.color, board))
        moves.update(get_forward_left_diagonal_moves(self.position, 8, self.color, board))
        moves.update(get_backward_right_diagonal_moves(self.position, 8, self.color, board))
        moves.update(get_backward_left_diagonal_moves(self.position, 8, self.color, board))

        return moves


class King(Piece):
    def __init__(self, position, color='W'):
        if color == 'W':
            icon = '♔'
        else:
            icon = '♚'
        super(King, self).__init__(position=position, color=color, name='K', icon=icon, score=100)

    def get_moves(self, board):
        possible_moves = set()
        moves = set()

        possible_moves.update(get_forward_moves(self.position, 1, self.color, board))
        possible_moves.update(get_backward_moves(self.position, 1, self.color, board))
        possible_moves.update(get_left_moves(self.position, 1, self.color, board))
        possible_moves.update(get_right_moves(self.position, 1, self.color, board))
        possible_moves.update(get_forward_right_diagonal_moves(self.position, 1, self.color, board))
        possible_moves.update(get_forward_left_diagonal_moves(self.position, 1, self.color, board))
        possible_moves.update(get_backward_right_diagonal_moves(self.position, 1, self.color, board))
        possible_moves.update(get_backward_left_diagonal_moves(self.position, 1, self.color, board))

        # King cannot move into a check
        # TODO - fix King moves into checks sometimes

        for move in possible_moves:
            board_copy = board.copy()
            board_copy.move_piece(self.position, move)
            if not board_copy.get_piece(move).is_in_check(board_copy):
                moves.add(move)

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
        moves = set()

        moves.update(get_forward_moves(self.position, 1, self.color, board))
        moves.update(get_backward_moves(self.position, 1, self.color, board))
        moves.update(get_left_moves(self.position, 1, self.color, board))
        moves.update(get_right_moves(self.position, 1, self.color, board))
        moves.update(get_forward_right_diagonal_moves(self.position, 1, self.color, board))
        moves.update(get_forward_left_diagonal_moves(self.position, 1, self.color, board))
        moves.update(get_backward_right_diagonal_moves(self.position, 1, self.color, board))
        moves.update(get_backward_left_diagonal_moves(self.position, 1, self.color, board))

        return moves


class Pieces:
    P = Pawn
    N = Knight
    R = Rook
    B = Bishop
    Q = Queen
    K = King
    E = Piece
