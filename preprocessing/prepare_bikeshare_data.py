import pandas as pd


from fastsr.data.learning_data import LearningData


dat = pd.read_csv('data/hour.csv')
datetime_index = list()
for i, r in dat.iterrows():
    datetime_index.append(pd.to_datetime(r[1]) + pd.DateOffset(hours=r[5]))
dt_index = pd.DatetimeIndex(datetime_index)
dat.set_index(dt_index)
dat_onehot = pd.get_dummies(dat, prefix_sep='', columns=['season', 'mnth', 'hr', 'weekday', 'weathersit'])
indices = [x for x in range(2, 9)] + [11] + [x for x in range(12, 63)]
dat_train = dat_onehot.iloc[:, indices]
cols = dat_train.columns.tolist()
cols_ordered = cols[0:7] + cols[8:58] + [cols[7]]
dat_train_ordered = dat_train[cols_ordered]
learning_data = LearningData()
learning_data.from_data(dat_train_ordered, cols_ordered[:-1], 'ucibike')
lag_variables = ['holiday', 'workingday', 'temp', 'atemp', 'hum', 'windspeed']
learning_data.lag_predictors(6, column_names=lag_variables)
learning_data.to_hdf('data/hour_lagged.hdf5')
