import streamlit as st
import pandas as pd
from PIL import Image
import streamlit.components.v1 as c
import pickle
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from funciones import *


directorio_actual = os.getcwd()

with open(os.path.join(directorio_actual, '..', 'models','modelo_final_GBR.pkl'), 'rb') as file:
    modelo_GBR = pickle.load(file)
with open(os.path.join(directorio_actual, '..', 'models','modelo_final_GBR_venta.pkl'), 'rb') as file:
    modelo_GBR_venta = pickle.load(file)

df_num_NS = pd.read_csv(os.path.join(directorio_actual, '..', 'data','processed', 'df_num_NS.csv'))
X = df_num_NS.drop(['price'],axis=1)
y = df_num_NS['price']


st.set_page_config(page_title='Alquileres en Sevilla',
                   page_icon='🏠')

df = df.rename(columns={'latitude':'lat', 'longitude':'lon'})

seleccion = st.sidebar.selectbox('Seleccione una opción', ['Introducción','Alquiler', 'Venta'])

if seleccion == 'Introducción':
    st.title('¿Cuánto cuesta vivir en Sevilla?')
    img = Image.open(os.path.join(directorio_actual, '..', 'img','img_1.jpg'))
    st.image(img)
    with st.expander('Introducción'):
        st.write('Esta aplicación te permitirá, obtener una recomendación del precio de alquiler de una vivienda situada en el área metropolitana de Sevilla')
    with st.expander('Zonas disponibles'):
        st.write(df['poblacion / distrito'].unique())
    with st.expander('Viviendas utilizadas para el modelo'):
        st.map(df)

elif seleccion == 'Alquiler':
    st.title('Calcular el precio de alquiler de tu vivienda')
    img_2 = Image.open(os.path.join(directorio_actual, '..', 'img','img_2.jpg'))
    st.image(img_2)

    e_poblacion_distrito = st.selectbox('Elige un población/distrito:', sorted(df['poblacion / distrito'].unique()))
    
    col1, col2 = st.columns(2)

    with col1:

        e_tamaño = st.text_input('Introduzca el tamaño de la vivienda en m\u00B2:')
        if e_tamaño.isdigit():
            e_tamaño = int(e_tamaño)
        else:
            st.error('Por favor, introduzca un valor numérico válido para el tamaño de la vivienda.')

        e_habitaciones = st.text_input('Introduzca el nº de habitaciones que tiene la vivienda:')
        if e_habitaciones.isdigit():
            e_habitaciones = int(e_habitaciones)   
        else:
            st.error('Por favor, introduzca un valor numérico válido para el nº de habitaciones.')

        e_parking = st.selectbox('Elije si tiene parking incluido en el precio:', ['Sí','No'])


    with col2:

        e_tipo_vivienda = st.selectbox('Elige el tipo de vivienda:', ['Piso','Estudio','Adosado','Duplex','Ático','Casa pareada','Chalet independiente'])

        e_baños = st.text_input('Introduzca el nº de baños que tiene la vivienda:')
        if e_baños.isdigit():
            e_baños = int(e_baños)
        else:
            st.error('Por favor, introduzca un valor numérico válido para el nº de baños.')

        e_piscina = st.selectbox('Elije si la vivienda dispone de piscina:', ['Sí','No'])

        
    calcular = st.sidebar.button('Calcular')
    seccion_contenido = st.empty()

    tipo_model = st.sidebar.selectbox('Seleccione el tipo de modelo', ['Supervisado','No supervisado'])

    if calcular and tipo_model == 'Supervisado':
        vivienda = pd.DataFrame([calcular_alquiler(e_tamaño, e_poblacion_distrito, e_parking, e_tipo_vivienda,e_piscina, e_habitaciones, e_baños)], index=['mi_indice'])
        prediction = int(modelo_GBR.predict(vivienda))

        st.title(f"El precio de alquiler de tu vivienda es: {prediction}€")

    elif calcular and tipo_model == 'No supervisado':
        vivienda = pd.DataFrame([calcular_alquiler_NS(e_tamaño, e_poblacion_distrito, e_parking, e_tipo_vivienda,e_piscina, e_habitaciones, e_baños)], index=['mi_indice'])
        nueva_df = pd.concat([X,vivienda])
        nueva_df.reset_index(inplace=True)
        nueva_df.drop(['index'],axis=1,inplace=True)

        n = 250
        scaler = StandardScaler()
        nueva_df_scaled = scaler.fit_transform(nueva_df)
        kmeans = KMeans(n_clusters = n) 
        clusters = kmeans.fit_predict(nueva_df_scaled)
        nueva_df['cluster'] = clusters

        while len(nueva_df[nueva_df['cluster'] == nueva_df['cluster'][len(nueva_df)-1]]) == 1:
            n = n - 1
            scaler = StandardScaler()
            nueva_df_scaled = scaler.fit_transform(nueva_df)
            kmeans = KMeans(n_clusters = n) 
            clusters = kmeans.fit_predict(nueva_df_scaled)
            nueva_df['cluster'] = clusters
        nueva_df_train, nueva_df_test = train_test_split(nueva_df,test_size=1, shuffle=False)
        nueva_df_train = pd.concat([nueva_df_train,df_num_NS['price']],axis=1)
        precio_medio_por_cluster = nueva_df_train.groupby(['cluster'],as_index=False)['price'].agg('mean')
        mapeo_cluster = dict(zip(precio_medio_por_cluster['cluster'], precio_medio_por_cluster['price']))
        nueva_df_train['prediccion'] = nueva_df_train['cluster'].map(mapeo_cluster)
        for i,cluster in enumerate(nueva_df_train['cluster']):
            if cluster == nueva_df_test['cluster'][len(nueva_df)-1]:
                prediccion = nueva_df_train['prediccion'][i]
                break
        st.title(f"El precio de alquiler de tu vivienda es: {prediccion}€")

elif seleccion == 'Venta':
    st.title('Invertir en una vivienda para alquilar')
    img_3 = Image.open(os.path.join(directorio_actual, '..', 'img','img_3.jpg'))
    st.image(img_3)

    e_poblacion_distrito_venta = st.selectbox('Elige un población/distrito:', sorted(df['poblacion / distrito'].unique()))
    
    col1_v, col2_v = st.columns(2)

    with col1_v:

        e_tamaño_venta = st.text_input('Introduzca el tamaño de la vivienda en m\u00B2:')
        if e_tamaño_venta.isdigit():
            e_tamaño = int(e_tamaño_venta)
        else:
            st.error('Por favor, introduzca un valor numérico válido para el tamaño de la vivienda.')

        e_habitaciones_venta = st.text_input('Introduzca el nº de habitaciones que tiene la vivienda:')
        if e_habitaciones_venta.isdigit():
            e_habitaciones_venta = int(e_habitaciones_venta)
        else:
            st.error('Por favor, introduzca un valor numérico válido para el nº de habitaciones.')

        e_parking_venta = st.selectbox('Elije si tiene parking incluido en el precio:', ['Sí','No'])


    with col2_v:   

        e_baños_venta = st.text_input('Introduzca el nº de baños que tiene la vivienda:')
        if e_baños_venta.isdigit():
            e_baños_venta = int(e_baños_venta)
        else:
            st.error('Por favor, introduzca un valor numérico válido para el nº de baños.')

        e_tipo_vivienda_venta = st.selectbox('Elige el tipo de vivienda:', ['Piso','Estudio','Adosado','Duplex','Ático','Casa pareada','Chalet independiente'])
        
        e_piscina_venta = st.selectbox('Elije si la vivienda dispone de piscina:', ['Sí','No'])

    calcular = st.sidebar.button('Calcular')
    seccion_contenido = st.empty()
    if calcular:
        vivienda = pd.DataFrame([calcular_venta(e_tamaño, e_poblacion_distrito_venta, e_parking_venta, e_tipo_vivienda_venta,e_piscina_venta, e_habitaciones_venta, e_baños_venta)], index=['mi_indice'])
        prediction = int(modelo_GBR_venta.predict(vivienda))

        st.title(f"El precio de la vivienda sería: {prediction}€")

