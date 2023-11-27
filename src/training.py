#Importar librerías
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pickle
import yaml
import os

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.feature_selection import SelectKBest
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")

#Importar dataframes
directorio_actual = os.getcwd()

df_train = pd.read_csv(os.path.join(directorio_actual, '..', 'data','train', 'df_train.csv'))
df_test = pd.read_csv(os.path.join(directorio_actual, '..', 'data','test', 'df_test.csv'))
df_num = pd.read_csv(os.path.join(directorio_actual, '..', 'data','processed', 'df_num.csv'))

X_train = df_train.drop(['price'],axis=1)
y_train = df_train['price']
X_test = df_test.drop(['price'],axis=1)
y_test = df_test['price']
X = df_num.drop(['price'],axis=1)
y = df_num['price']


#Entrenar modelo
pipe = Pipeline(steps=
                [("scaler", StandardScaler()),
                 ("reduce_dim", SelectKBest(k=5)),
                 ('regresor', GradientBoostingRegressor())])

GBR_param = {
    'scaler': [StandardScaler(),None],
    'reduce_dim': [SelectKBest(k=[5,6]),PCA(n_components=5),PCA(n_components=6)],
    'regresor': [GradientBoostingRegressor()],
    'regresor__n_estimators': [200],
    'regresor__max_depth': [4],
    'regresor__criterion':['friedman_mse'],
    'regresor__learning_rate': [0.1],
}

search_space = [
 
    GBR_param
]

Modelo_GBR = GridSearchCV(estimator = pipe,
                  param_grid = search_space,
                  scoring='neg_mean_absolute_error',
                  cv = 10)

Modelo_GBR.fit(X_train, y_train)

#Esxportar modelos

modelo_GBR = Modelo_GBR.best_estimator_

with open(os.path.join(directorio_actual, '..', 'models','modelo_GBR.pkl'), 'wb') as file:
    pickle.dump(modelo_GBR, file)

modelo_final_GBR = Modelo_GBR.best_estimator_.fit(X, y)

with open(os.path.join(directorio_actual, '..', 'models','modelo_final_GBR.pkl'), 'wb') as file:
    pickle.dump(modelo_final_GBR, file)
