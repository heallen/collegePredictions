from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostRegressor
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.preprocessing import PolynomialFeatures
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import mutual_info_classif
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import pdb

from sklearn.svm import SVC

'''Model functions must be manually added to L.'''


def decision_tree():
    clf = DecisionTreeClassifier()
    params = {'max_depth':[2, 3,5,10,None]}
    return clf, params

def boosted_decision_tree():
    clf = AdaBoostClassifier(DecisionTreeClassifier(min_samples_split=2,
                                                    random_state = None), 
                             algorithm="SAMME",
                             learning_rate = 2,
                             random_state = None)
    params = {'n_estimators':[25, 50],
              'base_estimator__max_depth':[2, 3, 5, 10, None]}
    return clf, params

def random_forest():
    clf = RandomForestClassifier()
    params = {'n_estimators':[5,25,50, 100], 'max_features':['sqrt', 'log2']}
    return clf, params


def mlp():
    clf = MLPClassifier() 
    params = {'hidden_layer_sizes':[(100), (30,30,30),(30,100,30), (10,10,10,10,10),(100,100,100)]}
    # params = {}
    return clf, params

def svm():
    clf = SVC()
    params = {}
    return clf, params

def svm_rbf():
    clf = SVC(kernel='rbf')
    params = {}
    return clf, params

model_list = [decision_tree, boosted_decision_tree, random_forest, mlp, svm, svm_rbf]

