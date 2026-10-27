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
| **Notebook ejecutada** (EDA corregido, selección de variables, entrenamiento, evaluación y conclusiones) | [`Grupo_Nro_12_Tema_Deteccion_Anomalias_Capturas_Pesqueras.ipynb`](Grupo_Nro_12_Tema_Deteccion_Anomalias_Capturas_Pesqueras.ipynb) |
| Abrir en Colab | [![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ifbotech/APRENDIZAJE-AUTOM-TICO/blob/claude/festive-lamport-xe0jzs/Grupo_Nro_12_Tema_Deteccion_Anomalias_Capturas_Pesqueras.ipynb) |
| Dataset de modelado | [`data/procesados/dataset_modelo.csv`](data/procesados/dataset_modelo.csv) |

La notebook se entrega ya ejecutada. En Colab corre sin archivos previos: descarga cada fuente la primera vez, unos 3 minutos en total.

### El proyecto en breve

**Problema.** Para cada especie y cada mes, usando solo la información disponible hasta el mes anterior, anticipar si el desembarque será una **caída anómala**, **normal** o un **aumento anómalo** respecto de lo habitual para esa especie en ese mes del año. Es una clasificación supervisada de tres clases.

**Etiqueta.** Se compara el desembarque en escala logarítmica con la mediana del mismo mes en los años anteriores y se divide por una escala robusta (MAD de los 24 meses previos). El puntaje *z* resultante define la clase: `caida` si *z* < −2,5, `aumento` si *z* > 2,5 y `normal` en otro caso.

**Datos.**

- **Desembarques:** estadísticas oficiales de la Subsecretaría de Pesca y Acuicultura, 2014–2025, por especie y mes, especie y puerto, y especie y flota.
- **Temperatura del mar:** NOAA OISST.
- **Índices climáticos:** ONI y SAM, de NOAA CPC.
- **Coordenadas de los puertos.**

**Cambio de fuente.** En el EDA se comprobó que el conjunto de datos abierto propuesto en la entrega inicial tiene los kilos desacoplados de la especie, el puerto y la flota de cada registro. Lo muestran tres pruebas (sección 4.1 de la notebook):

- una prueba de permutación;
- la persistencia de las series;
- el contraste con las tablas oficiales.

Por eso el modelo usa las estadísticas oficiales del mismo organismo.

**Modelo.** Un único bosque aleatorio con 18 variables elegidas en dos pasos:

1. Pruebas por tipo de variable: ANOVA de Welch, Kruskal-Wallis, χ² con V de Cramér, corrección de Holm y redundancia por correlación de Pearson.
2. Verificación dentro del modelo con validación temporal por años.

### Resultados en el conjunto de prueba (2024–2025)

| Métrica | Bosque aleatorio | Regla: persistencia | Regla: siempre normal |
| --- | ---: | ---: | ---: |
| F1 macro | **0,496** (IC 95 %: 0,430–0,549) | 0,407 | 0,315 |
| Exactitud balanceada | **0,557** | 0,407 | 0,333 |
| F1 caída | 0,303 | 0,302 | 0 |
| F1 aumento | **0,276** | 0 | 0 |
| PR-AUC caída (azar = 0,093) | **0,300** | — | — |

El modelo supera a la regla de persistencia en el 99,2 % de las réplicas *bootstrap*. Su uso recomendado es **priorizar**: si cada mes se revisa la especie con mayor riesgo de caída, la alerta es correcta en el 42 % de los casos, 4,5 veces más que al azar.

Las variables climáticas y geográficas sugeridas por la cátedra se incorporaron y se evaluaron. No mejoraron el modelo, así que se descartaron con esa evidencia (secciones 7.3 y 7.4).

## Historial de entregas

| Etapa | Material |
| --- | --- |
| Entrega inicial (24/09/2026) | [PDF](docs/entrega_inicial/Entrega_Inicial_Grupo12.pdf) · [diapositivas](docs/entrega_inicial/Presentacion_Entrega_Inicial_Grupo12.pdf) · [propuesta editable](docs/propuesta_proyecto.md) · [guía para la defensa](docs/entrega_inicial/guia.md) |
| Devolución y plan del EDA | [`docs/recomendaciones_y_plan_eda.md`](docs/recomendaciones_y_plan_eda.md) |
| EDA del grupo (versión revisada por la cátedra) | [`entregas/eda/Grupo_Nro_12_EDA_v2.ipynb`](entregas/eda/Grupo_Nro_12_EDA_v2.ipynb) · [revisión](docs/revision_eda.md) |
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
├── entregas/eda/                 # notebook del EDA presentada anteriormente
├── docs/                         # entrega inicial, recomendaciones y revisión del EDA
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
- No se aceptan comparativas de modelos ni datasets académicos o totalmente sintéticos. El trabajo usa **un solo modelo**; la persistencia y "siempre normal" son reglas de referencia sin aprendizaje.
- El trabajo debe ser inédito.
- La IA generativa solo se permite para código y material de presentación. Las decisiones, su justificación, el análisis de resultados y las conclusiones tienen que ser del grupo.
