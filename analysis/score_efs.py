import pickle
import re
from os.path import isfile, join
from os import listdir
from itertools import chain

from sklearn.model_selection import train_test_split

import numpy as np

from fastsr.containers.learning_data import LearningData

from fastgp.algorithms.evolutionary_feature_synthesis import get_basis_from_infix_features, Feature
from fastgp.utilities.metrics import mean_squared_error

experiment = 'rt'
dataset = 'energy_lagged'
path = '/'.join([dataset, experiment])
models_dir = '/home/cfusting/efsresults/' + path + '/saved_models/'
results_dir = '/home/cfusting/efsscores/' + path


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
all_features = {}
print('Processing seeds for ' + experiment)
for fl in files:
    with open(models_dir + '/' + fl, 'rb') as f:
        data = pickle.load(f)
    seed = get_seed(fl)
    print('Processing seed: ' + str(seed))
    statistics = data[0]
    best_models = data[1]
    best_features = data[2]
    best_scalers = data[3]
    best_validation_scores = data[4]
    data_length = len(best_models)
    print('Data length: ' + str(data_length))
    if data_length != len(best_features) or data_length != len(best_scalers):
        print('Inconsistent data.')
    # model_index = len(best_models) - 1
    model_index = len(best_models) - 1
    if model_index >= data_length:
        print('Using best model.')
        model_index = len(best_models) - 1
    for i, coef in enumerate(best_models[model_index].coef_):
        best_features[model_index][i].coef = coef
    for f in best_features[model_index]:
        if f.string in all_features:
            all_features[f.string].append(f)
        else:
            all_features[f.string] = [f]
    infixes = list(map(lambda x: x.infix_string, best_features[model_index]))
    test_basis = get_basis_from_infix_features(infixes, training_data.variable_names, X_test,
                                               best_scalers[model_index],
                                               training_data.variable_type_indices)
    test_predictions = best_models[model_index].predict(test_basis)
    score = mean_squared_error(test_predictions, y_test)[0]
    scores[seed] = [best_validation_scores[model_index], score]
    print('Score on test data for seed ' + str(seed) + ': ' + str(score))
    print('----------------------------------------------------------------')

for k in all_features.keys():
    fitness = np.mean(list(map(lambda x: x.fitness, all_features[k])))
    coef = np.mean(list(map(lambda x: x.coef, all_features[k])))
    feature = Feature(None, k, k, fitness=fitness, size=all_features[k][0].size)
    feature.coef = coef
    all_features[k] = feature

vals = []
tests = []
for score in list(scores.values()):
    vals.append(score[0])
    tests.append(score[1])
print('Average score on validation data: ' + str(np.mean(vals)))
print('Average score on test data: ' + str(np.mean(tests)))

with open(results_dir + '/scores.txt', 'w') as results:
    header = 'seed' + ',' + 'validation_score' + ',' + 'test_score'
    results.write(header)
    results.write('\n')
    for seed in scores.keys():
        scr = scores[seed]
        results.write(str(seed) + ',' + str(scr[0]) + ',' + str(scr[1]))
        results.write('\n')

final_features = list(all_features.values())
final_features.sort(reverse=True, key=lambda x: x.fitness)
with open(results_dir + '/features.txt', 'w') as results:
    header = 'fitness' + ',' + 'coef' + ',' + 'feature'
    results.write(header)
    results.write('\n')
    for f in final_features:
        results.write(str(f.fitness) + ',' + str(f.coef) + ',' + f.string)
        results.write('\n')

