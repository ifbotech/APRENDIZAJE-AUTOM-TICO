# Cuadernos de ejemplo de la cátedra: qué hacen y cómo los aplicamos

Este documento resume los 9 cuadernos de ejemplo que compartió la cátedra (en [`docs/material_catedra/`](material_catedra/)), el procedimiento que se repite en todos y cómo se refleja cada punto en nuestra notebook final.

## 1. Qué hace cada cuaderno

| Cuaderno | Tema | Pasos y técnicas que muestra | Qué tomamos para nuestro trabajo |
| --- | --- | --- | --- |
| `AnalisisExploratorio` (iris) | Análisis exploratorio | `shape`, `info`, `describe(include="all")`, faltantes, histogramas y **curvas de densidad por clase**, diagramas de caja por clase, **gráficos de dispersión de pares** y `pairplot`, matriz de correlación. | `describe(include="all")` del archivo abierto (4.1.1), caja de `log1p(desembarque)` por categoría (4.2.6), histogramas y densidades por clase (4.9.1), gráficos de pares y `pairplot` (4.9.1). |
| `02_A_ClasificacionKnn_Iris` | KNN, clasificación | Renombrar columnas, `shape`, `pairplot` por clase, `LabelEncoder`, partición 80/20, k = √n, matriz de confusión y `classification_report`. | Reporte de clasificación y matriz de confusión (sección 10). |
| `03_A_ClasificacionSVM_wine` | SVM, clasificación multiclase desbalanceada | `isnull`, `value_counts` de la clase, `info`, `describe`. Análisis univariado con caja, histograma y densidad. `pairplot`, **ANOVA (`f_oneway`) de cada variable contra la clase**, mapa de correlación, `StandardScaler`. La conclusión: el modelo falla en las clases raras, y se propone reducir el alcance a las clases frecuentes. | El formato univariado de tres paneles (4.2.6, 4.8.3), el ANOVA por variable (4.9.2) y la discusión de qué hacer con las clases raras (4.7.2). |
| `Clasificación_con_Arboles_de_Decisión_Dataset_Agaricus_Lepiota_Pre_pruning` (hongos) | Árbol de decisión, *pre-pruning* | Elimina variables con faltantes o dominadas por una categoría. Histogramas apilados por clase, tablas de contingencia y **χ² de independencia**. Partición estratificada y `max_depth`. **Explicita el criterio rector**: no clasificar un venenoso como comestible. | χ² para las categóricas (4.9.2), histogramas apilados por clase (4.9.1) y el criterio de qué error cuesta más (4.7.3). |
| `03_B_Ensamble_Hongos` | *Bagging* | `BaggingClassifier` con árboles y sus hiperparámetros. Advierte el sobreajuste cuando la exactitud llega a 1. | El bosque aleatorio presentado como extensión del *bagging* (8.1) y la brecha entre entrenamiento y prueba (9.1). |
| `Clustering_con_K_Means_en_California_Housing` | K-Means | EDA previo, `StandardScaler`, **método del codo y Silhouette** para elegir K, caracterización de los grupos con tablas y la advertencia de que "más clusters no significa mejores clusters". | La tipología de pesquerías con K-Means (4.6). |
| `Explorando_el_dataset_de_granos_de_arroz_con_PCA` | PCA | Análisis univariado, `pairplot`, estandarización, varianza explicada acumulada, cargas de las componentes y gráfico de las componentes coloreado por clase. Incluye una **decisión explícita sobre los valores atípicos**: no eliminarlos. | PCA de las especies (4.6) y de las candidatas coloreadas por clase (4.9.1), y la decisión sobre los valores atípicos (4.2.6, 4.8.3). |
| `RegresionLineal` | Regresión lineal | Correlación, partición, MAE, MSE, RMSE, R², histograma y gráfico de residuos. | No aplica directamente: nuestro problema es de clasificación. |
| `knn_ventas_ecommerce_v7` | KNN regresor sobre series temporales | **Fuga de información (*data leakage*)**: excluye variables que no se conocen al predecir y las controla con `assert`. Rezagos, media móvil y "misma semana del año anterior". **Partición cronológica** (nunca aleatoria), `TimeSeriesSplit` y análisis de residuos en el tiempo. | Es el cuaderno más cercano a nuestro problema. Lo usamos para el control explícito de fuga con `assert` (4.8.2), los rezagos y la referencia al mismo mes del año anterior (6, 7), y la partición y validación temporal (5.3, 9). |

## 2. El procedimiento común de la cátedra y dónde está en nuestra notebook

| Paso que se repite en los cuadernos | Dónde está en nuestra notebook |
| --- | --- |
| Contexto del problema y objetivo | 1 |
| Carga de datos y descripción de las variables | 3, 4.2 |
| Inspección: `shape`, `info`, `describe`, faltantes, duplicados, `value_counts` de la clase | 4.1.1 (archivo abierto), 4.2.6 (panel oficial), 4.7.1 (Tabla de valores de la clase) |
| Análisis univariado: caja, histograma y densidad | 4.2.6 (desembarque), 4.8.3 (candidatas) |
| Decisión explícita sobre valores atípicos | 4.2.6, 5.1, 4.8.3 |
| Análisis bivariado contra la clase | 4.9.1 (cajas, histogramas y densidades por clase, barras apiladas, gráficos de pares) |
| Correlación entre variables | 4.9.3 (Pearson y redundancia, umbral justificado frente al 0,7 de la Unidad 1) |
| Pruebas: ANOVA para numéricas y χ² para categóricas (Unidad 1, «Selección de atributos») | 4.9.2 (`f_oneway` y `chi2_contingency`, como en los cuadernos de vinos y de árboles de decisión con hongos) |
| Métodos de selección de la Unidad 1: filtro, envoltura e integrado | 4.9.2–4.9.3 (filtro), 6 (envoltura), 10.1 (integrado) |
| Construir la variable objetivo dentro del EDA y analizar la dependencia | 4.7 (variable objetivo), 4.9 (dependencia) |
| Escalado cuando el algoritmo usa distancias | 4.6 (K-Means), 4.9.1 (PCA). El bosque aleatorio no lo necesita (8.1). |
| Evitar la fuga de información en series temporales | 5.2, 4.8.2 (tabla y `assert`) |
| Partición: estratificada en datos independientes, cronológica en series | 5.3 (cronológica) |
| Codo y Silhouette (K-Means), varianza explicada (PCA) | 4.6, 4.9.1 |
| Matriz de confusión y `classification_report` | 9.1 |
| Clases desbalanceadas: no usar la exactitud; sobremuestreo, submuestreo o pesos de costo; curva ROC | 4.7.3, 8.1, 9.1, 9.2 (ROC por clase y de la alerta sin sentido) |
| Conclusiones orientadas al objetivo y al costo de los errores | 4.7.3, 9.4, 11 |

## 3. Diferencias con los ejemplos de clase, y por qué

- **Partición.** Los cuadernos de iris, vinos y hongos usan `train_test_split` aleatorio. Nosotros usamos una partición por años, como el cuaderno de ventas, porque nuestros datos son series temporales y una partición aleatoria mezclaría el futuro con el pasado.
- **Pruebas estadísticas.** Usamos las mismas pruebas que los cuadernos (ANOVA clásico, χ² y Pearson). Como las variables no son normales y la clase `aumento` es chica, las pruebas funcionan como filtro inicial, y la decisión final se verifica dentro del modelo con validación temporal (6).
- **Separación de las clases.** En los ejemplos (iris, arroz, hongos) las clases se separan casi a simple vista y la exactitud llega al 97–100 %. En nuestro problema la proyección PCA muestra las anomalías mezcladas con los meses normales (4.9.1). Por eso el F1 macro esperable es moderado y la evaluación pone el foco en el uso práctico: la lista mensual de especies con mayor riesgo (9.4).
- **Clases raras.** El cuaderno de vinos propone, como tarea, reducir el alcance a las clases frecuentes. Nosotros evaluamos cuatro esquemas de clases. Mantenemos las tres clases porque todas tienen casos suficientes (216 aumentos, la más chica) y cada una lleva a una acción distinta. La severidad no cambia la acción, así que se usa para evaluar y no como clase (4.7.2, 9.5).

## 4. Para la defensa

Preguntas que pueden surgir a partir de los ejemplos de clase:

- **¿Por qué no usaron `train_test_split`?** Porque mezcla meses futuros en el entrenamiento: es fuga de información, como muestra el cuaderno de ventas (4.8.2, 5.3).
- **¿Por qué no escalaron las variables?** El bosque aleatorio divide por umbrales y no usa distancias. Sí se escala para K-Means y PCA (4.6, 4.9.1).
- **¿Por qué no balancearon con SMOTE?** Porque interpola historias de especies distintas y crea combinaciones de rezagos imposibles. Se usan pesos de clase, el enfoque sensible al costo de la Unidad 6 (8.1).
- **¿Por qué no usaron PCA como entrada del modelo?** Porque hacen falta 23 componentes para el 95 % de la varianza, y las componentes mezclan variables de distinto significado y le quitan interpretabilidad al modelo (4.9.1).
- **¿Para qué sirvió K-Means?** Para ver si las especies forman tipos de pesquería. Apareció una división clara, entre 6 pesquerías de pulso y 37 continuas (Silhouette 0,58), y la variable resultante quedó en el modelo: quitarla baja el F1 macro de validación de 0,533 a 0,528 (4.6, 6).

## 5. Simplificación: solo técnicas vistas en clase

En la versión final se quitaron las técnicas que no se vieron en la asignatura: prueba de permutación, codificación cíclica del mes, ANOVA de Welch, Kruskal-Wallis, Levene, corrección de Holm, V de Cramér, ajuste de umbrales de decisión, PR-AUC, importancia por permutación y *bootstrap*. Se reemplazaron por técnicas de clase:

| Técnica quitada | Reemplazo visto en clase |
| --- | --- |
| Codificación cíclica (seno y coseno) del mes | Mes como variable categórica, probado con χ² |
| Welch, Kruskal-Wallis, Levene, Holm | ANOVA de un factor (`f_oneway`) |
| V de Cramér | χ² de independencia con el control de frecuencias esperadas |
| Ajuste de umbrales de decisión | Clase con mayor probabilidad y pesos de clase (`class_weight`) |
| PR-AUC | Curva ROC y ROC-AUC por clase (Unidad 6) |
| *Bootstrap* por bloques | Métricas por año de prueba (2024 y 2025) |
| Importancia por permutación | Importancia del bosque aleatorio (`feature_importances_`) |
| Prueba de permutación (auditoría del archivo abierto) | Persistencia de las series y contraste con las tablas oficiales |
| `log1p` | Desembarque sin transformar, medido en proporción del nivel habitual de cada especie |
| Mediana con MAD y puntaje *z* robusto | Regla del diagrama de caja (cuartiles y 1,5 × RIC) sobre los desvíos recientes |
| Índice de Herfindahl-Hirschman | Proporción desembarcada en el puerto principal |

Después se quitaron también las tres que quedaban: `log1p` (el desembarque ya no se transforma: cada mes se mide en proporción del nivel habitual de su especie), la mediana con MAD y el puntaje *z* robusto (la etiqueta usa ahora la regla del diagrama de caja sobre los cuartiles de los desvíos recientes) y el índice de Herfindahl-Hirschman (reemplazado por la proporción desembarcada en el puerto principal). El trabajo final usa solo técnicas vistas en clase. La autocorrelación se presenta como una correlación de Pearson entre la serie y su rezago (4.3), y la exactitud balanceada como el promedio de la exhaustividad de cada clase (9.1).
