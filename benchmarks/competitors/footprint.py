import json
import os
import re
import statistics
import subprocess
import sys
import time
from importlib import metadata

SP = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
# name -> (import statement, dist name)
PK = {
    "binomcikit": ("import binomcikit", "binomcikit"),
    "binomcikit[numba loaded]": ("import binomcikit; import numba", "binomcikit"),
    "DBCI": ("import diff_binom_confint", "diff-binom-confint"),
    "binomial_cis": ("import binomial_cis", "binomial-cis"),
    "pynomial": ("import pynomial", "pynomial"),
    "binoculars": ("import binoculars", "binoculars"),
    "statsmodels (proportion)": ("import statsmodels.stats.proportion", "statsmodels"),
    "astropy.stats": ("import astropy.stats", "astropy"),
    "scipy.stats": ("import scipy.stats", "scipy"),
}


def run(code, env=None):
    t = time.perf_counter()
    r = subprocess.run([PY, "-W", "ignore", "-c", code], capture_output=True, text=True, env=env)
    return time.perf_counter() - t, r


base = statistics.median(run("pass")[0] for _ in range(5))


def dist_size(name, seen):
    if name in seen:
        return 0
    seen.add(name)
    try:
        d = metadata.distribution(name)
    except Exception:
        return 0
    tot = 0
    for f in d.files or []:
        try:
            tot += os.path.getsize(d.locate_file(f))
        except Exception:
            pass
    for r in d.requires or []:
        if "extra ==" in r:
            continue
        n = re.split(r"[ ;<>=!\[(~]", r.strip())[0]
        tot += dist_size(n, seen)
    return tot


def closure(name, seen=None):
    seen = set() if seen is None else seen
    if name in seen:
        return seen
    seen.add(name)
    try:
        d = metadata.distribution(name)
    except Exception:
        return seen
    for r in d.requires or []:
        if "extra ==" in r:
            continue
        closure(re.split(r"[ ;<>=!\[(~]", r.strip())[0], seen)
    return seen


out = {"baseline_interpreter_s": base, "python": sys.version.split()[0], "rows": {}}
for k, (imp, dist) in PK.items():
    ts = []
    ok = True
    for _ in range(5):
        t, r = run(imp)
        if r.returncode:
            ok = False
            break
        ts.append(t)
    own = dist_size(dist, set()) if False else None
    seen = set()
    total = dist_size(dist, seen)
    solo = 0
    try:
        d = metadata.distribution(dist)
        for f in d.files or []:
            try:
                solo += os.path.getsize(d.locate_file(f))
            except Exception:
                pass
    except Exception:
        pass
    out["rows"][k] = {
        "import_s": (statistics.median(ts) - base) if ok else None,
        "own_bytes": solo,
        "closure_bytes": total,
        "n_deps_incl_self": len({s.lower().replace("_", "-") for s in seen}),
        "ok": ok,
    }
    print(k, out["rows"][k], flush=True)
json.dump(out, open(os.path.join(SP, "data", "footprint_static.json"), "w"), indent=1)
