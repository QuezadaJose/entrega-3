from fastapi import FastAPI, HTTPException
import sqlite3
import requests
from bs4 import BeautifulSoup
from formulas import obtener_presupuesto, lista_peliculas, ganancias_diarias, peliculas_año, calificacion_publico

app = FastAPI(title="Información de Películas")

# 🎬 Endpoint principal
@app.get("/peliculas/retorno/{nombre}")
def obtener_datos_pelicula(nombre: str):
    url = f"https://www.omdbapi.com/?t={nombre}&apikey=thewdb"
    r = requests.get(url)
    data = r.json()

    if data.get("Response") == "False":
        raise HTTPException(status_code=404, detail="Película no encontrada en OMDb")
    
    presupuesto = obtener_presupuesto(data["Title"])
    if not presupuesto:
        presupuesto = None

    # 3️⃣ Procesar BoxOffice (recaudación doméstica)
    recaudacion_local = data.get("BoxOffice")
    if recaudacion_local and recaudacion_local != "N/A":
        try:
            # Convertir "$415,004,880" → 415004880
            ganancia_local = int(recaudacion_local.replace("$", "").replace(",", ""))
        except ValueError:
            ganancia_local = None
    else:
        ganancia_local = None

    roi = None
    if presupuesto and ganancia_local:
        presupuesto = int(presupuesto)
        roi = round(((ganancia_local - presupuesto) / presupuesto) * 100, 2)

    # 5️⃣ Devolver resultado
    return {
        "recaudacion_local": recaudacion_local,
        "presupuesto": presupuesto,
        "roi_%": roi,
        "calificacion_critica": data.get("imdbRating"),
    }

@app.get("/peliculas/calificaciones/{nombre}")
def comparar_calificaciones(nombre: str):
    url = f"https://www.omdbapi.com/?t={nombre}&apikey=thewdb"
    r = requests.get(url)
    data = r.json()
    if data.get("imdbRating") > calificacion_publico(nombre):
        return f"La crítica calificó a esta película con una nota de {data.get('imdbRating')}, por un nivel más alto que el público general que le dio una nota de {calificacion_publico(nombre)}"
    elif data.get("imdbRating") == calificacion_publico(nombre):
        return f"La crítica y el público general evaluaron con una nota de {data.get('imdbRating')} a esta película"
    else:
        return f"El público general calificó a esta película con una nota de {calificacion_publico(nombre)}, por un nivel más alto que la crítica que le dio una nota de {data.get('imdbRating')}"

@app.get("/peliculas")
def lista():
    return lista_peliculas()

@app.get("/peliculas/ganancias-diarias/{nombre}")
def ganancias_dia_prom(nombre: str):
    return ganancias_diarias(nombre)

@app.get("/peliculas/mejores/{anio}")
def mejor_calificadas(anio: str):
    return peliculas_año(anio)