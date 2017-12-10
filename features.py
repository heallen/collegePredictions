import pandas as pd
import numpy as np
import pdb

### AP replace list of scores with number of tests and average test
def ap_features(ap_score):
    count = len(ap_score) if type(ap_score) is list else 0
    avg = np.mean(ap_score) if type(ap_score) is list else np.nan
    if avg > 5:
        avg = np.nan
    return pd.Series(data = {'ap_count': count, 'ap_mean': avg})

### SAT2 replace list of scores with number of tests and average test
def sat2_features(sat2_score):
    count = len(sat2_score) if type(sat2_score) is list else 0
    avg = np.mean(sat2_score) if type(sat2_score) is list else np.nan
    if avg > 800:
        avg = np.nan
    return pd.Series(data = {'sat2_count': count, 'sat2_mean': avg})

## Convert label column
def binary_decision(dec):
    if dec == 'A': return 1
    else: return 0

def ternary_decision(dec):
    if dec == 'A': return 1
    elif dec == 'A': return 2
    else: return 3

score_map = {36: 2390, 35: 2330, 34:2250, 33.35567282:2220, 33:2180, 32:2120, 31:2060, 30:2000, 
             29:1940, 28:1880, 27:1820, 26:1770, 25:1710, 24:1650, 23:1590, 22:1530, 21:1470, 1:600}

def get_best_test(row):
    global score_map
    if row.act == 0:
        return pd.Series({'test_type': 'sat', 'test_score': row.sat1})
    if row.sat1 == 0:
        return pd.Series({'test_type': 'act', 'test_score': score_map.get(row.act)})
    if row.sat1 > score_map.get(row.act):
        return pd.Series({'test_type': 'sat', 'test_score': row.sat1})
    return pd.Series({'test_type': 'act', 'test_score': score_map.get(row.act)})


def convert_to_features(df, cols):
    df = df.copy(deep = True)
    ### get rid of columns without a decision
    df = df.dropna(subset=['decision'])




    ### Replace Errors and Zeros of ACT/GPA/sat1/Rank with mean ACT/GPA/sat1/Rank
    df['gpa'] = pd.to_numeric(df['gpa'], errors = 'coerce')
    df['gpa']= df['gpa'].where(df['gpa']!=0, np.nan) 
    mean_gpa = df['gpa'].mean(skipna=True)
    df['gpa']=df['gpa'].fillna(value = mean_gpa)

    df['rank']= df['rank'].where(df['sat1']!=0, np.nan) 
    mean_rank = df['rank'].mean(skipna=True) 
    df['rank']=df['rank'].fillna(value = mean_rank)

    df['act'] = pd.to_numeric(df['act'], downcast = 'integer', errors = 'coerce')
    df['sat1'] = pd.to_numeric(df['sat1'], downcast = 'integer', errors = 'coerce')
    df = df.loc[(df.sat1 != 0) | (df.act != 0)].copy(deep = True)
    df[['test_score','test_type']] = df.apply(get_best_test, axis = 1)
    
    df['act']= df['act'].where(df['act']!=0, np.nan) 
    df['sat1']= df['sat1'].where(df['sat1']!=0, np.nan) 
    mean_act = df['act'].mean(skipna=True)
    mean_sat = df['sat1'].mean(skipna=True)
    df['act']=df['act'].fillna(value = mean_act)
    df['sat1']=df['sat1'].fillna(value = mean_sat)



    df[['ap_count', 'ap_mean']] = df['ap'].apply(ap_features)
    mean_ap_score = df['ap_mean'].mean(skipna=True)
    df['ap_mean']=df['ap_mean'].fillna(value = mean_ap_score)


    df[['sat2_count', 'sat2_mean']] = df['sat2'].apply(sat2_features)
    pdb.set_trace()
    mean_sat2_score = df['sat2_mean'].mean(skipna=True)
    df['sat2_mean']=df['sat2_mean'].fillna(value = mean_sat2_score)
    print(mean_sat2_score)

    ## Location Data
    df['state']= df['state'].fillna(value = 'international')
    df['country']= df['country'].fillna(value = 'US')


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


    df = df[cols]

    df.to_pickle('featuresDFwCat.pkl')

    ### Convert to categorical variable
    feature_count = len(df.columns)-1
    cat_cols = set(['gender', 'ethnicity', 'state', 'country', 'school', 'test_type'])
    cat_cols = list(set.intersection(cat_cols, set(df.columns)))
    df = pd.get_dummies(df, columns = cat_cols)
    
    cat_count = len(cat_cols)
    return df, (feature_count-cat_count, cat_count, len(df.columns)-1)




