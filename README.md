<p align="center"><img src="docs/img/logo_ugr.png" alt="Universidad del Gran Rosario" width="96"></p>

# Detección de anomalías en las capturas pesqueras argentinas

**Aprendizaje Automático · Universidad del Gran Rosario · Trabajo Práctico Grupal 2026, 2.º cuatrimestre · Grupo 12**

| Integrantes |
| --- |
| Bernal, Alejandro Matias |
| Paredes, Sebastian Pablo |
| Rodrigues, David Ezequiel |
| Barnetche, Iñaki Francisco |

## Entrega final

| Entregable | Archivo |
| --- | --- |
| **Notebook ejecutada, versión 5.5** (EDA corregido, selección de variables, entrenamiento, evaluación y conclusiones) | [`Grupo_Nro_12_Tema_Deteccion_Anomalias_Capturas_Pesqueras.ipynb`](Grupo_Nro_12_Tema_Deteccion_Anomalias_Capturas_Pesqueras.ipynb) |
| Abrir en Colab | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ifbotech/APRENDIZAJE-AUTOM-TICO/blob/claude/festive-lamport-xe0jzs/Grupo_Nro_12_Tema_Deteccion_Anomalias_Capturas_Pesqueras.ipynb) |
| Dataset de modelado | [`data/procesados/dataset_modelo.csv`](data/procesados/dataset_modelo.csv) · [descarga directa](https://raw.githubusercontent.com/ifbotech/APRENDIZAJE-AUTOM-TICO/claude/festive-lamport-xe0jzs/data/procesados/dataset_modelo.csv) |

La notebook se entrega ya ejecutada. En Colab corre sin archivos previos: descarga cada fuente la primera vez, unos 3 minutos en total.

### El proyecto en breve

**Problema.** Para cada especie y cada mes, usando solo la información disponible hasta el mes anterior, anticipar si el desembarque será una **caída anómala**, **normal** o un **aumento anómalo** respecto de lo habitual para esa especie en ese mes del año. Es una clasificación supervisada de tres clases.

**Etiqueta.** Se construye solo con herramientas vistas en clase. Cada mes se compara con la mediana del mismo mes en años anteriores, la diferencia se mide en proporción del nivel habitual de la especie (promedio de los 12 meses anteriores) y se aplica la regla del diagrama de caja sobre los desvíos de los 24 meses anteriores: `caida` si el desvío queda por debajo de $Q_1 - 1{,}5 \cdot \text{RIC}$, `aumento` si queda por encima de $Q_3 + 1{,}5 \cdot \text{RIC}$ y `normal` en otro caso.

**Datos.**

- **Desembarques:** estadísticas oficiales de la Subsecretaría de Pesca y Acuicultura, 2014–2025, por especie y mes, especie y puerto, y especie y flota.
- **Temperatura del mar:** NOAA OISST.
- **Índices climáticos:** ONI y SAM, de NOAA CPC.
- **Coordenadas de los puertos.**

**Cambio de fuente.** En el EDA se comprobó que el conjunto de datos abierto propuesto en la entrega inicial tiene los kilos desacoplados de la especie, el puerto y la flota de cada registro. Lo muestran dos pruebas (sección 4.1 de la notebook):

- la persistencia de las series;
- el contraste con las tablas oficiales.

Por eso el modelo usa las estadísticas oficiales del mismo organismo.

**Modelo.** Un único bosque aleatorio con 30 columnas elegidas en dos pasos, solo con técnicas vistas en clase:

1. **Filtro** (Unidad 1, dentro del EDA): ANOVA de un factor para las numéricas, χ² para las categóricas (con control de frecuencias esperadas) y correlación de Pearson para la redundancia. Deja 33 columnas.
2. **Envoltura** (Unidad 1): eliminación hacia atrás por familias de variables, con validación temporal por años. Quita el clima y el contexto nacional, que no mejoran el modelo.

El método **integrado** (importancia del bosque aleatorio) se usa para interpretar el modelo.

Las variables del modelo son la historia de la especie, la historia de sus anomalías, la cantidad de puertos de desembarque, la clase del mes anterior, el mes del año y la tipología de pesquerías obtenida con K-Means.

### Resultados en el conjunto de prueba (2024–2025)

| Métrica | Bosque aleatorio | Línea base: persistencia | Línea base: siempre normal |
| --- | ---: | ---: | ---: |
| F1 macro | **0,484** | 0,455 | 0,314 |
| Exactitud balanceada | **0,548** | 0,457 | 0,333 |
| F1 caída | **0,362** (precisión 0,271, exhaustividad 0,542) | 0,317 | 0 |
| F1 aumento | **0,195** (13 de 52 detectados) | 0,132 | 0 |
| ROC-AUC caída | **0,879** | — | — |
| ROC-AUC alerta sin sentido (1 − P(normal)) | **0,788** | — | — |

El modelo detecta el 70 % de las caídas extremas y supera a la persistencia en 2024 y en 2025. Su uso recomendado es **priorizar**: si cada mes se revisan las 2 o 3 especies con mayor riesgo de caída, se detecta entre el 29 % y el 42 % de las caídas con una precisión del 35 %, unas seis veces más que al azar. Los aumentos son la clase más difícil de anticipar.

Las cifras corresponden a la ejecución entregada (pandas 2.2.3, scikit-learn 1.6.1). Con otras versiones pueden variar en el segundo o tercer decimal.

Las variables sugeridas por la cátedra se incorporaron y se evaluaron:

- **Latitud y longitud de los puertos:** con las coordenadas se calcularon el centroide, el reparto por zona y la concentración en el puerto principal; ninguna aporta con esta etiqueta. Entra al modelo la cantidad de puertos de desembarque.
- **Clima y mareas:** la temperatura del mar, El Niño, el SAM, las mareas vivas y la iluminación lunar tienen una relación nula o muy débil con la clase y no mejoran el modelo, así que se descartaron con esa evidencia (secciones 4.5, 4.9 y 6).
- **Variables temporales:** el mes se trata como variable categórica y entra al modelo, los rezagos y las ventanas terminan en el mes anterior y la partición es por años (secciones 5.2 y 5.3).

### El EDA sigue el procedimiento de los cuadernos de la cátedra

Cada paso del procedimiento de los cuadernos tiene su sección en la notebook:

- inspección del panel (`shape`, `info`, `describe`, faltantes y duplicados);
- análisis univariado de caja, histograma y densidad;
- análisis de las variables categóricas: flotas, provincias, puertos y categorías «otros»;
- **construcción de la variable objetivo dentro del EDA** (4.7), como pidió la cátedra;
- análisis de la dependencia con la variable objetivo (4.9): cajas, histogramas y densidades por clase, gráficos de pares;
- correlaciones;
- ANOVA y χ²;
- decisión sobre los valores atípicos;
- control explícito de fuga de información con `assert`;
- PCA y K-Means.

Además se compararon cuatro esquemas de clasificación de anomalías (binario, tres clases, cinco clases por severidad y caídas según su mecanismo) y se explicitó qué error es más costoso. La notebook integra también el EDA de un integrante del grupo ([`entregas/eda/Grupo_Nro_12_EDA_v3.ipynb`](entregas/eda/Grupo_Nro_12_EDA_v3.ipynb)): análisis de categóricas con nombres normalizados, categorías «otros», alerta sin sentido, diccionario de variables con roles y exportación del dataset.

El trabajo usa **solo técnicas vistas en clase**: la etiqueta se construye con la mediana, el promedio, los cuartiles y la regla del diagrama de caja, sin transformaciones logarítmicas ni estadísticos robustos fuera del programa. La sección 2 de la notebook responde, uno por uno, todos los comentarios de la cátedra. El detalle de los nueve cuadernos de la cátedra, dónde se aplicó cada uno y qué técnicas se reemplazaron está en [`docs/analisis_notebooks_catedra.md`](docs/analisis_notebooks_catedra.md).

## Historial de entregas

| Etapa | Material |
| --- | --- |
| Entrega inicial (24/09/2026) | [PDF](docs/entrega_inicial/Entrega_Inicial_Grupo12.pdf) · [diapositivas](docs/entrega_inicial/Presentacion_Entrega_Inicial_Grupo12.pdf) · [propuesta editable](docs/propuesta_proyecto.md) · [guía para la defensa](docs/entrega_inicial/guia.md) |
| Devolución y plan del EDA | [`docs/recomendaciones_y_plan_eda.md`](docs/recomendaciones_y_plan_eda.md) |
| EDA del grupo (versión revisada por la cátedra) | [`entregas/eda/Grupo_Nro_12_EDA_v2.ipynb`](entregas/eda/Grupo_Nro_12_EDA_v2.ipynb) · [revisión](docs/revision_eda.md) |
| EDA de un integrante (integrado a la notebook final) | [`entregas/eda/Grupo_Nro_12_EDA_v3.ipynb`](entregas/eda/Grupo_Nro_12_EDA_v3.ipynb) |
| Perfilado del archivo 2019 | [`reports/perfilado_captura-puerto-flota-2019.md`](reports/perfilado_captura-puerto-flota-2019.md) |

## Estructura del repositorio

```text
.
├── Grupo_Nro_12_Tema_Deteccion_Anomalias_Capturas_Pesqueras.ipynb   # ENTREGA FINAL (ejecutada)
├── data/
│   ├── README.md                 # fuentes, contenido de cada carpeta y cómo leer los archivos
│   ├── raw/                      # conjunto abierto 2010–2018 y 2019 (auditoría, sección 4.1)
│   ├── oficial/                  # tablas oficiales 2014–2026 (HTML descargado sin modificar)
│   ├── externos/                 # temperatura del mar por zona, ONI y SAM
│   ├── referencias/              # coordenadas de los puertos
│   └── procesados/dataset_modelo.csv
├── entregas/eda/                 # notebooks del EDA presentadas anteriormente
├── docs/                         # entrega inicial, recomendaciones, revisión del EDA y análisis de los cuadernos de la cátedra
│   └── material_catedra/         # cuadernos de ejemplo y apuntes de las unidades 3, 4 y 6
├── reports/                      # perfilado del archivo 2019
├── src/                          # scripts de perfilado, coordenadas y PDF de la entrega inicial
└── requirements.txt
```

## Cómo reproducir

```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace Grupo_Nro_12_Tema_Deteccion_Anomalias_Capturas_Pesqueras.ipynb
```

La notebook usa los archivos de `data/` si existen y, si no, los descarga de las fuentes originales. Con la semilla fija (`SEMILLA = 42`) los resultados son reproducibles.

## Pautas del TP a tener presentes

- Grupos de 4 a 5 integrantes. En la defensa final tienen que estar todos.
- No se aceptan comparativas de modelos ni datasets académicos o totalmente sintéticos. El trabajo usa **un solo modelo**; la persistencia y "siempre normal" son líneas base sin aprendizaje.
- El trabajo debe ser inédito.
- La IA generativa solo se permite para código y material de presentación. Las decisiones, su justificación, el análisis de resultados y las conclusiones tienen que ser del grupo.
