"""Whole-table timings at n = 10^5 and 10^6 against statsmodels and astropy.

``python large_n.py`` writes ``data/large_n.json``. One call builds all n + 1 intervals.
"""

import json
import os
import sys
import time
import warnings

import numpy as np
from astropy.stats import binom_conf_interval as astropy_interval
from statsmodels.stats.proportion import proportion_confint

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "src"))
warnings.filterwarnings("ignore")

import binomcikit as bk  # noqa: E402


def best(fn, reps=3):
    fn()
    out = float("inf")
    for _ in range(reps):
        t = time.perf_counter()
        fn()
        out = min(out, time.perf_counter() - t)
    return out


def main():
    rows = []
    for n in (10**5, 10**6):
        k = np.arange(n + 1)
        for method, sm_name, astropy_name in (
            ("wilson", "wilson", "wilson"),
            ("exact", "beta", None),
        ):
            lo, hi = bk.limits(n, 0.05, method)
            slo, shi = proportion_confint(k, n, alpha=0.05, method=sm_name)
            row = {
                "n": n,
                "method": method,
                "limits_s": best(lambda: bk.limits(n, 0.05, method)),
                "ci_s": best(lambda: bk.ci(n=n, alpha=0.05, method=method), 2),
                "statsmodels_s": best(
                    lambda: proportion_confint(k, n, alpha=0.05, method=sm_name), 2
                ),
                "astropy_s": (
                    best(
                        lambda: astropy_interval(
                            k, n, confidence_level=0.95, interval=astropy_name
                        ),
                        2,
                    )
                    if astropy_name
                    else None
                ),
                "max_err": float(max(np.abs(lo - slo)[1:n].max(), np.abs(hi - shi)[1:n].max())),
            }
            rows.append(row)
            print(row)
    with open(os.path.join(HERE, "data", "large_n.json"), "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=1)


if __name__ == "__main__":
    main()
