"""3xx family - General expected length (R file 328).

    lengthgen  expected length for given limits over a given hp vector
    lengthsim  expected length for given limits over s simulated Beta(a, b) draws
"""
import numpy as np

from .base_all import _expl_series, _expl_summary


def _check_limits(n, LL, UL):
    if n is None:
        raise ValueError("'n' is missing")
    if LL is None:
        raise ValueError("'LL' is missing")
    if UL is None:
        raise ValueError("'UL' is missing")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if len(LL) != n + 1 or len(UL) != n + 1:
        raise ValueError("'LL' and 'UL' both have to be of length n+1")


def lengthgen(n, LL, UL, hp):
    """Expected length for given limits over a given hp vector (R lengthGEN)."""
    _check_limits(n, LL, UL)
    if hp is None:
        raise ValueError("'hp' is missing")
    hp = np.atleast_1d(np.asarray(hp, dtype=float))
    if np.any((hp < 0) | (hp > 1)):
        raise ValueError("'hp' has to be between 0 and 1")
    lengths = np.asarray(UL, dtype=float) - np.asarray(LL, dtype=float)
    ew = _expl_series(n, lengths, hp)
    return _expl_summary(lengths, ew)


def lengthsim(n, LL, UL, s, a, b, seed=None):
    """Expected length for given limits over s Beta(a, b) draws (R lengthSIM)."""
    _check_limits(n, LL, UL)
    if s is None:
        raise ValueError("'s' is missing")
    if not isinstance(s, (int, float)) or s <= 0:
        raise ValueError("'s' has to be greater than 0")
    if not isinstance(a, (int, float)) or a < 0:
        raise ValueError("'a' has to be greater than or equal to 0")
    if not isinstance(b, (int, float)) or b < 0:
        raise ValueError("'b' has to be greater than or equal to 0")
    hp = np.sort(np.random.default_rng(seed).beta(a, b, int(s)))
    lengths = np.asarray(UL, dtype=float) - np.asarray(LL, dtype=float)
    ew = _expl_series(n, lengths, hp)
    return _expl_summary(lengths, ew)
