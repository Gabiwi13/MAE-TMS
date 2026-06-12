# Experimento 1 — Caracterización del sistema MAE-TMS

Base de código v3: llenado por instancias (λ acumula la distribución real,
N=200 imágenes por clase), scoring oficial `Agent.recognize_gated`
(activación media gateada por containment — única definición, usada por
todas las secciones), directorios hetero-asociativos (DirectoryMemory),
rechazo explícito, vocabulario normalizado por lemas. Banco de evaluación:
80 consultas con ground truth (27/27/26). Parámetros EAM: ι=0, κ=0, ξ=0,
σ=0.1. La calibración ÷mem.mean quedó fuera del scoring final: la sección B
demuestra que con masas igualadas por el llenado es redundante.

## Sección A — Protocolo completo (temprana → directorio → madura)

| métrica | valor |
|---|---|
| accuracy temprana | 96.2 % (rechazo 2.5 %) |
| accuracy madura, lectura B1 | 97.5 % |
| accuracy madura, lectura cruda | 83.8 % |
| fidelidad temprana↔madura | 96.2 % |
| counts del directorio (TME) | [68, 54, 42] · entropía 1.558 / 1.585 bits |
| réplica 10 TEST_QUERIES | counts [5, 4, 4] · 1 rechazo honesto |

La lectura B1 del directorio sigue siendo necesaria: los counts difieren
porque las consultas rutean de forma desigual, y el score crudo de la HAM
crece con esa masa (97.5 % vs 83.8 %).

Artefactos: `results/exp3_corrected_routing/`

## Sección B — Parámetros nativos ι × κ

| condición | banco | diagnóstico 11 cues |
|---|---|---|
| ι=0, κ=0 (gate solo) | **96.2 %** | **100 %** |
| ι=0, κ=0 + ÷mem.mean | 96.2 % | 90.9 % |
| ι=0.25 | 77.5 % (rechazo 21 %) | 63.6 % |
| ι=0.5 | 53.8 % (rechazo 45 %) | 36.4 % |
| ι=1.0 | 0 % (rechazo 100 %) | 0 % |
| κ ∈ {0.5, 1.0, 1.5} | sin efecto en ninguna fila | — |

Hallazgo central: **con el llenado por instancias, el sesgo de densidad del
dominio desaparece** — las masas quedan igualadas por construcción (200 por
clase) y el gate de containment basta para discriminar (100 % en el
diagnóstico que con el llenado-promedio daba 64 %). La calibración ÷mem.mean,
indispensable sobre la base defectuosa, es redundante sobre la correcta.
ι sigue siendo destructiva con cues binarios (poda conocimiento ralo antes
que promiscuidad) y κ inerte como umbral en este rango.

Artefactos: `results/exp2_iota_kappa/`

## Sección C — Formación del directorio

| orden de las experiencias | transición ≥90 % (k) | acc final |
|---|---|---|
| intercalado | **14** | 97.5 % |
| barajado (5 semillas) | 18–34 (media ~26) | 97.5 % |
| bloqueado por dominio | 57 | 97.5 % |
| control: scoring crudo | 48 (sostenido 67) | 93.8 % |

El grupo "se conoce" en ~14–26 interacciones bien mezcladas. Con
experiencias segregadas por tema, la transición espera al último bloque:
el directorio no rutea expertise que no presenció. Todos los órdenes
convergen al mismo estado final ([68, 54, 42]) — el orden afecta velocidad,
no destino. El control crudo converge más tarde y deja un directorio
estructuralmente distinto ([73, 57, 34]).

Artefactos: `results/exp4_directory_formation/` (fig1 = curva central)

## Sección D — Capacidad de llenado

| N imágenes | test propio | falsos (otras clases) | routing labels | variedad recall (L1) |
|---|---|---|---|---|
| 25 | 0 % | 0 % | 60.0 %* | 0.00* |
| 50 | 0 % | 0 % | 91.2 % | 2.21 |
| 100 | 11.7 % | 0 % | 97.5 % | 2.70 |
| **200** | **56.7 %** | **0 %** | **96.2 %** | 2.84 |
| 328 | 78.3 % | 0 % | 81.2 % | 3.07 |

(*) en N<92 la secuencia de labels no alcanza a cubrirse: artefacto de
cobertura, no de capacidad.

La generalización a imágenes nuevas crece con la cobertura (sin necesidad
de ξ>0) mientras la especificidad permanece perfecta en todo el rango. El
costo de la saturación aparece en el routing por labels (96.2 → 81.2 % al
llenar todo): con más latentes por label, las relaciones cubren más del
eje contrario y el gate pierde filo. Zona de operación elegida: N=200.

Artefactos: `results/exp6_capacity/`

## Sección E — Hemisferio visual (imagen → agente → labels)

| métrica | valor |
|---|---|
| interacciones visuales (fase A) | 384 imágenes · routing 100 % sobre aceptadas · rechazo 49.7 % |
| directorio visual (mem_dir_R) | counts [91, 71, 31] · entropía 1.466 bits |
| routing de test por mem_dir_R (B1) | precisión 100 % sobre aceptadas · cobertura 32.9 % |
| evocación de labels (top-3 domain hit) | **94.1 %** |

El directorio visual nunca se equivoca pero su cobertura está limitada por
ξ=0 (acepta solo lo contenido exactamente). La evocación inversa —imagen →
labels vía recall modulado por los pesos de M_dom_R— funciona al 94 %.

Artefactos: `rerun_refactor.log` (stage 7)

## Síntesis

1. El sistema completo —texto→imagen e imagen→texto— opera exclusivamente
   sobre memorias asociativas, con rechazo explícito en ambas direcciones.
2. El llenado fiel a la teoría (λ acumula instancias) elimina de raíz el
   sesgo de densidad del dominio; la única calibración que permanece
   necesaria es B1 en la lectura del directorio, porque la especialización
   genuina produce masas desiguales.
3. La formación del directorio es rápida (k≈14–26), robusta al orden en su
   destino, y sensible al orden en su velocidad.
4. La capacidad tiene un equilibrio medible entre generalización visual y
   discriminación verbal; N=200 es el punto de operación.
5. Límites activos: cobertura visual (ξ=0) y margen semántico binario
   (sign en la extracción de fastText) — ambos con mitigación diseñada.
