# Experimento 11 — desglose por clase

Clase 1-NN (%), d a la instancia real más cercana y compat máximo, por clase y brazo; solo respuestas. Semillas y sorteos agregados.

## N = 25

| clase | M: clase / d_nn / compat | T-oraculo: clase / d_nn / compat | T-protocolo: clase / d_nn / compat | n M |
|---|---|---|---|---|
| apple | 87.6 / 17.9 / 0.95 | 100.0 / 13.0 / 1.00 | 97.7 / 14.0 / 1.00 | 660 |
| car | 100.0 / 20.6 / 0.99 | 100.0 / 19.4 / 1.00 | 88.9 / 22.3 / 1.00 | 270 |
| cow | 100.0 / 13.6 / 1.00 | 100.0 / 13.5 / 1.00 | 99.5 / 13.8 / 1.00 | 630 |
| cup | 100.0 / 16.7 / 1.00 | 100.0 / 16.3 / 1.00 | 100.0 / 16.3 / 1.00 | 630 |
| dog | 100.0 / 19.4 / 1.00 | 100.0 / 18.4 / 1.00 | 100.0 / 18.3 / 1.00 | 240 |
| horse | 83.3 / 20.8 / 1.00 | 100.0 / 14.8 / 1.00 | 96.7 / 15.6 / 1.00 | 360 |
| pear | 100.0 / 13.7 / 1.00 | 100.0 / 14.4 / 1.00 | 100.0 / 14.4 / 1.00 | 690 |
| tomato | 95.5 / 20.2 / 0.98 | 100.0 / 16.4 / 1.00 | 99.6 / 16.5 / 1.00 | 690 |

Errores de clase de M más frecuentes (verdadera → vecino real):

- horse → cow: 60
- apple → tomato: 59
- tomato → apple: 28
- apple → dog: 11
- apple → pear: 10
- tomato → pear: 2
- apple → cow: 2
- tomato → dog: 1

## N = 50

| clase | M: clase / d_nn / compat | T-oraculo: clase / d_nn / compat | T-protocolo: clase / d_nn / compat | n M |
|---|---|---|---|---|
| apple | 89.7 / 27.0 / 0.95 | 100.0 / 20.2 / 1.00 | 93.6 / 22.1 / 1.00 | 660 |
| car | 100.0 / 21.0 / 0.99 | 100.0 / 20.1 / 1.00 | 95.2 / 21.4 / 1.00 | 630 |
| cow | 100.0 / 16.2 / 1.00 | 100.0 / 16.5 / 1.00 | 98.5 / 17.2 / 1.00 | 630 |
| cup | 100.0 / 22.9 / 1.00 | 100.0 / 19.2 / 1.00 | 100.0 / 19.3 / 1.00 | 630 |
| dog | 100.0 / 27.6 / 1.00 | 100.0 / 29.4 / 1.00 | 100.0 / 29.4 / 1.00 | 570 |
| horse | 95.2 / 17.4 / 1.00 | 100.0 / 14.6 / 1.00 | 100.0 / 14.5 / 1.00 | 630 |
| pear | 100.0 / 17.9 / 1.00 | 100.0 / 15.5 / 1.00 | 98.3 / 16.0 / 1.00 | 690 |
| tomato | 92.6 / 21.0 / 0.97 | 100.0 / 16.7 / 1.00 | 98.3 / 17.8 / 1.00 | 690 |

Errores de clase de M más frecuentes (verdadera → vecino real):

- tomato → apple: 39
- apple → tomato: 31
- horse → cow: 30
- apple → pear: 18
- apple → dog: 16
- tomato → dog: 5
- tomato → pear: 4
- tomato → car: 3

## N = 100

| clase | M: clase / d_nn / compat | T-oraculo: clase / d_nn / compat | T-protocolo: clase / d_nn / compat | n M |
|---|---|---|---|---|
| apple | 93.5 / 27.0 / 0.95 | 100.0 / 19.6 / 1.00 | 93.6 / 21.3 / 1.00 | 660 |
| car | 100.0 / 26.2 / 0.99 | 100.0 / 24.7 / 1.00 | 95.2 / 25.6 / 1.00 | 630 |
| cow | 100.0 / 20.2 / 1.00 | 100.0 / 16.8 / 1.00 | 99.0 / 17.2 / 1.00 | 630 |
| cup | 100.0 / 23.6 / 1.00 | 100.0 / 19.2 / 1.00 | 100.0 / 19.2 / 1.00 | 630 |
| dog | 100.0 / 27.1 / 1.00 | 100.0 / 25.6 / 1.00 | 100.0 / 25.5 / 1.00 | 570 |
| horse | 95.2 / 20.2 / 1.00 | 100.0 / 17.0 / 1.00 | 100.0 / 16.9 / 1.00 | 630 |
| pear | 100.0 / 21.3 / 1.00 | 100.0 / 18.3 / 1.00 | 93.5 / 20.2 / 1.00 | 690 |
| tomato | 93.3 / 25.6 / 0.92 | 100.0 / 17.1 / 1.00 | 98.3 / 17.8 / 1.00 | 690 |

Errores de clase de M más frecuentes (verdadera → vecino real):

- tomato → apple: 36
- horse → cow: 30
- apple → tomato: 17
- apple → pear: 15
- apple → dog: 6
- tomato → pear: 5
- tomato → dog: 3
- apple → car: 3

## N = 200

| clase | M: clase / d_nn / compat | T-oraculo: clase / d_nn / compat | T-protocolo: clase / d_nn / compat | n M |
|---|---|---|---|---|
| apple | 91.8 / 29.2 / 0.94 | 100.0 / 20.3 / 1.00 | 93.6 / 22.0 / 1.00 | 660 |
| car | 99.8 / 27.7 / 0.98 | 100.0 / 24.6 / 1.00 | 95.2 / 25.5 / 1.00 | 630 |
| cow | 100.0 / 24.8 / 1.00 | 100.0 / 25.4 / 1.00 | 95.0 / 26.6 / 1.00 | 630 |
| cup | 100.0 / 26.4 / 1.00 | 100.0 / 25.9 / 1.00 | 100.0 / 25.6 / 1.00 | 630 |
| dog | 100.0 / 28.6 / 1.00 | 100.0 / 25.8 / 1.00 | 100.0 / 25.8 / 1.00 | 570 |
| horse | 95.2 / 22.9 / 1.00 | 100.0 / 19.6 / 1.00 | 100.0 / 19.1 / 1.00 | 630 |
| pear | 100.0 / 23.1 / 1.00 | 100.0 / 19.7 / 1.00 | 99.1 / 19.9 / 1.00 | 690 |
| tomato | 93.3 / 30.8 / 0.90 | 100.0 / 17.5 / 1.00 | 97.4 / 18.5 / 1.00 | 690 |

Errores de clase de M más frecuentes (verdadera → vecino real):

- tomato → apple: 41
- horse → cow: 30
- apple → pear: 25
- apple → tomato: 18
- apple → dog: 4
- apple → car: 4
- tomato → dog: 3
- apple → horse: 2
