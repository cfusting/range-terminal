from fastgp.parametrized import simple_parametrized_terminals as sp
from fastgp.utilities import metrics

from fastsr.experiments.truncation_elite import TruncationElite

NAME = 'TruncationEliteRTNOMUT'


class TruncationEliteRTNOMUT(TruncationElite):

    def __init__(self,
                 ngen=50,
                 pop_size=10,
                 tournament_size=2,
                 min_depth_init=1,
                 max_dept_init=6,
                 max_height=17,
                 max_size=200,
                 crossover_probability=0.9,
                 mutation_probability=0.1,
                 internal_node_selection_bias=0.9,
                 min_gen_grow=1,
                 max_gen_grow=6,
                 subset_proportion=1,
                 subset_change_frequency=10,
                 error_function=metrics.mean_squared_error,
                 num_randoms=1):
        super(TruncationEliteRTNOMUT, self).__init__(ngen,
                                                     pop_size,
                                                     tournament_size,
                                                     min_depth_init,
                                                     max_dept_init,
                                                     max_height,
                                                     max_size,
                                                     crossover_probability,
                                                     mutation_probability,
                                                     internal_node_selection_bias,
                                                     min_gen_grow,
                                                     max_gen_grow,
                                                     subset_proportion,
                                                     subset_change_frequency,
                                                     error_function,
                                                     num_randoms)

    def get_toolbox(self, predictors, response, pset, variable_type_indices, variable_names, test_predictors=None,
                    test_response=None):
        toolbox = super(TruncationEliteRTNOMUT, self).get_toolbox(predictors, response, pset, variable_type_indices,
                                                                  variable_names)
        return toolbox

    def get_pset(self, num_predictors, variable_type_indices, names, variable_dict):
        pset = super(TruncationEliteRTNOMUT, self).get_pset(num_predictors, variable_type_indices, names, variable_dict)
        for i in range(60):
            pset.add_parametrized_terminal(sp.RangeOperationTerminal)
        for i in range(60):
            pset.add_parametrized_terminal(sp.MomentFindingTerminal)
        return pset
