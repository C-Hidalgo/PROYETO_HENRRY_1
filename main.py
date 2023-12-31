from funciones import *
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd

app = FastAPI()


@app.get('/')
def bienvenida():
    return {'API de consultas a una base de datos de la Plataforma Steam'}


@app.get('/Year/{genero}')
def PlayTimeGenre(genero:str):
    """
   Devulve el año con mas horas jugadas para dicho género.
    """
    try:
        return PlayTimeGenre_fun(genero)
    except Exception as e:
        return {"Error":str(e)}
    

@app.get('/User/{genero}')
def UserForGenre(genero:str):
    """
   Devulve el usuario que acumula más horas jugadas para el género dado
   y una lista de la acumulación de horas jugadas por año
    """
    try:
        return UserForGenre_df(genero)
    except Exception as e:
        return {"Error":str(e)}


@app.get('/UsersRecommend/{year}')
def UsersRecommend(año: int):
    """
    Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado
    """
    try:
        return UsersRecommend_df(año)
    except Exception as e:
        return {"Error":str(e)}


@app.get('/UsersNotRecommend/{year}')
def UsersRecommend(año: int):
    """
    Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado
    """
    try:
        return UsersNotRecommend_df(año)
    except Exception as e:
        return {"Error":str(e)}


@app.get('/Sentimiento/{year}')
def sentiment_analysis(año: int):
    try:
        return sentiment_analysis_df(año)
    except Exception as e:
        return {"Error": str(e)}



steam_games = pd.read_csv('./Datasets/steam_games.csv')
cosine_sim, indices = preparar_datos(steam_games)

@app.get('/juegos_similares/{game_name}')
async def obtener_juegos_similares_endpoint(game_name: str):
    juegos_similares = obtener_juegos_similares(game_name, cosine_sim, indices, steam_games)
    
    return {"juegos_similares": list(juegos_similares)}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000, debug=True)
