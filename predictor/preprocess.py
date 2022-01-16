import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer


def map_type(x):
    if(x == 'List polecony priorytetowy'):
        return 0
    else:
        return 1
    
def get_place_type_OH(place):
    words = place.split(' ')
    w1 = words[0]
    if(w1 == 'UP'):
        return 'UP'
    elif(w1 == 'FUP'):
        return 'FUP'
    elif(w1 == 'AP'):
        return 'AP'
    else:
        return 'Unk'

def get_dist(d):
    words = d.split(' ')
    if(len(words) > 1):
        if(words[1] == 'km'):
            return float(words[0])
        else:
            return 0
    else:
        return 0    

def get_diff_h(data_wyslania, data_dotarcia):
    d1 = data_wyslania.to_pydatetime()
    d2 = data_dotarcia.to_pydatetime()
    diff = d2 - d1
    return diff.total_seconds() / 3600;    
 
def get_time(t):
    words = t.split(' ')
    if(len(words) == 4):
        return 60 * int(words[0]) + int(words[2])
    elif(len(words) == 2):
        if(words[1] == 'min'):
            return int(words[0])
        else:
            return 60 * int(words[0])
    else:
        return 0    

def boundary(g):
    if(g < 15):
        return 1
    else:
        return 0


def preprocess_data_frame(df):
    df = df.assign(dzien_tygodnia=lambda x: x.data_wyslania.dt.dayofweek)
    df['ilosc_dni_roboczych'] = df['ilosc_dni_roboczych'].astype(int)
    df = df.loc[df['typ'] != 'Przesyłka firmowa polecona zamiejscowa']
    df['typ'] = df['typ'].map({'List polecony priorytetowy':0, 'List polecony ekonomiczny':1})

    df['typ_placowki'] = df['miejsce_wysylki'].apply(get_place_type_OH)
    df = df.assign(godzina=lambda x: x.data_wyslania.dt.hour)
    df['dyst'] = df['czas'].apply(get_dist)
    df['y'] = df[['data_wyslania', 'data_dotarcia']].apply(lambda x : get_diff_h(*x), axis = 1)
    df['czas'] = df['dystans'].apply(get_time)

    df = df[df['ilosc_dni_roboczych'] < 10] 
    df['granica_15'] = df['godzina'].apply(boundary)

    return df

def get_train_val_sets(df, preprocessor):
    df_shuffled = df.sample(frac=1)
    y = df_shuffled['y']
    X_transformed = preprocessor.fit_transform(df_shuffled)
    
    X_train = X_transformed[:23733]
    y_train = y[:23733]
    X_valid = X_transformed[23733:]
    y_valid = y[23733:]

    return np.asarray(X_train), np.asarray(X_valid), np.asarray(y_train), np.asarray(y_valid)


def get_transformers():
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('std_scaler', StandardScaler())
    ])

    categorical_ORD_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('std_scaler', StandardScaler())
    ])

    categorical_OH_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    return numerical_transformer, categorical_ORD_transformer, categorical_OH_transformer


def get_preprocessor(numerical_transformer, categorical_ORD_transformer, categorical_OH_transformer, numerical_cols, categorical_cols_ORD, categorical_cols_OH):
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat_ORD', categorical_ORD_transformer, categorical_cols_ORD),
            ('cat_OH', categorical_OH_transformer, categorical_cols_OH),
            ('num', numerical_transformer, numerical_cols)
        ])

    return preprocessor
