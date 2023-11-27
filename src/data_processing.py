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
df = pd.read_csv(os.path.join(directorio_actual, '..', 'data','raw','df_total.csv'))
df = df.drop(['Unnamed: 0'], axis=1)

#Tratamiento de dataframes
df = df.drop(['thumbnail','numPhotos','operation','province','has360','country','url','hasVideo','hasPlan','has3DTour','hasStaging','externalReference','labels','newDevelopmentFinished','highlight'],axis=1)
df = df.drop(['topNewDevelopment','superTopHighlight'], axis=1)
df = df.drop([874,543,546,545,547,515,802,210,261,992])
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

grupo_ciudad_distrito.to_csv(os.path.join(directorio_actual, '..', 'data','processed','df_pob_distr.csv'), index=False)

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
df_num = df[['size','rooms','bathrooms','codigo_distrito','parking','price','codigo_tipo','piscina']]
df_num['total_rooms'] = df_num['bathrooms'] + df_num['rooms']
df_num.drop(['rooms','bathrooms'],axis=1,inplace=True)

df_num = df_num[[col for col in df_num.columns if col != 'price'] + ['price']]


#Train split
df_train, df_test = train_test_split(df_num,test_size=0.15,random_state=10)

#Exportar dataframes
df.to_csv(os.path.join(directorio_actual, '..', 'data','processed','df.csv'), index=False)
df_num.to_csv(os.path.join(directorio_actual, '..', 'data','processed','df_num.csv'), index=False)
df_train.to_csv(os.path.join(directorio_actual, '..', 'data','train','df_train.csv'), index=False)
df_test.to_csv(os.path.join(directorio_actual, '..', 'data','test','df_test.csv'), index=False)
