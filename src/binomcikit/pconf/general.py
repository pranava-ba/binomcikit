"""4xx family - General p-confidence and p-bias (R file 423).

pcopbigen  p-confidence and p-bias for user-supplied interval limits
"""

import numpy as np

from .base_all import _pconf_pbias


def pcopbigen(n, LL, UL):
    """p-confidence and p-bias for given limits (R pCOpBIGEN)."""
    if n is None:
        raise ValueError("'n' is missing")
    if LL is None:
        raise ValueError("'Lower limit' is missing")
    if UL is None:
        raise ValueError("'Upper Limit' is missing")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    LL = np.asarray(LL, dtype=float)
    UL = np.asarray(UL, dtype=float)
    if np.any(LL < 0) or np.any(UL < 0):
        raise ValueError("'LL' and 'UL' have to be positive")
    if len(LL) < n + 1 or len(UL) < n + 1:
        raise ValueError("'LL' and 'UL' both have to be of length n+1")
    if np.any(LL[: n + 1] > UL[: n + 1]):
        raise ValueError("LL values have to be lower than the corresponding UL")
    return _pconf_pbias(n, LL, UL)
