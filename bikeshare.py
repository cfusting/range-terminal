import pandas as pd

from sklearn.model_selection import train_test_split


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
train, test = train_test_split(dat_train_ordered, test_size=.2, shuffle=False)
print("train: " + str(len(train)) + ", test: " + str(len(test)))
store = pd.HDFStore('data/bike_convolution.hdf5')
store['train'] = train
store['test'] = test
