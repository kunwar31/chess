from .position import Position, File


def _get_fwd_rank(position, n_step):
    if 1 <= position.rank + n_step <= 8:
        return position.rank + n_step


def _get_right_file(position, n_step):
    if File('A') <= position.file + n_step <= File('H'):
        return position.file + n_step


def get_forward_moves(position, n_steps, color, cover_all=True):
    moves = []
    if cover_all:
        steps_range = range(1, n_steps+1) if n_steps > 0 else range(n_steps, 0)
    else:
        steps_range = [n_steps]
    color = -1 if color == 'B' else 1

    for n_step in steps_range:
        if _get_fwd_rank(position, n_step * color) is not None:
            moves.append(Position(rank=_get_fwd_rank(position, n_step * color), file=position.file))
    return moves


def get_backward_moves(position, n_steps, color, cover_all=True):
    return get_forward_moves(position, -n_steps, color, cover_all)


def get_right_moves(position, n_steps, color, cover_all=True):
    moves = []
    if cover_all:
        steps_range = range(1, n_steps + 1) if n_steps > 0 else range(n_steps, 0)
    else:
        steps_range = [n_steps]
    color = -1 if color == 'B' else 1

    for n_step in steps_range:
        if _get_right_file(position, n_step * color) is not None:
            moves.append(Position(rank=position.rank, file=_get_right_file(position, n_step * color)))
    return moves


def get_left_moves(position, n_steps, color, cover_all=True):
    return get_right_moves(position, -n_steps, color, cover_all)


def get_forward_right_diagonal_moves(position, n_steps, color):
    moves = []
    color = -1 if color == 'B' else 1

    for n_step in range(1, n_steps+1):
        n_step *= color

        if _get_right_file(position, n_step) is not None and \
                _get_fwd_rank(position, n_step) is not None:
            moves.append(Position(rank=_get_fwd_rank(position, n_step),
                                  file=_get_right_file(position, n_step))
                         )
    return moves


def get_forward_left_diagonal_moves(position, n_steps, color):
    moves = []
    color = -1 if color == 'B' else 1

    for n_step in range(1, n_steps+1):
        n_step *= color

        if _get_right_file(position, -n_step) is not None and \
                _get_fwd_rank(position, n_step) is not None:

            moves.append(Position(rank=_get_fwd_rank(position, n_step),
                                  file=_get_right_file(position, -n_step))
                         )
    return moves


def get_backward_left_diagonal_moves(position, n_steps, color):
    moves = []
    color = -1 if color == 'B' else 1

    for n_step in range(-n_steps, 0):
        n_step *= color

        if _get_right_file(position, n_step) is not None and \
                _get_fwd_rank(position, n_step) is not None:

            moves.append(Position(rank=_get_fwd_rank(position, n_step),
                                  file=_get_right_file(position, n_step))
                         )
    return moves


def get_backward_right_diagonal_moves(position, n_steps, color):
    moves = []
    color = -1 if color == 'B' else 1

    for n_step in range(-n_steps, 0):
        n_step *= color

        if _get_right_file(position, -n_step) is not None and \
                _get_fwd_rank(position, n_step) is not None:

            moves.append(Position(rank=_get_fwd_rank(position, n_step),
                                  file=_get_right_file(position, -n_step)))
    return moves


