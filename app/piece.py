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
        self.active = True

    def __repr__(self):
        if self.color is not None:
            return f"{self.color}:{self.name}"
        return f" {self.name} "

    def get_moves(self):
        raise NotImplementedError

    def move(self, position):
        self.history.append(self.position)
        self.position = position


class Knight(Piece):
    def __init__(self, position, color='W'):
        super(Knight, self).__init__(position=position, color=color,  name='N')

    def get_moves(self):
        moves = []
        forward_backward_moves = []
        forward_backward_moves.extend(get_forward_moves(self.position, 2, self.color, cover_all=False))
        forward_backward_moves.extend(get_backward_moves(self.position, 2, self.color, cover_all=False))
        for position in forward_backward_moves:
            moves.extend(get_left_moves(position, 1, self.color))
            moves.extend(get_right_moves(position, 1, self.color))

        left_right_moves = []
        left_right_moves.extend(get_left_moves(self.position, 2, self.color, cover_all=False))
        left_right_moves.extend(get_right_moves(self.position, 2, self.color, cover_all=False))
        for position in left_right_moves:
            moves.extend(get_forward_moves(position, 1, self.color))
            moves.extend(get_backward_moves(position, 1, self.color))

        return moves



class Rook(Piece):
    def __init__(self, position, color='W'):
        super(Rook, self).__init__(position=position, color=color,  name='R')

    def get_moves(self):
        moves = []

        moves.extend(get_forward_moves(self.position, 8, self.color))
        moves.extend(get_backward_moves(self.position, 8, self.color))
        moves.extend(get_left_moves(self.position, 8, self.color))
        moves.extend(get_right_moves(self.position, 8, self.color))

        return list(set(moves))


class Pawn(Piece):
    def __init__(self, position, color='W'):
        super(Pawn, self).__init__(position=position, color=color,  name='P')

    def get_moves(self):
        # Pawn moves:
        #   Forward 1 step
        #   Forward 2 step when at 2nd/7th rank
        #   Moves diagonally

        moves = []

        # 1 step fwd
        moves.extend(get_forward_moves(self.position, 1, self.color))

        # 1 step fwd diagonal
        moves.extend(get_forward_right_diagonal_moves(self.position, 1, self.color))
        moves.extend(get_forward_left_diagonal_moves(self.position, 1, self.color))

        # 2 step fwd
        if (self.color == 'W' and self.position.rank == 2) or (self.color == 'B' and self.position.rank == 7):
            moves.extend(get_forward_moves(self.position, 2, self.color))

        return list(set(moves))


class Bishop(Piece):
    def __init__(self, position, color='W'):
        super(Bishop, self).__init__(position=position, color=color,  name='B')

    def get_moves(self):
        moves = []

        moves.extend(get_forward_right_diagonal_moves(self.position, 8, self.color))
        moves.extend(get_forward_left_diagonal_moves(self.position, 8, self.color))
        moves.extend(get_backward_right_diagonal_moves(self.position, 8, self.color))
        moves.extend(get_backward_left_diagonal_moves(self.position, 8, self.color))

        return list(set(moves))


class Queen(Piece):
    def __init__(self, position, color='W'):
        super(Queen, self).__init__(position=position, color=color,  name='Q')

    def get_moves(self):
        moves = []

        moves.extend(get_forward_moves(self.position, 8, self.color))
        moves.extend(get_backward_moves(self.position, 8, self.color))
        moves.extend(get_left_moves(self.position, 8, self.color))
        moves.extend(get_right_moves(self.position, 8, self.color))
        moves.extend(get_forward_right_diagonal_moves(self.position, 8, self.color))
        moves.extend(get_forward_left_diagonal_moves(self.position, 8, self.color))
        moves.extend(get_backward_right_diagonal_moves(self.position, 8, self.color))
        moves.extend(get_backward_left_diagonal_moves(self.position, 8, self.color))

        return list(set(moves))


class King(Piece):
    def __init__(self, position, color='W'):
        super(King, self).__init__(position=position, color=color,  name='K')

    def get_moves(self):
        moves = []

        moves.extend(get_forward_moves(self.position, 1, self.color))
        moves.extend(get_backward_moves(self.position, 1, self.color))
        moves.extend(get_left_moves(self.position, 2, self.color))
        moves.extend(get_right_moves(self.position, 2, self.color))
        moves.extend(get_forward_right_diagonal_moves(self.position, 1, self.color))
        moves.extend(get_forward_left_diagonal_moves(self.position, 1, self.color))
        moves.extend(get_backward_right_diagonal_moves(self.position, 1, self.color))
        moves.extend(get_backward_left_diagonal_moves(self.position, 1, self.color))

        return list(set(moves))


class Pieces:
    P = Pawn
    N = Knight
    R = Rook
    B = Bishop
    Q = Queen
    K = King
    E = Piece
