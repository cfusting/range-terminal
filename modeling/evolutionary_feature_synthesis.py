import pickle
import argparse

from sklearn.model_selection import train_test_split

from fastsr.containers.learning_data import LearningData

from fastgp.algorithms.evolutionary_feature_synthesis import optimize

parser = argparse.ArgumentParser(description='Run symbolic regression.')
parser.add_argument('-d', '--data', help='Path to training data.', required=True)
parser.add_argument('-e', '--experiment', help='Experiment name.', required=True)
parser.add_argument('-m', '--model', help='Path to model save folder.', required=True)
parser.add_argument('-r', '--range-operators', help='Include Range Operators', required=True, default=False)
parser.add_argument('-s', '--seed', help='Random seed.', type=int)
args = parser.parse_args()

training_data = LearningData()
training_data.from_file(args.data)
range_operators = 0
if args.range_operators:
    range_operators = 100
X_train, X_test, y_train, y_test = train_test_split(training_data.predictors, training_data.response, test_size=0.2,
                                                    shuffle=False)
statistics, best_models, best_features = optimize(X_train, y_train, args.seed, fitness_algorithm='coefficient_rank',
                                                  max_gens=2, fitness_threshold=.01, num_additions=300,
                                                  preserve_originals=True, feature_names=training_data.variable_names,
                                                  range_operators=range_operators,
                                                  reinit_range_operators=3,
                                                  variable_type_indices=training_data.variable_type_indices,
                                                  verbose=True)
data = [statistics, best_models, best_features]
with open(args.model + '/' + args.seed, 'wb') as f:
    pickle.dump(data, f)
