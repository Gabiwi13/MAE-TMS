"""Llena heteros en paralelo, un subproceso por agente. Cada subproceso corre
solo este archivo (numpy y la hetero), no torch ni spaCy."""
import contextlib
import io
import pickle
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from hetero_memory import HeteroAssociativeMemory

MAX_PROCS = 4          # por la memoria libre de la máquina


def spec(official):
    return (official.n, official.m, official.p, official.q,
            official._iota, official._kappa, official._xi, official._sigma)


def _fill(sp, pairs):
    n, m, p, q, iota, kappa, xi, sigma = sp
    h = HeteroAssociativeMemory(n, m, p, q, iota=iota, kappa=kappa, xi=xi, sigma=sigma)
    with contextlib.redirect_stdout(io.StringIO()):
        for a, b in pairs:
            h.register(a, b)
    return h


def rebuild_heteros(jobs):
    """{agente: (hetero oficial, parejas)} -> heteros vacías con los parámetros
    de la oficial, llenadas con sus parejas."""
    tmp = Path(tempfile.mkdtemp())
    try:
        names = list(jobs)
        out = {}
        for k in range(0, len(names), MAX_PROCS):
            procs = {}
            for c in names[k:k + MAX_PROCS]:
                official, pairs = jobs[c]
                (tmp / f"{c}.job").write_bytes(pickle.dumps((spec(official), pairs)))
                procs[c] = subprocess.Popen([sys.executable, __file__, str(tmp / f"{c}.job"),
                                             str(tmp / f"{c}.out")])
            for c, pr in procs.items():
                if pr.wait() != 0:
                    raise RuntimeError(f"falló el llenado de {c}")
                out[c] = pickle.loads((tmp / f"{c}.out").read_bytes())
        return out
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sp, pairs = pickle.loads(Path(sys.argv[1]).read_bytes())
    Path(sys.argv[2]).write_bytes(pickle.dumps(_fill(sp, pairs)))
