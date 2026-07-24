"""2xx family - General coverage probability (R files 224 and 225).

These take user-supplied interval limits (LL, UL) rather than a built-in method:

    covpgen  coverage over a user-supplied vector of hypothetical p (hp)
    covpsim  coverage over s simulated Beta(a, b) draws of hypothetical p
"""

import numpy as np

from .base_all import _coverage_core


def _check_limits(n, LL, UL, alp, t1, t2):
    if n is None:
        raise ValueError("'n' is missing")
    if LL is None:
        raise ValueError("'LL' is missing")
    if UL is None:
        raise ValueError("'UL' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if len(LL) != n + 1 or len(UL) != n + 1:
        raise ValueError("'LL' and 'UL' both have to be of length n+1")
    if not 0 <= alp <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if t1 > t2:
        raise ValueError("t1 has to be lesser than t2")


def covpgen(n, LL, UL, alp, hp, t1, t2):
    """Coverage probability for given limits over a given hp vector (R covpGEN)."""
    _check_limits(n, LL, UL, alp, t1, t2)
    if hp is None:
        raise ValueError("'hp' is missing")
    hp = np.atleast_1d(np.asarray(hp, dtype=float))
    if np.any((hp < 0) | (hp > 1)):
        raise ValueError("'hp' has to be between 0 and 1")
    return _coverage_core(n, alp, LL, UL, hp, t1, t2)


def covpsim(n, LL, UL, alp, s, a, b, t1, t2, seed=None):
    """Coverage probability for given limits over s Beta(a, b) draws (R covpSIM)."""
    _check_limits(n, LL, UL, alp, t1, t2)
    if s is None:
        raise ValueError("'s' is missing")
    if not isinstance(s, (int, float)) or s <= 0:
        raise ValueError("'s' has to be greater than 0")
    if not isinstance(a, (int, float)) or a < 0:
        raise ValueError("'a' has to be greater than or equal to 0")
    if not isinstance(b, (int, float)) or b < 0:
        raise ValueError("'b' has to be greater than or equal to 0")
    rng = np.random.default_rng(seed)
    hp = np.sort(rng.beta(a, b, int(s)))
    return _coverage_core(n, alp, LL, UL, hp, t1, t2)
