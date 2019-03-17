#!/bin/bash

for run in {1..2}; do
    (../cmake-build-debug/fifteen_puzzle_solver) &
    sleep 1
done
