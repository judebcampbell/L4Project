from operator import mod
from functions import generateFeatures
import os
import time
import glob
import pickle

import numpy as np
import pandas as pd
import sklearn

import time

path = r"C:\Program Files\Wireshark"
file_type= r'\*csv'

print('opening model')
model = pickle.load(open(r'finalized_model.sav', 'rb'))

os.chdir(path)

print('collecting network data')
os.system(r"tshark -a duration:180 -w C:\Users\Workstation\Desktop\Automate\Captures\test.pcapng")
os.system(r"tshark -r C:\Users\Workstation\Desktop\Automate\Captures\test.pcapng -T fields -e frame.number -e frame.time_relative -e ip.src -e ip.dst -e ip.proto -e frame.len -E header=y -E separator=, -E occurrence=f, -E quote=n > C:\Users\Workstation\Desktop\Automate\Captures\testfile.csv")

save_loc = r"C:\Users\Workstation\Desktop\Automate\Captures"

while True:
    starting = time.time()
    
    files = glob.glob(save_loc + file_type)
    max_file = max(files, key=os.path.getctime)
    current = pd.read_csv(max_file)

    features = generateFeatures(current)
    predictions = model.predict(features)

    times = features.index.values

    print('checking for potential problems')
    for idx, value in enumerate(predictions):
        if value == 1:
            print("Potential problem!!!")
            if idx == 0:
                print("Packets sent between 0 and 0.5 seconds may be suspicious")
                
            else:
                start = times[idx - 1]
                end = times[idx]
                print("Packets sent between %s and %s may be suspicious" % (start, end))

    print('--- %s seconds ---' % (time.time() - starting))
    print('Next data collection ...')
    os.system(r"tshark -a duration:180 -w C:\Users\Workstation\Desktop\Automate\Captures\test.pcapng")
    os.system(r"tshark -r C:\Users\Workstation\Desktop\Automate\Captures\test.pcapng -T fields -e frame.number -e frame.time_relative -e ip.src -e ip.dst -e ip.proto -e frame.len -E header=y -E separator=, -E occurrence=f, -E quote=n > testfile.csv")
