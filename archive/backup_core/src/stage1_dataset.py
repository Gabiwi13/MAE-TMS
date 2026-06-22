"""
Etapa 1 — Dataset ETH-80.
Descarga, extrae y organiza en data/eth80/{clase}/.
Genera splits train/test 80/20 y los guarda en data/eth80/splits.json.
"""
import os
import json
import random
import tarfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data" / "eth80"
ETH80_URL = "http://datasets.d2.mpi-inf.mpg.de/eth80/eth80-cropped-close128.tgz"
TGZ_PATH = ROOT / "data" / "eth80-cropped-close128.tgz"

CLASSES = ["apple", "horse", "car"]


def download():
    DATA_DIR.parent.mkdir(parents=True, exist_ok=True)
    if TGZ_PATH.exists():
        print(f"Archive already downloaded: {TGZ_PATH}")
        return
    print(f"Downloading ETH-80 from {ETH80_URL} ...")
    urllib.request.urlretrieve(ETH80_URL, TGZ_PATH)
    print(f"Saved to {TGZ_PATH}")


def extract():
    if (DATA_DIR / "apple").exists():
        print("ETH-80 already extracted.")
        return
    print(f"Extracting {TGZ_PATH} ...")
    with tarfile.open(TGZ_PATH, "r:gz") as tar:
        tar.extractall(path=DATA_DIR.parent)
    print("Extraction complete.")


def organize():
    """
    ETH-80 archives extract to eth80-cropped-close128/{class_name}{N}/
    (e.g. apple1, apple2, ..., apple10, horse1, ..., car1, ...).
    Flatten to data/eth80/{class_name}/*.png.
    """
    import shutil, re
    for cls in CLASSES:
        (DATA_DIR / cls).mkdir(parents=True, exist_ok=True)

    raw_root = DATA_DIR.parent / "eth80-cropped-close128"

    count = {c: 0 for c in CLASSES}
    for subdir in sorted(raw_root.iterdir()):
        if not subdir.is_dir():
            continue
        # Match class prefix: e.g. "apple10" -> "apple", "horse3" -> "horse"
        m = re.match(r'^([a-zA-Z]+)\d+$', subdir.name)
        if m is None:
            continue
        cls = m.group(1).lower()
        if cls not in CLASSES:
            continue
        for img_path in subdir.glob("*.png"):
            dest = DATA_DIR / cls / img_path.name
            if not dest.exists():
                shutil.copy2(img_path, dest)
            count[cls] += 1
    for cls, n in count.items():
        print(f"  {cls}: {n} images")


def make_splits(seed: int = 42):
    splits_path = DATA_DIR / "splits.json"
    if splits_path.exists():
        print("Splits already exist.")
        return json.loads(splits_path.read_text())

    random.seed(seed)
    splits = {}
    for cls in CLASSES:
        imgs = sorted(str(p) for p in (DATA_DIR / cls).glob("*.png"))
        random.shuffle(imgs)
        n_train = int(0.8 * len(imgs))
        splits[cls] = {"train": imgs[:n_train], "test": imgs[n_train:]}
        print(f"  {cls}: {n_train} train / {len(imgs)-n_train} test")

    splits_path.write_text(json.dumps(splits, indent=2))
    print(f"Splits saved to {splits_path}")
    return splits


def verify():
    ok = True
    for cls in CLASSES:
        imgs = list((DATA_DIR / cls).glob("*.png"))
        n = len(imgs)
        if n < 200:
            print(f"ERROR: {cls} has only {n} images (expected ~410)")
            ok = False
        else:
            print(f"  OK {cls}: {n} images")
    return ok


if __name__ == "__main__":
    download()
    extract()
    organize()
    ok = verify()
    if ok:
        make_splits()
        print("\nEtapa 1 COMPLETADA.")
    else:
        print("\nEtapa 1 FALLIDA — revisar imágenes.")
