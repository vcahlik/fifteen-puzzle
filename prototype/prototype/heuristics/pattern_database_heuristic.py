from prototype.graph_search.node import Node
from prototype.board import PartialBoard
from prototype.utils import debug_print, FastLookupQueue
from prototype.heuristics.heuristic import Heuristic
import prototype.constants as constants
import pickle
import multiprocessing
import os
import copy


PATTERN_DATABASE_FOLDER = os.path.join(constants.PROJECT_ROOT, "data/pattern-databases/prototype")


class Subproblem(Heuristic):
    ZERO_COST = 255

    def __init__(self, pebbles):
        self.pebbles = pebbles
        self.db = bytearray(self._db_size())
        self._db_coefficients = self._calculate_db_coefficients()
        self.db_folder_path = None

    """
    Size of the subproblem's database in bytes.
    
    :return: db size
    """
    def _db_size(self):
        size = 1
        for n_placements in range(16 - len(self.pebbles), 17):
            size = size * n_placements
        return size

    def cost(self, pebble_positions):
        cost = self.db[self._db_index(pebble_positions)]
        if cost == self.ZERO_COST:
            return 0
        elif cost > 0:
            return cost
        else:
            raise RuntimeError(f"Cost not in database.")

    def _db_readjusted_positions(self, pebble_positions):
        readjustments = [0 for _ in pebble_positions]

        for i, current_position in enumerate(pebble_positions[:-1]):
            for j, latter_position in enumerate(pebble_positions[i + 1:]):
                if latter_position > current_position:
                    readjustments[i + j + 1] = readjustments[i + j + 1] - 1

        for i, readjustment in enumerate(readjustments):
            readjustments[i] = pebble_positions[i] + readjustment

        return readjustments

    def _calculate_db_coefficients(self):
        coefficients = []
        c = 1
        for i in range(16 - len(self.pebbles), 17):
            coefficients.append(c)
            c = c * i
        return list(reversed(coefficients))

    def _db_index(self, pebble_positions):
        readjusted_positions = self._db_readjusted_positions(pebble_positions)
        coefficients = self._db_coefficients
        index = 0
        for coef, pos in zip(coefficients, readjusted_positions):
            index = index + coef * pos
        return index

    def has_cost(self, pebble_positions):
        return self.db[self._db_index(pebble_positions)] != 0

    def save_cost(self, pebble_positions, cost):
        self.db[self._db_index(pebble_positions)] = cost if cost > 0 else self.ZERO_COST

    def db_file_path(self):
        return os.path.join(self.db_folder_path, f"subproblem_{self.pebbles}.pkl")

    def pre_calculate_db(self):
        init_node = self.PreCalculationNode(PartialBoard(self.pebbles))
        open_nodes = FastLookupQueue()
        open_nodes.push_right(init_node)

        while len(open_nodes) > 0:
            expansion_open_nodes = FastLookupQueue()
            expansion_open_nodes.push_right(open_nodes.pop_left())

            while len(expansion_open_nodes) > 0:
                node = expansion_open_nodes.pop_left()
                self.save_cost(node.board.pebble_positions_subset(self.pebbles), node.cost)

                for direction in node.board.valid_directions():
                    child_board = copy.deepcopy(node.board)
                    moved_pebble = child_board.move_blank(direction)
                    child_node = self.PreCalculationNode(child_board, node.cost)
                    if (child_node not in expansion_open_nodes) \
                            and (child_node not in open_nodes) \
                            and (not self.has_cost(child_node.board.pebble_positions_subset(self.pebbles))):
                        if moved_pebble not in self.pebbles:
                            expansion_open_nodes.push_right(child_node)
                        elif child_node not in open_nodes:
                            child_node.cost = child_node.cost + 1
                            open_nodes.push_right(child_node)

        with open(self.db_file_path(), 'wb') as f:
            pickle.dump(self, f)

    class PreCalculationNode(Node):
        def __init__(self, board, cost=0):
            super().__init__(board)
            self.cost = cost


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
    ]
}


class PatternDatabaseHeuristic(Heuristic):
    def __init__(self, max_pattern_size):
        self.max_pattern_size = max_pattern_size
        self.subproblems = [Subproblem(pebbles) for pebbles in _pattern_definitions[max_pattern_size]]

    def estimate_cost(self, board):
        return sum([subproblem.cost(board.pebble_positions_subset(subproblem.pebbles)) for subproblem in self.subproblems])

    def _default_folder(self):
        subproblem_lengths = [len(subproblem.pebbles) for subproblem in self.subproblems]
        subfolder_name = f"patterns-maxlen-{max(subproblem_lengths)}"
        return os.path.join(PATTERN_DATABASE_FOLDER, subfolder_name)

    def pre_calculate_db(self, n_processes=4, folder_path=None):
        if folder_path is None:
            folder_path = self._default_folder()
        try:
            os.mkdir(folder_path)
        except FileExistsError:
            pass

        for subproblem in self.subproblems:
            subproblem.db_folder_path = folder_path

        debug_print("Database precalculation started.")

        pool = multiprocessing.Pool(n_processes)
        pool.map(self._precalculation_worker, self.subproblems)

        debug_print("Database precalculation complete.")

    def load_db(self, folder_path=None):
        if folder_path is None:
            folder_path = self._default_folder()

        debug_print("Database loading from disk.")

        for i, subproblem in enumerate(self.subproblems):
            subproblem.db_folder_path = folder_path
            with open(subproblem.db_file_path(), 'rb') as f:
                a = pickle.load(f)
                self.subproblems[i] = a

        debug_print("Database loaded.")

    def _precalculation_worker(self, subproblem):
        subproblem.pre_calculate_db()
        debug_print(f"Subproblem {subproblem.pebbles}: done.")
        return subproblem

    def name(self):
        return f"PDB[Pat:{self.max_pattern_size}]"
