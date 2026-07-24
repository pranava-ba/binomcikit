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

import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy import optimize

# Tolerance for the "<=" tie in the acceptability sum: a k whose smaller tail
# ties g(x, th) up to floating-point noise must be counted (matters at the edges).
_TIE = 1e-10


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


def _blaker_limits(x, n, alp):
    """Lower and upper Blaker limits for a single ``x`` (root-find on gamma = alpha)."""
    phat = x / n
    if x == 0:
        lower = 0.0
    else:
        cp_l = stats.beta.ppf(alp / 2, x, n - x + 1)  # Clopper-Pearson lower (outer bracket)
        lower = optimize.brentq(lambda t: _blaker_gamma(x, n, t) - alp, cp_l, phat)
    if x == n:
        upper = 1.0
    else:
        cp_u = stats.beta.ppf(1 - alp / 2, x + 1, n - x)  # Clopper-Pearson upper (outer bracket)
        upper = optimize.brentq(lambda t: _blaker_gamma(x, n, t) - alp, phat, cp_u)
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
    lbk = np.empty(n + 1)
    ubk = np.empty(n + 1)
    labb = np.empty(n + 1, dtype=object)
    uabb = np.empty(n + 1, dtype=object)
    zwi = np.empty(n + 1, dtype=object)
    for i in range(n + 1):
        lo, hi = _blaker_limits(i, n, alp)
        lbk[i], ubk[i] = lo, hi
        labb[i], uabb[i], zwi[i] = _row_flags(lo, hi)
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
