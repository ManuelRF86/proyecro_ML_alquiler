#Importación de librerías
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings("ignore")

directorio_actual = os.getcwd()

#Importacion de dataframes
df_train = pd.read_csv(os.path.join(directorio_actual, '..', 'data','train', 'df_train.csv'))
df_test = pd.read_csv(os.path.join(directorio_actual, '..', 'data','test', 'df_test.csv'))
df_num = pd.read_csv(os.path.join(directorio_actual, '..', 'data','processed', 'df_num.csv'))

X_train = df_train.drop(['price'],axis=1)
y_train = df_train['price']
X_test = df_test.drop(['price'],axis=1)
y_test = df_test['price']
X = df_num.drop(['price'],axis=1)
y = df_num['price']

df_train_venta = pd.read_csv(os.path.join(directorio_actual, '..', 'data','train', 'df_train_venta.csv'))
df_test_venta = pd.read_csv(os.path.join(directorio_actual, '..', 'data','test', 'df_test_venta.csv'))
df_num_venta = pd.read_csv(os.path.join(directorio_actual, '..', 'data','processed', 'df_num_venta.csv'))

X_train_venta = df_train_venta.drop(['price'],axis=1)
y_train_venta = df_train_venta['price']
X_test_venta = df_test_venta.drop(['price'],axis=1)
y_test_venta = df_test_venta['price']
X_venta = df_num_venta.drop(['price'],axis=1)
y_venta = df_num_venta['price']

#Importación de modelos
with open(os.path.join(directorio_actual, '..', 'models','modelo_GBR_venta.pkl'), 'rb') as file:
    modelo_GBR_venta = pickle.load(file)

with open(os.path.join(directorio_actual, '..', 'models','modelo_GBR.pkl'), 'rb') as file:
    modelo_GBR = pickle.load(file)

#Predicciones
prediction = modelo_GBR.predict(X_test)
prediction_venta = modelo_GBR_venta.predict(X_test_venta)

#Evaluación
print('MAE de predicción de alquiler:', mean_absolute_error(y_test,prediction))
print('MAPE de predicción de alquiler:', mean_absolute_percentage_error(y_test,prediction))
print('RMSE de predicción de alquiler:', np.sqrt(mean_squared_error(y_test,prediction)))
print('-'*100)
print('MAE de predicción de compra:', mean_absolute_error(y_test_venta,prediction_venta))
print('MAPE de predicción de compra:', mean_absolute_percentage_error(y_test_venta,prediction_venta))
print('RMSE de predicción de compra:', np.sqrt(mean_squared_error(y_test_venta,prediction_venta)))