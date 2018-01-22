import pandas as pd

from fastsr.containers.learning_data import LearningData

dat = pd.read_csv('data/energydata_complete.csv')
cols = dat.columns.tolist()
cols_ordered = cols[3:len(cols)] + [cols[1]]
trimmed_dat = dat[cols_ordered]
learning_data = LearningData()
predictor_names = cols_ordered[:-1]
# We need to remove '_' as they don't play nice with Range Terminals
predictor_names = list(map(lambda x: x.replace('_', ''), predictor_names))
learning_data.from_data(trimmed_dat, predictor_names, 'energy_data')
learning_data.lag_predictors(24, column_names=predictor_names)
learning_data.to_hdf('data/energy_lagged.hdf5')
