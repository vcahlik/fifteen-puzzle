from prototype.utils import debug_print
from prototype.heuristics.heuristic import Heuristic
import prototype.constants as constants
import os


PATTERN_DATABASE_FOLDER = os.path.join(constants.PROJECT_ROOT, "data/pattern-databases")


class CppSubproblemPatternDatabase(Heuristic):
    """
    A subproblem of the C++ pattern database heuristic.

    The goal of the subproblem is to correctly place a subset of pebbles to their goal positions.
    """
    def __init__(self, pebbles):
        self.pebbles = pebbles
        self.n_db_pebbles = len(self.pebbles) + 1
        self.db = None
        self._db_coefficients = self._calculate_db_coefficients()

    def load_db(self):
        """
        Loads the database from disk.
        """
        db_file = open(self.db_file_path(), 'rb')
        self.db = bytearray(db_file.read())

    def cost(self, pebble_positions):
        """
        Returns the value from the database.
        """
        return self.db[self._db_index(pebble_positions)]

    def _calculate_db_coefficients(self):
        """
        Calculates the coefficient by which to multiply the pebble positions in order to get the key for the database.
        """
        index_coefficients = []
        coefficient = 1
        for i in range(17 - self.n_db_pebbles, 17):
            index_coefficients.append(coefficient)
            coefficient = coefficient * i
        return list(reversed(index_coefficients))

    def _db_index(self, pebble_positions):
        """
        Calculates the "index" (=key) for the database for the given configuration.
        """
        index = 0
        readjustments = [0] * self.n_db_pebbles

        for i in range(0, self.n_db_pebbles):
            index = index + self._db_coefficients[i] * (pebble_positions[i] + readjustments[i])

            for j in range(i + 1, self.n_db_pebbles):
                if pebble_positions[j] > pebble_positions[i]:
                    readjustments[j] = readjustments[j] - 1

        return index

        # readjusted_positions = self._db_readjusted_positions(pebble_positions)
        # coefficients = self._db_coefficients
        # index = 0
        # for coef, pos in zip(coefficients, readjusted_positions):
        #     index = index + coef * pos
        # return index

    def db_file_path(self):
        """
        Determines the file path of the database.
        """
        return os.path.join(PATTERN_DATABASE_FOLDER, f"Subproblem-{'-'.join([str(pebble) for pebble in self.pebbles])}.bin")


_pattern_definitions = {
    1: [(i, ) for i in range(1, 16)],
    2: [
        (1, 2),
        (3, 4),
        (5, 6),
        (7, 8),
        (9, 10),
        (11, 12),
        (13, 14),
        (15, ),
    ],
    3: [
        (1, 2, 5),
        (3, 4, 8),
        (6, 9, 10),
        (7, 11, 12),
        (13, 14, 15)
    ],
    4: [
        (1, 2, 5, 6),
        (3, 4, 7, 8),
        (9, 10, 13, 14),
        (11, 12, 15)
    ],
    5: [
        (1, 2, 3, 5, 6),
        (4, 7, 8, 11, 12),
        (9, 10, 13, 14, 15)
    ],
    6: [
        (1, 2, 5, 6, 9, 10),
        (3, 4, 7, 8, 11, 12),
        (13, 14, 15)
    ],
    7: [
        (1, 2, 3, 4, 5, 6, 7),
        (9, 10, 11, 12, 13, 14, 15),
        (8, )
    ],
    8: [
        (1, 2, 3, 4, 5, 6, 7, 8),
        (9, 10, 11, 12, 13, 14, 15)
    ]
}


class CppPatternDatabaseHeuristic(Heuristic):
    """
    A "C++" pattern database heuristic.

    In this heuristic, the pattern databases were calculated by a C++ implementation.
    This heuristic merely loads the results from the databases.
    """
    def __init__(self, max_pattern_size=2, weight=1, callback=None):
        self.max_pattern_size = max_pattern_size
        self.subproblems = [CppSubproblemPatternDatabase(pebbles) for pebbles in _pattern_definitions[max_pattern_size]]
        self.weight = weight
        self.callback = callback

    def estimate_cost(self, board):
        """
        Estimate the optimal solution cost of a board.
        """
        if self.callback is not None:
            self.callback(board)

        return self.weight * sum([subproblem.cost(board.pebble_positions_subset_cpp(subproblem.pebbles)) for subproblem in self.subproblems])

    def load_db(self):
        """
        Loads the subproblems' databases from disk.
        """
        debug_print("Database loading from disk.")

        for subproblem in self.subproblems:
            subproblem.load_db()

        debug_print("Database loaded.")

    def name(self):
        if self.weight == 1:
            return f"PDB[Pat:{self.max_pattern_size}]"
        else:
            return f"PDB[Pat:{self.max_pattern_size};W:{self.weight}]"
