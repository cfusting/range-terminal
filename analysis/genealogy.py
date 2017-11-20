import numpy as np
import matplotlib.pyplot as plt

from fastsr.estimators.symbolic_regression import SymbolicRegression
from fastsr.experiments.control import Control
from fastsr.containers.learning_data import LearningData

from experiments.range_terminal import RT
import utils

best_num = 0
experiment_class, experiment_name = utils.get_experiment_class_and_name(RT)
model = SymbolicRegression()
model.load('saved_models/' + experiment_name + '_hour_simple_lagged_2017')

training_data = LearningData()
# training_data.from_file('data/minimum.csv')
training_data.from_hdf('data/hour_simple_lagged.hdf5')
experiment = experiment_class()
pset = experiment.get_pset(training_data.num_variables, training_data.variable_type_indices,
                           training_data.variable_names, training_data.variable_dict)
scoring_toolbox = experiment.get_scoring_toolbox(training_data.predictors, training_data.response, pset)
best_individuals = []
for individual in model.best_individuals_:
    if hasattr(individual, 'history_index'):
        best_individuals.append(individual)
best_genealogy = model.history_.getGenealogy(best_individuals[best_num])
maxgen = 0
maxerror = 0
errors = []


def populate_individuals(history_index, generation):
    global maxgen
    global maxerror
    ind = model.history_.genealogy_history[history_index]
    ind.error = scoring_toolbox.score(ind)[0]
    ind.generation = generation
    errors.append(ind.error)
    if ind.error > maxerror:
        maxerror = ind.error
    parents = best_genealogy[history_index]
    if len(parents) > 0:
        populate_individuals(parents[0], generation + 1)
    if len(parents) > 1:
        populate_individuals(parents[1], generation + 1)

for k in best_genealogy.keys():
    populate_individuals(k, 1)
    break


def safe_log(x):
    if x == 0:
        return x
    return np.log(x)


median_error = np.median(errors)
for k, v in best_genealogy.items():
    xpoints = []
    ypoints = []

    def condition(y, median):
        return y > 1.5 * safe_log(median)
    offspring = model.history_.genealogy_history[k]
    x1 = offspring.generation
    y1 = safe_log(offspring.error)
    if condition(y1, median_error):
        continue
    xpoints.append(x1)
    ypoints.append(y1)
    if len(v) > 0:
        parent1 = model.history_.genealogy_history[v[0]]
        x2 = parent1.generation
        y2 = safe_log(parent1.error)
        if condition(y2, median_error):
            continue
        xpoints.append(x2)
        ypoints.append(y2)
        # print('Connecting: (' + str(x1) + ' ,' + str(y1) + ') - (' + str(x2) + ' ,' + str(y2) + ')')
    if len(v) > 1:
        parent2 = model.history_.genealogy_history[v[1]]
        x3 = parent2.generation
        y3 = safe_log(parent2.error)
        if condition(y3, median_error):
            continue
        xpoints.extend([xpoints[0], x3, xpoints[0], x3, xpoints[1], x3])
        ypoints.extend([ypoints[0], y3, ypoints[0], y3, ypoints[1], y3])
        # print('Connecting: (' + str(x1) + ' ,' + str(y1) + ') - (' + str(x2) + ' ,' + str(y2) + ')')
    plt.plot(xpoints, ypoints, marker='o')
plt.savefig('results/' + experiment_name + '_genealogy.png', figsize=(10, 10), dpi=200)

with open('results/' + experiment_name + '_genealogy.txt', 'w') as f:
    f.write(str(best_genealogy) + '\n')
    f.write('----------------------' + '\n')
    for k, v in best_genealogy.items():
        offspring = model.history_.genealogy_history[k]
        f.write(str(offspring.generation) + '| Offspring ' + str(k) + ', Score: ' + str(safe_log(offspring.error)) +
                ': ' + str(offspring) + '\n')
        if len(v) > 0:
            parent1 = model.history_.genealogy_history[v[0]]
            f.write(str(parent1.generation) + '| Parent ' + str(v[0]) + ', Score: ' + str(safe_log(parent1.error)) +
                    ': ' + str(parent1) + '\n')
        if len(v) > 1:
            parent2 = model.history_.genealogy_history[v[1]]
            f.write(str(parent2.generation) + '| Parent ' + str(v[1]) + ', Score: ' + str(safe_log(parent2.error)) +
                    ': ' + str(parent2) + '\n')
        f.write('----------------------' + '\n')
