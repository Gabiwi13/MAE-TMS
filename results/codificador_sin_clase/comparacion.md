| medida | oficial (MSE + 0.1·CE) | sin pérdida de clase |
|---|---|---|
| τ (umbral de energía) | 16.61 | 13.79 |
| fase A, acierto al formar directorios | 99.9 % | 81.0 % |
| fase A, rechazo / sin energía | 0.8 % / 1 | 0.9 % / 0 |
| entropía de los directorios visuales (bits) | 2.22–2.41 | 2.00–2.51 |
| ruteo de test (656) | 631/656 = 96.2 % | 462/656 = 70.4 % |
| falsos ruteos de test | 2 (0.3 %) | 169 (25.8 %) |
| rechazo de test (de ellas sin energía) | 23 = 3.5 % (4) | 25 = 3.8 % (0) |
| evocación top-3, log de la etapa 7 | 113/116 | 84/113 |
| evocación top-3, semilla 0 (eval_fase_b.py) | 113/116 = 97.4 % | 87/113 = 77.0 % |
| evocación, semilla 0, según el ruteo | 113/116 bien ruteadas · 0/0 mal ruteadas | 80/81 bien ruteadas · 7/32 mal ruteadas |
| etapa 6, ganadores iguales al oficial | 16/16 | 16/16 |
| etapa 8, fidelidad | 16/16 | 16/16 |
| exp16, objeto conocido, punta a punta | 95.5 [95.1, 95.9] | 69.9 [68.0, 71.6] |
| exp16, objeto conocido, directorio acepta | 98.0 [97.3, 98.6] | 97.3 [96.7, 97.8] |
| exp16, objeto conocido, contenido acepta | 99.1 [98.9, 99.4] | 97.4 [96.7, 98.1] |
| exp16, objeto conocido, falso ruteo | 0.1 [0.0, 0.2] | 23.6 [21.8, 25.5] |
| exp16, objeto conocido, falsos (de 3280) | 3 | 773 |
| exp16, objeto nuevo, punta a punta | 89.2 [85.1, 93.2] | 59.3 [55.5, 62.9] |
| exp16, objeto nuevo, directorio acepta | 92.2 [88.6, 95.4] | 95.5 [94.2, 96.6] |
| exp16, objeto nuevo, contenido acepta | 95.2 [92.1, 97.7] | 92.9 [90.9, 94.8] |
| exp16, objeto nuevo, falso ruteo | 0.1 [0.0, 0.2] | 30.2 [27.4, 33.2] |
| exp16, objeto nuevo, falsos (de 3280) | 2 | 992 |
| exp16, brecha e2e conocido − nuevo (puntos) | 6.3 [2.5, 10.4] | 10.6 [6.8, 14.8] |

Falsos de test, sin clase: {'horse → dog': 34, 'cow → dog': 31, 'horse → cow': 15, 'car → dog': 11, 'tomato → apple': 9, 'apple → tomato': 8, 'car → cow': 8, 'cow → car': 8, 'cup → cow': 7, 'pear → cow': 6, 'apple → cup': 5, 'dog → cow': 5, 'cow → horse': 4, 'car → horse': 2, 'dog → cup': 2, 'dog → horse': 2, 'pear → cup': 2, 'car → cup': 1, 'cup → car': 1, 'cup → dog': 1, 'dog → car': 1, 'dog → pear': 1, 'dog → apple': 1, 'horse → apple': 1, 'horse → car': 1, 'pear → horse': 1, 'tomato → cup': 1}
Falsos de test, oficial: {'horse → dog': 2}
exp16 falsos en objeto nuevo, sin clase: {'horse → dog': 161, 'cow → dog': 114, 'dog → horse': 93, 'horse → cow': 76, 'cow → horse': 64, 'dog → cow': 56, 'car → dog': 51, 'apple → tomato': 45, 'cow → car': 39, 'cup → cow': 32, 'tomato → apple': 29, 'apple → cup': 23, 'car → cow': 22, 'cup → horse': 21, 'horse → car': 20, 'dog → car': 17, 'car → horse': 15, 'horse → cup': 15, 'dog → cup': 14, 'pear → dog': 12, 'cup → dog': 11, 'pear → cup': 9, 'tomato → cup': 9, 'car → cup': 6, 'pear → cow': 5, 'cow → cup': 5, 'cup → apple': 5, 'horse → pear': 4, 'car → pear': 4, 'pear → horse': 3, 'cup → tomato': 3, 'apple → pear': 3, 'horse → apple': 2, 'apple → horse': 2, 'car → apple': 1, 'dog → pear': 1}
Ruteo de test por clase (ok/rechazo de 82), oficial -> sin clase:
  apple: 81/1 -> 66/3
  car: 76/6 -> 53/7
  cow: 77/5 -> 38/1
  cup: 80/2 -> 69/4
  dog: 79/3 -> 67/3
  horse: 79/1 -> 31/0
  pear: 78/4 -> 71/2
  tomato: 81/1 -> 67/5
Etapa 6, ganadores: [('apple', 'apple'), ('car', 'car'), ('cow', 'cow'), ('cup', 'cup'), ('dog', 'dog'), ('horse', 'horse'), ('apple', 'apple'), ('tomato', 'tomato'), ('apple', 'apple'), ('car', 'car'), ('cow', 'cow'), ('cup', 'cup'), ('dog', 'dog'), ('horse', 'horse'), ('pear', 'pear'), ('tomato', 'tomato')]
