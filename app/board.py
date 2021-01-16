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
        self._fill_board()

    def _add_piece(self, piece):
        self.board[piece.position] = piece

    def _fill_board(self):
        for rank in range(1, 9):
            for file in 'ABCDEFGH':
                position = Position(rank, file)
                self.board[position] = p.E(position=position, color=None)

        self._add_piece(p.R(position=Position(1, 'H')))
        self._add_piece(p.N(position=Position(1, 'G')))
        self._add_piece(p.B(position=Position(1, 'F')))
        self._add_piece(p.K(position=Position(1, 'E')))
        self._add_piece(p.Q(position=Position(1, 'D')))
        self._add_piece(p.B(position=Position(1, 'C')))
        self._add_piece(p.N(position=Position(1, 'B')))
        self._add_piece(p.R(position=Position(1, 'A')))

        for file in 'ABCDEFGH':
            self._add_piece(p.P(position=Position(2, file)))

        self._add_piece(p.R(position=Position(8, 'H'), color='B'))
        self._add_piece(p.N(position=Position(8, 'G'), color='B'))
        self._add_piece(p.B(position=Position(8, 'F'), color='B'))
        self._add_piece(p.K(position=Position(8, 'E'), color='B'))
        self._add_piece(p.Q(position=Position(8, 'D'), color='B'))
        self._add_piece(p.B(position=Position(8, 'C'), color='B'))
        self._add_piece(p.N(position=Position(8, 'B'), color='B'))
        self._add_piece(p.R(position=Position(8, 'A'), color='B'))

        for file in 'ABCDEFGH':
            self._add_piece(p.P(position=Position(7, file), color='B'))

        self.board_states[datetime.now()] = deepcopy(self.board)

    def view_board(self):
        for rank in range(8, 0, -1):
            for file in 'ABCDEFGH':
                print(self.board[Position(rank=rank, file=file)], end=' ')
            print()

    def view_board_history(self, sleep_time=5):
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
        self._add_piece(p.E(from_position))
        self.board[to_position] = piece
        self.board_states[datetime.now()] = deepcopy(self.board)
