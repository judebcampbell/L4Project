import numpy as np
import pandas as pd


from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from sklearn.metrics import matthews_corrcoef,  make_scorer, mean_absolute_error

from functions import *

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

import pickle


from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

mcc_scorer = make_scorer(matthews_corrcoef)

print("importing files")
file = pd.read_csv("longtraining.csv", engine="python")

print("generating features")
fileFeatures = generateFeatures(file)

print("creating target values")
y = y_values(file, fileFeatures)

print('creating model')
rfc = RandomForestClassifier(random_state=42)

n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
max_features = ['auto', 'sqrt']
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
min_samples_split = [2, 5, 10]
min_samples_leaf = [1, 2, 4]
bootstrap = [True, False]

random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}



randomGridSearch = RandomizedSearchCV(estimator=rfc, param_distributions=random_grid,
                              n_iter = 100, scoring=mcc_scorer, 
                              cv = 3, verbose=2, random_state=42, n_jobs=-1,
                              return_train_score=True)

randomGridSearch.fit(fileFeatures, y)

print(randomGridSearch.best_params_)

rfc_improved = randomGridSearch.best_estimator_
rfc_improved.fit(fileFeatures, y)

results = testResults(rfc_improved)
results.to_csv('optimisedResults/' + 'RandomForestImproved' +".csv", index=False)

pickle.dump(rfc_improved, open('models/randomisedOptimisedRandomForest.sav', 'wb'))

''' {'n_estimators': 2000, 'min_samples_split': 5, 
'min_samples_leaf': 1, 'max_features': 'sqrt',
'max_depth': 10, 'bootstrap': True} '''

param_grid = {
    'bootstrap' : [True],
    'max_depth' : [5,10,15],
    'max_features' : ["sqrt"],
    'min_samples_leaf' : [1,2],
    'min_samples_split' : [4,5,6],
    'n_estimators' : [1900, 2000, 2100]
}

rf = RandomForestClassifier()

grid_search = GridSearchCV(estimator = rf, param_grid = param_grid, 
                          cv = 3, n_jobs = -1, verbose = 2)

grid_search.fit(fileFeatures, y)

grid_search.best_params_

rf_improved = grid_search.best_estimator_
rf_improved.fit(fileFeatures, y)


results = testResults(rf_improved)
results.to_csv('optimisedResults/' + 'RandomForestImprovedGridSearch' +".csv", index=False)

pickle.dump(rf_improved, open('models/bestRandomForest.sav', 'wb'))
