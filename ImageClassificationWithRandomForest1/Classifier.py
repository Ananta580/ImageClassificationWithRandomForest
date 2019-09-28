
from random import seed
from random import randrange
from csv import reader
from math import sqrt
import pickle

# Load a CSV file
def load_csv(filename):
	dataset = list()
	with open(filename, 'r') as file:
		csv_reader = reader(file)
		for row in csv_reader:
			if not row:
				continue
			dataset.append(row)
	return dataset

# Convert string column to float
def str_column_to_float(dataset, column):
	for row in dataset:
		row[column] = float(row[column].strip())

# Make a prediction with a decision tree
def predict(node, row):
	if row[node['index']] < node['value']:
		if isinstance(node['left'], dict):
			return predict(node['left'], row)
		else:
			return node['left']
	else:
		if isinstance(node['right'], dict):
			return predict(node['right'], row)
		else:
			return node['right']

# Make a prediction with a list of bagged trees
def bagging_predict(trees, row):
	predictions = [predict(tree, row) for tree in trees]
	return max(set(predictions), key=predictions.count)

# Random Forest Algorithm
def random_forest(test):
    with open("C:/Users/anant/OneDrive/Desktop/Hamro dokan/Hamro dokan/ImageClassificationWithRandomForest1/Trees.pkl",'rb')as input:
        unpickler = pickle.Unpickler(input)
        trees=unpickler.load()
        
    predictions = [bagging_predict(trees, row) for row in test]
    return(predictions)
def main():
    trees = list()
    # Test the random forest algorithm
    seed(3)
    # load and prepare data
    filename = 'C:/Users/anant/OneDrive/Desktop/Hamro dokan/Hamro dokan/ImageClassificationWithRandomForest1/unknown.csv'
    dataset = load_csv(filename)
    # convert string attributes to integers

    for i in range(0, len(dataset[0]) - 1):
        str_column_to_float(dataset, i)
    n_folds = 2
    max_depth = 10
    min_size = 1
    sample_size = 1.0
    n_features = int(sqrt(len(dataset[0]) - 1))
    result = random_forest(dataset)
    if(result[0]==0):
        return "Kurtha"
    elif(result[0]==1):
        return "Tshirt"
    else:
        return "Pant"