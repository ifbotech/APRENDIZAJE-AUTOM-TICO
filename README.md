<p align="center"><img src="docs/img/logo_ugr.png" alt="Universidad del Gran Rosario" width="96"></p>

# Detección de anomalías en las capturas pesqueras argentinas

**Aprendizaje Automático · Universidad del Gran Rosario · Trabajo Práctico Grupal 2026, 2.º cuatrimestre · Grupo 12**

| Integrantes |
| --- |
| Bernal, Alejandro Matias |
| Paredes, Sebastian Pablo |
| Rodrigues, David Ezequiel |
| Barnetche, Iñaki Francisco |

## El proyecto en breve

Cada mes se registran desembarques pesqueros en los puertos del litoral marítimo argentino. Las capturas varían mucho según la especie, el puerto, la flota y la época del año, así que una captura alta o baja no dice por sí sola si pasó algo fuera de lo normal.

**Problema:** para cada combinación de especie y puerto, y usando solo la información disponible hasta el mes anterior (t − 1), predecir si la captura del mes t será **normal** o **anómala**. Es una tarea de aprendizaje supervisado (clasificación binaria). La etiqueta no existe en los datos: se va a construir a partir del comportamiento histórico de cada especie en cada puerto, con un criterio que se define después del análisis exploratorio.

**Datos:** desembarques de pesca marítima por puerto, flota y especie, publicados como datos abiertos por el Ministerio de Agricultura, Ganadería y Pesca (MAGyP).

| Archivo | Período | Registros | Variables |
| --- | --- | ---: | ---: |
| Principal | enero 2010 – diciembre 2018 | aprox. 41.340 | 13 |
| Complementario (`captura-puerto-flota-2019.csv`) | enero 2019 – noviembre 2019 | 3.040 | 13 |

- Conjunto de datos: <https://datos.magyp.gob.ar/dataset/http-www-magyp-gob-ar-sitio-areas-pesca-maritima-desembarques>
- Recurso principal (2010–2018): <https://datos.magyp.gob.ar/dataset/http-www-magyp-gob-ar-sitio-areas-pesca-maritima-desembarques/archivo/77a15b4a-71e1-4b81-9732-ae0b6863c8cc>

## Entrega inicial (24 de septiembre de 2026)

| Entregable | Archivo |
| --- | --- |
| Documento PDF para subir a la tarea | [`docs/entrega_inicial/Entrega_Inicial_Grupo12.pdf`](docs/entrega_inicial/Entrega_Inicial_Grupo12.pdf) |
| Diapositivas para la presentación de 5 minutos | [`docs/entrega_inicial/Presentacion_Entrega_Inicial_Grupo12.pdf`](docs/entrega_inicial/Presentacion_Entrega_Inicial_Grupo12.pdf) |
| Texto fuente del documento (editable) | [`docs/entrega_inicial/entrega_inicial.md`](docs/entrega_inicial/entrega_inicial.md) |
| Fuente de las diapositivas (editable) | [`docs/entrega_inicial/presentacion.html`](docs/entrega_inicial/presentacion.html) |
| **Guía para la defensa** (explicación simple, ejemplos y preguntas probables) | [`docs/entrega_inicial/guia.md`](docs/entrega_inicial/guia.md) |
| Propuesta original del grupo | [`docs/propuesta_proyecto.md`](docs/propuesta_proyecto.md) |
| Perfilado del archivo 2019 | [`reports/perfilado_captura-puerto-flota-2019.md`](reports/perfilado_captura-puerto-flota-2019.md) |

Lo que pide el enunciado y dónde está en el PDF:

| Requisito | Sección del PDF |
| --- | --- |
| Portada con nombre y apellido de los integrantes | Portada |
| Descripción del contexto y del problema a resolver | 1. Contexto y problema |
| Descripción del dataset: fuente, características y semántica de las variables | 2. Descripción del dataset |
| Acceso al dataset original | 3. Acceso al dataset |
| Propuesta de tareas de preprocesamiento y limpieza | 4. Propuesta de limpieza y preprocesamiento |

Fechas: el PDF se sube hasta el **24/09 a las 17 h** (lo sube un solo integrante). La presentación de 5 minutos es el 24 o el 25/09, en el turno que asigne la cátedra, con al menos un integrante presente. La devolución es en los encuentros del 1 y 2 de octubre.

## Primera revisión del archivo 2019

Resumen del perfilado automático ([reporte completo](reports/perfilado_captura-puerto-flota-2019.md)):

| Tema | Qué muestra el archivo 2019 |
| --- | --- |
| Lectura | Codificación Latin-1 (ISO-8859-1) con fin de línea CRLF. `provincia_id` y `departamento_id` tienen ceros a la izquierda y hay que leerlos como texto. |
| Coordenadas | 216 registros (7,1 %) sin latitud ni longitud, todos de «otros puertos Buenos Aires», que no tiene coordenadas en ningún registro. |
| Duplicados | 0 filas idénticas. 392 filas coinciden en fecha, flota, puerto y especie pero difieren en `especie_agrupada` (31 especies figuran en más de una agrupación). |
| Fecha | Cubre de enero a noviembre de 2019. Noviembre tiene 94 registros, contra 246–347 del resto de los meses. |
| Meses sin registro | No hay capturas en cero. De 351 series especie–puerto, 24 tienen registros en los 11 meses y 214 en 5 meses o menos. |
| Captura | De 1 kg a 18.622.724 kg. Mediana 2.680,5 kg, media 223.264 kg. |
| Consistencia | La correlación de log10(captura) entre meses consecutivos de una misma serie es 0,09. Hay registros para contrastar con las planillas oficiales, por ejemplo 9.569.699 kg de centolla en Caleta Olivia / Paula en abril de 2019. |

## Estructura del repositorio

```text
.
├── data/
│   ├── README.md                         # origen de los datos y cómo agregar el archivo 2010–2018
│   ├── raw/captura-puerto-flota-2019.csv # copia sin modificar del archivo publicado
│   └── referencias/coordenadas_puertos.csv  # una fila por puerto, para completar coordenadas
├── docs/
│   ├── propuesta_proyecto.md             # propuesta original del grupo
│   ├── img/                              # logo y tabla de variables del portal
│   └── entrega_inicial/
│       ├── Entrega_Inicial_Grupo12.pdf
│       ├── Presentacion_Entrega_Inicial_Grupo12.pdf
│       ├── entrega_inicial.md            # fuente del PDF
│       ├── presentacion.html             # fuente de las diapositivas
│       ├── guia.md                       # guía para la defensa
│       └── assets/                       # estilos, fuentes (OFL) y figuras
├── reports/
│   └── perfilado_captura-puerto-flota-2019.md
├── src/
│   ├── perfilado.py                      # perfilado de los CSV y figuras
│   ├── coordenadas.py                    # tabla de coordenadas por puerto y completado
│   └── generar_pdf.py                    # genera los PDF con Chrome/Chromium/Edge
└── requirements.txt
```

## Cómo reproducir

```bash
pip install -r requirements.txt

# Perfilado (reporte en reports/ y figuras en docs/entrega_inicial/assets/fig/)
python src/perfilado.py data/raw/captura-puerto-flota-2019.csv

# Con el archivo 2010–2018 descargado en data/raw/ (el reporte del último archivo compara categorías con el anterior)
python src/perfilado.py data/raw/<archivo-2010-2018>.csv data/raw/captura-puerto-flota-2019.csv

# Tabla de coordenadas por puerto (conserva las coordenadas cargadas a mano)
python src/coordenadas.py data/raw/captura-puerto-flota-2019.csv

# Regenerar los PDF después de editar entrega_inicial.md o presentacion.html
python src/generar_pdf.py              # documento y diapositivas
python src/generar_pdf.py documento    # solo el documento
```

`generar_pdf.py` usa Google Chrome, Chromium o Microsoft Edge en modo headless. Si no encuentra el navegador, indicá la ruta con la variable de entorno `CHROME`.

## Próximos pasos

1. Descargar el archivo 2010–2018 en `data/raw/` y correr el perfilado y `src/coordenadas.py` sobre ambos archivos. Si aparece un puerto real sin coordenadas, buscarlas y anotarlas en `data/referencias/coordenadas_puertos.csv`.
2. Si cambian los valores de 2010–2018, actualizar la tabla de la sección 2.2 de `entrega_inicial.md` y regenerar el PDF.
3. Contrastar los totales de captura con las planillas oficiales de desembarques del Ministerio.
4. Análisis exploratorio y definición del criterio de anomalía.

## Pautas del TP a tener presentes

- Grupos de 4 a 5 integrantes. En la defensa final tienen que estar todos.
- No se aceptan comparativas de modelos ni datasets académicos o totalmente sintéticos.
- El trabajo debe ser inédito.
- La IA generativa solo se permite para código y material de presentación. Las decisiones, su justificación, el análisis de resultados y las conclusiones tienen que ser del grupo.
