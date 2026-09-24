# Datos

Desembarques de pesca marítima por puerto, flota y especie publicados por el Ministerio de Agricultura, Ganadería y Pesca en su portal de datos abiertos.

- Conjunto de datos: <https://datos.magyp.gob.ar/dataset/http-www-magyp-gob-ar-sitio-areas-pesca-maritima-desembarques>
- Recurso principal (2010–2018): <https://datos.magyp.gob.ar/dataset/http-www-magyp-gob-ar-sitio-areas-pesca-maritima-desembarques/archivo/77a15b4a-71e1-4b81-9732-ae0b6863c8cc>

## Archivos en `raw/`

| Archivo | Contenido | Estado |
| --- | --- | --- |
| `captura-puerto-flota-2019.csv` | Desembarques de enero a noviembre de 2019 (3.040 filas, 13 columnas) | Copia sin modificar del archivo publicado |
| Archivo 2010–2018 | Desembarques de enero 2010 a diciembre 2018 (aprox. 41.340 filas, 13 columnas) | A descargar del recurso principal y guardar en esta carpeta |

Los archivos en `raw/` no se editan: la limpieza se hace por código y los resultados van a otra carpeta.

## Tabla de coordenadas en `referencias/`

`referencias/coordenadas_puertos.csv` tiene una fila por puerto con su latitud, longitud y la fuente del dato. La arma `src/coordenadas.py` a partir de las coordenadas que ya trae el dataset (cada puerto tiene siempre el mismo par):

```bash
python src/coordenadas.py data/raw/captura-puerto-flota-2019.csv [otro.csv ...]
```

Si un puerto real queda sin coordenadas, se buscan a mano (por ejemplo en Google Maps u OpenStreetMap) y se anotan en la tabla con la fuente en la columna `fuente`. Al volver a correr el script, esos valores se conservan. «otros puertos Buenos Aires» queda en blanco porque agrupa varios puertos y no tiene una ubicación única.

## Cómo leer los CSV

- Codificación: el archivo 2019 está en **Latin-1 (ISO-8859-1)** con fin de línea CRLF. Leído como UTF-8, los acentos se rompen.
- `provincia_id` y `departamento_id` tienen ceros a la izquierda (`06`, `06357`): hay que leerlos como texto.
- `captura` está en kilogramos.

```python
import pandas as pd

df = pd.read_csv(
    "data/raw/captura-puerto-flota-2019.csv",
    encoding="latin-1",
    dtype={"provincia_id": str, "departamento_id": str},
)
```

`src/perfilado.py` detecta la codificación sola (prueba UTF-8 y después Latin-1).
