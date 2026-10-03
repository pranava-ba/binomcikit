"""Lean array access to interval limits: ``limits(n, alpha, method)`` -> ``(lower, upper)``.

:func:`binomcikit.ci` returns a labelled ``DataFrame`` (limits plus the ``LABB`` / ``UABB`` / ``ZWI``
diagnostic flags). Building that frame costs far more than the arithmetic for closed-form
methods, so when you only need the numbers -- a simulation, a benchmark, a tight loop, an
evaluation sweep -- :func:`limits` returns the two ``float64`` arrays directly, computed by the
same vectorised kernels (and clipped into ``[0, 1]`` exactly like the tables).
"""

from __future__ import annotations

import math

import numpy as np
from scipy import special

from . import methods as _methods
from .ci import _fast
from .ci.blaker import _blaker_table
from .ci.bootstrap import ciboot

# method name -> kernel(n, alpha) -> (lower, upper)
_KERNELS = {
    "wald": _fast.wald_arrays,
    "wilson": _fast.wilson_arrays,
    "score": _fast.wilson_arrays,
    "agresti-coull": _fast.agresti_coull_arrays,
    "ac": _fast.agresti_coull_arrays,
    "arcsine": _fast.arcsine_arrays,
    "arc-sine": _fast.arcsine_arrays,
    "logit": _fast.logit_arrays,
    "logit-wald": _fast.logit_arrays,
    "exact": lambda n, a: _fast.exact_limits(n, a, 1.0),
    "clopper-pearson": lambda n, a: _fast.exact_limits(n, a, 1.0),
    "cp": lambda n, a: _fast.exact_limits(n, a, 1.0),
    "midp": lambda n, a: _fast.exact_limits(n, a, 0.5),
    "mid-p": lambda n, a: _fast.exact_limits(n, a, 0.5),
    "jeffreys": _fast.jeffreys_arrays,
    "lr": _fast.lr_limits,
    "likelihood": _fast.lr_limits,
    "likelihood-ratio": _fast.lr_limits,
    "blaker": lambda n, a: _blaker_table(int(n), a),
}


def _wilson1(x, n, a):
    z = _fast.zcrit(a)
    p = x / n
    mid = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + (z / (2 * n)) ** 2)
    c = n / (n + z * z)
    return max(c * (mid - h), 0.0), min(c * (mid + h), 1.0)


def _wald1(x, n, a):
    z = _fast.zcrit(a)
    p = x / n
    h = z * math.sqrt(p * (1 - p) / n)
    return max(p - h, 0.0), min(p + h, 1.0)


def _ac1(x, n, a):
    z = _fast.zcrit(a)
    nt = n + z * z
    pt = (x + z * z / 2) / nt
    h = z * math.sqrt(pt * (1 - pt) / nt)
    return max(pt - h, 0.0), min(pt + h, 1.0)


def _exact1(x, n, a):
    lo = 0.0 if x == 0 else float(special.betaincinv(x, n - x + 1, a / 2))
    hi = 1.0 if x == n else float(special.betaincinv(x + 1, n - x, 1 - a / 2))
    return lo, hi


def _jeffreys1(x, n, a):
    # the plain equal-tailed Beta(x+1/2, n-x+1/2) quantiles, exactly as the table function returns them
    # (use "modified-jeffreys" for the boundary-repaired x = 0 / x = n rows)
    return (
        float(special.betaincinv(x + 0.5, n - x + 0.5, a / 2)),
        float(special.betaincinv(x + 0.5, n - x + 0.5, 1 - a / 2)),
    )


_SCALAR = {
    "wald": _wald1,
    "wilson": _wilson1,
    "score": _wilson1,
    "agresti-coull": _ac1,
    "ac": _ac1,
    "exact": _exact1,
    "clopper-pearson": _exact1,
    "cp": _exact1,
    "jeffreys": _jeffreys1,
}


def interval(x: int, n: int, alpha: float = 0.05, method: str = "wilson", **params):
    """One ``(lower, upper)`` interval for an observed ``x`` of ``n`` as two plain Python floats.

    The fastest way to get a single interval (a few microseconds for the classic methods):
    no ``DataFrame``, no diagnostic flags. Other methods fall back to :func:`limits` (or the
    single-``x`` table row) and return the same tuple.

    Examples
    --------
    >>> import binomcikit as bk
    >>> tuple(round(v, 4) for v in bk.interval(3, 20, 0.05, "wilson"))
    (0.0524, 0.3604)
    """
    if not isinstance(n, (int, np.integer)) or n <= 0:
        raise ValueError("'n' has to be a positive integer")
    if not isinstance(x, (int, np.integer)) or x < 0 or x > n:
        raise ValueError("'x' has to be an integer between 0 and n")
    if not 0 <= alpha <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    key = str(method).lower().strip()
    fn = None if params else _SCALAR.get(key)
    if fn is not None:
        return fn(int(x), int(n), alpha)
    lo, hi = limits(int(n), alpha, method, **params)
    return float(lo[int(x)]), float(hi[int(x)])


def limits(n: int, alpha: float = 0.05, method: str = "wilson", **params):
    """Lower and upper ``(1 - alpha)`` limits for every ``x = 0..n`` as two ``numpy`` arrays.

    The fast path: no ``DataFrame``, no diagnostic flags. Accepts every method name
    :func:`binomcikit.ci` does (closed-form and root-finding methods run on dedicated
    vectorised kernels; the rest fall back to the table functions).

    Parameters
    ----------
    n : int
        Number of trials.
    alpha : float, default 0.05
        Significance level.
    method : str, default "wilson"
        Any method name :func:`binomcikit.ci` accepts, or an extended method from
        :func:`binomcikit.list_methods`.
    **params
        Method options (``lam=``, ``u=``, ``theta=``, ``a=``/``b=`` ...), as for ``ci``.

    Returns
    -------
    tuple of numpy.ndarray
        ``(lower, upper)``, each of length ``n + 1`` and clipped to ``[0, 1]``.

    Examples
    --------
    >>> import binomcikit as bk
    >>> lo, hi = bk.limits(20, 0.05, "wilson")
    >>> lo.shape, round(float(lo[3]), 4), round(float(hi[3]), 4)
    ((21,), 0.0524, 0.3604)
    """
    if not isinstance(n, (int, np.integer)) or n <= 0:
        raise ValueError("'n' has to be a positive integer")
    if not 0 <= alpha <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    key = str(method).lower().strip()
    n = int(n)
    if not params and key in _KERNELS:
        lo, hi = _KERNELS[key](n, alpha)
        return np.asarray(lo, dtype=float), np.asarray(hi, dtype=float)
    spec = _methods.lookup(key)
    if spec is not None:
        df = spec.table(n, alpha, **params)
        return df[spec.lo].to_numpy(float), df[spec.hi].to_numpy(float)
    from .highlevel import ci as _ci

    if key in ("boot", "bootstrap"):
        df = ciboot(
            n,
            alpha,
            B=params.pop("B", 2000),
            seed=params.pop("seed", None),
            kind=params.pop("kind", "smooth"),
        )
    else:
        df = _ci(n=n, alpha=alpha, method=method, **params)
    cols = [c for c in df.columns if c[0] in "LU" and c not in ("LABB", "UABB")]
    return df[cols[0]].to_numpy(float), df[cols[1]].to_numpy(float)
