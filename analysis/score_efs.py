import pickle
import re
from os.path import isfile, join
from os import listdir

from sklearn.model_selection import train_test_split

from fastsr.containers.learning_data import LearningData

from fastgp.algorithms.evolutionary_feature_synthesis import get_basis_from_infix_features
from fastgp.utilities.metrics import mean_squared_error

experiment = 'control'
models_dir = '/home/cfusting/efsresults/' + experiment
results_dir = '/home/cfusting/efsscores'


def get_seed(file):
    pattern = re.compile('\d+')
    match = pattern.search(file)
    return match.group(0)


training_data = LearningData()
training_data.from_file('/home/cfusting/bunny/range-terminal/data/energy_lagged.hdf5')
X_train, X_test, y_train, y_test = train_test_split(training_data.predictors, training_data.response, test_size=0.2,
                                                    shuffle=False)
files = [f for f in listdir(models_dir) if isfile(join(models_dir, f))]
scores = {}
all_features = []
for fl in files:
    with open('e', 'rb') as f:
        data = pickle.load(f)
    statistics = data[0]
    best_models = data[1]
    best_features = data[2]
    all_features.extend(best_features)
    infixes = list(map(lambda x: x.infix_string, best_features[len(best_features) - 1]))
    test_basis = get_basis_from_infix_features(infixes, training_data.variable_names, X_test,
                                               training_data.variable_type_indices)
    test_predictions = best_models[len(best_models) - 1].predict(test_basis)
    score = mean_squared_error(test_predictions, y_test)[0]
    seed = get_seed(fl)
    scores[seed] = score
    print('Score on test data for seed ' + str(seed) + ': ' + str(score))

with open(results_dir + '/' + experiment + '_scores.txt', 'w') as results:
    header = 'seed' + ',' + 'score'
    results.write(header)
    results.write('\n')
    for seed in scores.keys():
        results.write(seed + ',' + scores[seed])
        results.write('\n')

all_features.sort(reverse=True, key=lambda x: x.fitness)
with open(results_dir + '/' + experiment + '_features.txt', 'w') as results:
    header = 'fitness' + ',' + 'feature'
    results.write(header)
    results.write('\n')
    for f in all_features:
        results.write(f.fitness + ',' + f.string)
        results.write('\n')

