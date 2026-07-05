"""5xx family - Error and failure (limit-based) for the base CI methods (R file 501).

For a null hypothesis proportion ``phi`` and a failure threshold ``f``:

    delalp      100 * (alp - sum of binomial mass at x where phi is excluded)
    theta       100 * (fraction of x for which phi falls outside the interval)
    Fail_Pass   "failure" if delalp < f else "success"

These quantities are deterministic (no simulation). Interval limits are reused
from the 1xx ``ci`` family.
"""
import numpy as np
import pandas as pd
import scipy.stats as stats

from ..ci import ciwd, cisc, cias, cilr, citw, cilt, ciex


def _validate(n, alp, phi, f):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if phi is None:
        raise ValueError("'phi' is missing")
    if f is None:
        raise ValueError("'f' is missing")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not 0 <= alp <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(phi, (int, float)) or not 0 <= phi <= 1:
        raise ValueError("Null hypothesis 'phi' has to be between 0 and 1")
    if not isinstance(f, (int, float)):
        raise ValueError("'f' has to be numeric value")


def _error(n, alp, phi, f, lower, upper):
    """delta-alpha / theta / failure summary given interval limits (R 501)."""
    lower = np.asarray(lower, dtype=float)
    upper = np.asarray(upper, dtype=float)
    x = np.arange(n + 1)

    outside = (phi > upper) | (phi < lower)
    alpstar = np.where(outside, stats.binom.pmf(x, n, phi), 0.0)
    thetactr = int(np.sum(outside))

    delalp = round((alp - np.sum(alpstar)) * 100, 2)
    theta = round(100.0 * thetactr / (n + 1), 2)
    fail_pass = "failure" if delalp < f else "success"
    return pd.DataFrame([{'delalp': delalp, 'theta': theta,
                          'Fail_Pass': fail_pass}])


_BASE = {
    "Wald": (ciwd, 'LWD', 'UWD'), "ArcSine": (cias, 'LAS', 'UAS'),
    "Likelihood": (cilr, 'LLR', 'ULR'), "Score": (cisc, 'LSC', 'USC'),
    "Wald-T": (citw, 'LTW', 'UTW'), "Logit-Wald": (cilt, 'LLT', 'ULT'),
}


def _base(method, n, alp, phi, f):
    fn, lo, hi = _BASE[method]
    df = fn(n, alp)
    return _error(n, alp, phi, f, df[lo], df[hi])


def errwd(n, alp, phi, f):
    """Error/failure of the Wald interval (R errWD)."""
    _validate(n, alp, phi, f)
    return _base("Wald", n, alp, phi, f)


def errsc(n, alp, phi, f):
    """Error/failure of the Score interval (R errSC)."""
    _validate(n, alp, phi, f)
    return _base("Score", n, alp, phi, f)


def erras(n, alp, phi, f):
    """Error/failure of the ArcSine interval (R errAS)."""
    _validate(n, alp, phi, f)
    return _base("ArcSine", n, alp, phi, f)


def errlr(n, alp, phi, f):
    """Error/failure of the Likelihood-Ratio interval (R errLR)."""
    _validate(n, alp, phi, f)
    return _base("Likelihood", n, alp, phi, f)


def errlt(n, alp, phi, f):
    """Error/failure of the Logit-Wald interval (R errLT)."""
    _validate(n, alp, phi, f)
    return _base("Logit-Wald", n, alp, phi, f)


def errtw(n, alp, phi, f):
    """Error/failure of the Wald-T interval (R errTW)."""
    _validate(n, alp, phi, f)
    return _base("Wald-T", n, alp, phi, f)


def errex(n, alp, phi, f, e):
    """Error/failure of the Exact interval (R errEX)."""
    _validate(n, alp, phi, f)
    if e is None:
        raise ValueError("'e' is missing")
    df = ciex(n, alp, [e])
    return _error(n, alp, phi, f, df['LEX'], df['UEX'])


def errall(n, alp, phi, f):
    """Error/failure for all six base methods (R errAll)."""
    _validate(n, alp, phi, f)
    frames = []
    for name in _BASE:
        d = _base(name, n, alp, phi, f)
        d['method'] = name
        frames.append(d)
    return pd.concat(frames, ignore_index=True)[
        ['method', 'delalp', 'theta', 'Fail_Pass']]
