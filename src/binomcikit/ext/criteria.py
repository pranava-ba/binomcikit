"""Evaluation *criteria* for an interval estimator (as opposed to interval methods).

``locally_correct`` implements the criterion of Garthwaite, Moustafa & Elfadaly (2024, *Scand. J.
Statist.* 51, 220-244): an equal-tailed interval estimator is **locally correct** if, for each tail,
the coverage *averaged between every pair of consecutive coverage spikes* is at least ``1 - alpha/2``.
It is weaker than "coverage >= 1 - alpha for every theta" (which only Clopper-Pearson-type exact
intervals meet) yet, unlike "coverage is close to nominal", has a precise pass/fail definition.
The paper shows Clopper-Pearson and Mid-P (for ``alpha < 0.1``) are locally correct and Wilson is
not -- facts the test-suite reproduces with this function.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.special import betainc


def _g(i, n, p):
    """``G_i(p) = int_0^p P(X >= i | t) dt = p I_p(i, n-i+1) - i/(n+1) I_p(i+1, n-i+1)``."""
    return p * betainc(i, n - i + 1, p) - i / (n + 1.0) * betainc(i + 1, n - i + 1, p)


def cycle_averages(n, lower, upper):
    """Average one-sided coverage on every cycle between consecutive limits (both tails).

    Returns a tidy ``DataFrame(side, cycle, left, right, average)``; cycles of zero width are
    skipped. ``upper`` limits must be non-decreasing in ``x`` (so ``(u_{i-1}, u_i)`` is a cycle of
    ``P(X >= i | p)``), and so must ``lower`` (cycles of ``P(X <= i | p)``).
    """
    lower = np.asarray(lower, dtype=float)
    upper = np.asarray(upper, dtype=float)
    rows = []
    for i in range(1, n + 1):  # upper tail: coverage P(X >= i | p) for p in (u_{i-1}, u_i]
        a, b = upper[i - 1], upper[i]
        if b - a > 1e-14:
            rows.append(("upper", i, a, b, (_g(i, n, b) - _g(i, n, a)) / (b - a)))
    for i in range(n):  # lower tail: coverage P(X <= i | p) for p in [l_i, l_{i+1})
        a, b = lower[i], lower[i + 1]
        if b - a > 1e-14:
            avg = 1.0 - (_g(i + 1, n, b) - _g(i + 1, n, a)) / (b - a)
            rows.append(("lower", i, a, b, avg))
    return pd.DataFrame(rows, columns=["side", "cycle", "left", "right", "average"])


def locally_correct(n, alpha=0.05, method="wilson", tol=1e-9, **params):
    r"""Is ``method`` a *locally correct* interval estimator at ``(n, alpha)``?

    Computes the average coverage over every cycle of each tail (exactly, by closed-form integrals --
    no simulation) and compares it with the one-sided target :math:`1-\alpha/2`.

    Parameters
    ----------
    n : int
        Number of trials.
    alpha : float
        Two-sided significance level (each tail is judged at :math:`1-\alpha/2`).
    method : str
        Any method name :func:`binomcikit.ci` accepts.
    tol : float
        Slack when comparing an average with the target.

    Returns
    -------
    dict
        ``{"locally_correct": bool, "upper_ok": bool, "lower_ok": bool, "min_average": float,
        "target": float, "cycles": DataFrame}`` -- ``cycles`` lists every cycle and its average, so
        you can see *where* an interval falls short.

    Notes
    -----
    The criterion is defined for equal-tailed intervals; non-equal-tailed methods (Sterne,
    Blyth-Still-Casella) are judged tail by tail with the same target, which they may legitimately
    miss. Limits must be monotone in ``x``; the check reports ``False`` otherwise.

    Examples
    --------
    >>> import binomcikit as bk
    >>> bk.locally_correct(20, 0.05, "exact")["locally_correct"]
    True
    >>> bk.locally_correct(20, 0.05, "wilson")["locally_correct"]
    False
    """
    from ..limits import limits

    lo, hi = limits(int(n), alpha, method, **params)
    target = 1.0 - alpha / 2.0
    monotone = bool(
        np.all(np.diff(hi) >= -1e-12) and np.all(np.diff(lo) >= -1e-12) and hi[-1] >= 1 - 1e-12
    )
    cyc = cycle_averages(int(n), lo, hi)
    upper = cyc[cyc.side == "upper"].average
    lower = cyc[cyc.side == "lower"].average
    upper_ok = bool((upper >= target - tol).all()) if len(upper) else False
    lower_ok = bool((lower >= target - tol).all()) if len(lower) else False
    return {
        "locally_correct": bool(monotone and upper_ok and lower_ok),
        "upper_ok": upper_ok,
        "lower_ok": lower_ok,
        "min_average": float(cyc.average.min()) if len(cyc) else float("nan"),
        "target": target,
        "cycles": cyc,
    }
