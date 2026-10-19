"""
Enrutador de una flota de detectores PatchCore (uno por pieza). Diseño en
propuesta_olvido_y_flota.md, parte B.

  B1 piezas conocidas: MAE, kNN sin abstención, kNN con abstención y oráculo
  B2 pieza nueva: 12 pliegues dejando una pieza fuera del sistema
Percepción del enrutador: nivel 1 del demo (ResNet18 + PCA64). Detectores: parches del demo.

Uso: python run_enrutador_flota.py [--report-only]
"""
import argparse
import contextlib
import io
import json
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import run_industrial_demo as ind  # noqa: E402
import run_medico_demo as demo  # noqa: E402
from run_olvido_privacidad import industrial_level1  # noqa: E402

OUT = ROOT / "results" / "enrutador_flota"
CACHE = OUT / "cache"            # fuera de git
PIECES, N_FILL, DEV = ind.PIECES, ind.N_FILL, demo.DEV
ACCEPT_DET = 0.95


def detector_scores():
    """S[pieza de la imagen][i, d]: puntaje PatchCore (más alto = más normal) de cada imagen
    de test bajo el detector d, y el umbral de cada detector (95 % de su calibración)."""
    path = CACHE / "detectores.npz"
    if path.exists():
        z = np.load(path)
        return {p: z[f"S_{p}"] for p in PIECES}, z["thr"]
    net = ind.backbone()
    S = {p: np.zeros((len(ind.imgs()[f"test_{p}"]), len(PIECES)), dtype=np.float32) for p in PIECES}
    thr = np.zeros(len(PIECES))
    t0 = time.time()
    for d, pd in enumerate(PIECES):
        regp = ind.patch_feats(net, ind.imgs()[f"reg_{pd}"])
        Pp = ind.pca(regp[:N_FILL].reshape(-1, regp.shape[-1]))
        bank = torch.tensor(ind.proj(Pp, regp[:N_FILL]).reshape(-1, 64), device=DEV)
        cal = ind.proj(Pp, regp[N_FILL:])
        del regp

        def score(Z):
            out = []
            for im in Z:
                t = torch.tensor(im, device=DEV)
                dmin = torch.cat([torch.cdist(t[i:i + 392], bank).min(1).values for i in range(0, len(t), 392)])
                out.append(-float(dmin.max()))
            return np.array(out)

        thr[d] = np.quantile(score(cal), 1 - ACCEPT_DET)
        for p in PIECES:
            x = ind.imgs()[f"test_{p}"]
            for i in range(0, len(x), 64):
                S[p][i:i + 64, d] = score(ind.proj(Pp, ind.patch_feats(net, x[i:i + 64])))
        print(f"  detector {pd} listo ({time.time() - t0:.0f} s)", flush=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    np.savez(path, thr=thr, **{f"S_{p}": S[p] for p in PIECES})
    return S, thr


class KnnRouter:
    def __init__(self, fill, names):
        X = np.concatenate([fill[n][:, 0] for n in names]).astype(np.float64)
        self.y = np.concatenate([[k] * len(fill[n]) for k, n in enumerate(names)])
        self.Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
        self.X, self.names = X, names
        self.b2 = (X ** 2).sum(1)

    def route(self, Z):
        Z = np.asarray(Z, dtype=np.float64)
        sim = (Z / np.linalg.norm(Z, axis=1, keepdims=True)) @ self.Xn.T
        nn = np.argsort(-sim, axis=1)[:, :5]
        return [self.names[np.bincount(self.y[r]).argmax()] for r in nn]

    def dist(self, Z):
        Z = np.asarray(Z, dtype=np.float64)
        d2 = (Z ** 2).sum(1)[:, None] - 2 * Z @ self.X.T + self.b2[None]
        return np.sqrt(np.maximum(np.sort(d2, axis=1)[:, :5], 0)).mean(1)


def outcome(dest, piece, i, S, thr):
    if dest is None:
        return "abstencion"
    d = PIECES.index(dest)
    return "alarma" if S[piece][i, d] < thr[d] else "pasa"


def run_routers(L, kr, names, test_sets, cal, S, thr, label_y):
    """Destinos de los cuatro enrutadores para las imágenes de test_sets {pieza: Z}."""
    acc_mae = np.mean([L.route(z, k)[0] is not None for k, n in enumerate(names) for z in cal[n]])
    d_cal = kr.dist(np.concatenate([cal[n] for n in names]))
    thr_knn = np.quantile(d_cal, acc_mae)
    rows = []
    for p, Z in test_sets.items():
        k = names.index(p) if p in names else 0
        mae = [L.route(z, k)[0] for z in Z]
        knn = kr.route(Z)
        dist = kr.dist(Z)
        for i, z in enumerate(Z):
            dests = {"mae": mae[i], "knn": knn[i], "knn_abst": knn[i] if dist[i] <= thr_knn else None,
                     "oraculo": p if p in names else None}
            rows.append({"pieza": p, "falla": int(label_y[p][i]),
                         **{f"dest_{r}": v for r, v in dests.items()},
                         **{f"res_{r}": outcome(v, p, i, S, thr) for r, v in dests.items()}})
    return rows, float(acc_mae)


def state_bytes(L, kr):
    cells = 0
    for n in L.names:
        cells += L.agents[n].mem_dom_R._am._relation.size + L.agents[n].mem_dir_R._ham._relation.size
    cells += L.tme.mem_dir_R._ham._relation.size
    return {"mae_celdas": int(cells), "mae_bytes_uint16": int(cells * 2), "knn_bytes_float32": int(kr.X.size * 4)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    raw = OUT / "resultados.json"
    if not args.report_only:
        t0 = time.time()
        fill, pa, test, _ = industrial_level1()
        cal = {p: pa[p][:, 0] for p in PIECES}
        S, thr = detector_scores()
        print(f"detectores listos ({time.time() - t0:.0f} s)", flush=True)
        y = {p: ind.imgs()[f"testy_{p}"] for p in PIECES}
        with contextlib.redirect_stdout(io.StringIO()):
            L = demo.Level("flota", PIECES, None, fill, pa)
        kr = KnnRouter(fill, PIECES)
        rows, acc = run_routers(L, kr, PIECES, test, cal, S, thr, y)
        res = {"B1": {"filas": rows, "acepta_cal_mae": acc, "tamano": state_bytes(L, kr)}, "B2": {}}
        print(f"B1 listo ({time.time() - t0:.0f} s)", flush=True)
        del L
        for h in PIECES:
            names = [p for p in PIECES if p != h]
            with contextlib.redirect_stdout(io.StringIO()):
                Lh = demo.Level(f"sin_{h}", names, None, {p: fill[p] for p in names}, {p: pa[p] for p in names})
            rows_h, acc_h = run_routers(Lh, KnnRouter(fill, names), names, {h: test[h]}, cal, S, thr, y)
            res["B2"][h] = {"filas": rows_h, "acepta_cal_mae": acc_h}
            print(f"  pliegue sin {h} ({time.time() - t0:.0f} s)", flush=True)
            del Lh
        res["segundos"] = round(time.time() - t0)
        raw.write_text(json.dumps(res, ensure_ascii=False))
    report(json.loads(raw.read_text()))


def pct(x):
    return f"{100 * x:5.1f}"


ROUTERS = ("oraculo", "mae", "knn", "knn_abst")


def report(res):
    L = ["Enrutador de una flota de detectores PatchCore (propuesta_olvido_y_flota.md, parte B).",
         f"Detectores fijados al 95 % de aceptación de su calibración. Tamaño del estado: {json.dumps(res['B1']['tamano'])}"]
    rows = res["B1"]["filas"]
    L.append(f"\n[B1 · piezas conocidas] la MAE acepta {pct(res['B1']['acepta_cal_mae'])} % de la calibración; kNN con abstención se fija ahí")
    for r in ROUTERS:
        ok = np.mean([x[f"dest_{r}"] == x["pieza"] for x in rows])
        other = np.mean([x[f"dest_{r}"] not in (None, x["pieza"]) for x in rows])
        line = f"  {r:<9} a su pieza {pct(ok)} · a otra {pct(other)}"
        for lab, nm in ((0, "normales"), (1, "fallas")):
            c = Counter(x[f"res_{r}"] for x in rows if x["falla"] == lab)
            n = sum(c.values())
            line += f" | {nm}: alarma {pct(c['alarma'] / n)} · abstención {pct(c['abstencion'] / n)} · pasa {pct(c['pasa'] / n)}"
        L.append(line)
    L.append("\n[B2 · pieza nueva fuera del sistema] destino de sus imágenes de test: abstención / a otro detector y alarma / a otro y pasa (falla silenciosa)")
    agg = {r: Counter() for r in ROUTERS[1:]}
    for h, b in res["B2"].items():
        line = f"  {h:<11} n={len(b['filas']):>3} acepta cal {pct(b['acepta_cal_mae'])}"
        for r in ROUTERS[1:]:
            c = Counter(x[f"res_{r}"] for x in b["filas"])
            agg[r].update({k: v / len(b["filas"]) for k, v in c.items()})
            dest = Counter(x[f"dest_{r}"] for x in b["filas"] if x[f"dest_{r}"])
            line += f" | {r}: {pct(c['abstencion'] / len(b['filas']))} / {pct(c['alarma'] / len(b['filas']))} / {pct(c['pasa'] / len(b['filas']))}"
            if r == "mae":
                line += f" {dict(dest.most_common(2))}"
        L.append(line)
    k = len(res["B2"])
    L.append("  media (de los pliegues): " + " | ".join(
        f"{r}: abstención {pct(agg[r]['abstencion'] / k)} · alarma {pct(agg[r]['alarma'] / k)} · pasa {pct(agg[r]['pasa'] / k)}" for r in agg))
    L.append(f"\nTiempo total: {res.get('segundos', 0) / 60:.0f} min")
    text = "\n".join(L)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
