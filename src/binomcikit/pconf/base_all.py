"""4xx family - p-confidence and p-bias for the base CI methods (R file 401).

For each interior x (1..n-1) the interval limits give two tail probabilities;
p-confidence is 100*(1 - max tail) and p-bias is 100*max(0, tail difference).
These quantities are deterministic - there is no simulation - so results match
the R package exactly (up to floating point).

Interval limits are reused from the 1xx ``ci`` family.
"""

import numpy as np
import pandas as pd
import scipy.stats as stats

from ..ci import cias, ciex, cilr, cilt, cisc, citw, ciwd


def _validate(n, alp):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not 0 <= alp <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")


def _pconf_pbias(n, lower, upper):
    """p-confidence and p-bias per interior x, given interval limits (R 401)."""
    lower = np.asarray(lower, dtype=float)
    upper = np.asarray(upper, dtype=float)
    x1 = np.arange(1, n)  # interior successes 1..n-1
    pconf = np.empty(len(x1))
    pbias = np.empty(len(x1))
    for idx, x in enumerate(x1):
        L, U = lower[x], upper[x]
        # R: pbinom(x, n, L, lower.tail=FALSE) = sf(x); + dbinom(x, n, L)
        pcon = 2.0 * (stats.binom.sf(x, n, L) + stats.binom.pmf(x, n, L))
        # R: pbinom(x, n, U, lower.tail=TRUE) = cdf(x)
        pconC = 2.0 * stats.binom.cdf(x, n, U)
        hi = max(pcon, pconC)
        lo = min(pcon, pconC)
        pconf[idx] = (1.0 - hi) * 100.0
        pbias[idx] = max(0.0, hi - lo) * 100.0
    return pd.DataFrame({"x1": x1, "pconf": pconf, "pbias": pbias})


_BASE = {
    "Wald": (ciwd, "LWD", "UWD"),
    "ArcSine": (cias, "LAS", "UAS"),
    "Likelihood": (cilr, "LLR", "ULR"),
    "Score": (cisc, "LSC", "USC"),
    "Wald-T": (citw, "LTW", "UTW"),
    "Logit-Wald": (cilt, "LLT", "ULT"),
}


def _base(method, n, alp):
    fn, lo, hi = _BASE[method]
    df = fn(n, alp)
    return _pconf_pbias(n, df[lo], df[hi])


def pcopbiwd(n, alp):
    """p-confidence and p-bias of the Wald interval (R pCOpBIWD)."""
    _validate(n, alp)
    return _base("Wald", n, alp)


def pcopbisc(n, alp):
    """p-confidence and p-bias of the Score interval (R pCOpBISC)."""
    _validate(n, alp)
    return _base("Score", n, alp)


def pcopbias(n, alp):
    """p-confidence and p-bias of the ArcSine interval (R pCOpBIAS)."""
    _validate(n, alp)
    return _base("ArcSine", n, alp)


def pcopbilr(n, alp):
    """p-confidence and p-bias of the Likelihood-Ratio interval (R pCOpBILR)."""
    _validate(n, alp)
    return _base("Likelihood", n, alp)


def pcopbilt(n, alp):
    """p-confidence and p-bias of the Logit-Wald interval (R pCOpBILT)."""
    _validate(n, alp)
    return _base("Logit-Wald", n, alp)


def pcopbitw(n, alp):
    """p-confidence and p-bias of the Wald-T interval (R pCOpBITW)."""
    _validate(n, alp)
    return _base("Wald-T", n, alp)


def pcopbiex(n, alp, e):
    """p-confidence and p-bias of the Exact interval (R pCOpBIEX)."""
    _validate(n, alp)
    if e is None:
        raise ValueError("'e' is missing")
    df = ciex(n, alp, [e])
    return _pconf_pbias(n, df["LEX"], df["UEX"])


def pcopbiall(n, alp):
    """p-confidence and p-bias for all six base methods (R pCOpBIAll)."""
    _validate(n, alp)
    frames = []
    for name in _BASE:
        d = _base(name, n, alp)
        d["method"] = name
        frames.append(d)
    return pd.concat(frames, ignore_index=True)[["method", "x1", "pconf", "pbias"]]
