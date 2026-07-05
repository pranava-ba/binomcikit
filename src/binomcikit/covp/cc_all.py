"""2xx family - Coverage probability for the continuity-corrected CI methods (R file 221).

Subtracts/adds a continuity correction ``c`` to the interval limits. The CC
interval limits are reused from the 1xx ``ci`` continuity-corrected family; the
coverage simulation engine is shared with :mod:`binomcikit.covp.base_all`.

Note: continuity correction is defined for five methods (no Likelihood-Ratio).
"""
import pandas as pd

from ..ci import cicas, ciclt, cicsc, cictw, cicwd
from .base_all import _coverage, _validate


def _validate_cc(n, alp, c, a, b, t1, t2):
    if c is None:
        raise ValueError("'c' is missing")
    if not isinstance(c, (int, float)) or c < 0:
        raise ValueError("'c' has to be positive")
    _validate(n, alp, a, b, t1, t2)


def covpcwd(n, alp, c, a, b, t1, t2, seed=None):
    """Coverage probability of the continuity-corrected Wald interval (R covpCWD)."""
    _validate_cc(n, alp, c, a, b, t1, t2)
    df = cicwd(n, alp, c)
    return _coverage(n, alp, a, b, t1, t2, df['LCW'], df['UCW'], seed)


def covpcsc(n, alp, c, a, b, t1, t2, seed=None):
    """Coverage probability of the continuity-corrected Score interval (R covpCSC)."""
    _validate_cc(n, alp, c, a, b, t1, t2)
    df = cicsc(n, alp, c)
    return _coverage(n, alp, a, b, t1, t2, df['LCS'], df['UCS'], seed)


def covpcas(n, alp, c, a, b, t1, t2, seed=None):
    """Coverage probability of the continuity-corrected ArcSine interval (R covpCAS)."""
    _validate_cc(n, alp, c, a, b, t1, t2)
    df = cicas(n, alp, c)
    return _coverage(n, alp, a, b, t1, t2, df['LCA'], df['UCA'], seed)


def covpclt(n, alp, c, a, b, t1, t2, seed=None):
    """Coverage probability of the continuity-corrected Logit-Wald interval (R covpCLT)."""
    _validate_cc(n, alp, c, a, b, t1, t2)
    df = ciclt(n, alp, c)
    return _coverage(n, alp, a, b, t1, t2, df['LCLT'], df['UCLT'], seed)


def covpctw(n, alp, c, a, b, t1, t2, seed=None):
    """Coverage probability of the continuity-corrected Wald-T interval (R covpCTW)."""
    _validate_cc(n, alp, c, a, b, t1, t2)
    df = cictw(n, alp, c)
    return _coverage(n, alp, a, b, t1, t2, df['LCTW'], df['UCTW'], seed)


def covpcall(n, alp, c, a, b, t1, t2, seed=None):
    """Coverage probability summary for all five CC methods (R covpCAll)."""
    _validate_cc(n, alp, c, a, b, t1, t2)
    methods = {
        'Wald': covpcwd, 'ArcSine': covpcas, 'Score': covpcsc,
        'Wald-T': covpctw, 'Logit-Wald': covpclt,
    }
    rows = []
    for name, fn in methods.items():
        row = fn(n, alp, c, a, b, t1, t2, seed).iloc[0].to_dict()
        row['method'] = name
        rows.append(row)
    out = pd.DataFrame(rows)
    return out[['method', 'mcp', 'micp', 'RMSE_N', 'RMSE_M', 'RMSE_MI', 'tol']]
