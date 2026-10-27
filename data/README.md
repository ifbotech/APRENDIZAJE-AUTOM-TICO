# Datos

Todos los archivos de esta carpeta los descarga o los genera la notebook `Grupo_Nro_12_Tema_Deteccion_Anomalias_Capturas_Pesqueras.ipynb`. Si un archivo ya existe, se usa esa copia; si no, se descarga de la fuente original. Los archivos descargados no se editan: la limpieza se hace por código.

| Carpeta | Contenido | Fuente | Uso en la notebook |
| --- | --- | --- | --- |
| `raw/` | `captura-puerto-flota-2010-2018.csv` y `captura-puerto-flota-2019.csv`: desembarques por mes, flota, puerto y especie, en kg | [Datos abiertos MAGyP](https://datos.magyp.gob.ar/dataset/e2f12522-4dea-495e-877a-b6d2737ae6bf) | Auditoría de calidad (4.1) y coordenadas de los puertos (4.4) |
| `oficial/` | 65 tablas HTML, una por año (2014–2026) y tipo de cruce: `especie_mes`, `especie_puerto`, `especie_flota`, `puerto_mes` y `flota_mes`, en toneladas | [Estadísticas de desembarques de la Subsecretaría de Pesca y Acuicultura](https://www.magyp.gob.ar/sitio/areas/pesca_maritima/desembarques/) | Base del modelo |
| `externos/` | `sst_oisst_zonas_mensual.csv`: temperatura superficial del mar media mensual en tres zonas de la plataforma; `oni.txt`: Índice Oceánico El Niño; `sam_aao.txt`: Modo Anular del Sur | NOAA OISST v2.1 (vía ERDDAP) y NOAA Climate Prediction Center | Variables climáticas (4.5, 7) |
| `referencias/` | `coordenadas_puertos.csv`: tabla de la entrega inicial (archivo 2019); `coordenadas_puertos_completas.csv`: 22 puertos con zona y fuente de la coordenada | Conjunto abierto y OpenStreetMap (Nominatim) | Variables geográficas (4.4) |
| `procesados/` | `dataset_modelo.csv`: una fila por especie y mes (43 especies, 2017–2025) con la etiqueta y las 41 variables candidatas | Generado por la notebook (sección 8) | Dataset final |

## `procesados/dataset_modelo.csv`

| Grupo de columnas | Columnas |
| --- | --- |
| Identificación | `especie`, `categoria`, `fecha`, `anio`, `mes` |
| Objetivo y su construcción | `captura_t`, `y` = log1p(captura_t), `esperado`, `residuo`, `escala`, `z`, `clase` (`caida` / `normal` / `aumento`), `clase_cod` (−1 / 0 / 1) |
| Variables candidatas | ver la tabla de la sección 7.1 de la notebook; el modelo usa 24 columnas (diccionario de la sección 8, con el rol de cada variable) |

Todas las variables candidatas usan solo información disponible hasta el mes anterior.

## Cómo leer el conjunto abierto

- Codificación **Latin-1 (ISO-8859-1)**. Leído como UTF-8, los acentos se rompen.
- `provincia_id` y `departamento_id` tienen ceros a la izquierda: hay que leerlos como texto.
- `captura` está en kilogramos.

```python
import pandas as pd

df = pd.read_csv("data/raw/captura-puerto-flota-2019.csv", encoding="latin-1",
                 dtype={"provincia_id": str, "departamento_id": str})
```

## Cómo leer las tablas oficiales

Las tablas usan formato numérico argentino (punto de miles y coma decimal). El título está en las primeras filas, los encabezados en la fila 5 y debajo vienen bloques por categoría (Peces, Crustáceos, Moluscos) con subtotales. La notebook las convierte a formato largo con las funciones `especie_mes`, `cruce_anual` y `filas_simples` (sección 3).

```python
import io
import pandas as pd

html = open("data/oficial/especie_mes_2025.html", encoding="utf-8", errors="replace").read()
tabla = pd.read_html(io.StringIO(html), thousands=".", decimal=",")[0]
```
