# Cuadernos de ejemplo de la cátedra: qué hacen y cómo los aplicamos

Este documento resume los 8 cuadernos de ejemplo que compartió la cátedra (en [`docs/material_catedra/`](material_catedra/)), el procedimiento que se repite en todos y cómo se refleja cada punto en nuestra notebook final.

## 1. Qué hace cada cuaderno

| Cuaderno | Tema | Pasos y técnicas que muestra | Qué tomamos para nuestro trabajo |
| --- | --- | --- | --- |
| `02_A_ClasificacionKnn_Iris` | KNN, clasificación | Renombrar columnas, `shape`, `pairplot` por clase, `LabelEncoder`, partición 80/20, k = √n, matriz de confusión y `classification_report`. | Reporte de clasificación y matriz de confusión (sección 10). |
| `03_A_ClasificacionSVM_wine` | SVM, clasificación multiclase desbalanceada | `isnull`, `value_counts` de la clase, `info`, `describe`. Análisis univariado con caja, histograma y densidad. `pairplot`, **ANOVA (`f_oneway`) de cada variable contra la clase**, mapa de correlación, `StandardScaler`. La conclusión: el modelo falla en las clases raras, y se propone reducir el alcance a las clases frecuentes. | El formato univariado de tres paneles (4.2.4, 7.3), el ANOVA por variable (7.6) y la discusión de qué hacer con las clases raras (6.2). |
| `Clasificación_con_Arboles_de_Decisión` (hongos) | Árbol de decisión, *pre-pruning* | Elimina variables con faltantes o dominadas por una categoría. Histogramas apilados por clase, tablas de contingencia y **χ² de independencia**. Partición estratificada y `max_depth`. **Explicita el criterio rector**: no clasificar un venenoso como comestible. | χ² con V de Cramér para las categóricas (7.6), histogramas apilados por clase (7.4) y el criterio de qué error cuesta más (6.3). |
| `03_B_Ensamble_Hongos` | *Bagging* | `BaggingClassifier` con árboles y sus hiperparámetros. Advierte el sobreajuste cuando la exactitud llega a 1. | El bosque aleatorio presentado como extensión del *bagging* (9.1) y la brecha entre entrenamiento y prueba (10.1). |
| `Clustering_con_K_Means_en_California_Housing` | K-Means | EDA previo, `StandardScaler`, **método del codo y Silhouette** para elegir K, caracterización de los grupos con tablas y la advertencia de que "más clusters no significa mejores clusters". | La tipología de pesquerías con K-Means (4.6). |
| `Explorando_el_dataset_de_granos_de_arroz_con_PCA` | PCA | Análisis univariado, `pairplot`, estandarización, varianza explicada acumulada, cargas de las componentes y gráfico de las componentes coloreado por clase. Incluye una **decisión explícita sobre los valores atípicos**: no eliminarlos. | PCA de las especies (4.6) y de las candidatas coloreadas por clase (7.4), y la decisión sobre los valores atípicos (4.2.4, 7.3). |
| `RegresionLineal` | Regresión lineal | Correlación, partición, MAE, MSE, RMSE, R², histograma y gráfico de residuos. | No aplica directamente: nuestro problema es de clasificación. |
| `knn_ventas_ecommerce_v7` | KNN regresor sobre series temporales | **Fuga de información (*data leakage*)**: excluye variables que no se conocen al predecir y las controla con `assert`. Rezagos, media móvil y "misma semana del año anterior". **Partición cronológica** (nunca aleatoria), `TimeSeriesSplit` y análisis de residuos en el tiempo. | Es el cuaderno más cercano a nuestro problema. Lo usamos para el control explícito de fuga con `assert` (7.2), los rezagos y la referencia al mismo mes del año anterior (6, 7), y la partición y validación temporal (7.5, 9). |

## 2. El procedimiento común de la cátedra y dónde está en nuestra notebook

| Paso que se repite en los cuadernos | Dónde está en nuestra notebook |
| --- | --- |
| Contexto del problema y objetivo | 1 |
| Carga de datos y descripción de las variables | 3, 4.2 |
| Inspección: `shape`, `info`, `describe`, faltantes, duplicados, `value_counts` de la clase | 4.1.1 (archivo abierto), 4.2.4 (panel oficial), 6.1 (Tabla de valores de la clase) |
| Análisis univariado: caja, histograma y densidad | 4.2.4 (desembarque), 7.3 (candidatas) |
| Decisión explícita sobre valores atípicos | 4.2.4, 5.1, 7.3 |
| Análisis bivariado contra la clase | 7.4 (cajas por clase, barras apiladas) |
| Correlación entre variables | 7.6 (Pearson y redundancia) |
| Pruebas: ANOVA para numéricas y χ² para categóricas | 7.6 (con Welch, Kruskal-Wallis, Holm y V de Cramér, como pidió la devolución) |
| Escalado cuando el algoritmo usa distancias | 4.6 (K-Means), 7.4 (PCA). El bosque aleatorio no lo necesita (9.1). |
| Evitar la fuga de información en series temporales | 5.2, 7.2 (tabla y `assert`) |
| Partición: estratificada en datos independientes, cronológica en series | 7.5 (cronológica) |
| Codo y Silhouette (K-Means), varianza explicada (PCA) | 4.6, 7.4 |
| Matriz de confusión y `classification_report` | 10.1 |
| Clases desbalanceadas: no usar la exactitud; sobremuestreo, submuestreo o pesos de costo; curva ROC | 6.3, 9.1, 10.1, 10.2 |
| Conclusiones orientadas al objetivo y al costo de los errores | 6.3, 10.4, 12 |

## 3. Diferencias con los ejemplos de clase, y por qué

- **Partición.** Los cuadernos de iris, vinos y hongos usan `train_test_split` aleatorio. Nosotros usamos una partición por años, como el cuaderno de ventas, porque nuestros datos son series temporales y una partición aleatoria mezclaría el futuro con el pasado.
- **Pruebas estadísticas.** El cuaderno de vinos usa el ANOVA clásico. Nosotros lo complementamos con Welch, porque la prueba de Levene muestra varianzas distintas entre clases; con Kruskal-Wallis, porque varias variables no son normales; y con la corrección de Holm, porque se prueban 39 variables a la vez.
- **Separación de las clases.** En los ejemplos (iris, arroz, hongos) las clases se separan casi a simple vista y la exactitud llega al 97–100 %. En nuestro problema la proyección PCA muestra las anomalías mezcladas con los meses normales (7.4). Por eso el F1 macro esperable es moderado y la evaluación pone el foco en el uso práctico: la lista mensual de especies con mayor riesgo (10.4).
- **Clases raras.** El cuaderno de vinos propone, como tarea, reducir el alcance a las clases frecuentes. Nosotros evaluamos cuatro esquemas de clases. Mantenemos las tres clases porque la clase más chica (53 aumentos) todavía se puede aprender, y la severidad, que daría clases demasiado chicas, se usa para evaluar y no como clase (6.2, 10.5).

## 4. Para la defensa

Preguntas que pueden surgir a partir de los ejemplos de clase:

- **¿Por qué no usaron `train_test_split`?** Porque mezcla meses futuros en el entrenamiento: es fuga de información, como muestra el cuaderno de ventas (7.2, 7.5).
- **¿Por qué no escalaron las variables?** El bosque aleatorio divide por umbrales y no usa distancias. Sí se escala para K-Means y PCA (4.6, 7.4).
- **¿Por qué no balancearon con SMOTE?** Porque interpola historias de especies distintas y crea combinaciones de rezagos imposibles. Se usan pesos de clase, el enfoque sensible al costo de la Unidad 6 (9.1).
- **¿Por qué no usaron PCA como entrada del modelo?** Porque hacen falta 24 componentes para el 95 % de la varianza, y las componentes mezclan variables de distinto significado y le quitan interpretabilidad al modelo (7.4).
- **¿Para qué sirvió K-Means?** Para ver si las especies forman tipos de pesquería. Solo apareció una división clara, entre pesquerías de pulso y continuas, y no mejoró el modelo: se descartó con evidencia (4.6, 7.7).
