#!/usr/bin/env python3
import pandas as pd
import os
import glob
import sys


DATASET_NAME = "15-costs"
SOURCE_DIR = "../../data/datasets-raw/" + DATASET_NAME
DEST_DIR = "../../data/datasets"
DEST_FILE = DEST_DIR + "/" + DATASET_NAME + ".csv"

if os.path.exists(DEST_FILE):
    print(f"Error: File {DEST_FILE} already exists.", file=sys.stderr)
    sys.exit(1)

col_names = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "cost"]

datasets = []
for file_name in glob.glob(SOURCE_DIR + "/*.csv"):
    datasets.append(pd.read_csv(file_name, header=None, names=col_names))

merged = pd.concat(datasets, ignore_index=True)
n_merged = merged.shape[0]
merged.drop_duplicates(inplace=True)
n_duplicates = n_merged - merged.shape[0]

merged.to_csv(DEST_FILE, index=False)

print(f"Success, written: {merged.shape[0]}, dropped duplicates: {n_duplicates}")

