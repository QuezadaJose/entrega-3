# entrega-3
# API Economía y Ciencia de Datos

API construida con **FastAPI** que integra tres módulos principales:

1. **Historial Académico**  
   - CRUD de **ramos**  
   - CRUD de **evaluaciones**

2. **Películas**  
   - Consultas a BD local  
   - Integración con **OMDb** para datos externos, ROI y calificaciones

3. **Economía (World Bank)**  
   - Integración con **World Bank API (wbgapi)**  
   - Estadísticas, correlaciones y regresiones económicas
---

## 🧩 0. `main.py` — Configuración general y endpoint raíz

- Crea la app FastAPI con:
  - `title="API Economía y Ciencia de Datos"`
  - `description` con autores
  - `version="2.1.0"`

También incluye los routers:

- `/ramos` → `app.routers.ramos`
- `/evaluaciones` → `app.routers.evaluaciones`
- `/peliculas` → `app.routers.peliculas`
- `/economia` → `app.routers.economia`

---

## 🎓 1. Historial Académico – Ramos (`app/routers/ramos.py`)

Este router maneja el CRUD de los **ramos** (asignaturas) del historial académico. Toda la lógica de base de datos está en `crud_ramos.py` y los modelos Pydantic en `schemas.py`. :contentReference[oaicite:0]{index=0}

**Prefix:** `/ramos`  
**Tag:** `Historial Académico - Ramos`

### 1.1. `GET /ramos/obtener`

**Función:** `obtener_ramos_api`

**Qué hace:**  
Devuelve el listado de ramos del historial académico con filtros opcionales por nombre, año, semestre, área, estado y un flag para incluir la nota final.

**Parámetros (query, todos opcionales):**

- `ramo: str` — Filtra por nombre (o parte del nombre) del ramo.
- `año: int` — Filtra por año académico (ej: `2023`).
- `semestre: int` — Filtra por semestre (`1` o `2`).
- `area: str` — Filtra por área (ej: `"Matemáticas"`, `"Economía"`).
- `estado: str` — Filtra por estado (ej: `"Aprobado"`, `"En Curso"`, `"Reprobado"`).
- `incluir_nota_final: bool` — Si es `true`, incluye la nota final del ramo.

**Respuesta:**

Lista de ramos, cada uno con campos como:

```json
{
  "id_ramo": 1,
  "ramo": "Cálculo I",
  "año": 2023,
  "semestre": 1,
  "area": "Matemáticas",
  "estado": "Aprobado",
  "nota_final": 6.5
}
```
### 1.2. `POST /ramos/agregar`

**Función:**  `crear_ramo_api`

- `ramo: str` — Filtra por nombre (o parte del nombre) del ramo.
- `año: int` — Filtra por año académico (ej: `2023`).
- `semestre: int` — Filtra por semestre (`1` o `2`).
- `area: str` — Filtra por área (ej: `"Matemáticas"`, `"Economía"`).
- `estado: str` — Filtra por estado (ej: `"Aprobado"`, `"En Curso"`, `"Reprobado"`).
- `incluir_nota_final: bool` — Si es `true`, incluye la nota final del ramo.

**Qué hace:**
Crea un nuevo ramo en el historial académico. Si el ramo ya existe (según la lógica de crud_ramos), devuelve un mensaje con la info existente.

Ejemplo de request:

```json
{
  "ramo": "Cálculo I",
  "año": 2023,
  "semestre": 1,
  "area": "Matemáticas",
  "estado": "Aprobado",
  "nota_final": 6.8
}
```

### 1.3. `PATCH /ramos/actualizar/{id_ramo}`
**Función:** actualizar_ramo_api

**id_ramo:** int — ID del ramo a actualizar.

**Query:**

`confirm_ramo:` str — Nombre del ramo para confirmar que de verdad quieres actualizar ese ramo.

**Todos opcionales: ramo, año, semestre, area, estado, nota_final.**

**Qué hace:**
Actualiza uno o varios campos del ramo. La función de BD (actualizar_ramo) puede devolver:

- un objeto actualizado 
- un dict indicando: conflicto → 409 (ej: nombre no coincide con confirm_ramo)
- mensaje de no encontrado → 404

### 1.4. `DELETE /ramos/borrar/{id_ramo}`
**Función:** eliminar_ramo_api

**Parámetros:**
**Path:** `id_ramo:` int — ID del ramo a borrar.

**Query:** `confirm_ramo:` str — Nombre del ramo para confirmar eliminación.

**Qué hace:**
Elimina el ramo indicado si existe y si el nombre coincide con confirm_ramo.

Respuesta: mensaje de confirmación, por ejemplo:

```json
{
  "mensaje": "El ramo Cálculo I (ID: 1) fue eliminado exitosamente",
  "id_ramo_eliminado": 1,
  "ramo_eliminado": "Cálculo I"
}
```

## 📝 2. Historial Académico – Evaluaciones (app/routers/evaluaciones.py)
Este router maneja las evaluaciones asociadas a los ramos: controles, pruebas, exámenes, etc.

**Prefix:** /evaluaciones

**Tag:** Historial Académico - Evaluaciones

### 2.1. `GET /evaluaciones/obtener`
Función: obtener_evaluaciones_api

**Qué hace:**
Permite buscar evaluaciones con varios filtros opcionales. Se pueden combinar criterios.

Parámetros (query, todos opcionales):

- `id_ramo:` int — ID del ramo.

- `ramo:` str — Nombre del ramo (y debe ser coherente con id_ramo si ambos se dan).

- `evaluacion:` str — Nombre/descrición (ej: "Prueba 1").

- `id_evaluacion:` int — ID único de la evaluación.

- `nota:` float — Filtrar por nota exacta.

**Respuesta:**
Lista de evaluaciones con campos como:

```json
{
  "id_evaluacion": 1,
  "id_ramo": 5,
  "ramo": "Cálculo I",
  "evaluacion": "Prueba 1",
  "ponderacion": 0.3,
  "nota": 6.8
}
```
## 2.2. `POST /evaluaciones/agregar`
**Función:** crear_evaluacion_api

**Parámetros:**

**Query:**

- `id_ramo:` int — ID del ramo.

- `confirm_ramo:` str — Nombre del ramo para confirmar.

**Body:**

- `evaluacion:` str

- `ponderacion:` float (0–1)

- `nota:` float (0–7)

**Qué hace:**
Crea una nueva evaluación asociada a un ramo. Si la evaluación ya existe o hay conflicto con el nombre del ramo, se retorna 409 con detalles.

## 2.3. `PATCH /evaluaciones/actualizar/{id_evaluacion}`
**Función:** actualizar_evaluacion_api

**Parámetros:**

**Path:**

- `id_evaluacion:` int — Evaluación a actualizar.

**Query:**

- `confirm_ramo:` str — Confirma el ramo.

- `confirm_evaluacion:` str — Confirma el nombre de la evaluación.

**Body:** Campos opcionales **evaluacion, ponderacion, nota.**

**Qué hace:**
Actualiza una evaluación existente.

## 2.4. `DELETE /evaluaciones/eliminar/{id_evaluacion}`
**Función:** eliminar_evaluacion_api

**Parámetros:**

**Path:**

- `id_evaluacion:` int

**Query:**

- `confirm_evaluacion:` str

- `confirm_ramo:` str

**Qué hace:**
Elimina una evaluación específica, requiriendo confirmación tanto del nombre de la evaluación como del ramo.

Respuesta: mensaje del estilo:

```json
{
  "mensaje": "Evaluación 'Prueba 1' del ramo 'Cálculo I' eliminada exitosamente."
}
```

## 🎬 3. Módulo de Películas (app/routers/peliculas.py) 
Este router expone endpoints relacionados con una base de datos local de películas y la API externa OMDb para obtener datos adicionales, ROI y calificaciones.

**Prefix:** /peliculas
**Tag:** Películas

## 3.1. `GET /peliculas/lista`
**Función:** lista

**Qué hace:**
Devuelve la lista completa de películas en la base de datos local, con información básica (título, año, género, duración, calificación, etc.).

## 3.2. `GET /peliculas/{nombre}`
**Función:** dato_peli

**Parámetros:**

**Path:**

- `nombre:` str — Título (exacto o parcial, según la lógica interna) de la película.

**Qué hace:**
Devuelve todos los datos disponibles para una película específica en la BD local: título, año, géneros, duración, calificaciones, ingresos, director, reparto, etc.

## 3.3. `GET /peliculas/retorno/{nombre}`
**Función:** roi_pelicula

**Qué hace:**

Llama a OMDb con obtener_datos_omdb(nombre).

Si OMDb no encuentra la película → 404.

Si hay problemas de conexión → 502 o 504.

Llama a calcular_roi(nombre, data) para calcular:

- presupuesto

- ingresos en USA

- ROI (%)

- una etiqueta de rentabilidad (ej: "Muy Rentable").

**Respuesta:**

```json
{
  "titulo": "Inception",
  "presupuesto": 160000000,
  "ingresos_usa": 292000000,
  "roi": 82.5,
  "rentabilidad": "Muy Rentable"
}
```

## 3.4. `GET /peliculas/calificaciones/{nombre}`
**Función:** comparar_calificaciones

**Qué hace:**

Consulta OMDb con obtener_datos_omdb(nombre).

Compara calificaciones de:

BD local (crítica) v/s OMDb (público)

Llama a comparar_calificaciones_bd_omdb(nombre, data) que arma un análisis: calificacion_critica v/s calificacion_publico

Se calcula la diferencia y luego se entrega un texto interpretando quién valora más la película (crítica vs público).

## 3.5. `GET /peliculas/ganancias-diarias/{nombre}`
**Función:** ganancias_dia_prom

**Qué hace:**

Llama a ganancias_diarias(nombre) que devuelve un texto con:

- ingresos totales

- días en cartelera

- promedio diario.

Intenta formatear el monto final con separadores de miles usando formatear_usd.

El resultado final es un string descriptivo tipo:
```json
"Inception ganó un promedio de $5,264,458 al día. Los ingresos totales fueron de $839,000,000 en 160 días."
```

## 3.6. `GET /peliculas/años/disponibles`
**Función:** años_disponibles

**Qué hace:**

Obtiene la lista de años únicos desde la BD con obtener_años_disponibles().

Si la lista está vacía → 404.

Si hay años, devuelve:

```json
{
  "años": [2020, 2021, 2022],
  "cantidad": 3,
  "rango": "2020 - 2022"
}
```

## 3.7. `GET /peliculas/mejores/{anio}`
**Función:** mejor_calificadas

**Parámetros:**

**Path:**

- anio: str — año en formato YYYY.

**Qué hace:**

Valida que anio sea numérico de 4 dígitos.

Si no, 400 Bad Request.

Llama a peliculas_año(anio_normalizado) para obtener las películas con mejor calificación ese año.

Si no hay resultados → 404.

**Respuesta:**

```json
{
  "año": "2023",
  "peliculas": [
    {"titulo": "Barbie", "calificacion": 8.5},
    {"titulo": "Oppenheimer", "calificacion": 8.3}
  ],
  "cantidad": 2
}
```

## 🌍 4. Módulo de Economía – World Bank (app/routers/economia.py)
Este router maneja toda la integración con la World Bank API usando funciones auxiliares en funciones_economia.py: búsqueda de indicadores, estadísticas, correlaciones y regresiones. 
economia

**Prefix:** /economia
**Tag:** Economía - World Bank

### 4.1. `GET /economia/ejemplos`
**Función:** ejemplos

**Qué hace:**
Devuelve una lista de indicadores económicos de ejemplo (hardcodeada en ejemplos_series()), útil para que el usuario sepa qué códigos usar.

Cada elemento incluye:

- `id:` código del indicador (ej: NY.GDP.MKTP.KD.ZG)

- `serie:` descripción breve (ej: "GDP growth (annual %)")

### 4.2. GET /economia/indicador
**Función:** buscar

**Parámetros (query, opcionales):**

- `descripción:` str — texto a buscar en la descripción del indicador (case-insensitive, búsqueda parcial).

- `id:` str — ID exacto del indicador.

**Reglas:**

Debe proporcionarse al menos uno de los dos.

Si se dan ambos, se prioriza descripción.

**Qué hace:**

Llama a encontrar_serie(parametro=descripción or "", id=id) que consulta en World Bank:

Si falta todo → 400 Bad Request.

Maneja:

TimeoutError → 504 Gateway Timeout.

RuntimeError → 502 Bad Gateway.

Otros errores → 500.

**Respuesta:**

```json
{
  "resultados": [
    {"id": "NY.GDP.MKTP.KD.ZG", "value": "GDP growth (annual %)"},
    {"id": "NY.GDP.DEFL.ZS", "value": "GDP deflator (annual %)"}
  ],
  "mensaje": "OK"
}
```
## 4.3. GET /economia/estadistica
**Función:** estadistica_endpoint

**Parámetros (query, requeridos):**

- `code:` str — código del indicador (ej: NY.GDP.MKTP.KD.ZG).

- `countries:` str — lista de países ISO separados por comas, sin espacios (ej: "CHL,ARG,PER").

- `date_from:` int — año inicial.

- `date_to:` int (opcional) — año final (si no, se usa año actual).

- `include_series:` bool — incluye o no la serie anual detallada.

**Qué hace:**

Separa countries en una lista ["CHL", "ARG", ...].

Llama a estadistica(...) que:

Consulta la API del World Bank

Calcula estadísticas por país (promedio, desviación estándar, mínimo, máximo, cantidad de años)

Genera un resumen_comparativo en español.

**Respuesta:**

```json
{
  "resultados": [
    {
      "pais": "CHL",
      "cant_años": 15,
      "estadisticas": {
        "promedio": 3.2,
        "desviacion_std": 1.5,
        "minimo": 0.5,
        "maximo": 6.3
      },
      "series": [
        {"año": 2010, "valor": 2.5},
        {"año": 2011, "valor": 3.1}
      ]
    }
  ],
  "total_paises": 1,
  "resumen_comparativo": "CHL tuvo un promedio de 3.2% entre 2010-2024."
}
```

## 4.4. `GET /economia/correlacion`
**Función:** correlacion_endpoint

**Parámetros (query, requeridos):**

- `code1:` str — primer indicador (ej: PIB).

- `code2:` str — segundo indicador (ej: inflación).

- `country:` str — código ISO (ej: "CHL").

- `date_from:` int — año inicial.

- `date_to:` int (opcional) — año final.

**Qué hace:**

Llama a calcular_correlacion(...) que:

↳ Descarga ambas series (code1 y code2) para el país y rango de años.

↳ Alinea años comunes.

Calcula:

↳ Correlación de Pearson

↳ p-valor

Y arma un mensaje interpretando magnitud y significancia (ej: “correlación positiva moderada y significativa”).

**Respuesta:**

```json
{
  "pais": "CHL",
  "indicador_1": "NY.GDP.MKTP.KD.ZG",
  "indicador_1_label": "GDP growth",
  "indicador_2": "FP.CPI.TOTL.ZG",
  "indicador_2_label": "Inflation",
  "cant_common": 10,
  "years_common": "2010-2019",
  "correlacion": 0.65,
  "valor_p": 0.042,
  "mensaje": "Correlación positiva moderada y estadísticamente significativa (p < 0.05)."
}
```

## 4.5. `GET /economia/regresion`
**Función:** regresion_endpoint

**Parámetros (query):**

- `model:` str (opcional) — "okun" o "phillips".

- `variable_y:` str (opcional) — código de variable dependiente (si no se usa model).

- `variable_x:` str (opcional) — código de variable independiente.

- `country:` str — país (ej: "CHL").

- `date_from:` int — año inicial.

- `date_to:` int (opcional) — año final.

**Lógica:**

Si se especifica model:

"okun":

Y = SL.UEM.TOTL.ZS (desempleo)

X = NY.GDP.MKTP.KD.ZG (crecimiento PIB)

"phillips":

Y = FP.CPI.TOTL.ZG (inflación)

X = SL.UEM.TOTL.ZS (desempleo)

**Si no se especifica model, se deben pasar explícitamente variable_y y variable_x.**

Si model es desconocido → Error 400.

**Qué hace:**

Llama a regresion_economica(code_y, code_x, country, date_from, date_to) que:

En primer lugar, descarga las dos series y realiza una regresión lineal simple Y ~ X,
de la cual devuelve:
- número de observaciones
- intercepto β₀
- pendiente β₁
- p-valor
- significancia (***, **, *, o “No significativo”)
- R²
- labels de los indicadores
- una interpretación en español.


**Respuesta, ejemplo (modelo Okun):**

```json
{
  "cant_observaciones": 10,
  "intercepto_beta0": 8.5,
  "coeficiente_beta1": -0.42,
  "p_value": 0.032,
  "significancia": "*",
  "r_cuadrado": 0.58,
  "indicador_x_label": "GDP growth",
  "indicador_y_label": "Unemployment",
  "interpretacion": "Por cada punto de aumento en crecimiento del PIB, el desempleo disminuye 0.42 puntos (significativo al 5%)."
}
```
