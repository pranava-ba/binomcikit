"""Optional numba-accelerated kernels, with a transparent numpy fallback.

The metric engines (coverage, expected length, …) are vectorised in numpy, which
is excellent for the common small-``n`` case. For **large ``n``** the vectorised
form materialises a dense ``|hp| x (n+1)`` PMF matrix and slows down badly (see
``benchmarks/``); there a compiled kernel that skips uncovered ``x`` is 10–40x
faster. If ``numba`` is installed (``pip install binomcikit[fast]``) it is used
automatically for large workloads; otherwise everything falls back to numpy and
results are identical.
"""

import numpy as np

try:
    from math import exp, lgamma, log

    from numba import njit

    @njit(cache=True, fastmath=True)
    def _coverage_numba(n, lower, upper, hp):  # pragma: no cover - compiled
        """Coverage prob at each hp: sum of binomial PMF over covered x.

        Computes the PMF via ``lgamma``/``exp`` only for the ``x`` actually inside
        the interval, so it never builds the full matrix. ``log(p)``/``log(1-p)``
        at the p in {0, 1} edges are never used because no ``x`` is covered there.
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

    HAS_NUMBA = True
except Exception:  # pragma: no cover - numba not installed
    HAS_NUMBA = False

# Use the compiled kernel only once the dense PMF matrix is big enough that numpy
# is clearly slow; below this, numpy wins and avoids numba's JIT warm-up.
_NUMBA_MIN_CELLS = 2_000_000  # ~ |hp| * (n + 1)


def coverage_series(n, lower, upper, hp):
    """Coverage probability at each hp — numba for large workloads, else numpy."""
    lower = np.ascontiguousarray(lower, dtype=float)
    upper = np.ascontiguousarray(upper, dtype=float)
    hp = np.ascontiguousarray(hp, dtype=float)
    if HAS_NUMBA and hp.shape[0] * (n + 1) >= _NUMBA_MIN_CELLS:
        return _coverage_numba(n, lower, upper, hp)
    return _coverage_numpy(n, lower, upper, hp)


def _coverage_numpy(n, lower, upper, hp):
    from scipy import stats

    x = np.arange(n + 1)
    covered = (hp[:, None] > lower[None, :]) & (hp[:, None] < upper[None, :])
    pmf = stats.binom.pmf(x[None, :], n, hp[:, None])
    return (pmf * covered).sum(axis=1)
