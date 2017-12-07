import pandas as pd
import numpy as np
# from scikit.__ import
from datetime import datetime
from pytz import timezone
import model_list as ml
import pickle
import pdb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support

from features import convert_to_features

data_desc = 'Ivys 2016 - 2021'
date = "{:%B_%d_%Y_%I_%M_%p}".format(datetime.now(timezone('US/Eastern')))

# df = pd.read_csv('updateProfiles.csv')
with open('updatedProfiles.pkl', 'rb') as fobj:
    df = pickle.load(fobj)


# cols_to_use = ['gpa', 'act', 'sat1', 'ap_count', 'ap_mean', 'sat2_count', 'sat2_mean']
cols_to_use = None
label_column = 'decision'

df2 = convert_to_features(df)

df2.to_pickle('featuresDF.pkl')

if cols_to_use is None:
    df3 = df2.drop(columns=[label_column, 'ap', 'ib', 'sat2', 'income'])
else:
	df3 = df2[cols_to_use]


features = df3.as_matrix()
labels = df2[label_column].as_matrix()

pdb.set_trace()


####  RUN MODELS #### NEEDS features and labels

n, d = features.shape
# splits data into train and test
X_train, X_test, y_train, y_test = train_test_split(
                                    features, labels, test_size=0.1, random_state=1)
acc_count = np.sum(labels)
wait_count = 'NA'
rej_count = float(labels.shape[0] - acc_count)
class_balance = acc_count/rej_count
num_classes = len(np.unique(labels))

for model_func in ml.model_list:
    model, parameters = model_func()
    print model_func.__name__

    grid_search_clf = GridSearchCV(model, parameters, n_jobs=-1, cv=10)
    grid_search_clf.fit(X_train, y_train)

    model.set_params(**grid_search_clf.best_params_)
    model.fit(X_train, y_train)
    y_predict = model.predict(X_test)
    
    accuracy = np.mean(y_test == y_predict)
    cnf_matrix = confusion_matrix(y_test, y_predict)
    prec, rec, _, _ = precision_recall_fscore_support(y_test, y_predict, average='binary')
        
    # saves model performance and details to dictionary
    curr_model_details = {'Date': date, 
                        'Data Desc': data_desc,
                        'Model Type': model_func.__name__, 
                        'Parameters': str(grid_search_clf.best_params_),
                        'Num_Inputs': n,
                        'Num_Features': d,
                        'Num_Classes': num_classes,
                        'Acc_Count': acc_count,
                        'Wait_Count': wait_count,
                        'Rej_Count': rej_count,
                        'Class_Bal': class_balance,
                        'CV_score': str(grid_search_clf.best_score_),
                        'Accuracy': accuracy,
                        'Precision': prec,
                        'Recall': rec,
                        'true_neg': cnf_matrix[0][0],
                        'false_neg': cnf_matrix[0][1],
                        'false_pos': cnf_matrix[1][0],
                        'true_pos': cnf_matrix[1][1]}
    print curr_model_details
    # curr_model_details = {k: [v] for k, v in curr_model_details.items()}
    # result = pd.DataFrame.from_dict(curr_model_details)
    results = pd.read_csv('log.csv')
    results = results.append(curr_model_details, ignore_index=True)
    results.to_csv('log.csv', index = False)








