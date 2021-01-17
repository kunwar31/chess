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
    def __init__(self):
        self.board = {}
        self.board_states = {}
        self.attacked_positions = {}  # A history of attacked positions for both colors
        self.latest_datetime = datetime.now()

        self.king = {
            'W': None,
            'B': None
        }

        self.king_in_check = {
            'W': False,
            'B': False
        }
        self._fill_board()

    def __getitem__(self, position):
        return self.board[position]

    def set_piece(self, piece):
        self.board[piece.position] = piece

    def _board_snapshot(self):
        self.latest_datetime = datetime.now()

        self.board_states[self.latest_datetime] = deepcopy(self.board)
        self.attacked_positions[(self.latest_datetime, 'B')] = self.get_attacked_positions('B')
        self.attacked_positions[(self.latest_datetime, 'W')] = self.get_attacked_positions('W')

    def _fill_board(self):
        for rank in range(1, 9):
            for file in 'ABCDEFGH':
                position = Position(rank, file)
                self.board[position] = p.E(position=position, color=None)

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
                print(self.board[Position(rank=rank, file=file)], end=' ')
            print()

    def view_board_history(self, sleep_time=1.5):
        for date_time, board in self.board_states.items():
            clear_output(wait=True)
            view_board = []
            display(date_time)

            for rank in range(8, 0, -1):
                file_row = []
                for file in 'ABCDEFGH':
                    file_row.append(board[Position(rank=rank, file=file)])
                view_board.append(file_row)

            display(view_board)
            time.sleep(sleep_time)

    def view_board_positions(self):
        for rank in range(8, 0, -1):
            for file in 'ABCDEFGH':
                print(self.board[Position(rank=rank, file=file)].position, end=' ')
            print()

    def get_piece(self, position):
        return self.board[position]

    def move_piece(self, from_position, to_position):
        piece = self.get_piece(from_position)
        piece.move(to_position)
        self.set_piece(p.E(from_position))
        self.board[to_position] = piece
        self._board_snapshot()

    def get_attacked_positions(self, color):
        if (self.latest_datetime, color) in self.attacked_positions:
            return self.attacked_positions[(self.latest_datetime, color)]

        attacked_positions = {}

        for piece in self.board.values():
            if piece.name != 'E':
                if piece.color != color:
                    attacked_positions[piece] = piece.get_attacked_positions(self)

        return attacked_positions
