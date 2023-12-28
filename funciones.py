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

### CARGA DE DATASETS ###
steam_games = pd.read_csv('./DataSets/steam_games.csv')
user_reviews = pd.read_csv('./DataSets/user_reviews.csv')
users_items = pd.read_csv('./DataSets/users_items.csv')

### FUNCION Nº1 (PlayTimeGenre)###
# Devuelve el año con mas horas jugadas para dicho género.

def PlayTimeGenre_fun(genero: str):
    
    # Verificar si la columna del género existe en el DataFrame
    if genero not in users_items.columns:
        print(f"No existe el género '{genero}' en el DataFrame.")
        return None

    users_items_suma= users_items.groupby('item_id')['playtime_forever'].sum().reset_index()
    
    #unifico el dataframeusers_items y steam_games
    funcion_1 = pd.merge(steam_games, users_items_suma, left_on='id', right_on='item_id')
    
    # Filtrar el DataFrame para el género proporcionado
    filtro_genero = funcion_1[funcion_1[genero] == 1]

    if filtro_genero.empty:
        # Manejar el caso en que no hay juegos del género especificado
        print(f"No hay juegos del género '{genero}")
        return None

    # Encontrar la fila con la máxima cantidad de horas de juego
    fila_max_horas = filtro_genero.loc[filtro_genero['playtime_forever'].idxmax()]

    # Resultado como un diccionario
    resultado = {
        "nombre_genero": genero,
        "año_con_más_horas": fila_max_horas['Year'],
        "horas_máximas": fila_max_horas['playtime_forever']
    }

    return resultado