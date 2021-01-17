import time
from .piece import Pieces as p
from .position import Position
from datetime import datetime
from copy import deepcopy
from IPython.display import display, clear_output


"""

board -> {
    Position -> Piece
}

"""


class Board:
    """
    A chess board
    """
    def __init__(self, snapshots=True, fill=True):
        self.board = {}
        self.board_states = {}
        self.latest_datetime = datetime.now()
        self.snapshots = snapshots

        self.king = {
            'W': None,
            'B': None
        }

        self.king_in_check = {
            'W': False,
            'B': False
        }
        if fill:
            self._fill_board()

    def copy(self, snapshots=False):
        new_board = Board(snapshots=snapshots, fill=False)
        new_board.board = {}
        for position, piece in self.board.items():
            new_piece = piece.copy()
            new_board.board[new_piece.position] = new_piece
        new_board.king = self.king.copy()
        new_board.king_in_check = self.king_in_check.copy()
        return new_board

    def __hash__(self):
        hash_str = ''
        for position, piece in self.board.items():
            hash_str += str(piece.__hash__())
        return hash_str.__hash__()

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __getitem__(self, position):
        return self.board.get(position)

    def set_piece(self, piece):
        self.board[piece.position] = piece

    def _board_snapshot(self):
        if self.snapshots:
            self.latest_datetime = datetime.now()
            self.board_states[self.latest_datetime] = self.copy()

    def _fill_board(self):

        self.set_piece(p.R(position=Position(1, 'H')))
        self.set_piece(p.N(position=Position(1, 'G')))
        self.set_piece(p.B(position=Position(1, 'F')))
        self.set_piece(p.K(position=Position(1, 'E')))
        self.set_piece(p.Q(position=Position(1, 'D')))
        self.set_piece(p.B(position=Position(1, 'C')))
        self.set_piece(p.N(position=Position(1, 'B')))
        self.set_piece(p.R(position=Position(1, 'A')))

        for file in 'ABCDEFGH':
            self.set_piece(p.P(position=Position(2, file)))

        self.set_piece(p.R(position=Position(8, 'H'), color='B'))
        self.set_piece(p.N(position=Position(8, 'G'), color='B'))
        self.set_piece(p.B(position=Position(8, 'F'), color='B'))
        self.set_piece(p.K(position=Position(8, 'E'), color='B'))
        self.set_piece(p.Q(position=Position(8, 'D'), color='B'))
        self.set_piece(p.B(position=Position(8, 'C'), color='B'))
        self.set_piece(p.N(position=Position(8, 'B'), color='B'))
        self.set_piece(p.R(position=Position(8, 'A'), color='B'))

        self.king['W'] = self.get_piece(Position(1, 'E'))
        self.king['B'] = self.get_piece(Position(8, 'E'))

        for file in 'ABCDEFGH':
            self.set_piece(p.P(position=Position(7, file), color='B'))
        self._board_snapshot()

    def view_board(self):
        for rank in range(8, 0, -1):
            for file in 'ABCDEFGH':
                piece = self[Position(rank=rank, file=file)]
                if piece is None:
                    piece = p.E(Position(rank=rank, file=file))
                print(piece, end=' ')
            print()

    def view_board_history(self, sleep_time=1.5):
        for date_time, board in self.board_states.items():
            clear_output(wait=True)
            view_board = []
            display(date_time)

            for rank in range(8, 0, -1):
                file_row = []
                for file in 'ABCDEFGH':
                    piece = board[Position(rank=rank, file=file)]
                    if piece is None:
                        piece = p.E(Position(rank=rank, file=file))
                    file_row.append(piece)
                view_board.append(file_row)

            display(view_board)
            time.sleep(sleep_time)

    def view_board_positions(self):
        for rank in range(8, 0, -1):
            for file in 'ABCDEFGH':
                print(self[Position(rank=rank, file=file)].position, end=' ')
            print()

    def get_piece(self, position):
        return self[position]

    def move_piece(self, from_position, to_position):
        piece = self.get_piece(from_position)
        piece.move(to_position)
        del self.board[from_position]
        self.board[to_position] = piece
        self._board_snapshot()

    def get_attacked_positions(self, color):
        attacked_positions = {}

        for piece in self.board.values():
            if piece.color != color:
                attacked_positions[piece] = piece.get_attacked_positions(self)

        return attacked_positions
