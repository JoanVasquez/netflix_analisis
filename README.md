# Análisis de títulos de Netflix — arquitectura por capas

## Estructura

- `src/netflix_analisis/config.py`: configuración (ruta CSV, columnas, etiqueta para nulos).
- `src/netflix_analisis/repository.py`: acceso a datos (CSV).
- `src/netflix_analisis/cleaning.py`: preparación y transformación de datos.
- `src/netflix_analisis/analysis.py`: consultas y métricas.
- `src/netflix_analisis/visualization.py`: construcción de gráficos.
- `main.py`: orquestación del flujo completo.
- `analisis_netflix.ipynb`: exploración y resultados en un Jupyter Notebook.
- `tests/`: pruebas automatizadas con pytest.

## Instrucciones

Desde la carpeta raíz del proyecto:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

Copia el archivo `netflix_titles_ficticio (2).csv` a la carpeta `data/`.

Para ejecutar el análisis desde la terminal:

```bash
python main.py
```

Para usar el notebook, abre `analisis_netflix.ipynb` desde la raíz del proyecto y ejecuta las celdas.

Para las pruebas:

```bash
python -m pytest -q
```

## Criterios de diseño

- Responsabilidad única: lectura, limpieza, análisis y presentación no se mezclan.
- Dependencias explícitas: configuración y datos se inyectan en los objetos.
- DataFrame original inmutable desde el punto de vista de la limpieza.
- Gráficos reciben resultados precalculados; no hacen lecturas ni análisis.
- `country` conserva la semántica del ejercicio original: valores como `Estados Unidos, Canadá` se cuentan como una etiqueta compuesta, no como dos países.
- Los títulos repetidos se **detectan**, pero no se eliminan automáticamente para preservar el comportamiento original.
