import pandas as pd

from fastsr.containers.learning_data import LearningData

dat = pd.read_csv('data/hour.csv')
datetime_index = list()
for i, r in dat.iterrows():
    datetime_index.append(pd.to_datetime(r[1]) + pd.DateOffset(hours=r[5]))
dt_index = pd.DatetimeIndex(datetime_index)
dat.set_index(dt_index)
columns = ['atemp', 'windspeed', 'hum', 'cnt']
slim_dat = dat[columns]
learning_data = LearningData()
learning_data.from_data(slim_dat, columns, 'ucisimplebike')
learning_data.lag_predictors(24, column_names=['atemp', 'windspeed', 'hum'])
learning_data.to_hdf('data/hour_simple_lagged.hdf5')
