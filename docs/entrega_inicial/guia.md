# Guía para la defensa de la entrega inicial

**Grupo 12 · Detección de anomalías en las capturas pesqueras argentinas**

> Esta guía es para estudiar. Explica la propuesta con palabras simples, con ejemplos reales del archivo 2019 y las preguntas que puede hacer la profesora. En la presentación respondan con sus palabras: la cátedra evalúa que las decisiones y su justificación sean del grupo.

**Contenido**

1. [El proyecto en 30 segundos](#1-el-proyecto-en-30-segundos)
2. [Palabras clave](#2-palabras-clave)
3. [Las 8 tareas de limpieza, una por una](#3-las-8-tareas-de-limpieza-una-por-una)
4. [Otras preguntas probables](#4-otras-preguntas-probables)
5. [Números para tener a mano](#5-números-para-tener-a-mano)
6. [Guion para los 5 minutos](#6-guion-para-los-5-minutos)

---

## 1. El proyecto en 30 segundos

**Qué datos tenemos.** Una tabla donde cada fila dice cuántos kilos de una especie desembarcó un tipo de barco (la *flota*) en un puerto, en un mes. Por ejemplo, la primera fila del archivo 2019 dice que *en enero de 2019 la flota de rada o ría desembarcó 221.363 kg de camarón en Bahía Blanca*.

**Qué queremos hacer.** Avisar con un mes de anticipación si la captura de una especie en un puerto va a ser **normal** o **anómala**, es decir, muy distinta de lo habitual, para arriba o para abajo.

**Cómo.** Es un problema de **aprendizaje supervisado** de **clasificación binaria**: dos clases, normal o anómala. La etiqueta no viene en los datos: la vamos a construir nosotros a partir del historial de cada especie en cada puerto.

**La idea clave, con un ejemplo cotidiano.** Una compra grande en el súper puede ser normal para una familia de cinco y rarísima para alguien que vive solo, y en diciembre todos compramos más. Con la pesca pasa lo mismo: lo "normal" depende de la especie, del puerto y del mes. Por eso no existe un único número que separe lo normal de lo anómalo.

---

## 2. Palabras clave

| Palabra | Qué significa, fácil |
| --- | --- |
| Desembarque | Lo que un barco descarga en el puerto. Es lo que mide la columna `captura`, en kilos. |
| Registro o fila | Un mes + una flota + un puerto + una especie + una agrupación, con sus kilos. |
| Flota | El tipo de barco. «Rada o ría»: barcos chicos cerca de la costa. «Costeros»: flota costera. «Fresqueros»: barcos de altura que guardan la pesca en frío. «Congeladores»: congelan a bordo. |
| Especie agrupada | El grupo en el que se informa la especie. Por ejemplo, la merluza se separa por zona (S41, N41…), y hay grupos como «Variado costero» u «otras especies». |
| Serie | La captura de una especie en un puerto, mes a mes. Es una "línea de tiempo". |
| Etiqueta | La respuesta que el modelo tiene que aprender: normal o anómala. |
| t y t − 1 | t es el mes que queremos predecir; t − 1 es el mes anterior. |
| Fuga de información | Usar sin querer datos del futuro para predecir. El modelo parece muy bueno, pero está haciendo trampa. |
| Codificación | La "tabla" que usa la computadora para guardar letras. Si se lee con la equivocada, se rompen las tildes. |
| Escala logarítmica | Mirar los números por cuántos ceros tienen: 1.000 → 3; 1.000.000 → 6. |
| Perfilado | Revisión automática del archivo: cuántas filas hay, nulos, repetidos, valores raros. Lo hace `src/perfilado.py`. |
| Clases desbalanceadas | Cuando una clase es mucho más rara que la otra. Las anomalías van a ser pocas. |
| Clasificación y regresión | Clasificación predice una categoría (normal o anómala). Regresión predice un número (cuántos kilos). |

---

## 3. Las 8 tareas de limpieza, una por una

Para cada tarea: **qué es** en una frase, **qué vimos** en el archivo 2019, **qué hacemos**, un **ejemplo** y las **preguntas** que pueden aparecer.

### Tarea 1 · Lectura y unificación

**En una frase:** abrir bien los dos archivos y juntarlos en una sola tabla.

**Qué vimos**

- El archivo está guardado en *Latin-1*. Si se abre como UTF-8, que es lo más común, las tildes se rompen: «Bahía Blanca» aparece como «Bah�a Blanca».
- Los códigos de provincia y departamento empiezan con cero: `06` es Buenos Aires y `06357` es General Pueyrredon. Leídos como número quedarían `6` y `6357`.
- Dos nombres de especie están cortados a 25 letras: «Otras especies de crustác» y «Otras especies de molusco».

**Qué hacemos:** leer indicando la codificación, leer los códigos como texto, unir 2010–2018 con 2019 (tienen las mismas 13 columnas) y revisar que los nombres coincidan entre los dos archivos.

**Ejemplo:** en 2019 el puerto figura como «Caleta Cordova», sin tilde. Si en 2010–2018 figurara como «Caleta Córdova», la computadora los tomaría como dos puertos distintos y la serie quedaría partida en dos.

**Si la profe pregunta**

- *¿Por qué leen los códigos como texto?* Porque son etiquetas, como un código postal o un DNI: no se suman ni se promedian, y el cero es parte del código.
- *¿Cómo se dieron cuenta del problema de codificación?* Al abrir el archivo aparecían símbolos raros en lugar de las tildes. El script prueba UTF-8 y, si falla, usa Latin-1.
- *¿Para qué unen los dos archivos?* Para tener más historia por especie y puerto. Para saber qué es normal hace falta historial.

### Tarea 2 · Coordenadas faltantes

**En una frase:** hay filas que no dicen dónde está el puerto. Como los puertos son pocos, completamos la ubicación con una tabla de puertos.

**Qué vimos en 2019**

- 216 filas (7,1 %) no tienen latitud ni longitud.
- **Todas** son de «otros puertos Buenos Aires».
- Los otros 19 puertos tienen coordenadas en todas sus filas, y cada puerto tiene siempre el mismo par.

**Qué hacemos, en tres pasos**

1. **Armar una tabla de puertos**, una fila por puerto, con las coordenadas que ya trae el dataset. Son 20 puertos en 2019 y 23 en 2010–2018, así que la tabla es chica.
2. **Buscar a mano** las coordenadas de los puertos reales que no tengan ninguna, por ejemplo en Google Maps u OpenStreetMap, y anotarlas en la tabla con la fuente.
3. **Completar** las filas vacías con la tabla y marcar cuáles se completaron, con la columna `coordenadas_origen` (original, tabla o sin dato).

**Ejemplo paso a paso**

La tabla está en [`data/referencias/coordenadas_puertos.csv`](../../data/referencias/coordenadas_puertos.csv). Algunas filas:

| puerto | latitud | longitud | fuente |
| --- | ---: | ---: | --- |
| Mar del Plata | −38,0491 | −57,5368 | dataset |
| Puerto Madryn | −42,7234 | −65,0336 | dataset |
| Ushuaia | −54,8081 | −68,3043 | dataset |
| *un puerto sin coordenadas* | *buscar* | *buscar* | *Google Maps u OpenStreetMap* |
| otros puertos Buenos Aires | — | — | agrupa varios puertos |

- Si una fila de **Puerto Madryn** viniera sin coordenadas, se completa con −42,7234 y −65,0336, las mismas que tiene en el resto de sus filas.
- Si en 2010–2018 aparece un puerto real sin coordenadas en ninguna fila, se busca una sola vez en el mapa, se anota en la tabla y se completan todas sus filas.

```bash
# Arma o actualiza la tabla y muestra qué puertos quedan sin coordenadas
python src/coordenadas.py data/raw/captura-puerto-flota-2019.csv
```

```python
# En el código de limpieza: completa lo que falta y agrega la columna coordenadas_origen
import sys
sys.path.append("src")  # si se corre desde la raíz del repositorio (por ejemplo, en una notebook)
from coordenadas import completar_coordenadas
df = completar_coordenadas(df)
```

Resultado con el archivo 2019: 2.824 filas quedan con su coordenada original y 216 siguen sin dato, porque son todas de «otros puertos Buenos Aires».

**Atención con «otros puertos Buenos Aires».** No es un puerto: es una bolsa que junta varios puertos chicos de la provincia. En 2019 desembarca sobre todo corvina blanca, gatuzo y pescadilla. No tiene un punto único en el mapa, así que no hay coordenadas para buscar. Opciones, a decidir por el grupo:

- dejarlo sin coordenadas y marcado;
- no usar latitud y longitud en el modelo, porque puerto y provincia ya dicen dónde se desembarcó;
- darle un punto aproximado y marcarlo como aproximado. Ojo: el promedio de los puertos bonaerenses (−37,54; −58,81) cae tierra adentro, entre Tandil y Balcarce.

**Si la profe pregunta**

- *¿Por qué no completan con el promedio de todas las latitudes?* Porque una ubicación no se puede promediar: el promedio de varios puertos cae en un lugar donde no hay ningún puerto. El de los puertos bonaerenses queda tierra adentro.
- *¿De dónde sacan las coordenadas que faltan?* Primero de otras filas del mismo puerto. Si un puerto real no tiene ninguna, de un mapa, anotando la fuente.
- *¿Y «otros puertos Buenos Aires»?* No es un puerto sino un grupo de puertos, así que no tiene una ubicación única. Queda marcado.
- *¿Necesitan las coordenadas?* No son imprescindibles: el puerto y la provincia ya dicen dónde se desembarcó. Servirían si quisiéramos usar la ubicación como número, por ejemplo más al norte o más al sur.

### Tarea 3 · Duplicados

**En una frase:** buscar filas repetidas que harían contar dos veces la misma captura.

**Qué vimos:** no hay filas idénticas. Pero hay 392 filas que **parecen** repetidas: tienen la misma fecha, flota, puerto y especie, y solo cambia la agrupación. Hay 31 especies que aparecen en más de una agrupación.

**Ejemplo:** enero de 2019, flota costera, Mar del Plata, besugo.

| Agrupación | Captura |
| --- | ---: |
| otras especies | 9.417 kg |
| Variado costero | 1.081 kg |

No es un error: son dos partes distintas de la captura de besugo. Si borramos una fila, perdemos kilos reales.

**Qué hacemos:** consideramos duplicado solo si coinciden fecha, flota, puerto, especie **y** agrupación. Con esa clave hay 0 repetidos. Las filas que difieren en la agrupación se suman al agregar (tarea 7).

**Si la profe pregunta**

- *¿Cómo definen un duplicado?* Dos filas con la misma fecha, flota, puerto, especie y agrupación.
- *¿Por qué no borran esas 392 filas?* Porque cada una tiene kilos distintos. Borrarlas haría que la captura parezca más baja de lo que fue.
- *¿Por qué una especie está en dos agrupaciones?* Así viene informada en la fuente. Lo que nos importa es no perder kilos: el besugo de ese mes es la suma de las dos filas.

### Tarea 4 · Fecha

**En una frase:** convertir el texto "2019-01" en una fecha y separar año y mes.

**Por qué separar el mes:** para comparar enero con enero, porque muchas especies tienen temporada. Ejemplo real de 2019, calamar Illex en Puerto Madryn:

| Mes | ene | feb | mar | abr | may | jul | ago |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| kg | 84.683 | 79.242 | 150.365 | 56.414 | 2.064 | 1.591 | 4.256 |

Una captura baja en agosto puede ser normal para el calamar y la misma captura en marzo sería rarísima.

**Qué vimos:** el archivo 2019 llega hasta noviembre, y noviembre tiene solo 94 filas contra 246 a 347 del resto de los meses. Diciembre no está.

**El riesgo:** si usamos un noviembre incompleto, casi todas las series parecerían caer ese mes. Serían "anomalías" falsas, causadas por datos que faltan cargar.

**Qué hacemos:** separar año y mes, confirmar con la fuente si noviembre de 2019 está completo antes de usarlo y verificar que en 2010–2018 estén los 108 meses (9 años por 12 meses).

**Si la profe pregunta**

- *¿Para qué separan año y mes?* El mes sirve para la temporada; el año, para ver cambios a lo largo del tiempo.
- *¿Cómo saben que noviembre está incompleto?* No lo sabemos seguro. Tiene un tercio de las filas de un mes típico, por eso hay que confirmarlo con la fuente.

### Tarea 5 · Períodos sin registros

**En una frase:** decidir qué significa un mes "sin fila".

**Qué vimos:** el archivo no tiene ceros. Si una especie no se desembarcó en un puerto en un mes, la fila directamente no existe. De las 351 combinaciones especie–puerto de 2019:

- 24 tienen datos los 11 meses;
- 214 tienen datos en 5 meses o menos;
- 72 aparecen una sola vez.

**Ejemplo:** el calamar Illex en Puerto Madryn tiene datos de enero a mayo, julio y agosto. ¿En junio se pescaron 0 kg o faltó cargar el dato? ¿Y de septiembre a noviembre?

**Por qué importa:** para decir si un mes es normal hay que compararlo con los anteriores. Si rellenamos con 0 un dato que en realidad faltaba, inventamos una caída, o sea, una anomalía falsa.

**Qué hacemos:** armar la serie completa mes a mes por especie y puerto, decidir cómo representar los meses sin fila (0 = no hubo pesca, o dato faltante) y definir cuántos meses de historia necesita una serie para entrar al análisis.

**Si la profe pregunta**

- *¿Por qué no rellenan con 0?* Puede estar bien si no hubo pesca, pero si el dato faltaba, inventaríamos caídas. Hay que decidirlo mirando los datos.
- *¿Qué hacen con las series de un solo mes?* Con uno o dos datos no se puede saber qué es normal. Vamos a definir un mínimo de meses con el análisis exploratorio de 2010–2018, que tiene 9 años.

### Tarea 6 · La variable captura

**En una frase:** revisar la variable más importante: cuántos kilos.

**Qué vimos**

- Va de 1 kg a 18.622.724 kg.
- La mitad de las filas tiene 2.680 kg o menos, pero el promedio es 223.264 kg. Unos pocos valores gigantes tiran el promedio para arriba: la distribución es muy asimétrica.

**Escala logarítmica, fácil:** es mirar cuántos ceros tiene el número. 1.000 kg → 3; 1.000.000 kg → 6. Así 10 kg y 10 millones de kg entran en el mismo gráfico, y se comparan proporciones ("el doble", "la décima parte") en lugar de restas.

**Extremos por especie y puerto, no un único límite:** en 2019 la mediana mensual de merluza en Mar del Plata es 637.985 kg y la de langostino en Rawson, 19.219 kg. Un mes con 100.000 kg sería poco para la primera y muchísimo para la segunda.

**Valores a contrastar**

- 9.569.699 kg de centolla desembarcados por la flota fresquera en Caleta Olivia / Paula en abril de 2019.
- La merluza de la flota fresquera en Mar del Plata salta de 1.860 kg en febrero a 2.123.283 kg en julio y vuelve a 11.616 kg en agosto.

**La correlación de 0,09, fácil:** si un mes se pescó mucho, esperaríamos que el mes siguiente también se pesque bastante, porque los barcos, la temporada y el puerto no cambian de un mes a otro. La correlación mide ese parecido entre un mes y el siguiente, de 0 (nada que ver) a 1 (iguales). En 2019 dio 0,09: casi nada. Por eso vamos a contrastar el archivo con las planillas oficiales antes de construir la etiqueta.

**Qué hacemos:** analizar la captura en escala logarítmica, buscar extremos dentro de cada especie y puerto, y contrastar los totales con las planillas oficiales de desembarques del Ministerio.

**Si la profe pregunta**

- *¿Por qué no eliminan los valores extremos?* Porque justamente buscamos valores fuera de lo normal. Un extremo puede ser real, que es lo que queremos detectar, o un error de carga, que es lo que queremos limpiar. Primero hay que distinguirlos.
- *¿Qué diferencia hay entre un outlier y una anomalía?* Un outlier es un valor raro dentro de todos los datos. Una anomalía, para nosotros, es un valor raro para esa especie, ese puerto y esa época.
- *¿Qué hacen si los datos no coinciden con las planillas oficiales?* A decidir por el grupo. Por ejemplo: corregir los casos puntuales o, si el problema es general, consultarlo con la cátedra en la devolución.

### Tarea 7 · Agregación

**En una frase:** pasar a una fila por especie, puerto y mes, que es la unidad del problema.

**Ejemplo:** la merluza hubbsi en Mar del Plata, en enero de 2019, tiene 6 filas:

| Flota | Agrupación | kg |
| --- | --- | ---: |
| Costeros | Merluza hubbsi S41 | 386.001 |
| Costeros | Merluza hubbsi N41 CTMFM | 955 |
| Fresqueros | Merluza hubbsi N41 ZEEA | 26.707 |
| Fresqueros | Merluza hubbsi S41 | 40 |
| Fresqueros | Merluza hubbsi N41 CTMFM | 6 |
| Rada o ría | Merluza hubbsi N41 CTMFM | 126 |
| **Total** | | **413.835** |

Después de agregar queda una sola fila: *enero 2019 · Mar del Plata · Merluza hubbsi · 413.835 kg*.

**Si la profe pregunta**

- *¿No pierden información al sumar?* Sí, se pierde el detalle por flota. Queda por decidir si lo guardamos como información adicional.
- *¿Por qué agregan por especie y no por agrupación?* Porque el problema está planteado por especie y puerto.

### Tarea 8 · Etiqueta

**En una frase:** crear la columna "normal / anómala", que el dataset no trae.

**La idea:** comparar la captura de un mes con lo que pasó antes en períodos parecidos, por ejemplo el mismo mes de años anteriores. Si se aleja "demasiado", es anómala. Cuánto es "demasiado" lo vamos a definir después del análisis exploratorio.

**Ejemplo inventado, solo para explicar la idea:** si la merluza en Mar del Plata en enero de 2011 a 2018 estuvo siempre entre 300.000 y 500.000 kg, un enero con 50.000 kg sería anómalo (caída) y uno con 420.000 kg sería normal.

**Por qué después del análisis exploratorio:** todavía no sabemos cuánto varía normalmente cada serie. El límite tiene que salir de mirar los datos, no de un número elegido al azar.

**Lo más importante, no hacer trampa:** para decidir si enero de 2019 es normal usamos solo datos anteriores a enero de 2019. El modelo, para predecir el mes t, solo ve información hasta t − 1.

**Si la profe pregunta**

- *¿No es circular? Crean la etiqueta con una regla y después el modelo aprende la regla.* No, porque la etiqueta del mes t se calcula con la captura real del mes t, y el modelo tiene que predecirla **sin verla**, solo con información hasta t − 1. Es anticipar, no recalcular.
- *¿Cuántas anomalías esperan?* Pocas: si fueran muchas, serían lo normal. Eso da clases desbalanceadas, y un modelo que diga siempre "normal" acertaría casi siempre sin servir para nada. Lo tenemos en cuenta al elegir cómo evaluarlo.
- *¿Qué modelo van a usar?* Todavía no lo elegimos: primero limpieza, exploración y etiqueta. Va a ser un modelo de clasificación binaria, uno solo, no una comparación de modelos.

---

## 4. Otras preguntas probables

- **¿Por qué eligieron este dataset?** Tiene varios años de información y permite trabajar con muchas especies, puertos y tipos de flota.
- **¿Es un dataset real?** Sí. Son datos oficiales publicados por el Ministerio de Agricultura, Ganadería y Pesca. No es un dataset académico ni sintético.
- **¿Por qué clasificación y no regresión?** Lo que buscamos es avisar si un mes se va a salir de lo normal (alertas de caídas, cambios en la actividad de un puerto, registros incorrectos), no el número exacto de kilos. Además, predecir el volumen con series de tiempo como ARIMA ya está hecho en otros trabajos; nosotros lo planteamos distinto.
- **¿Qué variables van a usar?** Principalmente fecha, puerto, flota, especie, especie agrupada y captura. Provincia y departamento salen del puerto: en 2019 cada puerto pertenece a una sola provincia y a un solo departamento.
- **¿Cómo van a separar entrenamiento y prueba?** Lo definimos más adelante. Como son datos en el tiempo, no conviene mezclarlos al azar: lo habitual es entrenar con meses anteriores y probar con meses posteriores, para no usar el futuro.
- **¿Qué hacen con el archivo 2019?** Por ahora lo usamos para el perfilado. Más adelante podría sumarse como datos más recientes, pero primero hay que verificarlo: noviembre parece incompleto, falta diciembre y hay valores a contrastar.
- **¿Qué hicieron hasta ahora?** Revisamos los dos archivos, corrimos un perfilado automático del archivo 2019 y armamos la propuesta de limpieza. Todavía no entrenamos ningún modelo.
- **¿Qué significa «nep»?** Especies no especificadas en otra parte, por ejemplo «Rayas nep».
- **¿Qué es «Variado costero»?** Un grupo de especies costeras que se informan en conjunto.
- **¿Qué son S41, N41 CTMFM, N41 ZEEA y GSM?** Zonas de manejo de la merluza hubbsi: al sur del paralelo 41° S; al norte de 41° S en la zona común con Uruguay; al norte de 41° S en la Zona Económica Exclusiva Argentina; y Golfo San Matías.

---

## 5. Números para tener a mano

| Dato | Valor |
| --- | --- |
| Archivo principal | enero 2010 a diciembre 2018, aprox. 41.340 filas, 13 variables |
| Puertos, provincias, flotas | 23 puertos en 6 provincias, 8 tipos de flota |
| Especies y agrupaciones | 89 especies, 16 agrupaciones |
| Archivo 2019 | enero a noviembre, 3.040 filas, 20 puertos, 5 provincias, 79 especies |
| Coordenadas faltantes (2019) | 216 filas (7,1 %), todas de «otros puertos Buenos Aires» |
| Duplicados (2019) | 0 filas idénticas; 392 filas que difieren solo en la agrupación |
| Noviembre 2019 | 94 filas, contra 246 a 347 del resto de los meses |
| Series especie–puerto (2019) | 351: 24 completas, 214 con 5 meses o menos, 72 con un solo mes |
| Captura (2019) | mínimo 1 kg, mediana 2.680,5 kg, promedio 223.264 kg, máximo 18.622.724 kg |
| Correlación entre meses consecutivos (2019) | 0,09 |

---

## 6. Guion para los 5 minutos

| Diapositiva | Tiempo | Idea central |
| --- | --- | --- |
| 1 · Portada | 0:15 | Somos el grupo 12 y trabajamos con las capturas pesqueras argentinas. |
| 2 · Contexto | 0:45 | Lo normal depende de la especie, el puerto y el mes. Anticipar desvíos sirve para alertar, planificar y detectar errores. |
| 3 · Problema | 0:45 | Clasificación binaria: normal o anómala, con información hasta el mes anterior. La etiqueta la construimos nosotros. |
| 4 · Dataset | 0:45 | Datos oficiales del Ministerio, dos archivos, qué representa cada fila. |
| 5 · Variables | 0:30 | Cuándo, dónde, quién, qué y cuánto. Las principales: fecha, puerto, flota, especie, agrupación y captura. |
| 6 · Primera revisión | 1:00 | Lo que encontramos en 2019: coordenadas, duplicados aparentes, noviembre incompleto, meses sin fila y escala de la captura. |
| 7 · Limpieza | 1:00 | Las 8 tareas y el próximo paso. |
