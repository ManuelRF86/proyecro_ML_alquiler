import pandas as pd
import os

directorio_actual = os.getcwd()

df = pd.read_csv(os.path.join(directorio_actual, '..', 'data','processed','df.csv'))
df_venta = pd.read_csv(os.path.join(directorio_actual, '..', 'data','processed','df_venta.csv'))
df_NS = pd.read_csv(os.path.join(directorio_actual, '..', 'data','processed','df_NS.csv'))

def calcular_alquiler(tamaño,poblacion_distrito,parking,tipo_vivienda,piscina,habitaciones,baños):
    
    dicc_tipo = {'Estudio' : 1,'Piso' : 2,'Adosado' : 3,'Duplex' : 4,'Ático' : 5,'Casa pareada' : 6,'Chalet independiente' : 7}
    dicc = {}
    
    dicc['size'] = tamaño

    for i, pob_dis in enumerate(df['poblacion / distrito']):
        if pob_dis == poblacion_distrito:
            for n, codigo_dist in enumerate(df['codigo_distrito']):
                if n == i:
                    dicc['codigo_distrito'] = codigo_dist
                    break
    if parking == 'No':            
        dicc['parking'] = 0
    else:
        dicc['parking'] = 1

    for tipo,codigo in dicc_tipo.items():
        if tipo == tipo_vivienda:
            dicc['codigo_tipo'] = codigo

    if piscina == 'No':            
        dicc['piscina'] = 0
    else:
        dicc['piscina'] = 1

    
    dicc['total_rooms'] = habitaciones + baños
    
    
    return(dicc)  


def calcular_venta(tamaño,poblacion_distrito,parking,tipo_vivienda,piscina,habitaciones,baños):
    
    dicc_tipo = {'Estudio' : 1,'Piso' : 2,'Adosado' : 3,'Duplex' : 4,'Ático' : 5,'Casa pareada' : 6,'Chalet independiente' : 7}
    dicc = {}
    
    dicc['size'] = tamaño

    for i, pob_dis in enumerate(df_venta['poblacion / distrito']):
        if pob_dis == poblacion_distrito:
            for n, codigo_dist in enumerate(df_venta['codigo_distrito']):
                if n == i:
                    dicc['codigo_distrito'] = codigo_dist
                    break
    if parking == 'No':            
        dicc['parking'] = 0
    else:
        dicc['parking'] = 1

    for tipo,codigo in dicc_tipo.items():
        if tipo == tipo_vivienda:
            dicc['codigo_tipo'] = codigo

    if piscina == 'No':            
        dicc['piscina'] = 0
    else:
        dicc['piscina'] = 1

    
    dicc['total_rooms'] = habitaciones + baños
    
    
    return(dicc)  


def calcular_alquiler_NS(tamaño,poblacion_distrito,parking,tipo_vivienda,piscina,habitaciones,baños):
    
    dicc_tipo = {'Estudio' : 1,'Piso' : 2,'Adosado' : 3,'Duplex' : 4,'Ático' : 5,'Casa pareada' : 6,'Chalet independiente' : 7}
    dicc = {}
    
    dicc['size'] = tamaño

    for i, pob_dis in enumerate(df_NS['poblacion / distrito']):
        if pob_dis == poblacion_distrito:
            for n, codigo_dist in enumerate(df_NS['precio_area / distrito']):
                if n == i:
                    dicc['precio_area / distrito'] = codigo_dist
                    break
    if parking == 'No':            
        dicc['parking'] = 0
    else:
        dicc['parking'] = 1

    for tipo,codigo in dicc_tipo.items():
        if tipo == tipo_vivienda:
            dicc['codigo_tipo'] = codigo

    if piscina == 'No':            
        dicc['piscina'] = 0
    else:
        dicc['piscina'] = 1

    
    dicc['total_rooms'] = habitaciones + baños
    
    
    return(dicc)    