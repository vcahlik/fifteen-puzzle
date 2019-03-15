from heuristics import NeuralNetworkHeuristic
from heuristics import PatternDatabaseHeuristic
import keras

heuristics = list()

pdb = PatternDatabaseHeuristic(4)
# pdb.pre_calculate_db()
pdb.load_db()
heuristics.append(pdb)

# model = keras.models.load_model('../../../../data/keras-1024-1024-512-128-64.h5')
# heuristics.append(NeuralNetworkHeuristic(model, custom_name="Neural"))

model = keras.models.load_model('../../../../data/keras-1024-1024-512-128-64.h5')
heuristics.append(NeuralNetworkHeuristic(model, additive_constant=0, custom_name="Neural, shift -2"))

experiment(50, heuristics)
