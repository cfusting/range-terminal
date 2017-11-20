import argparse

import pandas as pd

parser = argparse.ArgumentParser(description='Run symbolic regression.')
parser.add_argument('-f', '--file', help='Path to file.', required=True)
args = parser.parse_args()

dat = pd.read_csv(args.file, header=None)
print(dat.describe())
print(dat.median())
