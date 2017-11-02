import numpy as np
import pandas as pd

index_names = [x for x in range(100)]
column_names = ['x' + str(x) for x in range(50)] + ['y']
features = np.random.randn(100, 50) * 100
response = features.min(axis=1).reshape((100, 1))
dat = np.concatenate([features, response], axis=1)
df = pd.DataFrame(dat, index=index_names, columns=column_names)
df.to_csv('data/minimum.csv', index=False)
