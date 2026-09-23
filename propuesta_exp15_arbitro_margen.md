# Experimento 15: propuesta de diseño para el árbitro por contenido y la abstención por margen

**Fecha:** 23 de septiembre de 2026
**Estado:** propuesta aprobada en el chat; decisiones fijadas aquí antes de correr.

## 1. Qué falta en el sistema estático

Con formación y luego solo lectura, el ruteo maduro tiene dos salidas: el argmax del directorio agregado o el rechazo por soporte cero. La doble compuerta (exp11) cierra el caso «el directorio señala a X y X no contiene la pista». Quedan dos casos abiertos, ambos medidos:

- **El directorio y el contenido se equivocan juntos.** Exp13: una vista frontal de `horse` ruteada a `dog`, y `dog` la contiene. Texto: el par animal y las pistas compartidas (`red`, `fruit`) donde el destino equivocado también reconoce la pista. Nadie compara.
- **No hay noción de «lo sé poco».** Un directorio con 0.31 contra 0.29 rutea igual que uno con 12 contra 0. Exp10 y exp11 sitúan los errores de texto en tokens compartidos, donde los scores están empatados.

## 2. Las dos políticas

Sobre la salida de `route_transactive` (vector agregado `total` de 8 scores calibrados, destino = argmax):

- **Árbitro por contenido (A).** Candidatos: los agentes con `total > 0`, los tres mejores. Cada candidato puntúa la pista con su contenido (`recognize_gated` en texto, máximo sobre las pistas; `recognize_gated_right` en imagen). Destino: el candidato con mayor score de contenido; si ninguno da soporte, rechazo. El directorio sigue decidiendo a quién preguntar; el contenido decide entre los preguntados. Es la doble compuerta generalizada de una a tres opiniones.
- **Abstención por margen (M).** Con $s_1 \geq s_2$ los dos mejores scores del directorio, se abstiene si $(s_1 - s_2)/s_1 < \delta$. Con un solo candidato el margen es 1. **δ = 0.2, pre-registrado**, sin calibrar sobre ningún banco; se reporta además la curva cobertura–error para δ de 0 a 0.5 como material, no como política.
- Combinadas (A+M): margen sobre el directorio y, si pasa, árbitro.
- Diagnóstico, no política: contenido sobre los ocho agentes (lo que haría el contenido solo, sin directorio), como cota.

## 3. Bancos y semillas

- **Texto**: la infraestructura de exp11 en N = 200 (contenido oficial bit a bit): directorios formados con las 240 consultas de formación por semilla, evaluación sobre las 171 reservadas y las 40 fuera de dominio, entrada al azar por consulta como exp11, 10 semillas (42–51).
- **Imagen**: la infraestructura de exp13 con el contenido oficial (Vc = 4): directorios formados con Vd = 1 (oficial) y Vd = 16 (donde aparece el falso de `horse7`), 656 imágenes de test, entrada no especialista, 5 semillas (42–46). El umbral de energía de exp14 se aplica antes (rechaza 4 de 656).

Se guarda por consulta el vector del directorio y el score de contenido de los ocho agentes; las políticas se evalúan sobre esos datos, así que la corrida es una y las políticas se comparan sobre las mismas decisiones.

## 4. Métricas

Por política y semilla: ruteo correcto (sobre todas las consultas), error (ruteo a otra clase), abstención o rechazo, y en fuera de dominio la aceptación falsa. En imagen, además, la cobertura de punta a punta (ruteo correcto y el destino responde). Se reportan aparte las consultas con primera pista compartida (texto) y el caso `horse7-000-000` (imagen).

## 5. Predicciones

- P1. El árbitro corrige la mayoría de los errores de ruteo en texto donde el destino correcto está entre los tres candidatos del directorio, sin bajar la cobertura (no rechaza nada que el argmax aceptara y el destino contuviera).
- P2. El árbitro no corrige `horse7 → dog` si `horse` no tiene soporte en el directorio para esa imagen: el error está antes de la comparación. Si `horse` está entre los candidatos, lo corrige.
- P3. El margen δ = 0.2 quita más errores que aciertos en texto (los errores viven en empates) y casi nada en imagen (con ξ = 0 casi siempre hay un solo candidato).
- P4. En fuera de dominio el árbitro iguala a la doble compuerta (2 de 40); el margen no añade falsos.

## 6. Criterio

La política A+M queda **confirmada** si, frente al argmax, reduce el error de ruteo de texto al menos a la mitad con una pérdida de cobertura menor que el error que quita, y no aumenta los falsos fuera de dominio ni los falsos ruteos de imagen. Queda **refutada** si el árbitro cambia más aciertos en errores que errores en aciertos, o si el margen cuesta más aciertos que errores quita.

## 7. Entregables

`run_experiment15_arbiter.py` (una corrida, minutos; `--report-only`), `results/experimento15/{README.md, resumen.json, raw/, fig1_curva_margen.png, veredicto.md}`.
