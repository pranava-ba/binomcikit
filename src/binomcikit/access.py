"""Access & usability layer — the modern, user-facing conveniences the R
``proportion`` package lacks.

These functions do not add new statistics; they make the existing engine easier
to reach: build ``(x, n)`` from raw data, pull point estimates and posteriors,
extract the coverage/length *curves* that previously lived only inside the plot
functions, and compare or rank methods in one call.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence

import numpy as np
import pandas as pd
import scipy.stats as stats

from ._accel import coverage_series
from ._hpd import hpd_beta
from .ci.bootstrap import _mue
from .highlevel import ci as _ci
from .plotly_viz import _METHODS, _limits

# Named conjugate priors for the Bayesian helpers.
PRIORS: dict[str, tuple[float, float]] = {
    "jeffreys": (0.5, 0.5),
    "laplace": (1.0, 1.0),
    "uniform": (1.0, 1.0),
    "haldane": (0.0, 0.0),
}

# Canonical comparable methods (keys of the shared limit registry, no aliases).
# "boot" is deliberately excluded: it is stochastic and much slower than every
# other method here (each call resamples B times per x), so it would silently
# change compare()/recommend()'s runtime and reproducibility contract. Pass
# methods=[..., "boot"] explicitly (with your own seed) if you want it.
DEFAULT_METHODS: tuple[str, ...] = (
    "wald",
    "wilson",
    "arcsine",
    "logit",
    "waldt",
    "lr",
    "exact",
    "midp",
    "jeffreys",
    "blaker",
)


# --- data input --------------------------------------------------------------
def from_counts(x: int, n: int) -> tuple[int, int]:
    """Validate a successes/trials pair and return it as ``(x, n)``.

    A tiny guard so downstream calls get clean integers.

    >>> from_counts(3, 20)
    (3, 20)
    """
    if not isinstance(n, (int, np.integer)) or n <= 0:
        raise ValueError("'n' has to be a positive integer")
    if not isinstance(x, (int, np.integer)) or x < 0 or x > n:
        raise ValueError("'x' has to be an integer in 0..n")
    return int(x), int(n)


def from_data(data: Iterable[object]) -> tuple[int, int]:
    """Derive ``(x, n)`` from a raw 0/1 (or boolean) sequence.

    ``x`` is the number of successes (truthy / ``1``) and ``n`` the length. Values
    must each be 0/1 or ``True``/``False``.

    >>> from_data([1, 0, 1, 1, 0])
    (3, 5)
    """
    arr = np.asarray(list(data))
    if arr.size == 0:
        raise ValueError("'data' is empty")
    is01 = np.isin(arr, [0, 1, True, False])
    if not is01.all():
        raise ValueError("'data' must contain only 0/1 or True/False values")
    n = int(arr.size)
    x = int(np.count_nonzero(arr.astype(bool)))
    return x, n


# --- point estimates ---------------------------------------------------------
def point_estimate(x: int, n: int, method: str = "mle", alpha: float = 0.05) -> float:
    """A single best-guess value for ``theta`` from ``(x, n)``.

    ``method`` is one of:

    * ``"mle"`` — the sample proportion ``x/n`` (maximum likelihood).
    * ``"ac"`` / ``"agresti-coull"`` — ``(x + z^2/2) / (n + z^2)`` (shrinks toward 1/2).
    * ``"jeffreys"`` — posterior mean under a Beta(0.5, 0.5) prior.
    * ``"laplace"`` / ``"bayes"`` — posterior mean under a flat Beta(1, 1) prior.
    * ``"mue"`` — the median-unbiased estimator (Wang & Hutson 2013, Eq. 8; the
      plug-in ``theta`` the smooth :func:`binomcikit.ciboot` bootstrap resamples
      from). Unlike ``"mle"``, never lands exactly on 0 or 1.

    >>> round(point_estimate(0, 20, "mle"), 3)
    0.0
    >>> round(point_estimate(0, 20, "laplace"), 3)     # prior lifts it off zero
    0.045
    >>> round(point_estimate(0, 20, "mue"), 3)         # also never exactly 0
    0.017
    """
    x, n = from_counts(x, n)
    key = str(method).lower().strip()
    if key == "mle":
        return x / n
    if key in ("ac", "agresti-coull"):
        z2 = stats.norm.ppf(1 - alpha / 2) ** 2
        return (x + z2 / 2) / (n + z2)
    if key in PRIORS or key in ("bayes",):
        a, b = PRIORS["laplace"] if key == "bayes" else PRIORS[key]
        return (x + a) / (n + a + b)
    if key == "mue":
        return _mue(x, n)
    raise ValueError(f"unknown method {method!r}; choose from mle, ac, jeffreys, laplace, mue")


# --- Bayesian conveniences ---------------------------------------------------
def posterior(x: int, n: int, a: float = 1.0, b: float = 1.0, alpha: float = 0.05) -> dict:
    """Summarise the Beta(x+a, n-x+b) posterior for ``theta``.

    Returns a dict with the posterior shape parameters, its mean/mode/variance,
    and both the equal-tailed (quantile) and HPD credible intervals at level
    ``1 - alpha``. ``a, b`` may be a named prior via :func:`prior`.

    >>> post = posterior(3, 20)
    >>> round(post["mean"], 3)
    0.182
    """
    x, n = from_counts(x, n)
    s1, s2 = x + a, n - x + b
    mean = s1 / (s1 + s2)
    var = (s1 * s2) / ((s1 + s2) ** 2 * (s1 + s2 + 1))
    mode = (s1 - 1) / (s1 + s2 - 2) if (s1 > 1 and s2 > 1) else float("nan")
    lo_q = stats.beta.ppf(alpha / 2, s1, s2)
    hi_q = stats.beta.ppf(1 - alpha / 2, s1, s2)
    lo_h, hi_h = hpd_beta(s1, s2, conf=1 - alpha)
    return {
        "a_post": s1,
        "b_post": s2,
        "mean": mean,
        "mode": mode,
        "var": var,
        "sd": float(np.sqrt(var)),
        "quantile_interval": (lo_q, hi_q),
        "hpd_interval": (lo_h, hi_h),
    }


def prior(name: str) -> tuple[float, float]:
    """Look up a named conjugate prior's ``(a, b)`` — ``jeffreys``, ``laplace``,
    ``uniform`` or ``haldane``.

    >>> prior("jeffreys")
    (0.5, 0.5)
    """
    key = str(name).lower().strip()
    if key not in PRIORS:
        raise ValueError(f"unknown prior {name!r}; choose from {sorted(PRIORS)}")
    return PRIORS[key]


# --- curve accessors (the data behind the plots) -----------------------------
def coverage_curve(
    n: int, method: str = "wilson", alpha: float = 0.05, points: int = 200
) -> pd.DataFrame:
    """The coverage-probability curve: coverage vs the true proportion ``theta``.

    Returns a tidy ``DataFrame(theta, coverage)`` — the numbers that
    :func:`binomcikit.plot_coverage` draws, exposed for your own analysis.
    """
    lower, upper, _ = _limits(method, n, alpha)
    theta = np.linspace(1e-4, 1 - 1e-4, points)
    cp = coverage_series(n, lower, upper, theta)
    return pd.DataFrame({"theta": theta, "coverage": cp})


def length_curve(
    n: int, method: str = "wilson", alpha: float = 0.05, points: int = 200
) -> pd.DataFrame:
    """The expected-length curve: mean interval width vs the true proportion.

    ``E[length | theta] = sum_x (U[x] - L[x]) * P(X = x | n, theta)``. Returns a
    tidy ``DataFrame(theta, expected_length)``.
    """
    lower, upper, _ = _limits(method, n, alpha)
    width = np.asarray(upper, dtype=float) - np.asarray(lower, dtype=float)
    theta = np.linspace(1e-4, 1 - 1e-4, points)
    k = np.arange(n + 1)
    pmf = stats.binom.pmf(k[:, None], n, theta[None, :])  # (n+1, points)
    el = (width[:, None] * pmf).sum(axis=0)
    return pd.DataFrame({"theta": theta, "expected_length": el})


# --- multi-method comparison & recommendation --------------------------------
def _method_keys(methods: Sequence[str] | None) -> list[str]:
    keys = list(DEFAULT_METHODS if methods is None else methods)
    bad = [m for m in keys if str(m).lower().strip() not in _METHODS]
    if bad:
        raise ValueError(f"unknown method(s) {bad}; choose from {sorted(set(_METHODS))}")
    return keys


def compare(
    x: int, n: int, alpha: float = 0.05, methods: Sequence[str] | None = None
) -> pd.DataFrame:
    """Every method's interval for a single observed ``x``, side by side.

    Returns a ``DataFrame`` with one row per method — ``lower``, ``upper`` and
    ``width`` — sorted from narrowest to widest. The practical "I saw x of n; what
    does each method give me?" table.

    >>> compare(3, 20).columns.tolist()
    ['method', 'lower', 'upper', 'width']
    """
    x, n = from_counts(x, n)
    rows = []
    for m in _method_keys(methods):
        lower, upper, label = _limits(m, n, alpha)
        lo, hi = float(lower[x]), float(upper[x])
        rows.append({"method": label, "lower": lo, "upper": hi, "width": hi - lo})
    return pd.DataFrame(rows).sort_values("width").reset_index(drop=True)


def _rejects(x, n, alpha, theta0, method):
    try:
        lower, upper, _ = _limits(method, n, alpha)
    except Exception:
        # A handful of numerical root-finders (e.g. Blaker) can't resolve an
        # essentially-degenerate bracket right at the extreme alpha -> 1 end
        # (the CI has shrunk to ~a single point there); treat that the same
        # as "rejected", which is what a genuinely point-sized CI would give.
        return True
    return theta0 < float(lower[x]) or theta0 > float(upper[x])


_NO_PVALUE = {"boot", "bootstrap", "boot-percentile", "boot-bca"}


def pvalue(x, n, theta0, method="wilson", alpha=0.05):
    r"""Two-sided p-value for :math:`H_0: \theta = \theta_0`, by CI-test duality.

    Not part of R ``proportion`` — the 2017 paper treats confidence intervals and
    tests as interchangeable (by construction, a 2-sided level-:math:`\alpha` test
    and a :math:`(1-\alpha)` CI reject/cover the same set of :math:`\theta_0`) and
    states explicitly that this "excludes adding additional functions". binomcikit
    adds them anyway: they are more convenient for users who think in tests, and
    the duality is only *approximate* for some methods (e.g. Wald), so an explicit
    test can expose subtle differences the CI alone does not show.

    The p-value is **defined directly from the method's own CI** — the smallest
    :math:`\alpha` at which :math:`\theta_0` falls outside the ``(1-\alpha)``
    interval for ``method`` — so it works for *any* registered method (not just
    ones with a closed-form test formula), and is guaranteed **by construction**
    to agree with :func:`binomcikit.ci`: ``pvalue(...) < alpha`` if and only if
    ``theta0`` sits outside ``bk.ci(x=x, n=n, alpha=alpha, method=method)``.

    .. note::
       This is the **equal-tailed** two-sided p-value (matches Clopper-Pearson's
       own equal-tailed CI: :math:`2 \min(P(X \le x), P(X \ge x))`, capped at 1).
       It does **not** match ``scipy.stats.binomtest``'s default two-sided
       p-value, which uses a different ("minlike", small-probability) convention
       — the two agree only where the binomial distribution is symmetric enough
       that the conventions coincide (e.g. :math:`\theta_0` near :math:`x/n`).
       This is deliberate: it is the p-value *dual to binomcikit's own CIs*, not
       a reproduction of scipy's unrelated test.

    Parameters
    ----------
    x : int
        Observed number of successes (``0 <= x <= n``).
    n : int
        Number of trials (``n > 0``).
    theta0 : float
        The hypothesised proportion, in ``[0, 1]``.
    method : str, default "wilson"
        Any method name :func:`binomcikit.ci` accepts, except the bootstrap
        family (stochastic CIs make the duality ill-defined without pinning a
        seed across the whole search).
    alpha : float, default 0.05
        Unused by the p-value itself (kept for symmetry with :func:`ci`/
        :func:`compare`); pass it to :func:`reject` to get a reject/accept call.

    Returns
    -------
    float
        The p-value, in ``[0, 1]``.

    See Also
    --------
    reject : Reject/accept H0 at a given alpha (a thin wrapper around this).

    Notes
    -----
    Each bisection step recomputes ``method``'s whole ``(n+1)``-row CI table, so
    this is instant for closed-form methods (Wald, Wilson, ArcSine, ...) but
    noticeably slower (tens to low hundreds of milliseconds, growing with ``n``)
    for the ones that root-find per row internally (Clopper-Pearson/Mid-P, LR,
    Blaker) -- roughly 20x that method's own ``bk.ci(...)`` cost.

    Examples
    --------
    >>> round(pvalue(3, 20, 0.5, method="exact"), 4)
    0.0026
    >>> pvalue(3, 20, 3 / 20, method="wilson")  # theta0 == phat -> never rejected
    1.0
    """
    del alpha  # not used by the p-value itself; documented for API symmetry
    x, n = from_counts(x, n)
    key = str(method).lower().strip()
    if key in _NO_PVALUE:
        raise ValueError(
            f"pvalue() does not support method {method!r} (stochastic CI; "
            "the alpha-duality search needs a deterministic boundary)"
        )
    if key not in _METHODS:
        raise ValueError(f"unknown method {method!r}; choose from {sorted(set(_METHODS))}")
    if not 0 <= theta0 <= 1:
        raise ValueError("'theta0' has to be between 0 and 1")

    lo, hi = 1e-8, 1 - 1e-6
    if not _rejects(x, n, hi, theta0, key):
        return 1.0  # never rejected, even at the narrowest CI tested
    if _rejects(x, n, lo, theta0, key):
        return 0.0  # rejected even at the widest CI tested
    # Bisection on alpha. 16 halvings resolves alpha to ~1/2**16 =~ 1.5e-5 --
    # comfortably past the precision any p-value is read to. Kept modest on
    # purpose: each step recomputes the method's *whole* CI table
    # (root-finding methods like Blaker/LR/exact loop over every x
    # internally), so this scales with n and with how expensive that method's
    # CI already is -- see the pvalue() docstring's performance note.
    for _ in range(16):
        mid = (lo + hi) / 2
        if _rejects(x, n, mid, theta0, key):
            hi = mid
        else:
            lo = mid
    return hi


def reject(x, n, theta0, method="wilson", alpha=0.05):
    r"""Reject :math:`H_0: \theta = \theta_0` at level ``alpha``? (CI-test duality.)

    A thin wrapper around :func:`pvalue`: ``True`` (reject) iff
    ``pvalue(x, n, theta0, method) < alpha`` — equivalently, iff ``theta0``
    falls outside ``bk.ci(x=x, n=n, alpha=alpha, method=method)``. Named
    ``reject`` rather than ``test`` to avoid colliding with the word every
    Python testing tool uses.

    >>> reject(3, 20, 0.5, method="exact")       # 0.5 is way outside the CI
    True
    >>> reject(3, 20, 0.15, method="exact")      # 0.15 == phat
    False
    """
    return pvalue(x, n, theta0, method=method) < alpha


# --- sample-size / power planning --------------------------------------------
def _width_at(method, n, alpha, p0):
    """Width of method's (1-alpha) CI at n, for the x nearest p0*n.

    Uses the single-``x`` dispatcher (``ciwdx``/``ciexx``/``ciblakerx``/...),
    not the whole-table one: a sample-size search calls this ``O(log n_max)``
    times, and root-finding methods (exact/LR/Blaker) computing their full
    ``n+1``-row table on every call would make that search cost ``O(n_max)``
    instead -- the same trap ``pvalue()`` had to be tuned around.
    """
    x = min(max(int(round(p0 * n)), 0), n)
    row = _ci(x=x, n=n, alpha=alpha, method=method)
    lo_col = [c for c in row.columns if c.startswith("L")][0]
    hi_col = [c for c in row.columns if c.startswith("U")][0]
    return float(row[hi_col].iloc[0]) - float(row[lo_col].iloc[0])


def sample_size(width, alpha=0.05, p0=0.5, method="wilson", n_max=100_000):
    r"""Smallest ``n`` whose ``(1-alpha)`` CI (for ``method``) is no wider than ``width``.

    Not part of R ``proportion`` — sample-size determination is a *pre-data*
    design question, outside the scope of interval *estimation*; a dedicated
    package (R `binomSamSize`) already existed, which the ported paper cites
    rather than duplicating. binomcikit adds it because it is the natural
    question practitioners ask before collecting data, and because — unlike
    the textbook Wald-only formula — it works for **any** registered method.

    "Width" is evaluated at the ``x`` nearest ``p0 * n`` (the standard
    sample-size-planning convention: plan around a guessed proportion ``p0``,
    default ``0.5`` — the worst case, since every method's CI is widest
    there). ``n`` is found by binary search (CI width shrinks monotonically
    in ``n`` for every method here), so this returns the *exact* smallest
    integer ``n`` for ``method``'s actual CI, not an approximation.

    Parameters
    ----------
    width : float
        The target CI width, in ``(0, 1)``.
    alpha : float, default 0.05
        Significance level; the interval has confidence ``1 - alpha``.
    p0 : float, default 0.5
        The proportion to plan around (worst case at ``0.5``, where every
        symmetric method is widest).
    method : str, default "wilson"
        Any method name :func:`binomcikit.ci` accepts, except the bootstrap
        family (a stochastic CI has no well-defined "width at n").
    n_max : int, default 100_000
        Upper search bound; raises if not even ``n_max`` reaches ``width``.

    Returns
    -------
    int

    See Also
    --------
    power : The complementary pre-data question -- given n, how likely is
        the study to detect a real effect?

    Examples
    --------
    >>> sample_size(0.1, method="wilson")     # width <= 0.1 at p0=0.5, 95% CI
    381
    >>> sample_size(0.2, method="wilson")     # a looser target needs far fewer trials
    93
    """
    key = str(method).lower().strip()
    if key in _NO_PVALUE:
        raise ValueError(
            f"sample_size() does not support method {method!r} (stochastic CI; "
            "width at a given n is not well-defined without pinning a seed)"
        )
    if key not in _METHODS:
        raise ValueError(f"unknown method {method!r}; choose from {sorted(set(_METHODS))}")
    if not 0 < width < 1:
        raise ValueError("'width' has to be between 0 and 1")
    if not 0 < p0 < 1:
        raise ValueError("'p0' has to be between 0 and 1")

    if _width_at(key, n_max, alpha, p0) > width:
        raise ValueError(f"target width {width} not reached by n_max={n_max}; raise n_max")
    lo, hi = 1, n_max
    while lo < hi:
        mid = (lo + hi) // 2
        if _width_at(key, mid, alpha, p0) <= width:
            hi = mid
        else:
            lo = mid + 1
    return hi


def power(n, theta0, p_true, alpha=0.05, method="wilson"):
    r"""Probability of rejecting :math:`H_0: \theta = \theta_0` if the true proportion is ``p_true``.

    Not part of R ``proportion`` (see :func:`sample_size`) — the power companion
    to :func:`pvalue`/:func:`reject`'s CI-test duality. Exact, not simulated:
    sums the rejection indicator over every possible ``x`` weighted by its
    Binomial(n, p_true) probability, using ``method``'s own ``(1-alpha)`` CI
    (computed once, not per ``x``) to decide which ``x`` reject ``theta0``.

    Parameters
    ----------
    n : int
        Planned number of trials.
    theta0 : float
        The null value being tested against.
    p_true : float
        The proportion you're assuming is actually true (the effect size to
        detect). Power is highest when ``p_true`` is far from ``theta0``.
    alpha : float, default 0.05
        Significance level.
    method : str, default "wilson"
        Any method name :func:`binomcikit.ci` accepts, except the bootstrap family.

    Returns
    -------
    float
        The power, in ``[0, 1]``.

    Examples
    --------
    >>> round(power(100, 0.5, 0.65, method="wilson"), 3)   # detect p=0.65 vs H0: p=0.5, n=100
    0.875
    >>> round(power(100, 0.5, 0.5, method="wilson"), 3)    # at p_true == theta0: power == the test's actual size
    0.057
    """
    key = str(method).lower().strip()
    if key in _NO_PVALUE:
        raise ValueError(
            f"power() does not support method {method!r} (stochastic CI; "
            "rejection at a given alpha is not well-defined without pinning a seed)"
        )
    if key not in _METHODS:
        raise ValueError(f"unknown method {method!r}; choose from {sorted(set(_METHODS))}")
    for name, val in (("theta0", theta0), ("p_true", p_true)):
        if not 0 <= val <= 1:
            raise ValueError(f"'{name}' has to be between 0 and 1")

    lower, upper, _ = _limits(key, n, alpha)  # computed once for the whole x-grid
    lower = np.asarray(lower, dtype=float)
    upper = np.asarray(upper, dtype=float)
    rejects = (theta0 < lower) | (theta0 > upper)
    k = np.arange(n + 1)
    pmf = stats.binom.pmf(k, n, p_true)
    return float((pmf * rejects).sum())


def recommend(
    n: int,
    alpha: float = 0.05,
    by: str = "length",
    points: int = 200,
    methods: Sequence[str] | None = None,
) -> pd.DataFrame:
    """Rank methods for a given ``n`` by measuring them on the metric engine.

    For each method it computes, over a grid of the true proportion, the mean and
    minimum {term}`coverage` and the mean {term}`expected length`, and flags whether
    the method is ``adequate`` (mean coverage within 0.02 of nominal — i.e. not badly
    under-covering). It then sorts:

    * ``by="length"`` — narrowest mean length first, but **adequate methods first** so a
      narrow-because-under-covering method (Wald, ArcSine) never wins on a technicality;
    * ``by="coverage"`` — closest mean coverage to nominal first;
    * ``by="min_coverage"`` — highest guaranteed (minimum) coverage first.

    Returns a tidy ``DataFrame`` — turning the method-selection guide into code.
    """
    nominal = 1 - alpha
    theta = np.linspace(1e-4, 1 - 1e-4, points)
    k = np.arange(n + 1)
    pmf = stats.binom.pmf(k[:, None], n, theta[None, :])
    rows = []
    for m in _method_keys(methods):
        lower, upper, label = _limits(m, n, alpha)
        cp = coverage_series(n, lower, upper, theta)
        width = np.asarray(upper, dtype=float) - np.asarray(lower, dtype=float)
        el = (width[:, None] * pmf).sum(axis=0)
        mean_cov = float(cp.mean())
        rows.append(
            {
                "method": label,
                "mean_coverage": mean_cov,
                "min_coverage": float(cp.min()),
                "mean_length": float(el.mean()),
                "coverage_gap": float(abs(mean_cov - nominal)),
                "adequate": mean_cov >= nominal - 0.02,
            }
        )
    df = pd.DataFrame(rows)
    by_key = str(by).lower().strip()
    if by_key == "length":
        # adequate methods first (True sorts before False when descending), then narrowest
        return df.sort_values(["adequate", "mean_length"], ascending=[False, True]).reset_index(
            drop=True
        )
    key = {
        "coverage": ("coverage_gap", True),
        "min_coverage": ("min_coverage", False),
    }.get(by_key)
    if key is None:
        raise ValueError(f"unknown 'by' {by!r}; choose from length, coverage, min_coverage")
    col, ascending = key
    return df.sort_values(col, ascending=ascending).reset_index(drop=True)
