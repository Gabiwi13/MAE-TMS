"""
Experimento 18, sonda de rasgos: ¿qué encoder lleva las características
dentro de la clase?

Misma sonda que exp17/exp18 (k = 5 vecinos, leave-object-out dentro de la clase,
acierto balanceado) sobre cuatro rasgos de la vista original:
  propio        latente de 64 del encoder del proyecto (ResNet18 de ImageNet
                ajustado con reconstrucción + 0.1 x clasificación de clase)
  resnet18_in   ResNet18 de ImageNet sin ese ajuste (512, avgpool)
  dinov2_s      DINOv2-small (384, token CLS)
y las dos externas reducidas a 64 con PCA (sin etiquetas). Diagnóstico: los
rasgos externos no entran al pipeline oficial.

Uso:
  python run_experiment18_feature_probe.py
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import run_experiment18_attributes as e18  # noqa: E402
from run_experiment17_specific_word import CLASSES, LAT_PATH, IDX_PATH, object_id  # noqa: E402

OUT = ROOT / "results" / "experimento18"
FEATS = OUT / "rasgos"          # fuera de git
COLORS = ROOT / "results" / "experimento17" / "colores_borrador.json"
K = 5


def extract(name):
    path = FEATS / f"{name}.npy"
    if path.exists():
        return np.load(path)
    import torch
    from PIL import Image
    from torchvision import models, transforms
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    if name == "resnet18_in":
        net = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        net.fc = torch.nn.Identity()
        size = 128          # el tamaño con que trabaja el encoder propio
    else:
        net = torch.hub.load("facebookresearch/dinov2", "dinov2_vits14")
        size = 224
    net = net.to(dev).eval()
    tf = transforms.Compose([transforms.Resize((size, size)), transforms.ToTensor(),
                             transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
    index = json.loads(IDX_PATH.read_text())
    out = []
    for cls in CLASSES:
        batch = [tf(Image.open(p).convert("RGB")) for p in index[cls]]
        with torch.no_grad():
            f = torch.cat([net(torch.stack(batch[i:i + 64]).to(dev)).cpu() for i in range(0, len(batch), 64)])
        out.append(f.numpy())
        print(f"  {name} {cls}: {f.shape}", flush=True)
    arr = np.stack(out).astype(np.float32)        # (8, 410, d)
    FEATS.mkdir(parents=True, exist_ok=True)
    np.save(path, arr)
    return arr


def resnet_variant_latents():
    """ResNet18 de ImageNet sobre las 16 variantes de cada vista, al mismo
    tamaño que el encoder propio; PCA a 64 ajustada sobre las originales (sin
    etiquetas). Estadísticas min/max sobre las originales con margen del 10 %,
    como compute_global_latent_stats."""
    lat = FEATS / "latentes_resnet18_in_pca64.npy"
    st = FEATS / "stats_resnet18_in_pca64.json"
    if lat.exists() and st.exists():
        return lat, st
    import torch
    from PIL import Image
    from torchvision import models, transforms
    from stage5_fill import augment_variants
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    net = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
    net.fc = torch.nn.Identity()
    net = net.to(dev).eval()
    tf = transforms.Compose([transforms.ToTensor(),
                             transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
    index = json.loads(IDX_PATH.read_text())
    feats = np.zeros((len(CLASSES), 410, 16, 512), dtype=np.float32)
    for ci, cls in enumerate(CLASSES):
        for i, p in enumerate(index[cls]):
            img = Image.open(p).convert("RGB").resize((128, 128))
            with torch.no_grad():
                feats[ci, i] = net(torch.stack([tf(v) for v in augment_variants(img)]).to(dev)).cpu().numpy()
        print(f"  variantes {cls}", flush=True)
    orig = feats[:, :, 0].reshape(-1, 512)
    mu = orig.mean(0)
    _u, _s, vt = np.linalg.svd(orig - mu, full_matrices=False)
    z = ((feats - mu) @ vt[:64].T).astype(np.float32)
    np.save(lat, z)
    zo = z[:, :, 0].reshape(-1, 64)
    lo, hi = zo.min(0), zo.max(0)
    pad = 0.1 * (hi - lo)
    st.write_text(json.dumps({"min": (lo - pad).tolist(), "max": (hi + pad).tolist(),
                              "nota": "originales de las 3280 vistas, margen 10 %"}))
    return lat, st


def pca64(arr):
    X = arr.reshape(-1, arr.shape[-1])
    X = X - X.mean(0)
    _u, _s, vt = np.linalg.svd(X, full_matrices=False)
    return (X @ vt[:64].T).reshape(arr.shape[0], arr.shape[1], 64)


def axis_values(cls, axis, path):
    if axis == "color":
        lab = json.loads(COLORS.read_text(encoding="utf-8"))[cls][str(object_id(path))]
        return lab["color"] if lab["claro"] else None
    return e18.value_of(cls, axis, path)


def probe(feats, cls, axis, index):
    ci = CLASSES.index(cls)
    I = [i for i, p in enumerate(index[cls]) if axis_values(cls, axis, p)]
    y = np.array([axis_values(cls, axis, index[cls][i]) for i in I])
    if len(set(y)) < 2:
        return None
    X = feats[ci, I]
    X = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-8)
    obj = np.array([object_id(index[cls][i]) for i in I])
    pred = []
    for k in range(len(I)):
        m = obj != obj[k]
        nn = np.argsort(-(X[m] @ X[k]))[:K]
        v, c = np.unique(y[m][nn], return_counts=True)
        pred.append(v[np.argmax(c)])
    pred = np.array(pred)
    return {c: float(np.mean(pred[y == c] == c)) for c in sorted(set(y))}


def main():
    index = json.loads(IDX_PATH.read_text())
    reps = {"propio": np.load(LAT_PATH)[:, :, 0, :]}
    for name in ("resnet18_in", "dinov2_s"):
        arr = extract(name)
        reps[name] = arr
        reps[name + "_pca64"] = pca64(arr)
    cases = [(c, "color") for c in CLASSES] + [(c, ax) for c in CLASSES for ax in e18.axes_of(c)]
    names = list(reps)
    lines = [f"Sonda de rasgos, k={K}, leave-object-out dentro de la clase, coseno. Acierto balanceado (%).",
             f"{'eje · clase':<16}{'azar':>6}" + "".join(f"{n:>18}" for n in names)]
    res = {}
    for cls, axis in cases:
        row = {n: probe(reps[n], cls, axis, index) for n in names}
        if row[names[0]] is None:
            continue
        nvals = len(row[names[0]])
        res[f"{axis}|{cls}"] = row
        lines.append(f"{axis + ' · ' + cls:<16}{100 / nvals:>6.0f}" +
                     "".join(f"{100 * np.mean(list(row[n].values())):>18.1f}" for n in names))
    lines.append("\nPor valor (acierto del valor minoritario entre paréntesis en el detalle JSON).")
    text = "\n".join(lines)
    (OUT / "sonda_rasgos_resumen.txt").write_text(text, encoding="utf-8")
    (OUT / "sonda_rasgos.json").write_text(json.dumps(res, indent=1))
    print(text)


if __name__ == "__main__":
    if "--variantes" in sys.argv:
        print(resnet_variant_latents())
    else:
        main()
