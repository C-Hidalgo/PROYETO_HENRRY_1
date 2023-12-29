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