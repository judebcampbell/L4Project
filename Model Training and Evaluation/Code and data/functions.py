from matplotlib import transforms
import numpy as np
import pandas as pd

import os

from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score


#Function generates features from datasets
def generateFeatures(df, interval=0.5): 
  stop = False
  time = interval
  final_time = float(df.tail(1)["Time"])
  rows = []

  while stop == False:
    sub_df = df[(df["Time"] >= time - interval) & (df["Time"] < time)]

    packet_count = sub_df.shape[0]
    no_sources = sub_df["Source"].nunique()
    no_dests = sub_df["Destination"].nunique()
    pack_length = round(sub_df["Length"].mean())
    min_length = sub_df["Length"].min()
    max_length = sub_df["Length"].max()
    packet_types = sub_df["Protocol"].nunique()
    s7_packs = sub_df[sub_df["Protocol"] == "S7COMM"].count()[0]
    row = [time, int(packet_count), no_sources, no_dests, pack_length, min_length, max_length, packet_types, s7_packs]
    rows.append(row)

    time += interval
    if final_time - time < - interval:
      stop = True
  
  features = pd.DataFrame(rows, columns=["Time","No Packets", "No Sources", "No Destinations", "Avg Pack Length", "Minimum Length", "Maximum Length", "No Packet Types", "No S7 packs"])
  features = features.set_index("Time")

  return(features)

#Calculates the scores for a set of predictions
def generateScores(true, predictions, title="Results", Print=True):
	accuracy = accuracy_score(true, predictions)
	precision = precision_score(true, predictions)
	recall = recall_score(true, predictions)

	f1_class = f1_score(true, predictions, average=None)
	mcc = matthews_corrcoef(true, predictions)

	if Print == True:
		print(title)
		print("------------------")
		print("Accuracy:     %5.3f\n     precision:    %5.4f\n     Recall:     %5.5f" % (accuracy, precision, recall))
		print("F1 score for normal:     %5.3f, F1 score for target:     %5.3f" % (f1_class[0], f1_class[1]))
		print("Mathews Correlation Coefficient:     %5.2f" % (mcc))
	
  
	return([accuracy, precision, recall, f1_class[0], f1_class[1], mcc])

#Calculates the exact times of the attacks to create the target values
def attack_times(file):
  return file[((file["Source"] == "192.168.5.64") & (file["Destination"] == "192.168.5.63")) | 
		((file["Source"] == "192.168.5.93") & (file["Destination"] == "192.168.5.63")) |
		((file["Source"] == "192.168.5.63") & (file["Destination"] == "192.168.5.64")) |
		((file["Source"] == "192.168.5.63") & (file["Destination"] == "192.168.5.93"))]

#Calculate true values for test cases
def y_values(file ,df, interval=0.5):
  attacks = attack_times(file)
  times = (df.index).tolist()
  y = []
  for time in times:
    for index, row in attacks.iterrows():
      if time - interval <= row["Time"] < time:
        y.append(1)
        break
      if row["Time"] > time:
        y.append(0)
        break
    if len(y) != times.index(time) + 1:
      y.append(0)
  return(y)


def testResults(model):
  i = 1
  df = pd.DataFrame(columns=['accuracy', 'precision', 'recall', 'f1 normal', 'f1 target', 'mcc'], index=[1,2,3,4,5,6,7,8,9,10])
  files = ['testdata/Test1 None.csv', 'testdata/Test2 None.csv','testdata/Test3 64Always.csv', 'testdata/test4 64variable.csv', 'testdata/Test5 64Sometimes.csv','testdata/Test6 Snap7.csv', 'testdata/Test7 Snap72.csv', 'testdata/Test8 Snap7Limited.csv',  'testdata/Test9 mixed1.csv', 'testdata/Test10 Mixed2.csv']
  for file in files:
    f = pd.read_csv(file)
    features = generateFeatures(f)

    if file == 'testdata/Test1 None.csv' or file == 'testdata/Test2 None.csv':
      y = [1 for i in range((features.shape[0]))]
    else:
      y = y_values(f, features)
    pred = model.predict(features)

    results = generateScores(y, pred, file, False)
    df.loc[i] = results
    i += 1
  return(df)
