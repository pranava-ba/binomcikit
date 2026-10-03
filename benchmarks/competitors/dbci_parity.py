import json
import os
import sys
import warnings

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src"))
import diff_binom_confint as d
import numpy as np

import binomcikit as bk

print("DBCI from", d.__file__)
print([m for m in bk.list_methods()][:0])
A = 0.05
pairs = {
    "wilson": "wilson",
    "wilson-cc": "wilson-cc",
    "wald": "wald",
    "wald-cc": "wald-cc",
    "agresti-coull": "agresti-coull",
    "jeffreys": "jeffreys",
    "clopper-pearson": "exact",
    "arcsine": "arcsine",
    "logit": "logit",
    "pratt": "pratt",
    "mid-p": "midp",
    "lik": "lr",
    "blaker": "blaker",
    "witting": "witting",
    "modified-wilson": None,
    "modified-jeffreys": None,
    "modified-newcombe": None,
}
names = set(getattr(bk, "list_methods")() if not hasattr(bk.list_methods(), "name") else [])
try:
    ml = bk.list_methods()
    names = {str(m) for m in (ml.index if hasattr(ml, "index") else ml)}
    if hasattr(ml, "columns"):
        names |= {str(v) for v in ml.iloc[:, 0]}
except Exception as e:
    print("lm", e)
res = {}
for n in (20, 100):
    for dm, bm in pairs.items():
        if bm is None:
            continue
        try:
            lo, hi = bk.limits(n, A, bm)
        except Exception as e:
            res[f"{dm}/n={n}"] = f"bk-err {type(e).__name__}"
            continue
        dl = np.empty(n + 1)
        du = np.empty(n + 1)
        try:
            for x in range(n + 1):
                c = d.compute_confidence_interval(x, n, 1 - A, dm)
                dl[x], du[x] = c.lower_bound, c.upper_bound
        except Exception as e:
            res[f"{dm}/n={n}"] = f"dbci-err {type(e).__name__}: {str(e)[:50]}"
            continue
        inner = slice(1, n)
        e = max(np.nanmax(np.abs(dl[inner] - lo[inner])), np.nanmax(np.abs(du[inner] - hi[inner])))
        eb = max(abs(dl[0] - lo[0]), abs(du[0] - hi[0]), abs(dl[n] - lo[n]), abs(du[n] - hi[n]))
        res[f"{dm}/n={n}"] = (float(e), float(eb))
for k, v in res.items():
    print(k, v)
json.dump(res, open(sys.argv[1], "w"), indent=1)
