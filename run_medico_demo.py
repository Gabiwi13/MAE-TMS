"""
Demo médico: el sistema EAM-TMS sobre MedMNIST+ (128 px, CC BY 4.0, Zenodo 10519652).

Jerarquía (exp19: cada nivel con su propia percepción):
  nivel 1  modalidad: rx_torax, tc_abdomen, dermatoscopia, us_mama.
           Encoder: ResNet18 de ImageNet congelado + PCA a 64 ajustada en train.
  nivel 2  hallazgo u órgano como dominio, uno por modalidad.
           Encoder: ResNet18 de ImageNet ajustado con la clasificación del hallazgo
           (muestreo balanceado por clase); el latente es la capa de 64.
Fuera de distribución: retinamnist (fondo de ojo) nunca se registra.
Transferencia: pneumoniamnist (tórax pediátrico de otro hospital).

Memoria con el protocolo oficial: 200 de llenado + 128 de fase A por agente,
16 variantes, Q = 32, umbral de energía, xi = 0, entrada por un no especialista.
Comparaciones sobre los mismos latentes: kNN (k = 5) y, en el nivel 2, la
cabeza lineal entrenada.

Uso:
  python run_medico_demo.py            # todo, con cachés
  python run_medico_demo.py --report-only
"""
import argparse
import contextlib
import io
import json
import os
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

import stage6_interaction as s6  # noqa: E402
from stage5_fill import augment_variants, quantize_latent_global  # noqa: E402
from stage7_bidirectional import recognize_gated_right  # noqa: E402

SMOKE = os.environ.get("DEMO_SMOKE") == "1"     # prueba corta de punta a punta
DATA = ROOT / "data" / "medmnist"
# Completo: todo el train (60 % llenado, 40 % fase A), todo el test, PCA y épocas completas.
FULL = os.environ.get("DEMO_FULL") == "1"
# Balanceado: como el completo, pero cada agente registra N = max(328, clase más chica del nivel).
BAL = os.environ.get("DEMO_BAL") == "1"
FULL = FULL or BAL
OUT = ROOT / "results" / ("medico_prueba" if SMOKE else "medico_balanceado" if BAL else
                          "medico_completo" if FULL else "medico")
CACHE = OUT / "cache"            # fuera de git
DEV = "cuda" if torch.cuda.is_available() else "cpu"
N_FILL, N_A, N_TEST_MAX, Q, K_NN = (20, 10, 15, 32, 5) if SMOKE else (200, 128, 300, 32, 5)
SEED = 42
ENERGY_MARGIN = 0.1

CHEST = ["atelectasis", "cardiomegaly", "effusion", "infiltration", "mass", "nodule", "pneumonia",
         "pneumothorax", "consolidation", "edema", "emphysema", "fibrosis", "pleural", "hernia"]
ORGAN = ["bladder", "femur-left", "femur-right", "heart", "kidney-left", "kidney-right", "liver",
         "lung-left", "lung-right", "pancreas", "spleen"]
DERMA = ["actinic-keratosis", "basal-cell-carcinoma", "benign-keratosis", "dermatofibroma",
         "melanoma", "melanocytic-nevus", "vascular-lesion"]
BREAST = ["malignant", "normal-benign"]
MODALITIES = {"rx_torax": "chestmnist", "tc_abdomen": "organamnist",
              "dermatoscopia": "dermamnist", "us_mama": "breastmnist"}
TF = transforms.Compose([transforms.ToTensor(),
                         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
_DATA = {}


def data(name):
    if name not in _DATA:
        z = np.load(DATA / f"{name}_128.npz", allow_pickle=False)
        _DATA[name] = {s: (z[f"{s}_images"], z[f"{s}_labels"]) for s in ("train", "val", "test")}
    return _DATA[name]


def to_pil(a):
    a = np.asarray(a, dtype=np.uint8)
    return Image.fromarray(a).convert("RGB")


def level2_agents(mod):
    """(nombre, selector de etiquetas) por agente del nivel 2. En tórax, solo
    imágenes de un único hallazgo (o ninguno) y hallazgos con >= N_FILL en train."""
    name = MODALITIES[mod]
    if mod == "rx_torax":
        y = data(name)["train"][1]
        agents = [("sin-hallazgo", lambda l: l.sum(1) == 0)]
        for k, f in enumerate(CHEST):
            sel = (lambda kk: (lambda l: (l.sum(1) == 1) & (l[:, kk] == 1)))(k)
            if sel(y).sum() >= N_FILL:
                agents.append((f, sel))
        return agents
    names = {"tc_abdomen": ORGAN, "dermatoscopia": DERMA, "us_mama": BREAST}[mod]
    return [(n, (lambda kk: (lambda l: l[:, 0] == kk))(k)) for k, n in enumerate(names)]


def level1_agents():
    return [(mod, (lambda l: np.ones(len(l), dtype=bool))) for mod in MODALITIES]


# ---------- percepción ----------

class Backbone(nn.Module):
    def __init__(self, n_classes=None):
        super().__init__()
        net = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
        self.features = nn.Sequential(*list(net.children())[:-1])
        self.fc = nn.Linear(512, 64)
        self.head = nn.Linear(64, n_classes) if n_classes else None

    def latent(self, x):
        return self.fc(self.features(x).flatten(1))


def frozen_level1():
    path = CACHE / "encoder_nivel1.pt"
    enc = Backbone().to(DEV).eval()
    if path.exists():
        enc.load_state_dict(torch.load(path, map_location=DEV))
        return enc
    rng = np.random.RandomState(SEED)
    feats = []
    for mod, name in MODALITIES.items():
        x = data(name)["train"][0]
        idx = rng.permutation(len(x))[:200 if SMOKE else len(x) if FULL else 2000]
        feats.append(_features(enc, [to_pil(x[i]) for i in idx]))
    X = np.concatenate(feats).astype(np.float64)
    mu = X.mean(0)
    _u, _s, vt = np.linalg.svd(X - mu, full_matrices=False)
    with torch.no_grad():
        enc.fc.weight.copy_(torch.tensor(vt[:64], dtype=torch.float32))
        enc.fc.bias.copy_(torch.tensor(-vt[:64] @ mu, dtype=torch.float32))
    CACHE.mkdir(parents=True, exist_ok=True)
    torch.save(enc.state_dict(), path)
    return enc


def _features(enc, imgs):
    out = []
    with torch.no_grad():
        for i in range(0, len(imgs), 128):
            out.append(enc.features(torch.stack([TF(im) for im in imgs[i:i + 128]]).to(DEV)).flatten(1).cpu().numpy())
    return np.concatenate(out)


def trained_level2(mod, epochs=1 if SMOKE else 8):
    """ResNet18 de ImageNet ajustado a los hallazgos de la modalidad."""
    path = CACHE / f"encoder_{mod}.pt"
    agents = level2_agents(mod)
    enc = Backbone(len(agents)).to(DEV)
    log = {}
    if path.exists():
        enc.load_state_dict(torch.load(path, map_location=DEV))
        return enc.eval(), json.loads((CACHE / f"encoder_{mod}.json").read_text())
    torch.manual_seed(SEED)
    x, y = data(MODALITIES[mod])["train"]
    idx, lab = [], []
    for k, (_n, sel) in enumerate(agents):
        ii = np.where(sel(y))[0]
        idx += ii.tolist()
        lab += [k] * len(ii)
    idx, lab = np.array(idx), np.array(lab)
    counts = np.bincount(lab)
    w = 1.0 / counts[lab]
    g = torch.Generator().manual_seed(SEED)
    aug = transforms.Compose([transforms.RandomHorizontalFlip(), transforms.RandomRotation(10)])
    opt = torch.optim.Adam(enc.parameters(), lr=1e-4)
    ce = nn.CrossEntropyLoss()
    steps = 5 if SMOKE else len(idx) // 64 if FULL else min(len(idx), 20000) // 64
    t0 = time.time()
    for ep in range(epochs):
        enc.train()
        pick = torch.multinomial(torch.tensor(w), steps * 64, replacement=True, generator=g).numpy()
        tot = 0.0
        for s in range(steps):
            b = pick[s * 64:(s + 1) * 64]
            xb = torch.stack([TF(aug(to_pil(x[idx[i]]))) for i in b]).to(DEV)
            yb = torch.tensor(lab[b]).to(DEV)
            opt.zero_grad()
            loss = ce(enc.head(enc.latent(xb)), yb)
            loss.backward()
            opt.step()
            tot += loss.item()
        print(f"  {mod} época {ep + 1}/{epochs} pérdida {tot / steps:.3f} ({time.time() - t0:.0f} s)", flush=True)
    enc.eval()
    log = {"epocas": epochs, "pasos_por_epoca": steps, "n_train": int(len(idx)),
           "conteo_por_clase": counts.tolist(), "segundos": round(time.time() - t0)}
    torch.save(enc.state_dict(), path)
    (CACHE / f"encoder_{mod}.json").write_text(json.dumps(log))
    return enc, log


def latents(enc, imgs, variants=False):
    """(n, 64) o (n, 16, 64) si variants."""
    out = []
    with torch.no_grad():
        for i in range(0, len(imgs), 32 if variants else 256):
            chunk = imgs[i:i + (32 if variants else 256)]
            if variants:
                vs = [v for im in chunk for v in augment_variants(im)]
                z = enc.latent(torch.stack([TF(v) for v in vs]).to(DEV)).cpu().numpy()
                out.append(z.reshape(len(chunk), 16, 64))
            else:
                out.append(enc.latent(torch.stack([TF(im) for im in chunk]).to(DEV)).cpu().numpy())
    return np.concatenate(out)


# ---------- un nivel del sistema ----------

class Level:
    """Agentes, directorios perspectivales y ruteo oficial sobre una lista de dominios."""

    def __init__(self, tag, names, enc, fill, phase_a):
        self.tag, self.names, self.enc = tag, names, enc
        zs = np.concatenate([fill[n][:, 0] for n in names])
        lo, hi = zs.min(0), zs.max(0)
        pad = 0.1 * (hi - lo)
        self.g = (lo - pad, hi + pad)
        self.tau = float(np.linalg.norm(zs, axis=1).min() * (1 - ENERGY_MARGIN))
        self.knn_X = zs / np.linalg.norm(zs, axis=1, keepdims=True)
        self.knn_y = np.concatenate([[k] * len(fill[n]) for k, n in enumerate(names)])
        with self.ctx():
            self.agents = {n: s6.Agent(n, None) for n in names}
            self.tme = s6.TME()
            for n in names:
                for z in fill[n].reshape(-1, 64):
                    self.agents[n].mem_dom_R.register(self.q(z))
            self.form = self._phase_a(phase_a)

    @contextlib.contextmanager
    def ctx(self):
        old = s6.AGENT_LIST
        s6.AGENT_LIST = self.names
        try:
            yield
        finally:
            s6.AGENT_LIST = old

    def q(self, z):
        return quantize_latent_global(np.asarray(z, dtype=np.float32), *self.g, Q)

    def _phase_a(self, phase_a):
        rng = np.random.RandomState(SEED)
        form = {"registradas": 0, "rechazadas": 0, "sin_energia": 0, "acierto": 0}
        for j in range(max(len(v) for v in phase_a.values())):
            for k, n in enumerate(self.names):
                if j >= len(phase_a[n]):
                    continue
                zv = phase_a[n][j]
                if np.linalg.norm(zv[0]) < self.tau:
                    form["sin_energia"] += 1
                    continue
                scores = {m: recognize_gated_right(self.agents[m], self.q(zv[0])) for m in self.names}
                if sum(scores.values()) == 0:
                    form["rechazadas"] += 1
                    continue
                w = max(scores, key=scores.get)
                widx = self.names.index(w)
                form["registradas"] += 1
                form["acierto"] += int(w == n)
                entry = self.names[int(rng.randint(len(self.names)))]
                with contextlib.redirect_stdout(io.StringIO()):
                    for z in zv:
                        s6.register_transaction(entry, widx, self.agents, self.tme, self.q(z), "image")
        return form

    def route(self, z, entry_idx):
        """Devuelve (destino o None, motivo)."""
        if np.linalg.norm(z) < self.tau:
            return None, "sin_energia"
        with self.ctx(), contextlib.redirect_stdout(io.StringIO()):
            d, *_ = s6.route_transactive(self.names[(entry_idx + 1) % len(self.names)], self.agents,
                                         self.q(z), modality="image", xi=0)
        return (self.names[d], "ok") if d >= 0 else (None, "rechazo")

    def knn(self, z):
        z = z / np.linalg.norm(z)
        nn_ = np.argsort(-(self.knn_X @ z))[:K_NN]
        return self.names[np.bincount(self.knn_y[nn_]).argmax()]


def pools(agents, name, enc, tag):
    """Llenado y fase A (train) con variantes; test sin variantes. Cacheado."""
    path = CACHE / f"pool_{tag}.npz"
    if path.exists():
        z = np.load(path, allow_pickle=False)
        names = [a for a, _ in agents]
        return ({n: z[f"fill_{n}"] for n in names}, {n: z[f"a_{n}"] for n in names},
                {n: z[f"test_{n}"] for n in names}, {n: z[f"testidx_{n}"] for n in names})
    rng = np.random.RandomState(SEED)
    fill, pa, test, tidx = {}, {}, {}, {}
    if BAL:
        sizes = [int(sel(data(name(n) if callable(name) else name)["train"][1]).sum()) for n, sel in agents]
        n_bal = max(N_FILL + N_A, min(sizes))
        print(f"  {tag}: N balanceado por agente {n_bal} (clase más chica {min(sizes)})", flush=True)
    for n, sel in agents:
        src = name(n) if callable(name) else name
        xt, yt = data(src)["train"]
        ii = rng.permutation(np.where(sel(yt))[0])
        # Clases chicas: 60 % al llenado y 40 % a la fase A, para que el agente
        # también gane percepciones y entre a los directorios.
        if BAL:
            ii = ii[:n_bal]
        nf = N_FILL if (len(ii) >= N_FILL + N_A and not FULL) else int(np.ceil(0.6 * len(ii)))
        na = len(ii) - nf if FULL else N_A
        fill[n] = latents(enc, [to_pil(xt[i]) for i in ii[:nf]], variants=True)
        pa[n] = latents(enc, [to_pil(xt[i]) for i in ii[nf:nf + na]], variants=True)
        xs, ys = data(src)["test"]
        jj = rng.permutation(np.where(sel(ys))[0])[:None if FULL else N_TEST_MAX]
        test[n] = latents(enc, [to_pil(xs[i]) for i in jj])
        tidx[n] = jj
        print(f"  {tag}/{n}: llenado {len(fill[n])}, fase A {len(pa[n])}, test {len(test[n])}", flush=True)
    np.savez(path, **{f"fill_{n}": v for n, v in fill.items()}, **{f"a_{n}": v for n, v in pa.items()},
             **{f"test_{n}": v for n, v in test.items()}, **{f"testidx_{n}": v for n, v in tidx.items()})
    return fill, pa, test, tidx


def evaluate(level, test, head=None, enc=None, raw=None):
    rows = []
    for k, n in enumerate(level.names):
        for j, z in enumerate(test[n]):
            d, why = level.route(z, k)
            rows.append({"nivel": level.tag, "verdad": n, "destino": d, "motivo": why, "knn": level.knn(z)})
    if head is not None:
        with torch.no_grad():
            i = 0
            for n in level.names:
                logits = head(torch.tensor(test[n], dtype=torch.float32).to(DEV)).cpu().numpy()
                for lg in logits:
                    rows[i]["cabeza"] = level.names[int(lg.argmax())]
                    i += 1
    return rows


def summarize(rows, names, title):
    lines = [f"\n[{title}] imágenes de test {len(rows)}"]
    n = len(rows)
    ok = sum(r["destino"] == r["verdad"] for r in rows)
    rej = sum(r["destino"] is None for r in rows)
    fal = n - ok - rej
    acc_ans = ok / max(n - rej, 1)
    bal = np.mean([np.mean([r["destino"] == c for r in rows if r["verdad"] == c]) for c in names])
    lines.append(f"  memoria: acierto {100 * ok / n:5.1f} % · rechazo {100 * rej / n:5.1f} % · "
                 f"falso {100 * fal / n:5.1f} % · acierto de lo respondido {100 * acc_ans:5.1f} % · balanceado {100 * bal:5.1f} %")
    for key in ("knn", "cabeza"):
        if key in rows[0]:
            a = sum(r[key] == r["verdad"] for r in rows)
            b = np.mean([np.mean([r[key] == c for r in rows if r["verdad"] == c]) for c in names])
            lines.append(f"  {key:<7}: acierto {100 * a / n:5.1f} % (sin abstención) · balanceado {100 * b:5.1f} %")
    lines.append("  por dominio (memoria acierto / rechazo / falso · knn · cabeza):")
    for c in names:
        rs = [r for r in rows if r["verdad"] == c]
        a = sum(r["destino"] == c for r in rs)
        rj = sum(r["destino"] is None for r in rs)
        extra = " · ".join(f"{sum(r[k] == c for r in rs)}" for k in ("knn", "cabeza") if k in rs[0])
        lines.append(f"    {c:<22} n={len(rs):>3}  {a:>3} / {rj:>3} / {len(rs) - a - rj:>3}  ·  {extra}")
    conf = {}
    for r in rows:
        if r["destino"] and r["destino"] != r["verdad"]:
            conf[(r["verdad"], r["destino"])] = conf.get((r["verdad"], r["destino"]), 0) + 1
    lines.append("  falsos más frecuentes: " + ", ".join(
        f"{a}->{b} {c}" for (a, b), c in sorted(conf.items(), key=lambda x: -x[1])[:8]))
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    raw_path = OUT / "filas.json"
    if not args.report_only:
        t0 = time.time()
        res = {"nivel1": [], "nivel2": {}, "ood": [], "transferencia": [], "jerarquia": [], "formacion": {},
               "encoders": {}}
        # nivel 1
        enc1 = frozen_level1()
        a1 = level1_agents()
        f1, p1, t1, _ = pools(a1, lambda n: MODALITIES[n], enc1, "nivel1")
        L1 = Level("nivel1", [n for n, _ in a1], enc1, f1, p1)
        res["formacion"]["nivel1"] = L1.form
        res["nivel1"] = evaluate(L1, t1)
        print(f"nivel 1 listo ({time.time() - t0:.0f} s)", flush=True)
        # fuera de distribución y transferencia, en el nivel 1
        rng = np.random.RandomState(SEED)
        # Fuera de distribución: en el completo, las tres particiones (nunca se registran).
        xr = np.concatenate([data("retinamnist")[s][0] for s in (("train", "val", "test") if FULL else ("test",))])
        for z in latents(enc1, [to_pil(xr[i]) for i in rng.permutation(len(xr))[:None if FULL else N_TEST_MAX]]):
            d, why = L1.route(z, 0)
            res["ood"].append({"destino": d, "motivo": why, "knn": L1.knn(z)})
        parts = ("train", "val", "test") if FULL else ("test",)
        xp = np.concatenate([data("pneumoniamnist")[s][0] for s in parts])
        yp = np.concatenate([data("pneumoniamnist")[s][1] for s in parts])
        pidx = rng.permutation(len(xp))[:None if FULL else N_TEST_MAX]
        zp1 = latents(enc1, [to_pil(xp[i]) for i in pidx])
        # nivel 2 por modalidad
        levels2 = {}
        for mod in MODALITIES:
            enc2, log = trained_level2(mod)
            res["encoders"][mod] = log
            a2 = level2_agents(mod)
            f2, p2, t2, _ = pools(a2, MODALITIES[mod], enc2, f"nivel2_{mod}")
            L2 = Level(f"nivel2_{mod}", [n for n, _ in a2], enc2, f2, p2)
            levels2[mod] = L2
            res["formacion"][mod] = L2.form
            res["nivel2"][mod] = evaluate(L2, t2, head=enc2.head, enc=enc2)
            # jerarquía: solo pasa al nivel 2 lo que el nivel 1 mandó a esta modalidad
            l1_ok = [r["destino"] == mod for r in res["nivel1"] if r["verdad"] == mod]
            res["jerarquia"].append({"modalidad": mod, "n": len(l1_ok), "nivel1_ok": int(sum(l1_ok))})
            print(f"nivel 2 {mod} listo ({time.time() - t0:.0f} s)", flush=True)
        # transferencia: pneumoniamnist (otro hospital) por la jerarquía completa
        enc2 = trained_level2("rx_torax")[0]
        zp2 = latents(enc2, [to_pil(xp[i]) for i in pidx])
        for z1, z2, lab in zip(zp1, zp2, yp[pidx, 0]):
            d1, _ = L1.route(z1, 0)
            d2 = levels2["rx_torax"].route(z2, 0)[0] if d1 == "rx_torax" else None
            res["transferencia"].append({"neumonia": int(lab), "nivel1": d1, "nivel2": d2,
                                         "knn2": levels2["rx_torax"].knn(z2)})
        res["segundos"] = round(time.time() - t0)
        raw_path.write_text(json.dumps(res, ensure_ascii=False))
    report(json.loads(raw_path.read_text()))


def report(res):
    lines = ["Demo médico EAM-TMS sobre MedMNIST+ 128 px. Splits oficiales; " +
             ("train balanceado: N = max(328, clase más chica) por agente (60 % llenado, 40 % fase A) y todo el test." if BAL else
              "todo el train (60 % llenado, 40 % fase A) y todo el test." if FULL else "test hasta 300 por dominio.")]
    lines.append(f"Formación de directorios (fase A): {json.dumps(res['formacion'], ensure_ascii=False)}")
    lines += summarize(res["nivel1"], list(MODALITIES), "nivel 1 · modalidad")
    for mod, rows in res["nivel2"].items():
        names = list(dict.fromkeys(r["verdad"] for r in rows))
        lines += summarize(rows, names, f"nivel 2 · {mod} (hallazgo u órgano como dominio)")
        lines.append(f"  encoder: {json.dumps(res['encoders'][mod])}")
    ood = res["ood"]
    from collections import Counter
    lines.append(f"\n[fuera de distribución · retinamnist, nunca registrada] n={len(ood)}: "
                 f"rechazo {100 * sum(r['destino'] is None for r in ood) / len(ood):.1f} % · "
                 f"destinos {dict(Counter(r['destino'] for r in ood))} · kNN (siempre responde) {dict(Counter(r['knn'] for r in ood))}")
    tr = res["transferencia"]
    lines.append(f"\n[transferencia · pneumoniamnist, otro hospital] n={len(tr)}: nivel 1 {dict(Counter(r['nivel1'] for r in tr))}")
    for lab, name in ((0, "normal"), (1, "neumonía")):
        rs = [r for r in tr if r["neumonia"] == lab]
        lines.append(f"  {name} (n={len(rs)}): nivel 2 {dict(Counter(r['nivel2'] for r in rs))} · kNN nivel 2 {dict(Counter(r['knn2'] for r in rs))}")
    lines.append("\n[jerarquía] fracción que el nivel 1 entrega a la modalidad correcta: " +
                 ", ".join(f"{j['modalidad']} {j['nivel1_ok']}/{j['n']}" for j in res["jerarquia"]))
    lines.append(f"\nTiempo total: {res.get('segundos', 0) / 60:.0f} min")
    text = "\n".join(lines)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
