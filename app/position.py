class File:
    def __init__(self, file):
        """
        A + 1 = B
        """
        self.file = file

    def __add__(self, other):
        return File(chr(ord(self.file)+other))

    def __sub__(self, other):
        return File(chr(ord(self.file)-other))

    def __gt__(self, other):
        return self.file > other.file

    def __lt__(self, other):
        return self.file < other.file

    def __ge__(self, other):
        return self.file >= other.file

    def __le__(self, other):
        return self.file <= other.file


class Position:
    def __init__(self, rank, file):
        if rank is None or file is None:
            raise ValueError

        self.rank = rank
        if not isinstance(file, File):
            self.file = File(file)
        else:
            self.file = file

    def __repr__(self):
        return f"{self.file.file}{self.rank}"

    def __hash__(self):
        return f"{self.file.file}{self.rank}".__hash__()

    def __gt__(self, other):
        return f"{self.file.file}{self.rank}" > f"{other.file.file}{other.rank}"

    def __lt__(self, other):
        return f"{self.file.file}{self.rank}" < f"{other.file.file}{other.rank}"

    def __eq__(self, other):
        if isinstance(other, Position):
            return f"{self.file.file}{self.rank}" == f"{other.file.file}{other.rank}"
