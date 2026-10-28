# Experimento 11 — desglose por clase

Clase 1-NN (%), d a la instancia real más cercana y compat máximo, por clase y brazo; solo respuestas. Semillas y sorteos agregados.

## N = 25

| clase | M: clase / d_nn / compat | T-oraculo: clase / d_nn / compat | T-protocolo: clase / d_nn / compat | n M |
|---|---|---|---|---|
| apple | 94.5 / 30.3 / 0.96 | 100.0 / 21.9 / 1.00 | 100.0 / 22.0 / 1.00 | 660 |
| car | 100.0 / 22.1 / 0.99 | 100.0 / 20.3 / 1.00 | 95.2 / 21.2 / 1.00 | 630 |
| cow | 100.0 / 19.2 / 1.00 | 100.0 / 16.3 / 1.00 | 94.8 / 17.7 / 1.00 | 630 |
| cup | 100.0 / 20.7 / 1.00 | 100.0 / 18.3 / 1.00 | 100.0 / 18.1 / 1.00 | 630 |
| dog | 100.0 / 25.5 / 1.00 | 100.0 / 21.3 / 1.00 | 100.0 / 21.3 / 1.00 | 570 |
| horse | 95.2 / 17.8 / 1.00 | 100.0 / 14.8 / 1.00 | 100.0 / 14.9 / 1.00 | 630 |
| pear | 100.0 / 22.3 / 1.00 | 100.0 / 16.9 / 1.00 | 77.0 / 22.9 / 1.00 | 690 |
| tomato | 92.2 / 24.5 / 0.94 | 100.0 / 16.0 / 1.00 | 99.6 / 15.9 / 1.00 | 690 |

Errores de clase de M más frecuentes (verdadera → vecino real):

- tomato → apple: 54
- horse → cow: 30
- apple → tomato: 19
- apple → pear: 9
- apple → dog: 5
- apple → car: 2
- apple → cow: 1

## N = 50

| clase | M: clase / d_nn / compat | T-oraculo: clase / d_nn / compat | T-protocolo: clase / d_nn / compat | n M |
|---|---|---|---|---|
| apple | 94.8 / 33.6 / 0.95 | 100.0 / 23.3 / 1.00 | 100.0 / 23.1 / 1.00 | 660 |
| car | 99.0 / 26.9 / 0.98 | 100.0 / 22.0 / 1.00 | 95.2 / 23.0 / 1.00 | 630 |
| cow | 100.0 / 22.8 / 1.00 | 100.0 / 18.2 / 1.00 | 100.0 / 18.3 / 1.00 | 630 |
| cup | 100.0 / 25.6 / 1.00 | 100.0 / 21.4 / 1.00 | 100.0 / 21.5 / 1.00 | 630 |
| dog | 100.0 / 30.0 / 1.00 | 100.0 / 23.3 / 1.00 | 100.0 / 23.1 / 1.00 | 570 |
| horse | 95.2 / 21.3 / 1.00 | 100.0 / 19.7 / 1.00 | 100.0 / 19.6 / 1.00 | 630 |
| pear | 100.0 / 24.7 / 1.00 | 100.0 / 18.4 / 1.00 | 93.5 / 20.5 / 1.00 | 690 |
| tomato | 92.5 / 27.2 / 0.93 | 100.0 / 17.4 / 1.00 | 99.6 / 17.5 / 1.00 | 690 |

Errores de clase de M más frecuentes (verdadera → vecino real):

- tomato → apple: 50
- horse → cow: 30
- apple → tomato: 15
- apple → pear: 8
- apple → dog: 7
- car → apple: 3
- car → dog: 2
- apple → cup: 2

## N = 100

| clase | M: clase / d_nn / compat | T-oraculo: clase / d_nn / compat | T-protocolo: clase / d_nn / compat | n M |
|---|---|---|---|---|
| apple | 93.2 / 35.2 / 0.95 | 100.0 / 25.9 / 1.00 | 100.0 / 25.4 / 1.00 | 660 |
| car | 98.3 / 31.1 / 0.98 | 100.0 / 25.4 / 1.00 | 95.2 / 26.2 / 1.00 | 630 |
| cow | 100.0 / 23.8 / 1.00 | 100.0 / 19.7 / 1.00 | 100.0 / 19.6 / 1.00 | 630 |
| cup | 100.0 / 28.7 / 1.00 | 100.0 / 24.1 / 1.00 | 100.0 / 23.9 / 1.00 | 630 |
| dog | 100.0 / 30.1 / 1.00 | 100.0 / 23.8 / 1.00 | 100.0 / 23.8 / 1.00 | 570 |
| horse | 95.2 / 24.7 / 1.00 | 100.0 / 25.4 / 1.00 | 100.0 / 25.7 / 1.00 | 630 |
| pear | 100.0 / 30.5 / 1.00 | 100.0 / 21.5 / 1.00 | 93.5 / 23.7 / 1.00 | 690 |
| tomato | 92.0 / 31.2 / 0.89 | 100.0 / 21.9 / 1.00 | 99.6 / 21.8 / 1.00 | 690 |

Errores de clase de M más frecuentes (verdadera → vecino real):

- tomato → apple: 50
- horse → cow: 30
- apple → tomato: 21
- apple → pear: 11
- apple → dog: 9
- car → dog: 8
- apple → cow: 3
- tomato → dog: 2

## N = 200

| clase | M: clase / d_nn / compat | T-oraculo: clase / d_nn / compat | T-protocolo: clase / d_nn / compat | n M |
|---|---|---|---|---|
| apple | 94.4 / 38.3 / 0.95 | 100.0 / 28.7 / 1.00 | 100.0 / 28.8 / 1.00 | 660 |
| car | 97.9 / 32.1 / 0.98 | 100.0 / 31.2 / 1.00 | 95.2 / 32.0 / 1.00 | 630 |
| cow | 100.0 / 28.9 / 1.00 | 100.0 / 22.0 / 1.00 | 100.0 / 21.8 / 1.00 | 630 |
| cup | 100.0 / 33.2 / 1.00 | 100.0 / 27.3 / 1.00 | 100.0 / 27.5 / 1.00 | 630 |
| dog | 100.0 / 33.2 / 1.00 | 100.0 / 28.9 / 1.00 | 100.0 / 28.9 / 1.00 | 570 |
| horse | 95.2 / 26.5 / 1.00 | 100.0 / 27.1 / 1.00 | 100.0 / 26.9 / 1.00 | 630 |
| pear | 100.0 / 33.4 / 1.00 | 100.0 / 24.1 / 1.00 | 93.9 / 25.7 / 1.00 | 690 |
| tomato | 87.7 / 33.4 / 0.90 | 100.0 / 25.3 / 1.00 | 99.6 / 25.0 / 1.00 | 690 |

Errores de clase de M más frecuentes (verdadera → vecino real):

- tomato → apple: 49
- tomato → pear: 32
- horse → cow: 30
- apple → tomato: 13
- apple → dog: 11
- apple → pear: 10
- car → dog: 7
- car → pear: 4
