import argparse

import numpy as np

from sklearn.model_selection import train_test_split

from fastgp.logging.reports import save_log_to_csv

from fastsr.experiments.control import Control
from fastsr.estimators.symbolic_regression import SymbolicRegression
from fastsr.containers.learning_data import LearningData

from experiments.range_terminal import RT
from experiments.range_terminal_no_mutation import RTNOMUT
import utils

parser = argparse.ArgumentParser(description='Run symbolic regression.')
parser.add_argument('-d', '--data', help='Path to training data.', required=True)
parser.add_argument('-e', '--experiment', help='Experiment name.', required=True)
parser.add_argument('-m', '--model', help='Path to model save folder.', required=True)
parser.add_argument('-o', '--output', help='Path to scoring folder.', required=True)
parser.add_argument('-l', '--logs', help='Path to logging folder.', required=True)
parser.add_argument('-s', '--seed', help='Random seed.', type=int)
args = parser.parse_args()

if args.experiment == 'Control':
    experiment_class, experiment_name = utils.get_experiment_class_and_name(Control)
elif args.experiment == 'RT':
    experiment_class, experiment_name = utils.get_experiment_class_and_name(RT)
else:
    experiment_class, experiment_name = utils.get_experiment_class_and_name(RTNOMUT)
training_data = LearningData()
training_data.from_file(args.data)
X_train, X_test, y_train, y_test = train_test_split(training_data.predictors, training_data.response, test_size=0.2,
                                                    shuffle=False)
print('Training examples: ' + str(X_train.shape[0]))
print('Testing examples: ' + str(X_test.shape[0]))
model = SymbolicRegression(experiment_class=experiment_class,
                           variable_type_indices=training_data.variable_type_indices,
                           variable_names=training_data.variable_names,
                           variable_dict=training_data.variable_dict,
                           num_features=training_data.num_variables,
                           pop_size=100,
                           ngen=1000,
                           crossover_probability=.5,
                           mutation_probability=.5,
                           subset_proportion=.7,
                           ensemble_size=1,
                           seed=args.seed)
model.fit(X_train, y_train)
validation_error = model.score(X_train, y_train)
test_error = model.score(X_test, y_test)
print('Model validation error: ' + str(validation_error))
print('Model test error: ' + str(test_error))
ident = experiment_name + '_' + training_data.name + '_'
model.save(args.model + '/' + ident + '_' + str(args.seed))
if args.output:
    with open(args.output + '/' + ident + '_validation.txt', 'a') as f:
        f.write(str(validation_error) + '\n')
    with open(args.output + '/' + ident + '_test.txt', 'a') as f:
        f.write(str(test_error) + '\n')
    save_log_to_csv(model.logbook_, args.logs + '/' + ident + '_' + str(args.seed))
