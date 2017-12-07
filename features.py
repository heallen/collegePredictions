import pandas as pd
import numpy as np
import pdb

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


def convert_to_features(df):
    df = df.copy(deep = True)
    ### get rid of columns without a decision
    df = df.dropna(subset=['decision'])

    ### Replace Errors and Zeros of ACT/GPA/sat1/Rank with mean ACT/GPA/sat1/Rank
    df['act'] = pd.to_numeric(df['act'], downcast = 'integer', errors = 'coerce')
    df['gpa'] = pd.to_numeric(df['gpa'], errors = 'coerce')
    df['sat1'] = pd.to_numeric(df['sat1'], downcast = 'integer', errors = 'coerce')

    df['act']= df['act'].where(df['act']!=0, np.nan) 
    df['gpa']= df['gpa'].where(df['gpa']!=0, np.nan) 
    df['sat1']= df['sat1'].where(df['sat1']!=0, np.nan) 
    df['rank']= df['rank'].where(df['sat1']!=0, np.nan) 


    mean_act = df['act'].mean(skipna=True)
    mean_gpa = df['gpa'].mean(skipna=True)
    mean_sat = df['sat1'].mean(skipna=True)
    mean_rank = df['rank'].mean(skipna=True) 

    df['act']=df['act'].fillna(value = mean_act)
    df['gpa']=df['gpa'].fillna(value = mean_gpa)
    df['sat1']=df['sat1'].fillna(value = mean_sat)
    df['rank']=df['rank'].fillna(value = mean_rank)



    df[['ap_count', 'ap_mean']] = df['ap'].apply(ap_features)
    mean_ap_score = df['ap_mean'].mean(skipna=True)
    df['ap_mean']=df['ap_mean'].fillna(value = mean_ap_score)


    df[['sat2_count', 'sat2_mean']] = df['ap'].apply(sat2_features)
    mean_sat2_score = df['sat2_mean'].mean(skipna=True)
    df['sat2_mean']=df['sat2_mean'].fillna(value = mean_sat2_score)



    ### Convert gender and ethnicity to categorical variable
    df['state']= df['state'].fillna(value = 'international')
    df['country']= df['country'].fillna(value = 'country')
    df = pd.get_dummies(df, columns = ['gender', 'ethnicity', 'state', 'country'])

    ## Location Data

    # pdb.set_trace()

    ### Leadership 
    # Set NA to zero
    df[['urm','first_generation','editor-in-chief','founder', 'president','captain',
        'siemens','intel', 'presidential_scholar', 'national_merit', 'ap_scholar', 
        'aime','imo', 'national_achievement']] = df[['urm','first_generation',
        'editor-in-chief','founder', 'president','captain',
        'siemens','intel', 'presidential_scholar', 'national_merit', 'ap_scholar', 
        'aime','imo', 'national_achievement']].fillna(value = 0).astype(int)

    df['ec_count']= df[['editor-in-chief','founder', 'president','captain',
        'siemens','intel', 'presidential_scholar', 'national_merit', 'ap_scholar', 
        'aime','imo', 'national_achievement']].apply(np.sum, axis = 1)
        # df['first_generation'] = df['first_generation'].fillna(value = 0)

    df['decision'] = df['decision'].apply(binary_decision)


    return df




