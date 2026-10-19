"""
Experimento 26: el sistema médico con modelos de fundación. Diseño y
predicciones en propuesta_exp26_fundacion.md.

Misma selección de imágenes que la corrida balanceada (mismas semillas y reglas);
cambia la percepción: BiomedCLIP (torre visual) para el índice de modalidad y para
órganos, piel y mama; RAD-DINO para tórax (también BiomedCLIP en tórax, para
comparar). PCA a 64 por nivel, ajustada con las originales del llenado.

Uso: python run_experiment26_fundacion.py
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torchvision import transforms

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import run_medico_demo as demo  # noqa: E402
from stage5_fill import augment_variants  # noqa: E402

OUT = ROOT / "results" / "experimento26"
CACHE = OUT / "cache"            # fuera de git
HF = Path.home() / ".cache" / "huggingface" / "hub"
SEED = 42
N_MIN = 328


# ---------- percepción ----------

class BiomedCLIPVisual(torch.nn.Module):
    def __init__(self):
        super().__init__()
        import timm
        snap = next((HF / "models--microsoft--BiomedCLIP-PubMedBERT_256-vit_base_patch16_224" / "snapshots").iterdir())
        sd = torch.load(snap / "open_clip_pytorch_model.bin", map_location="cpu", weights_only=True)
        self.trunk = timm.create_model("vit_base_patch16_224", pretrained=False, num_classes=0)
        self.trunk.load_state_dict({k[len("visual.trunk."):]: v for k, v in sd.items() if k.startswith("visual.trunk.")})
        self.proj = torch.nn.Linear(768, 512, bias=False)
        self.proj.weight.data = sd["visual.head.proj.weight"]
        self.tf = transforms.Compose([
            transforms.Resize(224, interpolation=transforms.InterpolationMode.BICUBIC),
            transforms.ToTensor(),
            transforms.Normalize([0.48145466, 0.4578275, 0.40821073], [0.26862954, 0.26130258, 0.27577711])])

    def forward(self, x):
        return self.proj(self.trunk(x))


class RadDINO(torch.nn.Module):
    def __init__(self):
        super().__init__()
        from transformers import AutoModel
        snap = next((HF / "models--microsoft--rad-dino" / "snapshots").iterdir())
        cfg = json.loads((snap / "preprocessor_config.json").read_text())
        self.model = AutoModel.from_pretrained(str(snap))
        size = cfg.get("crop_size", {}).get("height", 518)
        self.tf = transforms.Compose([
            transforms.Resize(size, interpolation=transforms.InterpolationMode.BICUBIC),
            transforms.ToTensor(),
            transforms.Normalize(cfg["image_mean"], cfg["image_std"])])

    def forward(self, x):
        return self.model(pixel_values=x).last_hidden_state[:, 0]


_ENC = {}


def encoder(kind):
    if kind not in _ENC:
        _ENC[kind] = (BiomedCLIPVisual() if kind == "biomedclip" else RadDINO()).to(demo.DEV).eval()
    return _ENC[kind]


def feats(kind, imgs, variants=False):
    enc = encoder(kind)
    bs = 32 if kind == "raddino" else 64
    out = []
    with torch.no_grad(), torch.autocast("cuda", dtype=torch.float16, enabled=demo.DEV == "cuda"):
        for i in range(0, len(imgs), bs // (16 if variants else 1) or 1):
            chunk = imgs[i:i + (bs // (16 if variants else 1) or 1)]
            vs = [v for im in chunk for v in augment_variants(im)] if variants else chunk
            f = enc(torch.stack([enc.tf(v) for v in vs]).to(demo.DEV)).float().cpu().numpy()
            out.append(f.reshape(len(chunk), 16, -1) if variants else f)
    return np.concatenate(out) if out else np.zeros((0, 16 if variants else 1, 1))


# ---------- pozos con la selección de la corrida balanceada ----------

def pools(tag, agents, name_of, kind):
    path = CACHE / f"{tag}_{kind}.npz"
    names = [n for n, _ in agents]
    if path.exists():
        z = np.load(path, allow_pickle=False)
        return names, {k: z[k] for k in z.files}
    rng = np.random.RandomState(SEED)
    sizes = [int(sel(demo.data(name_of(n))["train"][1]).sum()) for n, sel in agents]
    n_bal = max(N_MIN, min(sizes))
    out = {}
    t0 = time.time()
    for n, sel in agents:
        src = name_of(n)
        xt, yt = demo.data(src)["train"]
        ii = rng.permutation(np.where(sel(yt))[0])[:n_bal]
        nf = int(np.ceil(0.6 * len(ii)))
        out[f"fill_{n}"] = feats(kind, [demo.to_pil(xt[i]) for i in ii[:nf]], variants=True)
        out[f"a_{n}"] = feats(kind, [demo.to_pil(xt[i]) for i in ii[nf:]], variants=True)
        xs, ys = demo.data(src)["test"]
        jj = rng.permutation(np.where(sel(ys))[0])
        out[f"test_{n}"] = feats(kind, [demo.to_pil(xs[i]) for i in jj])
        out[f"testidx_{n}"] = jj
        xv, yv = demo.data(src)["val"]
        out[f"val_{n}"] = feats(kind, [demo.to_pil(xv[i]) for i in np.where(sel(yv))[0]])
        print(f"  {tag}/{kind}/{n}: llenado {nf}, fase A {len(ii) - nf}, test {len(jj)} ({time.time() - t0:.0f} s)", flush=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    np.savez(path, **out)
    return names, out


def pca64(raw, names):
    X = np.concatenate([raw[f"fill_{n}"][:, 0] for n in names]).astype(np.float64)
    mu = X.mean(0)
    _u, _s, vt = np.linalg.svd(X - mu, full_matrices=False)
    V = vt[:64]
    return lambda A: ((np.asarray(A, dtype=np.float64) - mu) @ V.T).astype(np.float32)


# ---------- sistemas sobre un nivel ----------

def unit(X):
    return X / (np.linalg.norm(X, axis=-1, keepdims=True) + 1e-12)


def evaluate_level(names, raw, proj):
    import run_experiment23_ambiguedad as e23
    from sklearn.linear_model import LogisticRegression
    fill = {n: proj(raw[f"fill_{n}"].reshape(-1, raw[f"fill_{n}"].shape[-1])).reshape(len(raw[f"fill_{n}"]), 16, 64)
            for n in names}
    pa = {n: proj(raw[f"a_{n}"].reshape(-1, raw[f"a_{n}"].shape[-1])).reshape(len(raw[f"a_{n}"]), 16, 64) for n in names}
    test = {n: proj(raw[f"test_{n}"]) for n in names}
    val = {n: proj(raw[f"val_{n}"]) for n in names}
    level = demo.Level("x", names, None, fill, pa)
    K = len(names)
    yt = np.concatenate([[k] * len(test[n]) for k, n in enumerate(names)])
    Zt = np.concatenate([test[n] for n in names])
    # Level.route(z, k) entra por el agente siguiente a k: nunca por el especialista
    mae = np.array([names.index(d) if d is not None else -1
                    for d in (level.route(z, int(k))[0] for z, k in zip(Zt, yt))])
    P = np.stack([unit(fill[n].reshape(-1, 64)).mean(0) for n in names])
    proto = (unit(Zt) @ unit(P).T).argmax(1)
    Pf = np.stack([unit(raw[f"fill_{n}"].reshape(-1, raw[f"fill_{n}"].shape[-1])).mean(0) for n in names])
    Ztf = np.concatenate([raw[f"test_{n}"] for n in names])
    proto_full = (unit(Ztf) @ unit(Pf).T).argmax(1)
    Xf = np.concatenate([fill[n].reshape(-1, 64) for n in names])
    yf = np.concatenate([[k] * (len(fill[n]) * 16) for k, n in enumerate(names)])
    Xn = unit(Xf)
    knn = []
    for i in range(0, len(Zt), 1024):
        nn = np.argsort(-(unit(Zt[i:i + 1024]) @ Xn.T), 1)[:, :5]
        knn.append(np.array([np.bincount(yf[r], minlength=K).argmax() for r in nn]))
    knn = np.concatenate(knn)
    clf = LogisticRegression(max_iter=3000).fit(Xf, yf)
    Pt, Pv = clf.predict_proba(Zt), clf.predict_proba(np.concatenate([val[n] for n in names]))
    yv = np.concatenate([[k] * len(val[n]) for k, n in enumerate(names)])
    S = np.array([[m in e23.content_sets(level, z)[0] for m in names] for z in Zt])
    out = {}
    for key, pred in (("mae", mae), ("prototipos", proto), ("prototipos_completo", proto_full), ("knn", knn),
                      ("logistica", Pt.argmax(1))):
        ok = pred == yt
        out[key] = {"acierto": float(ok.mean()), "rechazo": float((pred == -1).mean()),
                    "balanceado": float(np.mean([ok[yt == k].mean() for k in range(K)]))}
    cov_mae = S[np.arange(len(yt)), yt]
    out["lista_mae"] = {"cobertura": float(cov_mae.mean()), "tamano": float(S.sum(1).mean()),
                        "peor_clase": float(min(cov_mae[yt == k].mean() for k in range(K)))}
    import run_experiment24_mondrian as e24
    a = e24.match_alpha(lambda al: e24.mondrian_sets(Pv, yv, Pt, al, K), cov_mae.mean(), yt)
    M = e24.mondrian_sets(Pv, yv, Pt, a, K)
    cm = M[np.arange(len(yt)), yt]
    out["mondrian"] = {"cobertura": float(cm.mean()), "tamano": float(M.sum(1).mean()),
                       "peor_clase": float(min(cm[yt == k].mean() for k in range(K)))}
    out["por_clase"] = {n: {k: float((v == yt)[yt == i].mean()) for k, v in
                            (("mae", mae), ("prototipos", proto), ("logistica", Pt.argmax(1)))} for i, n in enumerate(names)}
    return out, level, P, proj, mae, proto, yt


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    res = {}
    # nivel 1
    a1 = demo.level1_agents()
    n1, raw1 = pools("nivel1", a1, lambda n: demo.MODALITIES[n], "biomedclip")
    proj1 = pca64(raw1, n1)
    res["nivel1"], L1, P1, _, _, _, _ = evaluate_level(n1, raw1, proj1)
    print(f"nivel 1 listo ({time.time() - t0:.0f} s)", flush=True)
    # nivel 2
    e2e = {}
    for mod in demo.MODALITIES:
        kinds = ["raddino", "biomedclip"] if mod == "rx_torax" else ["biomedclip"]
        for kind in kinds:
            a2 = demo.level2_agents(mod)
            n2, raw2 = pools(f"nivel2_{mod}", a2, lambda n, m=mod: demo.MODALITIES[m], kind)
            proj2 = pca64(raw2, n2)
            r, L2, P2, _, mae2, proto2, yt2 = evaluate_level(n2, raw2, proj2)
            res[f"{mod}|{kind}"] = r
            if kind == kinds[0]:
                # punta a punta: las mismas imágenes de test por el nivel 1 y luego el nivel 2
                x, _y = demo.data(demo.MODALITIES[mod])["test"]
                idx = np.concatenate([raw2[f"testidx_{n}"] for n in n2])
                z1 = proj1(feats("biomedclip", [demo.to_pil(x[i]) for i in idx]))
                m_idx = n1.index(mod)
                l1_mae = np.array([L1.route(z, m_idx)[0] == mod for z in z1])
                l1_proto = (unit(z1) @ unit(P1).T).argmax(1) == m_idx
                e2e[mod] = {"mae": float(np.mean(l1_mae & (mae2 == yt2))),
                            "prototipos": float(np.mean(l1_proto & (proto2 == yt2))),
                            "nivel1_mae": float(l1_mae.mean()), "nivel1_prototipos": float(l1_proto.mean())}
            print(f"  {mod}/{kind} listo ({time.time() - t0:.0f} s)", flush=True)
    res["punta_a_punta"] = e2e
    # lo ajeno en el nivel 1
    xr = np.concatenate([demo.data("retinamnist")[s][0] for s in ("train", "val", "test")])
    zo = proj1(feats("biomedclip", [demo.to_pil(a) for a in xr]))
    zin = np.concatenate([proj1(raw1[f"test_{n}"]) for n in n1])
    ein = np.concatenate([[(k + 1) % len(n1)] * len(raw1[f"test_{n}"]) for k, n in enumerate(n1)])
    acc_in = np.mean([L1.route(z, int(e))[0] is not None for z, e in zip(zin, ein)])
    s_in, s_out = (unit(zin) @ unit(P1).T).max(1), (unit(zo) @ unit(P1).T).max(1)
    res["ajeno"] = {"acepta_propias_mae": float(acc_in),
                    "rechaza_mae": float(np.mean([L1.route(z, 0)[0] is None for z in zo])),
                    "rechaza_prototipos": float(np.mean(s_out < np.quantile(s_in, 1 - acc_in)))}
    (OUT / "resultados.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    report(res, time.time() - t0)


def report(res, secs):
    lines = ["Exp26: el sistema médico con BiomedCLIP (modalidad, órganos, piel, mama) y RAD-DINO (tórax). PCA 64 por nivel."]
    for key, r in res.items():
        if key in ("punta_a_punta", "ajeno"):
            continue
        lines.append(f"\n[{key}]")
        for m in ("mae", "prototipos", "prototipos_completo", "knn", "logistica"):
            v = r[m]
            lines.append(f"  {m:<20} acierto {100 * v['acierto']:5.1f} · rechazo {100 * v['rechazo']:4.1f} · balanceado {100 * v['balanceado']:5.1f}")
        lines.append(f"  lista MAE: cobertura {100 * r['lista_mae']['cobertura']:.1f}, tamaño {r['lista_mae']['tamano']:.2f}, peor clase {100 * r['lista_mae']['peor_clase']:.1f}"
                     f" · Mondrian: cobertura {100 * r['mondrian']['cobertura']:.1f}, tamaño {r['mondrian']['tamano']:.2f}, peor clase {100 * r['mondrian']['peor_clase']:.1f}")
    lines.append("\n[punta a punta: nivel 1 correcto y nivel 2 correcto]")
    for mod, v in res["punta_a_punta"].items():
        lines.append(f"  {mod:<14} MAE {100 * v['mae']:5.1f} (nivel 1 {100 * v['nivel1_mae']:.1f}) · prototipos {100 * v['prototipos']:5.1f} (nivel 1 {100 * v['nivel1_prototipos']:.1f})")
    a = res["ajeno"]
    lines.append(f"\n[fondo de ojo, a igual aceptación de lo propio ({100 * a['acepta_propias_mae']:.1f} %)] rechazo: MAE {100 * a['rechaza_mae']:.1f} · prototipos {100 * a['rechaza_prototipos']:.1f}")
    lines.append(f"\nTiempo: {secs / 60:.0f} min")
    text = "\n".join(lines)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
