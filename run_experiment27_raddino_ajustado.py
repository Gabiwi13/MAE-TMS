"""
Experimento 27: RAD-DINO ajustado a los hallazgos de tórax, a 224 px nativos.
Diseño y predicciones en propuesta_exp27_raddino_ajustado.md.

Mismos 14 dominios y misma selección de imágenes que la corrida balanceada
(semillas y reglas iguales; ChestMNIST a 224 px tiene las mismas etiquetas).
Cuatro percepciones, cada una entrega un latente de 64:
  A  ResNet18 de ImageNet ajustado a 224 px
  B  RAD-DINO congelado, PCA a 64
  C  RAD-DINO ajustado (backbone 1e-5, capa de 64 y cabeza 1e-3, AdamW)
  D  RAD-DINO congelado con capa de 64 y cabeza entrenadas (linear probe)
A, C y D: entropía cruzada con muestreo balanceado, 5 épocas de 20 000, semilla 42,
época elegida por balanceado en validación.

Uso: python run_experiment27_raddino_ajustado.py [--smoke]
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import run_medico_demo as demo  # noqa: E402
import run_experiment26_fundacion as e26  # noqa: E402
from stage5_fill import augment_variants  # noqa: E402

OUT = ROOT / "results" / "experimento27"
CACHE = OUT / "cache"            # fuera de git
NPZ = ROOT / "data" / "medmnist" / "chestmnist_224.npz"
NPY = ROOT / "data" / "medmnist" / "chest224"
SEED, N_MIN = 42, 328
EPOCHS, PER_EPOCH, BS = 5, 20000, 32
SMOKE = False
IMNET = transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])


# ---------- datos a 224 con mapeo de memoria ----------

def extract():
    NPY.mkdir(parents=True, exist_ok=True)
    if (NPY / "test_labels.npy").exists():
        return
    z = np.load(NPZ, allow_pickle=False)
    for s in ("train", "val", "test"):
        for k in ("images", "labels"):
            np.save(NPY / f"{s}_{k}.npy", z[f"{s}_{k}"])
            print(f"  extraído {s}_{k}", flush=True)


def split(s):
    return (np.load(NPY / f"{s}_images.npy", mmap_mode="r"), np.load(NPY / f"{s}_labels.npy"))


def pil(a):
    return Image.fromarray(np.asarray(a, dtype=np.uint8)).convert("RGB")


def selection():
    """La misma selección que run_medico_demo.pools en modo balanceado."""
    agents = demo.level2_agents("rx_torax")
    for s in ("train", "val", "test"):
        assert np.array_equal(split(s)[1], demo.data("chestmnist")[s][1]), "etiquetas distintas a 128 px"
    rng = np.random.RandomState(SEED)
    yt = split("train")[1]
    sizes = [int(sel(yt).sum()) for _n, sel in agents]
    n_bal = max(N_MIN, min(sizes))
    out = {}
    for n, sel in agents:
        ii = rng.permutation(np.where(sel(yt))[0])[:n_bal]
        nf = int(np.ceil(0.6 * len(ii)))
        jj = rng.permutation(np.where(sel(split("test")[1]))[0])
        out[n] = {"fill": ii[:nf], "a": ii[nf:], "test": jj, "val": np.where(sel(split("val")[1]))[0]}
    return [n for n, _ in agents], agents, out


# ---------- percepciones ----------

class ResNetEnc(nn.Module):
    def __init__(self, k):
        super().__init__()
        net = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        self.features = nn.Sequential(*list(net.children())[:-1])
        self.fc, self.head = nn.Linear(512, 64), nn.Linear(64, k)
        self.tf = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor(), IMNET])

    def latent(self, x):
        return self.fc(self.features(x).flatten(1))


class RadEnc(nn.Module):
    def __init__(self, k, freeze):
        super().__init__()
        rd = e26.RadDINO()
        self.backbone, self.freeze = rd.model, freeze
        mean, std = rd.tf.transforms[-1].mean, rd.tf.transforms[-1].std
        self.tf = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor(), transforms.Normalize(mean, std)])
        self.fc, self.head = nn.Linear(768, 64), nn.Linear(64, k)
        if freeze:
            for p in self.backbone.parameters():
                p.requires_grad = False

    def cls(self, x):
        return self.backbone(pixel_values=x).last_hidden_state[:, 0]

    def latent(self, x):
        return self.fc(self.cls(x))


def train(enc, idx, lab, val_idx, val_lab, lr_backbone, tag):
    path = CACHE / f"enc_{tag}.pt"
    if path.exists():
        enc.load_state_dict(torch.load(path, map_location=demo.DEV))
        return enc.eval(), json.loads((CACHE / f"enc_{tag}.json").read_text())
    torch.manual_seed(SEED)
    x, _ = split("train")
    xv, _ = split("val")
    heads = list(enc.fc.parameters()) + list(enc.head.parameters())
    groups = [{"params": heads, "lr": 1e-3}]
    back = [p for n, p in enc.named_parameters() if p.requires_grad and not n.startswith(("fc.", "head."))]
    if back:
        groups.append({"params": back, "lr": lr_backbone})
    opt = torch.optim.AdamW(groups, weight_decay=0.01)
    scaler = torch.amp.GradScaler()
    ce = nn.CrossEntropyLoss()
    aug = transforms.Compose([transforms.RandomHorizontalFlip(), transforms.RandomRotation(10)])
    w = 1.0 / np.bincount(lab)[lab]
    g = torch.Generator().manual_seed(SEED)
    epochs, per = (1, 256) if SMOKE else (EPOCHS, PER_EPOCH)
    best, log = (-1, None), []
    t0 = time.time()
    for ep in range(epochs):
        enc.train()
        pick = torch.multinomial(torch.tensor(w), per, replacement=True, generator=g).numpy()
        for s in range(0, per, BS):
            b = pick[s:s + BS]
            xb = torch.stack([enc.tf(aug(pil(x[idx[i]]))) for i in b]).to(demo.DEV)
            yb = torch.tensor(lab[b]).to(demo.DEV)
            opt.zero_grad()
            with torch.autocast("cuda", dtype=torch.float16):
                loss = ce(enc.head(enc.latent(xb)), yb)
            scaler.scale(loss).backward()
            scaler.step(opt)
            scaler.update()
        enc.eval()
        pv = predict_head(enc, [pil(xv[i]) for i in val_idx])
        bal = float(np.mean([(pv[val_lab == k] == k).mean() for k in np.unique(val_lab)]))
        log.append({"epoca": ep + 1, "balanceado_val": bal, "segundos": round(time.time() - t0)})
        print(f"  {tag} época {ep + 1}: balanceado en validación {100 * bal:.1f} ({time.time() - t0:.0f} s)", flush=True)
        if bal > best[0]:
            best = (bal, {k: v.detach().clone() for k, v in enc.state_dict().items()})
    enc.load_state_dict(best[1])
    CACHE.mkdir(parents=True, exist_ok=True)
    torch.save(enc.state_dict(), path)
    (CACHE / f"enc_{tag}.json").write_text(json.dumps(log))
    return enc.eval(), log


def run_batches(enc, imgs, fn, variants=False):
    out = []
    step = max(1, BS // 16) if variants else BS * 2
    with torch.no_grad(), torch.autocast("cuda", dtype=torch.float16):
        for i in range(0, len(imgs), step):
            chunk = imgs[i:i + step]
            vs = [v for im in chunk for v in augment_variants(im)] if variants else chunk
            f = fn(torch.stack([enc.tf(v) for v in vs]).to(demo.DEV)).float().cpu().numpy()
            out.append(f.reshape(len(chunk), 16, -1) if variants else f)
    return np.concatenate(out)


def predict_head(enc, imgs):
    return run_batches(enc, imgs, lambda t: enc.head(enc.latent(t))).argmax(1)


def pool_latents(enc, sel, names, fn, tag):
    path = CACHE / f"pool_{tag}.npz"
    if path.exists():
        z = np.load(path)
        return {k: z[k] for k in z.files}
    x, _ = split("train")
    xs, _ = split("test")
    xv, _ = split("val")
    out = {}
    for n in names:
        s = sel[n]
        cap = 8 if SMOKE else None
        out[f"fill_{n}"] = run_batches(enc, [pil(x[i]) for i in s["fill"][:cap]], fn, variants=True)
        out[f"a_{n}"] = run_batches(enc, [pil(x[i]) for i in s["a"][:cap]], fn, variants=True)
        out[f"test_{n}"] = run_batches(enc, [pil(xs[i]) for i in s["test"][:(20 if SMOKE else None)]], fn)
        out[f"testidx_{n}"] = s["test"][:(20 if SMOKE else None)]
        out[f"val_{n}"] = run_batches(enc, [pil(xv[i]) for i in s["val"][:(20 if SMOKE else None)]], fn)
    np.savez(path, **out)
    return out


def auroc_per_finding(enc, names):
    """AUROC por hallazgo de la cabeza, sobre el test multi-etiqueta completo."""
    xs, ys = split("test")
    idx = np.arange(len(xs))[:(200 if SMOKE else None)]
    logits = run_batches(enc, [pil(xs[i]) for i in idx], lambda t: enc.head(enc.latent(t)))
    P = np.exp(logits - logits.max(1, keepdims=True))
    P /= P.sum(1, keepdims=True)
    from sklearn.metrics import roc_auc_score
    out = {}
    for k, n in enumerate(names):
        if n in demo.CHEST:
            y = ys[idx, demo.CHEST.index(n)]
            if 0 < y.sum() < len(y):
                out[n] = float(roc_auc_score(y, P[:, k]))
    return out


def main():
    global SMOKE
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    SMOKE = ap.parse_args().smoke
    global OUT, CACHE
    if SMOKE:
        OUT = ROOT / "results" / "experimento27_prueba"
        CACHE = OUT / "cache"
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    extract()
    names, agents, sel = selection()
    K = len(names)
    tr_idx = np.concatenate([np.where(s(split("train")[1]))[0] for _n, s in agents])
    tr_lab = np.concatenate([[k] * int(s(split("train")[1]).sum()) for k, (_n, s) in enumerate(agents)])
    v_idx = np.concatenate([sel[n]["val"] for n in names])
    v_lab = np.concatenate([[k] * len(sel[n]["val"]) for k, n in enumerate(names)])
    if SMOKE:
        v_idx, v_lab = v_idx[::50], v_lab[::50]
    res = {}
    plan = [
        ("A_resnet_ajustado", lambda: ResNetEnc(K), 1e-4, True),
        ("C_raddino_ajustado", lambda: RadEnc(K, False), 1e-5, True),
        ("D_raddino_probe", lambda: RadEnc(K, True), 0.0, True),
        ("B_raddino_congelado", lambda: RadEnc(K, True), 0.0, False),
    ]
    for tag, make, lr, trained in plan:
        enc = make().to(demo.DEV)
        log = None
        if trained:
            enc, log = train(enc, tr_idx, tr_lab, v_idx, v_lab, lr, tag)
            fn, proj = enc.latent, (lambda A: np.asarray(A, dtype=np.float32))
            raw = pool_latents(enc, sel, names, fn, tag)
        else:
            raw = pool_latents(enc.eval(), sel, names, enc.cls, tag)
            proj = e26.pca64(raw, names)
        r, *_ = e26.evaluate_level(names, raw, proj)
        r["log"] = log
        if trained:
            r["auroc_cabeza"] = auroc_per_finding(enc, names)
        res[tag] = r
        (OUT / "resultados.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
        print(f"{tag} listo ({time.time() - t0:.0f} s)", flush=True)
        del enc
        torch.cuda.empty_cache()
    report(res, time.time() - t0)


def report(res, secs):
    lines = ["Exp27: tórax (14 dominios) a 224 px con cuatro percepciones; latente de 64. Balanceado en test (%)."]
    for tag, r in res.items():
        lines.append(f"\n[{tag}]")
        for m in ("mae", "prototipos", "knn", "logistica"):
            v = r[m]
            lines.append(f"  {m:<12} acierto {100 * v['acierto']:5.1f} · rechazo {100 * v['rechazo']:4.1f} · balanceado {100 * v['balanceado']:5.1f}")
        lines.append(f"  lista MAE: cobertura {100 * r['lista_mae']['cobertura']:.1f}, tamaño {r['lista_mae']['tamano']:.2f}, peor {100 * r['lista_mae']['peor_clase']:.1f}"
                     f" · Mondrian: cobertura {100 * r['mondrian']['cobertura']:.1f}, tamaño {r['mondrian']['tamano']:.2f}, peor {100 * r['mondrian']['peor_clase']:.1f}")
        if r.get("auroc_cabeza"):
            a = r["auroc_cabeza"]
            lines.append(f"  AUROC por hallazgo de la cabeza (test multi-etiqueta): media {np.mean(list(a.values())):.3f} · "
                         + ", ".join(f"{k} {v:.2f}" for k, v in a.items()))
        if r.get("log"):
            lines.append("  validación por época: " + ", ".join(f"{100 * e['balanceado_val']:.1f}" for e in r["log"]))
    lines.append(f"\nTiempo: {secs / 60:.0f} min")
    text = "\n".join(lines)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
