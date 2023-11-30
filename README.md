# Predicción de precios en el mercado inmobiliario de Sevilla mediante Machine Learning

En este proyecto, vamos a intentar predecir mediante un modelo de machine learning, el precio de alquiler o de venta de una vivienda, en el area metropolitana de Sevilla, según las características de la vivienda.


El proceso que hemos seguido para obtener nuestro modelo de predicción de machine learning es:

1. Extracción de datos :
La extracción de los datos se ha realizado de la API de idealista, la cual nos proporcionó unas keys y un número de llamadas al mes limitado (100 llamadas)

2. Estudio y tratamiento de dataframes: 
La dataframe final con la cual, entrenaremos nuestro modelo, consta de las siguientes características:
    * size
    * codigo_distrito
    * parking
    * codigo_tipo
    * piscina
    * total_rooms
               
3. Entrenamiento y evaluación de nuestro modelo: 
Para la elección del modelo, primero hemos realizado una búsqueda mediante un Pipeline y utilizando la función GridsearchCV, eligiendo 5 modelos y algunos parametros y obteniendo como resultado mas exitoso, el modelo Gradient Boosting Regressor.
A pesar de que ya sabemos que nuestra elección será el modelo GradientBoostingRegressor, hemos hecho una busqueda individual de los mejores parametros en cada modelo, evaluándolos a su vez

4. Análisis gráfico:
En este apartado, representamos gráficamente la importancia de cada feature en la predicción del precio y como se comportan, los errores de nuestra predicción.
            
5. Predicciones:
Para predecir el alquiler o venta de una vivienda mediante la introducción de nuevos input, hemos realizado esta [aplicación de streamlit](https://github.com/ManuelRF86/proyecto_ML_alquiler/blob/main/app/app.py), donde introduciendo las características de una vivienda, la aplicación te calculará el precio recomendado para esa vivienda.
Para ejecutarla, solo tendras que, desde el terminal, ubicarte en la carpeta app de nuestro repositorio y ejecutar el comando: streamlit run app.py

En la [memoria](https://github.com/ManuelRF86/proyecto_ML_alquiler/blob/main/docs/memoria.ipynb), podrás encontrar mas detalles respecto al proyecto.

