<p align="center"><img src="img/logo_ugr.png" alt="Universidad del Gran Rosario" width="110"></p>

# Detección de anomalías en las capturas pesqueras argentinas

**Universidad del Gran Rosario** · **Aprendizaje Automático**

Trabajo Práctico Grupal 2026 · Entrega inicial · 24 de septiembre de 2026

**Grupo 12**

**Integrantes:**

- Bernal, Alejandro Matias
- Paredes, Sebastian Pablo
- Rodrigues, David Ezequiel
- Barnetche, Iñaki Francisco

## Contexto y problema

La pesca marítima es una actividad económica importante para Argentina. Cada mes se registran desembarques en distintos puertos del litoral marítimo, con especies, flotas y volúmenes muy diferentes entre sí. Estos registros son publicados como datos abiertos por el Ministerio de Agricultura, Ganadería y Pesca.

Al revisar los datos observamos que las capturas varían mucho según la especie, el puerto, el tipo de flota y el momento del año. Por eso una captura alta o baja no indica por sí sola que haya ocurrido algo fuera de lo normal: lo que es habitual para una especie en un puerto puede ser excepcional para otra.

Poder anticipar que la captura de una especie en un puerto se va a apartar de su comportamiento habitual tiene varios usos posibles:

- Alertar con tiempo sobre caídas inesperadas en la captura de una especie.
- Detectar cambios en la actividad de determinados puertos.
- Ayudar a planificar producción, almacenamiento y transporte.
- Identificar registros que podrían ser incorrectos.
- Orientar investigaciones sobre presión pesquera o cambios ambientales.

## Planteo del problema

Existen trabajos que abordan este tema como un problema de regresión, prediciendo el volumen de captura mediante modelos de series temporales (por ejemplo, ARIMA). En este trabajo, en cambio, lo planteamos como un problema de clasificación binaria:

**Para cada combinación de especie y puerto, y utilizando solamente la información disponible hasta el mes anterior (t − 1), predecir si la captura del mes t será normal o anómala.**

Las dos clases posibles son:

- **Normal:** la captura del mes se encuentra dentro de lo esperable para esa especie, ese puerto y esa época del año.
- **Anómala:** la captura del mes se aparta de manera marcada de ese comportamiento histórico, ya sea por una caída o por un aumento.

Se trata de un problema de aprendizaje supervisado: el dataset no trae la etiqueta normal o anómala, así que la construiremos nosotros a partir del comportamiento histórico de cada especie en cada puerto.

Que un mes sea clasificado como anómalo no explica por qué ocurrió. Detrás de una variación puede haber causas estacionales, ambientales, económicas, administrativas o cambios en la actividad de la flota. El objetivo del modelo es señalar esos casos con anticipación para que luego puedan analizarse con más detalle.

## Dataset

Para desarrollar el trabajo vamos a utilizar un conjunto de datos públicos sobre desembarques pesqueros realizados en puertos argentinos.

Cada registro indica la captura desembarcada, en kilogramos, de una especie, por un tipo de flota, en un puerto y en un mes. Solo hay registros cuando hubo captura: en el archivo 2019 no aparecen valores en cero.

El archivo principal reúne información desde enero de 2010 hasta diciembre de 2018. Tiene aproximadamente 41.340 registros y 13 variables. Además, contamos con otro archivo correspondiente al año 2019, que más adelante podríamos incorporar al análisis. Ese archivo tiene 3.040 registros con las mismas 13 variables y cubre de enero a noviembre de 2019: no incluye diciembre.

Dentro de los datos aparecen 23 puertos, distribuidos en 6 provincias. Uno de ellos, «otros puertos Buenos Aires», no es un puerto puntual sino un agregado de otros puertos de la provincia. También encontramos 8 tipos de flota, 89 especies diferentes y 16 agrupaciones de especies.

Nos resulta útil contar con varios años porque permite comparar cómo fue cambiando la captura de una misma especie o de un determinado puerto. También nos da una base histórica más amplia para tratar de definir qué situaciones se alejan de lo esperado.

## Variables principales

Las variables que contiene el dataset son las siguientes:

| Variable | Tipo | Descripción | Uso previsto |
| --- | --- | --- | --- |
| `fecha` | Fecha (ISO-8601) | Mes y año del desembarque. Cada registro resume un mes completo. | Clave temporal de cada serie |
| `flota` | Texto | Tipo de flota que realizó la captura (8 categorías). | Predictora |
| `puerto` | Texto | Puerto donde se realizó el desembarque (23 puertos). | Clave de la serie |
| `provincia` | Texto | Provincia del puerto (6 provincias). | Contexto / agrupación |
| `provincia_id` | Texto | Código de la provincia. | Se descarta (redundante) |
| `departamento` | Texto | Departamento donde se ubica el puerto. | Se descarta (redundante) |
| `departamento_id` | Texto | Código del departamento. | Se descarta (redundante) |
| `latitud` | Número decimal | Latitud del puerto. Presenta valores faltantes. | A definir (ver limpieza) |
| `longitud` | Número decimal | Longitud del puerto. Presenta valores faltantes. | A definir (ver limpieza) |
| `categoria` | Texto | Categoría de lo capturado: Peces, Crustáceos o Moluscos. | Predictora / agrupación |
| `especie` | Texto | Especie capturada (89 especies). | Clave de la serie |
| `especie_agrupada` | Texto | Agrupación de las principales especies (16 grupos). | Agrupación de especies poco frecuentes |
| `captura` | Número entero | Cantidad capturada, expresada en kilogramos. | Base de la etiqueta y de las predictoras |

En una primera etapa creemos que las variables que más vamos a utilizar son ***fecha, puerto, flota, especie, especie agrupada y captura***.

## Acceso al dataset

Los datos fueron obtenidos del portal oficial de Datos Abiertos de Argentina y corresponden a información sobre desembarques pesqueros.

**Fuente:** Datos Argentina / Ministerio de Agricultura, Ganadería y Pesca.

**Formato:** archivos CSV. **Fecha de consulta:** septiembre de 2026.

**Enlaces donde se encuentran los 2 dataset:**

[https://datos.magyp.gob.ar/dataset/http-www-magyp-gob-ar-sitio-areas-pesca-maritima-desembarques](https://datos.magyp.gob.ar/dataset/http-www-magyp-gob-ar-sitio-areas-pesca-maritima-desembarques)

**Recurso principal utilizado (desembarques 2010–2018):**

[https://datos.magyp.gob.ar/dataset/http-www-magyp-gob-ar-sitio-areas-pesca-maritima-desembarques/archivo/77a15b4a-71e1-4b81-9732-ae0b6863c8cc](https://datos.magyp.gob.ar/dataset/http-www-magyp-gob-ar-sitio-areas-pesca-maritima-desembarques/archivo/77a15b4a-71e1-4b81-9732-ae0b6863c8cc)

El segundo archivo, con los desembarques de 2019 (`captura-puerto-flota-2019.csv`), se encuentra en la misma página del conjunto de datos.

## Limpieza y preprocesamiento

Antes de entrenar un modelo necesitamos revisar mejor los datos y preparar algunas variables.

Lo primero es leer y unir bien los archivos. El archivo 2019 está guardado en codificación Latin-1: si se lo abre como UTF-8, las tildes se rompen. Los códigos de provincia y departamento tienen ceros a la izquierda (por ejemplo, `06`), así que hay que leerlos como texto. Al unir el archivo 2010–2018 con el de 2019 vamos a verificar que los puertos y las especies estén escritos de la misma forma en los dos; por ejemplo, hay nombres cortados, como «Otras especies de crustác».

Una de las cosas que encontramos en la primera revisión superficial fueron valores faltantes en las coordenadas con registros sin latitud y longitud.

Como un mismo puerto aparece varias veces dentro del dataset, primero vamos a comprobar si podemos completar esas coordenadas utilizando registros del mismo puerto que sí tengan esos datos. Como los puertos son pocos, si alguno no tiene coordenadas en ningún registro podemos buscarlas y cargarlas a mano. En el archivo 2019, los registros sin coordenadas son todos de «otros puertos Buenos Aires», que al ser un agregado de varios puertos no tiene una ubicación única. Otra posibilidad es directamente no utilizar latitud y longitud, sobre todo si vemos que trabajar con puerto y provincia ya nos da suficiente información.

También revisaremos la existencia de duplicados. Hay que tener en cuenta que una misma especie puede aparecer en más de una agrupación dentro del mismo mes, flota y puerto (en el archivo 2019 hay 392 filas en esa situación). Esas filas no son duplicados sino partes distintas de la captura, y al agregar hay que sumarlas.

La fecha también necesita cierto tratamiento. Nos interesa separar el año y el mes porque probablemente sea más útil analizarlos por separado. De esa forma podemos estudiar, por ejemplo, si una especie suele tener determinados niveles de captura durante ciertos meses. Además, en el archivo 2019 noviembre tiene 94 registros, contra 246 a 347 del resto de los meses, así que antes de usarlo hay que revisar si está completo.

Otro punto que queremos observar es si existen períodos en los que algunas especies o algunos puertos directamente no tengan registros. Como el archivo no tiene capturas en cero, un mes sin registro puede significar que no hubo captura o que falta el dato. Tendremos que decidir cómo representar esos meses y qué series tienen historia suficiente para el análisis.

Como el problema está planteado por especie, puerto y mes, y los datos vienen además separados por flota y por agrupación, también vamos a tener que sumar las capturas a ese nivel.

Finalmente está la variable **captura**, que probablemente sea una de las más importantes para nuestro análisis. Vamos a buscar valores extremos y posibles inconsistencias, pero teniendo en cuenta que no todas las especies manejan los mismos volúmenes.

Por ejemplo, no tendría mucho sentido fijar un único límite y considerar anómala cualquier captura que lo supere. Primero necesitamos conocer cómo se comportan las distintas especies, puertos y períodos para poder establecer comparaciones más razonables.

También vamos a contrastar los totales con las planillas oficiales de desembarques del Ministerio, porque en la primera revisión aparecieron valores llamativos, por ejemplo más de 9,5 millones de kg de centolla en Caleta Olivia en un solo mes.

### Qué se hará posteriormente

Uno de los puntos que todavía tenemos que resolver es cómo definir exactamente una anomalía.

Actualmente el dataset no tiene una columna que indique si una captura fue normal o anómala. Esa clasificación tendremos que construirla nosotros a partir del comportamiento histórico de los datos.

Una posibilidad es comparar la captura de una determinada especie en un puerto con lo que ocurrió anteriormente en períodos similares. Si el valor se encuentra demasiado alejado de lo que normalmente sucede en ese contexto, podría considerarse un posible caso anómalo.

Todavía tendremos que definir qué criterio vamos a utilizar para establecer ese límite. Esa decisión probablemente surja después de realizar el análisis exploratorio y conocer mejor la distribución de las capturas.

Una vez que tengamos una forma razonable de identificar esos casos, podremos entrenar un modelo de clasificación para ver si es posible distinguir entre registros habituales y registros anómalos.

Por ahora, el objetivo de esta primera etapa es más básico: entender bien el dataset, corregir los problemas que encontremos y dejar los datos preparados para continuar con el análisis.

## Conclusión

Elegimos este dataset principalmente porque tiene varios años de información y permite trabajar con diferentes especies, puertos y tipos de flota.

Antes de pensar directamente en un modelo, necesitamos entender cómo se comportan esos datos. Parte del trabajo va a estar justamente en descubrir qué diferencias son normales y cuáles podrían representar algo fuera de lo habitual.

El paso siguiente será limpiar y explorar el dataset con más profundidad. A partir de eso podremos definir mejor qué vamos a considerar una anomalía y cómo generar la clasificación necesaria para continuar con el trabajo de aprendizaje automático.
