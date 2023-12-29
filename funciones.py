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
    max_playtime_user = df_genre.groupby('user_id')['playtime_forever'].sum().idxmax()

    # Crear una lista de la acumulación de horas jugadas por año
    playtime_by_year = df_genre.groupby('Year')['playtime_forever'].sum().reset_index()

    return max_playtime_user, playtime_by_year