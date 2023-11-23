import streamlit as st
import pandas as pd
from PIL import Image
import streamlit.components.v1 as c
import pickle


with open('modelos_entrenados/modelo_final_GBR.pkl', 'rb') as file:
    modelo_GBR = pickle.load(file)

st.set_page_config(page_title='Alquileres en Sevilla',
                   page_icon='🏠')

df = pd.read_csv('data/df.csv')

df = df.rename(columns={'latitude':'lat', 'longitude':'lon'})

seleccion = st.sidebar.selectbox('Seleccione una opción', ['Introducción','Tengo una vivienda y la quiero alquilar', 'Quiero comprar una vivienda para alquilarla'])

if seleccion == 'Introducción':
    st.title('¿Cuánto cuesta vivir en Sevilla?')
    img = Image.open('img/img_1.jpg')
    st.image(img)
    with st.expander('Introducción'):
        st.write('Esta aplicación te permitirá, obtener una recomendación del precio de alquiler de una vivienda situada en el área metropolitana de Sevilla')
    with st.expander('Zonas disponibles'):
        st.write(df['poblacion / distrito'].unique())
    with st.expander('Viviendas utilizadas para el modelo'):
        st.map(df)

elif seleccion == 'Tengo una vivienda y la quiero alquilar':
    st.title('Calcular el precio de alquiler de tu vivienda')
    img_2 = Image.open('img/img_2.jpg')
    st.image(img_2)

    e_poblacion_distrito = st.selectbox('Elige un población/distrito:', sorted(df['poblacion / distrito'].unique()))
    

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
    

    e_baños = st.text_input('Introduzca el nº de baños que tiene la vivienda:')
    if e_baños.isdigit():
        e_baños = int(e_baños)
    else:
        st.error('Por favor, introduzca un valor numérico válido para el nº de baños.')

    e_parking = st.selectbox('Elije si tiene parking incluido en el precio:', ['Sí','No'])
    

    e_tipo_vivienda = st.selectbox('Elige el tipo de vivienda:', ['Piso','Estudio','Adosado','Duplex','Ático','Casa pareada','Chalet independiente'])
    

    def calcular_alquiler(tamaño,poblacion_distrito,parking,tipo_vivienda,habitaciones,baños):
    
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

        
        dicc['total_rooms'] = habitaciones + baños
    
    
        return(dicc)
    
    
    calcular = st.sidebar.button('Calcular')
    seccion_contenido = st.empty()
    if calcular:
        vivienda = pd.DataFrame([calcular_alquiler(e_tamaño, e_poblacion_distrito, e_parking, e_tipo_vivienda, e_habitaciones, e_baños)], index=['mi_indice'])
        prediction = int(modelo_GBR.predict(vivienda))

        st.title(f"El precio de alquiler de tu vivienda es: {prediction}€")

