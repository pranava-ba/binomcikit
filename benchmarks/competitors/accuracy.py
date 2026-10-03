import json
import os
import sys
import warnings

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src"))
import mpmath as mp
import numpy as np

mp.mp.dps = 30
A = 0.05


def ref_wilson(x, n):
    z = mp.sqrt(2) * mp.erfinv(1 - mp.mpf(A))
    p = mp.mpf(x) / n
    c = p + z * z / (2 * n)
    h = z * mp.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    d = 1 + z * z / n
    return float((c - h) / d), float((c + h) / d)


def _pmf(k, n, p):
    return mp.exp(
        mp.loggamma(n + 1)
        - mp.loggamma(k + 1)
        - mp.loggamma(n - k + 1)
        + k * mp.log(p)
        + (n - k) * mp.log(1 - p)
    )


def _cdf_le(x, n, p):  # P(X<=x), summing the shorter side with the term recurrence
    if x < 0:
        return mp.mpf(0)
    if x >= n:
        return mp.mpf(1)
    if x <= n / 2:
        t = _pmf(0, n, p)
        s = t
        for k in range(1, x + 1):
            t = t * (n - k + 1) / k * p / (1 - p)
            s += t
        return s
    t = _pmf(n, n, p)
    s = t  # P(X>=x+1) from the top
    for k in range(n - 1, x, -1):
        t = t * (k + 1) / (n - k) * (1 - p) / p
        s += t
    return 1 - s


def ref_cp(x, n):
    a2 = mp.mpf(A) / 2

    def solve(f):
        lo, hi = mp.mpf(10) ** -30, 1 - mp.mpf(10) ** -30
        for _ in range(70):
            mid = (lo + hi) / 2
            if f(mid) > 0:
                hi = mid
            else:
                lo = mid
        return (lo + hi) / 2

    # lower: P(X>=x|L)=a2 (decreasing in L going down => f>0 when L too big)
    L = 0.0 if x == 0 else float(solve(lambda p: (1 - _cdf_le(x - 1, n, p)) - a2))
    U = 1.0 if x == n else float(solve(lambda p: a2 - _cdf_le(x, n, p)))
    return L, U


import binoculars as bn
import diff_binom_confint as d
from astropy.stats import binom_conf_interval as abc
from scipy.stats import binomtest
from statsmodels.stats.proportion import proportion_confint as pc

import binomcikit as bk


def bk_(x, n, m):
    r = bk.interval(x, n, A, m)
    return tuple(float(v) for v in (r if not hasattr(r, "iloc") else r.iloc[0, -2:]))[:2]


def run(method):
    comps = {"binomcikit": lambda x, n: bk_(x, n, method)}
    if method == "wilson":
        comps["statsmodels"] = lambda x, n: tuple(
            float(v) for v in pc(x, n, alpha=A, method="wilson")
        )
        comps["astropy"] = lambda x, n: tuple(
            float(v) for v in abc(x, n, confidence_level=1 - A, interval="wilson")
        )
        comps["scipy"] = lambda x, n: (lambda c: (c.low, c.high))(
            binomtest(x, n).proportion_ci(1 - A, method="wilson")
        )
        comps["DBCI"] = lambda x, n: (lambda c: (c.lower_bound, c.upper_bound))(
            d.compute_confidence_interval(x, n, 1 - A, "wilson")
        )
        comps["binoculars"] = lambda x, n: bn.binomial_confidence(x / n, n, method="wilson")
        ref = ref_wilson
    else:
        comps["statsmodels"] = lambda x, n: tuple(
            float(v) for v in pc(x, n, alpha=A, method="beta")
        )
        comps["scipy"] = lambda x, n: (lambda c: (c.low, c.high))(
            binomtest(x, n).proportion_ci(1 - A, method="exact")
        )
        comps["DBCI"] = lambda x, n: (lambda c: (c.lower_bound, c.upper_bound))(
            d.compute_confidence_interval(x, n, 1 - A, "clopper-pearson")
        )
        comps["binoculars"] = lambda x, n: bn.binomial_confidence(
            x / n, n, method="clopper-pearson"
        )
        ref = ref_cp
    cases = [
        (0, 1),
        (1, 1),
        (0, 2),
        (1, 5),
        (2, 5),
        (0, 10),
        (10, 10),
        (1, 10),
        (9, 10),
        (0, 1000),
        (1000, 1000),
        (1, 1000),
        (999, 1000),
        (500, 1000),
        (0, 100000),
        (100000, 100000),
        (1, 100000),
        (99999, 100000),
        (3, 100000),
    ]
    res = {k: {"max_err": 0.0, "worst": None, "fails": []} for k in comps}
    for x, n in cases:
        r = ref(x, n)
        for k, f in comps.items():
            try:
                v = f(x, n)
                e = max(abs(v[0] - r[0]), abs(v[1] - r[1]))
                if not np.isfinite(e):
                    res[k]["fails"].append((x, n, "nan"))
                    continue
                if e > res[k]["max_err"]:
                    res[k]["max_err"] = e
                    res[k]["worst"] = (x, n)
                res[k].setdefault("errs", {})[f"{x}/{n}"] = e
            except Exception as ex:
                res[k]["fails"].append((x, n, type(ex).__name__))
    return res


out = {m: run(m) for m in ("wilson", "exact")}
json.dump(
    out,
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "accuracy.json"), "w"),
    indent=1,
    default=str,
)
for m, r in out.items():
    print(m)
    for k, v in r.items():
        print(" ", k, "max_err %.2e" % v["max_err"], v["worst"], "fails", v["fails"][:6])
