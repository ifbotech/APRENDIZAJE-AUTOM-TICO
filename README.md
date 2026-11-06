<p align="center"><img src="docs/img/logo_ugr.png" alt="Universidad del Gran Rosario" width="96"></p>

# Detección de anomalías en las capturas pesqueras argentinas

**Aprendizaje Automático · Universidad del Gran Rosario · Trabajo Práctico Grupal 2026, 2.º cuatrimestre · Grupo 12**

| Integrantes |
| --- |
| Barnetche, Iñaki Francisco |
| Bernal, Alejandro Matias |
| Paredes, Sebastian Pablo |
| Rodrigues, David Ezequiel |

**Estado (noviembre de 2026):** trabajo final entregado (notebook versión 5.5). Falta la defensa en video, que la cátedra presenta los días 12 y 13 de noviembre.

## Contenido

1. [Entregables](#1-entregables)
2. [La materia y el trabajo práctico](#2-la-materia-y-el-trabajo-práctico)
3. [El proyecto](#3-el-proyecto)
4. [Respuesta a las devoluciones de la cátedra](#4-respuesta-a-las-devoluciones-de-la-cátedra)
5. [Historia del trabajo, versión por versión](#5-historia-del-trabajo-versión-por-versión)
6. [Uso de IA generativa](#6-uso-de-ia-generativa)
7. [La defensa](#7-la-defensa)
8. [Estructura del repositorio](#8-estructura-del-repositorio)
9. [Cómo reproducir](#9-cómo-reproducir)
10. [Pendientes](#10-pendientes)

---

## 1. Entregables

| Entregable | Archivo |
| --- | --- |
| **Notebook final ejecutada, versión 5.5** (la entregada) | [`Grupo_Nro_12_Tema_Deteccion_Anomalias_Capturas_Pesqueras.ipynb`](Grupo_Nro_12_Tema_Deteccion_Anomalias_Capturas_Pesqueras.ipynb) |
| Abrir en Colab | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ifbotech/APRENDIZAJE-AUTOM-TICO/blob/claude/festive-lamport-xe0jzs/Grupo_Nro_12_Tema_Deteccion_Anomalias_Capturas_Pesqueras.ipynb) |
| Dataset de modelado | [`data/procesados/dataset_modelo.csv`](data/procesados/dataset_modelo.csv) · [descarga directa](https://raw.githubusercontent.com/ifbotech/APRENDIZAJE-AUTOM-TICO/claude/festive-lamport-xe0jzs/data/procesados/dataset_modelo.csv) |
| Guion del video de defensa | [`docs/guion_defensa.md`](docs/guion_defensa.md) |
| Presentación de defensa (16 diapositivas) | Artifact de claude.ai, privado del dueño de la cuenta: hay que compartirlo desde *Share* para que lo vea el resto del grupo |

La notebook se entrega ejecutada. En Colab corre sin archivos previos: descarga cada fuente la primera vez, unos 3 a 5 minutos en total.

---

## 2. La materia y el trabajo práctico

### 2.1 Cronograma

| Fecha | Hito | Material |
| --- | --- | --- |
| 24/09/2026 | Entrega inicial: propuesta, dataset y prueba preliminar | [PDF](docs/entrega_inicial/Entrega_Inicial_Grupo12.pdf) · [diapositivas](docs/entrega_inicial/Presentacion_Entrega_Inicial_Grupo12.pdf) · [propuesta editable](docs/propuesta_proyecto.md) |
| Después del 24/09 | Devolución de la entrega inicial | [`docs/recomendaciones_y_plan_eda.md`](docs/recomendaciones_y_plan_eda.md) |
| Antes de la entrega final | EDA del grupo y su revisión por la cátedra | [`entregas/eda/Grupo_Nro_12_EDA_v2.ipynb`](entregas/eda/Grupo_Nro_12_EDA_v2.ipynb) · [revisión](docs/revision_eda.md) |
| Fines de octubre | Entrega final: notebook ejecutada (versión 5.5) | Este repositorio |
| 12 y 13/11/2026 | Defensa: la cátedra presenta el video de cada grupo y hace preguntas | [`docs/guion_defensa.md`](docs/guion_defensa.md) |

### 2.2 Pautas del trabajo práctico

1. Grupos de 4 a 5 integrantes; en la defensa tienen que estar todos.
2. Datos reales: no se aceptan datasets académicos ni totalmente sintéticos.
3. El trabajo tiene que ser inédito.
4. Un solo modelo: **no se aceptan comparaciones de modelos**. La persistencia y "siempre normal" que usa el trabajo son líneas base (reglas sin aprendizaje), no modelos alternativos.
5. Formato de citas y de tablas y figuras según las normas APA (7.ª ed.).
6. **IA generativa (pauta 12):** se permite para el código y el material de presentación. Las decisiones, su justificación, el análisis de resultados y las conclusiones tienen que ser del grupo (ver la sección 6).
7. Técnicas: se pidió usar las vistas en clase y, si se usa alguna que no, explicarla. La versión final usa **solo técnicas vistas en clase**.

### 2.3 Contenidos de la materia que usa el proyecto

| Unidad o material | Qué se usó | Dónde (notebook) |
| --- | --- | --- |
| Unidad 1 · Selección de atributos | Métodos de filtro (χ², ANOVA, Pearson), envoltura (eliminación hacia atrás) e integrados (importancia del modelo) | 4.9, 6, 10.1 |
| Unidad 3 · Aprendizaje supervisado avanzado | Árboles de decisión, *bagging* y bosque aleatorio | 8 |
| Unidad 4 · Aprendizaje no supervisado | PCA y K-Means (codo y Silhouette), estandarización | 4.6, 4.9.1 |
| Unidad 6 · Conjuntos desbalanceados | Pesos de clase (sensible al costo), por qué no SMOTE ni submuestreo, matriz de confusión, precisión, exhaustividad, F1 macro, curva ROC | 4.7.3, 8.1, 9 |
| Estadística descriptiva | Mediana, promedio, cuartiles, diagrama de caja y regla de Tukey (1,5 × RIC) | 4.2.6, 4.7 |

Cuadernos de práctica de la cátedra (en [`docs/material_catedra/`](docs/material_catedra/)) y qué se tomó de cada uno:

| Cuaderno | Qué se tomó |
| --- | --- |
| Análisis exploratorio (iris) | `describe(include="all")`, histogramas y densidades por clase, gráficos de pares |
| KNN con iris | Matriz de confusión y `classification_report` |
| SVM con vinos | Análisis univariado en tres paneles, ANOVA (`f_oneway`), discusión de clases raras |
| Árboles de decisión con hongos | χ² de independencia (`chi2_contingency`), histogramas apilados por clase, criterio rector (qué error cuesta más) |
| Ensamble con hongos | Bosque aleatorio como extensión del *bagging*, brecha entre entrenamiento y prueba |
| K-Means con California Housing | Codo, Silhouette y caracterización de grupos |
| PCA con granos de arroz | Varianza explicada, cargas, proyección por clase y decisión de no eliminar atípicos |
| KNN de ventas (series temporales) | Control de fuga con `assert`, rezagos, partición cronológica y `TimeSeriesSplit` |

El detalle está en [`docs/analisis_notebooks_catedra.md`](docs/analisis_notebooks_catedra.md).

---

## 3. El proyecto

### 3.1 Problema

Para cada especie y cada mes, usando solo la información disponible hasta el mes anterior, anticipar si el desembarque será una **caída anómala**, **normal** o un **aumento anómalo** respecto de lo habitual para esa especie en ese mes del año. Es una **clasificación supervisada de tres clases**.

| Clase | Código | Significado | Acción que habilita |
| --- | --- | --- | --- |
| `caida` | −1 | Muy por debajo de lo habitual | Prever faltante de materia prima, revisar la pesquería |
| `normal` | 0 | Dentro del rango esperable | Ninguna |
| `aumento` | 1 | Muy por encima de lo habitual | Reforzar frío, almacenamiento y transporte |

### 3.2 Datos

| Fuente | Contenido | Uso |
| --- | --- | --- |
| Subsecretaría de Pesca y Acuicultura, estadísticas oficiales 2014–2025 | Desembarques por especie y mes, especie y puerto, especie y flota | Base del modelo |
| Datos abiertos MAGyP 2010–2019 (propuesto en la entrega inicial) | Desembarques por mes, flota, puerto y especie | Solo auditoría: se descartó (3.3) |
| NOAA OISST, ONI y SAM | Temperatura del mar en tres zonas, El Niño, Modo Anular del Sur | Candidatas de clima |
| Calendario astronómico | Mareas vivas e iluminación lunar | Candidatas de mareas |
| Coordenadas de 22 puertos | Ubicación de cada puerto | Candidatas geográficas |

**Unidad de análisis:** una especie en un mes. Son **43 especies** (al menos 10 t por mes y actividad en el 60 % de los meses, el 99,8 % del volumen) durante **108 meses** etiquetados (2017–2025): **4.644 observaciones**. Entrenamiento 2017–2023 (3.612) y prueba 2024–2025 (1.032), separados por año, nunca al azar.

### 3.3 El hallazgo más importante: el dataset abierto no servía

Antes de modelar se auditó el conjunto de datos abierto propuesto en la entrega inicial:

- **Persistencia:** la correlación del desembarque de un mes con el del mes anterior es −0,008 en el archivo abierto, contra 0,397 en las estadísticas oficiales. Una actividad real tiene memoria.
- **Contraste con las tablas oficiales:** el total nacional coincide, pero el reparto no. Las tres especies principales figuran con el 19 % de su volumen oficial y los grandes puertos patagónicos con el 2–3 %.

Conclusión: en el archivo abierto los kilos no corresponden a la especie, el puerto ni la flota de cada registro. Por eso el proyecto cambió a las estadísticas oficiales del mismo organismo.

### 3.4 La variable objetivo (construida dentro del EDA)

Solo con herramientas vistas en clase:

1. **Esperado:** mediana del desembarque del mismo mes en los años anteriores (al menos 2).
2. **Nivel habitual:** promedio de los 12 meses anteriores, con un piso de 10 t.
3. **Desvío relativo:** (desembarque − esperado) / nivel, comparable entre especies grandes y chicas.
4. **Regla del diagrama de caja:** con los cuartiles de los desvíos de los 24 meses anteriores, el mes es `caida` si queda por debajo de Q1 − 1,5 × RIC y `aumento` si queda por encima de Q3 + 1,5 × RIC.

Resultado: 87,8 % normal, 6,5 % caída (300 casos) y 5,8 % aumento (268 casos). Se compararon cuatro esquemas (binario, tres clases, cinco por severidad y caídas a cero aparte) y se eligieron tres clases porque son las que cambian la acción.

### 3.5 Principales hallazgos del EDA

- Tres especies (merluza hubbsi S41, langostino y calamar) explican el 75 % del volumen, y las especies van de pocas toneladas a 50.000 t por mes.
- Cada especie tiene su temporada: lo normal se define por especie y por mes del año.
- Las series tienen memoria: autocorrelación de 0,49 a un mes y de 0,52 a doce meses.
- K-Means separa 6 pesquerías de pulso de 37 continuas (Silhouette 0,58).
- En el PCA las clases no se separan: hace falta un modelo no lineal.

### 3.6 Selección de variables y modelo

- **41 candidatas:** historia de la especie, historia de anomalías, mes, categoría, contexto nacional, geografía y flota, clima, luna y mareas, y tipología de K-Means. Todas usan solo información hasta el mes anterior, verificado con `assert`.
- **Filtro (41 → 33 columnas):** χ² para las categóricas (repetido con la clase agrupada cuando había frecuencias esperadas bajas), ANOVA para las numéricas y Pearson con |r| > 0,90 para la redundancia. El umbral de 0,90 se justificó frente al 0,7 de la Unidad 1: con 0,7 el F1 de validación baja de 0,533 a 0,521.
- **Envoltura (33 → 30 columnas):** eliminación hacia atrás por familias con validación temporal 2020–2023. Salen el contexto nacional y el clima.
- **Modelo:** un bosque aleatorio de 500 árboles, con `class_weight="balanced_subsample"`, `min_samples_leaf=10` y `max_features="sqrt"`, elegidos en una grilla de 6 combinaciones.
- **Integrado:** la variable más importante es el salto estacional esperado (0,218), seguida de los desvíos de los meses anteriores.

### 3.7 Resultados en la prueba 2024–2025

| Métrica | Bosque aleatorio | Persistencia | Siempre normal |
| --- | ---: | ---: | ---: |
| F1 macro | **0,484** | 0,455 | 0,314 |
| Exactitud balanceada | **0,548** | 0,457 | 0,333 |
| Exhaustividad de caída | **0,542** | 0,322 | 0 |
| F1 de caída | **0,362** | 0,317 | 0 |
| F1 de aumento | **0,195** | 0,132 | 0 |
| ROC-AUC de caída | **0,879** | — | — |
| ROC-AUC alerta sin sentido | **0,788** | — | — |

- El modelo supera a la persistencia en 2024 (F1 macro 0,487) y en 2025 (0,481).
- Detecta el **70 % de las caídas extremas**, contra el 52 % de la persistencia.
- **Uso recomendado:** como lista de prioridades. Revisando cada mes las 3 especies con más riesgo se encuentra el 42 % de las caídas con 35 % de precisión. Si se revisa solo la primera, la precisión es 6,6 veces la del azar.
- "Siempre normal" tiene la mejor exactitud (0,892) sin detectar nada, y por eso se evalúa por clase.
- Las cifras corresponden a la ejecución entregada, con pandas 2.2.3 y scikit-learn 1.6.1. Con otras versiones varían en el segundo o tercer decimal.

### 3.8 Limitaciones y próximos pasos

- **Resolución nacional:** las tablas oficiales no cruzan especie, puerto y mes a la vez.
- **Aumentos difíciles de anticipar:** ROC-AUC de 0,705.
- **Faltan variables de gestión y mercado:** vedas, cupos, conflictos y precios.
- **Algunas diferencias de la selección son chicas:** quedan dentro de la variación propia del bosque (hasta 0,016).
- **Probabilidades infladas por los pesos de clase:** sirven para ordenar, no como riesgo real.

**Próximos pasos:**

1. Sumar variables de gestión y de mercado.
2. Usar una referencia adaptativa basada en los años recientes.
3. Probar el clima con rezagos de 6 a 24 meses.
4. Reentrenar el modelo cada año.
5. Informar al organismo el problema del dato abierto.

---

## 4. Respuesta a las devoluciones de la cátedra

La sección 2 de la notebook tiene una fila por comentario. En resumen:

| Comentario | Respuesta |
| --- | --- |
| Separar anomalía por exceso y por déficit | Tres clases (`caida`, `normal`, `aumento`) y comparación de cuatro esquemas |
| Qué hacer con «otros puertos» y sus coordenadas faltantes | Se excluyen de la latitud y la longitud; su peso entra como `prop_otros_puertos` |
| `log1p` es una técnica no vista | Se quitó: el desembarque se mide en proporción del nivel de cada especie |
| Falta el análisis de las variables categóricas | Análisis de flota, categoría, provincia y puerto, con conclusiones |
| EDA incompleto: pruebas según el tipo de variable | χ², ANOVA y Pearson, más envoltura e integrado (Unidad 1) |
| Construir la variable objetivo dentro del EDA y analizar la dependencia | La variable objetivo está en 4.7 y la dependencia en 4.9, dentro del EDA |
| ¿Binaria o tres clases? | Tres clases, con tabla de valores y códigos |
| No se entiende "línea base" | Definida: regla simple sin aprendizaje que el modelo debe superar |
| Incorporar clima o mareas | Incorporados y descartados con evidencia |
| Completar latitud y longitud | 22 puertos con coordenadas; se probaron centroide, zonas y concentración |
| Tratamiento de las variables temporales | Grilla mensual, mes categórico, rezagos hasta t − 1 y partición por años |
| Técnicas no vistas sin explicar | Solo técnicas vistas en clase |

---

## 5. Historia del trabajo, versión por versión

| Versión | Qué cambió | Modelo (F1 macro de prueba) |
| --- | --- | --- |
| Entrega inicial (24/09) | Dataset abierto 2010–2019, serie especie–puerto, etiqueta binaria con \|z\| > 3, propuesta de *gradient boosting* con regresión logística como base | Prueba preliminar |
| Auditoría y plan del EDA | Se detecta que el dataset abierto no sirve; se pasa a las estadísticas oficiales y a tres clases | — |
| Primera notebook final | EDA según los cuadernos de la cátedra, etiqueta con log y MAD, varias técnicas no vistas (Welch, Holm, V de Cramér, PR-AUC, *bootstrap*, permutación, etc.), 12 variables | 0,464 |
| Simplificación | Se quitan 11 técnicas no vistas, se integran el EDA de un integrante y el cuaderno de EDA de la cátedra, títulos sin preguntas y un comentario por celda; 24 columnas | 0,474 |
| Versión 3 | La variable objetivo y la dependencia pasan dentro del EDA; métodos de la Unidad 1; χ² con control de frecuencias; justificación del umbral de 0,90; una fila por comentario de la cátedra | 0,474 |
| Solo técnicas de clase | Se quitan `log1p`, MAD y el índice de Herfindahl-Hirschman; etiqueta con la regla del diagrama de caja; 30 columnas | 0,492 (pandas 3, scikit-learn 1.9) |
| Versión 4 (grupo) | Título de la sección 10, piso de 10 t documentado, cifra del χ² y cita a la Unidad 1 | 0,492 |
| Versión 5 (grupo) | Texto reescrito por el grupo y nueva ejecución con pandas 2.2.3 y scikit-learn 1.6.1 | 0,484 |
| **Versión 5.5 (entregada)** | Revisión de la V5: un comentario por celda, una cifra corregida (75 %) y registro más formal en una docena de expresiones | **0,484** |

Además se prepararon la presentación de defensa (16 diapositivas con notas del orador) y el guion del video, y se actualizaron este README y [`data/README.md`](data/README.md).

---

## 6. Uso de IA generativa

Durante el trabajo se usó un asistente de IA (Claude) para:

- el código de la notebook, la descarga y el procesamiento de los datos, y las figuras;
- borradores de texto de las versiones 1 a 4, que el grupo revisó;
- la revisión técnica de las versiones del grupo, para que las cifras del texto coincidan con las salidas;
- la presentación de defensa, el guion del video y este README, que son material de presentación.

Por la pauta 12, el análisis, las justificaciones y las conclusiones tienen que ser del grupo. La versión 5 es el texto reescrito por el grupo, y la 5.5 solo agrega correcciones de forma. Cada integrante tiene que poder explicar y defender las decisiones de su parte.

---

## 7. La defensa

**Formato:**

- Video grabado de **5 minutos como máximo**, con la participación de todos los integrantes.
- Se sube a YouTube como **Oculto** (cualquiera con el enlace puede verlo), y el enlace va en un documento que se entrega en la tarea.
- La cátedra lo presenta el 12 o el 13 de noviembre; el día exacto se avisa antes.
- Ese día tienen que estar todos, porque los docentes pueden hacer preguntas.
- La audiencia no es necesariamente técnica, así que no se muestra código.

**Reparto del guion** (completo en [`docs/guion_defensa.md`](docs/guion_defensa.md)):

| Parte | Integrante | Tiempo | Tema |
| --- | --- | --- | --- |
| 1 | Iñaki Barnetche | 0:00–1:10 | Presentación, problema y calidad de los datos |
| 2 | Alejandro Bernal | 1:10–2:20 | Qué es una anomalía y qué mostró el análisis |
| 3 | Pablo Paredes | 2:20–3:30 | Variables probadas y el modelo |
| 4 | David Rodrigues | 3:30–4:50 | Resultados, uso, límites y cierre |

El guion incluye también las preguntas probables, con su respuesta corta y quién la contesta.

---

## 8. Estructura del repositorio

```text
.
├── Grupo_Nro_12_Tema_Deteccion_Anomalias_Capturas_Pesqueras.ipynb   # ENTREGA FINAL (versión 5.5, ejecutada)
├── data/
│   ├── README.md                 # fuentes, contenido de cada carpeta y cómo leer los archivos
│   ├── raw/                      # conjunto abierto 2010–2018 y 2019 (auditoría, sección 4.1)
│   ├── oficial/                  # tablas oficiales 2014–2026 (HTML descargado sin modificar)
│   ├── externos/                 # temperatura del mar por zona, ONI y SAM
│   ├── referencias/              # coordenadas de los puertos
│   └── procesados/dataset_modelo.csv
├── entregas/eda/                 # notebooks del EDA presentadas anteriormente
├── docs/
│   ├── guion_defensa.md          # guion del video y preguntas probables
│   ├── analisis_notebooks_catedra.md
│   ├── recomendaciones_y_plan_eda.md
│   ├── revision_eda.md
│   ├── propuesta_proyecto.md
│   ├── entrega_inicial/          # PDF, diapositivas y guía de la entrega inicial
│   └── material_catedra/         # cuadernos de ejemplo y apuntes de las unidades 3, 4 y 6
├── reports/                      # perfilado del archivo 2019
├── src/                          # scripts de perfilado, coordenadas y PDF de la entrega inicial
└── requirements.txt
```

---

## 9. Cómo reproducir

```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace Grupo_Nro_12_Tema_Deteccion_Anomalias_Capturas_Pesqueras.ipynb
```

O en Colab: *Entorno de ejecución → Ejecutar todas*. La notebook usa los archivos de `data/` si existen y, si no, los descarga de las fuentes originales; si una fuente no responde, usa la copia de este repositorio. Con la semilla fija (`SEMILLA = 42`) los resultados son reproducibles dentro de una misma versión de las librerías.

---

## 10. Pendientes

- [ ] Correr la notebook una vez en Colab: la versión entregada se ejecutó en Windows.
- [ ] Grabar las cuatro partes del video, editarlo (5 minutos como máximo), subirlo a YouTube como Oculto y entregar el documento con el enlace.
- [ ] Compartir la presentación de defensa con el grupo desde *Share*.
- [ ] Prepararse para las preguntas en vivo (tabla en [`docs/guion_defensa.md`](docs/guion_defensa.md)).
- [ ] Opcional: renombrar la rama principal del repositorio a `main` y actualizar los enlaces de Colab y del dataset.
