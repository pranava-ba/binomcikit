"""4xx family - p-confidence and p-bias of the Bayesian credible interval (R pCOpBIBA).

Reports p-confidence and p-bias for both the quantile-based (Q) and HPD (H)
credible intervals from the 1xx ``ciba``.
"""
import pandas as pd

from ..ci import ciba
from .base_all import _pconf_pbias, _validate


def pcopbiba(n, alp, a1, a2):
    """p-confidence and p-bias of the Bayesian credible interval (R pCOpBIBA)."""
    _validate(n, alp)
    if not isinstance(a1, (int, float)) or a1 < 0:
        raise ValueError("'a1' has to be greater than or equal to 0")
    if not isinstance(a2, (int, float)) or a2 < 0:
        raise ValueError("'a2' has to be greater than or equal to 0")

    ba = ciba(n, alp, a1, a2)
    q = _pconf_pbias(n, ba['LBAQ'], ba['UBAQ'])
    h = _pconf_pbias(n, ba['LBAH'], ba['UBAH'])
    return pd.DataFrame({
        'x1': q['x1'],
        'pconfQ': q['pconf'], 'pbiasQ': q['pbias'],
        'pconfH': h['pconf'], 'pbiasH': h['pbias'],
    })
