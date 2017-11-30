import pandas as pd
import numpy as np
from scikit.__ import
from datetime import datetime
from pytz import timezone
import model_list as ml

data_desc = 'Harvard 20xx - 20xx'
date = "{:%B_%d_%Y_%I_%M_%p}".format(datetime.now(timezone('US/Eastern')))

df = pd.read_csv('updateProfiles.csv')

### Replace 0 ACT/GPA with mean ACT/GPA
df=df.replace({'act': {0: np.nan}}, {'gpa': {0: np.nan}}) 
mean_act = df['act'].mean(skipna=True)
mean_gpa = df['gpa'].mean(skipna=True)
data=df['act'].fillna(value = mean_act)
data=df['gpa'].fillna(value = mean_gpa)

### AP
def ap_features(ap_score):
	print type(ap_score)
	count = len(ap_score) if type(ap_score) is list else 0
	avg = np.mean(ap_score) if type(ap_score) is list else 0
	return pd.Series(data = {'ap_count': count, 'ap_mean': avg})

df[['ap_count', 'ap_mean']] = df['ap'].apply(ap_features, axis = 1)


label = 'decision'
numerical_feats = ['act', 'gpa', 'sat'] 
categorical_feats = ['ethnicity', 'gender', 'state', 'schooltype'] 
binary_feats = [] # to add: AP's, awards, 

# results = pd.DataFrame(index = [], columns = [])







####  RUN MODELS #### NEEDS features and labels

n, d = features.shape
# splits data into train and test
X_train, X_test, y_train, y_test = train_test_split(
									features, labels, test_size=0.1, random_state=1)
acc_count = np.sum(labels)
wait_count = 'NA'
rej_count = labels.shape[0] - one_count
class_balance = acc_count/rej_count
num_labels = length(np.unique(labels))

for model_func in ml.model_list:
        model, parameters = model_func()

        grid_search_clf = GridSearchCV(model, parameters, n_jobs=-1, cv=10)

        model.set_params(**grid_search_clf.best_params_)
		model.fit(X_train, y_train)
        y_predict = clf.predict(X_test)
        
        accuracy = np.sum(y_test == y_predict)
        cnf_matrix = skm.confusion_matrix(y_test, y_predict)
        prec, rec, f1_score = precision_recall_fscore_support(y_test, y_predict)
            
        # saves model performance and details to dictionary
        curr_model_details = {'Date': date, 
        					'Data Desc': data_desc
		        			'Model Type': model_func.__name__. 
		                    'Parameters': grid_search_clf.best_params_,
		                    'Num_Inputs': n,
		                    'Num_Features': d,
		                    'Num_Labels': label_count,
		                    'Acc_Count': acc_count,
		                    'Wait_Count:' wait_count,
		                    'Rej_Count': rej_count,
		                    'Class_Bal': class_balance,
		                    'Acc': accuracy,
		                    'Precision': prec,
		                    'Recall': rec,
		                    'true_neg': cnf_matrix[0][0],
		                    'false_neg': cnf_matrix[0][1],
		                    'false_pos': cnf_matrix[1][0],
		                    'true_pos': cnf_matrix[1][1]}
		result = pd.DataFrame(data = curr_model_details)
		result.to_csv('log.csv', header=False, mode = 'a')
