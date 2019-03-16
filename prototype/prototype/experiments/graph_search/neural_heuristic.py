from heuristics.neural_network import NeuralNetworkHeuristic
from heuristics.pattern_database import PatternDatabaseHeuristic
from experiments.solving_experiment import SolvingExperiment
from graph_search.algorithms.a_star_search import AStarSearch
from graph_search.algorithms.ida_star_search import IDAStarSearch
import keras

algorithms = list()
algorithms.append(AStarSearch())
algorithms.append(IDAStarSearch())

heuristics = list()

# pdb = PatternDatabaseHeuristic(4)
# pdb.pre_calculate_db()
# pdb.load_db()
# heuristics.append(pdb)

model = keras.models.load_model('../../../../data/keras-1024-1024-512-128-64.h5')
heuristics.append(NeuralNetworkHeuristic(model, additive_constant=0))

experiment = SolvingExperiment(algorithms, heuristics, 10)
experiment.start()
