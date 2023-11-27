#Importar librerías
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore")

#Importar dataframes 
directorio_actual = os.getcwd()
df = pd.read_csv(os.path.join(directorio_actual, '..', 'data','raw','df_total_venta.csv'))
df = df.drop(['Unnamed: 0'], axis=1)
df_pob_distr = pd.read_csv(os.path.join(directorio_actual, '..', 'data','processed','df_pob_distr.csv'))

#Tratamiento de dataframes
df = df.drop(['thumbnail','numPhotos','operation','province','has360','country','url','hasVideo','hasPlan','has3DTour','hasStaging','externalReference','labels','newDevelopmentFinished','highlight'],axis=1)
df = df.drop(['topNewDevelopment','superTopHighlight'], axis=1)
df = df[df['priceByArea'] >= 500]
df = df.drop([502,726])
df.reset_index(inplace=True)
df.drop(['index'],axis=1,inplace=True)

#Parking
df['parking'] = 0
df['parkingSpace'] = df['parkingSpace'].fillna(0)

for i, dicc in enumerate(df['parkingSpace']):
    if dicc != 0:
        string = str(dicc)
        if 'False' not in string:
            df['parking'][i] = 1

#Población / distrito
df['district'].fillna(df['municipality'],inplace=True)

grupo_ciudad_distrito = df.groupby(['municipality','district'],as_index=False)['priceByArea'].agg(['mean'])
grupo_ciudad_distrito = grupo_ciudad_distrito.sort_values(by='mean',ascending=True)
grupo_ciudad_distrito = grupo_ciudad_distrito.reset_index()
grupo_ciudad_distrito = grupo_ciudad_distrito.reset_index()
grupo_ciudad_distrito.drop(['index'],axis=1,inplace=True)
grupo_ciudad_distrito['level_0'] = grupo_ciudad_distrito['level_0']+1
grupo_ciudad_distrito.rename(columns={'level_0':'codigo_distrito'},inplace=True)
grupo_ciudad_distrito['poblacion / distrito'] = grupo_ciudad_distrito['municipality'] + ' / ' + grupo_ciudad_distrito['district']

df['codigo_distrito'] = 0
df['poblacion / distrito'] = 0
df['precio_area / distrito'] = 0

for i, municipio in enumerate(df['municipality']):
    if df['codigo_distrito'][i] == 0:
        for n, municipio_group in enumerate(grupo_ciudad_distrito['municipality']):
            if municipio_group == municipio:
                for w, distrito in enumerate(df['district']):
                    if w == i:
                        for p, distrito_group in enumerate(grupo_ciudad_distrito['district']):
                            if distrito_group == distrito and grupo_ciudad_distrito['municipality'][p] == municipio:
                                df['codigo_distrito'][i] = grupo_ciudad_distrito['codigo_distrito'][p]
                                df['poblacion / distrito'][i] = grupo_ciudad_distrito['poblacion / distrito'][p]
                                df['precio_area / distrito'][i] = grupo_ciudad_distrito['mean'][p]

df = df[df['poblacion / distrito'].isin(df_pob_distr['poblacion / distrito'])]
df.drop(['codigo_distrito'],axis=1,inplace=True)
df['codigo_distrito'] = df['poblacion / distrito'].map(df_pob_distr.set_index('poblacion / distrito')['codigo_distrito'])

df.reset_index(inplace=True)
df.drop(['index'],axis=1,inplace=True)

#Tipo de vivienda
df['codigo_tipo'] = 0

for i, tipo in enumerate(df['detailedType']):
    variable = str(tipo)
    if variable == "{'typology': 'flat', 'subTypology': 'studio'}": 
        df['codigo_tipo'][i] = 1
    elif variable == "{'typology': 'flat'}": 
        df['codigo_tipo'][i] = 2
    elif variable == "{'typology': 'chalet', 'subTypology': 'terracedHouse'}": 
        df['codigo_tipo'][i] = 3
    elif variable == "{'typology': 'flat', 'subTypology': 'duplex'}": 
        df['codigo_tipo'][i] = 4
    elif variable == "{'typology': 'flat', 'subTypology': 'penthouse'}": 
        df['codigo_tipo'][i] = 5
    elif variable == "{'typology': 'chalet', 'subTypology': 'semidetachedHouse'}": 
        df['codigo_tipo'][i] = 6
    else: 
        df['codigo_tipo'][i] = 7

for i, comment in enumerate(df['description']):
    if pd.notna(comment) and ('ático' in comment or 'atico' in comment or 'Ático' in comment or 'Atico' in comment):
        df['codigo_tipo'][i] = 5

#Piscina
def tiene_piscina(description):
    if pd.notna(description):  
        return 1 if 'piscina' in description.lower() else 0
    else:
        return 0

df['piscina'] = df['description'].apply(tiene_piscina)

#Tratamiento de dataframe
df = df.drop(['municipality','address','district','showAddress','exterior','distance','suggestedTexts','neighborhood','floor','detailedType','newDevelopment','hasLift','parkingSpace'],axis=1)

#Dataframe numérica
df_num_venta = df[['size','rooms','bathrooms','codigo_distrito','parking','price','codigo_tipo','piscina']]
df_num_venta['total_rooms'] = df_num_venta['bathrooms'] + df_num_venta['rooms']
df_num_venta.drop(['rooms','bathrooms'],axis=1,inplace=True)

df_num_venta = df_num_venta[[col for col in df_num_venta.columns if col != 'price'] + ['price']]


#Train split
df_train_venta, df_test_venta = train_test_split(df_num_venta,test_size=0.15,random_state=10)

#Exportar dataframes
df.to_csv(os.path.join(directorio_actual, '..', 'data','processed','df_venta.csv'), index=False)
df_num_venta.to_csv(os.path.join(directorio_actual, '..', 'data','processed','df_num_venta.csv'), index=False)
df_train_venta.to_csv(os.path.join(directorio_actual, '..', 'data','train','df_train_venta.csv'), index=False)
df_test_venta.to_csv(os.path.join(directorio_actual, '..', 'data','test','df_test_venta.csv'), index=False)
