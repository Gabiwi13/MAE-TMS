"""
Olvido exacto y privacidad de la MAE. Diseño en propuesta_olvido_y_flota.md, parte A.

  A1a olvidar contenido (10 % del llenado) contra reconstruir sin él
  A1b olvidar transacciones de fase A (10 %) contra rehacer la fase A sin ellas
  A2  ataque de pertenencia y exposición por celdas únicas (MAE, kNN, NCM, gaussiana)
Olvidar = restar la relación que sumó el registro (inversa de abstract, sin saturación).

Uso: python run_olvido_privacidad.py [--report-only]
"""
import argparse
import contextlib
import io
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import run_industrial_demo as ind  # noqa: E402
import run_medico_demo as demo  # noqa: E402
import stage6_interaction as s6  # noqa: E402
from stage7_bidirectional import recognize_gated_right  # noqa: E402

OUT = ROOT / "results" / "olvido_privacidad"
MED = Path("C:/Users/aq99l/Projects/MAE-TMS-medico/results/medico_balanceado/cache")
SEED, FRAC = 42, 0.10


# ---------- olvido ----------

def forget_homo(mem, zq):
    am = mem._am
    r = am.to_relation(am.validate(zq))
    am._relation = am._relation - r
    am._updated = False


def forget_dir(d, zq, k):
    ham = d._ham
    a = np.zeros(d._n_agents, dtype=np.int32)
    a[k] = 1
    ca, cb = ham.validate(zq, 0), ham.validate(a, 1)
    r = ham.vectors_to_relation(ca, cb, np.ones(len(ca)), np.ones(len(cb)))
    ham._relation = ham._relation - r
    ham._updated = False
    d._counts[k] -= 1


class LoggedLevel(demo.Level):
    """Level oficial con la fase A registrada (entrada y ganador de cada percepción).
    g, tau y entries permiten reconstruir con la misma percepción y las mismas entradas."""

    def __init__(self, tag, names, fill, phase_a, g=None, tau=None, entries=None, skip=()):
        self.tag, self.names, self.enc = tag, names, None
        zs = np.concatenate([fill[n][:, 0] for n in names])
        lo, hi = zs.min(0), zs.max(0)
        self.g = g if g is not None else (lo - 0.1 * (hi - lo), hi + 0.1 * (hi - lo))
        self.tau = tau if tau is not None else float(np.linalg.norm(zs, axis=1).min() * (1 - demo.ENERGY_MARGIN))
        self.knn_X = zs / np.linalg.norm(zs, axis=1, keepdims=True)
        self.knn_y = np.concatenate([[k] * len(fill[n]) for k, n in enumerate(names)])
        self.entries, self.skip, self.log = entries, set(skip), {}
        with self.ctx():
            self.agents = {n: s6.Agent(n, None) for n in names}
            self.tme = s6.TME()
            for n in names:
                for z in fill[n].reshape(-1, 64):
                    self.agents[n].mem_dom_R.register(self.q(z))
            self.form = self._phase_a(phase_a)

    def _phase_a(self, phase_a):
        rng = np.random.RandomState(SEED)
        rng_new = np.random.RandomState(SEED + 1)
        form = {"registradas": 0, "rechazadas": 0, "sin_energia": 0, "acierto": 0}
        for j in range(max(len(v) for v in phase_a.values())):
            for k, n in enumerate(self.names):
                if j >= len(phase_a[n]) or (n, j) in self.skip:
                    continue
                zv = phase_a[n][j]
                if np.linalg.norm(zv[0]) < self.tau:
                    form["sin_energia"] += 1
                    self.log[(n, j)] = None
                    continue
                scores = {m: recognize_gated_right(self.agents[m], self.q(zv[0])) for m in self.names}
                if sum(scores.values()) == 0:
                    form["rechazadas"] += 1
                    self.log[(n, j)] = None
                    continue
                w = max(scores, key=scores.get)
                widx = self.names.index(w)
                form["registradas"] += 1
                form["acierto"] += int(w == n)
                if self.entries is None:
                    entry = self.names[int(rng.randint(len(self.names)))]
                elif (n, j) in self.entries:
                    entry = self.entries[(n, j)]
                else:
                    entry = self.names[int(rng_new.randint(len(self.names)))]
                self.log[(n, j)] = (entry, w)
                with contextlib.redirect_stdout(io.StringIO()):
                    for z in zv:
                        s6.register_transaction(entry, widx, self.agents, self.tme, self.q(z), "image")
        return form

    def forget_transaction(self, zv, entry, winner):
        widx = self.names.index(winner)
        for z in zv:
            zq = self.q(z)
            forget_dir(self.tme.mem_dir_R, zq, widx)
            for name in {entry, winner}:
                forget_dir(self.agents[name].mem_dir_R, zq, widx)


def dir_state(L):
    out = {"tme": (L.tme.mem_dir_R._ham._relation.copy(), L.tme.mem_dir_R._counts.copy())}
    for n in L.names:
        d = L.agents[n].mem_dir_R
        out[n] = (d._ham._relation.copy(), d._counts.copy())
    return out


def diff_dirs(a, b):
    return int(sum(np.count_nonzero(a[k][0] != b[k][0]) + np.count_nonzero(a[k][1] != b[k][1]) for k in a))


def content_diff(La, Lb):
    return int(sum(np.count_nonzero(La.agents[n].mem_dom_R._am._relation != Lb.agents[n].mem_dom_R._am._relation)
                   for n in La.names))


def routes(L, test):
    return [L.route(z, k)[0] for k, n in enumerate(L.names) for z in test[n]]


# ---------- datos ----------

def industrial_level1():
    F5 = dict(np.load(ind.CACHE / "rasgos512.npz", allow_pickle=False))
    P1 = ind.pca(np.concatenate([ind.imgs()[f"f512all_{p}"] for p in ind.PIECES]))
    reg = {p: ind.proj(P1, F5[f"reg_{p}"]) for p in ind.PIECES}
    fill = {p: reg[p][:ind.N_FILL] for p in ind.PIECES}
    pa = {p: reg[p][ind.N_FILL:] for p in ind.PIECES}
    test = {p: ind.proj(P1, F5[f"test_{p}"]) for p in ind.PIECES}
    return fill, pa, test, F5


def med_pool(tag):
    z = np.load(MED / f"pool_{tag}.npz", allow_pickle=False)
    names = [k[5:] for k in z.files if k.startswith("fill_")]
    return names, {n: z[f"fill_{n}"] for n in names}, {n: z[f"a_{n}"] for n in names}


# ---------- A1 ----------

def part_A1(fill, pa, test):
    res = {}
    names = ind.PIECES
    t0 = time.time()
    L = LoggedLevel("full", names, fill, pa)
    t_build = time.time() - t0
    with contextlib.redirect_stdout(io.StringIO()):
        Loff = demo.Level("oficial", names, None, fill, pa)
    res["verificacion"] = {"directorios_distintos_contra_oficial": diff_dirs(dir_state(L), dir_state(Loff)),
                           "contenido_distinto_contra_oficial": content_diff(L, Loff),
                           "formacion_igual": L.form == Loff.form}
    del Loff
    rng = np.random.RandomState(SEED)
    base_routes = routes(L, test)
    base_dirs = dir_state(L)
    # A1a: olvidar contenido
    forg = {n: np.sort(rng.permutation(len(fill[n]))[:int(round(FRAC * len(fill[n])))]) for n in names}
    t0 = time.time()
    for n in names:
        for z in fill[n][forg[n]].reshape(-1, 64):
            forget_homo(L.agents[n].mem_dom_R, L.q(z))
    t_forget = time.time() - t0
    keep = {n: np.delete(fill[n], forg[n], axis=0) for n in names}
    entries = {k: v[0] for k, v in L.log.items() if v}
    t0 = time.time()
    Lref = LoggedLevel("ref_a", names, keep, pa, g=L.g, tau=L.tau, entries=entries)
    t_rebuild = time.time() - t0
    changed = sum((L.log[k] or (None,))[-1] != (Lref.log[k] or (None,))[-1] for k in L.log)
    r_forget, r_ref = routes(L, test), routes(Lref, test)
    res["A1a"] = {"olvidadas_por_pieza": int(len(forg[names[0]])), "registros_olvidados": int(sum(len(v) for v in forg.values()) * 16),
                  "contenido_celdas_distintas": content_diff(L, Lref),
                  "fase_a_destino_distinto": int(changed), "fase_a_total": len(L.log),
                  "directorios_celdas_distintas": diff_dirs(dir_state(L), dir_state(Lref)),
                  "test_decisiones_distintas": int(sum(a != b for a, b in zip(r_forget, r_ref))),
                  "test_cambian_por_olvidar": int(sum(a != b for a, b in zip(base_routes, r_forget))),
                  "test_n": len(r_ref), "segundos_olvidar": t_forget, "segundos_reconstruir": t_rebuild,
                  "segundos_construir": t_build}
    print(f"  A1a listo: {res['A1a']}", flush=True)
    del Lref
    # A1b: olvidar transacciones (sobre la memoria original)
    L = LoggedLevel("full_b", names, fill, pa)
    reg_keys = sorted(k for k, v in L.log.items() if v)
    pick = rng.permutation(len(reg_keys))[:int(round(FRAC * len(reg_keys)))]
    gone = [reg_keys[i] for i in pick]
    t0 = time.time()
    for (n, j) in gone:
        entry, w = L.log[(n, j)]
        L.forget_transaction(pa[n][j], entry, w)
    t_forget_b = time.time() - t0
    entries = {k: v[0] for k, v in L.log.items() if v}
    Lref = LoggedLevel("ref_b", names, fill, pa, g=L.g, tau=L.tau, entries=entries, skip=gone)
    r_forget, r_ref = routes(L, test), routes(Lref, test)
    res["A1b"] = {"transacciones_olvidadas": len(gone), "de": len(reg_keys),
                  "directorios_celdas_distintas": diff_dirs(dir_state(L), dir_state(Lref)),
                  "contenido_celdas_distintas": content_diff(L, Lref),
                  "test_decisiones_distintas": int(sum(a != b for a, b in zip(r_forget, r_ref))),
                  "test_cambian_por_olvidar": int(sum(a != b for a, b in zip(base_routes, r_forget))),
                  "test_n": len(r_ref), "segundos_olvidar": t_forget_b}
    print(f"  A1b listo: {res['A1b']}", flush=True)
    # costo de olvidar en una cabeza entrenada: reentrenar
    from sklearn.linear_model import LogisticRegression
    X = np.concatenate([fill[n][:, 0] for n in names])
    y = np.concatenate([[k] * len(fill[n]) for k, n in enumerate(names)])
    t0 = time.time()
    LogisticRegression(max_iter=2000).fit(X, y)
    res["cabeza_logistica_segundos_reentrenar"] = time.time() - t0
    res["dir_base_igual_a_original"] = diff_dirs(base_dirs, dir_state(LoggedLevel("again", names, fill, pa)))
    return res


# ---------- A2 ----------

def membership(mem, q, members, nonmembers, member_variants):
    """AUROC del ataque de pertenencia de cada método y exposición por celdas únicas."""
    R = mem._am._relation
    idx = np.arange(64)

    def mae(X):
        return np.array([np.log1p(R[idx, q(z)]).sum() for z in X])

    bank = members.astype(np.float64)
    mu = bank.mean(0)
    P = np.linalg.inv(np.cov(bank.T) + 0.01 * np.eye(64))

    b2 = (bank ** 2).sum(1)

    def knn(X):
        X = np.asarray(X, dtype=np.float64)
        d2 = (X ** 2).sum(1)[:, None] - 2 * X @ bank.T + b2[None]
        return -np.sqrt(np.maximum(d2.min(1), 0))

    def ncm(X):
        return -np.linalg.norm(np.asarray(X, dtype=np.float64) - mu, axis=1)

    def gauss(X):
        d = np.asarray(X, dtype=np.float64) - mu
        return -np.einsum("ij,jk,ik->i", d, P, d)

    out = {k: ind.auroc(f(members), f(nonmembers)) for k, f in (("mae", mae), ("knn", knn), ("ncm", ncm), ("gaussiana", gauss))}
    uniq = []
    for z0, zv in zip(members, member_variants):
        lv = q(z0)
        own = np.array([sum(q(v)[i] == lv[i] for v in zv) for i in range(64)])
        uniq.append(int(np.count_nonzero(R[idx, lv] == own)))
    uniq = np.array(uniq)
    out["unicas_media"] = float(uniq.mean())
    out["miembros_con_unicas"] = float(np.mean(uniq > 0))
    out["n_miembros"], out["n_no_miembros"] = int(len(members)), int(len(nonmembers))
    return out


def part_A2(fill, pa, F5):
    res = {"industrial_nivel1": {}, "industrial_g2": {}, "medico_modalidad": {}, "medico_organos": {}}
    L = LoggedLevel("priv", ind.PIECES, fill, pa)
    for n in ind.PIECES:
        res["industrial_nivel1"][n] = membership(L.agents[n].mem_dom_R, L.q, fill[n][:, 0], pa[n][:, 0], fill[n])
    for p in ind.PIECES:
        P2 = ind.pca(F5[f"reg_{p}"][:ind.N_FILL, 0])
        reg2 = ind.proj(P2, F5[f"reg_{p}"])
        sp = ind.Specialist(reg2[:ind.N_FILL])
        res["industrial_g2"][p] = membership(sp.mem, sp.q, reg2[:ind.N_FILL, 0], reg2[ind.N_FILL:, 0], reg2[:ind.N_FILL])
    print("  A2 industrial listo", flush=True)
    for tag, key in (("nivel1", "medico_modalidad"), ("nivel2_tc_abdomen", "medico_organos")):
        names, mf, ma = med_pool(tag)
        with contextlib.redirect_stdout(io.StringIO()):
            Lm = demo.Level(tag, names, None, mf, ma)
        for n in names:
            res[key][n] = membership(Lm.agents[n].mem_dom_R, Lm.q, mf[n][:, 0], ma[n][:, 0], mf[n])
        print(f"  A2 {key} listo", flush=True)
        del Lm
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    raw = OUT / "resultados.json"
    if not args.report_only:
        t0 = time.time()
        fill, pa, test, F5 = industrial_level1()
        res = {"A1": part_A1(fill, pa, test)}
        print(f"A1 listo ({time.time() - t0:.0f} s)", flush=True)
        res["A2"] = part_A2(fill, pa, F5)
        res["segundos"] = round(time.time() - t0)
        raw.write_text(json.dumps(res, ensure_ascii=False, indent=1))
    report(json.loads(raw.read_text()))


def report(res):
    a = res["A1"]
    L = ["Olvido exacto y privacidad de la MAE (propuesta_olvido_y_flota.md, parte A).",
         f"\n[verificación] fase A registrada contra Level oficial: {json.dumps(a['verificacion'])}; "
         f"reconstrucción repetida, celdas de directorio distintas: {a['dir_base_igual_a_original']}"]
    x = a["A1a"]
    L.append(f"\n[A1a · olvidar contenido] {x['olvidadas_por_pieza']} imágenes por pieza ({x['registros_olvidados']} registros con variantes)")
    L.append(f"  contenido: celdas distintas contra reconstruir sin ellas {x['contenido_celdas_distintas']}")
    L.append(f"  fase A: percepciones con otro destino al reconstruir {x['fase_a_destino_distinto']} de {x['fase_a_total']}; "
             f"celdas de directorio distintas {x['directorios_celdas_distintas']}")
    L.append(f"  test: decisiones distintas entre olvidar y reconstruir {x['test_decisiones_distintas']} de {x['test_n']}; "
             f"cambian respecto de antes de olvidar {x['test_cambian_por_olvidar']}")
    L.append(f"  tiempo: olvidar {x['segundos_olvidar']:.2f} s · reconstruir {x['segundos_reconstruir']:.1f} s · "
             f"construir {x['segundos_construir']:.1f} s · reentrenar la cabeza logística {a['cabeza_logistica_segundos_reentrenar']:.1f} s")
    y = a["A1b"]
    L.append(f"\n[A1b · olvidar transacciones] {y['transacciones_olvidadas']} de {y['de']} percepciones de fase A")
    L.append(f"  directorios: celdas distintas contra rehacer la fase A sin ellas {y['directorios_celdas_distintas']}; contenido {y['contenido_celdas_distintas']}")
    L.append(f"  test: decisiones distintas {y['test_decisiones_distintas']} de {y['test_n']}; cambian respecto de antes de olvidar {y['test_cambian_por_olvidar']}; "
             f"olvidar {y['segundos_olvidar']:.2f} s")
    L.append("\n[A2 · ataque de pertenencia] AUROC (0.5 = no distingue miembros) · coordenadas en celdas únicas")
    for key, rows in res["A2"].items():
        L.append(f"  {key}")
        for n, r in rows.items():
            L.append(f"    {n:<22} n={r['n_miembros']}/{r['n_no_miembros']}  mae {r['mae']:.3f} · knn {r['knn']:.3f} · ncm {r['ncm']:.3f} · "
                     f"gaussiana {r['gaussiana']:.3f} · únicas {r['unicas_media']:.2f} (miembros con alguna {100 * r['miembros_con_unicas']:.1f} %)")
        m = {k: np.mean([r[k] for r in rows.values()]) for k in ("mae", "knn", "ncm", "gaussiana", "unicas_media", "miembros_con_unicas")}
        L.append(f"    media                  mae {m['mae']:.3f} · knn {m['knn']:.3f} · ncm {m['ncm']:.3f} · gaussiana {m['gaussiana']:.3f} · "
                 f"únicas {m['unicas_media']:.2f} ({100 * m['miembros_con_unicas']:.1f} %)")
    L.append(f"\nTiempo total: {res.get('segundos', 0) / 60:.0f} min")
    text = "\n".join(L)
    (OUT / "resumen.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
