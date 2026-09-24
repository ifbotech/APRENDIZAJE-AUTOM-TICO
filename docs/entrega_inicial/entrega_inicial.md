<section class="portada">
<img class="logo" src="../img/logo_ugr.png" alt="Universidad del Gran Rosario">
<div class="institucion"><strong>Universidad del Gran Rosario</strong><br>Aprendizaje Automático · Trabajo Práctico Grupal 2026, 2.º cuatrimestre</div>
<div class="centro">
<p class="etiqueta">Entrega inicial</p>
<h1>Detección de anomalías en las capturas pesqueras argentinas</h1>
<p class="bajada">Contexto y planteo del problema, descripción del dataset, acceso a los datos originales y propuesta de limpieza y preprocesamiento.</p>
</div>
<div class="equipo">
<div>
<p class="grupo">Grupo 12</p>
<h2>Integrantes</h2>
<ul>
<li>Bernal, Alejandro Matias</li>
<li>Paredes, Sebastian Pablo</li>
<li>Rodrigues, David Ezequiel</li>
<li>Barnetche, Iñaki Francisco</li>
</ul>
</div>
<div>
<h2>Fecha de entrega</h2>
<p>24 de septiembre de 2026</p>
<h2 style="margin-top: 5mm">Datos</h2>
<p>Desembarques de pesca marítima por puerto, flota y especie. Ministerio de Agricultura, Ganadería y Pesca (datos abiertos).</p>
</div>
</div>
</section>

## 1. Contexto y problema

### 1.1 Contexto

La pesca marítima es una actividad económica importante para Argentina. Cada mes se registran desembarques en distintos puertos del litoral marítimo, con especies, flotas y volúmenes muy diferentes entre sí. Estos registros son publicados como datos abiertos por el Ministerio de Agricultura, Ganadería y Pesca.

Al revisar los datos observamos que las capturas varían mucho según la especie, el puerto, el tipo de flota y el momento del año. Por eso una captura alta o baja no indica por sí sola que haya ocurrido algo fuera de lo normal: lo que es habitual para una especie en un puerto puede ser excepcional para otra.

Poder anticipar que la captura de una especie en un puerto se va a apartar de su comportamiento habitual tiene varios usos posibles:

- Alertar con tiempo sobre caídas inesperadas en la captura de una especie.
- Detectar cambios en la actividad de determinados puertos.
- Ayudar a planificar producción, almacenamiento y transporte.
- Identificar registros que podrían ser incorrectos.
- Orientar investigaciones sobre presión pesquera o cambios ambientales.

### 1.2 Planteo del problema

Existen trabajos que abordan este tema como un problema de regresión, prediciendo el volumen de captura mediante modelos de series temporales (por ejemplo, ARIMA). En este trabajo, en cambio, lo planteamos como un problema de clasificación binaria:

<div class="destacado" markdown="1">
**Para cada combinación de especie y puerto, y utilizando solamente la información disponible hasta el mes anterior (t − 1), predecir si la captura del mes t será normal o anómala.**
</div>

<div class="sin-salto" markdown="1">

| Elemento | Definición |
| --- | --- |
| Unidad de análisis | Una combinación especie – puerto – mes. |
| Información disponible | Solo la registrada hasta el mes t − 1. |
| Salida | Clase del mes t: normal o anómala. |
| Tipo de tarea | Aprendizaje supervisado: clasificación binaria. |
| Etiqueta | No existe en el dataset. Se construirá a partir del comportamiento histórico de cada especie en cada puerto; el criterio se definirá después del análisis exploratorio (sección 4.8). |

</div>

<div class="sin-salto" markdown="1">

Las dos clases posibles son:

- **Normal:** la captura del mes se encuentra dentro de lo esperable para esa especie, ese puerto y esa época del año.
- **Anómala:** la captura del mes se aparta de manera marcada de ese comportamiento histórico, ya sea por una caída o por un aumento.

</div>

Que un mes sea clasificado como anómalo no explica por qué ocurrió. Detrás de una variación puede haber causas estacionales, ambientales, económicas, administrativas o cambios en la actividad de la flota. El objetivo del modelo es señalar esos casos con anticipación para que luego puedan analizarse con más detalle.

## 2. Descripción del dataset

### 2.1 Fuente

Para desarrollar el trabajo vamos a utilizar un conjunto de datos públicos sobre desembarques pesqueros realizados en puertos argentinos.

<div class="kv" markdown="1">

| | |
| --- | --- |
| Fuente | Datos Argentina / Ministerio de Agricultura, Ganadería y Pesca (portal de datos abiertos datos.magyp.gob.ar). |
| Contenido | Desembarques mensuales de pesca marítima por puerto, tipo de flota y especie. |
| Formato | Archivos CSV, uno por período (2010–2018 y 2019). |
| Naturaleza de los datos | Datos oficiales publicados por el organismo: no son sintéticos ni un dataset académico. |

</div>

### 2.2 Archivos y características generales

El archivo principal reúne información desde enero de 2010 hasta diciembre de 2018. Tiene aproximadamente 41.340 registros y 13 variables. Además, contamos con otro archivo correspondiente al año 2019, que más adelante podríamos incorporar al análisis. Dentro de los datos aparecen 23 puertos, distribuidos en 6 provincias. También encontramos 8 tipos de flota, 89 especies diferentes y 16 agrupaciones de especies.

Nos resulta útil contar con varios años porque permite comparar cómo fue cambiando la captura de una misma especie o de un determinado puerto. También nos da una base histórica más amplia para tratar de definir qué situaciones se alejan de lo esperado.

<div class="sin-salto" markdown="1">
<div class="num" markdown="1">

| Característica | Archivo principal (2010–2018) | Archivo complementario (2019) |
| --- | --- | --- |
| Período | enero 2010 – diciembre 2018 | enero 2019 – noviembre 2019 |
| Registros | aprox. 41.340 | 3.040 |
| Variables | 13 | 13 |
| Puertos | 23 | 20 |
| Provincias | 6 | 5 |
| Tipos de flota | 8 | 8 |
| Especies | 89 | 79 |
| Agrupaciones de especies | 16 | 16 |
| Categorías de especie | a relevar | 3 |
| Codificación del archivo | a relevar | Latin-1 (ISO-8859-1) |

</div>
</div>

<div class="nota" markdown="1">
Valores de 2010–2018: primera revisión del grupo. Valores de 2019: perfilado automático del archivo con el script `src/perfilado.py` del repositorio del grupo (reporte completo en `reports/perfilado_captura-puerto-flota-2019.md`). El mismo perfilado se aplicará al archivo 2010–2018 al comenzar la limpieza.
</div>

### 2.3 Qué representa cada registro

Cada fila informa la **captura desembarcada, en kilogramos, de una especie** (dentro de una agrupación de especies), **por un tipo de flota, en un puerto y en un mes**. Por ejemplo, la primera fila del archivo 2019 indica que en enero de 2019 la flota de rada o ría desembarcó 221.363 kg de camarón en Bahía Blanca.

Solo hay filas cuando hubo captura: en 2019 no aparecen valores en cero (el mínimo es 1 kg). Una misma especie puede figurar en más de una agrupación dentro del mismo mes, flota y puerto (por ejemplo, besugo en «Variado costero» y en «otras especies»), por lo que un registro queda identificado por la combinación fecha – flota – puerto – especie – agrupación. Con esa clave no hay registros repetidos en 2019.

### 2.4 Semántica de las variables

La descripción de cada variable es la que publica el portal; la última columna resume lo que encontramos en el archivo 2019.

| Variable | Tipo | Significado | Valores en 2019 |
| --- | --- | --- | --- |
| `fecha` | Fecha ISO 8601 (año-mes) | Mes y año al que corresponde el desembarque. | `2019-01` a `2019-11` (11 meses). |
| `flota` | Texto | Tipo de flota de captura. | 8 tipos: Rada o ría, Costeros, Fresqueros y Congeladores arrastreros, tangoneros, poteros nacionales, trampas y palangreros. |
| `puerto` | Texto | Nombre del puerto de desembarque. | 20 valores, p. ej. Mar del Plata (45 % de los registros). Incluye «otros puertos Buenos Aires». |
| `provincia` | Texto | Nombre de la provincia del puerto. | Buenos Aires, Río Negro, Chubut, Santa Cruz y Tierra del Fuego. |
| `provincia_id` | Texto | Código de la provincia. | 2 dígitos con cero inicial, p. ej. `06` (Buenos Aires). |
| `departamento` | Texto | Nombre del departamento (partido) del puerto. | 16 valores, p. ej. General Pueyrredon; «sin especificar» para «otros puertos Buenos Aires». |
| `departamento_id` | Texto | Código del departamento. | 5 dígitos, p. ej. `06357` (General Pueyrredon). |
| `latitud` | Número decimal | Coordenada de latitud del puerto. | Un valor por puerto, p. ej. −38,0491 (Mar del Plata). 216 nulos. |
| `longitud` | Número decimal | Coordenada de longitud del puerto. | Un valor por puerto, p. ej. −57,5368 (Mar del Plata). 216 nulos. |
| `categoria` | Texto | Categoría de la especie capturada. | Peces (2.637 registros), Crustáceos (234) y Moluscos (169). |
| `especie` | Texto | Nombre de la especie capturada. | 79 especies, p. ej. Merluza hubbsi, Langostino, Calamar Illex. |
| `especie_agrupada` | Texto | Nombre de las principales especies capturadas (agrupación). | 16 grupos, p. ej. Merluza hubbsi S41, Langostino, Variado costero, otras especies. |
| `captura` | Número entero | Cantidad de kilos capturados. | De 1 a 18.622.724 kg; mediana 2.680,5 kg. Sin nulos ni ceros. |

<div class="notas-cat" markdown="1">

**Notas sobre algunas categorías.**

- **Tipos de flota.** «Rada o ría» agrupa embarcaciones pequeñas que operan cerca de la costa; «Costeros», buques de la flota costera; «Fresqueros», buques de altura que conservan la captura enfriada, sin congelar. Los «Congeladores» procesan y congelan a bordo y se distinguen por el arte de pesca: arrastreros (red de arrastre), tangoneros (arrastre con tangones, dirigido al langostino), poteros (poteras, dirigido al calamar), trampas (dirigido a la centolla) y palangreros (palangre, dirigido a la merluza negra).
- **Agrupaciones de especies.** La merluza común (*Merluza hubbsi*) se desagrega según su zona de manejo: S41 (al sur del paralelo 41° S), N41 CTMFM (al norte de 41° S, en la zona común argentino-uruguaya de la Comisión Técnica Mixta del Frente Marítimo), N41 ZEEA (al norte de 41° S, en la Zona Económica Exclusiva Argentina) y GSM (Golfo San Matías). «Variado costero» reúne especies costeras que se capturan en conjunto, «Rayas (sin V. Cost)» son las rayas no incluidas en el variado costero y «otras especies» agrupa el resto.
- **«otros puertos Buenos Aires».** No es un puerto puntual sino un agregado de puertos bonaerenses; por eso no tiene departamento ni coordenadas.
- **Sufijo «nep».** Indica especies no especificadas en otra parte, por ejemplo «Rayas nep» o «Tiburones nep».

</div>

En una primera etapa creemos que las variables que más vamos a utilizar son **fecha, puerto, flota, especie, especie agrupada y captura**.

## 3. Acceso al dataset

Los datos fueron obtenidos del portal oficial de Datos Abiertos de Argentina y corresponden a información sobre desembarques pesqueros.

<div class="enlaces" markdown="1">

- **Conjunto de datos (página con los dos archivos):**<br>[https://datos.magyp.gob.ar/dataset/http-www-magyp-gob-ar-sitio-areas-pesca-maritima-desembarques](https://datos.magyp.gob.ar/dataset/http-www-magyp-gob-ar-sitio-areas-pesca-maritima-desembarques)
- **Recurso principal utilizado (desembarques 2010–2018):**<br>[https://datos.magyp.gob.ar/dataset/http-www-magyp-gob-ar-sitio-areas-pesca-maritima-desembarques/archivo/77a15b4a-71e1-4b81-9732-ae0b6863c8cc](https://datos.magyp.gob.ar/dataset/http-www-magyp-gob-ar-sitio-areas-pesca-maritima-desembarques/archivo/77a15b4a-71e1-4b81-9732-ae0b6863c8cc)
- **Recurso complementario (desembarques 2019):** archivo `captura-puerto-flota-2019.csv`, en la misma página del conjunto de datos.

</div>

## 4. Propuesta de limpieza y preprocesamiento

Antes de entrenar un modelo necesitamos revisar mejor los datos y preparar algunas variables. Para que la propuesta sea concreta corrimos un primer perfilado automático del archivo 2019; los números de esta sección salen de ese perfilado y el mismo script se va a aplicar al archivo 2010–2018.

### 4.1 Lectura y unificación de los archivos

El archivo 2019 está codificado en Latin-1 (ISO-8859-1): si se lo lee como UTF-8, los acentos se rompen («Bah�a Blanca»). Los códigos `provincia_id` y `departamento_id` tienen ceros a la izquierda (`06`, `06357`) que se pierden si se leen como números. Además, dos nombres de especie aparecen cortados en 25 caracteres: «Otras especies de crustác» y «Otras especies de molusco».

**Propuesta:** leer ambos archivos indicando la codificación y el tipo de cada columna, unirlos en una sola tabla con las mismas 13 variables y comparar los valores de las variables categóricas entre archivos (2019 tiene 20 puertos y 79 especies, frente a 23 y 89 en 2010–2018) para unificar nombres escritos de distinta forma o truncados.

### 4.2 Coordenadas faltantes

Una de las cosas que encontramos en la primera revisión fueron registros sin latitud ni longitud. Como un mismo puerto aparece varias veces dentro del dataset, primero vamos a comprobar si podemos completar esas coordenadas utilizando registros del mismo puerto que sí tengan esos datos. Otra posibilidad es directamente no utilizar latitud y longitud, sobre todo si vemos que trabajar con puerto y provincia ya nos da suficiente información.

**En 2019:** hay 216 registros (7,1 %) sin coordenadas y todos corresponden a «otros puertos Buenos Aires» (departamento «sin especificar»). Ese valor no tiene ningún registro con coordenadas, así que en 2019 no se pueden completar desde el mismo puerto. Los otros 19 puertos tienen coordenadas en todos sus registros, con un único par de valores por puerto. Vamos a verificar si en 2010–2018 ocurre lo mismo antes de elegir entre las dos alternativas.

### 4.3 Duplicados

También revisaremos la existencia de duplicados.

**En 2019:** no hay filas idénticas. Sí hay 392 filas que coinciden en fecha, flota, puerto y especie pero difieren en la agrupación: 31 especies aparecen en más de una agrupación (por ejemplo, besugo en «Variado costero» y en «otras especies», o la merluza hubbsi en cuatro agrupaciones según la zona). Estas filas no son duplicados: al llevar la captura a nivel especie – puerto hay que sumarlas, no eliminarlas.

### 4.4 Tratamiento de la fecha

La fecha también necesita cierto tratamiento. Nos interesa separar el año y el mes porque probablemente sea más útil analizarlos por separado. De esa forma podemos estudiar, por ejemplo, si una especie suele tener determinados niveles de captura durante ciertos meses.

**En 2019:** la fecha viene como texto año-mes (`2019-01`). El archivo cubre de enero a noviembre: noviembre tiene 94 registros, frente a 246–347 del resto de los meses, y diciembre no está (figura 1). Antes de usar noviembre de 2019 hay que confirmar si está completo; en 2010–2018 vamos a verificar que estén los 108 meses.

<figure>
<img src="assets/fig/captura-puerto-flota-2019_registros_por_mes.png" alt="Registros por mes en el archivo 2019">
<figcaption><strong>Figura 1.</strong> Registros por mes en el archivo 2019. Noviembre tiene 94 registros y diciembre no figura en el archivo.</figcaption>
</figure>

### 4.5 Períodos sin registros

Otro punto que queremos observar es si existen períodos en los que algunas especies o algunos puertos directamente no tengan registros.

**En 2019:** el archivo no tiene capturas en cero; cuando una especie no se desembarca en un puerto en un mes, la fila no existe. De las 351 combinaciones especie – puerto de 2019, solo 24 (6,8 %) tienen registros en los 11 meses, 214 (61 %) tienen registros en 5 meses o menos y 72 (20,5 %) aparecen en un único mes (figura 2). Al construir las series mensuales vamos a tener que decidir cómo representar los meses sin fila (captura cero o dato faltante) y qué combinaciones especie – puerto tienen historia suficiente para definir su comportamiento habitual.

<figure>
<img src="assets/fig/captura-puerto-flota-2019_meses_con_registro.png" alt="Combinaciones especie-puerto según meses con registros">
<figcaption><strong>Figura 2.</strong> Combinaciones especie – puerto de 2019 según la cantidad de meses (de 11) en los que tienen al menos un registro.</figcaption>
</figure>

### 4.6 La variable captura: escala, extremos e inconsistencias

Finalmente está la variable **captura**, que probablemente sea una de las más importantes para nuestro análisis. Vamos a buscar valores extremos y posibles inconsistencias, pero teniendo en cuenta que no todas las especies manejan los mismos volúmenes. Por ejemplo, no tendría mucho sentido fijar un único límite y considerar anómala cualquier captura que lo supere. Primero necesitamos conocer cómo se comportan las distintas especies, puertos y períodos para poder establecer comparaciones más razonables.

**En 2019:** la captura es un entero en kilogramos que va de 1 kg a 18.622.724 kg. La distribución es muy asimétrica: la mediana es 2.680,5 kg, la media 223.264 kg y el 1 % de registros más altos supera los 5,8 millones de kg (figura 3), por lo que conviene explorarla en escala logarítmica.

<figure>
<img src="assets/fig/captura-puerto-flota-2019_distribucion_captura.png" alt="Distribución de la captura por registro en 2019">
<figcaption><strong>Figura 3.</strong> Distribución de la captura por registro en 2019, en escala logarítmica. Las líneas marcan la mediana y la media.</figcaption>
</figure>

En esta primera mirada también aparecieron registros que conviene contrastar con otras fuentes, por ejemplo 9.569.699 kg de centolla desembarcados por la flota fresquera en Caleta Olivia / Paula en abril de 2019. Además, dentro de una misma serie (flota – puerto – especie) la captura de un mes casi no se relaciona con la del mes anterior: la correlación entre los logaritmos de meses consecutivos es de 0,09. Antes de construir la etiqueta vamos a contrastar los totales del archivo con las planillas oficiales de desembarques que el Ministerio publica en su sección de pesca marítima, para distinguir errores de carga de variaciones reales.

### 4.7 Nivel de agregación

El problema está planteado por especie, puerto y mes, pero el archivo informa la captura desagregada además por flota y por agrupación de especies. Para llevar los datos a la unidad del problema hay que sumar la captura de todas las flotas y agrupaciones de una misma especie en un puerto y un mes. Queda por decidir si la flota se conserva como información adicional en el análisis.

### 4.8 Construcción de la etiqueta (etapa siguiente)

Uno de los puntos que todavía tenemos que resolver es cómo definir exactamente una anomalía. Actualmente el dataset no tiene una columna que indique si una captura fue normal o anómala. Esa clasificación tendremos que construirla nosotros a partir del comportamiento histórico de los datos.

Una posibilidad es comparar la captura de una determinada especie en un puerto con lo que ocurrió anteriormente en períodos similares. Si el valor se encuentra demasiado alejado de lo que normalmente sucede en ese contexto, podría considerarse un posible caso anómalo. Todavía tendremos que definir qué criterio vamos a utilizar para establecer ese límite. Esa decisión probablemente surja después de realizar el análisis exploratorio y conocer mejor la distribución de las capturas.

Una vez que tengamos una forma razonable de identificar esos casos, podremos entrenar un modelo de clasificación para ver si es posible distinguir entre registros habituales y registros anómalos. Por ahora, el objetivo de esta primera etapa es más básico: entender bien el dataset, corregir los problemas que encontremos y dejar los datos preparados para continuar con el análisis.

### 4.9 Resumen de la propuesta

<div class="compacta sin-salto" markdown="1">

| # | Tarea | Qué vimos en 2019 | Qué proponemos |
| --- | --- | --- | --- |
| 1 | Lectura y unificación | Latin-1; códigos con ceros a la izquierda; 2 nombres truncados. | Leer con codificación y tipos explícitos; unir 2010–2018 y 2019; unificar nombres. |
| 2 | Coordenadas faltantes | 216 registros (7,1 %), todos de «otros puertos Buenos Aires». | Completar desde el mismo puerto si es posible; si no, no usar latitud y longitud. |
| 3 | Duplicados | 0 filas idénticas; 392 filas que difieren solo en la agrupación. | Revisar con la clave completa; sumar (no eliminar) al agregar. |
| 4 | Fecha | Año-mes; noviembre con 94 registros; sin diciembre. | Separar año y mes; verificar meses incompletos. |
| 5 | Períodos sin registros | Sin ceros; 61 % de las series especie – puerto con 5 meses o menos. | Definir cómo representar los meses sin fila y qué series tienen historia suficiente. |
| 6 | Captura | De 1 a 18,6 millones de kg; muy asimétrica; valores a contrastar. | Analizar por especie y puerto en escala logarítmica; revisar extremos; contrastar con las planillas oficiales. |
| 7 | Agregación | Captura por flota y agrupación. | Sumar a especie – puerto – mes. |
| 8 | Etiqueta | No existe en el dataset. | Construirla a partir del histórico; criterio a definir tras el análisis exploratorio. |

</div>

## 5. Conclusión

Elegimos este dataset principalmente porque tiene varios años de información y permite trabajar con diferentes especies, puertos y tipos de flota.

Antes de pensar directamente en un modelo, necesitamos entender cómo se comportan esos datos. Parte del trabajo va a estar justamente en descubrir qué diferencias son normales y cuáles podrían representar algo fuera de lo habitual.

El paso siguiente será limpiar y explorar el dataset con más profundidad. A partir de eso podremos definir mejor qué vamos a considerar una anomalía y cómo generar la clasificación necesaria para continuar con el trabajo de aprendizaje automático.
