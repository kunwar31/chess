from .position import Position, File


def _get_fwd_rank(position, n_step):
    if 1 <= position.rank + n_step <= 8:
        return position.rank + n_step


def _get_right_file(position, n_step):
    if File('A') <= position.file + n_step <= File('H'):
        return position.file + n_step


def _get_straight_moves(position, n_steps, color, board, is_not_knight=True, is_sideways=True):
    moves = []
    if is_not_knight:
        steps_range = range(1, n_steps + 1) if n_steps > 0 else range(-1, n_steps - 1, -1)
    else:
        steps_range = [n_steps]
    color_sign = -1 if color == 'B' else 1

    for n_step in steps_range:

        new_file = _get_right_file(position, n_step * color_sign) if is_sideways else position.file
        new_rank = _get_fwd_rank(position, n_step * color_sign) if not is_sideways else position.rank

        if new_file is not None and new_rank is not None:
            new_position = Position(rank=new_rank, file=new_file)
            if is_not_knight:
                if board[new_position].name == 'E':
                    moves.append(new_position)
                elif board[new_position].name != 'E' and color != board[new_position].color:
                    moves.append(new_position)
                    break
                else:
                    break
            else:
                if board[new_position].name != 'E' and color != board[new_position].color:
                    moves.append(new_position)
                elif board[new_position].name == 'E':
                    moves.append(new_position)
    return moves


def _get_diagonal_moves(position, n_steps, color, board, is_forward=True, is_right=True, is_for_attack=False):
    moves = []
    color_sign = -1 if color == 'B' else 1

    steps_range = range(1, n_steps+1) if is_forward else range(-n_steps, 0)
    right_file_sign = 1 if is_right else -1

    for n_step in steps_range:
        fwd_rank = _get_fwd_rank(position, n_step * color_sign)
        right_file = _get_right_file(position, right_file_sign * n_step * color_sign)

        if fwd_rank is not None and right_file is not None:
            new_position = Position(rank=fwd_rank, file=right_file)
            if board[new_position].name == 'E' and (
                    board[position].name != 'P' or (board[position].name == 'P' and is_for_attack)):
                moves.append(new_position)
            elif (board[position].name == 'P' and
                  board[new_position].color != board[position].color and
                  board[new_position].name != 'E'):
                moves.append(new_position)
            elif board[new_position].name != 'E' and color != board[new_position].color:
                moves.append(new_position)
                break
            else:
                break
    return moves


def get_forward_moves(position, n_steps, color, board, is_not_knight=True):
    return _get_straight_moves(position, n_steps, color, board, is_not_knight, is_sideways=False)


def get_backward_moves(position, n_steps, color, board, is_not_knight=True):
    return get_forward_moves(position, -n_steps, color, board, is_not_knight)


def get_right_moves(position, n_steps, color, board, is_not_knight=True):
    return _get_straight_moves(position, n_steps, color, board, is_not_knight, is_sideways=True)


def get_left_moves(position, n_steps, color, board, is_not_knight=True):
    return get_right_moves(position, -n_steps, color, board, is_not_knight)


def get_forward_right_diagonal_moves(position, n_steps, color, board, **kwargs):
    return _get_diagonal_moves(position, n_steps, color, board, **kwargs)


def get_forward_left_diagonal_moves(position, n_steps, color, board, **kwargs):
    return _get_diagonal_moves(position, n_steps, color, board, is_right=False, **kwargs)


def get_backward_left_diagonal_moves(position, n_steps, color, board, **kwargs):
    return _get_diagonal_moves(position, n_steps, color, board, is_forward=False, is_right=False, **kwargs)


def get_backward_right_diagonal_moves(position, n_steps, color, board, **kwargs):
    return _get_diagonal_moves(position, n_steps, color, board, is_forward=False, **kwargs)
