import numpy as np
import pandas as pd

NUM_OBS = 10000
index_names = [x for x in range(NUM_OBS)]
column_names = ['x' + str(x) for x in range(50)] + ['y']
features = np.random.randn(NUM_OBS, 50) * 100
response = features.min(axis=1).reshape((NUM_OBS, 1))
dat = np.concatenate([features, response], axis=1)
df = pd.DataFrame(dat, index=index_names, columns=column_names)
df.to_csv('data/minimum.csv', index=False)
