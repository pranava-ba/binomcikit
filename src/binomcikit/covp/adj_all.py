"""2xx family - Coverage probability for the adjusted CI methods (R file 212).

Adds ``h`` pseudo-counts to x (and 2h to n) before forming the interval. The
adjusted interval limits are reused from the 1xx ``ci`` adjusted family; the
coverage simulation engine is shared with :mod:`binomcikit.covp.base_all`.
"""

from ..ci import ciaas, cialr, cialt, ciasc, ciatw, ciawd
from .base_all import _coverage, _validate


def _validate_adj(n, alp, h, a, b, t1, t2):
    if h is None:
        raise ValueError("'h' is missing")
    if not isinstance(h, (int, float)) or h < 0:
        raise ValueError("'h' has to be greater than or equal to 0")
    _validate(n, alp, a, b, t1, t2)


def covpawd(n, alp, h, a, b, t1, t2, seed=None):
    """Coverage probability of the adjusted Wald interval (R covpAWD)."""
    _validate_adj(n, alp, h, a, b, t1, t2)
    df = ciawd(n, alp, h)
    return _coverage(n, alp, a, b, t1, t2, df["LAWD"], df["UAWD"], seed)


def covpasc(n, alp, h, a, b, t1, t2, seed=None):
    """Coverage probability of the adjusted Score interval (R covpASC)."""
    _validate_adj(n, alp, h, a, b, t1, t2)
    df = ciasc(n, alp, h)
    return _coverage(n, alp, a, b, t1, t2, df["LASC"], df["UASC"], seed)


def covpaas(n, alp, h, a, b, t1, t2, seed=None):
    """Coverage probability of the adjusted ArcSine interval (R covpAAS)."""
    _validate_adj(n, alp, h, a, b, t1, t2)
    df = ciaas(n, alp, h)
    return _coverage(n, alp, a, b, t1, t2, df["LAAS"], df["UAAS"], seed)


def covpalt(n, alp, h, a, b, t1, t2, seed=None):
    """Coverage probability of the adjusted Logit-Wald interval (R covpALT)."""
    _validate_adj(n, alp, h, a, b, t1, t2)
    df = cialt(n, alp, h)
    return _coverage(n, alp, a, b, t1, t2, df["LALT"], df["UALT"], seed)


def covpatw(n, alp, h, a, b, t1, t2, seed=None):
    """Coverage probability of the adjusted Wald-T interval (R covpATW)."""
    _validate_adj(n, alp, h, a, b, t1, t2)
    df = ciatw(n, alp, h)
    return _coverage(n, alp, a, b, t1, t2, df["LATW"], df["UATW"], seed)


def covpalr(n, alp, h, a, b, t1, t2, seed=None):
    """Coverage probability of the adjusted Likelihood-Ratio interval (R covpALR)."""
    _validate_adj(n, alp, h, a, b, t1, t2)
    df = cialr(n, alp, h)
    return _coverage(n, alp, a, b, t1, t2, df["LALR"], df["UALR"], seed)


def covpaall(n, alp, h, a, b, t1, t2, seed=None):
    """Coverage probability summary for all six adjusted methods (R covpAAll)."""
    _validate_adj(n, alp, h, a, b, t1, t2)
    methods = {
        "Wald": covpawd,
        "ArcSine": covpaas,
        "Likelihood": covpalr,
        "Score": covpasc,
        "Wald-T": covpatw,
        "Logit-Wald": covpalt,
    }
    import pandas as pd

    rows = []
    for name, fn in methods.items():
        row = fn(n, alp, h, a, b, t1, t2, seed).iloc[0].to_dict()
        row["method"] = name
        rows.append(row)
    out = pd.DataFrame(rows)
    return out[["method", "mcp", "micp", "RMSE_N", "RMSE_M", "RMSE_MI", "tol"]]
