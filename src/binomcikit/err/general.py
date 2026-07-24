"""5xx family - General error and failure (R file 523).

errgen  error/failure summary for user-supplied interval limits
"""

import numpy as np

from .base_all import _error


def errgen(n, LL, UL, alp, phi, f):
    """Error/failure for given limits (R errGEN)."""
    if n is None:
        raise ValueError("'n' is missing")
    if LL is None:
        raise ValueError("'LL' is missing")
    if UL is None:
        raise ValueError("'UL' is missing")
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
    LL = np.asarray(LL, dtype=float)
    UL = np.asarray(UL, dtype=float)
    if len(LL) < n + 1 or len(UL) < n + 1:
        raise ValueError("'LL' and 'UL' both have to be of length n+1")
    return _error(n, alp, phi, f, LL, UL)
