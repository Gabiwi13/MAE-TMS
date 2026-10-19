# Demo industrial: propuesta de diseño

**Fecha:** 18 de octubre de 2026
**Estado:** fijada antes de correr. Lo que cambie después se declara en el informe como desviación.

## 1. Pregunta

En una línea donde pasan piezas distintas, ¿el sistema EAM-TMS rutea cada pieza a su especialista y el especialista, que solo conoce piezas sanas, rechaza las piezas con falla? ¿Ese rechazo detecta fallas mejor, igual o peor que los detectores estándar sobre los mismos latentes?

## 2. Datos

VisA (Zou et al., ECCV 2022; Amazon, CC BY 4.0), `VisA_20220922.tar` de S3, verificado contra el ETag multiparte (`05c8…0cfb-113`), extraído fuera de git en `C:\Users\aq99l\Datasets\VisA`. Partición oficial `1cls.csv`: 12 piezas (candle, capsules, cashew, chewinggum, fryum, macaroni1, macaroni2, pcb1–pcb4, pipe_fryum); train solo normales (450 a 905 por pieza); test 50 a 101 normales y 100 fallas por pieza (1200 fallas). Tipos de falla en `image_anno.csv` de cada pieza; una imagen puede tener varios.

Preproceso: cada imagen se lleva a 224 × 224 RGB sin recorte (las fallas pueden estar en el borde y un recorte central las quitaría).

## 3. Diseño

**Registro.** Por pieza, N = máx(328, pieza más chica) = 450 normales de train, barajadas con semilla 42: las primeras 270 (60 %) son el llenado y las 180 restantes (40 %) la fase A. Las mismas 180 son las **normales de calibración**: el especialista nunca las registró (la fase A solo escribe en los directorios). El resto del train no se usa.

**Nivel 1, ruteo por pieza.** Encoder: ResNet18 de ImageNet congelado (salida del average pooling, 512) + PCA a 64 ajustada sobre todas las normales de train de las 12 piezas. Protocolo de `run_medico_demo.py` sin cambios (clase `Level`): llenado con 16 variantes, Q = 32, umbral de energía, fase A con ganador por `recognize_gated_right`, directorios perspectivales, `route_transactive` desde un no especialista con ξ = 0. Comparación: kNN (k = 5) sobre los mismos latentes. Se evalúa sobre todo el test, normales y fallas por separado.

**Nivel 2, detección de fallas por rechazo.** Un especialista por pieza, lleno solo con sus 270 normales × 16 variantes. Falla = el especialista no contiene la pieza (alguna coordenada sin soporte, ξ = 0) o queda bajo su umbral de energía. Tres percepciones, fijadas aquí:

- **G1**: los latentes del nivel 1 (es el especialista del nivel 1 tal cual).
- **G2** (principal): misma ResNet18, PCA a 64 ajustada sobre los 270 originales del llenado de esa pieza; cuantización con el rango del llenado de esa pieza con el margen del 10 % de `Level`.
- **P (por parches, estilo PatchCore)**: capas 2 y 3 de la ResNet18 (la 3 interpolada a 28 × 28), promedio local 3 × 3, 384 canales por posición, 784 parches por imagen; PCA a 64 ajustada sobre parches del llenado de la pieza. Una memoria por pieza registra los 784 parches de cada uno de los 270 originales (sin variantes: las rotaciones mezclan posiciones y multiplican por 16 un llenado de 211 680 parches). Falla = algún parche no contenido. Sin umbral de energía (es una regla por imagen).

**Detectores sobre los mismos latentes de cada percepción**, ajustados al llenado (originales):
- kNN: similitud coseno media a los 5 vecinos (global) — en P, distancia euclídea al parche más cercano del llenado y máximo sobre los parches de la imagen (PatchCore sin coreset).
- Mahalanobis estilo PaDiM global: una gaussiana por pieza, covarianza + 0.01 I (en P, una gaussiana común a todas las posiciones; máximo sobre parches).

**Comparación justa.** La memoria tiene un punto de operación: acepta una fracción A de las normales de calibración. Cada detector se fija para aceptar esa misma fracción A de esas mismas normales. Luego, en test: rechazo de fallas (detección) y rechazo de normales (falsa alarma) de cada método. Se da también el AUROC de test (normales contra fallas) de cada detector y de una **lectura graduada de la memoria**: número de coordenadas sin soporte (en P, el máximo sobre los parches). Esa lectura es la misma regla de contención contada, no el punto de operación del sistema; se reporta aparte.

**Punta a punta.** Imagen de test → nivel 1; si va a su pieza, el especialista G2 de esa pieza decide; si el nivel 1 la rechaza, cuenta como alarma; si la manda a otra pieza, se cuenta como ruteo falso.

**Análisis secundario: tipos de falla como dominios.** Por pieza, tipos con etiqueta única y al menos 10 imágenes; 60 % llenado (16 variantes, percepción G2), 40 % test, estratificado, semilla 42. Asignación por `recognize_gated_right` máximo entre los especialistas de tipo (todos en cero = rechazo); kNN k = 5 sobre los mismos originales. Sin fase A ni directorio: con 6 a 30 imágenes por tipo no hay con qué formar directorios. Se reporta con n y azar.

## 4. Predicciones

- **P1.** Nivel 1: ≥ 95 % de acierto de lo respondido en normales; las fallas se rutean a su pieza casi igual que las normales (la identidad de la pieza domina el vector global). Confusiones, si hay, entre pcb1–pcb4 y entre macaroni1 y macaroni2.
- **P2.** G1 y G2: la memoria rechaza parte de las fallas, pero también parte de las normales de test. A igual aceptación de normales de calibración, kNN y Mahalanobis detectan igual o más que la memoria (lo de exp20: el rechazo de la memoria es de cobertura). G2 detecta más que G1 porque su PCA mira la variación de una sola pieza. AUROC global de kNN y Mahalanobis en G2 entre 0.75 y 0.90; la lectura graduada de la memoria, por debajo.
- **P3.** P: el kNN por parches tiene el AUROC más alto de todo el demo (≥ 0.85 de media). La memoria por parches satura: con 211 680 parches registrados casi todos los niveles dentro del rango quedan con soporte, así que rechaza poco más que valores extremos; su detección a su punto de operación queda muy por debajo de la de PatchCore a igual aceptación.
- **P4.** Tipos de falla: memoria y kNN por encima del azar en las piezas con tipos visualmente distintos (pcb: melt, missing, bent, scratch), con mucho rechazo de la memoria; empate o peor que kNN en lo respondido.

## 5. Criterio

Se mide por pieza en las 12, sobre G2 (principal) y P:
- «La memoria detecta fallas como los detectores estándar» queda **sostenida** si, a igual aceptación de normales de calibración, su rechazo de fallas en test es ≥ al mejor de kNN y Mahalanobis menos 2 puntos en al menos 8 de las 12 piezas, y **refutada** si queda más de 2 puntos por debajo en al menos 8. La predicción, por exp20, es la refutación.
- «El rechazo por cobertura detecta algo» queda **sostenida** si, en la media de las 12 piezas, la memoria rechaza al menos 20 puntos más fallas que normales de test, y **refutada** si la diferencia es menor de 5.

## 6. Entregables

`run_industrial_demo.py` (caché de imágenes y latentes en `results/industrial/cache/`, fuera de git; `--report-only`), `results/industrial/{README.md, resumen.txt, resultados.json}`.
