from prototype.exceptions import InvalidPathError
import copy


class Path:
    def __init__(self):
        self.boards = list()

    def __len__(self):
        return len(self.boards)

    def __getitem__(self, key):
        return self.boards[key]

    def __reversed__(self):
        reversed_path = Path()
        reversed_path.boards = list(reversed(self.boards))
        return reversed_path

    def append(self, board):
        self.boards.append(board)

    def concatenate(self, other):
        if not self.boards[-1] == other.boards[0]:
            raise RuntimeError("Can't concatenate these boards")
        self.boards = self.boards + other.boards[1:]
        return self

    def check_validity(self):
        if len(self) < 2:
            return

        for current_board, next_board in zip(self.boards, self.boards[1:]):
            found = False
            for direction in current_board.valid_directions():
                moved_board = copy.deepcopy(current_board)
                moved_board.move_blank(direction)
                if moved_board == next_board:
                    found = True
                    break
            if not found:
                raise InvalidPathError()
