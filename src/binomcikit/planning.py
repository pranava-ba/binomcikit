"""Sample-size, interval-width and power planning for a single binomial proportion.

Everything a practitioner reaches for PASS (NCSS) or SAS ``PROC POWER`` to do for *one*
proportion, implemented from their published documentation and verified against it:

========================  =========================================================
Question                  Function
========================  =========================================================
How many subjects for a   :func:`binomcikit.sample_size` (``plug_in="continuous"`` is
CI of a given width?      PASS Chapter 115; ``sides`` for one-sided distance)
How likely is a trial of  :func:`prob_width` (SAS ``PROBWIDTH=``) and
``n`` to hit that width?  :func:`expected_width`
How many for an           :func:`sample_size_assurance` (smallest ``n`` whose
*assured* width?          probability of meeting the width reaches a target)
Power / sample size of    :func:`power_test`, :func:`sample_size_test` (exact test,
a hypothesis test?        z test, continuity-adjusted z; SAS ``ONESAMPLEFREQ``)
Equivalence (TOST)?       :func:`power_equivalence`, :func:`sample_size_equivalence`
Allow for dropout?        :func:`inflate_for_dropout`
========================  =========================================================

Two conventions matter and are made explicit rather than hidden:

* **Plug-in width.** PASS plans at a *real-valued* sample proportion ``p-hat = P`` (so
  ``x = P n`` need not be an integer); the original ``sample_size`` rounds ``x`` to the
  nearest integer. ``plug_in="continuous"`` reproduces PASS exactly.
* **Discreteness.** Probabilities that depend on ``n`` through a discrete rejection region
  or interval are *saw-toothed*: power or assurance can dip as ``n`` grows. The searches
  return the **smallest** ``n`` that reaches the target (the SAS/PASS convention);
  ``lookahead=`` additionally demands the target holds for the next ``lookahead`` sizes.

References
----------
* NCSS PASS, *Chapter 115: Confidence Intervals for One Proportion*.
* SAS/STAT *The POWER Procedure*, ONESAMPLEFREQ statement and its computational details
  (exact test, normal-approximate tests, TOST equivalence, confidence-interval precision).
* Newcombe (1998), *Two-sided confidence intervals for the single proportion: comparison of
  seven methods*, Statist. Med. 17.
"""

from __future__ import annotations

import math

import numpy as np
import scipy.stats as stats

from .plotly_viz import _METHODS, _limits

# --------------------------------------------------------------------------- intervals
_REAL_METHODS = {
    "wald": "wald",
    "wald-cc": "wald-cc",
    "waldcc": "wald-cc",
    "wald-corrected": "wald-cc",
    "wilson": "wilson",
    "score": "wilson",
    "wilson-cc": "wilson-cc",
    "score-cc": "wilson-cc",
    "agresti-coull": "agresti-coull",
    "ac": "agresti-coull",
    "exact": "exact",
    "cp": "exact",
    "clopper-pearson": "exact",
    "jeffreys": "jeffreys",
}


def _real_interval(method, n, a_total, x):
    """Two-sided ``(1 - a_total)`` limits at *real-valued* counts ``x`` (vectorised).

    ``method`` is a canonical name from ``_REAL_METHODS``. These are the closed forms PASS
    and SAS document (Newcombe 1998 for the continuity-corrected score).
    """
    x = np.asarray(x, dtype=float)
    z = stats.norm.ppf(1 - a_total / 2)
    p = x / n
    if method == "wald":
        h = z * np.sqrt(p * (1 - p) / n)
        lo, hi = p - h, p + h
    elif method == "wald-cc":
        h = z * np.sqrt(p * (1 - p) / n) + 1 / (2 * n)
        lo, hi = p - h, p + h
    elif method == "wilson":
        mid = (p + z * z / (2 * n)) / (1 + z * z / n)
        h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
        lo, hi = mid - h, mid + h
    elif method == "wilson-cc":
        with np.errstate(invalid="ignore"):
            d = 2 * (n + z * z)
            lo = (
                2 * n * p
                + z * z
                - 1
                - z * np.sqrt(np.maximum(z * z - (2 + 1 / n) + 4 * p * (n * (1 - p) + 1), 0.0))
            ) / d
            hi = (
                2 * n * p
                + z * z
                + 1
                + z * np.sqrt(np.maximum(z * z + (2 - 1 / n) + 4 * p * (n * (1 - p) - 1), 0.0))
            ) / d
        lo = np.where(x <= 0, 0.0, lo)
        hi = np.where(x >= n, 1.0, hi)
    elif method == "agresti-coull":
        nt = n + z * z
        pt = (x + z * z / 2) / nt
        h = z * np.sqrt(pt * (1 - pt) / nt)
        lo, hi = pt - h, pt + h
    elif method == "exact":
        with np.errstate(invalid="ignore"):
            lo = np.where(x > 0, stats.beta.ppf(a_total / 2, np.maximum(x, 1e-300), n - x + 1), 0.0)
            hi = np.where(
                x < n, stats.beta.ppf(1 - a_total / 2, x + 1, np.maximum(n - x, 1e-300)), 1.0
            )
    elif method == "jeffreys":
        lo = np.where(x > 0, stats.beta.ppf(a_total / 2, x + 0.5, n - x + 0.5), 0.0)
        hi = np.where(x < n, stats.beta.ppf(1 - a_total / 2, x + 0.5, n - x + 0.5), 1.0)
    else:  # pragma: no cover - guarded by the caller
        raise ValueError(f"unsupported method {method!r}")
    return np.clip(lo, 0.0, 1.0), np.clip(hi, 0.0, 1.0)


def _canon(method):
    key = str(method).lower().strip()
    return _REAL_METHODS.get(key)


def _check_common(alpha=None, p=None, name="p"):
    if alpha is not None and not 0 < alpha < 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if p is not None and not 0 <= p <= 1:
        raise ValueError(f"'{name}' has to be between 0 and 1")


def _a_total(alpha, sides):
    """The two-sided level whose limits give a one-/two-sided interval at ``alpha``."""
    return alpha if sides == 2 else 2 * alpha


def _norm_sides(sides):
    s = str(sides).lower().strip()
    if s in ("2", "two", "two-sided", "both"):
        return 2
    if s in ("1", "upper", "u", "greater"):
        return "upper"
    if s in ("lower", "l", "less"):
        return "lower"
    raise ValueError("'sides' has to be 2, 'upper' or 'lower'")


# ------------------------------------------------------------------------ CI sample size
def _width_continuous(method, n, alpha, p0, sides):
    lo, hi = _real_interval(method, n, _a_total(alpha, 2 if sides == 2 else 1), np.array(p0 * n))
    lo, hi = float(lo), float(hi)
    if sides == 2:
        return hi - lo, lo, hi
    return (hi - p0 if sides == "upper" else p0 - lo), lo, hi


def _smallest_n(ok, n_max):
    """Smallest ``n`` with ``ok(n)`` true: binary search, then walk down any saw-tooth."""
    if not ok(n_max):
        return None
    lo, hi = 1, n_max
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    n = hi
    for _ in range(
        200
    ):  # the width can wiggle by one trial for some methods; take the true minimum
        if n > 1 and ok(n - 1):
            n -= 1
        else:
            break
    return n


def sample_size_ci(
    width, alpha=0.05, p0=0.5, method="wilson", n_max=100_000, plug_in="continuous", sides=2
):
    """Smallest ``n`` (and the interval it gives) for a confidence interval of a target width.

    This is the engine behind :func:`binomcikit.sample_size` when called with
    ``plug_in="continuous"`` / ``sides`` / ``details``. Returns ``(n, actual_width, lower, upper)``.
    """
    sides = _norm_sides(sides)
    _check_common(alpha, p0, "p0")
    if not 0 < width < 1:
        raise ValueError("'width' has to be between 0 and 1")
    if plug_in not in ("continuous", "nearest"):
        raise ValueError("'plug_in' has to be 'continuous' or 'nearest'")
    key = _canon(method)
    if key is None:
        raise ValueError(
            f"method {method!r} is not available for plug-in planning; use one of {sorted(set(_REAL_METHODS.values()))}"
        )
    if not 0 < p0 < 1:
        raise ValueError("'p0' has to be strictly between 0 and 1")

    def measure(n):
        if plug_in == "continuous":
            return _width_continuous(key, n, alpha, p0, sides)
        x = float(min(max(round(p0 * n), 0), n))
        a = _a_total(alpha, 2 if sides == 2 else 1)
        lo, hi = (float(v) for v in _real_interval(key, n, a, np.array(x)))
        ph = x / n
        w = hi - lo if sides == 2 else (hi - ph if sides == "upper" else ph - lo)
        return w, lo, hi

    n = _smallest_n(lambda m: measure(m)[0] <= width + 1e-12, n_max)
    if n is None:
        raise ValueError(f"target width {width} not reached by n_max={n_max}; raise n_max")
    w, lo, hi = measure(n)
    return n, w, lo, hi


def inflate_for_dropout(n, rate):
    """Enrolment size so that ``n`` *evaluable* subjects remain after a dropout ``rate``.

    PASS's rule: ``ceil(n / (1 - rate))``.

    >>> inflate_for_dropout(914, 0.20)
    1143
    """
    if not 0 <= rate < 1:
        raise ValueError("'rate' has to be in [0, 1)")
    return int(math.ceil(n / (1 - rate) - 1e-12))


# -------------------------------------------------------------------- width probabilities
def _limit_arrays(method, n, alpha, sides):
    """Per-``x`` interval limits for any method (closed-form fast path, registry otherwise)."""
    key = _canon(method)
    a = _a_total(alpha, 2 if sides == 2 else 1)
    if key is not None:
        return _real_interval(key, n, a, np.arange(n + 1, dtype=float))
    name = str(method).lower().strip()
    if name not in _METHODS:
        raise ValueError(
            f"unknown method {method!r}; choose from {sorted(set(_METHODS) | set(_REAL_METHODS))}"
        )
    lower, upper, _ = _limits(name, n, a)
    return np.asarray(lower, dtype=float), np.asarray(upper, dtype=float)


def prob_width(n, p, halfwidth, alpha=0.05, method="wilson", sides=2):
    r"""Probability that the confidence interval's half-width is at most ``halfwidth``.

    SAS ``PROC POWER``'s ``PROBWIDTH``: with true proportion ``p`` and ``n`` trials, sum the
    binomial probabilities of every outcome ``x`` whose interval half-width
    :math:`(U_x-L_x)/2` does not exceed ``halfwidth`` (for one-sided intervals the distance
    from :math:`\hat p` to the limit). Exact by enumeration -- no simulation. Works for the
    methods in the PASS/SAS lists (Wald, Wald with continuity correction, Wilson,
    continuity-corrected Wilson, Agresti-Coull, Clopper-Pearson, Jeffreys) **and for every other
    method binomcikit registers**.

    Parameters
    ----------
    n : int
        Planned number of trials.
    p : float
        The true proportion the trial will actually see.
    halfwidth : float
        The target half-width.
    alpha, method, sides : see :func:`binomcikit.sample_size`.

    Returns
    -------
    float

    Examples
    --------
    >>> round(prob_width(100, 0.2, 0.08, method="wilson"), 3)  # P(half-width <= 0.08), n=100, p=0.2
    0.654
    >>> round(prob_width(100, 0.2, 0.08, method="exact"), 3)    # the exact interval is wider
    0.362
    """
    sides = _norm_sides(sides)
    _check_common(alpha, p)
    if n < 1 or int(n) != n:
        raise ValueError("'n' has to be a positive integer")
    n = int(n)
    if halfwidth <= 0:
        raise ValueError("'halfwidth' has to be positive")
    lo, hi = _limit_arrays(method, n, alpha, sides)
    k = np.arange(n + 1)
    if sides == 2:
        half = (hi - lo) / 2
    elif sides == "upper":
        half = hi - k / n
    else:
        half = k / n - lo
    pmf = stats.binom.pmf(k, n, p)
    return min(1.0, float(pmf[half <= halfwidth + 1e-12].sum()))


def expected_width(n, p, alpha=0.05, method="wilson", sides=2):
    r"""Expected interval width :math:`E[U-L]` when the true proportion is ``p``.

    The scalar behind ``binGroup::binWidth``: :math:`\sum_x (U_x-L_x)\,P(X=x\mid n,p)`.
    One-sided intervals use the distance from :math:`\hat p` to the limit.
    """
    sides = _norm_sides(sides)
    _check_common(alpha, p)
    n = int(n)
    lo, hi = _limit_arrays(method, n, alpha, sides)
    k = np.arange(n + 1)
    w = hi - lo if sides == 2 else (hi - k / n if sides == "upper" else k / n - lo)
    return float((w * stats.binom.pmf(k, n, p)).sum())


def sample_size_assurance(
    halfwidth, assurance=0.9, p=0.5, alpha=0.05, method="wilson", n_max=20_000, lookahead=0, sides=2
):
    r"""Smallest ``n`` whose interval is *assured* to meet the half-width target.

    Planning at a plug-in :math:`\hat p` (``sample_size``) says the width is met *if* the
    data come out at :math:`p`; real data scatter around ``p``. This returns the smallest
    ``n`` with :func:`prob_width` :math:`\ge` ``assurance`` -- the probability the *realised*
    interval will be narrow enough. Because the probability saw-tooths in ``n``,
    ``lookahead=k`` additionally requires the target to hold for the next ``k`` sample sizes.

    Returns
    -------
    int

    Examples
    --------
    >>> sample_size_assurance(0.05, assurance=0.9, p=0.3, method="wilson") >= 323
    True
    """
    _check_common(alpha, p)
    if not 0 < assurance < 1:
        raise ValueError("'assurance' has to be between 0 and 1")
    if lookahead < 0:
        raise ValueError("'lookahead' has to be >= 0")
    z = stats.norm.ppf(1 - alpha / 2)
    start = max(
        1, int(0.5 * z * z * max(p * (1 - p), 1e-4) / halfwidth**2)
    )  # well below the answer
    for n in range(start, n_max + 1):
        if prob_width(n, p, halfwidth, alpha, method, sides) >= assurance and all(
            prob_width(n + j, p, halfwidth, alpha, method, sides) >= assurance
            for j in range(1, lookahead + 1)
        ):
            return n
    raise ValueError(f"assurance {assurance} not reached by n_max={n_max}; raise n_max")


# ----------------------------------------------------------------------- hypothesis tests
def _norm_alt(alternative):
    a = str(alternative).lower().strip()
    if a in ("two-sided", "two.sided", "2", "both", "two"):
        return "two-sided"
    if a in ("greater", "upper", "u", "1"):
        return "greater"
    if a in ("less", "lower", "l"):
        return "less"
    raise ValueError("'alternative' has to be 'two-sided', 'greater' or 'less'")


def _exact_region(n, null, alpha, alternative):
    """SAS critical values: each tail filled with as much probability as fits within its level."""
    k = np.arange(n + 1)
    cdf = stats.binom.cdf(k, n, null)  # P(X <= k)
    sf = stats.binom.sf(k - 1, n, null)  # P(X >= k)
    a = alpha / 2 if alternative == "two-sided" else alpha
    lower = k[cdf <= a + 1e-14]
    upper = k[sf <= a + 1e-14]
    c_l = int(lower.max()) if lower.size else -1
    c_u = int(upper.min()) if upper.size else n + 1
    return c_l, c_u


def _z_region(n, null, alpha, alternative, adjusted):
    k = np.arange(n + 1)
    sd = math.sqrt(n * null * (1 - null))
    delta = k - n * null
    if adjusted:  # continuity adjustment toward the null
        delta = delta + 0.5 * (delta < 0) - 0.5 * (delta > 0)
    z = delta / sd
    if alternative == "two-sided":
        rej = np.abs(z) >= stats.norm.ppf(1 - alpha / 2) - 1e-12
    elif alternative == "greater":
        rej = z >= stats.norm.ppf(1 - alpha) - 1e-12
    else:
        rej = z <= -stats.norm.ppf(1 - alpha) + 1e-12
    return rej


def power_test(n, null, p, alpha=0.05, test="exact", alternative="two-sided", method="exact"):
    r"""Power of a one-sample binomial test of :math:`H_0:\theta=\theta_0` (SAS ``ONESAMPLEFREQ``).

    Parameters
    ----------
    n : int
        Number of trials.
    null : float
        The null proportion :math:`\theta_0` (for non-inferiority/superiority pass the shifted
        value ``p0 - margin`` / ``p0 + margin``).
    p : float
        The true proportion.
    alpha : float
        Significance level.
    test : {"exact", "z", "adjz"}
        ``"exact"`` -- the exact binomial test with SAS's critical values (each tail filled with
        as much probability as fits within ``alpha`` or ``alpha/2``; equivalent to inverting
        Clopper-Pearson); ``"z"`` -- the normal-approximate z test with null variance;
        ``"adjz"`` -- the z test with continuity adjustment.
    alternative : {"two-sided", "greater", "less"}
    method : {"exact", "normal"}
        ``"exact"`` enumerates the binomial distribution (all tests); ``"normal"`` uses SAS's
        closed-form normal power approximation (``test="z"`` only).

    Returns
    -------
    float
    """
    _check_common(alpha)
    for nm, v in (("null", null), ("p", p)):
        if not 0 < v < 1 and nm == "null":
            raise ValueError("'null' has to be strictly between 0 and 1")
        if not 0 <= v <= 1:
            raise ValueError(f"'{nm}' has to be between 0 and 1")
    n = int(n)
    alt = _norm_alt(alternative)
    test = str(test).lower().strip()
    k = np.arange(n + 1)
    pmf = stats.binom.pmf(k, n, p)
    if method == "normal":
        if test != "z":
            raise ValueError("method='normal' is only defined for test='z'")
        s0 = math.sqrt(null * (1 - null))
        s1 = math.sqrt(p * (1 - p)) if 0 < p < 1 else 1e-12
        shift = math.sqrt(n) * (p - null) / s0
        ratio = s1 / s0
        if alt == "greater":
            return float(stats.norm.cdf((shift - stats.norm.ppf(1 - alpha)) / ratio))
        if alt == "less":
            return float(stats.norm.cdf((-shift - stats.norm.ppf(1 - alpha)) / ratio))
        zc = stats.norm.ppf(1 - alpha / 2)
        return float(stats.norm.cdf((shift - zc) / ratio) + stats.norm.cdf((-shift - zc) / ratio))
    if method != "exact":
        raise ValueError("'method' has to be 'exact' or 'normal'")
    if test == "exact":
        c_l, c_u = _exact_region(n, null, alpha, alt)
        if alt == "two-sided":
            rej = (k <= c_l) | (k >= c_u)
        elif alt == "greater":
            rej = k >= c_u
        else:
            rej = k <= c_l
    elif test in ("z", "adjz"):
        rej = _z_region(n, null, alpha, alt, adjusted=(test == "adjz"))
    else:
        raise ValueError("'test' has to be 'exact', 'z' or 'adjz'")
    return float(pmf[rej].sum())


def sample_size_test(
    power,
    null,
    p,
    alpha=0.05,
    test="exact",
    alternative="two-sided",
    method="exact",
    n_max=50_000,
    lookahead=0,
):
    r"""Smallest ``n`` whose test reaches the target ``power`` (SAS ``NTOTAL`` solve).

    Power of a discrete test saw-tooths in ``n``: this returns the *first* ``n`` that reaches the
    target, exactly as SAS does; ``lookahead=k`` additionally requires the target to hold for the
    next ``k`` sample sizes. ``method="normal"`` (``test="z"``, one-sided) uses SAS's closed form
    :math:`N=\{[z_{pow}\sqrt{p(1-p)}+z_{1-\alpha}\sqrt{p_0(1-p_0)}]/(p-p_0)\}^2`.
    """
    if not 0 < power < 1:
        raise ValueError("'power' has to be between 0 and 1")
    alt = _norm_alt(alternative)
    if method == "normal" and test == "z" and alt != "two-sided":
        z_pow = stats.norm.ppf(power)
        z_a = stats.norm.ppf(1 - alpha)
        s1, s0 = math.sqrt(p * (1 - p)), math.sqrt(null * (1 - null))
        return int(math.ceil(((z_pow * s1 + z_a * s0) / (p - null)) ** 2))
    if abs(p - null) < 1e-12:
        raise ValueError("'p' must differ from 'null' for power to exceed alpha")
    z_a = stats.norm.ppf(1 - alpha / 2 if alt == "two-sided" else 1 - alpha)
    z_pow = stats.norm.ppf(power)
    s1, s0 = math.sqrt(p * (1 - p)), math.sqrt(null * (1 - null))
    start = max(2, int(0.5 * ((z_pow * s1 + z_a * s0) / (p - null)) ** 2))
    for n in range(start, n_max + 1):
        if power_test(n, null, p, alpha, test, alt, method) >= power - 1e-12 and all(
            power_test(n + j, null, p, alpha, test, alt, method) >= power - 1e-12
            for j in range(1, lookahead + 1)
        ):
            return n
    raise ValueError(f"power {power} not reached by n_max={n_max}; raise n_max")


# ------------------------------------------------------------------------- equivalence
def power_equivalence(n, lower, upper, p, alpha=0.05, test="exact", method="exact"):
    r"""Power of the two one-sided tests (TOST) of equivalence :math:`\theta_L\le\theta\le\theta_U`.

    Rejects :math:`H_0:\theta\notin[\theta_L,\theta_U]` only when **both** one-sided tests
    (:math:`\theta\le\theta_L` and :math:`\theta\ge\theta_U`) reject at level ``alpha``.

    ``test="exact"`` (default) enumerates the binomial distribution with SAS's exact critical
    values; ``test="z"`` with ``method="normal"`` evaluates SAS's closed form
    :math:`\Phi(\cdot)+\Phi(\cdot)-1`.
    """
    _check_common(alpha, p)
    if not 0 < lower < upper < 1:
        raise ValueError("need 0 < lower < upper < 1")
    n = int(n)
    if test == "z" and method == "normal":
        za = stats.norm.ppf(alpha)  # SAS's z_alpha is the (negative) alpha-quantile
        su, sl = math.sqrt(upper * (1 - upper)), math.sqrt(lower * (1 - lower))
        s1 = math.sqrt(p * (1 - p))
        a = stats.norm.cdf((za - math.sqrt(n) * (p - upper) / su) / (s1 / su))
        c = stats.norm.cdf((za + math.sqrt(n) * (p - lower) / sl) / (s1 / sl))
        return float(max(a + c - 1, 0.0))
    k = np.arange(n + 1)
    pmf = stats.binom.pmf(k, n, p)
    if test == "exact":
        c_l, _ = _exact_region(n, upper, alpha, "less")  # reject theta >= upper: X <= c_l
        _, c_u = _exact_region(n, lower, alpha, "greater")  # reject theta <= lower: X >= c_u
        rej = (k >= c_u) & (k <= c_l)
    elif test in ("z", "adjz"):
        adj = test == "adjz"
        rej = _z_region(n, lower, alpha, "greater", adj) & _z_region(n, upper, alpha, "less", adj)
    else:
        raise ValueError("'test' has to be 'exact', 'z' or 'adjz'")
    return float(pmf[rej].sum())


def sample_size_equivalence(
    power, lower, upper, p, alpha=0.05, test="exact", method="exact", n_max=50_000, lookahead=0
):
    """Smallest ``n`` whose TOST equivalence test reaches the target ``power``.

    Starts from SAS's initial guess
    ``N0 = p(1-p) {[z_{1-a} + z_{(1+power)/2}] / [0.5 (U - L) - |p - 0.5 (L + U)|]}^2``
    (well below the answer) and increases ``n`` until the exact/z power is reached.
    """
    if not 0 < power < 1:
        raise ValueError("'power' has to be between 0 and 1")
    half = 0.5 * (upper - lower) - abs(p - 0.5 * (lower + upper))
    if half <= 0:
        raise ValueError("'p' must lie strictly inside the equivalence bounds")
    n0 = p * (1 - p) * ((stats.norm.ppf(1 - alpha) + stats.norm.ppf((1 + power) / 2)) / half) ** 2
    for n in range(max(2, int(0.4 * n0)), n_max + 1):
        if power_equivalence(n, lower, upper, p, alpha, test, method) >= power - 1e-12 and all(
            power_equivalence(n + j, lower, upper, p, alpha, test, method) >= power - 1e-12
            for j in range(1, lookahead + 1)
        ):
            return n
    raise ValueError(f"power {power} not reached by n_max={n_max}; raise n_max")


# ------------------------------------------------------ zero-failure / upper-bound plans
def sample_size_upper_bound(p_max, confidence=0.95, failures=0, method="exact", n_max=1_000_000):
    r"""Smallest ``n`` that demonstrates :math:`\theta \le p_{max}` with a given confidence.

    The "success-run" / reliability-demonstration / acceptance-sampling question: how many items must
    be tested so that observing at most ``failures`` defects proves, with ``confidence``, that the
    true defect rate is below ``p_max``? It is the smallest ``n`` whose **one-sided upper**
    ``confidence`` bound, at ``failures`` observed, is at most ``p_max``. For ``failures=0`` and
    ``method="exact"`` this is the classical :math:`n=\lceil\ln(1-C)/\ln(1-p_{max})\rceil`
    (the "rule of three" is its :math:`p_{max}\to0` limit, :math:`n\approx3/p_{max}` at 95%).

    Parameters
    ----------
    p_max : float
        The largest tolerable proportion (e.g. 0.01 for a 1% defect rate).
    confidence : float, default 0.95
        One-sided confidence level.
    failures : int, default 0
        The number of failures you plan to allow while still claiming success.
    method : {"exact", "wilson", "jeffreys"}
        Which one-sided bound: Clopper-Pearson (guaranteed), Wilson score, or Jeffreys.
    n_max : int
        Search ceiling.

    Returns
    -------
    int

    Examples
    --------
    >>> sample_size_upper_bound(0.01, 0.95)        # zero failures in 299 trials proves p < 1% at 95%
    299
    >>> sample_size_upper_bound(0.05, 0.90, failures=1)
    78
    """
    if not 0 < p_max < 1:
        raise ValueError("'p_max' has to be between 0 and 1")
    if not 0 < confidence < 1:
        raise ValueError("'confidence' has to be between 0 and 1")
    if failures < 0 or int(failures) != failures:
        raise ValueError("'failures' has to be a non-negative integer")
    f = int(failures)
    key = {
        "exact": "exact",
        "cp": "exact",
        "clopper-pearson": "exact",
        "wilson": "wilson",
        "score": "wilson",
        "jeffreys": "jeffreys",
    }.get(str(method).lower().strip())
    if key is None:
        raise ValueError("'method' has to be 'exact', 'wilson' or 'jeffreys'")
    a_two = 2 * (
        1 - confidence
    )  # a one-sided bound at `confidence` is the two-sided upper limit at 2(1-C)

    def upper(n):
        return float(_real_interval(key, n, a_two, np.array(float(f)))[1])

    if f == 0 and key == "exact":
        return int(math.ceil(math.log(1 - confidence) / math.log(1 - p_max) - 1e-12))
    n = _smallest_n(lambda m: m > f and upper(m) <= p_max, n_max)
    if n is None:
        raise ValueError(f"p_max={p_max} not demonstrable within n_max={n_max}")
    return n


# ------------------------------------------------------------- Bayesian sample size
def sample_size_bayes(
    length, criterion="alc", a=1.0, b=1.0, alpha=0.05, interval="hpd", n_max=20_000
):
    r"""Bayesian sample size for a credible interval of a target length (Joseph, Wolfson & du Berger 1995).

    With a Beta(``a``, ``b``) prior, the data ``x`` are beta-binomial *before* they are seen, and the
    posterior is Beta(``x + a``, ``n - x + b``). Two standard criteria:

    * ``"alc"`` -- the **average length criterion**: the smallest ``n`` whose *expected* interval length
      :math:`\sum_x P(x)\,\ell(x,n)` is at most ``length``;
    * ``"woc"`` -- the **worst outcome criterion**: the smallest ``n`` for which the length is at most
      ``length`` for *every* possible ``x`` (the most demanding; the worst case is near ``x = n/2``).

    Parameters
    ----------
    length : float
        Target credible-interval length.
    criterion : {"alc", "woc"}
    a, b : float
        Prior Beta shape.
    alpha : float
        The interval has credibility ``1 - alpha``.
    interval : {"hpd", "central"}
        Highest-posterior-density or equal-tailed credible interval.
    n_max : int

    Returns
    -------
    int
    """
    from .ci import _fast

    if not 0 < length < 1:
        raise ValueError("'length' has to be between 0 and 1")
    if a <= 0 or b <= 0:
        raise ValueError("'a' and 'b' have to be positive")
    crit = str(criterion).lower().strip()
    if crit not in ("alc", "woc"):
        raise ValueError("'criterion' has to be 'alc' or 'woc'")
    itype = str(interval).lower().strip()
    if itype not in ("hpd", "central"):
        raise ValueError("'interval' has to be 'hpd' or 'central'")
    from scipy.special import betaln, gammaln

    def measure(n):
        x = np.arange(n + 1)
        s1, s2 = x + a, n - x + b
        if itype == "central":
            ln = stats.beta.ppf(1 - alpha / 2, s1, s2) - stats.beta.ppf(alpha / 2, s1, s2)
        else:
            lo, hi = _fast.hpd_beta_vec(s1, s2, 1 - alpha)
            ln = hi - lo
        if crit == "woc":
            return float(ln.max())
        lw = (
            gammaln(n + 1)
            - gammaln(x + 1)
            - gammaln(n - x + 1)
            + betaln(x + a, n - x + b)
            - betaln(a, b)
        )
        return float((np.exp(lw) * ln).sum())

    n = _smallest_n(lambda m: measure(m) <= length + 1e-12, n_max)
    if n is None:
        raise ValueError(f"length {length} not reached by n_max={n_max}; raise n_max")
    return n
