import json
import os
import sys
import time
import warnings

warnings.filterwarnings("ignore")
import numpy as np
import psutil

pkg, method, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
p = psutil.Process()
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src"))
k = np.arange(n + 1)
A = 0.05
if pkg == "binomcikit.ci":
    import binomcikit as bk

    f = lambda: bk.ci(n=n, alpha=A, method=method)
elif pkg == "binomcikit.limits":
    import binomcikit as bk

    f = lambda: bk.limits(n, A, method)
elif pkg == "statsmodels":
    from statsmodels.stats.proportion import proportion_confint as pc

    m = {"wilson": "wilson", "exact": "beta"}[method]
    f = lambda: pc(k, n, alpha=A, method=m)
elif pkg == "astropy":
    from astropy.stats import binom_conf_interval as b

    f = lambda: b(k, n, confidence_level=1 - A, interval="wilson")
elif pkg == "DBCI":
    import diff_binom_confint as d

    m = {"wilson": "wilson", "exact": "clopper-pearson"}[method]
    f = lambda: [d.compute_confidence_interval(i, n, 1 - A, m) for i in range(n + 1)]
elif pkg == "binoculars":
    import binoculars as b

    m = {"wilson": "wilson", "exact": "clopper-pearson"}[method]
    f = lambda: [b.binomial_confidence(i / n, n, method=m) for i in range(n + 1)]
elif pkg == "scipy":
    from scipy.stats import binomtest

    m = {"wilson": "wilson", "exact": "exact"}[method]
    f = lambda: [
        binomtest(i, n).proportion_ci(confidence_level=1 - A, method=m) for i in range(n + 1)
    ]
f.__call__  # warm small
import gc

gc.collect()
base = p.memory_info().rss  # after import
mi = p.memory_info()
peak0 = mi.peak_wset
t = time.perf_counter()
f()
dt = time.perf_counter() - t
peak = p.memory_info().peak_wset
print(
    json.dumps(
        {
            "pkg": pkg,
            "method": method,
            "n": n,
            "after_import_mb": base / 2**20,
            "peak_mb": peak / 2**20,
            "delta_mb": (peak - max(peak0, base)) / 2**20,
            "s": dt,
        }
    )
)
