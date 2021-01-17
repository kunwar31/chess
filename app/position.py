file_map = {
            1: 'A',
            2: 'B',
            3: 'C',
            4: 'D',
            5: 'E',
            6: 'F',
            7: 'G',
            8: 'H',
            -1: '??'
        }

rev_file_map = {
            'A': 1,
            'B': 2,
            'C': 3,
            'D': 4,
            'E': 5,
            'F': 6,
            'G': 7,
            'H': 8,
        }


class Position:
    def __init__(self, rank, file):
        if rank is None or file is None:
            raise ValueError

        self.rank = rank
        self.file = rev_file_map.get(file, file)

    def __repr__(self):

        return f"{file_map[self.file]}{self.rank}"

    def __hash__(self):
        return (self.rank * 8) + self.file

    def __gt__(self, other):
        return f"{self.file}{self.rank}" > f"{other.file.file}{other.rank}"

    def __lt__(self, other):
        return f"{self.file}{self.rank}" < f"{other.file.file}{other.rank}"

    def __eq__(self, other):
        return self.file == other.file and self.rank == other.rank
