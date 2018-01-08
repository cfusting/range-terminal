import argparse
import re
from os import listdir
from os.path import isfile, join

from fastsr.estimators.symbolic_regression import SymbolicRegression
from fastsr.containers.learning_data import LearningData

from sklearn.model_selection import train_test_split

parser = argparse.ArgumentParser(description='Score models.')
parser.add_argument('-d', '--data', help='Path to training data.', required=True)
parser.add_argument('-m', '--models', help='Path to models save folder.', required=True)
parser.add_argument('-r', '--results', help='Path to results directory.', required=True)
args = parser.parse_args()


def get_seed(file):
    pattern = re.compile('\d+')
    match = pattern.search(file)
    return match.group(0)


def get_ident(file):
    pattern = re.compile('(.+)_\d')
    match = pattern.search(file)
    return match.group(1)

ENSEMBLE_SIZES = [1, 5, 10, 20, 50]
files = [f for f in listdir(args.models) if isfile(join(args.models, f))]
files = [f for f in files if 'parameter' not in f]
training_data = LearningData()
training_data.from_file(args.data)
X_train, X_test, y_train, y_test = train_test_split(training_data.predictors, training_data.response,
                                                    test_size=0.2, shuffle=False)
with open(args.results + '/' + get_ident(files[0]) + '.csv', 'w') as results:
    header = 'Seed' + ',' + ','.join(['Ensemble' + str(x) for x in ENSEMBLE_SIZES])
    results.write(header)
    results.write('\n')
    for f in files:
        seed = get_seed(f)
        model = SymbolicRegression()
        model.load(args.models + '/' + f)
        test_errors = []
        for s in ENSEMBLE_SIZES:
            model.ensemble_size = s
            test_errors.append(str(model.score(X_test, y_test)))
        line = seed + ',' + ','.join(test_errors)
        results.write(line)
        results.write('\n')
