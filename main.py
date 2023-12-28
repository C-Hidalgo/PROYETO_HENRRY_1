from funciones import *
from fastapi import FastAPI
import pandas as pd
import uvicorn

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000, debug=True)


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