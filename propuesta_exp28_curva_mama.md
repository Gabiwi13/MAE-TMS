# Propuesta del experimento 28: ¿más datos ayudan en cáncer de mama?

**Estado:** propuesta; nada corrido. Se fija antes de correr y pide aprobación.

## Pregunta

Con BreastMNIST (ultrasonido de mama, 128 px), ¿cuánto mejora cada método al tener más casos de entrenamiento? ¿La mejora viene de la percepción (el encoder) o del registro en la memoria? ¿Cuántos malignos se escapan sin aviso?

Sirve para la reunión con médicos: decide si vale pedirles más datos del mismo tipo y qué se puede prometer sobre la sensibilidad.

## Datos

BreastMNIST 128 px, ya descargado (`data/medmnist/breastmnist_128.npz`). Sin descargas.

| split | maligno | normal o benigno |
|---|---|---|
| train | 147 | 399 |
| val | 21 | 57 |
| test | 42 | 114 |

El test es fijo y completo en todos los brazos. La validación solo se usa para calibrar el conformal (Mondrian).

## Diseño

**Fracciones de entrenamiento:** 25, 50, 75 y 100 % del train, muestreo estratificado por clase y anidado (el 25 % está dentro del 50 %, y así). Con 5 semillas de submuestreo (42 a 46). Al 100 % las semillas solo cambian el entrenamiento del encoder.

**Dos brazos de percepción:**
- **A, encoder fijo:** el ResNet18 de la corrida balanceada, ajustado con todo el train. Solo cambia lo que se registra. Mide cuánto le sirven los datos a la memoria por sí sola.
- **B, encoder reentrenado con la fracción:** el mismo procedimiento de `trained_level2` (ResNet18 de ImageNet, muestreo balanceado, aumentos, Adam 1e-4), con el **mismo número total de pasos** (64 pasos de 64 imágenes) en todas las fracciones. Así la diferencia es de datos, no de cómputo. Mide al sistema completo.

**Dos registros en la memoria:**
- **completo:** toda la fracción, 60 % para llenar y 40 % para la fase A, con 16 variantes.
- **igualado:** las dos clases con el mismo número de casos, el de la clase más chica (se submuestrean los benignos). Prueba el ancho de la envolvente.

La regla balanceada oficial, N = máx(328, clase más chica), coincide con «completo» en todas las fracciones salvo al 100 % (benignos 328 de 399). Por eso no se usa como brazo; solo sirve para la verificación.

**Métodos sobre los mismos latentes:**
- **memoria:** el nivel 2 de mama con el protocolo oficial (`Level`: Q = 32, umbral de energía, ξ = 0, directorios perspectivales, entrada por el no especialista);
- **prototipos:** la media por clase y la clase más cercana;
- **kNN** (k = 5);
- **la cabeza lineal del encoder;**
- **Mondrian:** conformal por clase sobre la cabeza, calibrado con la validación.

## Medidas

- **Sensibilidad estricta:** malignos con respuesta «maligno» / 42, con intervalo de Wilson al 95 %.
- **Especificidad:** benignos con respuesta «benigno» / 114, con intervalo de Wilson.
- **Acierto balanceado** y **AUROC** para los métodos que dan puntaje (cabeza, kNN y prototipos).
- **Malignos que se escapan en silencio:** el caso que importa clínicamente.
  - En la memoria: respuesta «benigno» en estado claro, es decir, solo el especialista benigno contiene la imagen (los tres estados de exp23).
  - Todo lo demás va a revisión humana: estado ambiguo, desconocido o rechazo.
- **Fracción enviada a revisión** sobre los 156 casos de prueba.
- **Comparación a igual carga de revisión:**
  - la cabeza manda a revisión la misma fracción que la memoria, eligiendo los casos de menor margen;
  - Mondrian manda a revisión las listas con dos clases o vacías, con alfa fijado para igualar esa fracción.
  - Se cuentan los malignos que se escapan en silencio en cada método.
- **Por fracción:** la media de las 5 semillas y su rango (mínimo y máximo).

## Verificación antes de leer la curva

Con la semilla 42, el 100 %, el encoder en caché de la corrida balanceada y la regla oficial, el nivel 2 de mama tiene que dar lo de `results/medico_balanceado`: 28 de 42 malignos y 109 de 114 benignos, con 87.8 % de acierto. Si no lo reproduce, se para y se busca la causa antes de seguir.

En el brazo B, con la semilla 42 y el 100 %, el encoder reentrenado puede no ser idéntico bit a bit al de la caché, por el no determinismo de la GPU. Si difiere, se reporta la diferencia.

## Predicciones

| | predicción | cómo se decide |
|---|---|---|
| P1 | Los datos le sirven sobre todo a la percepción. En el brazo B, la cabeza, kNN y prototipos ganan **≥ 5 puntos** de acierto balanceado entre el 25 y el 100 %. En el brazo A ganan **≤ 3** | media de 5 semillas |
| P2 | Con registro completo, la sensibilidad estricta de la memoria **no sube** del 25 al 100 % (cambio ≤ +3 puntos), porque la envolvente benigna se ensancha más que la maligna. Al 100 %, la sensibilidad con registro igualado supera a la del completo en **≥ 5 puntos**, a costa de especificidad | brazo A y brazo B |
| P3 | (incierta) La curva del mejor método no está saturada: la ganancia del 75 al 100 % es positiva y mayor que el rango entre semillas | brazo B |
| P4 | A igual carga de revisión, la memoria deja escapar en silencio **igual o más** malignos que la cabeza con umbral y que Mondrian | brazo B al 100 %, media de semillas |
| P5 | Al 100 %, el intervalo de Wilson de la sensibilidad mide **≥ 25 puntos de ancho** en todos los métodos, y los de la memoria, kNN y la cabeza se solapan. Con 42 malignos no se puede decir cuál detecta más | semilla 42 |

## Criterio

- **«Más datos del mismo tipo ayudan»:** se sostiene si el mejor método del brazo B gana ≥ 5 puntos balanceados del 25 al 100 % **y** la ganancia del 75 al 100 % es mayor que el rango entre semillas. Si gana menos de 2 puntos, se refuta: en ese caso pedirles a los médicos más ultrasonidos del mismo tipo no sería la prioridad.
- **«La memoria aprovecha los datos como los demás»:** se sostiene si su ganancia, con su mejor registro, es al menos la mitad de la de los prototipos en el mismo brazo; si no, se refuta.
- **«La revisión de la memoria tiene valor propio»:** se sostiene solo si, a igual carga de revisión, deja escapar en silencio **al menos 2 malignos menos** que la cabeza y que Mondrian (media de semillas). Si no, la propiedad de los tres estados queda como explicación del mecanismo, no como ventaja.

## Costo

Unos 60–90 min con la GPU: 4 fracciones × 5 semillas × 2 brazos × 2 registros = 80 configuraciones. Cada una registra unos 500 casos con 16 variantes. Un solo proceso, sin competir con la sesión industrial por memoria. Sin descargas.

## Archivos

`run_experiment28_curva_mama.py` reutiliza `run_medico_demo` (datos, `Backbone`, `Level`, `latents`) sin modificarlo. Resultados en `results/experimento28/` (`README.md`, `resumen.txt`, `resultados.json`) y caché en `results/experimento28/cache/`, fuera de git. Todo en la rama `medico-demo`.

## Lo que no responde

- Más resolución (BreastMNIST a 224 px requiere descarga).
- Otras fuentes del mismo paciente (mamografía, edad, BI-RADS).
- Datos de otro hospital.

Ninguno de los tres se infiere de esta curva.
