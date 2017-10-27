from fastsr.experiments.control import Control
from fastsr.estimators.symbolic_regression import SymbolicRegression
from fastsr.data.learning_data import LearningData

from experiments.range_terminal import RT
import utils

experiment_class, experiment_name = utils.get_experiment_class_and_name(Control)
training_data = LearningData()
training_data.from_file('data/minimum.csv')
model = SymbolicRegression(experiment_class=experiment_class,
                           variable_type_indices=training_data.variable_type_indices,
                           variable_names=training_data.variable_names,
                           variable_dict=training_data.variable_dict,
                           num_features=training_data.num_variables,
                           pop_size=200,
                           ngen=1000,
                           crossover_probability=.5,
                           mutation_probability=.5)
model.fit(training_data.predictors, training_data.response)
print('Model score: ' + str(model.score(training_data.predictors, training_data.response)))
model.save('models/' + str(experiment_name))
