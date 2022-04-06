# Code for Training and Optimising Model
This repository contains 3 .py files and 1 .ipnyb file. 

functions.py is support file that holds various functions needed throughout the running.
model_selection.py holds to code the trains and evaluates the six initial models on the two training sets
model_optimisation.py holds the code to optmise the Random Forest classifer.
Graph Production.ipynb is the jupyter notebook used to generate and save all of the models. 

For you convenience all of the data files generating during the running of these file has been retained. 

## Installation
The .txt file requirements.txt describes the requirements necessary to run the program.


## Usage
If you remove the generated data files it is important to ensure that the files are run in the order shown below. 
```python
python model_selection.py
python model_optimisation.py
python Graph Production.ipynb