"""Shared helpers for the extended-method subpackage.

Every extended method is a *limit-producer*: it returns the same ``(n+1)``-row table
as the original ``ci*`` functions (``x``, lower, upper, ``LABB``/``UABB``/``ZWI``
flags), so the whole metric engine (coverage, expected length, p-confidence/p-bias,
error, plots, ``compare``/``recommend``) consumes it unchanged.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def validate(n, alp):
    """Same input contract as the original ``ci*`` functions."""
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if not 0 <= alp <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, np.integer, float)) or n <= 0 or int(n) != n:
        raise ValueError("'n' has to be a positive integer")
    return int(n)


def check_x(x, n):
    if x is None:
        raise ValueError("'x' is missing")
    if not isinstance(x, (int, np.integer)) or x < 0 or x > n:
        raise ValueError("'x' has to be an integer between 0 and n")
    return int(x)


def table(code, lower, upper, clamp=True):
    """Assemble the standard limits table from raw limit vectors.

    The ``LABB``/``UABB`` flags record whether a *raw* limit fell outside
    ``[0, 1]`` (an "aberration") before it was clamped, exactly as the original
    methods do.
    """
    lower = np.asarray(lower, dtype=float)
    upper = np.asarray(upper, dtype=float)
    labb = np.where(lower < 0, "YES", "NO").astype(object)
    uabb = np.where(upper > 1, "YES", "NO").astype(object)
    if clamp:
        lower = np.maximum(lower, 0.0)
        upper = np.minimum(upper, 1.0)
    zwi = np.where(upper - lower == 0, "YES", "NO").astype(object)
    return pd.DataFrame(
        {
            "x": np.arange(lower.shape[0]),
            f"L{code}": lower,
            f"U{code}": upper,
            "LABB": labb,
            "UABB": uabb,
            "ZWI": zwi,
        }
    )


def single(df, x, code):
    """One row of a full table, with the original ``...x`` column naming."""
    row = df.iloc[[x]].reset_index(drop=True)
    return row.rename(columns={f"L{code}": f"L{code}x", f"U{code}": f"U{code}x"})


def bisect_monotone(f, lo, hi, increasing, iters=60):
    """Vectorised bisection for the root of a monotone function.

    ``f`` maps an array of abscissae to an array of values; ``lo``/``hi`` are
    arrays of brackets (one per row). ``increasing`` says whether ``f`` rises
    through zero between them. Returns the midpoint after ``iters`` halvings
    (~1e-18 of the bracket), so root-finding for every ``x`` happens in a handful
    of numpy calls instead of ``n+1`` scalar ``brentq`` loops.
    """
    lo = np.array(lo, dtype=float)
    hi = np.array(hi, dtype=float)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        above = f(mid) > 0
        if increasing:
            hi = np.where(above, mid, hi)
            lo = np.where(above, lo, mid)
        else:
            lo = np.where(above, mid, lo)
            hi = np.where(above, hi, mid)
    return 0.5 * (lo + hi)
