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


data_desc = 'Harvard 2016 - 2021'
date = "{:%B_%d_%Y_%I_%M_%p}".format(datetime.now(timezone('US/Eastern')))

# df = pd.read_csv('updateProfiles.csv')
with open('updatedProfiles.pkl', 'rb') as fobj:
    df = pickle.load(fobj)


### get rid of columns without a decision
df = df.dropna(subset=['decision'])

### Replace Errors and Zeros of  ACT/GPA with mean ACT/GPA
df['act'] = pd.to_numeric(df['act'], downcast = 'integer', errors = 'coerce')
df['gpa'] = pd.to_numeric(df['gpa'], errors = 'coerce')
df['sat1'] = pd.to_numeric(df['sat1'], downcast = 'integer', errors = 'coerce')

df['act']= df['act'].where(df['act']!=0, np.nan) 
df['gpa']= df['gpa'].where(df['gpa']!=0, np.nan) 
df['sat1']= df['sat1'].where(df['sat1']!=0, np.nan) 

mean_act = df['act'].mean(skipna=True)
mean_gpa = df['gpa'].mean(skipna=True)
mean_sat = df['sat1'].mean(skipna=True)

df['act']=df['act'].fillna(value = mean_act)
df['gpa']=df['gpa'].fillna(value = mean_gpa)
df['sat1']=df['sat1'].fillna(value = mean_sat)


### AP replace list of scores with number of tests and average test
def ap_features(ap_score):
    count = len(ap_score) if type(ap_score) is list else 0
    avg = np.mean(ap_score) if type(ap_score) is list else np.nan
    return pd.Series(data = {'ap_count': count, 'ap_mean': avg})

df[['ap_count', 'ap_mean']] = df['ap'].apply(ap_features)
mean_ap_score = df['ap_mean'].mean(skipna=True)
df['ap_mean']=df['ap_mean'].fillna(value = mean_ap_score)


### SAT2 replace list of scores with number of tests and average test
def sat2_features(sat2_score):
    count = len(sat2_score) if type(sat2_score) is list else 0
    avg = np.mean(sat2_score) if type(sat2_score) is list else np.nan
    return pd.Series(data = {'sat2_count': count, 'sat2_mean': avg})

df[['sat2_count', 'sat2_mean']] = df['ap'].apply(sat2_features)
mean_sat2_score = df['sat2_mean'].mean(skipna=True)
df['sat2_mean']=df['sat2_mean'].fillna(value = mean_sat2_score)

### Convert gender and ethnicity to categorical variable
df = pd.get_dummies(df, columns = ['gender', 'ethnicity'])

## Convert column
def binary_decision(dec):
    if dec == 'A': return 1
    else: return 0

def ternary_decision(dec):
    if dec == 'A': return 1
    elif dec == 'A': return 2
    else: return 3

df['decision'] = df['decision'].apply(binary_decision)

# label = 'decision'
# numerical_feats = ['act', 'gpa', 'sat'] 
# categorical_feats = ['ethnicity', 'gender', 'state', 'schooltype'] 
# binary_feats = [] # to add: AP's, awards, 

# results = pd.DataFrame(index = [], columns = [])
cols_to_use = ['gpa', 'act', 'sat1', 'ap_count', 'ap_mean', 'sat2_count', 'sat2_mean']

features = df[cols_to_use].as_matrix()
labels = df['decision'].as_matrix()




####  RUN MODELS #### NEEDS features and labels
results = pd.read_csv('log.csv')

n, d = features.shape
# splits data into train and test
X_train, X_test, y_train, y_test = train_test_split(
                                    features, labels, test_size=0.1, random_state=1)
acc_count = np.sum(labels)
wait_count = 'NA'
rej_count = labels.shape[0] - acc_count
class_balance = acc_count/rej_count
num_classes = len(np.unique(labels))

for model_func in ml.model_list:
        model, parameters = model_func()

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
        results = results.append(curr_model_details, ignore_index=True)

results.to_csv('log.csv')








