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
from .plotly_viz import _METHODS, _limits

# Named conjugate priors for the Bayesian helpers.
PRIORS: dict[str, tuple[float, float]] = {
    "jeffreys": (0.5, 0.5),
    "laplace": (1.0, 1.0),
    "uniform": (1.0, 1.0),
    "haldane": (0.0, 0.0),
}

# Canonical comparable methods (keys of the shared limit registry, no aliases).
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

    >>> round(point_estimate(0, 20, "mle"), 3)
    0.0
    >>> round(point_estimate(0, 20, "laplace"), 3)     # prior lifts it off zero
    0.045
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
    raise ValueError(f"unknown method {method!r}; choose from mle, ac, jeffreys, laplace")


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
