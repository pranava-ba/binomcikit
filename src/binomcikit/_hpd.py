"""Highest posterior density (HPD) interval for a Beta distribution.

Reimplements ``TeachingDemos::hpd(qbeta, shape1=a, shape2=b, conf=...)`` used
throughout the R package: it finds the shortest interval [lo, hi] whose Beta
probability mass equals ``conf`` by minimising the width over the lower-tail
probability.
"""
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import beta


def hpd_beta(a, b, conf=0.95):
    """Return (lower, upper) of the HPD interval of Beta(a, b) at level conf."""
    alpha = 1.0 - conf

    # Degenerate priors can make ppf(0) or ppf(1) non-finite; the shortest
    # interval then sits at a boundary, which the bounded search below finds.
    def width(p):
        lo = beta.ppf(p, a, b)
        hi = beta.ppf(p + conf, a, b)
        return hi - lo

    res = minimize_scalar(width, bounds=(0.0, alpha), method="bounded",
                          options={"xatol": 1e-8})
    p = res.x
    lo = float(beta.ppf(p, a, b))
    hi = float(beta.ppf(p + conf, a, b))
    if not np.isfinite(lo):
        lo = 0.0
    if not np.isfinite(hi):
        hi = 1.0
    return lo, hi
