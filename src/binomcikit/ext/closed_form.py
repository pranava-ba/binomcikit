"""Closed-form and transformation-based intervals missing from R ``proportion``.

Everything here is a function of ``(x, n)`` only, vectorised over every ``x`` at once
(no per-row Python loops, no root-finding except where noted), so a whole table
costs a handful of numpy calls. Each ``ci<name>(n, alp)`` returns the standard
``(n+1)``-row limits table; ``ci<name>x(x, n, alp)`` returns one row.

References
----------
* Pratt (1968), *A normal approximation for binomial, F, beta, and other common,
  related tail probabilities*, JASA 63.
* Brown, Cai & DasGupta (2001), *Interval estimation for a binomial proportion*,
  Statist. Sci. 16 (modified Wilson / modified Jeffreys).
* Cai (2005), *One-sided confidence intervals in discrete distributions*, J. Stat.
  Plan. Inference 131 (second-order corrected, SOC).
* Freeman & Tukey (1950), *Transformations related to the angular and the square
  root*, Ann. Math. Statist. 21; Miller (1978).
* Garwood (1936), *Fiducial limits for the Poisson distribution*, Biometrika 28.
* R package ``binom`` (Dorai-Raj) for the complementary log-log and probit forms.
"""

from __future__ import annotations

import numpy as np
import scipy.stats as stats

from ._common import bisect_monotone, check_x, single, table, validate


def _z(alp):
    return stats.norm.ppf(1 - alp / 2)


def _boundary_upper0(n, alp):
    """Exact upper limit at ``x = 0``: ``1 - (alpha/2)^(1/n)`` (Clopper-Pearson's)."""
    return 1 - (alp / 2) ** (1.0 / n)


# --------------------------------------------------------------------------- Pratt
def _pratt_upper(x, n, z, alp):
    """Pratt's normal-approximation upper limit for ``x = 1..n-1`` (vectorised).

    Falls back to the exact Clopper-Pearson upper limit wherever the closed form
    is numerically invalid (it needs ``d > 0`` and ``b + c > 0``, which fails for
    extreme ``alpha`` such as 0.001).
    """
    x = np.asarray(x, dtype=float)
    a = ((x + 1) / (n - x)) ** 2
    b = 81 * (x + 1) * (n - x) - 9 * n - 8
    inner = 9 * (x + 1) * (n - x) * (9 * n + 5 - z * z) + n + 1
    c = -3 * z * np.sqrt(np.maximum(inner, 0.0))
    d = 81 * (x + 1) ** 2 - 9 * (x + 1) * (2 + z * z) + 1
    with np.errstate(all="ignore"):
        base = (b + c) / d
        u = 1.0 / (1.0 + a * base**3)
    bad = (~np.isfinite(u)) | (d <= 0) | ((b + c) <= 0) | (inner < 0)
    if bad.any():
        cp = stats.beta.ppf(1 - alp / 2, x + 1, n - x)
        u = np.where(bad, cp, u)
    return u


def ciprat(n, alp):
    r"""Pratt's normal-approximation interval, for every ``x``.

    A **closed-form** approximation to the exact Clopper-Pearson limits
    (Pratt 1968): no root-finding and no beta quantiles, yet within about
    :math:`10^{-3}` of them. The upper limit uses Pratt's formula; the lower
    limit is its mirror image, :math:`L(x) = 1 - U(n - x)`, so the interval is
    exactly equivariant. ``x = 0`` and ``x = n`` use the exact one-sided closed
    forms.

    .. note::
       ``DescTools::BinomCI(method="pratt")`` (and ports of it) compute the
       lower limit from a different expression that drifts from exact
       Clopper-Pearson by up to 0.13 at ``n = 20`` for ``x`` near ``n``, and use
       full-:math:`\alpha` boundary rows. binomcikit uses the mirror construction;
       see ``tests/test_ext_closed_form.py`` for the measured comparison.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LPRA``, ``UPRA`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    z = _z(alp)
    k = np.arange(n)  # 0..n-1
    uf = np.empty(n)
    uf[0] = _boundary_upper0(n, alp)
    if n > 1:
        uf[1:] = _pratt_upper(k[1:], n, z, alp)
    upper = np.empty(n + 1)
    upper[:n] = uf
    upper[n] = 1.0
    lower = np.empty(n + 1)
    lower[0] = 0.0
    lower[1:] = 1.0 - uf[::-1]  # L(x) = 1 - U(n - x), x = 1..n
    return table("PRA", lower, upper)


def cipratx(x, n, alp):
    """Pratt interval for a single observed ``x`` (see :func:`ciprat`)."""
    n = validate(n, alp)
    return single(ciprat(n, alp), check_x(x, n), "PRA")


# ------------------------------------------------------- complementary log-log, probit
def _transformed(n, alp, kind):
    """Wald interval on the cloglog / probit scale (R ``binom`` conventions)."""
    z = _z(alp)
    x = np.arange(n + 1)
    p = x / n
    lower = np.zeros(n + 1)
    upper = np.ones(n + 1)
    inner = (x > 0) & (x < n)
    pi = p[inner]
    if kind == "cloglog":
        mu = np.log(pi)
        sd = np.sqrt((1 - pi) / n / pi / mu**2)
        g = np.log(-mu)
        lower[inner] = np.exp(-np.exp(g + z * sd))
        upper[inner] = np.exp(-np.exp(g - z * sd))
    else:  # probit
        q = stats.norm.ppf(pi)
        sd = np.sqrt(pi * (1 - pi) / n) / stats.norm.pdf(q)
        lower[inner] = stats.norm.cdf(q - z * sd)
        upper[inner] = stats.norm.cdf(q + z * sd)
    # Boundary rows: the exact one-sided closed forms (as in R `binom`).
    lower[0] = 0.0
    upper[0] = _boundary_upper0(n, alp)
    lower[n] = (alp / 2) ** (1.0 / n)
    upper[n] = 1.0
    return lower, upper


def cicloglog(n, alp):
    r"""Complementary log-log transformed-Wald interval, for every ``x``.

    A Wald interval on :math:`g(p) = \log(-\log p)` (delta-method variance
    :math:`(1-\hat p)/(n\hat p\log^2\hat p)`), back-transformed. It is a cousin of
    the Logit and ArcSine intervals, absent from R ``proportion`` (present in R
    ``binom``). Boundary rows use the exact one-sided limits, as in ``binom``.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LCLL``, ``UCLL`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    return table("CLL", *_transformed(n, alp, "cloglog"))


def cicloglogx(x, n, alp):
    """Complementary log-log interval for a single observed ``x``."""
    n = validate(n, alp)
    return single(cicloglog(n, alp), check_x(x, n), "CLL")


def ciprobit(n, alp):
    r"""Probit transformed-Wald interval, for every ``x``.

    A Wald interval on :math:`\Phi^{-1}(p)` (delta-method variance
    :math:`\hat p\hat q/(n\,\varphi(\Phi^{-1}(\hat p))^2)`), back-transformed with
    :math:`\Phi`. Absent from R ``proportion``; present in R ``binom``.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LPRB``, ``UPRB`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    return table("PRB", *_transformed(n, alp, "probit"))


def ciprobitx(x, n, alp):
    """Probit interval for a single observed ``x``."""
    n = validate(n, alp)
    return single(ciprobit(n, alp), check_x(x, n), "PRB")


# ------------------------------------------------- Brown-Cai-DasGupta modifications
def cimodwilson(n, alp):
    r"""Modified Wilson interval (Brown, Cai & DasGupta 2001), for every ``x``.

    Wilson's interval, except when ``x`` is within 1-2 (``n <= 50``) or 1-3
    (``n > 50``) of a boundary, where the limit next to the boundary is replaced
    by the Poisson-based value :math:`\tfrac{1}{2n}\chi^2_{2x,\alpha}` (and its
    mirror), which repairs Wilson's under-coverage there. Follows
    ``DescTools::BinomCI(method="modified wilson")`` exactly (including its use of
    the full :math:`\alpha` in the chi-square quantile).

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LMWS``, ``UMWS`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    z = _z(alp)
    x = np.arange(n + 1)
    p = x / n
    t1 = (x + z * z / 2) / (n + z * z)
    t2 = z * np.sqrt(n) / (n + z * z) * np.sqrt(p * (1 - p) + z * z / (4 * n))
    lower = t1 - t2
    upper = t1 + t2
    near = (lambda k: (k >= 1) & (k <= 2)) if n <= 50 else (lambda k: (k >= 1) & (k <= 3))
    lo_sel = near(x)
    hi_sel = near(n - x)
    with np.errstate(all="ignore"):
        lower = np.where(lo_sel, 0.5 * stats.chi2.ppf(alp, 2 * x) / n, lower)
        upper = np.where(hi_sel, 1 - 0.5 * stats.chi2.ppf(alp, 2 * (n - x)) / n, upper)
    return table("MWS", lower, upper)


def cimodwilsonx(x, n, alp):
    """Modified Wilson interval for a single observed ``x``."""
    n = validate(n, alp)
    return single(cimodwilson(n, alp), check_x(x, n), "MWS")


def cimodjeffreys(n, alp):
    r"""Modified Jeffreys interval (Brown, Cai & DasGupta 2001), for every ``x``.

    The equal-tailed Jeffreys credible interval, with the boundary rows fixed to
    the frequentist-friendly values: lower limit 0 for ``x <= 1``, upper limit 1
    for ``x >= n - 1``, and the exact closed forms
    :math:`1-(\alpha/2)^{1/n}` / :math:`(\alpha/2)^{1/n}` at ``x = 0`` / ``x = n``.
    Matches ``DescTools::BinomCI(method="modified jeffreys")``.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LMJF``, ``UMJF`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    x = np.arange(n + 1)
    lower = stats.beta.ppf(alp / 2, x + 0.5, n - x + 0.5)
    upper = stats.beta.ppf(1 - alp / 2, x + 0.5, n - x + 0.5)
    lower = np.where(x <= 1, 0.0, lower)
    upper = np.where(x >= n - 1, 1.0, upper)
    lower[n] = (alp / 2) ** (1.0 / n)
    upper[0] = _boundary_upper0(n, alp)
    return table("MJF", lower, upper)


def cimodjeffreysx(x, n, alp):
    """Modified Jeffreys interval for a single observed ``x``."""
    n = validate(n, alp)
    return single(cimodjeffreys(n, alp), check_x(x, n), "MJF")


# ------------------------------------------------------------- Poisson / Garwood
def cipoisson(n, alp):
    r"""Garwood (Poisson-approximation) interval, for every ``x``.

    Treats ``x`` as a Poisson count with mean :math:`n\theta` -- the right model
    for **rare events** (small :math:`\theta`, large ``n``):
    :math:`L = \chi^2_{2x}(\alpha/2)/(2n)`,
    :math:`U = \chi^2_{2x+2}(1-\alpha/2)/(2n)`, with :math:`U` capped at 1.
    Always at least as wide as the exact binomial limits at the upper end, so it
    is conservative for the upper limit.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LPOI``, ``UPOI`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    x = np.arange(n + 1)
    with np.errstate(all="ignore"):
        lower = np.where(x == 0, 0.0, 0.5 * stats.chi2.ppf(alp / 2, 2 * x) / n)
    upper = 0.5 * stats.chi2.ppf(1 - alp / 2, 2 * x + 2) / n
    return table("POI", lower, upper)


def cipoissonx(x, n, alp):
    """Garwood Poisson interval for a single observed ``x``."""
    n = validate(n, alp)
    return single(cipoisson(n, alp), check_x(x, n), "POI")


# ----------------------------------------------------------------- Freeman-Tukey
def _ft(x, n):
    """Freeman-Tukey double-arcsine transform of a (real) count ``x``."""
    return np.arcsin(np.sqrt(x / (n + 1.0))) + np.arcsin(np.sqrt((x + 1.0) / (n + 1.0)))


def cifreemantukey(n, alp):
    r"""Freeman-Tukey double-arcsine interval, for every ``x``.

    Variance-stabilises with
    :math:`T(x)=\arcsin\sqrt{x/(n+1)}+\arcsin\sqrt{(x+1)/(n+1)}`, whose variance
    is :math:`\approx 1/(n+\tfrac12)`. The interval is
    :math:`T(x)\pm z/\sqrt{n+1/2}` mapped back through :math:`T^{-1}` (inverted
    numerically on the count scale, then divided by ``n``) -- the standard
    transform for proportions near 0 or 1 in meta-analysis. It stays inside
    :math:`[0,1]` and never collapses to zero width.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LFTK``, ``UFTK`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    z = _z(alp)
    x = np.arange(n + 1)
    t0 = _ft(x.astype(float), n)
    half = z / np.sqrt(n + 0.5)
    tlo, thi = _ft(0.0, n), _ft(float(n), n)

    def solve(target):
        out = np.zeros(n + 1)
        hit = (target > tlo) & (target < thi)
        if hit.any():
            tg = target[hit]
            root = bisect_monotone(
                lambda m: _ft(m, n) - tg,
                np.zeros(tg.shape),
                np.full(tg.shape, float(n)),
                increasing=True,
            )
            out[hit] = root
        out = np.where(target >= thi, float(n), out)
        return out

    lower = solve(t0 - half) / n
    upper = solve(t0 + half) / n
    return table("FTK", lower, upper)


def cifreemantukeyx(x, n, alp):
    """Freeman-Tukey interval for a single observed ``x``."""
    n = validate(n, alp)
    return single(cifreemantukey(n, alp), check_x(x, n), "FTK")


# ------------------------------------------------------------ SOC (Cai 2005)
def cisoc(n, alp):
    r"""Second-order corrected (SOC) interval, Cai (2005), for every ``x``.

    An Edgeworth-corrected score-type interval built so the *one-sided* coverage
    is as symmetric as possible; ``binGroup`` recommends it when mean coverage
    close to nominal is wanted. With :math:`\kappa = z_{1-\alpha/2}`,
    :math:`\eta=\kappa^2/3+1/6`, :math:`\gamma_1=-(13\kappa^2/18+17/18)`,
    :math:`\gamma_2=\kappa^2/18+7/36` and :math:`m=(x+\eta)/(n+2\eta)`:

    .. math:: m \pm \kappa\sqrt{\hat p\hat q+(\gamma_1\hat p\hat q+\gamma_2)/n}\,/\sqrt n,

    widened if necessary so the interval always contains :math:`\hat p`.
    Ported from ``binGroup::binSOC``.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LSOC``, ``USOC`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    kappa = _z(alp)
    eta = kappa**2 / 3 + 1 / 6
    g1 = -((13 / 18) * kappa**2 + 17 / 18)
    g2 = kappa**2 / 18 + 7 / 36
    x = np.arange(n + 1)
    p = x / n
    mid = (x + eta) / (n + 2 * eta)
    arg = np.maximum(p * (1 - p) + (g1 * p * (1 - p) + g2) / n, 0.0)
    half = kappa * np.sqrt(arg) / np.sqrt(n)
    lower = np.minimum(mid - half, p)
    upper = np.maximum(mid + half, p)
    return table("SOC", lower, upper)


def cisocx(x, n, alp):
    """Second-order corrected (SOC) interval for a single observed ``x``."""
    n = validate(n, alp)
    return single(cisoc(n, alp), check_x(x, n), "SOC")
