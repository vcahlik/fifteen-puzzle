# Fifteen Puzzle

This repository contains code that we used for experimenting with using artificial neural networks as a heuristic for solving the [15 puzzle](https://en.wikipedia.org/wiki/15_puzzle), which we presented in the following scientific papers:
* [On the Design of a Heuristic based on Artificial Neural Networks for the Near Optimal Solving of the (N2-1)-puzzle](https://doi.org/10.5220/0008163104730478)
* [Near Optimal Solving of the (N2-1)-puzzle Using Heuristics Based on Artificial Neural Networks](https://doi.org/10.1007/978-3-030-70594-7_12)

## Dataset

Using the code in this repository we have collected a dataset ([link](https://drive.google.com/file/d/1sAhDL847ku-mo3C-LyMCb5-QYdAta8HQ/view?usp=sharing)) of **optimal** solution lengths to 6 million instances of 15 puzzle obtained via random permutations. Here are the first lines of the dataset (CSV format):

    0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,cost
    10,1,5,4,14,11,15,7,0,9,3,2,6,8,12,13,48
    1,7,12,2,5,0,6,3,9,8,14,4,13,11,10,15,26
    6,9,4,1,13,0,12,10,7,5,11,14,3,15,8,2,54
    15,5,0,6,9,4,8,11,10,13,2,1,12,3,14,7,54
    6,7,12,4,0,15,11,3,13,10,1,5,9,14,8,2,53
    ...
    (6M total instances)

The first row is the header row. Pebbles are numbered from 1 to 15, pebble 0 represents an empty position. Positions are indexed from left to right, top to bottom, starting at 0. The first column, *0*, represents the number of the pebble at position 0. An equivalent rule holds for columns *1* to *15*. The final column, *cost*, represents the optimal (lowest) number of moves in which the puzzle instance can be solved.

For example, the row:

    10,1,5,4,14,11,15,7,0,9,3,2,6,8,12,13,48

means that the instance

    +----+----+----+----+
    | 10 |  1 |  5 |  4 |
    +----+----+----+----+
    | 14 | 11 | 15 |  7 |
    +----+----+----+----+
    |    |  9 |  3 |  2 |
    +----+----+----+----+
    |  6 |  8 | 12 | 13 |
    +----+----+----+----+

can optimally be solved in **48 moves**.

The row:

    1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0,0

would represent the solved puzzle:

    +----+----+----+----+
    |  1 |  2 |  3 |  4 |
    +----+----+----+----+
    |  5 |  6 |  7 |  8 |
    +----+----+----+----+
    |  9 | 10 | 11 | 12 |
    +----+----+----+----+
    | 13 | 14 | 15 |    |
    +----+----+----+----+

The dataset was collected using IDA* with the 7-8 pattern database heuristic. The CSV (235 MB) can be downloaded [from here](https://drive.google.com/file/d/1sAhDL847ku-mo3C-LyMCb5-QYdAta8HQ/view?usp=sharing).

## Repository structure

* *prototype* - Python code with solver that uses the ANN-distance heuristic, and additional Jupyter notebooks with experiments
* *evaluation* - C++ app for compute-efficient implementations of algorithms (currently only used for generating the optimal cost datasets)
* *utils* - Utilities for working with datasets
* *data* - Directory for storing data (must be created manually)

## How to run

### Python section (solver with the ANN-distance heuristic + experiment notebooks)

1. Set the current `PROJECT_ROOT` in prototype/constants.py
2. Create the [conda](https://github.com/conda/conda) environment using the *environment-cpu.yml* or *environment-gpu.yml* file (use the latter if you have a CUDA compatible GPU)
3. Activate the conda environment
4. Choose a module and run it with python -m MODULE_NAME (for example, python -m prototype.experiments.random_boards_distribution)

### C++ section (generating datasets with optimal costs)

1. Enter the *evaluation* directory: `cd evaluation`
2. Create a build directory and enter it: `mkdir build && cd build`
3. Run cmake (with the project root directory as argument): `cmake ..`
4. Build the project: `make`
5. Run the program: `./fifteen_puzzle_solver` (this currently only runs the dataset generator, which requires additional pattern database files **TODO**)

## Citing

In case you find this repository or dataset helpful, feel free to cite our related publication [Near Optimal Solving of the (N2-1)-puzzle Using Heuristics Based on Artificial Neural Networks](https://doi.org/10.1007/978-3-030-70594-7_12):

    @inbook{Cahlik2021,
        title        = {Near Optimal Solving of the (N2-1)-puzzle Using Heuristics Based on Artificial Neural Networks},
        author       = {Cahlik, Vojtech and Surynek, Pavel},
        year         = 2021,
        booktitle    = {Computational Intelligence: 11th International Joint Conference, IJCCI 2019, Vienna, Austria, September 17--19, 2019, Revised Selected Papers},
        publisher    = {Springer International Publishing},
        address      = {Cham},
        pages        = {291--312},
        doi          = {10.1007/978-3-030-70594-7_12},
        isbn         = {978-3-030-70594-7},
        url          = {https://doi.org/10.1007/978-3-030-70594-7_12}
    }
