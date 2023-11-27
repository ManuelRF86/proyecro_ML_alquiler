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

df_train_venta = pd.read_csv(os.path.join(directorio_actual, '..', 'data','train', 'df_train_venta.csv'))
df_test_venta = pd.read_csv(os.path.join(directorio_actual, '..', 'data','test', 'df_test_venta.csv'))
df_num_venta = pd.read_csv(os.path.join(directorio_actual, '..', 'data','processed', 'df_num_venta.csv'))

X_train_venta = df_train_venta.drop(['price'],axis=1)
y_train_venta = df_train_venta['price']
X_test_venta = df_test_venta.drop(['price'],axis=1)
y_test_venta = df_test_venta['price']
X_venta = df_num_venta.drop(['price'],axis=1)
y_venta = df_num_venta['price']


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

Modelo_GBR.fit(X_train_venta, y_train_venta)

#Exportar modelos
modelo_GBR = Modelo_GBR.best_estimator_

with open(os.path.join(directorio_actual, '..', 'models','modelo_GBR_venta.pkl'), 'wb') as file:
    pickle.dump(modelo_GBR, file)

modelo_final_GBR = Modelo_GBR.best_estimator_.fit(X_venta, y_venta)

with open(os.path.join(directorio_actual, '..', 'models','modelo_final_GBR.pkl'), 'wb') as file:
    pickle.dump(modelo_final_GBR, file)
