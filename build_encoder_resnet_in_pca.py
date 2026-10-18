"""
Exp19: encoder congelado = ResNet18 de ImageNet + PCA a 64.

Cabe en la clase Encoder de stage2_encoder sin cambiarla: `features` lleva los
pesos de ImageNet tal cual y `fc` es la PCA (pesos = componentes, sesgo =
-componentes · media). La PCA se ajusta solo con las imágenes originales de
train. Escribe models/encoder.pt y su manifiesto.
"""
import json
import sys
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torchvision import models

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from stage2_encoder import Encoder, MODELS_DIR, DATA_DIR, IMG_SIZE, CLASSES  # noqa: E402
from stage7_bidirectional import IMG_TRANSFORM  # noqa: E402


def main():
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    enc = Encoder()
    backbone = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
    enc.features.load_state_dict(torch.nn.Sequential(*list(backbone.children())[:-1]).state_dict())
    enc = enc.to(dev).eval()
    splits = json.loads((DATA_DIR / "splits.json").read_text())
    feats = []
    for cls in CLASSES:
        batch = torch.stack([IMG_TRANSFORM(Image.open(p).convert("RGB").resize((IMG_SIZE, IMG_SIZE)))
                             for p in splits[cls]["train"]]).to(dev)
        with torch.no_grad():
            for i in range(0, len(batch), 64):
                feats.append(enc.features(batch[i:i + 64]).flatten(1).cpu().numpy())
    X = np.concatenate(feats).astype(np.float64)
    mu = X.mean(0)
    _u, s, vt = np.linalg.svd(X - mu, full_matrices=False)
    V = vt[:64]
    var = float((s[:64] ** 2).sum() / (s ** 2).sum())
    with torch.no_grad():
        enc.fc.weight.copy_(torch.tensor(V, dtype=torch.float32))
        enc.fc.bias.copy_(torch.tensor(-V @ mu, dtype=torch.float32))
    torch.save(enc.state_dict(), MODELS_DIR / "encoder.pt")
    (MODELS_DIR / "encoder.meta.json").write_text(json.dumps({
        "completed": True, "source": "congelado: ResNet18 IMAGENET1K_V1 + PCA a 64 (train)",
        "n_train": int(X.shape[0]), "varianza_explicada_64": var, "passed": True}, indent=1))
    print(f"encoder congelado guardado; {X.shape[0]} imágenes de train, varianza explicada por 64 componentes {var:.3f}")


if __name__ == "__main__":
    main()
