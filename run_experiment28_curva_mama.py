"""
Experimento 28: curva de aprendizaje en BreastMNIST (ultrasonido de mama, 128 px).
Diseño, predicciones y criterio en propuesta_exp28_curva_mama.md.

Fracciones 25/50/75/100 % del train (estratificadas y anidadas), semillas 42-46.
Brazo A: encoder fijo (el de la corrida balanceada). Brazo B: encoder reentrenado
con la fracción, con 64 pasos de 64 imágenes en todas las fracciones.
Registro completo (60 % llenado, 40 % fase A) o igualado (las dos clases con el
tamaño de la más chica). Test fijo: 42 malignos y 114 benignos.

Uso:
  python run_experiment28_curva_mama.py --verificar
  python run_experiment28_curva_mama.py
  python run_experiment28_curva_mama.py --report-only
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

os.environ["DEMO_BAL"] = "1"     # para que demo.pools lea la caché balanceada en la verificación

import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import roc_auc_score
from torchvision import transforms

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import run_medico_demo as demo  # noqa: E402
import run_experiment23_ambiguedad as e23  # noqa: E402

OUT = ROOT / "results" / "experimento28"
CACHE = OUT / "cache"
CACHE_B = ROOT / "results" / "medico_balanceado" / "cache"
MOD = "us_mama"
NAMES = ["malignant", "normal-benign"]
FRACS = (0.25, 0.5, 0.75, 1.0)
SEEDS = (42, 43, 44, 45, 46)
EPOCHS, STEPS = 8, 8


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (100 * (c - h), 100 * (c + h))


def class_index():
    y = demo.data("breastmnist")["train"][1][:, 0]
    return [np.where(y == k)[0] for k in range(2)]


def subset(seed, frac):
    """Índices por clase en orden permutado por la semilla; las fracciones son prefijos."""
    rng = np.random.RandomState(seed)
    return [rng.permutation(ii)[:int(round(frac * len(ii)))] for ii in class_index()]


def train_encoder(seed, idx_by_class):
    """Como demo.trained_level2, con la fracción y un número fijo de pasos."""
    torch.manual_seed(seed)
    x = demo.data("breastmnist")["train"][0]
    idx = np.concatenate([np.sort(ii) for ii in idx_by_class])
    lab = np.concatenate([[k] * len(ii) for k, ii in enumerate(idx_by_class)])
    w = 1.0 / np.bincount(lab)[lab]
    g = torch.Generator().manual_seed(seed)
    aug = transforms.Compose([transforms.RandomHorizontalFlip(), transforms.RandomRotation(10)])
    enc = demo.Backbone(2).to(demo.DEV)
    opt = torch.optim.Adam(enc.parameters(), lr=1e-4)
    ce = nn.CrossEntropyLoss()
    for _ep in range(EPOCHS):
        enc.train()
        pick = torch.multinomial(torch.tensor(w), STEPS * 64, replacement=True, generator=g).numpy()
        for s in range(STEPS):
            b = pick[s * 64:(s + 1) * 64]
            xb = torch.stack([demo.TF(aug(demo.to_pil(x[idx[i]]))) for i in b]).to(demo.DEV)
            yb = torch.tensor(lab[b]).to(demo.DEV)
            opt.zero_grad()
            ce(enc.head(enc.latent(xb)), yb).backward()
            opt.step()
    return enc.eval()


def encode(enc, which, idx, variants):
    x = demo.data("breastmnist")[which][0]
    return demo.latents(enc, [demo.to_pil(x[i]) for i in idx], variants=variants)


def test_set(enc):
    y = demo.data("breastmnist")["test"][1][:, 0]
    return {n: encode(enc, "test", np.where(y == k)[0], False) for k, n in enumerate(NAMES)}


def val_set(enc):
    y = demo.data("breastmnist")["val"][1][:, 0]
    z = encode(enc, "val", np.arange(len(y)), False)
    return z, y


def split_registro(lat_by_class, mode):
    """lat_by_class: latentes (n, 16, 64) por clase en orden permutado."""
    m = min(len(v) for v in lat_by_class)
    fill, pa = {}, {}
    for n, v in zip(NAMES, lat_by_class):
        v = v[:m] if mode == "igualado" else v
        nf = int(np.ceil(0.6 * len(v)))
        fill[n], pa[n] = v[:nf], v[nf:]
    return fill, pa


def head_probs(enc, Z):
    with torch.no_grad():
        return torch.softmax(enc.head(torch.tensor(Z, dtype=torch.float32).to(demo.DEV)), 1).cpu().numpy()


def evaluate(level, fill, test, enc_head):
    """Filas por imagen de test con la decisión de cada método."""
    X = np.concatenate([fill[n][:, 0] for n in NAMES])
    y = np.concatenate([[k] * len(fill[n]) for k, n in enumerate(NAMES)])
    Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
    protos = np.stack([fill[n][:, 0].mean(0) for n in NAMES])
    rows = []
    for k, n in enumerate(NAMES):
        Z = test[n]
        P = head_probs(enc_head, Z) if enc_head is not None else None
        for i, z in enumerate(Z):
            s, _ = e23.content_sets(level, z)
            prot, why = level.route(z, k)
            zn = z / np.linalg.norm(z)
            nn25 = np.argsort(-(Xn @ zn))[:25]
            dproto = np.linalg.norm(protos - z, axis=1)
            r = {"verdad": n, "S": s, "prot": prot, "motivo": why, "knn": level.knn(z),
                 "knn25_mal": float(np.mean(y[nn25] == 0)),
                 "proto": NAMES[int(dproto.argmin())], "proto_score": float(dproto[1] - dproto[0])}
            if P is not None:
                r["p_mal"] = float(P[i, 0])
            rows.append(r)
    return rows


def mondrian_sets(p_val, y_val, p_test, alpha):
    """Conformal por clase (LAC): un cuantil de 1 - p(clase) por clase, calibrado en val."""
    qs = []
    for k in range(2):
        sc = np.sort(1 - p_val[y_val == k, k])
        n = len(sc)
        j = int(np.ceil((n + 1) * (1 - alpha))) - 1
        qs.append(sc[j] if j < n else np.inf)
    return [[NAMES[k] for k in range(2) if 1 - p[k] <= qs[k]] for p in p_test]


def metrics(rows, p_val=None, y_val=None):
    mal = [r for r in rows if r["verdad"] == NAMES[0]]
    ben = [r for r in rows if r["verdad"] == NAMES[1]]
    out = {}
    methods = ["prot", "knn", "proto"] + (["cabeza"] if "p_mal" in rows[0] else [])
    for mth in methods:
        pred = (lambda r: NAMES[0] if r["p_mal"] >= 0.5 else NAMES[1]) if mth == "cabeza" else (lambda r, m=mth: r[m])
        tp = sum(pred(r) == NAMES[0] for r in mal)
        tn = sum(pred(r) == NAMES[1] for r in ben)
        out[mth] = {"sens": 100 * tp / len(mal), "espec": 100 * tn / len(ben),
                    "bal": 50 * (tp / len(mal) + tn / len(ben)), "tp": tp, "tn": tn,
                    "sens_ic": wilson(tp, len(mal)), "espec_ic": wilson(tn, len(ben)),
                    "rechazo": 100 * np.mean([pred(r) is None for r in rows])}
    truth = np.array([r["verdad"] == NAMES[0] for r in rows])
    out["knn"]["auroc"] = float(roc_auc_score(truth, [r["knn25_mal"] for r in rows]))
    out["proto"]["auroc"] = float(roc_auc_score(truth, [r["proto_score"] for r in rows]))
    if "cabeza" in out:
        out["cabeza"]["auroc"] = float(roc_auc_score(truth, [r["p_mal"] for r in rows]))

    # Memoria: claro = S de un solo agente y el protocolo responde lo mismo; lo demás va a revisión.
    def claro(r):
        return len(r["S"]) == 1 and r["prot"] == r["S"][0]
    rev = [not claro(r) for r in rows]
    n_rev = int(sum(rev))
    out["estados"] = {"desconocido": sum(len(r["S"]) == 0 for r in rows), "claro_S": sum(len(r["S"]) == 1 for r in rows),
                      "ambiguo": sum(len(r["S"]) >= 2 for r in rows),
                      "claro_con_protocolo_distinto": sum(len(r["S"]) == 1 and r["prot"] != r["S"][0] for r in rows)}
    silent = {"memoria": sum(claro(r) and r["prot"] == NAMES[1] for r in mal)}
    benign_rev = {"memoria": sum(not claro(r) for r in ben)}
    if "cabeza" in out:
        margin = np.array([abs(2 * r["p_mal"] - 1) for r in rows])
        to_rev = np.zeros(len(rows), bool)
        to_rev[np.argsort(margin, kind="stable")[:n_rev]] = True
        silent["cabeza"] = sum((not to_rev[i]) and r["p_mal"] < 0.5 for i, r in enumerate(rows) if r["verdad"] == NAMES[0])
        benign_rev["cabeza"] = int(sum(to_rev[i] for i, r in enumerate(rows) if r["verdad"] == NAMES[1]))
        p_test = np.array([[r["p_mal"], 1 - r["p_mal"]] for r in rows])
        best = None
        for a in np.round(np.arange(0.005, 0.5, 0.005), 3):
            sets = mondrian_sets(p_val, y_val, p_test, a)
            frac = sum(len(c) != 1 for c in sets)
            if best is None or abs(frac - n_rev) < abs(best[1] - n_rev):
                best = (a, frac, sets)
        a, frac, sets = best
        silent["mondrian"] = sum(sets[i] == [NAMES[1]] for i, r in enumerate(rows) if r["verdad"] == NAMES[0])
        benign_rev["mondrian"] = sum(len(sets[i]) != 1 for i, r in enumerate(rows) if r["verdad"] == NAMES[1])
        out["mondrian"] = {"alpha": float(a), "revision": int(frac),
                           "cobertura_maligno": 100 * np.mean([NAMES[0] in sets[i] for i, r in enumerate(rows) if r["verdad"] == NAMES[0]])}
    out["revision"] = {"n": n_rev, "frac": 100 * n_rev / len(rows), "malignos_silenciosos": silent,
                       "benignos_a_revision": benign_rev}
    return out


def run_config(arm, seed, frac, mode, enc, lat_by_class, test, val):
    fill, pa = split_registro(lat_by_class, mode)
    level = demo.Level(f"exp28_{arm}_{seed}_{frac}_{mode}", NAMES, None, fill, pa)
    rows = evaluate(level, fill, test, enc if arm == "B" else None)
    p_val = head_probs(enc, val[0]) if arm == "B" else None
    m = metrics(rows, p_val, val[1] if arm == "B" else None)
    m.update({"brazo": arm, "semilla": seed, "fraccion": frac, "registro": mode,
              "n_llenado": {n: len(v) for n, v in fill.items()}, "n_fase_a": {n: len(v) for n, v in pa.items()},
              "formacion": level.form})
    return m, rows


def verify():
    """Semilla 42, 100 %, encoder y pools de la corrida balanceada: 28/42 malignos y 109/114 benignos."""
    enc = demo.Backbone(2).to(demo.DEV).eval()
    enc.load_state_dict(torch.load(CACHE_B / "encoder_us_mama.pt", map_location=demo.DEV))
    names, fill, pa, test = e23.e20.load_pool(CACHE_B, "nivel2_us_mama")
    assert names == NAMES, names
    level = demo.Level("verif", NAMES, None, fill, pa)
    rows = evaluate(level, fill, test, enc)
    tp = sum(r["prot"] == NAMES[0] for r in rows if r["verdad"] == NAMES[0])
    tn = sum(r["prot"] == NAMES[1] for r in rows if r["verdad"] == NAMES[1])
    mal_head = sum(r["p_mal"] >= 0.5 for r in rows if r["verdad"] == NAMES[0])
    print(f"verificación con pools en caché: malignos {tp}/42, benignos {tn}/114, cabeza malignos {mal_head}/42 "
          f"(esperado 28, 109, 33)")
    zt = test_set(enc)
    dz = max(float(np.abs(np.sort(zt[n], 0) - np.sort(test[n], 0)).max()) for n in NAMES)
    print(f"latentes de test recalculados contra la caché: máx |dif| {dz:.2e}")
    ok = (tp, tn, mal_head) == (28, 109, 33)
    print("VERIFICACIÓN", "OK" if ok else "FALLA")
    return ok


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    if not verify():
        sys.exit(1)
    t0 = time.time()
    results, all_rows = [], {}
    enc_a = demo.Backbone(2).to(demo.DEV).eval()
    enc_a.load_state_dict(torch.load(CACHE_B / "encoder_us_mama.pt", map_location=demo.DEV))
    full = class_index()
    path_a = CACHE / "latentes_brazoA.npz"
    if path_a.exists():
        za = np.load(path_a)
        lat_a = [za["mal"], za["ben"]]
    else:
        lat_a = [encode(enc_a, "train", ii, True) for ii in full]
        np.savez(path_a, mal=lat_a[0], ben=lat_a[1])
    pos = [{int(j): t for t, j in enumerate(ii)} for ii in full]
    test_a = test_set(enc_a)
    for seed in SEEDS:
        for frac in FRACS:
            sub = subset(seed, frac)
            lat_sub_a = [lat_a[k][[pos[k][int(j)] for j in sub[k]]] for k in range(2)]
            for mode in ("completo", "igualado"):
                m, rows = run_config("A", seed, frac, mode, enc_a, lat_sub_a, test_a, None)
                results.append(m)
                all_rows[f"A_{seed}_{frac}_{mode}"] = rows
            enc_b = train_encoder(seed, sub)
            if seed == 42 and frac == 1.0:
                sd = enc_a.state_dict()
                dw = max(float((v - sd[k]).abs().max()) for k, v in enc_b.state_dict().items() if v.is_floating_point())
                print(f"  encoder B (42, 100 %) contra el de la caché: máx |dif| de pesos {dw:.2e}", flush=True)
            lat_sub_b = [encode(enc_b, "train", sub[k], True) for k in range(2)]
            test_b, val_b = test_set(enc_b), val_set(enc_b)
            for mode in ("completo", "igualado"):
                m, rows = run_config("B", seed, frac, mode, enc_b, lat_sub_b, test_b, val_b)
                results.append(m)
                all_rows[f"B_{seed}_{frac}_{mode}"] = rows
            print(f"  semilla {seed} fracción {frac:.2f} ({time.time() - t0:.0f} s)", flush=True)
            (OUT / "resultados.json").write_text(json.dumps(results, ensure_ascii=False, default=float))
    (OUT / "filas.json").write_text(json.dumps(all_rows, ensure_ascii=False))
    report(results)


def report(results):
    L = ["Exp28: curva de aprendizaje en BreastMNIST (test fijo: 42 malignos, 114 benignos). "
         "Media de 5 semillas [mín, máx]."]

    def agg(arm, mode, frac, key, mth):
        v = [r[mth][key] for r in results if r["brazo"] == arm and r["registro"] == mode and r["fraccion"] == frac and mth in r]
        if not v:
            return "      —"
        f = ".3f" if key == "auroc" else "5.1f"
        return f"{np.mean(v):{f}} [{np.min(v):{f}}, {np.max(v):{f}}]"

    for arm in ("A", "B"):
        for mode in ("completo", "igualado"):
            L.append(f"\n[brazo {arm} · registro {mode}]")
            for key, title in (("bal", "acierto balanceado"), ("sens", "sensibilidad estricta"), ("espec", "especificidad")):
                L.append(f"  {title}")
                for mth, label in (("prot", "memoria"), ("proto", "prototipos"), ("knn", "kNN"), ("cabeza", "cabeza")):
                    L.append(f"    {label:<11}" + "  ".join(f"{int(f * 100):>3} % {agg(arm, mode, f, key, mth)}" for f in FRACS))
            for mth, label in (("proto", "prototipos"), ("knn", "kNN"), ("cabeza", "cabeza")):
                L.append(f"  AUROC {label:<11}" + "  ".join(f"{int(f * 100):>3} % {agg(arm, mode, f, 'auroc', mth)}" for f in FRACS))
            L.append(f"  rechazo memoria " + "  ".join(f"{int(f * 100):>3} % {agg(arm, mode, f, 'rechazo', 'prot')}" for f in FRACS))
            for f in FRACS:
                rs = [r for r in results if r["brazo"] == arm and r["registro"] == mode and r["fraccion"] == f]
                rv = np.mean([r["revision"]["frac"] for r in rs])
                sil = {k: np.mean([r["revision"]["malignos_silenciosos"][k] for r in rs]) for k in rs[0]["revision"]["malignos_silenciosos"]}
                brv = {k: np.mean([r["revision"]["benignos_a_revision"][k] for r in rs]) for k in rs[0]["revision"]["benignos_a_revision"]}
                st = {k: np.mean([r["estados"][k] for r in rs]) for k in rs[0]["estados"]}
                L.append(f"  {int(f * 100):>3} %: a revisión {rv:4.1f} % · malignos que escapan en silencio "
                         + ", ".join(f"{k} {v:.1f}" for k, v in sil.items())
                         + " · benignos a revisión " + ", ".join(f"{k} {v:.1f}" for k, v in brv.items())
                         + " · estados " + ", ".join(f"{k} {v:.1f}" for k, v in st.items()))
    L.append("\n[semilla 42, 100 %: sensibilidad con IC de Wilson al 95 %]")
    for r in results:
        if r["semilla"] == 42 and r["fraccion"] == 1.0:
            L.append(f"  brazo {r['brazo']} · {r['registro']}: " + " · ".join(
                f"{m} {r[m]['tp']}/42 [{r[m]['sens_ic'][0]:.0f}, {r[m]['sens_ic'][1]:.0f}]"
                for m in ("prot", "proto", "knn", "cabeza") if m in r))
    text = "\n".join(L)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--verificar", action="store_true")
    ap.add_argument("--report-only", action="store_true")
    a = ap.parse_args()
    if a.verificar:
        sys.exit(0 if verify() else 1)
    if a.report_only:
        report(json.loads((OUT / "resultados.json").read_text()))
    else:
        main()
