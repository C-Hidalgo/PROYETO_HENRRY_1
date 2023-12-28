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
