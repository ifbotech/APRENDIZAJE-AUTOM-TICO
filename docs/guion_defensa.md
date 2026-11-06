# Guion del video de defensa · Grupo 12

**Formato pedido por la cátedra:** video grabado de 5 minutos como máximo, con la participación de todos los integrantes, subido a YouTube como **Oculto**, con el enlace en un documento entregado en la tarea. Se presenta en los encuentros del 12 y 13 de noviembre de 2026; ese día tienen que estar todos, porque los docentes pueden hacer preguntas. La audiencia no es necesariamente técnica: no se muestra código.

Cada parte dura unos 70 segundos (unas 150 palabras a ritmo tranquilo). Las diapositivas son las de la presentación de defensa.

| Parte | Integrante | Tiempo | Diapositivas | Tema |
| --- | --- | --- | --- | --- |
| 1 | Iñaki Barnetche | 0:00–1:10 | Portada, 2, 3 | Presentación, problema y calidad de los datos |
| 2 | Alejandro Bernal | 1:10–2:20 | 5, 7, 6 | Qué es una anomalía y qué mostró el análisis |
| 3 | Pablo Paredes | 2:20–3:30 | 8, 9, 10 | Variables probadas y el modelo |
| 4 | David Rodrigues | 3:30–4:50 | 11, 12, 13, 14 | Resultados, uso, límites y cierre |

## Parte 1 · Iñaki Barnetche

> Hola, somos el grupo 12: Iñaki Barnetche, Alejandro Bernal, Pablo Paredes y David Rodrigues. Nuestro proyecto trata sobre la pesca marítima argentina.
>
> Cada mes, en los puertos del país se desembarcan miles de toneladas de distintas especies. A veces una especie trae mucho menos de lo habitual y a veces mucho más. Para una planta procesadora o para quien controla la pesca, saberlo con anticipación cambia mucho. Por eso nos propusimos anticipar, con un mes de ventaja, si cada especie va a tener un mes normal, una caída o un aumento fuera de lo común.
>
> Antes de construir nada revisamos los datos, y ese fue nuestro primer gran hallazgo. El archivo público que habíamos elegido tenía las toneladas mal asignadas: especies y puertos importantes aparecían con una pequeña parte de lo que realmente se pescó. Con esos datos, cualquier modelo hubiera aprendido ruido. Así que cambiamos a las estadísticas oficiales del mismo organismo, y eso hizo posible todo el trabajo.

## Parte 2 · Alejandro Bernal

> Trabajamos con 43 especies, mes a mes, entre 2017 y 2025. El primer desafío fue definir qué es una anomalía, porque los datos no la traían.
>
> En el análisis exploratorio vimos que cada especie tiene su propia temporada: el calamar, por ejemplo, se pesca casi todo entre febrero y mayo. Entonces 50 toneladas de calamar en octubre es algo normal, pero en marzo sería una caída enorme. Por eso comparamos cada mes con el mismo mes de los años anteriores, y medimos la diferencia en proporción al tamaño de cada especie, para que una especie chica y una grande queden en la misma escala.
>
> Para decidir cuándo una diferencia es anormal usamos la regla del diagrama de caja que vimos en la materia. Así cada mes queda en una de tres clases: caída, normal o aumento. Separamos caída y aumento, como nos sugirió la cátedra, porque llevan a decisiones distintas: una caída significa falta de materia prima, y un aumento, exceso que hay que almacenar.

## Parte 3 · Pablo Paredes

> Después elegimos qué información usar para anticipar. La cátedra nos pidió probar el clima, las mareas y la ubicación de los puertos. Los incorporamos todos y los pusimos a prueba. Casi ninguno ayudó: la temperatura del mar y las mareas no cambiaban el resultado, y de la ubicación solo sirvió en cuántos puertos desembarca cada especie.
>
> Lo que sí ayuda es el calendario de cada especie y su historia reciente. La señal más fuerte es esta: se esperaba que empezara la temporada, pero el mes anterior ya venía flojo.
>
> Como modelo usamos un bosque aleatorio, que combina cientos de árboles de decisión, cada uno aprendiendo de una parte distinta de los datos. Como las anomalías son pocas, le dimos más peso a esos casos para que el modelo no las ignore. Y lo entrenamos respetando el tiempo: aprende con los años anteriores y lo evaluamos en 2024 y 2025, años que nunca vio.

## Parte 4 · David Rodrigues

> ¿Funcionó? Lo comparamos con dos reglas simples: decir siempre «normal» y repetir lo que pasó el mes anterior. El modelo les gana a las dos. Detecta más de la mitad de las caídas, casi el doble que repetir el mes anterior, y siete de cada diez caídas grandes, que son las que más importan.
>
> En la práctica lo proponemos como una lista de prioridades: si cada mes se revisan las tres especies con más riesgo, se encuentran cuatro de cada diez caídas, con una precisión unas seis veces mejor que elegir al azar.
>
> También tiene límites. Los aumentos son más difíciles de anticipar, y muchas anomalías dependen de cosas que no están en los datos, como vedas, cupos o conflictos. Ese sería nuestro próximo paso.
>
> Como conclusión: el modelo cumple en parte el objetivo, y la lección más grande fue revisar la calidad de los datos antes de modelar. Muchas gracias.

## Recomendaciones para grabar

- Duración total estimada: 4 minutos 50 segundos. Si alguien se pasa, recorta primero el segundo párrafo de su parte.
- Grabar en horizontal, con buena luz y sin ruido; cara en un recuadro chico y diapositiva en pantalla completa, o alternando.
- Usar el guion como guía y decirlo con palabras propias.
- Dejar 2 segundos de silencio al principio y al final de cada parte para facilitar la edición.
- No mostrar código.

## Preguntas probables en la presentación en vivo

| Pregunta | Respuesta corta | Quién responde |
| --- | --- | --- |
| ¿Por qué no usaron el dataset de la entrega inicial? | Sus kilos no corresponden a especie, puerto ni flota: persistencia mes a mes de −0,008 (0,397 en los datos oficiales) y repartos que no coinciden con las tablas oficiales. | Iñaki |
| ¿Por qué no un umbral fijo en toneladas? | Las especies van de pocas toneladas a 50.000 por mes y cada una tiene su temporada. | Alejandro |
| ¿Qué pasa si el nivel habitual es 0? | Tiene un piso de 10 t, el mismo umbral que se usó para elegir las especies. | Alejandro |
| ¿Por qué 1,5 × RIC? | Es la regla estándar del diagrama de caja; con ese valor hay unas cinco alertas por mes sobre 43 especies. | Alejandro |
| ¿Hay fuga de información? | No: todas las variables terminan en el mes anterior, hay controles con `assert` (4.8.2) y los años de prueba no se usaron para decidir nada. | Pablo |
| ¿Por qué no `train_test_split`? | Mezclaría meses futuros en el entrenamiento; con series temporales se separa por años. | Pablo |
| ¿Por qué no SMOTE? | Interpolaría historias de especies distintas y crearía casos imposibles; se usan pesos de clase. | Pablo |
| ¿Por qué un solo modelo? | La pauta no admite comparar modelos; las líneas base son reglas simples, no modelos. | Pablo |
| ¿Por qué 0,90 y no 0,7 en Pearson? | Con 0,7 se pierden rezagos que el modelo usa y el F1 macro de validación baja de 0,533 a 0,521. | Pablo |
| ¿Hay sobreajuste? | Moderado: F1 macro de 0,748 en entrenamiento y 0,484 en prueba, cerca de la validación temporal (0,533). | David |
| ¿Por qué la exactitud no sirve? | "Siempre normal" tiene 0,892 de exactitud y no detecta ninguna anomalía. | David |
