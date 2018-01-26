import pickle
import argparse

from sklearn.model_selection import train_test_split

from fastsr.containers.learning_data import LearningData

from fastgp.algorithms.evolutionary_feature_synthesis import optimize

parser = argparse.ArgumentParser(description='Run symbolic regression.')
parser.add_argument('-d', '--data', help='Path to training data.', required=True)
parser.add_argument('-e', '--experiment', help='Experiment name.', required=True)
parser.add_argument('-m', '--model', help='Path to model save folder.', required=True)
parser.add_argument('-r', '--range-operators', help='Include Range Operators', action='store_true',
                    default=False)
parser.add_argument('-s', '--seed', help='Random seed.', type=int)
args = parser.parse_args()

training_data = LearningData()
training_data.from_file(args.data)
num_additions = 100
num_range_operators = 20
range_operators = 0
if args.range_operators:
    range_operators = num_range_operators
else:
    # Keep things fair for the control
    num_additions += num_range_operators
X_train, X_test, y_train, y_test = train_test_split(training_data.predictors, training_data.response, test_size=0.2,
                                                    shuffle=False, random_state=args.seed)
statistics, best_models, best_features, best_scalers, best_validation_scores = \
    optimize(X_train, y_train, args.seed,
             fitness_algorithm='coefficient_rank',
             max_gens=100, fitness_threshold=0, num_additions=num_additions,
             max_useless_steps=10,
             preserve_originals=True,
             feature_names=training_data.variable_names,
             range_operators=range_operators,
             reinit_range_operators=10,
             variable_type_indices=training_data.variable_type_indices,
             time_series_cv=True,
             splits=10,
             verbose=False)
data = [statistics, best_models, best_features, best_scalers, best_validation_scores]
with open(args.model + '/' + str(args.seed), 'wb') as f:
    pickle.dump(data, f)
