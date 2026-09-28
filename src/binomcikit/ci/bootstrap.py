"""Bootstrap confidence intervals for a single binomial proportion.

**New in binomcikit -- not part of the original R ``proportion`` package**,
and explicitly named as future work by the paper this package ports
(Subbiah & Rajeswaran 2017). Two families, selected by ``kind``:

* ``kind="smooth"`` (default) -- the Wang & Hutson (2013) smooth bootstrap
  [25], which resamples from a *smoothed* quantile function instead of the
  raw 0/1 data, to avoid the discrete, degenerate resampling distribution
  that cripples an ordinary bootstrap for binomial data (see below).
* ``kind="percentile"`` / ``kind="bca"`` -- the standard nonparametric
  bootstrap (percentile, or bias-corrected-and-accelerated), a thin wrapper
  around :func:`scipy.stats.bootstrap` -- it inherits scipy's own
  correctness testing as its oracle.

**Why the naive bootstrap needs fixing.** Ordinary bootstrap resamples the
observed 0/1 data with replacement, so a bootstrap replicate's proportion can
only take values ``k/n`` -- a discrete, degenerate distribution. This is
worst exactly where it matters most: at ``x = 0`` or ``x = n``, *every*
resample reproduces the same all-0/all-1 sample, so ``kind="percentile"``/
``"bca"`` collapse to the zero-width interval ``(0, 0)`` / ``(1, 1)``
(handled explicitly below, verified in ``tests/test_bootstrap.py``). Wang &
Hutson's smooth quantile function fixes this by resampling from a continuous
approximation instead.

**Construction** (Wang & Hutson 2013 [25], Section 2 -- verified against the
paper's primary text at
https://pmc.ncbi.nlm.nih.gov/articles/PMC4789773/, not just a secondary
summary):

1. Estimate ``theta`` by the **median-unbiased estimator** (MUE, Eq. 8):
   solve ``P(X >= x | theta) = 0.5`` and ``P(X <= x | theta) = 0.5`` for
   ``theta_MUEL`` / ``theta_MUER`` (the same incomplete-beta identity that
   gives the Clopper-Pearson formula, but evaluated at the 50% level instead
   of alpha/2) and average: ``theta_hat = (theta_MUEL + theta_MUER) / 2``.
   Matches the paper's own boundary formulas at ``x = 0`` and ``x = n``
   exactly (see ``tests/test_bootstrap.py``).
2. The smooth quantile function (Eq. 3/4) is
   ``Q(u | theta) = 1 - BetaCDF(1 - theta; 3u, 3(1-u))``, ``u in (0, 1)``.
3. For ``b = 1..B``: draw ``n`` iid Uniform(0,1) values ``u*``; map them
   through ``Q(. | theta_hat)`` to get ``n`` smoothed pseudo-observations
   ``x*``; take their mean ``xbar*``; convert it back to a proportion
   ``theta*_b = g(xbar*)`` via the paper's own fitted cubic B-spline
   (Eq. 7 -- knots/coefficients transcribed below exactly as printed in the
   paper, not refit here).
4. The CI is the empirical ``(alpha/2, 1-alpha/2)`` percentile of the
   ``theta*_b`` sample.

**No third-party oracle exists for ``kind="smooth"``** -- this is genuinely
new code. See ``docs/under_the_hood.md`` ("Correctness") for exactly what
verification was used instead: cross-checked against ``kind="percentile"``/
``"bca"`` at well-behaved ``x`` (both should roughly agree away from the
boundary), and checked to give a non-degenerate interval exactly where the
naive bootstrap collapses (the property the whole method exists to fix).
"""

import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy.interpolate import BSpline

# Wang & Hutson (2013), Equation 7: the fixed cubic B-spline g(.) that
# inverts the mean(X*) -> theta relationship. Knots and coefficients as
# printed in the paper -- a global constant, not refit per n or per call.
_BOOT_KNOTS = np.array([0, 0, 0, 0, 0.293, 0.498, 0.699, 1, 1, 1, 1], dtype=float)
_BOOT_COEF = np.array([0.005, -0.033, 0.159, 0.495, 0.835, 1.033, 0.996], dtype=float)
_boot_spline = BSpline(_BOOT_KNOTS, _BOOT_COEF, 3, extrapolate=False)

_KINDS = ("smooth", "percentile", "bca")
_EPS = 1e-10


def _mue(x, n):
    """Median-unbiased estimator of theta (Wang & Hutson 2013, Eq. 8)."""
    muel = 0.0 if x == 0 else stats.beta.ppf(0.5, x, n - x + 1)
    muer = 1.0 if x == n else stats.beta.ppf(0.5, x + 1, n - x)
    return 0.5 * (muel + muer)


def _smooth_ci(x, n, alp, B, rng):
    """Wang-Hutson smooth-bootstrap percentile CI for one x (see module docstring)."""
    pihat = _mue(x, n)
    u = np.clip(rng.random((B, n)), _EPS, 1 - _EPS)
    xstar = 1 - stats.beta.cdf(1 - pihat, 3 * u, 3 * (1 - u))
    xbar = np.clip(xstar.mean(axis=1), 0.0, 1.0)
    thetastar = np.asarray(_boot_spline(xbar))
    return np.quantile(thetastar, [alp / 2, 1 - alp / 2])


def _resample_ci(x, n, alp, B, rng, method):
    """Ordinary nonparametric bootstrap (percentile / BCa) -- a thin wrapper
    around ``scipy.stats.bootstrap``, which is its own oracle.

    Degenerate at x = 0 / x = n (every resample is identical, so BCa's
    acceleration constant is 0/0): handled explicitly rather than left to
    raise, matching the naive bootstrap's well-known collapse to a
    zero-width interval there.
    """
    if x == 0:
        return 0.0, 0.0
    if x == n:
        return 1.0, 1.0
    data = (np.concatenate([np.ones(x), np.zeros(n - x)]),)
    res = stats.bootstrap(
        data,
        np.mean,
        n_resamples=B,
        method=method,
        confidence_level=1 - alp,
        random_state=rng,
    )
    return float(res.confidence_interval.low), float(res.confidence_interval.high)


def _boot_limits(x, n, alp, B, rng, kind):
    key = str(kind).lower().strip()
    if key not in _KINDS:
        raise ValueError(f"unknown kind {kind!r}; choose from {_KINDS}")
    if key == "smooth":
        lo, hi = _smooth_ci(x, n, alp, B, rng)
    else:
        lo, hi = _resample_ci(x, n, alp, B, rng, key)
    return float(lo), float(hi)


def _validate(n, alp, B):
    if n is None:
        raise ValueError("'n' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if not 0 <= alp <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not isinstance(B, (int, np.integer)) or B <= 0:
        raise ValueError("'B' has to be a positive integer")


def _row_flags(lower, upper):
    labb = "YES" if lower < 0 else "NO"
    uabb = "YES" if upper > 1 else "NO"
    lower_c, upper_c = max(lower, 0.0), min(upper, 1.0)
    zwi = "YES" if upper_c - lower_c == 0 else "NO"
    return lower_c, upper_c, labb, uabb, zwi


def ciboot(n, alp, B=2000, seed=None, kind="smooth"):
    r"""Bootstrap confidence intervals, for every ``x``.

    **New in binomcikit** (absent from the R ``proportion`` package; the
    2017 paper names bootstrap as future work). See the module docstring for
    the construction and why ``kind="smooth"`` exists.

    Parameters
    ----------
    n : int
        Number of trials (``n > 0``).
    alp : float
        Significance level :math:`\alpha` in ``[0, 1]``.
    B : int, default 2000
        Number of bootstrap resamples per ``x``.
    seed : int, optional
        Seeds the resampling for reproducible output.
    kind : {"smooth", "percentile", "bca"}, default "smooth"
        ``"smooth"`` -- Wang & Hutson's smooth quantile bootstrap (no
        third-party oracle; see module docstring). ``"percentile"`` /
        ``"bca"`` -- ordinary nonparametric bootstrap via
        :func:`scipy.stats.bootstrap` (oracle-verified).

    Returns
    -------
    pandas.DataFrame
        One row per ``x`` with columns ``x``, ``LBOOT``, ``UBOOT`` and the
        flags ``LABB``, ``UABB``, ``ZWI``.

    See Also
    --------
    ciex : Clopper-Pearson / Mid-P exact family (a non-simulated alternative).
    ciblaker : Blaker's exact interval (also new in binomcikit).

    Examples
    --------
    >>> import binomcikit as bk
    >>> bk.ciboot(20, 0.05, B=200, seed=1).columns.tolist()
    ['x', 'LBOOT', 'UBOOT', 'LABB', 'UABB', 'ZWI']
    """
    _validate(n, alp, B)
    rng = np.random.default_rng(seed)
    x = np.arange(n + 1)
    lbo = np.empty(n + 1)
    ubo = np.empty(n + 1)
    labb = np.empty(n + 1, dtype=object)
    uabb = np.empty(n + 1, dtype=object)
    zwi = np.empty(n + 1, dtype=object)
    for i in range(n + 1):
        raw_lo, raw_hi = _boot_limits(i, n, alp, B, rng, kind)
        lbo[i], ubo[i], labb[i], uabb[i], zwi[i] = _row_flags(raw_lo, raw_hi)
    return pd.DataFrame(
        {"x": x, "LBOOT": lbo, "UBOOT": ubo, "LABB": labb, "UABB": uabb, "ZWI": zwi}
    )


def cibootx(x, n, alp, B=2000, seed=None, kind="smooth"):
    r"""Bootstrap confidence interval for a single observed ``x``.

    **New in binomcikit** (absent from the R ``proportion`` package). See
    :func:`ciboot` for the all-``x`` version, parameters, and construction.

    Returns
    -------
    pandas.DataFrame
        A single row with columns ``x``, ``LBOOTx``, ``UBOOTx`` and the
        flags ``LABB``, ``UABB``, ``ZWI``.
    """
    _validate(n, alp, B)
    if x is None:
        raise ValueError("'x' is missing")
    if not isinstance(x, (int, np.integer)) or x < 0 or x > n:
        raise ValueError("'x' has to be an integer between 0 and n")
    rng = np.random.default_rng(seed)
    raw_lo, raw_hi = _boot_limits(x, n, alp, B, rng, kind)
    lo, hi, labb, uabb, zwi = _row_flags(raw_lo, raw_hi)
    return pd.DataFrame(
        {"x": [x], "LBOOTx": [lo], "UBOOTx": [hi], "LABB": [labb], "UABB": [uabb], "ZWI": [zwi]}
    )
