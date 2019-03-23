#!/usr/bin/env python3
import pandas as pd
import os
import glob
import sys


OUTPUT_FILE_NAME = "solutions-2019-02-07T23:42:31.961-merged.csv"
SOURCE_DIR = "datasets-raw/2019-02-07T23:42:31.961"
OUTPUT_DIR = "datasets-output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, OUTPUT_FILE_NAME)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    
if os.path.exists(OUTPUT_FILE):
    raise RuntimeError(f"Error: File {OUTPUT_FILE} already exists.")

print("Concat: started.")

file_names = list(glob.glob(SOURCE_DIR + "/*.csv"))
col_names = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "cost"]

merged = pd.read_csv(file_names[0], header=None, names=col_names)
for file_name in file_names[1:]:
    df = pd.read_csv(file_name, header=None, names=col_names)
    merged = merged.append(df, sort=False)
    print(f"Concat: appended {df.shape[0]} rows.")

print(f"Concat: {merged.shape[0]} total rows.")
print("Concat: done.")

print("Drop duplicates: started.")

n_total = merged.shape[0]
merged.drop_duplicates(inplace=True)
n_unique = merged.shape[0]
n_duplicates = n_total - n_unique

print(f"Drop duplicates: {n_duplicates} dropped, {n_unique} left.")
print("Drop duplicates: done.")

print("Write to CSV: started.")

merged.to_csv(OUTPUT_FILE, index=False)

print("Write to CSV: done.")
print(f"Finished.")
