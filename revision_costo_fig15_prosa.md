# Propuesta viejo/nuevo: costo computacional y figura 15

**Estado:** pendiente de aprobación. La figura 15 ya está regenerada y copiada a `.tex8/figuras/`; el texto que la describe no se ha tocado.

---

## 1. Costo computacional (`05_resultados.tex:518–567`)

**Medición.** Pipeline completo (etapas 1 a 8) desde cero, el 1 nov 2026, en la carpeta aparte `MAE-TMS-costo`, solo en CPU (`CUDA_VISIBLE_DEVICES` vacío). Resultado en `results/computational_cost/nov2026_cpu/{cost.json, report.md}`, con una nota de condiciones (`NOTA.md`).

| Etapa | Minutos |
|---|---:|
| 1. Partición del conjunto de datos | 0.00 |
| 2. Entrenamiento del encoder | 21.48 |
| 3. ConceptNet | 0.30 |
| 4. fastText | 0.28 |
| 5. Llenado de las memorias de contenido | 37.42 |
| 6. Fase temprana (texto) | 0.94 |
| 7. Hemisferio visual | 40.03 |
| 8. Fase madura (texto) | 2.42 |
| **Pipeline** | **102.9** |

**Lo que cambia respecto del texto actual.** La tabla vieja (133.5 min en otra laptop, con la batería de análisis, y la comparación entre dos laptops) era de antes de pasar a 16 variantes de llenado. La medición del 22 sep en esta misma máquina dio 50.6 min, con 10.3 min de llenado: un día antes de pasar a 16 variantes, cuando el llenado registraba 4 por imagen. Ahora son 3200 registros por módulo en lugar de 800, y el llenado tarda 37.4 min. Con eso, **la parte más cara ya no es el entrenamiento del encoder sino las memorias**: llenado y hemisferio visual suman el 75 % del total. La frase fija que imprime `run_cost_benchmark.py` al final de `report.md` («El entrenamiento del encoder domina el costo») ya no es cierta para esta medición; lo dice la nota.

**Viejo:** toda la subsección, desde «Se midió el tiempo de pared» hasta «Tabla completa en \texttt{results/computational\_cost/comparacion\_laptops.md}.»

**Nuevo:**
```latex
\subsection{Costo computacional}
\label{sec:costo}

Se midió el tiempo de pared (\textit{wall-clock}) de reproducir el sistema completo
desde cero, de la partición del conjunto de datos a la fase madura, en una laptop con
un Intel Core Ultra 7 265HX (20 hilos lógicos) y 16.6~GB de RAM, con la GPU oculta:
todo corre en CPU.
La Tabla~\ref{tab:costo} resume los tiempos.

\begin{table}[H]
    \centering
    \caption{Costo computacional de reproducir el sistema desde cero (etapas 1 a 8,
    solo CPU). Fuente: \texttt{results/computational\_cost/nov2026\_cpu/}.}
    \label{tab:costo}
    \small
    \begin{tabular}{lr}
        \toprule
        Componente & Tiempo \\
        \midrule
        Entrenamiento del encoder ResNet18 (50 épocas, 2624 imágenes) & 21.5 min \\
        Vocabulario: ConceptNet y fastText & 0.6 min \\
        Llenado de las memorias de contenido (8 módulos, 3200 registros cada uno) & 37.4 min \\
        Fases temprana y madura de texto & 3.4 min \\
        Hemisferio visual (fase A con 1024 imágenes, fase B con 656, evocación) & 40.0 min \\
        \midrule
        Sistema completo (etapas 1--8) & \textbf{102.9 min} \\
        \bottomrule
    \end{tabular}
\end{table}

El sistema completo se reproduce en 102.9 minutos.
La parte más cara no es el entrenamiento del encoder, la única con gradientes y
retropropagación (21.5 min), sino las memorias: el llenado de las ocho memorias de
contenido y el hemisferio visual suman 77.4 minutos, tres cuartas partes del total.
Ninguna de las dos entrena nada: registran vectores cuantizados en las memorias
(200 imágenes por 16 variantes en cada módulo) y los leen para decidir.
Las fases de texto, con el banco de 411 consultas, tardan menos de cuatro minutos.
```

**Cifras (verificadas en `cost.json`):** etapa 2 1288.6 s; etapas 3 + 4 = 34.4 s (0.57 min); etapa 5 2245.0 s; etapas 6 + 8 = 201.1 s (3.35 min); etapa 7 2401.7 s; total 6174 s = 102.9 min; 37.42 + 40.03 = 77.45 min = 75.3 %. 2624 = 328 imágenes de entrenamiento × 8 clases; 3200 = 200 × 16. La etapa 1 tarda 0.0 s porque la partición ya existe en disco; no tiene fila.

**Dudas para ti.**
- La medición corrió mientras el consejo de redacción revisaba la tesis: lecturas de archivos y búsquedas, en las etapas 5 y 7. El llenado tardó entre 4:05 y 4:37 min por módulo en siete de los ocho; `car` tardó 5:18, justo cuando arrancaron los revisores. A lo más es un minuto de ruido en 102.9. Si quieres una cifra limpia, volver a correr cuesta 1 h 45 min con la máquina sola.
- La tabla no incluye la batería de análisis (como pediste) ni la comparación entre laptops.

---

## 2. Figura 15 y el texto que la describe

**La figura nueva** (`.tex8/figuras/fig15_image_rejection.png`, generada con `generate_paper_figures.py` con τ aplicado, en el mismo orden que la etapa 7):
- Arriba: tres imágenes de prueba aceptadas (`apple` 599, `car` 333, `cow` 673; entre paréntesis, la puntuación de contención del módulo).
- En medio: dos vistas de `car` que ningún módulo contiene (ξ = 0) y una vista de `cow` cuyo latente no alcanza τ.
- Abajo: el ruido (norma 117.4) y los píxeles barajados (104.9) pasan τ y la contención los rechaza; el gris uniforme (norma 10.72, τ = 16.607) se rechaza antes de la memoria.

Las puntuaciones son unas cuatro veces las de la copia vieja (apple 151 → 599), y las rechazadas reales ya no son manzanas: la copia que tenía la tesis era de los modelos de 4 variantes. Las normas las calculé con el mismo encoder y `models/latent_energy_threshold.json`.

Los rótulos de la figura siguen en inglés en parte («noise», «solid», «scrambled», «containment», «MAE»). Se traducen con la propuesta de figuras; regenerarla tarda 13 s.

### 2a. Párrafo del rechazo (`05:345–359`)

**Viejo:**
```latex
La Figura~\ref{fig:rechazo-imagenes} ilustra el rechazo por containment: imágenes
reales que la memoria contiene se aceptan, mientras que imágenes reales no
contenidas y las sondas sintéticas de ruido y de píxeles barajados reciben puntuación
cero en los ocho módulos y se rechazan, sin que intervenga ningún filtro externo.
La tercera sonda sintética, un lienzo gris uniforme, \emph{sí} obtiene soporte del
contenido: es la excepción honesta del panel. El experimento 14 localizó la causa: el
encoder lleva las entradas sin estructura (gris uniforme, un objeto desenfocado o sin
contraste) a latentes de norma baja que caen dentro de la envolvente por coordenada de
los animales. Los grises de nivel 120 a 160 (el del panel, 127, cae en ese tramo) los
aceptan a la vez \texttt{cow}, \texttt{dog} y \texttt{horse}, aunque la instancia real más cercana
está a entre 2.4 y 4.4 veces la mediana de la distancia intraclase.
No es cualquier fondo liso: de 12 sólidos de color se aceptan 2.
Esos grises tienen norma de 10.7 a 13.0, por debajo de $\tau = 16.61$, y el umbral de
energía los rechaza antes de la memoria (Sección~\ref{sec:percepcion}).
Esta fuga con entradas degeneradas se retoma en la Sección~\ref{sec:limitaciones}.
```

**Nuevo:**
```latex
La Figura~\ref{fig:rechazo-imagenes} ilustra el rechazo: imágenes reales que la memoria
contiene se aceptan, mientras que imágenes reales no contenidas y las sondas sintéticas
de ruido y de píxeles barajados reciben puntuación cero en los ocho módulos y se
rechazan, sin que intervenga ningún filtro externo.
La tercera sonda, un lienzo gris uniforme, no llega a la memoria: la norma de su
latente (10.7) queda por debajo del umbral de energía $\tau = 16.61$
(Sección~\ref{sec:percepcion}), igual que una vista real de \texttt{cow} del panel.
Sin ese umbral, el contenido sí le daría soporte. El experimento 14 localizó la causa:
el encoder lleva las entradas sin estructura (gris uniforme, un objeto desenfocado o sin
contraste) a latentes de norma baja que caen dentro de la envolvente por coordenada de
los animales. Los grises de nivel 120 a 160 (el del panel, 127, cae en ese tramo) los
aceptan a la vez \texttt{cow}, \texttt{dog} y \texttt{horse}, aunque la instancia real
más cercana está a entre 2.4 y 2.9 veces la mediana de la distancia intraclase.
No es cualquier fondo liso: de 12 sólidos de color se aceptan 2.
Esos grises tienen norma de 10.7 a 13.0, y el umbral los rechaza.
Las entradas degeneradas que sí pasan el umbral se discuten en la
Sección~\ref{sec:limitaciones}.
```
**Por qué:** el gris ya no se acepta en la figura; «la excepción honesta» describía la figura vieja. El 4.4 → 2.9 es el hecho E11 de `revision_consejo_hechos.md` (aquí ya incluido). Fuentes: norma del gris 127 = 10.72 (calculada); `results/experimento14/README.md`, grises 120–160 (normas 10.69–13.04; distancias 13.9–16.5 con mediana 5.7).

### 2b. Pie de la figura (`05:370–377`)

**Viejo:** «Rechazo de imágenes por la memoria (containment, sin filtro léxico). Arriba: imágenes reales aceptadas por el contenido. En medio: imágenes reales no contenidas, rechazadas ($\xi = 0$). Abajo: sondas sintéticas fuera de dominio: el ruido y los píxeles barajados se rechazan; el gris uniforme obtiene soporte, una fuga con entradas degeneradas que en el sistema completo cierra el umbral de energía (la figura no lo aplica) y que se discute en la Sección~\ref{sec:limitaciones}. El rechazo emerge de la ausencia de soporte, y la figura muestra también su excepción.»

**Nuevo:**
```latex
\caption{Rechazo de imágenes en el hemisferio visual (sin filtro léxico), con el umbral
de energía $\tau$ y la contención en el mismo orden que el sistema. Arriba: imágenes de
prueba aceptadas por el contenido, con el módulo de mayor soporte y su puntuación de
contención. En medio: imágenes de prueba rechazadas, dos porque ningún módulo las
contiene ($\xi = 0$) y una vista de \texttt{cow} porque la norma de su latente no
alcanza $\tau$. Abajo: sondas sintéticas; el ruido y los píxeles barajados reciben
puntuación cero en los ocho módulos, y el gris uniforme se rechaza antes de la memoria
por el umbral $\tau$.}
```

### 2c. Discusión, limitación (b) (`06:248–253`)

**Viejo:** «En sentido inverso, el containment visual también tiene una fuga con \emph{entradas degeneradas}: una imagen de color sólido uniforme obtiene soporte y se acepta (Figura~\ref{fig:rechazo-imagenes}), presumiblemente porque el fondo liso de ETH-80 puebla esa región del espacio latente; las sondas estructuradas (ruido, píxeles barajados) sí se rechazan.»

**Nuevo:**
```latex
En sentido inverso, el containment visual tiene una fuga con \emph{entradas
degeneradas}: sin el umbral de energía, el contenido da soporte a un lienzo gris
uniforme, porque el encoder lleva las entradas sin estructura a latentes de norma baja
que caen dentro de la envolvente de los animales
(Sección~\ref{sec:hemisferio-visual}); las sondas con estructura (ruido, píxeles
barajados) se rechazan por contención (Figura~\ref{fig:rechazo-imagenes}).
```
**Por qué:** la figura ya no muestra el gris aceptado, y «presumiblemente porque el fondo liso» contradecía a 05, donde el experimento 14 localiza la causa (lo señaló el revisor de antipatrones). La frase siguiente («Densificar agranda esa fuga…») se queda.

Si apruebas la decisión T de términos, «containment» pasa a «contención» también aquí.
