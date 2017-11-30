import pandas as pd
import numpy as np

### AP replace list of scores with number of tests and average test
def ap_features(ap_score):
    count = len(ap_score) if type(ap_score) is list else 0
    avg = np.mean(ap_score) if type(ap_score) is list else np.nan
    return pd.Series(data = {'ap_count': count, 'ap_mean': avg})

### SAT2 replace list of scores with number of tests and average test
def sat2_features(sat2_score):
    count = len(sat2_score) if type(sat2_score) is list else 0
    avg = np.mean(sat2_score) if type(sat2_score) is list else np.nan
    return pd.Series(data = {'sat2_count': count, 'sat2_mean': avg})

## Convert label column
def binary_decision(dec):
    if dec == 'A': return 1
    else: return 0

def ternary_decision(dec):
    if dec == 'A': return 1
    elif dec == 'A': return 2
    else: return 3

def convert_to_features(df, columns_to_use, label_column):
    df = df.copy(deep = True)
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



    df[['ap_count', 'ap_mean']] = df['ap'].apply(ap_features)
    mean_ap_score = df['ap_mean'].mean(skipna=True)
    df['ap_mean']=df['ap_mean'].fillna(value = mean_ap_score)


    df[['sat2_count', 'sat2_mean']] = df['ap'].apply(sat2_features)
    mean_sat2_score = df['sat2_mean'].mean(skipna=True)
    df['sat2_mean']=df['sat2_mean'].fillna(value = mean_sat2_score)

    ### Convert gender and ethnicity to categorical variable
    df = pd.get_dummies(df, columns = ['gender', 'ethnicity'])

    df['decision'] = df['decision'].apply(binary_decision)

    features = df[columns_to_use].as_matrix()
    labels = df[label_column].as_matrix()
    return features, labels




