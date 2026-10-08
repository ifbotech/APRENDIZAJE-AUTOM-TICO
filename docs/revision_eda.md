# Revisión del EDA del grupo

**Notebook revisado:** `Grupo_Nro_12_Tema_Deteccion_Anomalias_Capturas_Pesqueras.ipynb` (commit `70a645f`).

**Cómo se hizo:** leí las 50 celdas, sus salidas y los 12 gráficos guardados. No pude volver a ejecutar el notebook, porque este entorno no puede descargar el CSV 2010–2018 del portal. Por eso, las pruebas de código se hicieron sobre el archivo 2019 y sobre una réplica sintética del flujo del notebook. Todo el código del anexo está probado.

> La redacción de las observaciones y conclusiones del EDA tiene que ser del grupo (pauta 12). Esta revisión marca problemas y propone correcciones; cómo las interpretan y escriben lo deciden ustedes.

---

## Resumen

| Prioridad | Tema | Qué pasa | Qué hacer |
| --- | --- | --- | --- |
| **1 · Crítico** | Calidad de `captura` | Las propias salidas del notebook muestran que los kilos no se parecen a los desembarques reales por especie, puerto y flota, aunque el total mensual sí es razonable. | Correr el diagnóstico A, contrastar con las estadísticas oficiales y hablarlo con las profesoras **antes** de seguir con la etiqueta y el modelo. |
| **2 · Alta** | La etiqueta | Al completar con 0 los meses sin desembarque, la etiqueta marca sobre todo "hubo o no hubo desembarque", no capturas fuera de lo normal. | Correr el diagnóstico B y redefinir cómo se tratan los meses en cero. |
| **3 · Alta** | Devolución de las profesoras | Siguen pendientes las tres clases, las coordenadas de los puertos agregados y las variables de clima. La fecha sí quedó bien tratada. | Ver la sección 5. |
| **4 · Media** | Errores de código | La escala (MAD) se rompe con NaN, `flota_principal` usa datos del mes a predecir, el filtro de series mira años futuros y el early stopping valida al azar. | Correcciones C1 a C5 del anexo. |
| **5 · Media** | Pauta 7 | Se entrena una regresión logística y se compara contra el boosting en una tabla. | Dejar un solo modelo y referencias simples, y confirmarlo con las profesoras. |
| **6 · Media** | Texto contra evidencia | Cuatro afirmaciones del texto no coinciden con las salidas. | Ver la sección 8. |

---

## 1. Lo que está bien

- **Estructura clara:** carga, EDA, limpieza justificada, dataset limpio, acceso y modelo.
- **Carga reproducible:** se descarga del portal oficial, se prueban dos codificaciones y se normalizan las columnas.
- **Atención a la fuga de información:** casi todas las predictoras usan `shift(1)`, y el "esperado" usa solo años anteriores.
- **Etiqueta bien pensada:** mediana del mismo mes en años anteriores y puntaje robusto (MAD). Además se registra el sentido (caída o aumento).
- **Tratamiento temporal completo**, que era uno de los pedidos de la devolución: año, mes con seno y coseno, rezagos 1, 2, 3 y 12, ventanas móviles y división por tiempo (2016 / 2017 / 2018).
- **Métricas acordes al desbalance:** PR-AUC, recall y F1, sin usar la exactitud.
- **Diccionario de variables con su rol**, separando claramente las columnas que no se usan como predictoras.
- **Decisiones razonables:** las coordenadas faltantes se identifican bien en la sección 3.2, se suman las filas repetidas en lugar de borrarlas, y se usa `log1p` y un filtro de series con poca historia.

---

## 2. Crítico: `captura` no parece reflejar desembarques reales

### 2.1 Evidencia en las propias salidas del notebook (2010–2018)

1. **Concentración baja.** "Las 5 especies principales concentran el 26,4 % de la captura total". En las estadísticas oficiales, merluza hubbsi, langostino y calamar Illex explican la mayor parte de los desembarques argentinos.
2. **Ranking de especies.** Rayas nep, lenguados nep y pescadilla aparecen por encima del langostino, y mero, corvina y pez gallo por encima del calamar Illex.
3. **Ranking de puertos.** General Lavalle aparece segundo, con unas 920 mil t en 9 años. En cambio, Puerto Madryn tiene unas 70 mil t, Puerto Deseado unas 45 mil, Rawson unas 20 mil y Ushuaia ni siquiera está entre los 15 primeros, aunque esos puertos patagónicos son de los principales desembarcos de langostino, calamar y merluza.
4. **Ranking de flotas.** "Rada o ría", que son barcos chicos de costa, tiene la mayor captura (unas 2,5 millones de t), por encima de fresqueros y congeladores. Los poteros, la flota del calamar, suman unas 60 mil t en 9 años.
5. **Estacionalidad del calamar Illex.** El mapa de calor reparte su captura casi pareja en el año, con 47 % entre julio y diciembre. La pesquería de Illex se concentra en la primera mitad del año.
6. **Serie de merluza hubbsi en Mar del Plata.** Muestra muchos meses cerca de 0 t y picos aislados de 15.000 a 27.000 t. En la realidad, la merluza se desembarca en Mar del Plata todos los meses.
7. **Distribución por categoría.** Peces, crustáceos y moluscos tienen prácticamente la misma distribución de `log1p(captura)` en el boxplot.
8. **Primeras filas del dataset limpio.** El abadejo en Mar del Plata pasa de 680 kg a 116.925 kg, luego a 13.778.127 kg y vuelve a 1.230 kg en meses consecutivos.

En contraste, **el total mensual sí es razonable**: entre 60 y 80 mil t por mes, unas 750 mil t por año. El total parece bien; lo que no cierra es cómo se reparte entre especies, puertos y flotas.

### 2.2 Evidencia en el archivo 2019 (prueba propia)

- **La especie no explica nada.** Explica el 3,2 % de la varianza de log10(captura). Si se mezclan los kilos al azar entre las especies de una misma celda mes–puerto–flota, da 3,1 % ± 0,4 %: es decir, dentro de cada celda los kilos no tienen relación con la especie.
- **No hay persistencia.** La correlación entre meses consecutivos de una misma serie es 0,09, y quitando el nivel propio de cada serie da −0,12.
- **Totales bajos.** Enero a noviembre de 2019 suma 55 mil t de merluza hubbsi, 52 mil t de langostino y 36 mil t de calamar Illex. Conviene contrastarlo con las cifras oficiales del año.

### 2.3 Qué hacer

1. **Correr el diagnóstico A** (anexo) sobre `df_raw` 2010–2018. Da los mismos indicadores y una tabla de toneladas anuales por especie.
2. **Contrastar con las estadísticas oficiales** de desembarques de la Subsecretaría de Pesca: totales anuales de merluza hubbsi, langostino y calamar Illex, y de Puerto Madryn, Rawson y Puerto Deseado.
3. **Si se confirma, hablarlo con las profesoras antes de seguir.** Opciones para proponerles:
   - *Cambiar de fuente:* usar las planillas oficiales de desembarques mensuales del Ministerio, que tienen las mismas variables. El problema y el planteo no cambian.
   - *Cambiar la unidad de análisis* a puerto–mes o puerto–flota–mes. Solo sirve si se verifica que los totales por puerto sí son correctos, y el punto 3 de la sección 2.1 sugiere que tampoco.
   - En cualquier caso, **documentarlo como hallazgo del EDA**: detectar un problema de calidad del dato es parte del proceso que evalúa la materia.
4. **Leer los resultados del modelo con cuidado.** Con una variable objetivo que no refleja la realidad, un PR-AUC de 0,33 no muestra que el modelo anticipe anomalías reales (ver secciones 3 y 7).

---

## 3. La etiqueta hoy mide sobre todo "hubo o no hubo desembarque"

**El mecanismo:**

- Al completar con 0 los meses sin registro, `log1p(0) = 0`.
- En series intermitentes, la mediana del mismo mes en años anteriores ("esperado") muchas veces también es 0, o un valor alto si ese mes solía tener desembarques.
- Resultado: un mes en cero donde se esperaba captura da una **caída** con z muy negativo, y cualquier desembarque en un mes que solía estar en cero da un **aumento**.

**Evidencia en el notebook:**

- El histograma de z tiene un **pico marcado en z = 0**: esa barra tiene unas 2.200 filas, contra unas 800 de las vecinas. Probablemente son meses en cero cuyo esperado también es 0, que quedan "normales" de forma trivial; el diagnóstico B lo confirma o lo descarta. También hay acumulaciones en ±10.
- La serie de ejemplo que eligieron, langostino en San Antonio Este, es casi toda ceros con desembarques esporádicos, y la mayoría de los puntos rojos son justamente esas apariciones.
- El 30 % de los últimos 12 meses son ceros en promedio (`prop_sin_desembarque_12m`), y al menos un 25 % de los `lag_1` valen 0.
- La correlación alta entre rezagos (0,5 a 0,6) se explica en buena parte por la alternancia entre 0 y valores positivos, no por una persistencia de los kilos.
- Las predictoras más importantes son `anomalias_12m`, `anomalia_lag1` y `media_12`, o sea, rachas de anomalías y nivel de actividad reciente, que es lo esperable si las anomalías son tramos de "sin desembarque".

**Qué hacer:**

1. **Correr el diagnóstico B** (anexo). Muestra qué proporción de caídas son meses en cero y qué proporción de aumentos tenían un esperado casi cero.
2. **Decidir cómo tratar los meses en cero.** Opciones a evaluar en el EDA:
   - etiquetar solo los meses con desembarque y modelar aparte si hubo o no desembarque;
   - exigir que las series tengan un mínimo de meses activos dentro de cada mes calendario;
   - tratar "sin desembarque" como un estado propio en lugar de una caída.
3. **Pasar a tres clases** (caída, normal, aumento), como sugirieron las profesoras. El notebook ya calcula `tipo_anomalia`, así que es cambiar el objetivo y las métricas (corrección C4).
4. **Analizar la sensibilidad** de la proporción de caídas y aumentos a K, al piso y a la historia mínima (diagnóstico D). Ya lo tienen en "Próximos pasos"; además les da con qué justificar por qué K = 3.

---

## 4. Errores de código y fugas de información

| # | Dónde | Problema | Impacto | Corrección |
| --- | --- | --- | --- | --- |
| C1 | 4.1, cálculo de `escala` | `np.median` devuelve NaN si la ventana tiene algún NaN, así que la escala recién existe cuando hay 24 residuos completos. | Las etiquetas arrancan en **2014** en vez de **2013**: se pierde un año de entrenamiento (el texto dice "los primeros dos años", pero son cuatro). | Usar `np.nanmedian` (verificado: el primer mes etiquetado pasa a 2013-01). |
| C2 | Paso 7, `flota_principal` | Se calcula con los datos **del mes t**, y en los meses sin registro se rellena con la moda de toda la serie, incluido el futuro. | **Fuga de información**: el modelo ve qué flota desembarcó en el mes que tiene que anticipar. El impacto medido es chico (importancia 0,005), pero el error es conceptual. | Usar la flota principal del mes anterior y la categoría "Sin desembarque" en lugar de la moda. |
| C3 | Paso 9, filtro de 36 meses | Cuenta los meses activos en todo 2010–2018, incluidos validación y prueba. | Selecciona series según el futuro (sesgo de selección leve). | Contar solo hasta el corte de entrenamiento (2016-12). |
| C4 | Sección 7, modelo | El objetivo es binario aunque ya existe `tipo_anomalia`. | No responde a la devolución. | Modelo multiclase con `tipo_anomalia` y métricas por clase. |
| C5 | Sección 7, `early_stopping=True` | El boosting elige cuándo parar con un 10 % de filas de entrenamiento **al azar**, no por tiempo. | Mezcla meses en la validación interna. | Pasar `X_val` y `y_val` de 2017 al `fit` o, si la versión de scikit-learn no lo permite, usar `early_stopping=False` y elegir `max_iter` mirando 2017. |
| C6 | Predictoras, `anio` | El año de prueba (2018) está fuera del rango de entrenamiento: el árbol lo trata igual que el último año visto. | No aporta y puede confundir. | Sacarlo o justificarlo. |
| C7 | Paso 8, rango activo | Las series se completan hasta su último mes observado, que puede ser futuro. | Leve. | Completar hasta el corte de cada partición. |
| C8 | Paso 1, `.str.title()` | Cambia los nombres ("Mar Del Plata", "Rada O Ría"). | Complica cruzar con otras tablas, como las coordenadas o el clima. | Solo quitar espacios sobrantes. |
| C9 | Celda de importaciones | `warnings.filterwarnings("ignore")` oculta avisos de pandas y scikit-learn. | Puede esconder errores silenciosos. | Quitarlo. |

---

## 5. Devolución de las profesoras: estado en el notebook

| Pedido | Estado | Qué falta |
| --- | --- | --- |
| Más de dos clases (caída / aumento) | **Pendiente.** La introducción y el modelo siguen siendo binarios; `tipo_anomalia` se calcula pero no se usa. | Cambiar el objetivo a tres clases y medir por clase (C4). |
| Variables de clima o mareas | **Pendiente.** No se menciona. | Al menos una subsección con el plan (temperatura del mar, viento, índice El Niño, con rezago) y por qué no mareas. Conviene esperar a validar `captura`. |
| Completar latitud y longitud | **Parcial.** El paso 4 no puede completar los dos puertos agregados («otros puertos» y «otros puertos Buenos Aires»): quedan 927 filas sin coordenadas en el dataset limpio. | Decidir entre excluirlos o asignarles una ubicación aproximada con una marca, y explicarles a las profesoras que no son puertos reales. |
| Tratamiento de la fecha | **Resuelto.** | Mencionarlo explícitamente en la tabla de limpieza: mes cíclico, rezagos, ventanas y división por tiempo. |

---

## 6. Mejoras al EDA

**Lo que falta analizar:**

- **Bloque de calidad del dato** (sección 2): diagnóstico A y contraste con las estadísticas oficiales.
- **Categorías especiales que no se comentan:**
  - la cuarta categoría «otras»;
  - la provincia «sin especificar»;
  - el puerto «otros puertos», aparte de «otros puertos Buenos Aires»;
  - `departamento` tiene 17 valores pero `departamento_id` tiene 18;
  - `provincia_id` llega hasta 99 y `departamento_id` hasta 99.999, que parecen códigos de "sin especificar".
- **Cobertura del filtro:** las 221 series que quedan, ¿qué porcentaje de los kilos totales representan?
- **Persistencia real:** la correlación entre meses consecutivos calculada solo sobre meses con desembarque y dentro de cada serie (diagnóstico A), no la matriz de correlación con los ceros incluidos.
- **Estacionalidad por especie y puerto** para las series principales, no solo por especie a nivel país.
- **Valores redondos:** el histograma de `log1p(captura)` muestra picos en valores puntuales (por ejemplo, alrededor de 3,5 y 4), que sugieren cifras redondeadas.
- **El archivo 2019**, y si sus categorías coinciden con las de 2010–2018.

**Forma:**

- Cada gráfico tiene que responder una pregunta y terminar en una observación del grupo con números.
- Las conclusiones de 3.7 hoy son generales: conviene que cada una cite la salida que la respalda.

---

## 7. Sección de modelo

- **Pauta 7.** La tabla "Azar / Regresión logística / Gradient Boosting" y la lista de alternativas descartadas pueden leerse como una comparación de modelos. Para justificar la elección alcanza con el argumento conceptual. Como referencia numérica, se pueden usar reglas simples que no son modelos: la prevalencia, o "anomalía si el mes anterior fue anomalía". Conviene confirmarlo con las profesoras.
- **Elegir una sola librería.** El texto menciona "HistGradientBoostingClassifier / LightGBM".
- **Tres clases**, con matriz de confusión, precisión y sensibilidad por clase, PR-AUC por clase y F1 macro (corrección C4).
- **Interpretar con cautela.** Las predictoras más importantes son las anomalías recientes. Antes de presentar el resultado como "anticipación", conviene revisar los aciertos: ¿son rachas de meses sin desembarque? Esto se ve con el diagnóstico B aplicado a las predicciones.
- **Validación:** usar 2017 para el early stopping y el umbral, y 2018 solo al final (C5).

---

## 8. Afirmaciones del texto que no coinciden con la evidencia

| Dónde | Qué dice el texto | Qué muestran las salidas |
| --- | --- | --- |
| 3.7, conclusiones | "Hay una fuerte concentración de la captura en pocas especies" | Las 5 principales concentran el 26,4 %. |
| 3.7, conclusiones | "Las coordenadas... se pueden completar desde otros registros del mismo puerto" | La sección 3.2 muestra que los faltantes son de dos puertos agregados que no tienen coordenadas en ningún registro, y el paso 4 deja 2.380 faltantes. |
| 3.5, después del mapa de calor | "Cada especie tiene un patrón estacional propio (zafras)" | El mapa no muestra temporadas claras: por ejemplo, el calamar Illex tiene 47 % de su captura entre julio y diciembre. |
| 4.1, etiqueta | "Los primeros dos años de cada serie quedan sin etiqueta" | El período etiquetado empieza en 2014-01, es decir, cuatro años sin etiqueta (C1). |

Cómo reescribir cada una lo deciden ustedes; lo importante es que el texto y la evidencia digan lo mismo.

---

## 9. Orden de trabajo sugerido

1. **Validar el dato:** diagnóstico A más el contraste oficial. Llevar el resultado a las profesoras.
2. **Corregir C1 a C3**, que son cambios chicos que mejoran la etiqueta y eliminan fugas.
3. **Redefinir la etiqueta:** tratamiento de los meses en cero (diagnóstico B), tres clases y sensibilidad (diagnóstico D).
4. **Coordenadas** de los puertos agregados y **plan de clima**.
5. **Modelo:** multiclase, validación temporal y referencias simples (C4 y C5, más la pauta 7).
6. **Texto:** alinear observaciones y conclusiones con la evidencia (sección 8), escritas por el grupo.

---

## Anexo · Código probado

### A. Diagnóstico de calidad de `captura`

Se corre sobre `df_raw` 2010–2018, antes de la limpieza.

```python
def diagnostico_calidad(df, n_perm=20, semilla=0):
    """¿Los kilos tienen relación con la especie y con el mes anterior?"""
    rng = np.random.default_rng(semilla)
    d = df[df.captura > 0].copy()
    d["y"] = np.log10(d.captura)

    def eta2(y, g):
        m = y.mean(); gg = y.groupby(g.values)
        return float((gg.size() * (gg.mean() - m) ** 2).sum() / ((y - m) ** 2).sum())

    # 1) ¿Cuánto explica la especie dentro de cada celda mes–puerto–flota?
    celda = d.fecha.astype(str) + "|" + d.puerto + "|" + d.flota
    real = eta2(d.y, d.especie)
    perm = []
    for _ in range(n_perm):
        yp = d.y.groupby(celda.values).transform(lambda s: pd.Series(rng.permutation(s.values), index=s.index))
        perm.append(eta2(yp, d.especie))
    print(f"Varianza de log10(captura) explicada por la especie: {real:.3f} | "
          f"mezclando los kilos entre especies de la misma celda mes–puerto–flota: {np.mean(perm):.3f} ± {np.std(perm):.3f}")

    # 2) Persistencia: meses consecutivos con desembarque, dentro de cada serie
    clave = ["especie", "puerto", "flota", "especie_agrupada"]
    f = pd.to_datetime(d.fecha.astype(str).str[:7], format="%Y-%m")
    d["t"] = f.dt.year * 12 + f.dt.month
    d = d.sort_values(clave + ["t"])
    g = d.groupby(clave)
    d["y_prev"], d["t_prev"] = g.y.shift(1), g.t.shift(1)
    pares = d[(d.t - d.t_prev) == 1]
    r = np.corrcoef(pares.y, pares.y_prev)[0, 1]
    dm = pares.assign(yc=pares.y - pares.groupby(clave).y.transform("mean"),
                      ypc=pares.y_prev - pares.groupby(clave).y_prev.transform("mean"))
    r_intra = np.corrcoef(dm.yc, dm.ypc)[0, 1]
    print(f"Correlación entre meses consecutivos con desembarque: {r:.2f} (n = {len(pares):,}) | "
          f"dentro de cada serie: {r_intra:.2f}")

    # 3) Totales anuales para contrastar con las estadísticas oficiales
    tabla = (d.assign(anio=f.dt.year).groupby(["anio", "especie"]).captura.sum().div(1e6)
               .unstack().reindex(columns=["Merluza hubbsi", "Langostino", "Calamar Illex"]).round(1))
    print("\nMiles de toneladas por año de las tres especies principales (contrastar con las cifras oficiales):")
    display(tabla)

diagnostico_calidad(df_raw)
```

En el archivo 2019 da: especie 0,032 contra 0,031 ± 0,004 mezclando; correlación 0,09, y −0,12 dentro de cada serie. En datos reales de desembarques se esperaría que la especie explique mucho más que al mezclar, y una correlación claramente positiva.

### B. Composición de las anomalías

Se corre después de la sección 4.1, con `et` y `agg` del notebook.

```python
d = et.assign(sin_desembarque=et.captura.eq(0), esperado_casi_cero=et.esperado.lt(1))
display(d.groupby("tipo_anomalia")[["sin_desembarque", "esperado_casi_cero"]].mean().round(2))
print(f"Filas con z exactamente 0: {(et.z == 0).mean():.1%} | "
      f"de esas, meses sin desembarque: {et[et.z == 0].captura.eq(0).mean():.1%}")
```

Si la mayoría de las caídas son meses en cero, o la mayoría de los aumentos tenían un esperado casi cero, la etiqueta está midiendo presencia o ausencia.

### C. Correcciones

```python
# C1 · Escala robusta que tolera NaN en la ventana (reemplaza la lambda de la sección 4.1)
mad = lambda x: np.nanmedian(np.abs(x - np.nanmedian(x)))
agg["escala"] = agg.groupby(["especie", "puerto"]).residuo.transform(
    lambda s: s.shift(1).rolling(24, min_periods=12).apply(mad, raw=True)) * 1.4826
agg["escala"] = agg.escala.clip(lower=PISO)

# C2 · Flota principal del mes anterior, sin rellenar con la moda de toda la serie
#      (en el paso 8, reemplazar el relleno con la moda por esta línea)
agg["flota_principal"] = agg.flota_principal.fillna("Sin desembarque")
#      (en la sección 4.2)
agg["flota_principal_lag1"] = agg.groupby(["especie", "puerto"]).flota_principal.shift(1)
FEATURES_CAT = ["categoria", "especie_agrupada", "provincia", "puerto", "flota_principal_lag1"]

# C3 · Filtro de historia usando solo los años de entrenamiento (paso 9)
CORTE = pd.Timestamp("2016-12-01")
meses_activos = agg[(agg.captura > 0) & (agg.fecha <= CORTE)].groupby(["especie", "puerto"]).size()
validas = meses_activos[meses_activos >= MIN_MESES].index

# C4 y C5 · Tres clases y early stopping con la validación temporal
TARGET = "tipo_anomalia"
y = df_limpio[TARGET]
hgb = HistGradientBoostingClassifier(categorical_features="from_dtype", class_weight="balanced",
                                     learning_rate=0.05, max_iter=400, early_stopping=True,
                                     random_state=RANDOM_STATE)
hgb.fit(X[tr], y[tr], X_val=X[va], y_val=y[va])   # si la versión de scikit-learn no acepta X_val:
                                                  # early_stopping=False y elegir max_iter mirando 2017
pred = hgb.predict(X[va])
print(classification_report(y[va], pred, zero_division=0))
clases = ["caida", "normal", "aumento"]
display(pd.DataFrame(confusion_matrix(y[va], pred, labels=clases), index=clases, columns=clases))
proba = pd.DataFrame(hgb.predict_proba(X[va]), columns=hgb.classes_, index=X[va].index)
for c in ["caida", "aumento"]:
    print(f"PR-AUC {c}: {average_precision_score(y[va].eq(c), proba[c]):.2f} (prevalencia {y[va].eq(c).mean():.2f})")
```

Importar además `confusion_matrix` desde `sklearn.metrics`. Con C4 hay que quitar `df_limpio[TARGET].astype(int)` en la sección 4.2: `tipo_anomalia` es texto.

### D. Sensibilidad de la etiqueta a K y al piso

```python
escala_base = agg.groupby(["especie", "puerto"]).residuo.transform(
    lambda s: s.shift(1).rolling(24, min_periods=12).apply(mad, raw=True)) * 1.4826
filas = []
for piso in (0.10, 0.25, 0.50):
    z_ = (agg.residuo / escala_base.clip(lower=piso)).dropna()
    for k in (2.0, 2.5, 3.0, 3.5):
        filas.append({"piso": piso, "K": k, "caida": (z_ < -k).mean(), "aumento": (z_ > k).mean()})
display(pd.DataFrame(filas).pivot(index="K", columns="piso", values=["caida", "aumento"]).round(3))
```
