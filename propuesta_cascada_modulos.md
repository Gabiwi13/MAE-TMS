# Cascada de módulos: malas → buenas partidas → revisión humana

**Fecha:** 19 de octubre de 2026
**Estado:** fijada antes de correr. Lo que cambie después se declara en el informe como desviación.

## 1. Pregunta

En el experimento de cierre, el esquema «ambas» casi nunca dijo «nadie la reconoce». Ante un tipo de falla nunca visto se abstuvo en el 2.6 % de los casos y dejó pasar el 34.2 % como buena, porque el módulo de buenas tiene una envolvente ancha. Si el módulo de buenas se parte en varios especialistas más estrechos, ¿la cascada manda a revisión humana las fallas nuevas en vez de dejarlas pasar? ¿A qué costo en piezas buenas mandadas a revisión? ¿Le gana a la confianza de la red con la misma cantidad de revisión?

## 2. Diseño

Misma red especializada y mismos repartos que la parte 2 del cierre: WideResNet50, capas 3 y 4 ajustadas, buenas contra malas, tipo primario más frecuente excluido, semilla 42. Se reentrena; las cifras pueden diferir un poco de las del cierre por el no determinismo de la GPU. Esta vez se guardan los latentes.

**Módulos sobre el latente de 64**, con una cuantización común (el rango de lo registrado y margen del 10 %) y 16 variantes por imagen registrada:
- **malas:** un especialista con las fallas de entrenamiento;
- **buenas, partido en k ∈ {1, 2, 4, 8}:** k-means (semilla 42) sobre los 270 originales de llenado. Cada grupo es un especialista con sus imágenes y sus variantes.

**Cascada:** si el módulo de malas la contiene, es **mala**. Si no, y algún especialista de buenas la contiene, es **buena**. Si no, es **desconocida** y va a revisión humana.

**Medidas:**
- Test conocido (normales de test y el 40 % de las fallas de tipos entrenados): detección, falsa alarma y revisión humana de normales y de fallas.
- Tipo nunca visto: desconocida, mala y buena (falla silenciosa).

**Rivales a igual revisión humana:** la cabeza de la red con abstención por MSP, por energía y por distancia kNN (de dos clases). Su umbral se fija para que manden a revisión la misma fracción del test conocido que la cascada con cada k; lo que no mandan a revisión lo decide el argmax (kNN: la mayoría de 5 vecinos).

## 3. Predicciones

- **PC1.** Al subir k, sube la revisión humana de las fallas nuevas y baja la falla silenciosa. También sube la revisión de normales conocidas.
- **PC2.** Con k = 1 la cascada se parece a «ambas» del cierre (abstención en lo nuevo de alrededor del 3 %).
- **PC3.** No sé si a igual revisión la cascada le gana a MSP. Mi apuesta débil es que con k = 8 queda cerca de MSP, sin ganarle por 10 puntos.

## 4. Criterio

- **«Partir los módulos de buenas hace útil la cascada»** queda **sostenido** si, para algún k, la falla silenciosa en el tipo nuevo es al menos 10 puntos menor que la de MSP y la de la energía a igual revisión humana en lo conocido (media de 11 piezas), y la falsa alarma en normales conocidas no supera en más de 2 puntos a la de la cabeza.
- Queda **refutado** si para ningún k la falla silenciosa de la cascada baja de la de MSP.

## 5. Entregables

`run_cascada_modulos.py` (latentes en `results/cascada_modulos/cache/`, fuera de git) y `results/cascada_modulos/{README.md, resumen.txt, resultados.json}`.
