"""Optional numba-accelerated kernels, with a transparent numpy fallback.

The metric engines (coverage, expected length, ...) are vectorised in numpy, which is excellent for
the common small-``n`` case. For **large ``n``** the vectorised form materialises a dense
``|hp| x (n+1)`` PMF matrix and slows down badly (see ``benchmarks/``); there a compiled kernel that
skips uncovered ``x`` is 10-40x faster. If ``numba`` is installed (``pip install binomcikit[fast]``) it
is used automatically for large workloads; otherwise everything falls back to numpy and results are
identical.

numba is imported **lazily**, the first time a compiled kernel is actually needed (and compiled with
``cache=True``, so later processes load it from disk): ``import binomcikit`` no longer pays numba's
~0.5 s import for users who never hit a large-``n`` workload.
"""

import importlib.util
from math import exp, lgamma, log

import numpy as np

HAS_NUMBA = importlib.util.find_spec("numba") is not None


def _coverage_py(n, lower, upper, hp):  # pragma: no cover - compiled by numba
    """Coverage prob at each hp: sum of binomial PMF over covered x.

    Computes the PMF via ``lgamma``/``exp`` only for the ``x`` actually inside the interval, so it
    never builds the full matrix. ``log(p)``/``log(1-p)`` at the p in {0, 1} edges are never used
    because no ``x`` is covered there.
    """
    S = hp.shape[0]
    out = np.empty(S)
    lfn = lgamma(n + 1.0)
    for j in range(S):
        p = hp[j]
        lp = log(p)
        lq = log(1.0 - p)
        s = 0.0
        for k in range(n + 1):
            if lower[k] < p < upper[k]:
                s += exp(lfn - lgamma(k + 1.0) - lgamma(n - k + 1.0) + k * lp + (n - k) * lq)
        out[j] = s
    return out


_kernel = None


def _coverage_numba(n, lower, upper, hp):
    """The compiled coverage kernel (compiled on first use; raises ``ImportError`` without numba)."""
    global _kernel
    if _kernel is None:
        from numba import njit

        _kernel = njit(cache=True, fastmath=True)(_coverage_py)
    return _kernel(n, lower, upper, hp)


# Use the compiled kernel only once the dense PMF matrix is big enough that numpy is clearly slow;
# below this, numpy wins and avoids numba's JIT warm-up.
_NUMBA_MIN_CELLS = 2_000_000  # ~ |hp| * (n + 1)


def coverage_series(n, lower, upper, hp):
    """Coverage probability at each hp — numba for large workloads, else numpy."""
    lower = np.ascontiguousarray(lower, dtype=float)
    upper = np.ascontiguousarray(upper, dtype=float)
    hp = np.ascontiguousarray(hp, dtype=float)
    if HAS_NUMBA and hp.shape[0] * (n + 1) >= _NUMBA_MIN_CELLS:
        return _coverage_numba(n, lower, upper, hp)
    return _coverage_numpy(n, lower, upper, hp)


def pmf_matrix(n, theta):
    """Binomial pmf as a ``(len(theta), n + 1)`` matrix, from logs.

    ~10x cheaper than ``scipy.stats.binom.pmf``'s argument handling for a grid of ``theta``, and the
    same value (``xlogy`` / ``xlog1py`` make the ``theta = 0`` and ``1`` edges exact).
    """
    from scipy.special import gammaln, xlog1py, xlogy

    theta = np.asarray(theta, dtype=float)
    x = np.arange(n + 1)
    lchoose = gammaln(n + 1.0) - gammaln(x + 1.0) - gammaln(n - x + 1.0)
    return np.exp(
        lchoose[None, :]
        + xlogy(x[None, :], theta[:, None])
        + xlog1py((n - x)[None, :], -theta[:, None])
    )


def _coverage_numpy(n, lower, upper, hp):
    covered = (hp[:, None] > lower[None, :]) & (hp[:, None] < upper[None, :])
    return (pmf_matrix(n, hp) * covered).sum(axis=1)
