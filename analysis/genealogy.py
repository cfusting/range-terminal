import numpy as np
import matplotlib.pyplot as plt

from fastsr.estimators.symbolic_regression import SymbolicRegression
from fastsr.containers.learning_data import LearningData
from fastsr.experiments.truncation_elite import TruncationElite
from experiments.truncation_elite_rt import TruncationEliteRT
import utils

best_num = 0
experiment_class, experiment_name = utils.get_experiment_class_and_name(TruncationEliteRT)
model = SymbolicRegression()
model.load('/home/cfusting/rtresults_1000_100/energy_lagged/' + experiment_name + '/saved_models/' +
           experiment_name + '_energy_lagged_3965.pkl')

training_data = LearningData()
#training_data.from_file('data/minimum.csv')
training_data.from_hdf('data/energy_lagged.hdf5')
experiment = experiment_class()
pset = experiment.get_pset(training_data.num_variables, training_data.variable_type_indices,
                           training_data.variable_names, training_data.variable_dict)
scoring_toolbox = experiment.get_scoring_toolbox(training_data.predictors, training_data.response, pset)
best_individuals = []
for individual in model.best_individuals_:
    if hasattr(individual, 'history_index'):
        best_individuals.append(individual)
best_genealogy = model.history_.getGenealogy(best_individuals[best_num])
errors = []


def populate_individuals(history_index):
    generation = 1
    stack = []
    stack.append(history_index)
    while len(stack) > 0:
        history_index = stack.pop()
        ind = model.history_.genealogy_history[history_index]
        if not hasattr(ind, 'visited'):
            ind.visited = True
            ind.error = scoring_toolbox.score(ind)[0]
            ind.generation = generation
            generation += 1
            errors.append(ind.error)
            parents = best_genealogy[history_index]
            if len(parents) > 0:
                stack.append(parents[0])
            if len(parents) > 1:
                stack.append(parents[1])
        else:
            print('Loopback found to node: ' + str(history_index))

keys = best_genealogy.keys()
populate_individuals(max(keys))
for i in best_genealogy:
    print(str(i), str(best_genealogy[i]))
dupes = (len(keys) != len(set(keys)))
print('duplicates: ' + str(dupes))


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
plt.savefig('/home/cfusting/Desktop/' + experiment_name + '_genealogy.png', figsize=(10, 10), dpi=200)

with open('/home/cfusting/Desktop/' + experiment_name + '_genealogy.txt', 'w') as f:
    f.write(str(best_genealogy) + '\n')
    f.write('----------------------' + '\n')
    for k, v in best_genealogy.items():
        offspring = model.history_.genealogy_history[k]
        f.write(str(offspring.generation) + '| Offspring ' + str(k) + ', Score: ' + str(offspring.error) +
                ': ' + str(offspring) + '\n')
        if len(v) > 0:
            parent1 = model.history_.genealogy_history[v[0]]
            f.write(str(parent1.generation) + '| Parent ' + str(v[0]) + ', Score: ' + str(parent1.error) +
                    ': ' + str(parent1) + '\n')
        if len(v) > 1:
            parent2 = model.history_.genealogy_history[v[1]]
            f.write(str(parent2.generation) + '| Parent ' + str(v[1]) + ', Score: ' + str(parent2.error) +
                    ': ' + str(parent2) + '\n')
        f.write('----------------------' + '\n')
