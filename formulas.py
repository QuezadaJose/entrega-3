# main.py (versión simple)
from fastapi import FastAPI, HTTPException
import sqlite3
import requests
from bs4 import BeautifulSoup

# 📦 Función para obtener presupuesto desde SQLite
def obtener_presupuesto(titulo: str):
    ## Con esta fórmula buscamos obtener el dato del presupuesto que tuvo cierta película,
    ## para ello el usuario le debe entregar un nombre exacto.
    try:
        ## Conexión a la base de datos y búsqueda de la información ##
        conexion = sqlite3.connect("pelis1.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT presupuesto FROM peliculas WHERE titulo = ?", (titulo,))
        fila = cursor.fetchone()
        conexion.close()
        ## Si la fila existe retorna el valor, si no arroja None ##
        if fila:
            return fila[0]
        else:
            return None
    ## Si en caso que la película no existiese se le devuelve el siguiente mensaje ##
    except Exception as e:
        print("Error accediendo a la base de datos:", e)
        return None

def lista_peliculas():
    ## Función que genera un diccionario que contiene todos los nombres de las películas en la base de datos ##
    conexion = sqlite3.connect("pelis1.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT titulo from peliculas")
    filas = cursor.fetchall()
    conexion.close()
    titulos = [fila[0] for fila in filas]
    return {"Títulos": titulos}

def ganancias_diarias(titulo: str):
    ## Función que calcula las ganancias diarias en promedio de una película 
    ## Se le entrega al nombre de la película deseada
    conexion = sqlite3.connect("pelis1.db")
    cursor = conexion.cursor()
    ## Busca las ganancias totales generadas y el número de días "al aire" ##
    cursor.execute("SELECT ganancias, dias FROM peliculas WHERE titulo = ?", (titulo,))
    fila = cursor.fetchone()
    conexion.close()
    ## Si la fila tiene un valor entonces procede a calcular la cantidad de ganancias diarias promedio ##
    if fila:
        ganancias = int(fila[0])
        dias = int(fila[1])
        promedio = round(ganancias/dias)
        return f"Las ganancias diarias promedio de {titulo} fueron de ${promedio}"
    ## Si la fila no tiene valor entonces se le entrega el siguiente mensaje ##
    else:
        return "Película no encontrada, verificar título"
        
def peliculas_año(anio: str):
    ## Función que retorna las películas estrenadas durante un año especifico ##
    conexion = sqlite3.connect("pelis1.db")
    cursor = conexion.cursor()
    ## Se busca toda la información de las peliculas de tal año ##
    ## En la base de datos la fecha está en formato: DIA/MES/AÑO ##
    ## Es por lo anterior que al extraer los ultimos cuatro caracteres obtenemos el año indicado ##
    cursor.execute("SELECT * FROM peliculas WHERE substr(lanzamiento, -4) = ?", (anio,))
    filas = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    conexion.close()
    ## Datos peliculas se encarga de entregar una lista de diccionarios, uno por película ##
    ## [dict(zip(columnas, fila)) for fila in filas] se encarga de generar diccionarios que unen el nombre de la columna con el valor de la fila ##
    datos_peliculas = [dict(zip(columnas, fila)) for fila in filas]
    resultado = [
         {"Título": peli["titulo"],
          "Calificación": peli["calificacion"],
          "Estreno": peli["lanzamiento"]}
        for peli in datos_peliculas
    ]
    ## Se ordenan de mayor a menor según su calificación recibida, ##
    ## entrega la pelicula mejor criticada del año especificado en primera posición ##
    resultado.sort(key=lambda x: x["Calificación"], reverse = True)
    return resultado

def calificacion_publico(titulo: str):
    ## Esta función se encarga de entregar la calificación obtenida para la película especificada ##
    conexion = sqlite3.connect("pelis1.db")
    cursor = conexion.cursor()
    ## Se selcciona el dato en la base ##
    cursor.execute("SELECT calificacion FROM peliculas WHERE titulo = ?", (titulo,))
    fila = cursor.fetchone()
    conexion.close()
    ## Se entrega ##
    if fila: 
        return fila[0]
    ## En caso que no exista la pelicula ##
    else:
        return "Película no encontrada, verificar título"