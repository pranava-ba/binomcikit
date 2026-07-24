"""5xx family - Error and failure of the Bayesian credible interval (R errBA).

Reports the error/failure summary for both the quantile-based and HPD credible
intervals from the 1xx ``ciba``.
"""

import pandas as pd

from ..ci import ciba
from .base_all import _error, _validate


def errba(n, alp, phi, f, a, b):
    """Error/failure of the Bayesian credible interval (R errBA)."""
    _validate(n, alp, phi, f)
    if not isinstance(a, (int, float)) or a < 0:
        raise ValueError("'a' has to be greater than or equal to 0")
    if not isinstance(b, (int, float)) or b < 0:
        raise ValueError("'b' has to be greater than or equal to 0")

    ba = ciba(n, alp, a, b)
    rows = []
    for label, lo, hi in [("Quantile", "LBAQ", "UBAQ"), ("HPD", "LBAH", "UBAH")]:
        row = _error(n, alp, phi, f, ba[lo], ba[hi]).iloc[0].to_dict()
        row["method"] = label
        rows.append(row)
    out = pd.DataFrame(rows)
    return out[["method", "delalp", "theta", "Fail_Pass"]]
