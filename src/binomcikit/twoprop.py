"""Confidence intervals for the **difference of two independent binomial proportions**.

For ``X1 ~ Bin(n1, p1)`` and ``X2 ~ Bin(n2, p2)`` the interval is for ``delta = p1 - p2``. The
methods are the ones recommended in Newcombe (1998) and Fagerland, Lydersen & Laake (2011):

=============================  ===========================================================
``wald``                       ``d +- z * sqrt(p1 q1 / n1 + p2 q2 / n2)``
``wald-cc``                    Wald widened by the Fleiss continuity correction ``(1/n1 + 1/n2) / 2``
``agresti-caffo``              Wald after adding one success and one failure to each sample
``newcombe``                   hybrid score: the two Wilson intervals combined (Newcombe's method 10)
``newcombe-cc``                the same from continuity-corrected Wilson intervals (method 11)
``mee``                        score interval, restricted MLE variance (Mee 1984)
``miettinen-nurminen``         ``mee`` with the ``N / (N - 1)`` variance factor (Miettinen & Nurminen 1985)
``haldane``                    Haldane's interval (Newcombe's method 3)
``jeffreys-perks``             Haldane's form with Jeffreys-Perks shrunken proportions (method 4)
``hauck-anderson``             Wald with ``n - 1`` variances and a ``1 / (2 min(n1, n2))`` correction
``brown-li``                   Wald around the Jeffreys-shrunken proportions ``(x + 1/2) / (n + 1)``
``miettinen-nurminen-brown-li``  ``2/3`` of the MN limits plus ``1/3`` of the Brown-Li limits
=============================  ===========================================================

Every method returns limits clipped to ``[-1, 1]`` (a difference of proportions cannot leave it).
:func:`diff_interval` returns the two limits, :func:`diff_ci` a one-row table, and
:func:`list_diff_methods` the catalogue. Inputs may be scalars or broadcastable arrays.

References
----------
* Newcombe (1998), *Interval estimation for the difference between independent proportions:
  comparison of eleven methods*, Statistics in Medicine 17, 873-890.
* Miettinen & Nurminen (1985), *Comparative analysis of two rates*, Statistics in Medicine 4.
* Mee (1984), *Confidence bounds for the difference between two probabilities*, Biometrics 40.
* Agresti & Caffo (2000), *Simple and effective confidence intervals for proportions and
  differences of proportions result from adding two successes and two failures*, Am. Statistician 54.
* Fagerland, Lydersen & Laake (2011), *Recommended confidence intervals for two independent
  binomial proportions*, Statistical Methods in Medical Research 24.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy import optimize

from .ci import _fast

__all__ = ["diff_ci", "diff_interval", "list_diff_methods"]

_EPS = 1e-12


# ------------------------------------------------------------------------------ closed forms
def _wald(x1, n1, x2, n2, z, cc=False):
    p1, p2 = x1 / n1, x2 / n2
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    half = z * se + (0.5 * (1 / n1 + 1 / n2) if cc else 0.0)
    d = p1 - p2
    return d - half, d + half


def _agresti_caffo(x1, n1, x2, n2, z):
    p1, p2 = (x1 + 1) / (n1 + 2), (x2 + 1) / (n2 + 2)
    se = math.sqrt(p1 * (1 - p1) / (n1 + 2) + p2 * (1 - p2) / (n2 + 2))
    d = p1 - p2
    return d - z * se, d + z * se


def _wilson(x, n, z, cc=False):
    """Wilson score limits for one sample; ``cc`` adds Newcombe's continuity correction."""
    p = x / n
    z2 = z * z
    den = 2 * (n + z2)
    if not cc:
        mid = 2 * n * p + z2
        h = z * math.sqrt(z2 + 4 * n * p * (1 - p))
        return (mid - h) / den, (mid + h) / den
    lo = 0.0
    hi = 1.0
    if x > 0:
        lo = (2 * n * p + z2 - 1 - z * math.sqrt(z2 - 2 - 1 / n + 4 * p * (n * (1 - p) + 1))) / den
    if x < n:
        hi = (2 * n * p + z2 + 1 + z * math.sqrt(z2 + 2 - 1 / n + 4 * p * (n * (1 - p) - 1))) / den
    return max(lo, 0.0), min(hi, 1.0)


def _newcombe(x1, n1, x2, n2, z, cc=False):
    p1, p2 = x1 / n1, x2 / n2
    l1, u1 = _wilson(x1, n1, z, cc)
    l2, u2 = _wilson(x2, n2, z, cc)
    d = p1 - p2
    return d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2), d + math.sqrt(
        (u1 - p1) ** 2 + (p2 - l2) ** 2
    )


def _haldane(x1, n1, x2, n2, z, jeffreys_perks=False):
    """Haldane's (and, with shrunken proportions, Jeffreys-Perks') interval: ``theta* +- w``."""
    p1, p2 = x1 / n1, x2 / n2
    if jeffreys_perks:
        psi = 0.5 * ((x1 + 0.5) / (n1 + 1) + (x2 + 0.5) / (n2 + 1))
    else:
        psi = 0.5 * (p1 + p2)
    d = p1 - p2
    u = (1 / n1 + 1 / n2) / 4
    v = (1 / n1 - 1 / n2) / 4
    z2 = z * z
    den = 1 + z2 * u
    centre = (d + z2 * v * (1 - 2 * psi)) / den
    inside = (
        u * (4 * psi * (1 - psi) - d * d)
        + 2 * v * (1 - 2 * psi) * d
        + 4 * z2 * u * u * (1 - psi) * psi
        + z2 * v * v * (1 - 2 * psi) ** 2
    )
    half = z / den * math.sqrt(max(inside, 0.0))
    return centre - half, centre + half


def _hauck_anderson(x1, n1, x2, n2, z):
    if n1 < 2 or n2 < 2:
        raise ValueError("'hauck-anderson' needs at least 2 trials in each sample")
    p1, p2 = x1 / n1, x2 / n2
    se = math.sqrt(p1 * (1 - p1) / (n1 - 1) + p2 * (1 - p2) / (n2 - 1))
    half = 1 / (2 * min(n1, n2)) + z * se
    d = p1 - p2
    return d - half, d + half


def _brown_li(x1, n1, x2, n2, z):
    """Brown & Li's Jeffreys interval: Wald around the Jeffreys-shrunken proportions."""
    p1, p2 = (x1 + 0.5) / (n1 + 1), (x2 + 0.5) / (n2 + 1)
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    d = p1 - p2
    return d - z * se, d + z * se


def _mn_brown_li(x1, n1, x2, n2, z, k=2.0 / 3.0):
    """Laud & Dane's weighted average ``k * MN + (1 - k) * Brown-Li`` of the two limits."""
    lo_mn, hi_mn = _score_limits(x1, n1, x2, n2, z, True)
    lo_bl, hi_bl = _brown_li(x1, n1, x2, n2, z)
    return k * lo_mn + (1 - k) * lo_bl, k * hi_mn + (1 - k) * hi_bl


# ------------------------------------------------------------------------------ score methods
def _restricted_mle(x1, n1, x2, n2, delta):
    """MLE of ``(p1, p2)`` under ``p1 - p2 = delta``: the log-likelihood is concave in ``p1``."""
    lo, hi = max(0.0, delta), min(1.0, 1.0 + delta)

    def score(p):
        out = 0.0
        out += x1 / p - (n1 - x1) / (1 - p)
        out += x2 / (p - delta) - (n2 - x2) / (1 - p + delta)
        return out

    a, b = lo + _EPS, hi - _EPS
    if a >= b:
        p1 = 0.5 * (lo + hi)
    elif score(a) <= 0:
        p1 = lo
    elif score(b) >= 0:
        p1 = hi
    else:
        p1 = optimize.brentq(score, a, b, xtol=1e-14, rtol=1e-14)
    return p1, p1 - delta


def _score_stat2(x1, n1, x2, n2, delta, factor):
    """Squared score statistic ``(d - delta)^2 / V(delta)`` (``inf`` when the variance is 0)."""
    p1, p2 = x1 / n1, x2 / n2
    q1, q2 = _restricted_mle(x1, n1, x2, n2, delta)
    var = factor * (q1 * (1 - q1) / n1 + q2 * (1 - q2) / n2)
    num = (p1 - p2 - delta) ** 2
    if var <= 0:
        return math.inf if num > 0 else 0.0
    return num / var


def _score_limits(x1, n1, x2, n2, z, miettinen_nurminen):
    d = x1 / n1 - x2 / n2
    factor = (n1 + n2) / (n1 + n2 - 1) if miettinen_nurminen else 1.0
    z2 = z * z

    def f(delta):
        return _score_stat2(x1, n1, x2, n2, delta, factor) - z2

    # the statistic is 0 at delta = d and grows away from it; look for the crossing on each side
    upper = 1.0
    if d < 1.0:
        hi = 1.0 - _EPS
        upper = optimize.brentq(f, d, hi, xtol=1e-14, rtol=1e-14) if f(hi) > 0 else 1.0
    lower = -1.0
    if d > -1.0:
        lo = -1.0 + _EPS
        lower = optimize.brentq(f, lo, d, xtol=1e-14, rtol=1e-14) if f(lo) > 0 else -1.0
    return lower, upper


# ------------------------------------------------------------------------------ dispatcher
def _kernels(z):
    return {
        "wald": lambda a, b, c, d: _wald(a, b, c, d, z),
        "wald-cc": lambda a, b, c, d: _wald(a, b, c, d, z, cc=True),
        "agresti-caffo": lambda a, b, c, d: _agresti_caffo(a, b, c, d, z),
        "newcombe": lambda a, b, c, d: _newcombe(a, b, c, d, z),
        "newcombe-cc": lambda a, b, c, d: _newcombe(a, b, c, d, z, cc=True),
        "mee": lambda a, b, c, d: _score_limits(a, b, c, d, z, False),
        "miettinen-nurminen": lambda a, b, c, d: _score_limits(a, b, c, d, z, True),
        "haldane": lambda a, b, c, d: _haldane(a, b, c, d, z),
        "jeffreys-perks": lambda a, b, c, d: _haldane(a, b, c, d, z, jeffreys_perks=True),
        "hauck-anderson": lambda a, b, c, d: _hauck_anderson(a, b, c, d, z),
        "brown-li": lambda a, b, c, d: _brown_li(a, b, c, d, z),
        "miettinen-nurminen-brown-li": lambda a, b, c, d: _mn_brown_li(a, b, c, d, z),
    }


_ALIASES = {
    "hybrid-score": "newcombe",
    "wilson-hybrid": "newcombe",
    "newcomb": "newcombe",
    "mn": "miettinen-nurminen",
    "score": "miettinen-nurminen",
    "ac": "agresti-caffo",
    "fleiss": "wald-cc",
}

_CATALOGUE = [
    ("wald", "Wald", "closed-form", "Wald (normal approximation)"),
    ("wald-cc", "Wald, continuity-corrected", "closed-form", "Fleiss 1981"),
    ("agresti-caffo", "Agresti-Caffo", "closed-form", "Agresti & Caffo 2000, Am. Stat. 54"),
    (
        "newcombe",
        "Newcombe hybrid score",
        "closed-form",
        "Newcombe 1998, Stat. Med. 17 (method 10)",
    ),
    (
        "newcombe-cc",
        "Newcombe hybrid score, continuity-corrected",
        "closed-form",
        "Newcombe 1998, Stat. Med. 17 (method 11)",
    ),
    ("mee", "Mee score", "root-finding", "Mee 1984, Biometrics 40"),
    (
        "miettinen-nurminen",
        "Miettinen-Nurminen score",
        "root-finding",
        "Miettinen & Nurminen 1985, Stat. Med. 4",
    ),
    ("haldane", "Haldane", "closed-form", "Newcombe 1998, Stat. Med. 17 (method 3)"),
    ("jeffreys-perks", "Jeffreys-Perks", "closed-form", "Newcombe 1998, Stat. Med. 17 (method 4)"),
    ("hauck-anderson", "Hauck-Anderson", "closed-form", "Hauck & Anderson 1986, Am. Stat. 40"),
    (
        "brown-li",
        "Brown-Li (Jeffreys)",
        "closed-form",
        "Brown & Li 2005, J. Stat. Plan. Inference 130",
    ),
    (
        "miettinen-nurminen-brown-li",
        "Miettinen-Nurminen / Brown-Li blend",
        "root-finding",
        "Laud & Dane 2014 (k = 2/3 weighting of the two limits)",
    ),
]


def list_diff_methods():
    """Catalogue of the difference-of-proportions methods (one row per method)."""
    return pd.DataFrame(_CATALOGUE, columns=["method", "label", "cost", "reference"])


def _validate(x1, n1, x2, n2, alpha):
    if not 0 < alpha < 1:
        raise ValueError("'alpha' has to be strictly between 0 and 1")
    for name, n in (("n1", n1), ("n2", n2)):
        if np.any(np.asarray(n) <= 0) or np.any(np.asarray(n) != np.floor(n)):
            raise ValueError(f"'{name}' has to be a positive integer")
    for name, x, n in (("x1", x1, n1), ("x2", x2, n2)):
        if np.any(np.asarray(x) < 0) or np.any(np.asarray(x) > np.asarray(n)):
            raise ValueError(f"'{name}' has to be an integer between 0 and its sample size")
        if np.any(np.asarray(x) != np.floor(x)):
            raise ValueError(f"'{name}' has to be an integer")


def diff_interval(x1, n1, x2, n2, alpha=0.05, method="newcombe"):
    """Confidence interval ``(lower, upper)`` for ``p1 - p2`` from two independent samples.

    Parameters
    ----------
    x1, n1, x2, n2 : int or array-like
        Successes and trials in each sample (scalars, or arrays that broadcast together).
    alpha : float, default 0.05
        Significance level; the interval has nominal coverage ``1 - alpha``.
    method : str, default ``"newcombe"``
        One of :func:`list_diff_methods` (``"mn"`` / ``"score"`` are aliases of
        ``"miettinen-nurminen"``). Newcombe's hybrid score is the default: it never leaves
        ``[-1, 1]``, is defined for every table (including zero cells) and has good coverage.

    Returns
    -------
    tuple of float (or of arrays)
        ``(lower, upper)``, clipped to ``[-1, 1]``.
    """
    key = _ALIASES.get(str(method).lower().strip(), str(method).lower().strip())
    _validate(x1, n1, x2, n2, alpha)
    z = _fast.zcrit(alpha)
    kernels = _kernels(z)
    if key not in kernels:
        known = sorted(set(kernels) | set(_ALIASES))
        raise ValueError(f"unknown method {method!r}; choose from {known}")
    kernel = kernels[key]
    a, b, c, d = np.broadcast_arrays(*(np.asarray(v) for v in (x1, n1, x2, n2)))
    if a.ndim == 0:
        lo, hi = kernel(int(a), int(b), int(c), int(d))
        return float(max(lo, -1.0)), float(min(hi, 1.0))
    lo = np.empty(a.shape)
    hi = np.empty(a.shape)
    for idx in np.ndindex(a.shape):
        lo[idx], hi[idx] = kernel(int(a[idx]), int(b[idx]), int(c[idx]), int(d[idx]))
    return np.maximum(lo, -1.0), np.minimum(hi, 1.0)


def diff_ci(x1, n1, x2, n2, alpha=0.05, method="newcombe"):
    """One-row table: estimate and interval for ``p1 - p2`` (scalar inputs)."""
    lo, hi = diff_interval(x1, n1, x2, n2, alpha, method)
    return pd.DataFrame(
        {
            "method": [str(method).lower()],
            "x1": [x1],
            "n1": [n1],
            "x2": [x2],
            "n2": [n2],
            "estimate": [x1 / n1 - x2 / n2],
            "lower": [lo],
            "upper": [hi],
            "width": [hi - lo],
        }
    )
