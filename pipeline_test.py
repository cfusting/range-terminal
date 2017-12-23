from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split

from fastsr.estimators.symbolic_regression import SymbolicRegression
from fastsr.containers.learning_data import LearningData

estimators = [('reduce_dim', PCA()), ('symbolic_regression', SymbolicRegression())]
pipe = Pipeline(estimators)

training_data = LearningData()
training_data.from_file('data/hour_simple_lagged.hdf5')
X_train, X_test, y_train, y_test = train_test_split(training_data.predictors, training_data.response, test_size=0.1,
                                                    shuffle=False)

pipe.fit(X_train, y_train)
print(pipe.score(X_train, y_train))

model = SymbolicRegression()
model.fit(X_train, y_train)
print(model.score(X_train, y_train))
