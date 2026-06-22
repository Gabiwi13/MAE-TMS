# Experimento 1 — Caracterización del sistema EAM-TMS

Base de código v3: llenado por instancias (λ acumula la distribución real,
N=200 imágenes por clase), scoring oficial `Agent.recognize_gated`
(activación media gateada por containment — única definición, usada por
todas las secciones), directorios hetero-asociativos (DirectoryMemory),
rechazo por la propia memoria, vocabulario normalizado por lemas. **No hay
filtro léxico**: cada token con vector fastText real entra como pista y la EAM
decide soporte/rechazo; `token_in_vocabulary` quedó solo como diagnóstico.
Banco de evaluación: 80 consultas con ground truth (27/27/26). Parámetros EAM:
ι=0, κ=0, ξ=0, σ=0.1. La calibración ÷mem.mean quedó fuera del scoring final:
la sección B demuestra que con masas igualadas por el llenado es redundante.
Fuente canónica de métricas: `results/exp3_corrected_routing/summary.json`.

## Sección A — Protocolo completo (temprana → directorio → madura)

| métrica | valor |
|---|---|
| accuracy temprana | 97.5 % (rechazo 1.25 %) |
| accuracy madura, lectura B1 | 98.75 % |
| accuracy madura, lectura cruda | 53.75 % |
| fidelidad temprana↔madura | 97.5 % |
| counts del directorio (TME) | [78, 65, 53] · entropía 1.567 bits |
| desglose de rechazo | 79 ruteadas · 0 rechazo-EAM · 1 frontera-encoder |
| réplica 10 TEST_QUERIES | counts [6, 7, 6] · 1 rechazo honesto |

El único rechazo del banco principal ocurre **antes** de la EAM —una consulta
sin token representable (frontera del encoder)— y no por falta de soporte en
la memoria; la demostración del rechazo-por-EAM real está en
`results/rejection_probe/`. La lectura B1 del directorio sigue siendo
necesaria: al admitir todos los tokens representables se registran más cues,
el score crudo crece con esa masa desigual y la lectura cruda cae a 53.75 %,
que B1 corrige a 98.75 %. La caída del crudo respecto a versiones previas no
es regresión: refleja que ahora entran más pistas y el sesgo de masa queda
más expuesto, lo que hace a B1 la única corrección irreducible.

Artefactos: `results/exp3_corrected_routing/`

## Sección B — Parámetros nativos ι × κ

| condición | banco | diagnóstico 11 cues |
|---|---|---|
| ι=0, κ=0 (gate solo) | **97.5 %** | **100 %** |
| ι=0, κ=0 + ÷mem.mean | 97.5 % | 90.9 % |
| ι=0.25 | 77.5 % (rechazo 21 %) | 63.6 % |
| ι=0.5 | 53.8 % (rechazo 45 %) | 36.4 % |
| ι=1.0 | 0 % (rechazo 100 %) | 0 % |
| κ ∈ {0.5, 1.0, 1.5} | sin efecto en ninguna fila | — |

Hallazgo central: **con el llenado por instancias, el sesgo de densidad del
dominio desaparece** — las masas quedan igualadas por construcción (200 por
clase) y el gate de containment basta para discriminar (100 % en el
diagnóstico). La calibración ÷mem.mean, indispensable sobre la base
defectuosa, es redundante sobre la correcta. ι sigue siendo destructiva con
cues binarios (poda conocimiento ralo antes que promiscuidad) y κ inerte como
umbral en este rango.

Artefactos: `results/exp2_iota_kappa/`

## Sección C — Formación del directorio

| orden de las experiencias | transición ≥90 % (k) | acc final |
|---|---|---|
| intercalado | **13** | 98.75 % |
| barajado (5 semillas) | 15–24 (sostenido hasta 44) | 98.75 % |
| bloqueado por dominio | 67 | 98.75 % |
| control: scoring crudo | primer 14 (sostenido 66) | 93.8 % |

El grupo "se conoce" en ~13–24 interacciones bien mezcladas. Con experiencias
segregadas por tema, la transición espera al último bloque: el directorio no
rutea expertise que no presenció. Todos los órdenes convergen al mismo estado
final ([78, 65, 53], entropía 1.567) — el orden afecta velocidad, no destino.
El control crudo converge más tarde y deja un directorio estructuralmente
distinto ([84, 67, 45]).

Artefactos: `results/exp4_directory_formation/` (fig1 = curva central)

## Sección D — Capacidad de llenado

| N imágenes | test propio | falsos (otras clases) | routing labels | variedad recall (L1) |
|---|---|---|---|---|
| 25 | 0 % | 0 % | 60.0 %* | 0.00* |
| 50 | 0 % | 0 % | 93.8 % | 2.25 |
| 100 | 11.7 % | 0 % | 98.8 % | 2.53 |
| **200** | **56.7 %** | **0 %** | **97.5 %** | 2.75 |
| 328 | 78.3 % | 0 % | 85.0 % | 3.09 |

(*) en N<92 la secuencia de labels no alcanza a cubrirse: artefacto de
cobertura, no de capacidad.

La generalización a imágenes nuevas crece con la cobertura (sin necesidad de
ξ>0) mientras la especificidad permanece perfecta en todo el rango (falsos
0 % siempre). El costo de la saturación aparece en el routing por labels
(97.5 → 85.0 % al llenar todo): con más latentes por label, las relaciones
cubren más del eje contrario y el gate pierde filo. Zona de operación elegida:
N=200.

Artefactos: `results/exp6_capacity/`

## Sección E — Hemisferio visual (imagen → agente → labels)

| métrica | valor |
|---|---|
| interacciones visuales (fase A) | 384 imágenes · routing 100 % sobre aceptadas · rechazo 49.7 % |
| directorio visual (mem_dir_R) | counts [91, 71, 31] · entropía 1.466 bits |
| routing de test por mem_dir_R (B1) | precisión 100 % sobre aceptadas · cobertura 32.9 % |
| evocación de labels (top-3 domain hit) | **94.1 %** |

El hemisferio visual opera sobre latentes de imágenes reales (no se vio
afectado por el cambio de representación de texto). El directorio visual nunca
se equivoca pero su cobertura está limitada por ξ=0 (acepta solo lo contenido
exactamente). La evocación inversa —imagen → labels vía recall modulado por
los pesos de M_dom_R— funciona al 94 %.

Artefactos: `rerun_refactor.log` (stage 7)

## Síntesis

1. El sistema completo —texto→imagen e imagen→texto— opera exclusivamente
   sobre memorias asociativas. El rechazo lo decide la EAM (recognize_gated →
   score 0) o la frontera del encoder (sin vector fastText), nunca un filtro
   léxico externo ni una clase `unknown` explícita.
2. El llenado fiel a la teoría (λ acumula instancias) elimina de raíz el sesgo
   de densidad del dominio; la única calibración que permanece necesaria es B1
   en la lectura del directorio (98.75 % vs 53.75 % crudo), porque la
   especialización genuina produce masas desiguales.
3. La formación del directorio es rápida (k≈13–24), robusta al orden en su
   destino, y sensible al orden en su velocidad.
4. La capacidad tiene un equilibrio medible entre generalización visual y
   discriminación verbal; N=200 es el punto de operación.
5. Límites activos: cobertura visual (ξ=0) y margen semántico binario
   (sign en la extracción de fastText) — ambos con mitigación diseñada.
