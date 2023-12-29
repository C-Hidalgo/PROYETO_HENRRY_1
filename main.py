from funciones import *
from fastapi import FastAPI
import pandas as pd
import uvicorn

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



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000, debug=True)
