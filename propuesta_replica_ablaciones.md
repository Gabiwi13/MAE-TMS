# Réplica y ablaciones de la línea de módulos (diseño congelado)

**Fecha:** 19 de octubre de 2026
**Estado:** fijada antes de correr. El diseño evaluado es el que cumplió el criterio en la etapa 2 (entrada por receptor y R3 con ξ = 1), **congelado**: no se cambia ningún detalle al ver resultados. Las predicciones salen de [`results/revision_cientifica/modelo_formal.md`](results/revision_cientifica/modelo_formal.md).

## 1. Preguntas

1. **Réplica.** ¿El resultado de la etapa 2 (aprender qué módulo lo hace mejor y quedar cerca del router central) se sostiene con 10 semillas? ¿Y en una flota que no se usó para diseñar?
2. **Ablación.** ¿Qué componente carga el resultado: la memoria de directorio, o simplemente contar éxitos por módulo con la entrada en el dominio correcto?

## 2. Flotas

- **VisA** (la del diseño): 12 piezas × 2 redes especializadas (la base y la variante más débil según la mitad de aprendizaje). Pistas con 16 variantes. Desconocidas: las 756 imágenes médicas del piloto.
- **MedMNIST** (nueva, nunca usada para diseñar): 4 modalidades (tórax, órganos, piel y mama) × 3 módulos reales del demo médico balanceado: la **cabeza** entrenada, **kNN** y la **memoria** (el especialista de nivel 2; su rechazo cuenta como error). Ruteo con los latentes del nivel 1 médico (ResNet18 + PCA del demo); el contenido de cada módulo es el llenado de su modalidad (328 × 16). Consultas: hasta 600 imágenes de test por modalidad (mama: las 156). Pistas sin variantes (el demo no guardó variantes del test). Desconocidas: las 400 imágenes de test de retinamnist, codificadas con el mismo encoder de nivel 1.

## 3. Protocolo (idéntico al de la etapa 2)

Por semilla s ∈ {0, …, 9}: reparto aprendizaje/evaluación 50/50 por dominio, corriente de aprendizaje en orden aleatorio, entrada por receptor (un módulo cuyo contenido contiene la pista, al azar entre ellos), exploración al azar entre los candidatos y registro de intentos y éxitos en los directorios de entrada y ganador. La evaluación usa los directorios congelados. Cada semilla cambia el reparto, el orden, las entradas y la exploración.

## 4. Lecturas comparadas (todas con la misma entrada en cada consulta)

| lectura | qué usa |
|---|---|
| **R3** (el diseño congelado) | directorio de la MAE: el propio y luego los conocidos en orden de conteos, ξ = 1, cociente éxitos/intentos de proyecciones; respaldo por contenido |
| **TAB** (ablación 1) | el mismo recorrido, pero la evidencia es una **tabla de conteos** de éxitos e intentos por (directorio, módulo): sin núcleo y sin filtro de soporte |
| **PROPIO** (ablación 2) | R3 leyendo solo el directorio propio, sin conocidos; luego el respaldo por contenido |
| **GLOBAL** (ablación 3) | entre los candidatos por contenido, la mejor tasa global de éxitos/intentos de toda la flota (un contador central por módulo) |
| router central kNN | el del piloto (10 vecinos con tasa de éxito, abstención por distancia) |
| azar entre candidatos | cota baja |
| mejor módulo fijo | por dominio, el módulo con mayor acierto en evaluación (techo sin ruteo) |

## 5. Medidas

Por semilla:
- acierto en conocidas, abstención en conocidas y en desconocidas, y costo (lecturas + 24 si hubo respaldo por contenido);
- **pérdida frente al mejor módulo fijo** (en puntos);
- en VisA, **fracción al mejor** en dominios con diferencia de ≥ 5 puntos (como en el piloto);
- en MedMNIST, **fracción al peor** en dominios donde el peor está ≥ 5 puntos bajo el mejor (tórax y piel).

Se reporta la media sobre semillas con un intervalo de confianza del 95 % por bootstrap sobre las 10 semillas.

## 6. Predicciones (del modelo formal)

- **PF1.** TAB rinde igual que R3: diferencia en «al mejor» y en acierto dentro del intervalo de confianza.
- **PF2.** GLOBAL rinde igual o mejor que R3 en «al mejor».
- **PF3.** PROPIO rinde igual que R3.
- **PF4.** El núcleo de la memoria solo aportaría si la calidad relativa de los módulos cambia dentro del dominio. Se mide, por dominio, el acierto de cada módulo en normales y en fallas (VisA) y por clase (MedMNIST), y se cuenta en cuántos dominios se invierte el orden.
- **PF5.** En MedMNIST, R3 aprende a evitar al peor módulo (fracción al peor < 1/3, que es el azar entre 3), y TAB y GLOBAL hacen lo mismo.
- **Réplica:** R3 en VisA mantiene ≥ 70 % al mejor en la media de semillas, y el acierto queda a ≤ 3 puntos del router central.

## 7. Criterios

- **«La memoria de directorio aporta como mecanismo de decisión»:** sostenido si R3 supera a TAB en «al mejor» (VisA) o en pérdida frente al mejor fijo (ambas flotas) por ≥ 5 puntos, con un intervalo del 95 % que excluya el 0. Si no, la decisión se atribuye a contar éxitos, y la memoria aporta el reconocimiento de dominio (receptor y abstención), el olvido exacto y la agregación auditable.
- **«El resultado de la etapa 2 se replica»:** sostenido si en VisA la media de R3 da ≥ 70 % al mejor, con el límite inferior del intervalo ≥ 60 %, y su acierto queda a ≤ 3 puntos del router central; y si en MedMNIST, R3 queda a ≤ 3 puntos del central y con fracción al peor < 1/3.

## 8. Entregables

`run_replica_ablaciones.py` y `results/replica_ablaciones/{README.md, resumen.txt, resultados.json}`. Después, el registro de afirmaciones en `results/revision_cientifica/README.md`.
