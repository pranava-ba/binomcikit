"""3xx family - Expected length of the Bayesian credible interval (R lengthBA).

Reports the expected length for both the quantile-based and HPD credible
intervals (from the 1xx ``ciba``), over hypothetical p drawn from Beta(a, b).
The ``a1, a2`` prior defines the credible interval; ``a, b`` the simulation prior.
"""
import numpy as np
import pandas as pd

from ..ci import ciba
from .base_all import _validate, _expl_series, _expl_summary, _beta_hp


def lengthba(n, alp, a, b, a1, a2, seed=None):
    """Expected length of the Bayesian credible interval (R lengthBA)."""
    _validate(n, alp, a, b)
    if not isinstance(a1, (int, float)) or a1 < 0:
        raise ValueError("'a1' has to be greater than or equal to 0")
    if not isinstance(a2, (int, float)) or a2 < 0:
        raise ValueError("'a2' has to be greater than or equal to 0")

    ba = ciba(n, alp, a1, a2)
    hp = _beta_hp(a, b, seed)
    rows = []
    for label, lo, hi in [("Quantile", 'LBAQ', 'UBAQ'), ("HPD", 'LBAH', 'UBAH')]:
        lengths = ba[hi].to_numpy() - ba[lo].to_numpy()
        ew = _expl_series(n, lengths, hp)
        row = _expl_summary(lengths, ew).iloc[0].to_dict()
        row['method'] = label
        rows.append(row)
    out = pd.DataFrame(rows)
    return out[['method', 'sumLen', 'explMean', 'explSD', 'explMax',
                'explLL', 'explUL']]
