from fastapi import FastAPI, HTTPException
import sqlite3
import requests
from bs4 import BeautifulSoup
from formulas import obtener_presupuesto, lista_peliculas, ganancias_diarias, peliculas_año, calificacion_publico

app = FastAPI(title="Información de Películas")

@app.get("/peliculas/retorno/{nombre}")
def roi_pelicula(nombre: str):
    ## Conexión con la API externa ##
    ## Se busca el nombre especificado en la API ##
    ## La API retorna datos para la película especificada ##
    url = f"https://www.omdbapi.com/?t={nombre}&apikey=thewdb"
    r = requests.get(url)
    data = r.json()

    ## Si la respuesta es negativa entonces devuelve el siguiente mensaje ##
    if data.get("Response") == "False":
        raise HTTPException(status_code=404, detail="Película no encontrada en OMDb")
    
    ## Llamamos a la función de presupuesto ( inversión inicial ) ##
    presupuesto = obtener_presupuesto(data["Title"])
    if not presupuesto:
        presupuesto = None

    ## Obtenemos la recaudación a nivel local (EE.UU) que logró la película (ganancias) ##
    recaudacion_local = data.get("BoxOffice")
    if recaudacion_local and recaudacion_local != "N/A":
        try:
            ## Convertirmos el string a un entero "$415,004,880" → 415004880 ##
            ganancia_local = int(recaudacion_local.replace("$", "").replace(",", ""))
        except ValueError:
            ganancia_local = None
    else:
        ganancia_local = None
    
    ## Asumimos que el valor del roi es 0 inicialmente ##
    roi = None
    ## Si ambos valores existen entonces se calcula el roi ##
    if presupuesto and ganancia_local:
        presupuesto = int(presupuesto)
        roi = round(((ganancia_local - presupuesto) / presupuesto) * 100, 2)

    ## Se devuelve un diccionario con los valores de recaudación, presupuesto y roi porcentual ##
    return {
        "recaudacion_local": recaudacion_local,
        "presupuesto": presupuesto,
        "roi_%": roi,
    }

@app.get("/peliculas/calificaciones/{nombre}")
def comparar_calificaciones(nombre: str):
    ## Conexión con la API externa ##
    ## Tiene el objetivo de obtener la calificacion que le dieron los críticos a la pelicula seleccionada ##
    ## Luego compara a tráves de casos (if) y entrega un mensaje de vuelta ##
    url = f"https://www.omdbapi.com/?t={nombre}&apikey=thewdb"
    r = requests.get(url)
    data = r.json()
    ## Para ver caso a caso se llama a la función calificacion_publico de la base de datos para obtener la nota indicada por el publico general, ##
    ## luego se compara con la nota que dio la crítica y se entrega un mensaje ##
    if data.get("imdbRating") > calificacion_publico(nombre):
        return f"La crítica calificó a esta película con una nota de {data.get('imdbRating')}, por un nivel más alto que el público general que le dio una nota de {calificacion_publico(nombre)}"
    elif data.get("imdbRating") == calificacion_publico(nombre):
        return f"La crítica y el público general evaluaron con una nota de {data.get('imdbRating')} a esta película"
    else:
        return f"El público general calificó a esta película con una nota de {calificacion_publico(nombre)}, por un nivel más alto que la crítica que le dio una nota de {data.get('imdbRating')}"

@app.get("/peliculas")
def lista():
    ## Entrega la lista completa de películas que posee la base de datos ##
    return lista_peliculas()

@app.get("/peliculas/ganancias-diarias/{nombre}")
def ganancias_dia_prom(nombre: str):
    ## Retorna la ganancias diarias promedio obtenida por la película indicada ##
    return ganancias_diarias(nombre)

@app.get("/peliculas/mejores/{anio}")
def mejor_calificadas(anio: str):
    ## Entrega la lista de películas estrenadas en el año seleccionado, 
    ## las ordena de mejor calificadas a peor calificadas ##
    return peliculas_año(anio)