"""Concentration-inequality intervals: guaranteed coverage with no asymptotics.

These intervals invert a *non-asymptotic* tail bound, so their coverage is at least
``1 - alpha`` at **every** ``n`` and ``theta`` (they are conservative, typically wider
than Clopper-Pearson). They matter for machine-learning and safety-critical work where
"approximately 95%" is not good enough, and they are the building blocks that the
variance-adaptive betting intervals improve on.

References
----------
* Hoeffding (1963), *Probability inequalities for sums of bounded random variables*,
  JASA 58.
* Chernoff (1952); the Kullback-Leibler form is the bound inverted by the "kl-UCB"
  index of Garivier & Cappe (2011).
* Bernstein (1924); see Boucheron, Lugosi & Massart (2013), *Concentration
  Inequalities*, Thm 2.10.
* Maurer & Pontil (2009), *Empirical Bernstein bounds and sample variance
  penalization*, COLT, Thm 4.
"""

from __future__ import annotations

import numpy as np
from scipy.special import xlogy

from ._common import bisect_monotone, check_x, single, table, validate


def _L(alp):
    """``ln(2/alpha)``: the two-sided union-bound level shared by the Chernoff family."""
    if alp <= 0:
        raise ValueError("'alpha' has to be greater than 0 for this method")
    return np.log(2.0 / alp)


def cihoeffding(n, alp):
    r"""Hoeffding interval, for every ``x``.

    :math:`\hat p \pm \sqrt{\ln(2/\alpha)/(2n)}` (clamped to :math:`[0,1]`). The
    simplest distribution-free interval: coverage :math:`\ge 1-\alpha` always, but
    its width ignores the variance, so it is very wide when :math:`\theta` is near 0
    or 1.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LHOE``, ``UHOE`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    p = np.arange(n + 1) / n
    h = np.sqrt(_L(alp) / (2 * n))
    return table("HOE", p - h, p + h)


def cihoeffdingx(x, n, alp):
    """Hoeffding interval for a single observed ``x``."""
    n = validate(n, alp)
    return single(cihoeffding(n, alp), check_x(x, n), "HOE")


def _kl(p, q):
    """Bernoulli KL divergence ``KL(p || q)`` (vectorised, safe at the edges)."""
    q = np.clip(q, 1e-300, 1 - 1e-16)
    return xlogy(p, p / q) + xlogy(1 - p, (1 - p) / (1 - q))


def cikl(n, alp):
    r"""Chernoff / Kullback-Leibler interval, for every ``x``.

    The set :math:`\{\theta : n\,\mathrm{KL}(\hat p\,\|\,\theta)\le\ln(2/\alpha)\}`,
    the exact inversion of the Chernoff bound. It is never wider than Hoeffding's,
    adapts to :math:`\theta` near 0 or 1, and keeps the guaranteed coverage; the
    limits are found by vectorised bisection (``kl-UCB`` in the bandit literature).

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LKLC``, ``UKLC`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    c = _L(alp) / n
    p = np.arange(n + 1) / n
    lower = np.zeros(n + 1)
    upper = np.ones(n + 1)
    lo_rows = p > 0
    hi_rows = p < 1
    if lo_rows.any():
        pp = p[lo_rows]
        lower[lo_rows] = bisect_monotone(
            lambda t: _kl(pp, t) - c, np.zeros(pp.shape), pp, increasing=False
        )
    if hi_rows.any():
        pp = p[hi_rows]
        upper[hi_rows] = bisect_monotone(
            lambda t: _kl(pp, t) - c, pp, np.ones(pp.shape), increasing=True
        )
    return table("KLC", lower, upper)


def ciklx(x, n, alp):
    """Chernoff/KL interval for a single observed ``x``."""
    n = validate(n, alp)
    return single(cikl(n, alp), check_x(x, n), "KLC")


def cibernstein(n, alp):
    r"""Bernstein interval (variance-aware, closed form), for every ``x``.

    Inverts Bernstein's inequality with the Bernoulli variance
    :math:`\theta(1-\theta)`: the set
    :math:`\{\theta : n(\hat p-\theta)^2 \le L\,(2\theta(1-\theta) +
    \tfrac23|\hat p-\theta|)\}` with :math:`L=\ln(2/\alpha)`. That set is cut out by
    a convex quadratic in :math:`\theta`, so the limits are its two roots -- no
    iteration. Narrower than Hoeffding's near 0 or 1, coverage guaranteed.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LBRN``, ``UBRN`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    L = _L(alp)
    p = np.arange(n + 1) / n
    a = n + 2 * L
    # upper (theta >= p): a t^2 - (2 n p + 2L + 2L/3) t + n p^2 + (2L/3) p = 0
    b_u = -(2 * n * p + 2 * L + 2 * L / 3)
    c_u = n * p**2 + (2 * L / 3) * p
    upper = (-b_u + np.sqrt(np.maximum(b_u**2 - 4 * a * c_u, 0.0))) / (2 * a)
    # lower (theta <= p): a t^2 - (2 n p + 2L - 2L/3) t + n p^2 - (2L/3) p = 0
    b_l = -(2 * n * p + 2 * L - 2 * L / 3)
    c_l = n * p**2 - (2 * L / 3) * p
    lower = (-b_l - np.sqrt(np.maximum(b_l**2 - 4 * a * c_l, 0.0))) / (2 * a)
    return table("BRN", lower, upper)


def cibernsteinx(x, n, alp):
    """Bernstein interval for a single observed ``x``."""
    n = validate(n, alp)
    return single(cibernstein(n, alp), check_x(x, n), "BRN")


def ciempbern(n, alp):
    r"""Empirical-Bernstein interval (Maurer & Pontil 2009), for every ``x``.

    :math:`\hat p \pm \Bigl(\sqrt{2V_n\ln(4/\alpha)/n} + \tfrac{7\ln(4/\alpha)}{3(n-1)}\Bigr)`
    with the *sample* variance :math:`V_n = n\hat p(1-\hat p)/(n-1)`. It needs no
    knowledge of :math:`\theta`, adapts to low variance, and has guaranteed
    coverage. Requires ``n >= 2``.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LEBN``, ``UEBN`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    if n < 2:
        raise ValueError("the empirical-Bernstein interval needs n >= 2")
    L = np.log(4.0 / alp) if alp > 0 else np.inf
    p = np.arange(n + 1) / n
    v = n * p * (1 - p) / (n - 1)
    h = np.sqrt(2 * v * L / n) + 7 * L / (3 * (n - 1))
    return table("EBN", p - h, p + h)


def ciempbernx(x, n, alp):
    """Empirical-Bernstein interval for a single observed ``x``."""
    n = validate(n, alp)
    return single(ciempbern(n, alp), check_x(x, n), "EBN")
