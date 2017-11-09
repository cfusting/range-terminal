import argparse

import numpy as np

from sklearn.model_selection import train_test_split

from fastsr.experiments.control import Control
from fastsr.estimators.symbolic_regression import SymbolicRegression
from fastsr.containers.learning_data import LearningData

from experiments.range_terminal import RT
import utils

parser = argparse.ArgumentParser(description='Run symbolic regression.')
parser.add_argument('-d', '--data', help='Path to training data.', required=True)
parser.add_argument('-e', '--experiment', help='Experiment name.', required=True)
parser.add_argument('-m', '--model', help='Path to model save folder.', required=True)
parser.add_argument('-o', '--output', help='Path to scoring folder.')
parser.add_argument('-s', '--seed', help='Random seed.', type=int)
args = parser.parse_args()

if args.experiment == 'Control':
    experiment_class, experiment_name = utils.get_experiment_class_and_name(Control)
else:
    experiment_class, experiment_name = utils.get_experiment_class_and_name(RT)
training_data = LearningData()
training_data.from_file(args.data)
X_train, X_test, y_train, y_test = train_test_split(training_data.predictors, training_data.response, test_size=0.1,
                                                    shuffle=False)
print('Training examples: ' + str(X_train.shape[0]))
print('Testing examples: ' + str(X_test.shape[0]))
model = SymbolicRegression(experiment_class=experiment_class,
                           variable_type_indices=training_data.variable_type_indices,
                           variable_names=training_data.variable_names,
                           variable_dict=training_data.variable_dict,
                           num_features=training_data.num_variables,
                           pop_size=10,
                           ngen=2,
                           crossover_probability=.5,
                           mutation_probability=.5,
                           subset_proportion=1,
                           ensemble_size=1,
                           seed=args.seed)
model.fit(X_train, y_train)
validation_error = np.sqrt(model.score(X_train, y_train))
test_error = np.sqrt(model.score(X_test, y_test))
print('Model validation error: ' + str(validation_error))
print('Model test error: ' + str(test_error))
model.save(args.model + '/' + experiment_name + '_' + training_data.name + '_' + str(args.seed))
if args.output:
    with open(args.output + '/' + args.experiment + '_validation.txt', 'a') as f:
        f.write(str(validation_error) + '\n')
    with open(args.output + '/' + args.experiment + '_test.txt', 'a') as f:
        f.write(str(test_error) + '\n')
