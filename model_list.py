from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostRegressor
from sklearn.svm import SVC
from sklearn.linear_model import Perceptron, SGDClassifier, LogisticRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import pdb

from sklearn.svm import SVC

'''Model functions must be manually added to L.'''


def decision_tree():
    clf = DecisionTreeClassifier()
    params = {'max_depth':[2, 3,5,10,None], 'max_features':['sqrt', 'log2', None], 'criterion': ['gini','entropy']}
    return clf, params

def boosted_decision_tree():
    clf = AdaBoostClassifier(DecisionTreeClassifier(min_samples_split=2,
                                                    random_state = None), 
                             algorithm="SAMME")
    params = {'n_estimators':[25, 50, 100],
              'base_estimator__max_depth':[2, 3, 5, 10, None]}
    return clf, params

def random_forest():
    clf = RandomForestClassifier()
    params = {'max_depth':[1,5,10,15, 20, 25, None],
              'n_estimators':[5,25,50, 100, 150, 200, 250, 300], #300, 500, 1000
              'max_features':['sqrt','log2', None], # , 
              'criterion': ['gini','entropy'],
              'bootstrap': [True, False]}
    return clf, params

def logreg():
    clf = LogisticRegression() 
    params = {'dual':[True, False], 'C':[.01, .1, 1, 2, 5]}
    # params = {}
    return clf, params

def perceptron():
    clf = Perceptron() 
    params = {'penalty':[None, 'l2','l1','elasticnet']}
    # params = {}
    return clf, params

def mlp():
    clf = MLPClassifier() 
    params = {'hidden_layer_sizes':[(100), (30,30,30),(30,100,30), (10,10,10,10,10),(100,100,100)],
               'activation': ['tanh', 'relu'], 'max_iter': [200, 500]}
    # params = {}
    return clf, params


def svm_rbf():
    clf = SVC(kernel='rbf')
    params = {}
    return clf, params

def svm_linear():
    clf = SVC(kernel='linear')
    params = {}
    return clf, params

def svm_poly():
    clf = SVC(kernel='poly')
    params = {}
    return clf, params

# model_list = [decision_tree, boosted_decision_tree, random_forest, logreg, perceptron, svm_rbf, svm_linear]

model_list = [decision_tree, random_forest, svm_rbf]
