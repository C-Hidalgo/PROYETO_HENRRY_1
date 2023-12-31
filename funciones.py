import pandas as pd
import numpy as np
import ast
import gzip
import json
import matplotlib.pyplot as plt
import seaborn as sns
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split


### CARGA GENERAL DE DATASETS ###
steam_games = pd.read_csv('./Datasets/steam_games.csv')
user_reviews = pd.read_csv('./Datasets/user_reviews.csv')
users_items = pd.read_csv('./Datasets/users_items.csv')


### FUNCION Nº1 (PlayTimeGenre)###
# Devuelve el año con mas horas jugadas para dicho género y cantidad de horas.

def PlayTimeGenre_fun(genero: str):
    users_items_suma = users_items.groupby('item_id')['playtime_forever'].sum().reset_index()
    
    # Merge the dataframes
    funcion_1 = pd.merge(steam_games, users_items_suma, left_on='id', right_on='item_id')

    # Check if the genre column exists in the DataFrame
    if genero not in funcion_1.columns:
        return {"error": f"No existe el género '{genero}' en el DataFrame."}

    # Filter the DataFrame for the specified genre
    filtro_genero = funcion_1[funcion_1[genero] == 1]

    if filtro_genero.empty:
        return {"error": f"No hay juegos del género '{genero}'."}

    # Find the row with the maximum playtime
    fila_max_horas = filtro_genero.loc[filtro_genero['playtime_forever'].idxmax()]

    # Convert numpy.int64 to native Python types
    horas_maximas = int(fila_max_horas['playtime_forever'])
    year_con_mas_horas = int(fila_max_horas['Year'])

    # Result as a dictionary
    resultado = {
        "nombre_genero": genero,
        "año_con_más_horas": year_con_mas_horas,
        "horas_máximas": horas_maximas
    }

    return resultado


### FUNCION Nº2 (def UserForGenre)###
# Devuelve el usuario que acumula más horas jugadas para el género dado
#  y una lista de la acumulación de horas jugadas por año

def UserForGenre_df(genero: str):
    # Merge the dataframes
    funcion_2 = pd.merge(steam_games, users_items, left_on='id', right_on='item_id')

    # Verificar si la columna del género existe en el DataFrame
    if genero not in funcion_2.columns:
        print(f"No existe el género '{genero}' en el DataFrame.")
        return None

    # Filtrar el DataFrame por el género dado
    df_genre = funcion_2[funcion_2[genero] == 1]

    # Encontrar al usuario con más horas jugadas para el género dado
    max_playtime_user = int(df_genre.groupby('user_id')['playtime_forever'].sum().idxmax())

    # Crear una lista de la acumulación de horas jugadas por año
    playtime_by_year = df_genre.groupby('Year')['playtime_forever'].sum().reset_index()

    # Convertir las horas jugadas a int
    playtime_by_year['playtime_forever'] = playtime_by_year['playtime_forever'].astype(int)

    # Convertir los resultados a JSON
    max_playtime_user_json = json.dumps(max_playtime_user)
    playtime_by_year_json = playtime_by_year.to_json(orient='records')

    return max_playtime_user_json, playtime_by_year_json



### FUNCION Nº3 (def UsersRecommend)###
### Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado

def UsersRecommend_df(año: int):

    # Unifico los dos DataFrame user_reviews y steam_games, atravez de las columnas 'id' y 'item_id'
    df_unido_f3= pd.merge(steam_games, user_reviews, left_on='id', right_on='item_id')

    # Filtrar el DataFrame por el año y condiciones específicas
    df_filtrado = df_unido_f3[(df_unido_f3['Year'] == año) & (df_unido_f3['recommend'] == True) & (df_unido_f3['sentiment_analysis'].isin([1, 2]))]

    # Agrupar por app_name y contar el número de recomendaciones
    top_juegos = df_filtrado.groupby('app_name')['recommend'].sum().reset_index()

    # Ordenar en orden descendente y seleccionar los 3 primeros
    top_juegos = top_juegos.sort_values(by='recommend', ascending=False).head(3)

    # Crear la lista de diccionarios con el formato deseado
    resultado = [{"Puesto {}: ".format(i + 1): juego} for i, juego in enumerate(top_juegos['app_name'])]

    return resultado

### FUNCION Nº4 def UsersWorstDeveloper ###
### Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado

def UsersNotRecommend_df(año: int):

    # Unifico los dos DataFrame user_reviews y steam_games, atravez de las columnas 'id' y 'item_id'
    df_unido_f4= pd.merge(steam_games, user_reviews, left_on='id', right_on='item_id')

   # Filtrar el DataFrame por el año y condiciones específicas
    df_filtrado = df_unido_f4[(df_unido_f4['Year'] == año) & (df_unido_f4['recommend'] == False) & (df_unido_f4['sentiment_analysis'].isin([0]))]

    # Agrupar por app_name y contar el número de recomendaciones
    top_juegos = df_filtrado.groupby('app_name')['recommend'].sum().reset_index()

    # Ordenar en orden descendente y seleccionar los 3 primeros
    top_juegos = top_juegos.sort_values(by='recommend', ascending=False).head(3)

    # Crear la lista de diccionarios con el formato deseado
    resultado = [{"Puesto {}: ".format(i + 1): juego} for i, juego in enumerate(top_juegos['app_name'])]

    return resultado


 ### FUNCION 5 def sentiment_analysis ###

# Según el año de lanzamiento, se devuelve una lista con la cantidad de registros
# de reseñas de usuarios que se encuentran categorizadas con un analisis de sentimientos

def sentiment_analysis_df(año: int):

    # Unifico los dos DataFrame user_reviews y steam_games, atravez de las columnas 'id' y 'item_id'
    df_unido_f5= pd.merge(steam_games, user_reviews, left_on='id', right_on='item_id')

    # Filtrar el DataFrame por el desarrollador seleccionado
    sentimientos = df_unido_f5[df_unido_f5['Year'] == año]

    # Contar la cantidad total de registros de sentiment_analysis
    conteo_sentimientos = sentimientos['sentiment_analysis'].value_counts().to_dict()

    # Mapear los códigos de sentimientos a etiquetas
    mapeo_sentimientos = {'Negative': 0, 'Neutral': 1, 'Positive': 2}
    conteo_final = {clave: conteo_sentimientos.get(mapeo_sentimientos[clave], 0) for clave in mapeo_sentimientos}

    # Crear el diccionario final con el nombre del desarrollador como llave
    resultado = conteo_final

    return resultado



#### FUNCION 6 obtener_juegos_similares ###

### Sistema de recomendacion de juegos

def preparar_datos(steam_games):
    # Eliminamos las columnas 'id', 'Year', 'app_name'
    genres_df = steam_games.drop(['id', 'Year', 'app_name'], axis=1)

    # Calculamos la similitud del coseno entre los juegos
    cosine_sim = cosine_similarity(genres_df, genres_df)

    # Creamos un diccionario que asocia el índice del juego con su nombre
    indices = pd.Series(steam_games.index, index=steam_games['app_name']).to_dict()

    return cosine_sim, indices

def obtener_juegos_similares(nombre_juego, cosine_sim, indices, steam_games):
    # Obtenemos el índice del juego dado su nombre
    idx = indices.get(nombre_juego, -1)

    if idx == -1:
        print(f'El juego "{nombre_juego}" no se encuentra en el conjunto de steam_games.')
        return []

    # Obtenemos las puntuaciones de similitud del juego con otros juegos
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Ordenamos los juegos según las puntuaciones de similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Tomamos los primeros 10 juegos (excluyendo el propio juego)
    sim_scores = sim_scores[1:11]

    # Obtenemos los índices de los juegos similares
    juego_indices = [i[0] for i in sim_scores]

    # Devolvemos los nombres de los juegos similares sin el índice
    return steam_games['app_name'].iloc[juego_indices].values
