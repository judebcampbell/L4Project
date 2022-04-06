import numpy as np
import pandas as pd


from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from sklearn.model_selection import cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline, Pipeline

from functions import *

import os

import matplotlib.pyplot as plt


#%matplotlib inline
plt.style.use('fivethirtyeight')

import pickle


def trial_Models(x, y, loc):
	p = []

	pipeline = Pipeline([
		('clf', LogisticRegression())
	])
	pipeline.steps

	clfs = []
	clfs.append(SGDClassifier())
	clfs.append(DecisionTreeClassifier())
	clfs.append(KNeighborsClassifier())
	clfs.append(LogisticRegression(max_iter=5000))
	clfs.append(RandomForestClassifier())
	clfs.append(GradientBoostingClassifier())

	for classifier in clfs:
		pipeline.set_params(clf = classifier)
		scores = cross_validate(pipeline, x, y)
		p.append(scores["fit_time"])
		classifier.fit(x, y)

		results = testResults(classifier)
		results.to_csv(loc + str(classifier) +".csv", index=False)
	
	print(p)
print("importing files")
file1 = pd.read_csv("shorttraining.csv.csv", engine="python")
file2 = pd.read_csv("longtraining.csv", engine="python")

print("generating features")
file1Features = generateFeatures(file1)
file2Features = generateFeatures(file2)

print("creating target values")
y1 = y_values(file1, file1Features)
y2 = y_values(file2, file2Features)

print("Trialling models for first data set")
results = trial_Models(file1Features, y1, 'shortTraining/')


print("Trialling models on second data set")
trial_Models(file2Features, y2, 'longTraining/')

