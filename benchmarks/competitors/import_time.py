"""Interleaved import-time comparison (fresh interpreter per sample, minimum and median of N).

Sampling the packages round-robin, rather than one after another, keeps slow phases of the machine from
landing on a single package. ``python import_time.py [repeats]`` writes ``data/import_time.json``.
"""

import json
import os
import statistics
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "src")
IMPORTS = {
    "binomcikit": "import binomcikit",
    "DBCI": "import diff_binom_confint",
    "binomial_cis": "import binomial_cis",
    "pynomial (Dpananos)": "import pynomial",
    "binoculars": "import binoculars",
    "statsmodels (proportion)": "import statsmodels.stats.proportion",
    "astropy.stats": "import astropy.stats",
    "scipy.stats": "import scipy.stats",
    "pandas + scipy.stats (floor for binomcikit)": "import pandas, scipy.stats",
}


def sample(code):
    prefix = f"import sys; sys.path.insert(0, {SRC!r}); "
    t = time.perf_counter()
    r = subprocess.run([sys.executable, "-W", "ignore", "-c", prefix + code], capture_output=True)
    return time.perf_counter() - t, r.returncode


def main(repeats=9):
    t = time.perf_counter()
    subprocess.run([sys.executable, "-c", "pass"])
    base = time.perf_counter() - t
    times = {k: [] for k in IMPORTS}
    for _ in range(repeats):
        for k, code in IMPORTS.items():
            dt, rc = sample(code)
            if rc == 0:
                times[k].append(dt - base)
    out = {
        "python": sys.version.split()[0],
        "repeats": repeats,
        "baseline_interpreter_s": base,
        "min_s": {k: min(v) for k, v in times.items() if v},
        "median_s": {k: statistics.median(v) for k, v in times.items() if v},
    }
    with open(os.path.join(HERE, "data", "import_time.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    for k in out["min_s"]:
        print(f"{k:46s} min {out['min_s'][k]:.2f} s   median {out['median_s'][k]:.2f} s")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 9)
