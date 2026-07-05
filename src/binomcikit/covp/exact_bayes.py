"""2xx family - Coverage probability for the Exact and Bayesian intervals.

covpex reuses the Exact interval (ciex); covpba reuses the Bayesian credible
interval (ciba), reporting coverage for both its quantile and HPD variants.
"""
import pandas as pd

from ..ci import ciex, ciba
from .base_all import _validate, _coverage


def covpex(n, alp, e, a, b, t1, t2, seed=None):
    """Coverage probability of the Exact interval (R covpEX)."""
    _validate(n, alp, a, b, t1, t2)
    if e is None:
        raise ValueError("'e' is missing")
    df = ciex(n, alp, [e])
    return _coverage(n, alp, a, b, t1, t2, df['LEX'], df['UEX'], seed)


def covpba(n, alp, a, b, t1, t2, a1, a2, seed=None):
    """Coverage probability of the Bayesian credible interval (R covpBA).

    ``a1, a2`` set the credible-interval prior; ``a, b`` the simulation prior.
    Returns coverage for both the quantile-based and HPD credible intervals.
    """
    _validate(n, alp, a, b, t1, t2)
    if not isinstance(a1, (int, float)) or a1 < 0:
        raise ValueError("'a1' has to be greater than or equal to 0")
    if not isinstance(a2, (int, float)) or a2 < 0:
        raise ValueError("'a2' has to be greater than or equal to 0")
    ba = ciba(n, alp, a1, a2)
    rows = []
    for label, lo, hi in [("Quantile", 'LBAQ', 'UBAQ'), ("HPD", 'LBAH', 'UBAH')]:
        row = _coverage(n, alp, a, b, t1, t2, ba[lo], ba[hi], seed).iloc[0].to_dict()
        row['method'] = label
        rows.append(row)
    out = pd.DataFrame(rows)
    return out[['method', 'mcp', 'micp', 'RMSE_N', 'RMSE_M', 'RMSE_MI', 'tol']]
