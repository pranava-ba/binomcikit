"""Blaker's exact acceptability confidence interval.

**New in binomcikit — not part of the original R ``proportion`` package.** Blaker
(2000) is an *exact* interval (coverage guaranteed >= 1 - alpha) that is provably
**nested inside Clopper-Pearson** (never wider), so it removes some of Clopper-
Pearson's waste while keeping the guarantee. The source R package flagged exact
alternatives like this as future work; binomcikit implements it, closing a gap
that exists even against R ``proportion``.

Construction (Blaker 2000). With the binomial CDF ``F(k; th) = P(X <= k)``, the
smaller-tail function is ``g(x, th) = min(F(x; th), 1 - F(x-1; th))`` and the
acceptability function is ``gamma(x, th) = P_th( g(X, th) <= g(x, th) )``. The
1 - alpha interval is ``{ th : gamma(x, th) >= alpha }``; the limits solve
``gamma(x, th) = alpha`` and are found by bracketed root-finding inward from the
Clopper-Pearson bounds (Blaker is nested inside them).
"""

import importlib.util

import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy import optimize
from scipy.special import gammaln

# Tolerance for the "<=" tie in the acceptability sum: a k whose smaller tail
# ties g(x, th) up to floating-point noise must be counted (matters at the edges).
_TIE = 1e-10

# optional: a compiled kernel makes a whole table ~100x faster; results are identical. numba is
# imported lazily (on the first compiled call), so `import binomcikit` does not pay for it.
HAS_NUMBA = importlib.util.find_spec("numba") is not None


# The acceptability function gamma(x, .) is NOT unimodal (Klaschka & Reitmeir 2014), so a plain
# bisection can converge to an *inner* crossing and return an interval that is too short. The
# limits are therefore found like R's ``PropCIs::blakerci`` does: walk inward from the (outer)
# Clopper-Pearson bound to the *first* theta that is acceptable -- here on a K-point scan -- and
# bisect only that last sub-interval.
#
# Accepted "islands" are real but tiny (~1e-3 wide) and start only ~1e-4 inside the outer bound, so
# the scan is dense next to the outer end: geometric fractions 2^-24 ... 2^-1 plus a uniform grid.
_SCAN = 40
_FRACS = np.unique(np.concatenate([2.0 ** -np.arange(24, 0, -1), np.arange(1, _SCAN + 1) / _SCAN]))


def _blaker_table_np(n, alp, iters=46):
    """Whole-table Blaker limits (no numba): outward-in scan, then vectorised bisection."""
    k = np.arange(n + 1)
    lch = gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)
    xs = np.arange(n + 1)
    lower = np.zeros(n + 1)
    upper = np.ones(n + 1)
    cp_lo = np.where(xs > 0, stats.beta.ppf(alp / 2, np.maximum(xs, 1), n - xs + 1), 0.0)
    cp_hi = np.where(xs < n, stats.beta.ppf(1 - alp / 2, xs + 1, np.maximum(n - xs, 1)), 1.0)

    def gam(rows, th):
        t = th[:, None]
        with np.errstate(divide="ignore", invalid="ignore"):
            pmf = np.exp(lch[None, :] + k[None, :] * np.log(t) + (n - k[None, :]) * np.log1p(-t))
        cdf = np.cumsum(pmf, axis=1)
        sf = np.cumsum(pmf[:, ::-1], axis=1)[:, ::-1]
        g = np.minimum(cdf, sf)
        gx = g[np.arange(rows.size), rows][:, None]
        return (pmf * (g <= gx + _TIE)).sum(axis=1)

    def limit(r, outer, inner):
        """Boundary between ``outer`` (rejected side) and ``inner`` (accepted ``p-hat`` side)."""
        # 1. outward-in scan: the first scan point that is acceptable
        first = np.full(r.size, _FRACS.size - 1)
        found = np.zeros(r.size, dtype=bool)
        for j, f in enumerate(_FRACS):
            hit = ~found & (gam(r, outer + (inner - outer) * f) >= alp)
            first = np.where(hit, j, first)
            found |= hit
        prev = np.concatenate([[0.0], _FRACS])  # fraction just before each scan point
        out_b = outer + (inner - outer) * prev[first]  # rejected end of the bracket
        in_b = outer + (inner - outer) * _FRACS[first]  # accepted end
        # 2. bisect that one sub-interval
        for _ in range(iters):
            mid = 0.5 * (out_b + in_b)
            ok = gam(r, mid) >= alp
            in_b = np.where(ok, mid, in_b)
            out_b = np.where(ok, out_b, mid)
        return 0.5 * (out_b + in_b)

    # chunk the rows so the (rows x (n+1)) working matrices stay a few MB
    step = max(1, int(4_000_000 // (n + 1)))
    for s in range(0, n + 1, step):
        rows = xs[s : s + step]
        ph = rows / n
        lo_r = rows > 0
        if lo_r.any():
            r = rows[lo_r]
            lower[r] = limit(r, cp_lo[r], ph[lo_r])
        hi_r = rows < n
        if hi_r.any():
            r = rows[hi_r]
            upper[r] = limit(r, cp_hi[r], ph[hi_r])
    return lower, upper


if True:  # plain-Python kernels; compiled lazily by _compile()

    def _gamma_nb(x, n, theta, lch, tie, pmf, sf, g):  # pragma: no cover - compiled
        lt = np.log(theta)
        l1t = np.log1p(-theta)
        for k in range(n + 1):
            pmf[k] = np.exp(lch[k] + k * lt + (n - k) * l1t)
        s = 0.0
        for k in range(n, -1, -1):
            s += pmf[k]
            sf[k] = s
        c = 0.0
        for k in range(n + 1):
            c += pmf[k]
            g[k] = c if c < sf[k] else sf[k]
        gx = g[x] + tie
        tot = 0.0
        for k in range(n + 1):
            if g[k] <= gx:
                tot += pmf[k]
        return tot

    def _limit_nb(x, n, alp, outer, inner, lch, tie, pmf, sf, g, fracs, iters):  # pragma: no cover
        """Outermost acceptable boundary between ``outer`` (rejected) and ``inner`` (accepted)."""
        first = fracs.shape[0] - 1
        for j in range(fracs.shape[0]):
            th = outer + (inner - outer) * fracs[j]
            if _gamma_nb(x, n, th, lch, tie, pmf, sf, g) >= alp:
                first = j
                break
        prev = fracs[first - 1] if first > 0 else 0.0
        out_b = outer + (inner - outer) * prev
        in_b = outer + (inner - outer) * fracs[first]
        for _ in range(iters):
            mid = 0.5 * (out_b + in_b)
            if _gamma_nb(x, n, mid, lch, tie, pmf, sf, g) >= alp:
                in_b = mid
            else:
                out_b = mid
        return 0.5 * (out_b + in_b)

    def _blaker_table_nb(
        n, alp, lch, cp_lo, cp_hi, tie, fracs, iters
    ):  # pragma: no cover - compiled
        lower = np.zeros(n + 1)
        upper = np.ones(n + 1)
        pmf = np.empty(n + 1)
        sf = np.empty(n + 1)
        g = np.empty(n + 1)
        for x in range(n + 1):
            ph = x / n
            if x > 0:
                lower[x] = _limit_nb(x, n, alp, cp_lo[x], ph, lch, tie, pmf, sf, g, fracs, iters)
            if x < n:
                upper[x] = _limit_nb(x, n, alp, cp_hi[x], ph, lch, tie, pmf, sf, g, fracs, iters)
        return lower, upper


_COMPILED = False


def _compile():
    """Compile the kernels once (numba imported here, not at package import)."""
    global _COMPILED, _gamma_nb, _limit_nb, _blaker_table_nb
    if _COMPILED:
        return
    from numba import njit

    # the callees must be compiled objects *before* the callers are compiled
    _gamma_nb = njit(cache=True)(_gamma_nb)
    _limit_nb = njit(cache=True)(_limit_nb)
    _blaker_table_nb = njit(cache=True)(_blaker_table_nb)
    _COMPILED = True


def _blaker_table(n, alp, iters=46):
    """Lower/upper Blaker limits for every ``x`` at once (compiled kernel when numba is present)."""
    if HAS_NUMBA and n >= 8:
        _compile()
        xs = np.arange(n + 1)
        lch = gammaln(n + 1) - gammaln(xs + 1) - gammaln(n - xs + 1)
        cp_lo = np.where(xs > 0, stats.beta.ppf(alp / 2, np.maximum(xs, 1), n - xs + 1), 0.0)
        cp_hi = np.where(xs < n, stats.beta.ppf(1 - alp / 2, xs + 1, np.maximum(n - xs, 1)), 1.0)
        return _blaker_table_nb(n, alp, lch, cp_lo, cp_hi, _TIE, _FRACS, iters)
    return _blaker_table_np(n, alp, iters)


def _blaker_gamma(x, n, theta):
    """Blaker's acceptability function ``gamma(x, theta)`` (the direct definition)."""
    if theta <= 0.0:
        return 1.0 if x == 0 else 0.0
    if theta >= 1.0:
        return 1.0 if x == n else 0.0
    k = np.arange(n + 1)
    # g(k, theta) = min(lower tail P(X<=k), upper tail P(X>=k)) for every k
    g = np.minimum(stats.binom.cdf(k, n, theta), stats.binom.sf(k - 1, n, theta))
    pmf = stats.binom.pmf(k, n, theta)
    return float(pmf[g <= g[x] + _TIE].sum())


def _outermost(x, n, alp, outer, inner, iters=46):
    """Outermost acceptable boundary between ``outer`` (rejected) and ``inner`` (accepted) for one row.

    Scalar twin of the table kernels: scan inward from ``outer`` on ``_FRACS`` for the first
    acceptable theta, then bisect that last sub-interval.
    """
    first = _FRACS.size - 1
    for j, f in enumerate(_FRACS):
        if _blaker_gamma(x, n, outer + (inner - outer) * f) >= alp:
            first = j
            break
    prev = _FRACS[first - 1] if first > 0 else 0.0
    out_b = outer + (inner - outer) * prev
    in_b = outer + (inner - outer) * _FRACS[first]
    for _ in range(iters):
        mid = 0.5 * (out_b + in_b)
        if _blaker_gamma(x, n, mid) >= alp:
            in_b = mid
        else:
            out_b = mid
    return 0.5 * (out_b + in_b)


def _blaker_limits(x, n, alp):
    """Lower and upper Blaker limits for a single ``x`` (outermost crossing of gamma = alpha)."""
    phat = x / n
    lower = 0.0 if x == 0 else _outermost(x, n, alp, stats.beta.ppf(alp / 2, x, n - x + 1), phat)
    upper = (
        1.0 if x == n else _outermost(x, n, alp, stats.beta.ppf(1 - alp / 2, x + 1, n - x), phat)
    )
    return lower, upper


def _blaker_limits_brentq(x, n, alp):
    """The original single-root ``brentq`` search -- kept only to document the defect it had.

    Not used by the package: gamma(x, .) is not unimodal, so this can return an *inner* crossing
    (see ``tests/test_blaker.py``: the outermost-crossing regression tests).
    """
    phat = x / n
    lower = (
        0.0
        if x == 0
        else optimize.brentq(
            lambda t: _blaker_gamma(x, n, t) - alp, stats.beta.ppf(alp / 2, x, n - x + 1), phat
        )
    )
    upper = (
        1.0
        if x == n
        else optimize.brentq(
            lambda t: _blaker_gamma(x, n, t) - alp, phat, stats.beta.ppf(1 - alp / 2, x + 1, n - x)
        )
    )
    return lower, upper


def _validate(n, alp):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if not 0 <= alp <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")


def _row_flags(lower, upper):
    labb = "YES" if lower < 0 else "NO"
    uabb = "YES" if upper > 1 else "NO"
    zwi = "YES" if upper - lower == 0 else "NO"
    return labb, uabb, zwi


def ciblaker(n, alp):
    r"""Blaker's exact confidence intervals, for every ``x``.

    **New in binomcikit** (absent from the R ``proportion`` package). An exact
    interval with coverage guaranteed at least :math:`1-\alpha`, provably nested
    inside (never wider than) Clopper--Pearson.

    Parameters
    ----------
    n : int
        Number of trials (``n > 0``).
    alp : float
        Significance level :math:`\alpha` in ``[0, 1]``.

    Returns
    -------
    pandas.DataFrame
        One row per ``x`` with columns ``x``, ``LBK``, ``UBK`` and the flags
        ``LABB``, ``UABB``, ``ZWI``.

    See Also
    --------
    ciex : Clopper--Pearson / Mid-P exact family (Blaker is nested inside Clopper--Pearson).

    Notes
    -----
    The limits solve :math:`\gamma(x, \theta) = \alpha` for Blaker's acceptability
    function :math:`\gamma`; see the module docstring for the construction.

    Examples
    --------
    >>> import binomcikit as bk
    >>> bk.ciblaker(20, 0.05).columns.tolist()
    ['x', 'LBK', 'UBK', 'LABB', 'UABB', 'ZWI']
    """
    _validate(n, alp)
    x = np.arange(n + 1)
    lbk, ubk = _blaker_table(int(n), alp)
    flags = [_row_flags(lo, hi) for lo, hi in zip(lbk, ubk)]
    labb, uabb, zwi = (np.array(col, dtype=object) for col in zip(*flags))
    return pd.DataFrame({"x": x, "LBK": lbk, "UBK": ubk, "LABB": labb, "UABB": uabb, "ZWI": zwi})


def ciblakerx(x, n, alp):
    r"""Blaker's exact confidence interval for a single observed ``x``.

    **New in binomcikit** (absent from the R ``proportion`` package). See
    :func:`ciblaker` for the all-``x`` version and the construction.

    Parameters
    ----------
    x : int
        Observed number of successes (``0 <= x <= n``).
    n : int
        Number of trials (``n > 0``).
    alp : float
        Significance level :math:`\alpha` in ``[0, 1]``.

    Returns
    -------
    pandas.DataFrame
        A single row with columns ``x``, ``LBKx``, ``UBKx`` and the flags
        ``LABB``, ``UABB``, ``ZWI``.
    """
    _validate(n, alp)
    if x is None:
        raise ValueError("'x' is missing")
    if not isinstance(x, (int, np.integer)) or x < 0 or x > n:
        raise ValueError("'x' has to be an integer between 0 and n")
    lo, hi = _blaker_limits(x, n, alp)
    labb, uabb, zwi = _row_flags(lo, hi)
    return pd.DataFrame(
        {"x": [x], "LBKx": [lo], "UBKx": [hi], "LABB": [labb], "UABB": [uabb], "ZWI": [zwi]}
    )
