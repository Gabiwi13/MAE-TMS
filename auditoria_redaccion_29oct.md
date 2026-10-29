# Auditoría de la redacción contra los resultados actuales (29 oct 2026)

Cuatro auditorías de solo lectura compararon cada cifra y cada descripción de mecanismo con los resultados del inventario (16 variantes, pesos homo) y con `src/`. Aquí se junta lo que no cubre `revision_pesos_homo_principal_prosa.md`. Lo marcado ✔ lo verifiqué yo contra el archivo; lo demás viene de las auditorías con su fuente.

**Ningún hallazgo pide volver a correr un experimento.** Todos son de redacción: cifras de 4 variantes o de pesos uniformes que quedaron escritas, o descripciones del sistema anteriores a los directorios perspectivales (14 sep).

## 1. Tesis (`.tex8`): cambia el significado

| # | Dónde | Dice | Ahora | Fuente |
|---|---|---|---|---|
| T1 ✔ | `main.tex:74–79` (resumen) | temprana 88.0, madura 93.2, apple 13.0, visual 75.0 % «con cero falsos» | 90.0 / 93.0 / 13.8; visual 96.2 % con 2 falsos | ablación; etapa 7 |
| T2 ✔ | `05:390–418`, `06:139–151`, `07:42–46` (EHAM única, exp11) | la clase empata (97.4 contra 97.5); «no clasifica mejor»; la brecha de fidelidad crece 2.0 → 4.5; precio del directorio 2.5; fuera de dominio M 3/40; dominio ajeno 7–9× | el protocolo gana en clase desde N=50 (98.5 contra 96.8, intervalos separados; en N=25 gana M); brecha 4.6 / 6.1 / 6.1 / 5.7, sin tendencia; precio 1.5 desde N=50 (4.4 en N=25); M acepta 2 / 2 / 5 / 8 de 40; dominio ajeno ≈3×; «bit a bit 8/8» pasa a 4/8 | `experimento11/README.md` |
| T3 ✔ | `03:73–76, 264–279` | «todos los agentes, incluidos los perdedores, registran» | registran el de entrada y el ganador; el TME, todas. El registro en los nueve queda solo en la ablación y en exp2–4 | `stage6_interaction.register_transaction` |
| T4 | `03:310–364, 500–503` | el agente de entrada consulta su directorio y reenvía | `route_transactive`: suma su B1 y el de sus conocidos, encadena si nadie tiene soporte; en texto, doble compuerta; en imagen la entrada es el agente de la clase siguiente | `stage6:282–327`, `stage8:88–96`, `stage7:231` |
| T5 ✔ | `03:313, 360, 441–452`; `04:165–182`; `05:321–329`; `06:177–180, 258–260` | ξ = 2 en el directorio visual, elegido sobre test; rechazo del 25 % («625 de 656») | `XI_VISUAL = 0` desde a423950; rechazo actual 3.5 %. Las limitaciones (b) y (f) parten de un estado que ya no existe | `stage7_bidirectional.py:46` |
| T6 ✔ | `03:169–174`, `04:36–41` | espejo y dos rotaciones (4 variantes) | 16 variantes; la fase A visual también registra las 16 con el mismo ganador | `stage5_fill.py:49` |
| T7 ✔ | `03` y `04` (omisión); `06:202–213` | no mencionan el umbral de energía; τ cierra 94 % «sin cambiar el ruteo», vacas «que el directorio ya rechazaba» | τ = 16.61 rechaza antes de la memoria; cierra 88–90 %; las 4 vacas de test las ruteaba bien el directorio y su contenido las aceptaba: τ cuesta 4 aciertos | `experimento14/resumen.json` |
| T8 | `06:130–131`, `07:26–27` | especificidad del contenido «perfecta», 0 % de falsos | 0 % solo en exp6 (llena sin variantes); con 16 variantes, 5 de 656 (0.8 %), todos entre animales | `experimento13/README.md` |
| T9 | `02:222–227` | la hetero «no genera pesos por característica» (justifica las cinco memorias) | `relation_weights` obtiene pesos marginalizando la relación; los directorios lo usan | `associative_memory.py:60–76` |
| T10 ✔ | `.tex8/figuras/` | fig02, 03, 04, 09, 15, 16 del 13 jul | las regeneradas están en `papers_images/es/` (d0df16c, c0a0d61); hay que copiarlas. El pie de fig16 cita 97.4 % con una imagen vieja | git |

## 2. Tesis: solo cifras o precisión

- `05:78–81` y `06:121–122`: desglose B1 por clase. Dice cow y dog 96, pear 86, horse 82; ahora cow 100, dog 93.9, apple 88.2, horse 88.0, pear 76.0 (pear es la peor).
- `06:73–74`: pear 78 → 76.
- `05:152–153`: el error residual citado, «sweet fruit from an orchard tree» → apple, es un acierto. El error real es «a ripe green pear from the orchard» → apple.
- `05:352–355`: la fuga cerca del origen la aceptan dog, horse y cow, no solo horse; 2 de 12 sólidos de color se aceptan.
- `05:441–447`: tiempos medidos con 4 variantes. El renglón de 293.4 min es pipeline más batería; la batería sola es 159.9.
- `06:22`, `01:83`, `07:34–35`: temprana 85–88 % y «50 → 90 %». La cuantización sola llegó a 88; el 90 incluye las 16 variantes; el 50 % no tiene archivo.
- `06:168–169`: compuerta 21 % en N=25 → 2.05 %.
- `06:171–173`: árbitro 96.1 → 90.6 pasa a 96.8 → 93.6; el margen quita más de un acierto por error.
- `06:248–250`: 74 de 80 objetos sobre 70 % → 71 (quedan 9 abajo).
- `03:431`: conteos TME [50,16,44,…] → [46,16,40,25,30,18,21,31].
- `04:73`: S = 0.1864 → 0.1881.
- `04:137–139`: el rango min–max de la cuantización (`latent_global_stats.json`, 5 jul) es el del llenado de 4 variantes y no se recalculó; las variantes nuevas se recortan a ese rango. Se describe tal cual; recalcularlo pediría re-correr todo.
- `02:78–80`: κ se define con el criterio homo de Pineda; el κ que barre la tesis actúa sobre la proyección hetero.
- `02:275–281`, `03:454–466`: «entropía máxima = deseable» no aplica a los directorios perspectivales (2.22–2.41 bits por construcción); solo el TME llega a 3.0.
- `03:437`: B1 divide entre `_counts`, que está fuera de la relación.
- `03:485`: la evocación busca en los 168 labels de los ocho vocabularios, no en todo fastText.
- **Sin fuente actual:**
  - 98.75 % del reporte de tres agentes (`01:28`);
  - «traducía 0 %» del TME (`01:90`);
  - rescate léxico +23.8 y 41/42 contra 31/42 (`04:92–96`, `06:268`; medido en agosto con 4 variantes);
  - candidatos de pear y tomato (`04:59–60`).

## 3. `results/revision_cientifica/modelo_formal.md` y `discusion_marco_teorico_directorio.md`

- **modelo_formal:38–47:** «proyección con pesos uniformes» → pesos homo de la propia relación. P_k(z) = Σᵢ w'ᵢ(z)·D[i,k,qᵢ(z),1], con w' de media 1; C2.4 (Nadaraya–Watson) sigue valiendo con `weights_from`. Línea 49: R1 del piloto 52.6 → 46.0.
- **discusion (exp8, exp9 y exp10 con los directorios oficiales):**
  - envolvente 2.9–5.5 → 3.0–4.3;
  - el directorio rutea a k 9.7 % en texto (40/411), no 55.7 %;
  - la sustitución responde 0 %;
  - la descripción queda a 19.6 contra 25.1 y su envolvente es **más estrecha**, no más ancha;
  - en imagen→texto la descripción responde 16.7 % contra 100 % del especialista (se invierte);
  - agregado 90.1 contra pizarrón 94.2.

## 4. Documentos de trabajo

- **README.md:**
  - exp11 (líneas 82–101, 132) igual que T2;
  - exp12 (104–106) igual que la sección 7;
  - ablación 93.0 / 85.2 / 93.5 / 13.8, pear 76;
  - registros visuales 2016–2048 propios y 144–368 de cada otro;
  - 9 objetos de 80;
  - falta declarar los pesos homo en todas las lecturas.
- **CONTEXTO_SEP2026.md e INICIO_NUEVA_SESION.md:**
  - dicen que exp8 a exp15 quedan con 4 variantes, pero se re-corrieron el 28 oct;
  - no mencionan los pesos homo ni el inventario;
  - exp11, exp14, exp15, ablación y exp16 con cifras viejas (mismas que arriba);
  - la lista pendiente del deck (CONTEXTO:147, INICIO:132) hay que rehacerla.
- **sintesis_exp7_a_exp16.md:**
  - línea 13: «se pierde la respuesta, no la ubicación» ya no vale con los directorios oficiales (40 de 411; la ubicación también se pierde, salvo con muchas interacciones);
  - línea 19: «en clase empata» y «cuesta cobertura»;
  - línea 25: la fuga no es solo de horse.
- **Veredictos escritos a mano (21–24 sep), viejos:**
  - **exp11:** el criterio 1 ya no se cumple, P3 se ve y aparece la forma fuerte.
  - **exp12:** la primera parte ya no se confirma (falta en la sección 7).
  - **exp13:** los escalones no cuadran con su tabla.
  - **exp14:** τ cuesta 4 aciertos; el directorio rutea 164 de 231 entradas degeneradas (se invierte).
  - **exp15:** 96.8 / 93.6; con Vd=16 el directorio no cuesta cobertura.
  - **exp16:** 71 de 80 objetos.
  - **README de exp8, exp9 y exp10 (escritos a mano, 21 sep):**
    - exp8: los directorios ya no son idénticos y el dos-hot apple+car responde;
    - exp9: imagen→texto por descripción se invierte;
    - exp10: pizarrón 94.2.
  - **exp17 y exp22:** exp17 dice 52.6, ahora 51.7; exp22 dice 93.5, ahora 93.0.
- **Industrial ✔:** la línea de módulos (`piloto_modulos`, `etapa1`, `etapa2`, `replica_ablaciones`, `deriva_olvido`, `olvido_privacidad`) se re-corrió con pesos homo (d0df16c), pero sus README escritos a mano siguen con las cifras anteriores (R1 52.6, «W=300 nunca se recupera»). Las cifras del resumen de CIFIN no salen de ahí. En `revision_cientifica/README.md`: R3 74.3, MedMNIST al peor 31.6, rango de 44 puntos, y la etapa 2 cumple solo con el respaldo por contenido.

## 5. Lo que cambia en la teoría

1. **exp11 pasa a la forma fuerte.** Con 16 variantes y pesos homo, la partición también clasifica mejor desde N=50, y la memoria única acepta más fuera de dominio (P3 se ve). La lectura «partir compra fidelidad, no exactitud» queda corta: compra las dos, salvo con poco contenido.
2. La brecha de fidelidad existe en todos los cortes, pero no crece con el contenido.
3. τ no es gratis: cuesta 4 aciertos de test.
4. Con los directorios perspectivales oficiales, perder un miembro pierde también la ubicación, salvo que haya muchas interacciones (exp9, sección 5 de la propuesta).
