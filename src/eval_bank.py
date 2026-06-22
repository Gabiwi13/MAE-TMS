"""
Banco de evaluacion neutral: las 80 consultas con ground truth.

Vive aqui (y no en run_ablation.py) para que los experimentos oficiales no
dependan de un script. Modulo sin dependencias pesadas: solo listas de texto.

  APPLE/HORSE/CAR_QUERIES  consultas por dominio
  DOMAIN_QUERIES           dict dominio -> consultas
  ALL_QUERIES, GROUND_TRUTH  banco interleaved apple/horse/car (80 items)
"""

CLASSES = ("apple", "horse", "car")

APPLE_QUERIES = [
    "a round red fruit", "green food from trees", "red or green round food",
    "has core and seeds", "a delicious pome", "red fruit with a stem",
    "grows on fruit trees", "juicy round fruit", "sweet core fruit",
    "a pear or apple fruit", "fruit with skin and seeds", "orange cousin red food",
    "green and red food", "a macintosh variety", "made into pie",
    "round red food", "stem leaf core inside", "a green fruit",
    "fruit with seeds inside", "delicious red round fruit",
    "adam and eve fruit", "orange red green food", "core inside skin fruit",
    "tree fruit food", "pome variety fruit", "green round food",
    "red sweet fruit food",
]

HORSE_QUERIES = [
    "animal with a mane", "large powerful mammal", "has four legs and hooves",
    "riding and racing animal", "an equine animal", "big farm animal",
    "has a long tail", "a pony or donkey", "mammal with saddle",
    "racing animal with mane", "big four legged animal", "riding farm animal",
    "farm mammal with mane", "equine riding beast", "has hooves and tail",
    "donkey and zebra relative", "big strong animal", "saddle riding animal",
    "cow and horse farm animals", "animal that races", "a ridden animal",
    "four legged riding mammal", "mammal with hooves and mane",
    "equine with saddle", "big farm riding animal",
    "domesticated equine mammal", "animal with mane and tail",
]

CAR_QUERIES = [
    "fast vehicle with wheels", "machine for transportation",
    "automobile with seats", "has wheels and engine", "a heavy vehicle",
    "passenger transportation machine", "seats and windows inside",
    "a motor vehicle", "used for driving", "wheeled automobile",
    "driving machine", "automobile with heavy seats",
    "crash and accident vehicle", "passenger seats inside",
    "vehicle with driver", "red automobile", "transportation vehicle",
    "automobile for transport", "seats and windows vehicle",
    "heavy automobile", "motor vehicle transport", "driver automobile",
    "wheeled transportation", "crash vehicle", "automobile commuting",
    "auto transportation machine",
]

DOMAIN_QUERIES = {"apple": APPLE_QUERIES, "horse": HORSE_QUERIES, "car": CAR_QUERIES}

# Banco interleaved apple/horse/car (mismo orden de construccion que el original)
ALL_QUERIES, GROUND_TRUTH = [], []
for _i in range(max(len(APPLE_QUERIES), len(HORSE_QUERIES), len(CAR_QUERIES))):
    for _cls in CLASSES:
        _pool = DOMAIN_QUERIES[_cls]
        if _i < len(_pool):
            ALL_QUERIES.append(_pool[_i])
            GROUND_TRUTH.append(_cls)
