# Experimento 11 — desglose por clase

Clase 1-NN (%), d a la instancia real más cercana y compat máximo, por clase y brazo; solo respuestas. Semillas y sorteos agregados.

## N = 25

| clase | M: clase / d_nn / compat | T-oraculo: clase / d_nn / compat | T-protocolo: clase / d_nn / compat | n M |
|---|---|---|---|---|
| apple | 93.5 / 30.4 / 0.95 | 100.0 / 21.8 / 1.00 | 99.5 / 21.8 / 1.00 | 660 |
| car | 100.0 / 22.1 / 0.99 | 100.0 / 20.4 / 1.00 | 95.2 / 21.3 / 1.00 | 630 |
| cow | 100.0 / 19.2 / 1.00 | 100.0 / 16.3 / 1.00 | 100.0 / 16.3 / 1.00 | 630 |
| cup | 100.0 / 20.9 / 1.00 | 100.0 / 18.4 / 1.00 | 100.0 / 18.4 / 1.00 | 630 |
| dog | 100.0 / 25.4 / 1.00 | 100.0 / 21.3 / 1.00 | 100.0 / 21.2 / 1.00 | 570 |
| horse | 95.2 / 18.0 / 1.00 | 100.0 / 15.0 / 1.00 | 100.0 / 14.8 / 1.00 | 630 |
| pear | 100.0 / 22.1 / 1.00 | 100.0 / 16.9 / 1.00 | 82.6 / 21.3 / 1.00 | 690 |
| tomato | 92.8 / 24.5 / 0.94 | 100.0 / 16.0 / 1.00 | 99.1 / 16.3 / 1.00 | 690 |

Errores de clase de M más frecuentes (verdadera → vecino real):

- tomato → apple: 50
- horse → cow: 30
- apple → tomato: 16
- apple → pear: 15
- apple → dog: 10
- apple → car: 2

## N = 50

| clase | M: clase / d_nn / compat | T-oraculo: clase / d_nn / compat | T-protocolo: clase / d_nn / compat | n M |
|---|---|---|---|---|
| apple | 93.9 / 33.8 / 0.95 | 100.0 / 23.2 / 1.00 | 99.1 / 23.2 / 1.00 | 660 |
| car | 99.4 / 26.8 / 0.98 | 100.0 / 22.0 / 1.00 | 95.2 / 22.9 / 1.00 | 630 |
| cow | 100.0 / 22.7 / 1.00 | 100.0 / 18.2 / 1.00 | 100.0 / 18.1 / 1.00 | 630 |
| cup | 100.0 / 26.0 / 1.00 | 100.0 / 21.6 / 1.00 | 100.0 / 21.3 / 1.00 | 630 |
| dog | 100.0 / 30.0 / 1.00 | 100.0 / 23.3 / 1.00 | 100.0 / 23.2 / 1.00 | 570 |
| horse | 95.2 / 21.6 / 1.00 | 100.0 / 19.6 / 1.00 | 100.0 / 19.6 / 1.00 | 630 |
| pear | 100.0 / 24.5 / 1.00 | 100.0 / 18.4 / 1.00 | 96.5 / 19.7 / 1.00 | 690 |
| tomato | 92.2 / 27.2 / 0.93 | 100.0 / 17.4 / 1.00 | 99.6 / 17.6 / 1.00 | 690 |

Errores de clase de M más frecuentes (verdadera → vecino real):

- tomato → apple: 53
- horse → cow: 30
- apple → tomato: 23
- apple → pear: 9
- apple → dog: 7
- car → horse: 3
- car → dog: 1
- apple → cow: 1

## N = 100

| clase | M: clase / d_nn / compat | T-oraculo: clase / d_nn / compat | T-protocolo: clase / d_nn / compat | n M |
|---|---|---|---|---|
| apple | 95.0 / 35.3 / 0.95 | 100.0 / 25.6 / 1.00 | 99.5 / 25.8 / 1.00 | 660 |
| car | 98.7 / 31.2 / 0.98 | 100.0 / 25.2 / 1.00 | 95.2 / 26.1 / 1.00 | 630 |
| cow | 100.0 / 23.8 / 1.00 | 100.0 / 19.9 / 1.00 | 100.0 / 19.8 / 1.00 | 630 |
| cup | 100.0 / 28.6 / 1.00 | 100.0 / 23.9 / 1.00 | 100.0 / 24.3 / 1.00 | 630 |
| dog | 100.0 / 30.3 / 1.00 | 100.0 / 23.8 / 1.00 | 100.0 / 23.7 / 1.00 | 570 |
| horse | 95.2 / 25.2 / 1.00 | 100.0 / 25.4 / 1.00 | 100.0 / 25.8 / 1.00 | 630 |
| pear | 100.0 / 29.3 / 1.00 | 100.0 / 21.4 / 1.00 | 96.1 / 22.9 / 1.00 | 690 |
| tomato | 92.3 / 31.1 / 0.89 | 100.0 / 21.9 / 1.00 | 99.6 / 21.9 / 1.00 | 690 |

Errores de clase de M más frecuentes (verdadera → vecino real):

- tomato → apple: 50
- horse → cow: 30
- apple → pear: 14
- apple → tomato: 12
- apple → dog: 5
- car → dog: 3
- tomato → dog: 2
- car → apple: 1

## N = 200

| clase | M: clase / d_nn / compat | T-oraculo: clase / d_nn / compat | T-protocolo: clase / d_nn / compat | n M |
|---|---|---|---|---|
| apple | 94.5 / 38.7 / 0.95 | 100.0 / 29.1 / 1.00 | 97.7 / 28.7 / 1.00 | 660 |
| car | 98.9 / 32.0 / 0.98 | 100.0 / 31.0 / 1.00 | 95.2 / 31.9 / 1.00 | 630 |
| cow | 100.0 / 28.6 / 1.00 | 100.0 / 21.8 / 1.00 | 100.0 / 21.8 / 1.00 | 630 |
| cup | 100.0 / 33.3 / 1.00 | 100.0 / 27.4 / 1.00 | 100.0 / 27.3 / 1.00 | 630 |
| dog | 100.0 / 33.6 / 1.00 | 100.0 / 29.6 / 1.00 | 100.0 / 28.8 / 1.00 | 570 |
| horse | 94.9 / 27.1 / 1.00 | 100.0 / 27.1 / 1.00 | 100.0 / 27.0 / 1.00 | 630 |
| pear | 100.0 / 32.7 / 1.00 | 100.0 / 23.9 / 1.00 | 94.8 / 25.2 / 1.00 | 690 |
| tomato | 88.0 / 33.8 / 0.90 | 100.0 / 25.1 / 1.00 | 99.1 / 25.2 / 1.00 | 690 |

Errores de clase de M más frecuentes (verdadera → vecino real):

- tomato → apple: 46
- tomato → pear: 34
- horse → cow: 30
- apple → tomato: 16
- apple → dog: 8
- apple → pear: 7
- car → pear: 5
- tomato → dog: 3
