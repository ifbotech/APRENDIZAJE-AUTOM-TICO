# Recomendaciones y plan del EDA

**Grupo 12 · Detección de anomalías en las capturas pesqueras argentinas**

> Propuestas para conversar con las profesoras después de la devolución de la entrega inicial, y un plan para el análisis exploratorio (EDA). Ordena las opciones con lo que ya sabemos de los datos; las decisiones son del grupo.

---

## 1. Lo más importante, en cinco líneas

1. **Validar la variable `captura` en 2010–2018 antes que nada.** En 2019 los valores casi no se relacionan con el mes anterior ni con la especie. Si 2010–2018 tiene el mismo problema, hay que hablarlo ya con las profesoras.
2. **Pasar a tres clases** (caída anómala, normal, aumento anómalo) con un único modelo multiclase, como sugirieron.
3. **Decidir si el proyecto anticipa o detecta.** Si anticipa (información hasta t − 1), el clima entra con rezago; si detecta, puede usar el clima del mismo mes.
4. **Completar latitud y longitud y usarlas como variables numéricas.** Además permiten cruzar con datos de clima. Falta resolver «otros puertos Buenos Aires».
5. **Especificar el tratamiento temporal**: serie mensual completa, rezagos, estacionalidad y división de los datos por tiempo.

---

## 2. Recomendaciones según la devolución

### 2.1 Tres clases en lugar de dos

**Qué dijeron:** con dos clases puede quedar corto, porque las acciones ante un exceso y ante una falta son distintas.

**Recomendación:** separar "anómala" en **caída anómala** y **aumento anómalo**. Ya está en la definición original ("por una caída o por un aumento"), así que es una extensión natural.

- **Pauta 7:** sigue siendo un único modelo (multiclase), no una comparación de modelos.
- **La etiqueta necesita dos límites**, uno por debajo y otro por encima de lo habitual. Dos formas de construirla, para comparar en el EDA:
  - *Desvío respecto de lo estacional:* para cada serie y mes, comparar log(captura) con la mediana del mismo mes en los años anteriores y medir la distancia en desvíos robustos (MAD). Caída si queda muy por debajo; aumento si queda muy por arriba.
  - *Percentiles del mismo mes:* caída si está por debajo de un percentil bajo de los años anteriores; aumento si está por encima de uno alto.
- **Escala logarítmica:** "la mitad" y "el doble" quedan a la misma distancia, así que los dos límites se pueden definir de forma pareja.
- **Solo pasado:** "lo normal" de enero 2015 se calcula con eneros anteriores a 2015. Los primeros años sirven solo como historia y no tienen etiqueta.
- **Desbalance:** habrá dos clases raras. Para evaluar: matriz de confusión, precisión y sensibilidad de cada clase y F1 macro, no la exactitud sola.
- **Meses sin registro:** si se completan con 0, todos quedan como "caída anómala" (y log(0) no existe). Esta decisión impacta directo en la etiqueta.

### 2.2 Variables externas: clima

**Qué dijeron:** con las variables del dataset la predicción puede ser insuficiente; evaluar clima o mareas.

**Recomendación:** sumar dos o tres variables climáticas **mensuales** y dejar las mareas de lado.

- **Por qué no mareas:** tienen ciclos de horas y de unas dos semanas, así que en datos mensuales se promedian y casi no cambian de un mes a otro.
- **Qué sí cambia mes a mes, con fuentes públicas:**

| Variable | Por qué puede importar | Fuente pública |
| --- | --- | --- |
| Temperatura superficial del mar (y su anomalía) | Cambia la distribución de las especies | NOAA OISST (mensual, grilla de 0,25°) |
| Viento o días de temporal | Con mal tiempo los barcos no salen, sobre todo los costeros | ERA5 de Copernicus |
| Índice de El Niño (ONI) | Resume el estado climático general del océano | NOAA |

- **Cómo unirlas:** por coordenadas del puerto (por eso conviene completarlas) y por mes. La temperatura del mar se puede tomar en una zona frente al puerto; el viento, en el puerto.
- **Anticipar o detectar (decisión clave):**
  - *Anticipar*, como dice la propuesta: para predecir el mes t solo se puede usar el clima hasta t − 1. Es coherente con el beneficio que plantean ("señalar con anticipación").
  - *Detectar:* clasificar el mes t usando el clima de ese mismo mes. Probablemente funcione mejor, pero ya no anticipa.
  - El EDA puede mostrar cuánta relación hay con el clima del mes anterior y cuánta con el del mismo mes, para decidir con datos.
- **Matiz:** la captura se hace en el mar, a veces lejos del puerto (sobre todo los congeladores). El clima del puerto es una aproximación, más útil para la flota costera y la de rada o ría.
- **Otros factores externos**, como vedas o conflictos, explican muchas anomalías, pero armarlos lleva trabajo manual. Pueden quedar como mejora opcional.

### 2.3 Latitud y longitud

**Qué dijeron:** completarlas, porque son solo 23 puertos y la ubicación aporta más que la variable categórica "puerto".

**Recomendación:** completarlas para todos los puertos y usarlas como variables numéricas.

- **Cómo:** con `src/coordenadas.py` y la tabla `data/referencias/coordenadas_puertos.csv`: se toman del propio dataset y, si un puerto real no tiene, se buscan a mano anotando la fuente. Los puertos de 2010–2018 que no están en 2019 son al menos 3.
- **«otros puertos Buenos Aires»:** en 2019 explica todos los faltantes y no es un puerto, así que conviene aclarárselo a las profesoras. Opciones:
  - darle un punto de la costa bonaerense y marcarlo como aproximado;
  - excluirlo: en 2019 es el 7 % de las filas y menos del 2 % de los kilos.
- **Qué aportan:** una relación de cercanía entre puertos y la diferencia norte–sur entre especies bonaerenses y patagónicas. Además, son dos columnas en lugar de unas 22 categorías y permiten cruzar con clima.

### 2.4 Tratamiento de la fecha

**Qué dijeron:** faltó especificar el tratamiento de las variables temporales.

**Recomendación:** describirlo paso a paso.

1. Convertir `fecha` ("AAAA-MM") a período mensual y crear **año** y **mes**.
2. Codificar el mes de forma **cíclica** (seno y coseno), para que diciembre quede cerca de enero.
3. Armar la **serie mensual completa** de cada especie y puerto, de 2010-01 en adelante, y decidir qué valor llevan los meses sin fila.
4. Crear **rezagos** con datos del pasado: captura en t − 1 y t − 2, mismo mes del año anterior (t − 12), promedio móvil de los últimos 3 y 12 meses y mediana histórica de ese mes.
5. Todo cálculo con ventanas usa **solo meses anteriores** al mes que se etiqueta, para no filtrar información del futuro.
6. **División por tiempo**, sin mezclar al azar. Una propuesta para discutir: los primeros años solo como historia, entrenamiento hasta 2016, validación 2017 y prueba 2018. 2019 quedaría como prueba extra si pasa los controles de calidad.
7. Verificar que estén los **108 meses** de 2010–2018 y tratar con cuidado los meses incompletos (noviembre de 2019).

### 2.5 Otras recomendaciones que conviene definir

- **Calidad de `captura`** (el riesgo principal). En 2019:
  - la correlación entre meses consecutivos de una misma serie es 0,09;
  - la especie explica 3,2 % de la varianza, casi lo mismo que si los valores estuvieran mezclados al azar (2,6 %);
  - hay valores llamativos, como 9,57 millones de kg de centolla en Caleta Olivia en un mes.

  Si 2010–2018 muestra lo mismo, no hay historial del cual aprender. Plan B para conversar: usar las planillas oficiales de desembarques del Ministerio, que tienen las mismas variables, así el problema no cambia.
- **Alcance.** En 2019, el 61 % de las series especie–puerto tiene 5 meses o menos con datos. Conviene trabajar con las series que tengan historia suficiente (el EDA define el mínimo) e informar qué porcentaje de los kilos totales cubren.
- **Unidad de análisis de la merluza.** El archivo la separa por zona de manejo (S41, N41…). Hay que decidir si conviene especie–puerto o agrupación–puerto.
- **Línea de referencia.** Para saber si el modelo sirve, ayuda compararlo con una regla simple, como "siempre normal" o "lo mismo que el mismo mes del año anterior". Conviene preguntar si eso cuenta como comparación de modelos (pauta 7).
- **Archivo 2019.** Usarlo solo si pasa los controles de calidad, porque noviembre está incompleto y falta diciembre.

---

## 3. Preguntas para llevarles a las profesoras

1. ¿Les parece bien pasar a tres clases (caída, normal, aumento) con un único modelo multiclase?
2. ¿Prefieren que el proyecto **anticipe** (información hasta el mes anterior) o que **detecte** (con el clima del mismo mes)?
3. ¿Cuántas variables externas esperan? ¿Alcanza con temperatura del mar, viento e índice de El Niño?
4. ¿Podemos comparar el modelo con una regla simple de referencia sin que cuente como comparación de modelos?
5. Si la variable captura de 2010–2018 resulta inconsistente, ¿aceptan cambiar a las planillas oficiales de desembarques?
6. ¿Está bien limitar el análisis a las series especie–puerto con historia suficiente?
7. Para «otros puertos Buenos Aires», ¿prefieren excluirlo o asignarle una ubicación aproximada?

---

## 4. Plan del EDA

Cada bloque responde preguntas concretas y termina en una decisión. El EDA no es "hacer gráficos": es juntar la evidencia para definir la etiqueta, las variables y la división de los datos.

### Bloque 0 · Calidad y consistencia (primero)

| Pregunta | Qué mirar | Decisión que alimenta |
| --- | --- | --- |
| ¿El archivo 2010–2018 está completo y bien formado? | `python src/perfilado.py` sobre 2010–2018: filas, nulos, duplicados, los 108 meses, categorías contra 2019 | Cómo unificar archivos |
| ¿La captura tiene coherencia en el tiempo? | Sección 9 del reporte: correlación entre meses consecutivos y varianza explicada por especie, comparadas con datos mezclados al azar | Si el dataset sirve o hay que cambiar de fuente |
| ¿Los totales coinciden con los oficiales? | Totales anuales de 3 o 4 especies principales (merluza hubbsi, langostino, calamar Illex) contra las planillas oficiales | Si hay errores de carga y dónde |

### Bloque 1 · Estructura y cobertura

| Pregunta | Qué mirar | Decisión que alimenta |
| --- | --- | --- |
| ¿Cuántas series hay y cuánta historia tienen? | Meses con datos por serie especie–puerto, y qué parte de los kilos totales cubren | Mínimo de historia y alcance del estudio |
| ¿Dónde están los huecos? | Grilla de meses por serie, para ver si son huecos sueltos o temporadas completas | Si los meses sin fila son 0 o dato faltante |
| ¿Qué puertos y especies pesan más? | Ranking por kilos y por cantidad de registros | Si conviene enfocarse en las series principales |

### Bloque 2 · La variable captura

| Pregunta | Qué mirar | Decisión que alimenta |
| --- | --- | --- |
| ¿Cómo se distribuye? | Histograma en escala logarítmica, general y por especie, flota y categoría | Transformación logarítmica |
| ¿Qué valores son extremos? | Valores extremos dentro de cada especie–puerto, no globales | Qué es un error de carga y qué es una anomalía real |

### Bloque 3 · Series temporales (el núcleo)

| Pregunta | Qué mirar | Decisión que alimenta |
| --- | --- | --- |
| ¿Hay estacionalidad? | Mapa de calor mes × año para las especies principales (en 2019, por ejemplo, el calamar Illex en Puerto Madryn concentra la captura entre enero y abril) | Codificación del mes y referencia "mismo mes" para la etiqueta |
| ¿Hay tendencia? | Serie total mensual 2010–2018 y por especie principal | Si "lo normal" debe actualizarse con los años |
| ¿El pasado anticipa el presente? | Autocorrelación de log(captura) con rezagos 1 y 12 | Si los rezagos sirven como variables y si anticipar es viable |
| ¿Cuánto varía lo normal? | Descomposición en tendencia, estacionalidad y residuo (STL) para algunas series; distribución de los residuos | Dónde poner los límites de la etiqueta |

### Bloque 4 · Geografía y flota

| Pregunta | Qué mirar | Decisión que alimenta |
| --- | --- | --- |
| ¿La ubicación explica diferencias? | Puertos en un gráfico de latitud y longitud, con su captura total y sus especies principales | Uso de latitud y longitud como variables |
| ¿Cómo se reparte cada especie entre flotas? | Participación de cada flota por especie y puerto | Si la flota se guarda como información adicional |

### Bloque 5 · Etiqueta preliminar

| Pregunta | Qué mirar | Decisión que alimenta |
| --- | --- | --- |
| ¿Cuántas anomalías salen con cada criterio? | Proporción de caídas y aumentos según el criterio (desvío robusto o percentiles) y según el límite elegido | Criterio y límites de la etiqueta |
| ¿Las anomalías tienen sentido? | Algunas series graficadas con los meses marcados como caída o aumento | Ajustar el criterio |
| ¿Cómo queda el balance de clases? | Proporción por clase, por año, especie y puerto | Cómo tratar el desbalance más adelante |

### Bloque 6 · Variables externas (si se incorporan)

| Pregunta | Qué mirar | Decisión que alimenta |
| --- | --- | --- |
| ¿El clima se relaciona con las anomalías? | Anomalía de temperatura del mar y viento contra las anomalías de captura, con el clima del mismo mes y del mes anterior, por tipo de flota | Qué variables externas entran y si el proyecto anticipa o detecta |

### Lo que el EDA tiene que dejar decidido

- [ ] Si el dataset es usable, o el plan B.
- [ ] Unidad de análisis y series incluidas, con el porcentaje de kilos cubierto.
- [ ] Qué valor llevan los meses sin registro.
- [ ] Criterio y límites de las tres clases, y su proporción.
- [ ] Lista de variables: rezagos, estacionalidad, ubicación, flota y clima.
- [ ] División por tiempo: años de historia, entrenamiento, validación y prueba.
- [ ] Qué hacer con 2019 y con «otros puertos Buenos Aires».

---

## 5. Cómo armar el notebook del EDA

- **Una sección por bloque**, con este orden: pregunta → gráfico o tabla → observación → decisión.
- **Las observaciones y decisiones las escriben ustedes.** La pauta 12 permite usar IA para el código, no para el análisis ni las conclusiones, y la cátedra evalúa sobre todo la justificación.
- **Reusar lo que ya está:** `src/perfilado.py` para la calidad, `src/coordenadas.py` para la ubicación, y los datos originales en `data/raw/` sin tocar. Lo procesado va a otra carpeta.
- **Pocos gráficos y buenos:** cada uno tiene que responder una pregunta de la tabla. Si no lleva a una decisión, sobra.
- **Registrar el esfuerzo por etapa:** la materia pide identificar qué etapas requieren más trabajo. Probablemente sean la calidad de los datos y la construcción de la etiqueta.
