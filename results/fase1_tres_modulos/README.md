# Fase 1: prototipo de tres módulos (archivo histórico)

Copia de `results/` de la rama `v3-experimento1` (punta `c6f0f3d`, 29 jun 2026). Las cifras de formación del directorio salen de los commits `0ff1619` y `54f30ca` (22 jun 2026). No se recalculó nada. Se quitó solo `exp3_corrected_routing/exp3_mdir_state.pkl` (3.3 MB, estado binario del directorio).

## Arquitectura de esta fase
Es distinta de la del sistema final:
- tres módulos (apple, horse, car);
- cuatro memorias por módulo;
- cuantización por signo;
- TME mediador en la fase temprana;
- directorio compartido;
- banco de 80 consultas.

Con el código actual de `una-hetero`, que fija ocho clases, no se reproduce, y los pesos del codificador de tres clases no se guardaron. Por eso estas cifras se reportan como resultados de su fase, no como comparación controlada con el sistema de ocho módulos.

## Estado de cada carpeta
- `exp4_directory_formation`: formación del directorio. Vigente. Se evalúa dentro de muestra (las mismas 80 consultas que forman el directorio) y necesita la lectura B1.
- `exp3_corrected_routing`: lectura B1 de la fase madura. Vigente.
- `exp2_iota_kappa`: la conclusión «κ inerte» de una versión anterior era un error de programación, corregido en `29f401c`. La versión copiada aquí es la corregida.
- `rejection_probe`: sonda de rechazo de tres clases. Quedó obsoleta.
- `experimento1`: informe del primer prototipo. Sus cifras de tres clases las reemplaza `exp3_corrected_routing`.
- `exp5_entropic_prototype`: corrida del 12 jun con 50 instancias, no con 200.
- `ablation_mdir_bias`, `exp6_capacity`, `label_recall` y `computational_cost`: corridas de tres clases de la misma rama.
