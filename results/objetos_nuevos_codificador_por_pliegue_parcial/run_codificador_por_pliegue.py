"""
Exp16 con el codificador reentrenado por pliegue (M4 de la lectura de jurado).

Por pliegue k:
  1. entrena el codificador con src/stage2_encoder.train() (receta oficial) sobre
     splits.json sin las imágenes de los objetos reservados (train y test);
  2. codifica las 410 × 16 vistas por clase con encode_all() de exp16;
  3. recalcula la escala min-max (variantes 0-3 del llenado del pliegue) con
     compute_global_latent_stats() y τ con latent_energy_threshold(), las funciones
     oficiales, apuntadas a la carpeta del pliegue;
  4. corre run_fold(k) de exp16 sin cambios.

Uso (desde la raíz del worktree):
  python results/objetos_nuevos_codificador_por_pliegue/run_codificador_por_pliegue.py --folds 1 --solo-codificador
  python results/objetos_nuevos_codificador_por_pliegue/run_codificador_por_pliegue.py --folds 1,3,5
  python results/objetos_nuevos_codificador_por_pliegue/run_codificador_por_pliegue.py --report
"""
import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
MOD = ROOT / "models" / "codificador_por_pliegue"
OFICIAL_RAW = ROOT / "results" / "experimento16" / "raw"
os.environ["EXP16_OUT"] = str(OUT)
os.environ.pop("CLS_WEIGHT", None)
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

import run_experiment16_leave_object_out as e16  # noqa: E402
import stage2_encoder as s2  # noqa: E402
import stage5_fill as s5  # noqa: E402
import stage7_bidirectional as s7  # noqa: E402
from run_experiment11_monolithic import _ci, _rate, _fmt  # noqa: E402

CLASSES = s5.CLASSES
TIEMPOS = OUT / "tiempos"


def fold_dir(k):
    return MOD / f"pliegue_{k:02d}"


def full_index():
    return {c: e16.class_images(c) for c in CLASSES}


def held_objects(k):
    split = e16.fold_split(full_index(), k)
    return {c: split[c]["objeto"] for c in CLASSES}


def _log_time(k, key, secs):
    TIEMPOS.mkdir(parents=True, exist_ok=True)
    p = TIEMPOS / f"pliegue_{k:02d}.json"
    t = json.loads(p.read_text()) if p.exists() else {}
    t[key] = round(secs, 1)
    p.write_text(json.dumps(t, indent=1))


def _load_fold_encoder(d):
    import torch
    enc = s2.Encoder().to(s2.DEVICE)
    enc.load_state_dict(torch.load(d / "encoder.pt", map_location=s2.DEVICE))
    enc.eval()
    return enc


def train_encoder(k):
    d = fold_dir(k)
    meta_path = d / "encoder.meta.json"
    if meta_path.exists() and json.loads(meta_path.read_text()).get("completed"):
        return json.loads(meta_path.read_text())
    d.mkdir(parents=True, exist_ok=True)
    held = held_objects(k)
    splits = json.loads((s5.DATA_DIR / "splits.json").read_text())
    filt = {c: {part: [p for p in splits[c][part] if e16.object_id(p) != held[c]]
                for part in ("train", "test")} for c in CLASSES}
    (d / "splits.json").write_text(json.dumps(filt, indent=1))
    assert s2.CLS_WEIGHT == 0.1 and s2.EPOCHS == 50 and s2.SEED == 42
    s2.DATA_DIR, s2.MODELS_DIR, s2.META_PATH = d, d, meta_path
    t0 = time.time()
    rmse, acc, *_ = s2.train(seed=s2.SEED)
    secs = time.time() - t0
    _log_time(k, "entrenamiento_codificador", secs)
    meta = json.loads(meta_path.read_text())
    meta.update(device=str(s2.DEVICE), objetos_reservados=held, segundos=round(secs, 1),
                n_train=sum(len(v["train"]) for v in filt.values()),
                n_test=sum(len(v["test"]) for v in filt.values()))
    meta_path.write_text(json.dumps(meta, indent=2))
    print(f"  pliegue {k}: codificador RMSE={rmse:.4f} acc={acc:.1f}% ({secs/60:.1f} min)", flush=True)
    if not meta["passed"]:
        raise RuntimeError(f"pliegue {k}: el codificador no cumple los criterios oficiales ({meta})")
    return meta


def held_classifier_accuracy(k, d):
    """Diagnóstico: acierto de la cabeza clasificadora (que el sistema no usa) sobre
    las vistas del objeto reservado y sobre el banco «conocido»."""
    import torch
    from PIL import Image
    arr = np.load(d / "latentes.npy")
    index = json.loads((d / "latentes_indice.json").read_text())
    split = e16.fold_split(index, k)
    clf = s2.Classifier().to(s2.DEVICE)
    clf.load_state_dict(torch.load(d / "classifier.pt", map_location=s2.DEVICE))
    clf.eval()
    out = {}
    for banco in ("nuevo", "conocido"):
        ok = n = 0
        for ci, c in enumerate(CLASSES):
            z = torch.tensor(arr[ci, split[c][banco], 0]).to(s2.DEVICE)
            with torch.no_grad():
                ok += int((clf(z).argmax(1) == ci).sum().item())
            n += len(split[c][banco])
        out[banco] = ok / n
    return out


def prepare_fold(k):
    """Latentes, escala y τ del pliegue con las funciones oficiales."""
    d = fold_dir(k)
    e16.LAT_PATH, e16.IDX_PATH = d / "latentes.npy", d / "latentes_indice.json"
    if not e16.LAT_PATH.exists():
        e16.load_encoder = lambda: _load_fold_encoder(d)
        t0 = time.time()
        e16.encode_all()
        _log_time(k, "latentes", time.time() - t0)
    s5.MODELS_DIR = d
    s7.MODELS_DIR, s7.ENERGY_PATH = d, d / "latent_energy_threshold.json"
    if not s7.ENERGY_PATH.exists():
        arr = np.load(e16.LAT_PATH)
        split = e16.fold_split(json.loads(e16.IDX_PATH.read_text()), k)
        by_cls = {c: [arr[ci, i, v] for i in split[c]["llenado"] for v in range(s5.FILL_VARIANTS)]
                  for ci, c in enumerate(CLASSES)}
        s5.compute_global_latent_stats(None, by_cls)
        for c in CLASSES:
            (d / f"instance_latents_{c}.json").write_text(json.dumps([z.tolist() for z in by_cls[c]]))
        s7.latent_energy_threshold()
    diag = d / "diagnostico.json"
    if not diag.exists():
        diag.write_text(json.dumps({"clasificador_acierto": held_classifier_accuracy(k, d),
                                    "tau": s7.latent_energy_threshold()}, indent=1))


def run_fold(k, solo_codificador=False):
    train_encoder(k)
    if solo_codificador:
        return
    prepare_fold(k)
    t0 = time.time()
    if not (e16.RAW_DIR / f"pliegue_{k:02d}.json").exists():
        e16.run_fold(k)
        _log_time(k, "logica_exp16", time.time() - t0)


# ---------- reporte ----------

def _load(raw_dir, folds):
    return {k: json.loads((raw_dir / f"pliegue_{k:02d}.json").read_text(encoding="utf-8")) for k in folds}


def _rows(raw, banco, cls=None, obj=None):
    return [r for r in raw["filas"] if r["banco"] == banco and (cls is None or r["clase"] == cls)
            and (obj is None or r["objeto"] == obj)]


def report():
    folds = sorted(int(p.stem.split("_")[1]) for p in e16.RAW_DIR.glob("pliegue_*.json"))
    summary = e16.aggregate()
    e16.make_figure(summary)
    mine, ofi = _load(e16.RAW_DIR, folds), _load(OFICIAL_RAW, folds)

    per_fold = []
    for k in folds:
        meta = json.loads((fold_dir(k) / "encoder.meta.json").read_text())
        diag = json.loads((fold_dir(k) / "diagnostico.json").read_text())
        t = json.loads((TIEMPOS / f"pliegue_{k:02d}.json").read_text())
        row = {"pliegue": k, "rmse": meta["rmse"], "acc_test": meta["acc"],
               "clf_nuevo": diag["clasificador_acierto"]["nuevo"],
               "clf_conocido": diag["clasificador_acierto"]["conocido"], "tau": diag["tau"],
               "registradas_A": mine[k]["meta"]["formacion"]["registradas"],
               "registradas_A_oficial": ofi[k]["meta"]["formacion"]["registradas"],
               "min_entrenamiento": t.get("entrenamiento_codificador", float("nan")) / 60,
               "min_logica": t.get("logica_exp16", float("nan")) / 60}
        for src, raw in (("pliegue", mine[k]), ("oficial", ofi[k])):
            for banco in ("nuevo", "conocido"):
                rs = _rows(raw, banco)
                row[f"e2e_{banco}_{src}"] = _rate(rs, "e2e")
                row[f"falsos_{banco}_{src}"] = int(sum(r["falso_ruteo"] for r in rs))
                row[f"contenido_{banco}_{src}"] = _rate(rs, "contenido_acepta")
                row[f"dir_{banco}_{src}"] = _rate(rs, "dir_acepta")
        per_fold.append(row)

    per_obj = []
    for k in folds:
        for c in CLASSES:
            obj = mine[k]["meta"]["objeto_reservado"][c]
            per_obj.append({"pliegue": k, "clase": c, "objeto": f"{c}{obj}",
                            "e2e_pliegue": _rate(_rows(mine[k], "nuevo", c, obj), "e2e"),
                            "e2e_oficial": _rate(_rows(ofi[k], "nuevo", c, obj), "e2e"),
                            "falsos_pliegue": int(sum(r["falso_ruteo"] for r in _rows(mine[k], "nuevo", c, obj))),
                            "falsos_oficial": int(sum(r["falso_ruteo"] for r in _rows(ofi[k], "nuevo", c, obj)))})

    for name, rows in (("por_pliegue.csv", per_fold), ("por_objeto.csv", per_obj)):
        with open(OUT / name, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)

    def ci_of(key):
        return _ci([r[key] for r in per_fold])

    comp = {
        "e2e_nuevo": {s: ci_of(f"e2e_nuevo_{s}") for s in ("pliegue", "oficial")},
        "e2e_conocido": {s: ci_of(f"e2e_conocido_{s}") for s in ("pliegue", "oficial")},
        "dif_nuevo_pliegue_menos_oficial": _ci([r["e2e_nuevo_pliegue"] - r["e2e_nuevo_oficial"] for r in per_fold]),
        "dif_conocido_pliegue_menos_oficial": _ci([r["e2e_conocido_pliegue"] - r["e2e_conocido_oficial"]
                                                  for r in per_fold]),
        "brecha_oficial": _ci([r["e2e_conocido_oficial"] - r["e2e_nuevo_oficial"] for r in per_fold]),
        "brecha_pliegue": _ci([r["e2e_conocido_pliegue"] - r["e2e_nuevo_pliegue"] for r in per_fold]),
        "falsos": {f"{b}_{s}": int(sum(r[f"falsos_{b}_{s}"] for r in per_fold))
                   for b in ("nuevo", "conocido") for s in ("pliegue", "oficial")},
        "n_imagenes_por_banco": 328 * len(folds),
    }
    fr = {}
    for k in folds:
        for r in mine[k]["filas"]:
            if r["falso_ruteo"]:
                key = f"{r['banco']}: {r['clase']} → {r['destino']}"
                fr[key] = fr.get(key, 0) + 1
    comp["falsos_pares"] = dict(sorted(fr.items(), key=lambda kv: -kv[1]))
    (OUT / "comparacion_oficial.json").write_text(json.dumps(comp, indent=1, ensure_ascii=False), encoding="utf-8")
    (OUT / "destinos_objeto_nuevo.json").write_text(
        json.dumps(held_destinations(folds, mine), indent=1, ensure_ascii=False), encoding="utf-8")
    write_tables(summary, per_fold, per_obj, comp, folds)


def held_destinations(folds, mine):
    """Por objeto reservado: clase que da la cabeza clasificadora del codificador del
    pliegue (no la usa el sistema) junto al destino del ruteo."""
    import torch
    out = {}
    for k in folds:
        d = fold_dir(k)
        arr = np.load(d / "latentes.npy")
        split = e16.fold_split(json.loads((d / "latentes_indice.json").read_text()), k)
        clf = s2.Classifier()
        clf.load_state_dict(torch.load(d / "classifier.pt", map_location="cpu"))
        clf.eval()
        for ci, c in enumerate(CLASSES):
            with torch.no_grad():
                pred = clf(torch.tensor(arr[ci, split[c]["nuevo"], 0])).argmax(1).numpy()
            dest = {}
            for r in _rows(mine[k], "nuevo", c):
                dest[r.get("destino") or "rechazo"] = dest.get(r.get("destino") or "rechazo", 0) + 1
            out[f"{k}|{c}{split[c]['objeto']}"] = {
                "cabeza_clasificadora": {CLASSES[j]: int((pred == j).sum()) for j in sorted(set(pred))},
                "destino_ruteo": dest}
    return out


def write_tables(summary, per_fold, per_obj, comp, folds):
    L = [f"# Tablas (pliegues {folds})", "",
         "## Punta a punta y etapas, codificador por pliegue (formato de exp16)", "",
         "| banco | contenido acepta | responde | directorio acepta | ruteo ok (de aceptadas) | falso ruteo | e2e | hit estricto | otro dominio |",
         "|---|---|---|---|---|---|---|---|---|"]
    for banco in ("conocido", "nuevo"):
        b = summary["bancos"][banco]
        L.append(f"| objeto {banco} | " + " | ".join(_fmt(b[m]) for m in e16.METRICS) + " |")
    L += ["", "Brecha (conocido − nuevo, puntos, por pliegue):", "", "| medida | brecha |", "|---|---|"]
    for m, v in summary["brecha"].items():
        L.append(f"| {m} | {_fmt(v)} |")
    L += ["", f"Razón e2e nuevo / conocido por pliegue: {_fmt(summary['razon_e2e_nuevo_conocido'], False)}.", "",
          "## Contra exp16 oficial (mismos pliegues; % de 328 por pliegue, media y bootstrap 95 %)", "",
          "| medida | exp16 oficial | codificador por pliegue | diferencia (pliegue − oficial) |", "|---|---|---|---|",
          f"| e2e objeto conocido | {_fmt(comp['e2e_conocido']['oficial'])} | {_fmt(comp['e2e_conocido']['pliegue'])} "
          f"| {_fmt(comp['dif_conocido_pliegue_menos_oficial'])} |",
          f"| e2e objeto nuevo | {_fmt(comp['e2e_nuevo']['oficial'])} | {_fmt(comp['e2e_nuevo']['pliegue'])} "
          f"| {_fmt(comp['dif_nuevo_pliegue_menos_oficial'])} |",
          f"| brecha conocido − nuevo | {_fmt(comp['brecha_oficial'])} | {_fmt(comp['brecha_pliegue'])} | |",
          f"| falsos ruteos, objeto nuevo (de {comp['n_imagenes_por_banco']}) | {comp['falsos']['nuevo_oficial']} "
          f"| {comp['falsos']['nuevo_pliegue']} | |",
          f"| falsos ruteos, objeto conocido (de {comp['n_imagenes_por_banco']}) | {comp['falsos']['conocido_oficial']} "
          f"| {comp['falsos']['conocido_pliegue']} | |",
          "", "## Pliegue por pliegue", "",
          "| pliegue | codificador RMSE / acc test | τ | e2e conocido: oficial → pliegue | e2e nuevo: oficial → pliegue "
          "| falsos nuevo: oficial / pliegue | fase A registradas: oficial / pliegue | min entrenar / lógica |",
          "|---|---|---|---|---|---|---|---|"]
    for r in per_fold:
        L.append(f"| {r['pliegue']} | {r['rmse']:.4f} / {r['acc_test']:.1f} | {r['tau']:.2f} | "
                 f"{r['e2e_conocido_oficial']*100:.1f} → {r['e2e_conocido_pliegue']*100:.1f} | "
                 f"{r['e2e_nuevo_oficial']*100:.1f} → {r['e2e_nuevo_pliegue']*100:.1f} | "
                 f"{r['falsos_nuevo_oficial']} / {r['falsos_nuevo_pliegue']} | "
                 f"{r['registradas_A_oficial']} / {r['registradas_A']} | "
                 f"{r['min_entrenamiento']:.1f} / {r['min_logica']:.1f} |")
    L += ["", "Diagnóstico (no lo usa el sistema): acierto de la cabeza clasificadora del codificador del pliegue.", "",
          "| pliegue | objeto nuevo | objeto conocido |", "|---|---|---|"]
    for r in per_fold:
        L.append(f"| {r['pliegue']} | {r['clf_nuevo']*100:.1f} | {r['clf_conocido']*100:.1f} |")
    L += ["", "## Por clase (media de pliegues, %)", "",
          "| clase | contenido acepta: conocido / nuevo | responde | directorio acepta | e2e | falso ruteo (nuevo) |",
          "|---|---|---|---|---|---|"]
    for cls in CLASSES:
        c = summary["por_clase"][f"conocido|{cls}"]; nw = summary["por_clase"][f"nuevo|{cls}"]
        L.append(f"| {cls} | {c['contenido_acepta']*100:.1f} / {nw['contenido_acepta']*100:.1f} | "
                 f"{c['responde']*100:.1f} / {nw['responde']*100:.1f} | {c['dir_acepta']*100:.1f} / {nw['dir_acepta']*100:.1f} | "
                 f"{c['e2e']*100:.1f} / {nw['e2e']*100:.1f} | {nw['falso_ruteo']*100:.1f} |")
    L += ["", "## Falsos ruteos (todos los pliegues corridos)", "", "| banco: par | imágenes |", "|---|---|"]
    for k, v in comp["falsos_pares"].items():
        L.append(f"| {k} | {v} |")
    if not comp["falsos_pares"]:
        L.append("| ninguno | 0 |")
    f = summary["formacion"]
    L += ["", f"Fase A (media por pliegue): registradas {f['registradas']:.0f}, rechazadas {f['rechazadas']:.1f}, "
          f"sin energía {f['sin_energia']:.1f}, acierto {f['acierto']:.0f} de las registradas.", "",
          "## Por objeto reservado (e2e sobre sus 41 vistas, %)", ""]
    lo = [r for r in per_obj if min(r["e2e_pliegue"], r["e2e_oficial"]) < 0.7]
    n70 = {s: sum(r[f"e2e_{s}"] >= 0.7 for r in per_obj) for s in ("oficial", "pliegue")}
    L += [f"Objetos con e2e ≥ 70 %: oficial {n70['oficial']} de {len(per_obj)}, "
          f"codificador por pliegue {n70['pliegue']} de {len(per_obj)}. Los que quedan debajo en alguno:", "",
          "| objeto | pliegue | oficial | codificador por pliegue | falsos (oficial / pliegue) |", "|---|---|---|---|---|"]
    for r in sorted(lo, key=lambda r: r["e2e_pliegue"]):
        L.append(f"| {r['objeto']} | {r['pliegue']} | {r['e2e_oficial']*100:.0f} | {r['e2e_pliegue']*100:.0f} | "
                 f"{r['falsos_oficial']} / {r['falsos_pliegue']} |")
    L += ["", "Tabla completa en `por_objeto.csv`; por pliegue en `por_pliegue.csv`."]
    (OUT / "tablas.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--folds", default="")
    ap.add_argument("--solo-codificador", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--cola", action="store_true",
                    help="cada proceso toma el siguiente pliegue que nadie haya reclamado")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    for k in [int(x) for x in args.folds.split(",") if x]:
        if args.cola:
            (OUT / "reclamos").mkdir(exist_ok=True)
            try:
                os.close(os.open(OUT / "reclamos" / f"pliegue_{k:02d}", os.O_CREAT | os.O_EXCL))
            except FileExistsError:
                continue
            print(f"pliegue {k}: tomado por el proceso {os.getpid()} ({time.strftime('%H:%M:%S')})", flush=True)
        run_fold(k, args.solo_codificador)
    if args.report:
        report()


if __name__ == "__main__":
    main()
