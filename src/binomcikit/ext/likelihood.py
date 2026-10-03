"""Likelihood-family intervals: the Cressie-Read continuum and higher-order ``r*``.

References
----------
* Cressie & Read (1984), *Multinomial goodness-of-fit tests*, JRSS-B 46: the
  power-divergence family that contains Pearson (score, ``lam=1``), likelihood-ratio
  (``lam=0``), Freeman-Tukey (``lam=-1/2``) and the recommended compromise
  ``lam=2/3``.
* Barndorff-Nielsen (1986), *Inference on full or partial parameters based on the
  standardized signed log likelihood ratio*, Biometrika 73: the modified signed root
  ``r* = r + r^-1 log(q/r)``; see Brazzale, Davison & Reid (2007), *Applied Asymptotics*.
"""

from __future__ import annotations

import numpy as np
import scipy.stats as stats

from ._common import bisect_monotone, check_x, single, table, validate


def _cr_stat(x, n, theta, lam):
    """Cressie-Read power-divergence statistic for counts ``(x, n-x)`` vs ``theta``.

    ``2/(lam(lam+1)) * sum O ((O/E)^lam - 1)``; the ``lam -> 0`` limit is the
    likelihood-ratio statistic. Cells with ``O = 0`` contribute nothing (valid
    for ``lam > -1``).
    """
    theta = np.clip(theta, 1e-300, 1 - 1e-16)
    e1 = n * theta
    e2 = n * (1 - theta)
    o1 = np.asarray(x, dtype=float)
    o2 = n - o1
    with np.errstate(all="ignore"):
        if abs(lam) < 1e-12:
            t = 2 * (
                np.where(o1 > 0, o1 * np.log(o1 / e1), 0.0)
                + np.where(o2 > 0, o2 * np.log(o2 / e2), 0.0)
            )
        else:
            c = 2.0 / (lam * (lam + 1.0))
            t1 = np.where(o1 > 0, o1 * ((o1 / e1) ** lam - 1.0), 0.0)
            t2 = np.where(o2 > 0, o2 * ((o2 / e2) ** lam - 1.0), 0.0)
            t = c * (t1 + t2)
    return np.where(np.isnan(t), np.inf, t)


def cicressieread(n, alp, lam=2.0 / 3.0):
    r"""Cressie-Read power-divergence interval, for every ``x``.

    Inverts the Cressie-Read statistic
    :math:`2/(\lambda(\lambda+1))\sum_i O_i[(O_i/E_i)^\lambda-1]` -- a one-parameter
    family that **contains** the score (Wilson, ``lam=1``), likelihood-ratio
    (``lam=0``) and Freeman-Tukey (``lam=-1/2``) intervals as special cases, with
    ``lam=2/3`` the value Cressie & Read recommend. The limits are the two roots of
    ``stat(theta) = z^2`` on either side of :math:`\hat p`, found by vectorised
    bisection.

    Parameters
    ----------
    n : int
        Number of trials.
    alp : float
        Significance level.
    lam : float, default 2/3
        Power-divergence index, ``lam > -1``.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LCRD``, ``UCRD`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    if not lam > -1:
        raise ValueError("'lam' has to be greater than -1")
    z2 = stats.norm.ppf(1 - alp / 2) ** 2
    x = np.arange(n + 1)
    p = x / n
    lower = np.zeros(n + 1)
    upper = np.ones(n + 1)

    # lower limit: statistic decreases as theta rises from 0 to p-hat
    rows = x > 0
    if rows.any():
        xx, pp = x[rows].astype(float), p[rows]
        lo = np.full(pp.shape, 1e-300)
        reach = _cr_stat(xx, n, lo, lam) > z2  # does the statistic reach z^2 near 0?
        root = bisect_monotone(lambda t: _cr_stat(xx, n, t, lam) - z2, lo, pp, increasing=False)
        lower[rows] = np.where(reach, root, 0.0)

    # upper limit: statistic increases as theta rises from p-hat to 1
    rows = x < n
    if rows.any():
        xx, pp = x[rows].astype(float), p[rows]
        hi = np.full(pp.shape, 1 - 1e-16)
        reach = _cr_stat(xx, n, hi, lam) > z2
        root = bisect_monotone(lambda t: _cr_stat(xx, n, t, lam) - z2, pp, hi, increasing=True)
        upper[rows] = np.where(reach, root, 1.0)
    return table("CRD", lower, upper)


def cicressiereadx(x, n, alp, lam=2.0 / 3.0):
    """Cressie-Read interval for a single observed ``x``."""
    n = validate(n, alp)
    return single(cicressieread(n, alp, lam), check_x(x, n), "CRD")


def _rstar(p, n, theta):
    """Modified signed root ``r*`` of the binomial likelihood at ``theta``."""
    with np.errstate(all="ignore"):
        dev = p * np.log(p / theta) + (1 - p) * np.log((1 - p) / (1 - theta))
        r = np.sign(p - theta) * np.sqrt(2 * n * np.maximum(dev, 0.0))
        q = (np.log(p / (1 - p)) - np.log(theta / (1 - theta))) * np.sqrt(n * p * (1 - p))
        out = r + np.log(q / r) / r
    return np.where(np.isfinite(out), out, 0.0)


def cilrstar(n, alp):
    r"""Higher-order likelihood interval (Barndorff-Nielsen :math:`r^*`), for every ``x``.

    Replaces the signed likelihood-ratio root :math:`r` by
    :math:`r^*=r+r^{-1}\log(q/r)`, with :math:`q` the Wald statistic on the logit
    scale. :math:`r^*` is standard normal to **third** order (the plain LR root
    only to first), so this interval is very close to exact coverage with no
    discreteness correction. The limits solve :math:`r^*(\theta)=\pm z`. Rows
    ``x = 0`` and ``x = n`` (where :math:`r^*` is undefined) use the exact one-sided
    closed forms.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LLRS``, ``ULRS`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    z = stats.norm.ppf(1 - alp / 2)
    x = np.arange(n + 1)
    p = x / n
    inner = (x > 0) & (x < n)
    pp = p[inner]
    eps = 1e-12
    lower = np.zeros(n + 1)
    upper = np.ones(n + 1)
    lower[inner] = bisect_monotone(
        lambda t: _rstar(pp, n, t) - z, np.full(pp.shape, 1e-300), pp * (1 - eps), increasing=False
    )
    upper[inner] = bisect_monotone(
        lambda t: _rstar(pp, n, t) + z,
        pp * (1 + eps),
        np.full(pp.shape, 1 - 1e-16),
        increasing=False,
    )
    lower[0], upper[0] = 0.0, 1 - (alp / 2) ** (1.0 / n)
    lower[n], upper[n] = (alp / 2) ** (1.0 / n), 1.0
    return table("LRS", lower, upper)


def cilrstarx(x, n, alp):
    """Higher-order likelihood (:math:`r^*`) interval for a single observed ``x``."""
    n = validate(n, alp)
    return single(cilrstar(n, alp), check_x(x, n), "LRS")
