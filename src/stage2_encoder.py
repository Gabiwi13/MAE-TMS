"""
Etapa 2 — Autoencoder basado en ResNet18 para ETH-80 (NO es un masked
autoencoder: no hay enmascaramiento de entrada).
Encoder: ResNet18 pretrained -> 64-dim latent vector.
Decoder: ConvTranspose -> 128x128x3.
Loss: MSE reconstrucción + 0.1 * CrossEntropy clasificación. La cabeza
clasificadora es solo una señal auxiliar de entrenamiento; durante las fases
EAM-TMS (routing y recall) NO participa: solo se usan encoder y decoder.
"""
import json
import sys
import os
import copy
import time
import random
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from PIL import Image

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data" / "eth80"
MODELS_DIR = ROOT / "models"
MODELS_DIR.mkdir(exist_ok=True)
META_PATH = MODELS_DIR / "encoder.meta.json"

CLASSES = ["apple", "horse", "car"]
CLASS_TO_IDX = {c: i for i, c in enumerate(CLASSES)}
LATENT_DIM = 64
IMG_SIZE = 128
BATCH_SIZE = 32
EPOCHS = 50
LR = 1e-3
SEED = 42
# Criterios de aceptación del encoder. Un modelo que no los cumpla NO debe usarse
# aguas abajo: las etapas 5-8 cuantizan los latentes de este encoder, así que un
# encoder a medio entrenar contamina todo el experimento sin lanzar errores.
RMSE_MAX = 0.3
ACC_MIN = 85.0
MODEL_FILES = ("encoder.pt", "decoder.pt", "classifier.pt")
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def set_seed(seed: int = SEED):
    """Fija todas las fuentes de aleatoriedad para que el entrenamiento sea
    reproducible: sin esto cada réplica obtiene un encoder distinto y los números
    del reporte no se pueden reproducir."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def _inv_norm():
    return transforms.Normalize(
        mean=[-0.485/0.229, -0.456/0.224, -0.406/0.225],
        std=[1/0.229, 1/0.224, 1/0.225])


class ETH80Dataset(Dataset):
    def __init__(self, image_paths, transform=None):
        self.paths = image_paths
        self.transform = transform

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        path = self.paths[idx]
        img = Image.open(path).convert("RGB").resize((IMG_SIZE, IMG_SIZE))
        # extract class from path
        cls = Path(path).parent.name
        label = CLASS_TO_IDX[cls]
        if self.transform:
            img = self.transform(img)
        return img, label


class Encoder(nn.Module):
    def __init__(self, latent_dim=LATENT_DIM):
        super().__init__()
        backbone = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        # Remove final FC, keep up to avgpool -> 512-dim
        self.features = nn.Sequential(*list(backbone.children())[:-1])
        self.fc = nn.Linear(512, latent_dim)

    def forward(self, x):
        f = self.features(x)         # (B, 512, 1, 1)
        f = f.view(f.size(0), -1)    # (B, 512)
        z = self.fc(f)               # (B, latent_dim)
        return z


class Decoder(nn.Module):
    """ConvTranspose2d decoder: 64-dim -> 128x128x3."""
    def __init__(self, latent_dim=LATENT_DIM):
        super().__init__()
        self.fc = nn.Linear(latent_dim, 512 * 4 * 4)
        self.deconv = nn.Sequential(
            # 4x4 -> 8x8
            nn.ConvTranspose2d(512, 256, 4, stride=2, padding=1),
            nn.BatchNorm2d(256), nn.ReLU(),
            # 8x8 -> 16x16
            nn.ConvTranspose2d(256, 128, 4, stride=2, padding=1),
            nn.BatchNorm2d(128), nn.ReLU(),
            # 16x16 -> 32x32
            nn.ConvTranspose2d(128, 64, 4, stride=2, padding=1),
            nn.BatchNorm2d(64), nn.ReLU(),
            # 32x32 -> 64x64
            nn.ConvTranspose2d(64, 32, 4, stride=2, padding=1),
            nn.BatchNorm2d(32), nn.ReLU(),
            # 64x64 -> 128x128
            nn.ConvTranspose2d(32, 3, 4, stride=2, padding=1),
            nn.Sigmoid(),
        )

    def forward(self, z):
        x = self.fc(z)
        x = x.view(-1, 512, 4, 4)
        return self.deconv(x)


class Classifier(nn.Module):
    def __init__(self, latent_dim=LATENT_DIM, n_classes=len(CLASSES)):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(latent_dim, 64),
            nn.ReLU(),
            nn.Linear(64, n_classes),
        )

    def forward(self, z):
        return self.fc(z)


def get_loaders(seed: int = SEED):
    splits_path = DATA_DIR / "splits.json"
    if not splits_path.exists():
        raise FileNotFoundError(
            f"No existe {splits_path}. Ejecuta la etapa 1 (stage1_dataset) para "
            f"descargar ETH-80 y generar los splits antes de entrenar el encoder.")
    splits = json.loads(splits_path.read_text())

    transform_train = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(0.2, 0.2, 0.2),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

    train_paths = []
    test_paths = []
    for cls in CLASSES:
        train_paths += splits[cls]["train"]
        test_paths += splits[cls]["test"]

    train_ds = ETH80Dataset(train_paths, transform_train)
    test_ds = ETH80Dataset(test_paths, transform_test)
    g = torch.Generator()
    g.manual_seed(seed)
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,
                              num_workers=0, generator=g)
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)
    return train_loader, test_loader


def _snapshot(*nets):
    """Copia profunda de los pesos (en CPU) para conservar el mejor modelo en
    memoria sin tocar el disco hasta el final."""
    return [copy.deepcopy({k: v.detach().cpu() for k, v in n.state_dict().items()})
            for n in nets]


def _restore(nets, state):
    for n, s in zip(nets, state):
        n.load_state_dict(s)


def train(seed: int = SEED):
    set_seed(seed)
    print(f"Training on {DEVICE} (seed={seed})")
    train_loader, test_loader = get_loaders(seed)

    encoder = Encoder().to(DEVICE)
    decoder = Decoder().to(DEVICE)
    classifier = Classifier().to(DEVICE)

    params = list(encoder.parameters()) + list(decoder.parameters()) + list(classifier.parameters())
    optimizer = optim.Adam(params, lr=LR)
    mse_loss = nn.MSELoss()
    ce_loss = nn.CrossEntropyLoss()
    inv_norm = _inv_norm()

    # Cualquier manifiesto previo deja de ser válido en cuanto empieza un
    # entrenamiento nuevo: lo borramos para que, si esto se interrumpe a la
    # mitad, no quede un centinela mintiendo que el entrenamiento terminó.
    if META_PATH.exists():
        META_PATH.unlink()

    best = {"rmse": float("inf"), "acc": 0.0, "state": None}
    for epoch in range(1, EPOCHS + 1):
        encoder.train(); decoder.train(); classifier.train()
        total_loss = 0.0
        for imgs, labels in train_loader:
            imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
            # denormalize for MSE target
            imgs_orig = torch.stack([inv_norm(img) for img in imgs]).clamp(0, 1)

            optimizer.zero_grad()
            z = encoder(imgs)
            recon = decoder(z)
            logits = classifier(z)

            loss_recon = mse_loss(recon, imgs_orig)
            loss_cls = ce_loss(logits, labels)
            loss = loss_recon + 0.1 * loss_cls
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * len(imgs)

        avg_loss = total_loss / len(train_loader.dataset)
        if epoch % 10 == 0:
            rmse, acc = evaluate(encoder, decoder, classifier, test_loader, inv_norm)
            print(f"Epoch {epoch:3d}/{EPOCHS}  loss={avg_loss:.4f}  "
                  f"RMSE={rmse:.4f}  acc={acc:.1f}%")
            # El mejor modelo se conserva EN MEMORIA, no en disco: así lo validado
            # y lo guardado son siempre el mismo modelo (antes podían diferir).
            if rmse < best["rmse"]:
                best.update(rmse=rmse, acc=acc,
                            state=_snapshot(encoder, decoder, classifier))

    # Restaurar el mejor modelo, validarlo, y solo entonces persistirlo + manifiesto.
    if best["state"] is not None:
        _restore((encoder, decoder, classifier), best["state"])
    rmse, acc = evaluate(encoder, decoder, classifier, test_loader, inv_norm)
    save_models(encoder, decoder, classifier)
    write_manifest(rmse, acc, seed=seed, source="trained")
    print(f"\nFinal (best) RMSE={rmse:.4f}  acc={acc:.1f}%")
    return rmse, acc, encoder, decoder, classifier


def evaluate(encoder, decoder, classifier, loader, inv_norm):
    encoder.eval(); decoder.eval(); classifier.eval()
    mse_total = 0.0
    correct = 0
    n = 0
    with torch.no_grad():
        for imgs, labels in loader:
            imgs, labels = imgs.to(DEVICE), labels.to(DEVICE)
            imgs_orig = torch.stack([inv_norm(img) for img in imgs]).clamp(0, 1)
            z = encoder(imgs)
            recon = decoder(z)
            logits = classifier(z)
            # per-pixel MSE: sum over all pixels, divide by n*H*W*C later
            mse_total += nn.MSELoss(reduction="mean")(recon, imgs_orig).item() * len(imgs)
            correct += (logits.argmax(1) == labels).sum().item()
            n += len(imgs)
    rmse = (mse_total / n) ** 0.5   # per-pixel RMSE in [0,1] range
    acc = 100.0 * correct / n
    return rmse, acc


def _atomic_save(state, path):
    """Guarda a un temporal y renombra: un Ctrl-C a mitad de torch.save deja el
    .tmp corrupto, nunca el .pt definitivo."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    torch.save(state, tmp)
    os.replace(tmp, path)


def save_models(encoder, decoder, classifier):
    _atomic_save(encoder.state_dict(), MODELS_DIR / "encoder.pt")
    _atomic_save(decoder.state_dict(), MODELS_DIR / "decoder.pt")
    _atomic_save(classifier.state_dict(), MODELS_DIR / "classifier.pt")
    print("  Models saved (atómico).")


def write_manifest(rmse, acc, seed, source="trained"):
    """Centinela de entrenamiento completo. Se escribe DESPUÉS de los tres .pt;
    su presencia + 'completed' garantiza que el conjunto está completo y validado."""
    META_PATH.write_text(json.dumps({
        "completed": True,
        "source": source,
        "seed": seed,
        "epochs": EPOCHS,
        "rmse": round(float(rmse), 6),
        "acc": round(float(acc), 4),
        "criteria": {"rmse_max": RMSE_MAX, "acc_min": ACC_MIN},
        "passed": bool(rmse < RMSE_MAX and acc >= ACC_MIN),
        "torch": torch.__version__,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }, indent=2), encoding="utf-8")


def read_manifest():
    if not META_PATH.exists():
        return None
    try:
        return json.loads(META_PATH.read_text(encoding="utf-8"))
    except Exception:
        return None


def _purge_models():
    """Elimina cualquier artefacto de encoder (incl. manifiesto y temporales)
    para forzar un reentrenamiento limpio."""
    for name in MODEL_FILES:
        for p in (MODELS_DIR / name, MODELS_DIR / (name + ".tmp")):
            if p.exists():
                p.unlink()
    if META_PATH.exists():
        META_PATH.unlink()


def models_status():
    """Estado del encoder en disco. Devuelve (status, detalle):
      ok        -> .pt completos + manifiesto que reporta criterios cumplidos
      missing   -> no hay ningún .pt
      corrupt   -> faltan archivos del conjunto o algún .pt es ilegible/truncado
      unmanaged -> .pt presentes pero sin manifiesto (versión previa: hay que validar)
      belowpar  -> manifiesto reporta entrenamiento incompleto o criterios no cumplidos
    """
    present = [n for n in MODEL_FILES if (MODELS_DIR / n).exists()]
    if not present:
        return "missing", "no hay encoder entrenado"
    if len(present) < len(MODEL_FILES):
        faltan = [n for n in MODEL_FILES if n not in present]
        return "corrupt", f"conjunto incompleto, faltan {faltan} (entrenamiento interrumpido)"
    # Todos presentes: detectar truncamiento/corrupción intentando deserializar.
    for n in MODEL_FILES:
        try:
            torch.load(MODELS_DIR / n, map_location="cpu")
        except Exception as e:
            return "corrupt", f"checkpoint ilegible ({n}): {e}"
    meta = read_manifest()
    if meta is None:
        return "unmanaged", "modelos presentes sin manifiesto (versión previa)"
    if not meta.get("completed") or not meta.get("passed"):
        return "belowpar", f"manifiesto reporta criterios no cumplidos ({meta})"
    return "ok", meta


def load_models():
    encoder = Encoder().to(DEVICE)
    decoder = Decoder().to(DEVICE)
    classifier = Classifier().to(DEVICE)
    encoder.load_state_dict(torch.load(MODELS_DIR / "encoder.pt", map_location=DEVICE))
    decoder.load_state_dict(torch.load(MODELS_DIR / "decoder.pt", map_location=DEVICE))
    classifier.load_state_dict(torch.load(MODELS_DIR / "classifier.pt", map_location=DEVICE))
    encoder.eval(); decoder.eval(); classifier.eval()
    return encoder, decoder, classifier


def ensure_models(force_retrain: bool = False, seed: int = SEED):
    """Garantiza un encoder válido y lo devuelve (encoder, decoder, classifier).

    Reentrena automáticamente si falta, está corrupto o no cumple criterios.
    Modelos de una versión previa sin manifiesto se VALIDAN (no se reentrenan):
    si pasan los criterios se les genera el manifiesto; si no, se reentrenan.
    """
    status, detail = ("missing", "reentrenamiento forzado") if force_retrain else models_status()

    if status == "unmanaged":
        print("  Modelos sin manifiesto detectados — validando los existentes "
              "(en vez de reentrenar)...")
        try:
            encoder, decoder, classifier = load_models()
            _, test_loader = get_loaders(seed)
            rmse, acc = evaluate(encoder, decoder, classifier, test_loader, _inv_norm())
        except Exception as e:
            status, detail = "corrupt", f"no se pudieron validar los modelos previos: {e}"
        else:
            if rmse < RMSE_MAX and acc >= ACC_MIN:
                write_manifest(rmse, acc, seed=None, source="pre-existing (validado, no reentrenado)")
                print(f"  Modelos previos válidos (RMSE={rmse:.4f} acc={acc:.1f}%) "
                      f"— manifiesto generado.")
                return encoder, decoder, classifier
            status, detail = "belowpar", (
                f"modelos previos no cumplen criterios (RMSE={rmse:.4f} acc={acc:.1f}%)")

    if status == "ok":
        print(f"  Encoder válido (RMSE={detail['rmse']} acc={detail['acc']}% "
              f"seed={detail.get('seed')}). Cargando...")
        return load_models()

    # missing / corrupt / belowpar  ->  reentrenamiento automático
    print(f"  Encoder no utilizable: {detail}")
    if status in ("corrupt", "belowpar"):
        print("  Limpiando artefactos inválidos antes de reentrenar...")
        _purge_models()
    print("  Reentrenando el encoder automáticamente desde cero "
          f"(~24 min en CPU, seed={seed})...")
    rmse, acc, encoder, decoder, classifier = train(seed=seed)
    if not (rmse < RMSE_MAX and acc >= ACC_MIN):
        raise RuntimeError(
            f"El reentrenamiento no alcanzó los criterios "
            f"(RMSE={rmse:.4f} acc={acc:.1f}%; se requiere RMSE<{RMSE_MAX} y acc>={ACC_MIN}). "
            f"Revisa que el dataset ETH-80 esté completo (etapa 1) y los hiperparámetros "
            f"antes de continuar; NO se debe seguir con un encoder inválido.")
    return encoder, decoder, classifier


def visualize_reconstructions(encoder, decoder, test_loader, n=5):
    """Save a grid of original vs reconstructed images."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    inv_norm = transforms.Normalize(
        mean=[-0.485/0.229, -0.456/0.224, -0.406/0.225],
        std=[1/0.229, 1/0.224, 1/0.225])

    encoder.eval(); decoder.eval()
    imgs, labels = next(iter(test_loader))
    imgs = imgs[:n].to(DEVICE)
    with torch.no_grad():
        z = encoder(imgs)
        recon = decoder(z)

    fig, axes = plt.subplots(2, n, figsize=(3*n, 6))
    for i in range(n):
        orig = inv_norm(imgs[i].cpu()).clamp(0, 1).permute(1, 2, 0).numpy()
        rec = recon[i].cpu().permute(1, 2, 0).numpy()
        axes[0, i].imshow(orig); axes[0, i].set_title(f"orig {CLASSES[labels[i]]}")
        axes[1, i].imshow(rec); axes[1, i].set_title("recon")
        for ax in [axes[0, i], axes[1, i]]:
            ax.axis("off")
    plt.tight_layout()
    out = ROOT / "stage2_reconstructions.png"
    plt.savefig(out, dpi=80)
    print(f"Reconstructions saved to {out}")


def get_prototype_latent(encoder, cls: str) -> np.ndarray:
    """Return mean latent vector for all training images of a class."""
    splits_path = DATA_DIR / "splits.json"
    splits = json.loads(splits_path.read_text())
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    paths = splits[cls]["train"]
    zs = []
    encoder.eval()
    with torch.no_grad():
        for p in paths:
            img = Image.open(p).convert("RGB").resize((IMG_SIZE, IMG_SIZE))
            img = transform(img).unsqueeze(0).to(DEVICE)
            z = encoder(img).cpu().numpy()[0]
            zs.append(z)
    return np.mean(zs, axis=0)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Etapa 2 — encoder/decoder ETH-80")
    ap.add_argument("--force-retrain", action="store_true",
                    help="ignora cualquier modelo en disco y reentrena desde cero")
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    encoder, decoder, classifier = ensure_models(force_retrain=args.force_retrain,
                                                 seed=args.seed)
    _, test_loader = get_loaders(args.seed)
    rmse, acc = evaluate(encoder, decoder, classifier, test_loader, _inv_norm())
    print(f"RMSE={rmse:.4f}  acc={acc:.1f}%")
    visualize_reconstructions(encoder, decoder, test_loader)

    if rmse < RMSE_MAX and acc >= ACC_MIN:
        print("\nEtapa 2 COMPLETADA.")
    else:
        print("\nEtapa 2 no cumple criterios — ajustar hiperparámetros.")
