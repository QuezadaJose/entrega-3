# main.py (versión simple)
from fastapi import FastAPI, HTTPException
import sqlite3
import requests
from bs4 import BeautifulSoup

# 📦 Función para obtener presupuesto desde SQLite
def obtener_presupuesto(titulo: str):
    try:
        conexion = sqlite3.connect("pelis1.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT presupuesto FROM peliculas WHERE titulo = ?", (titulo,))
        fila = cursor.fetchone()
        conexion.close()
        if fila:
            return fila[0]
        else:
            return None
    except Exception as e:
        print("Error accediendo a la base de datos:", e)
        return None

def lista_peliculas():
    conexion = sqlite3.connect("pelis1.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT titulo from peliculas")
    filas = cursor.fetchall()
    conexion.close()
    titulos = [fila[0] for fila in filas]
    return {"Títulos": titulos}

def ganancias_diarias(titulo: str):
        conexion = sqlite3.connect("pelis1.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT ganancias, dias FROM peliculas WHERE titulo = ?", (titulo,))
        fila = cursor.fetchone()
        conexion.close()
        if fila:
            ganancias = int(fila[0])
            dias = int(fila[1])
            promedio = round(ganancias/dias)
            return f"Las ganancias diarias promedio de {titulo} fueron de ${promedio}"
        else:
            return "Película no encontrada, verificar título"
        
def peliculas_año(anio: str):
    conexion = sqlite3.connect("pelis1.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM peliculas WHERE substr(lanzamiento, -4) = ?", (anio,))
    filas = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    conexion.close()
    datos_peliculas = [dict(zip(columnas, fila)) for fila in filas]
    resultado = [
         {"Título": peli["titulo"],
          "Calificación": peli["calificacion"],
          "Estreno": peli["lanzamiento"]}
        for peli in datos_peliculas
    ]
    resultado.sort(key=lambda x: x["Calificación"], reverse = True)
    return resultado

def calificacion_publico(titulo: str):
        conexion = sqlite3.connect("pelis1.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT calificacion FROM peliculas WHERE titulo = ?", (titulo,))
        fila = cursor.fetchone()
        conexion.close()
        if fila: 
             return fila[0]
        else:
             return "Película no encontrada, verificar título"