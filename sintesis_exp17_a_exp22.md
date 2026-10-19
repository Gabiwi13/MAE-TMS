# Síntesis: qué se aprendió del sistema entre el experimento 17 y el 22

**Fecha:** 18 de octubre de 2026. Continúa `sintesis_exp7_a_exp16.md`. El código y las cifras de cada experimento están en su carpeta `results/` y su README. Exp17 y exp22 están en esta rama. Exp18 y exp19 están en la copia `MAE-TMS-exp18` (rama `exp18-heteroasociacion-significativa`). El demo médico, exp20 y exp21 están en la copia `MAE-TMS-medico` (rama `medico-demo`). Nada de esto se ha integrado al pipeline oficial ni a la prosa.

## 1. La evocación da el dominio, no la palabra (exp17)

El 97.4 % de evocación imagen → palabras es un acierto de dominio en top-3. En top-1 el dominio se mantiene (96.0 %). El nombre de la clase sale en 48.0 % (apple 0/45, cup 3/45), y recordar la misma imagen tres veces da la misma palabra solo en el 38.9 % de las imágenes. La causa es de construcción: el llenado oficial empareja la imagen *i* con `label_seq[i % L]`, la siguiente palabra de la lista de la clase. La heteroasociación es significativa **a nivel de clase**, no de imagen. Con una palabra arbitraria por objeto, la memoria acierta 40.8 % (azar 10 %) y solo 51.2 % en las vistas que memorizó: los objetos de una clase se pisan en la envolvente.

## 2. La pertenencia generaliza; el atributo no (exp17 C, exp18)

Con palabras que sí describen la imagen (color, manchas, pelo, techo, etiquetadas a mano), la memoria acierta en objetos que vio: color 74 % con lectura normalizada; patrón, pelo y techo 63–72 % balanceado. En objetos nuevos (leave-object-out) **responde el valor más común de su clase**: el valor mayoritario sale en el 98–99 % de los casos y el minoritario en el 1–6 %, sin rechazar. La frase de la síntesis anterior se precisa así: *la envolvente generaliza la pertenencia y falla rechazando; dentro del dominio, el atributo lo decide la densidad y falla confundiendo hacia lo común.*

## 3. Dos cuellos de botella: la percepción y la lectura (exp18, exp19)

- **Percepción.** Con el encoder propio, la sonda de vecinos da azar en manchas, pelo y techo. ResNet18 de ImageNet sin ajustar sí los separa (patrón de cow 91 %, pelo de dog 84 %). No es la pérdida de clase: reentrenado sin ella, el encoder recupera el color de apple pero no las manchas ni el pelo. Lo que borra el detalle es comprimir a 64 dimensiones con reconstrucción.
- **Lectura.** Con rasgos que sí traen el atributo, la memoria generaliza mucho menos que un kNN sobre esos mismos rasgos (cow 59 contra 91). La lectura tolerante (niveles vecinos) baja el rechazo pero casi no transfiere el atributo. La noción de parecido de la MAE es **contención por coordenada, no distancia**. Esto explica exp14 (acepta lo que su envolvente cubre aunque no se parezca a nada visto) y exp18 (no aprovecha lo que se parece si cae fuera de las celdas vistas).
- **Tensión índice ↔ especialista (exp19).** Con el sistema completo sobre el encoder congelado, el ruteo de test baja de 96.2 a 80.5 % y los falsos suben de 2 a 83. En exp16, la cobertura de punta a punta en objeto nuevo baja de 89.2 a 60.8 %, con 14.4 % de falsos, todos entre animales. A cambio, el atributo en objeto nuevo sube solo unos 5 puntos sobre el azar. Una sola percepción no sirve a las dos partes: el índice necesita invariancia dentro de la clase y el especialista, sensibilidad.

## 4. El ancho de la envolvente manda (demo médico)

MedMNIST+ a 128 px, jerarquía modalidad → órgano u hallazgo como dominio.
- **Con registro balanceado** (200 + 128 por agente, o N = máx(328, clase más chica)): modalidad 99.6 % de lo respondido, órganos 97.5 %, melanoma 175/223. Es triaje con abstención.
- **Con todo el train**: los dominios grandes ensanchan su envolvente hasta contener a los chicos (la de tórax contiene el 93 % de las imágenes de piel y el 89 % de las de mama). Melanoma cae a 37/223, todo hallazgo de tórax sale «sin hallazgo» y el fondo de ojo deja de rechazarse (29.7 → 0 %). B1 no lo corrige: no es un sesgo de conteo sino de **ancho**.
- **Radiografía de tórax**: ningún método pasa de ≈ 21 % balanceado con 14 dominios. El límite ahí es la percepción.

## 5. El principio de tamaño corrige el sesgo de ancho (exp20, exp22)

Leer el directorio con el principio de tamaño (Tenenbaum y Griffiths 2001): entre los agentes que contienen la pista gana la envolvente más estrecha (−Σᵢ log|soporte|).
- **Con desbalance** recupera piel (736 → 1785 de 2005), melanoma (37 → 147 de 223) y el balanceado de piel (46.3 → 62.5, igual que balancear el registro).
- **No recupera** mama ni tórax: solo reordena a los agentes que contienen la pista, y la envolvente chica no contiene la imagen. Quedan dos fallas separables: el **sesgo de ancho entre contenedores**, que la lectura corrige, y la **falta de contención de las envolventes chicas**, que pide cobertura.
- **Con registro balanceado equivale a B1**: en el sistema oficial de ETH-80 cambia 1 decisión de 656 en imagen (a favor) y 8 de 411 en texto (3 a favor, 4 en contra). Es candidata a reemplazar a B1.

## 6. El rechazo es de cobertura, no superior (exp20)

A igual aceptación de lo propio, la máxima softmax rechaza el 99.8–100 % de otras modalidades y la memoria el 6–24 %. Con tórax de otro hospital, la memoria rechaza 31.8 % y kNN 75.0 %. Dentro de una modalidad (un órgano nunca registrado), la memoria rechaza el 96.3 %, igual que kNN (97.7) y Mahalanobis (96.6). Un hallazgo nuevo (hernia) no lo detecta nadie. «Falla rechazando» describe la pertenencia, pero no es una ventaja medible sobre los detectores estándar. Es rechazo de cobertura integrado en el mismo mecanismo que rutea.

## 7. Memoria única contra partición a escala (exp21)

Mismo contenido (200 × 16 por agente) en tres brazos: una sola memoria hetero con etiquetas fastText del término de cada dominio (M), especialistas sin directorio y el protocolo con directorios.
- **Con dominios separables, M iguala a la partición** (modalidad 93.4 contra 93.5 balanceado; órganos 90.7 contra 90.8; piel 63.1 contra 63.1). Lo mismo que exp11 en ETH-80.
- **Con 14 hallazgos de tórax muy superpuestos, la partición casi duplica a M** (24.4 contra 13.1 balanceado; azar 7.1). M converge a un atractor: casi todo cae en «pleural thickening». Es exp12 a escala: la ventaja de partir crece con el solapamiento.
- La predicción de que M confundiría más entre términos que comparten palabras (lados izquierdo y derecho) **no se cumplió**: la confusión es la misma en los dos.
- «Varias guardan más que una» se sostiene **cuando los contenidos se pisan**, no como regla general. Lo que la partición compra es no mezclar.
- Los directorios suman sobre los especialistas en mama (88.5 contra 78.8) y no en modalidad ni órganos.

## 8. Qué es el sistema, después de todo esto

- **Lo que tiene:** una memoria semántica distribuida y transactiva, de caja blanca, basada en familiaridad. Reconoce y rutea a nivel de categoría, mantiene separados los dominios mejor que una memoria única (exp11–12), se abstiene por falta de cobertura y explica cada decisión con conteos, soportes y recorridos legibles.
- **Lo que no tiene:** recolección (detalle de la instancia), separación de patrones (lo que evitaría que una envolvente ancha se trague a otra), predicación de atributos y aprendizaje en operación (la mitad dinámica de Wegner).
- **En neurociencia** encaja con la teoría de dos procesos del reconocimiento: hay familiaridad, que es la contención, y no hay recolección. Con los sistemas complementarios, las envolventes son el lado neocortical y falta el hipocampal.
- **En filosofía**, Russell (familiaridad contra descripción) y Putnam (división del trabajo epistémico) se cumplen literalmente; falta la predicación.
