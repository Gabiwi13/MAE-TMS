# Plan de cierre: pesos homo, por prioridad

**Estado:** propuesta, pendiente de aprobación. No se corre nada hasta aprobarla.
**Fecha:** 28 oct 2026.

## Prioridades

1. **Sistema principal (ETH-80).** Es lo que se presenta: tiene que quedar pulido.
2. **Industrial (VisA).** Sostiene el resumen de CIFIN 2026, que se adaptará para la revista de la UACJ.
3. **Médico.** Diferido.

Una prioridad empieza cuando la anterior está cerrada, salvo las corridas largas, que se lanzan de noche mientras se trabaja en la prosa.

## Reglas para no dejar cosas atrás

1. **Inventario.** `inventario_experimentos.md`: una fila por script, con rama, qué memorias lee, pesos, versión del sistema (llenado, directorio, pesos) y commit de la última corrida. Si la versión no es la actual, el resultado está **desactualizado**.
2. **Criterio antes de correr.** Qué mide y cómo se lee, escrito aquí antes de lanzarlo. Nada se ajusta después de ver el número.
3. **Commit al terminar** cada corrida, con el commit del código en el mensaje.
4. **Búsqueda de dependientes.** Si se cambia una lectura, se buscan todos los scripts que la usan, también por imports indirectos.
5. **Prosa solo con aprobación**, con la propuesta viejo/nuevo.

## Fase 0. Congelar lo que hay (15 min, sin decisiones)

- Commit de los resultados de las colas en `pesos-homo` y `pesos-homo-md`, más el cambio de exp28. Nada se sube.
- Crear `inventario_experimentos.md` con todos los `run_*.py` y las etapas.
- Listo cuando: `git status` limpio en las dos carpetas y el inventario tiene todos los scripts.

---

## Prioridad 1. Sistema principal (ETH-80)

### Dónde estamos

El núcleo quedó idéntico con pesos homo: fase A 99.9 %; ruteo 631/656 = 96.2 % con 2 errores; evocación 97.4 %; fidelidad 16/16. Lo pendiente está en lo que rodea al núcleo.

### Lo que la tesis cita y hay que arreglar

| # | Qué | Problema | Costo |
|---|---|---|---|
| 1.1 | **κ (exp2, tabla `tab:grid-iota-kappa`)** | la tesis muestra columnas de κ idénticas; con la compuerta corregida siguen idénticas porque κ ≤ 1.5 nunca rechaza. La tabla no prueba κ | 15 min de cómputo + texto |
| 1.2 | **Cifras de la fase madura de texto** | exp2/exp3: sin normalizar 71.2 → 72.5 %. Ablación: base 87.0 → 85.3; G 94.0 → 93.5 (mejora +7.0 → +8.3) | solo prosa |
| 1.3 | **Figuras de la tesis** | se regeneraron fig02, 03, 04, 09 y 16; fig11 (espacio semántico) y fig15 (rechazo de imagen) no leen pesos | revisión visual, 15 min |

**1.1, criterio declarado:** primero se mide, para cada consulta del banco, la razón (activación media por celda) / mem.mean. La rejilla de κ va de su mínimo a su máximo por cuantiles (0, 10, 25, 50, 75, 90 y 100 %). No se elige κ mirando la exactitud. Se reporta la tabla completa, rechace o no.

### Lo que está en el repo y no en la tesis (decidir qué entra en la presentación)

| # | Qué | Estado | Costo |
|---|---|---|---|
| 1.4 | **Metaconocimiento perspectival en texto (exp9 y exp8, mitad texto)** | medidos con el directorio global; el oficial es perspectival con solo 16 interacciones de texto | ~1 h |
| 1.5 | **exp12** (brecha contra solapamiento) | la correlación desaparece (r 0.45 → 0.00); mezcla pesos y 4 → 16 variantes | ~7 h, de noche |
| 1.6 | **missing_cue** | menos recuperaciones perfectas; misma mezcla | ~10 min |
| 1.7 | **exp17 B y C, exp18** | no se volvieron a correr | por medir (horas) |
| 1.8 | **exp19** (checkout `MAE-TMS-exp18`) y **exp22** (solo en `origin/exp7-directorio-unificado`) | no se volvieron a correr | por medir |
| 1.9 | **rejection_probe** | de agosto, memorias viejas | ~minutos, o declararlo obsoleto |
| 1.10 | **Textos generados** | exp7: «96.2 % vs 96.2 % difiere»; exp2 no dice si κ rechazó; exp11: «DISTINTOS 4/8» sin explicar; exp14 dice «agentes v5» | 30 min |

**1.4, criterio declarado:** se forman los directorios de texto con el registro oficial (entrada + ganador) sobre las 240 consultas de formación de exp10, con entrada al azar, y se vuelve a correr la mitad texto con 16, 60, 120 y 240 interacciones. Se reporta la curva de «ruteado al miembro perdido» contra interacciones, entre el piso actual (40/411) y el techo global (229/411). Sin umbral de éxito.

**1.5 y 1.6, criterio declarado:** se corren con pesos uniformes sobre las memorias actuales, en una carpeta de salida aparte. Si el resultado con uniformes se parece al viejo, el cambio es de los pesos; si se parece al nuevo, es de las 16 variantes. Se reportan las dos cifras.

### Cierre de la prioridad 1

- Propuesta `revision_pesos_homo_principal_prosa.md` viejo/nuevo para `.tex8` (secciones 4 a 7), README, CONTEXTO, INICIO, `modelo_formal.md` (línea 38, «con pesos uniformes», y Prop. 3) y `discusion_marco_teorico_directorio.md`.
- Listo cuando: la apruebas, se aplica y cada script de ETH-80 está al día en el inventario.

---

## Prioridad 2. Industrial (CIFIN → revista de la UACJ)

### Las cifras del resumen y de dónde salen

| Cifra del resumen | Script | ¿La mueven los pesos? |
|---|---|---|
| AUROC 0.789 (MAE) · 0.800 (Mahalanobis) · 0.784 (kNN) | `run_parametros_mae` / `run_industrial_demo` | no (se verificó: la lectura en grado no pasa por el ruteo) |
| 0.695 contra 0.830 de PatchCore en fallas pequeñas | ídem | no |
| Identifica la pieza 98.4 %, sin confusiones | `run_enrutador_flota` / `run_industrial_clip` | pasa por el ruteo, pero sin confusiones entre agentes que contienen la pista: no debería |
| Fallas pequeñas de 28 % a 59 % | `run_parametros_mae`, parches: H 28.2 contra PatchCore 58.7 (todas las fallas, no solo pequeñas) | no |
| Escapan 37.9 % contra 39.2 % del detector que conoce la pieza | `run_enrutador_flota` / cierre | ídem que 98.4 % |
| 100 % de piezas nunca registradas como desconocidas (kNN 0 %) | `run_industrial_demo` | no (es contención) |
| Agregar o retirar sin reentrenar; olvido exacto; sin imágenes | `run_olvido_privacidad` | no (ya se volvió a correr con pesos homo: 0 de 2162 decisiones distintas) |
| La elección del módulo se explica con conteos y aciertos | piloto, etapas 1 y 2 | ya se volvió a correr con pesos homo; R2 > R1 sale más fuerte |

### Tareas

**Decisión del 28 oct:** como el resumen aceptado se puede corregir, la parte industrial también pasa a pesos homo. Se quita la excepción de los 5 scripts de CIFIN y las cifras corregidas salen de la corrida con pesos homo. `use_uniform_weights()` se conserva solo para los controles.

| # | Qué | Costo |
|---|---|---|
| 2.1 | **Rastrear «28 % → 59 %»** hasta un archivo de resultados. Si no aparece, sale del resumen corregido | 30 min |
| 2.2 | **Quitar `use_uniform_weights()` de los 5 scripts de CIFIN y volver a correrlos, más cierre, cascada y red_sintetica**, como resultados oficiales | por medir (estimo 1–3 h) |
| 2.3 | Comparar cada cifra del resumen, vieja contra nueva, y escribir el resumen corregido | 1 h |
| 2.4 | Commit de la línea de flota ya corrida y su prosa | solo prosa |
| 2.5 | Los experimentos pendientes de `plan_articulo.md` (nombrar la falla, mapa de la falla, calibración, edición sin efectos colaterales): ¿entran en la revista? (decisión D3) | según D3 |

**2.2, criterio declarado:** las cifras del resumen corregido son las de la corrida con pesos homo. Cada una se compara con la del resumen enviado; si alguna cambia, se dice cuánto y por qué. No se elige la que salga mejor.

---

## Prioridad 3. Médico (diferido)

- Mama pierde sensibilidad a malignos con pesos homo (28 → 25 de 42; exp28 59.5 → 51.9 %): medir si viene de la mayoría benigna en los pesos.
- exp20_ood, exp24 incremental y Mondrian no se volvieron a correr.
- Sincronizar las copias médicas en industrial-clip; exp20 y exp23 de esa rama tienen el bug del caché por `id()`.

---

## Decisiones que necesito

- **D1.** Para la presentación: ¿entran 1.4 a 1.9 (lo que no está en la tesis), o solo 1.1 a 1.3? Mi recomendación: 1.1 a 1.4 sí, porque el metaconocimiento es parte de la historia transactiva; 1.5 y 1.6 sí, porque son baratos o corren de noche; 1.7 a 1.9, solo si se presentan.
- **D2. Pesos de la parte industrial (resuelta, 28 oct):** homo, como el resto; el resumen se corrige con las cifras nuevas.
- **D3.** ¿Entran en la revista los experimentos pendientes de `plan_articulo.md`?
- **D4. Fechas (resuelta).** Correo de CIFIN del 27 de octubre: trabajo aceptado con folio **P176**. Se pueden hacer correcciones; el trabajo se vuelve a enviar ajustado a la plantilla oficial («resumen o extenso, según corresponda») por el formulario del correo. El **10 de noviembre** es el límite para avisar errores en la carta de aceptación. La parte visible del correo no dice la fecha para reenviar el trabajo; se toma el 10 de noviembre como límite hasta confirmarlo. El título se mantiene.

## Calendario (límite de trabajo: 10 de noviembre)

| Cuándo | Qué |
|---|---|
| 28 oct | Fase 0; 1.1, 1.6 y 1.10; lanzar 1.5 de noche |
| 29–30 oct | 1.4; 1.7 a 1.9 según D1 |
| 31 oct – 2 nov | propuesta de prosa de la prioridad 1 y su revisión |
| 3–6 nov | prioridad 2: 2.1, 2.2 (corre mientras se revisa la prosa), resumen corregido en la plantilla |
| 7–9 nov | revisión con la doctora; margen |
| 10 nov | límite; el envío por el formulario y el pago los haces tú |
| Al final | push como fast-forward con tu aprobación; borrar carpetas temporales |

## Nota aparte

`realtime_lab/salvaged_voice_camera.py` no se puede importar y nunca se corre; no se tocó.

## Bitácora

- **28 oct.**
  - **Hecho:**
    - Fase 0 (d0df16c, af52f80; inventario 2d191f8).
    - 1.1 κ por cuantiles (abf1735): con ι=0, κ solo rechaza; con ι ≥ 0.25 no actúa.
    - 1.6 control de missing_cue (aa283f6): el cambio viene de las 16 variantes.
    - 1.10 textos generados (224f7cd).
    - Propuesta de prosa de la prioridad 1: `revision_pesos_homo_principal_prosa.md`.
  - **1.4, curva de exp9:** con el ruteo transactivo, 90 → 368 de 411 a 240 interacciones, contra 393 del pizarrón. La mitad texto completa con 240 interacciones está corriendo.
  - **Prioridad 2:**
    - Se quitaron los pesos uniformes de los 5 scripts de CIFIN.
    - Cola `rerun/ind.json` lista; se lanza cuando termine exp9.
    - «28 % → 59 %» no aparece en ninguna rama, commit ni resumen: sale del resumen corregido salvo que se encuentre su fuente.
  - **Corriendo:** control de exp12 con pesos uniformes (~7 h); terminó el 29 oct, ver abajo.
  - **Industrial (tarde):**
    - Las 9 corridas con pesos homo salen idénticas a las uniformes (a2898e2): ninguna cifra del resumen cambia.
    - «28 % → 59 %» sí tiene fuente: la tabla de parches de `parametros_mae`.
    - Propuesta del resumen corregido en `revision_resumen_cifin.md`, pendiente de aprobación: quita «fallas pequeñas» (no hay corte por tamaño), dice el 12.5 % a revisión humana y que kNN con umbral también da 100 %.
  - **Noche:**
    - exp8 queda al día sin correr: sus sondas de texto describen el directorio oficial; la curva de formación está en exp9.
    - rejection_probe y exp22 re-corridos con pesos homo: idénticos byte a byte.
    - exp17 b y c y exp18 no se re-corren: pasan los pesos homo explícitos (`recog_weights`), ya eran homo.
    - **exp19, decisión tuya:** es el único que falta. Costo: ~2.2 h de cómputo (etapas 6–8 y exp16; el llenado no usa pesos y su exp18 ya pasa pesos explícitos) más portar el código de pesos homo al checkout `MAE-TMS-exp18`, que diverge. Ahí los pesos sí pueden mover decisiones: con el encoder congelado hay 83 ruteos falsos entre animales, donde varios agentes contienen la pista.
- **29 oct.**
  - 1.5 control de exp12: la correlación se pierde por las 16 variantes (uniformes 0.06, p 0.75; homo −0.00; vieja 0.45). Los pesos homo alejan a M2 1.0 en promedio, parejo en los pares. El oráculo del control es el homo de exp11: un oráculo uniforme costaría unas 2–3 h (estimado, sin medir).
  - exp19 con pesos homo (7d83bac en `MAE-TMS-exp18`, sin subir): etapas 6–8 y exp16 re-corridos sobre el mismo llenado (3.8 h). Ruteo de test 528 → 522 de 656 (rechazo 6.9 % igual), fase A 90.2 % igual, evocación 83.5 → 84.4 %; exp16 e2e conocido 76.3 → 75.7, nuevo 60.8 → 60.6, falso ruteo 14.4 → 14.6. Los pesos solo mueven el ganador entre animales; las conclusiones de exp19 se mantienen. Respaldo de los modelos viejos en `rerun/exp19_previo`.
  - **Criterio declarado antes de correr (homo como marginal):** se reemplaza cada memoria homo por la marginal de la hetero de su agente: la latente suma la relación sobre los niveles de etiqueta, la de etiquetas suma sobre los niveles latentes. Después se repiten, decisión por decisión, las lecturas oficiales: puntajes y ganador temprano de texto en las 411 consultas del banco y las 16 de la etapa 6; destino y compuerta del ruteo transactivo de texto; recuerdo texto→latente con la misma semilla; contención y puntaje de imagen, ruteo y evocación top-3 en las 656 imágenes de test. Predicción:
    - (1) la contención no cambia en ninguna pista;
    - (2) en imagen, puntajes, ruteo y evocación son idénticos, porque la marginal latente es igual celda por celda;
    - (3) en texto los puntajes cambian por el factor de 32 a 33, y las decisiones solo pueden cambiar en empates cercanos.

    Se reporta el número de decisiones distintas, sin umbral de éxito. Control: la corrida oficial repetida, para separar el azar del recuerdo.
  - **Criterio declarado antes de correr (¿cuándo agregan algo las homo?).** Con el llenado oficial las homo son la marginal de la hetero. Se prueban tres casos; los llenados nuevos viven en memoria y no tocan `models/`.
    - **A. Pesos y calidad del recuerdo** (`run_pesos_recuerdo.py`, modelos oficiales). En las 411 consultas del banco, el agente y la pista son los del ganador temprano oficial. Se recuerda texto→latente con pesos uniformes, homo y marginal, con dos semillas cada uno. El latente recordado se clasifica por vecino más cercano (L1 sobre niveles) entre los latentes de llenado de los ocho agentes. Se reporta el acierto contra la clase verdadera y la distancia al latente más cercano. Predicción: los tres pesos difieren en menos de 2 puntos, sin dirección clara, y la diferencia entre pesos no supera la que hay entre semillas.
    - **B. Datos sin pareja** (`run_homo_sin_pareja.py`). La hetero de cada agente se llena solo con las primeras 50 o 100 imágenes de llenado (25 o 50 %, con sus 16 variantes y el emparejamiento oficial). La homo latente se queda con las 200. En las 652 imágenes de test con energía se compara el reconocimiento con la homo oficial y con la marginal de la hetero reducida: aceptación de la propia clase, aceptaciones de otras clases y clase top-1 por puntaje. También se mide cuántas imágenes reconoce la homo pero la hetero reducida no puede evocar (recuerdo imagen→texto no reconocido). Predicción: la homo acepta más vistas de su clase que la marginal, y también más de otras clases. Esas vistas extra son las que la hetero no puede nombrar.
    - **C. Emparejamiento desigual** (`run_emparejamiento_desigual.py`). La homo de etiquetas se queda como la oficial. Se prueban dos llenados de la hetero sobre los mismos latentes:
      - C1: todas las palabras distintas emparejadas, con frecuencia proporcional a 1/rango;
      - C2: solo la primera mitad de las palabras distintas emparejadas.

      En las 411 consultas se cuenta la contención por pista y agente según la homo y según la marginal, y se cuentan las decisiones distintas del sistema tal como está (ganador temprano y compuerta) con pesos homo contra marginal. También se mide la calidad del recuerdo como en A. Predicción:
      - C1: el soporte de la homo y el de la marginal son iguales, los pesos cambian de forma y el ganador temprano cambia en menos de 3 % de las consultas.
      - C2: la homo contiene pistas que la marginal no, y la compuerta de la hetero las rechaza: la homo sabe la palabra pero el agente no puede recordar una imagen.

    Se reportan conteos sin umbral de éxito.

  - **Resultados (homo como marginal y ¿cuándo agregan algo?), en `results/homo_marginal/`:**
    - Marginal: ninguna decisión distinta de texto ni de imagen. Cambian 66 de 420 recuerdos texto→latente, por la escala de los pesos; cambiar solo la semilla cambia los 420, con un efecto unas 47 veces mayor.
    - A: el acierto del recuerdo es igual con los tres pesos (91.8 %), porque el vecino siempre cae en la clase del agente. Homo y marginal quedan a la misma distancia del llenado. Con pesos, el recuerdo queda 0.03–0.06 niveles más lejos que con uniformes en las dos semillas. «Sin dirección clara» no se cumple, y la diferencia no favorece a los pesos.
    - B: con la hetero reducida a 100 o 50 imágenes, la homo reconoce 10 o 38 vistas más de su clase. Ninguna se puede nombrar. Se cumple.
    - C1: mismo soporte; 8 de 411 ganadores tempranos distintos y ningún ruteo distinto. Se cumple.
    - C2: la homo contiene 322 pares que la hetero rechaza. Se cumple.
    - Lectura: con todo emparejado, las homo son redundantes; agregan algo solo con datos sin pareja.
  - **Criterio declarado antes de correr (D. ¿la hetero guarda lo que llega sin pareja?)** (`run_homo_borde.py`). La hetero reserva un valor indefinido por dominio (`m+1`, `q+1`, «funciones parciales»), con su borde fijado en 1. Leyendo el código, todas sus lecturas (proyección, entropías, medias, relación ι) usan solo `[:m, :q]`. Se repite B: la hetero recibe las primeras 100 o 50 imágenes con su palabra, y el resto de las 200 se registra con la palabra indefinida (NaN). Se compara con la hetero de B, que solo recibe las emparejadas. Predicción:
    - (1) el interior de la relación, la relación ι, las medias y las entropías son iguales a los de B; la proyección desde las 652 imágenes de test es idéntica, y las vistas extra de B siguen sin recuerdo imagen→texto;
    - (2) el borde guarda la misma tabla latente en cada coordenada de palabra, y el borde más la marginal del interior es igual, celda por celda, a la homo latente oficial;
    - (3) el reconocimiento con esa tabla es el de la homo oficial, y con la marginal del interior es el de B.

    Se reportan conteos sin umbral de éxito.
- **30 oct.** D (`results/homo_marginal/borde.json`): se cumplen las tres predicciones. Con 100 o 50 imágenes emparejadas y el resto registrado con la palabra indefinida:
  - el interior, la relación ι, las medias, las entropías y la proyección quedan iguales a B (8 de 8 agentes, 652 de 652 imágenes);
  - las vistas extra siguen sin nombre (10 de 10, 38 de 38);
  - el borde más la marginal es la homo latente oficial, celda por celda, en los 8 agentes, con 0 decisiones de reconocimiento distintas.

  La hetero sí guarda lo sin pareja; solo falta una lectura que use el borde. La primera corrida falló por un error de nombre en `homo_from` y se repitió completa.
