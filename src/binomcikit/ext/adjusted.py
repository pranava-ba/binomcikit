"""Coverage-adjusted Clopper-Pearson intervals (Thulin 2014) and the noise-based Wilson variants.

**Coverage-adjusted Clopper-Pearson** (Thulin, *Scand. J. Statist.* 41, 291-300; arXiv:1204.5894).
Clopper-Pearson is exact but conservative for most ``theta``. Thulin keeps the Clopper-Pearson
*form* but evaluates it at an adjusted level ``alpha' >= alpha`` chosen so that the **mean**
coverage under a Beta(r, s) weight equals ``1 - alpha``:

    C(alpha') = int_0^1 P_p( p in CP(X, alpha') ) f(p) dp = 1 - alpha.

For a Beta(r, s) weight the integral is closed form -- the beta-binomial pmf times differences of
regularised incomplete betas -- and ``C`` is strictly decreasing in ``alpha'`` (Thulin's Lemma 1), so
``alpha'`` is a single scalar root. With ``kind="posterior"`` the weight is the posterior
Beta(x + r, n - x + s), so ``alpha'`` is found separately for every observed ``x``. The result is
equivariant and nested in Clopper-Pearson, with minimum coverage at least ``1 - alpha'``.

**Noise-based Wilson intervals** (Decrouez & Hall 2014; Thulin 2014, arXiv:1402.6536). Smoothing the
discrete count with a little random noise improves the normal approximation and damps the coverage
oscillations: the *split-sample* Wilson interval (a hypergeometric noise) and the
*U(-1/2, 1/2)* Wilson interval (uniform noise, which Thulin shows is better). Both are randomised.
"""

from __future__ import annotations

import numpy as np
import scipy.stats as stats
from scipy import optimize
from scipy.special import betainc, betaincinv, betaln, gammaln

from ._common import check_x, single, table, validate

# ------------------------------------------------------------------ coverage-adjusted CP


def _cp_limits(n, x, a):
    """Clopper-Pearson limits at level ``1 - a`` for counts ``x`` (arrays)."""
    x = np.asarray(x)
    lo = np.where(x > 0, betaincinv(np.maximum(x, 1), n - x + 1, a / 2), 0.0)
    hi = np.where(x < n, betaincinv(x + 1, np.maximum(n - x, 1), 1 - a / 2), 1.0)
    return lo, hi


def mean_coverage(n, alpha_adj, r=1.0, s=None):
    """Mean coverage of the ``1 - alpha_adj`` Clopper-Pearson interval under a Beta(r, s) weight.

    ``C = sum_x BB(x; n, r, s) * [ I_U(x + r, n - x + s) - I_L(x + r, n - x + s) ]`` where ``BB`` is
    the beta-binomial pmf and ``I`` the regularised incomplete beta (Thulin 2014, eq. 3).
    """
    s = r if s is None else s
    x = np.arange(n + 1)
    lo, hi = _cp_limits(n, x, alpha_adj)
    lw = (
        gammaln(n + 1)
        - gammaln(x + 1)
        - gammaln(n - x + 1)
        + betaln(x + r, n - x + s)
        - betaln(r, s)
    )
    a, b = x + r, n - x + s
    return float((np.exp(lw) * (betainc(a, b, hi) - betainc(a, b, lo))).sum())


def adjusted_alpha(n, alpha, r=1.0, s=None):
    """The adjusted level ``alpha'`` with mean coverage ``1 - alpha`` under Beta(r, s) (a scalar root)."""
    s = r if s is None else s
    if not 0 < alpha < 1:
        raise ValueError("'alpha' has to be strictly between 0 and 1")
    f = lambda a: mean_coverage(n, a, r, s) - (1 - alpha)  # noqa: E731  (decreasing in a)
    lo, hi = alpha, min(0.9999, max(4 * alpha, 0.5))
    if f(lo) < 0:  # already below nominal on average (cannot happen for a CP interval)
        return alpha
    while f(hi) > 0 and hi < 0.9999:
        hi = min(0.9999, hi + 0.25)
    return float(optimize.brentq(f, lo, hi, xtol=1e-14, rtol=1e-13))


def cigcp(n, alp, r=1.0, s=None, kind="prior"):
    r"""Thulin's coverage-adjusted Clopper-Pearson interval, for every ``x``.

    The ``(1 - alpha')`` Clopper-Pearson interval with :math:`\alpha'\ge\alpha` solving
    :math:`C(\alpha')=1-\alpha`, where :math:`C` is the mean coverage under a Beta(``r``, ``s``)
    weight on :math:`\theta` (``kind="prior"``, one :math:`\alpha'` for every ``x``) or under the
    posterior Beta(``x + r``, ``n - x + s``) (``kind="posterior"``, :math:`\alpha'` found per ``x``).
    Thulin's guidance: ``r = 1/2`` when :math:`\theta` may be near 0 or 1, ``r = 1`` (the default,
    which coincides with Reiczigel's informal correction) for mid-range, ``r = 2`` near 1/2.

    Parameters
    ----------
    n : int
        Number of trials.
    alp : float
        Nominal significance level (the mean-coverage target is ``1 - alp``).
    r, s : float
        Beta weight shape (``s`` defaults to ``r``).
    kind : {"prior", "posterior"}

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LGCP``, ``UGCP`` and the flags ``LABB``, ``UABB``, ``ZWI``. The table carries the
        adjusted level(s) in the ``alpha_adj`` column.
    """
    n = validate(n, alp)
    if r <= 0 or (s is not None and s <= 0):
        raise ValueError("'r' and 's' have to be positive")
    if not 0 < alp < 1:
        raise ValueError("'alpha' has to be strictly between 0 and 1")
    kind = str(kind).lower().strip()
    x = np.arange(n + 1)
    sh = r if s is None else s
    if kind == "prior":
        a_adj = np.full(n + 1, adjusted_alpha(n, alp, r, sh))
    elif kind == "posterior":
        a_adj = np.array([adjusted_alpha(n, alp, x0 + r, n - x0 + sh) for x0 in x])
    else:
        raise ValueError("'kind' has to be 'prior' or 'posterior'")
    lower = np.zeros(n + 1)
    upper = np.ones(n + 1)
    for i in range(n + 1):
        lo, hi = _cp_limits(n, x[i : i + 1], a_adj[i])
        lower[i], upper[i] = lo[0], hi[0]
    df = table("GCP", lower, upper)
    df["alpha_adj"] = a_adj
    return df


def cigcpx(x, n, alp, r=1.0, s=None, kind="prior"):
    """Coverage-adjusted Clopper-Pearson interval for a single observed ``x``."""
    n = validate(n, alp)
    x = check_x(x, n)
    sh = r if s is None else s
    if kind == "prior":
        a = adjusted_alpha(n, alp, r, sh)
    elif kind == "posterior":
        a = adjusted_alpha(n, alp, x + r, n - x + sh)
    else:
        raise ValueError("'kind' has to be 'prior' or 'posterior'")
    lo, hi = _cp_limits(n, np.array([x]), a)
    df = table("GCP", lo, hi)
    df["x"] = x
    df["alpha_adj"] = a
    return df.rename(columns={"LGCP": "LGCPx", "UGCP": "UGCPx"})


# ------------------------------------------------------------------- noise-based Wilson


def _wilson_from(p, n, alp):
    z = stats.norm.ppf(1 - alp / 2)
    mid = (p * n + z * z / 2) / (n + z * z)
    h = z / (n + z * z) * np.sqrt(np.maximum(p * (1 - p) * n + z * z / 4, 0.0))
    return mid - h, mid + h


def ciunifwilson(n, alp, u=None, seed=None):
    r"""Wilson interval on the noise-smoothed count :math:`X+U`, :math:`U\sim U(-\tfrac12,\tfrac12)`.

    Thulin (2014) shows adding *continuous* uniform noise to ``x`` before applying the Wilson formula
    reduces the coverage oscillations about as much again as Decrouez & Hall's split sample does,
    without lengthening the interval. The noisy count is clipped to ``[0, n]``.

    Parameters
    ----------
    n, alp : see :func:`binomcikit.cisc`.
    u : float or None
        ``None`` draws an independent ``U`` per ``x`` (seeded by ``seed``); a number in
        ``[-1/2, 1/2]`` fixes it (``0`` reproduces plain Wilson).
    seed : int, optional

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LUNW``, ``UUNW`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    if u is None:
        noise = np.random.default_rng(seed).uniform(-0.5, 0.5, n + 1)
    else:
        if not -0.5 <= float(u) <= 0.5:
            raise ValueError("'u' has to be between -1/2 and 1/2")
        noise = np.full(n + 1, float(u))
    xt = np.clip(np.arange(n + 1) + noise, 0.0, n)
    return table("UNW", *_wilson_from(xt / n, n, alp))


def ciunifwilsonx(x, n, alp, u=None, seed=None):
    """Uniform-noise Wilson interval for a single observed ``x``."""
    n = validate(n, alp)
    return single(ciunifwilson(n, alp, u=u, seed=seed), check_x(x, n), "UNW")


def cisplitwilson(n, alp, seed=None):
    r"""Split-sample Wilson interval (Decrouez & Hall 2014), for every ``x``.

    Splits the (unrecorded) sequence into parts of size :math:`n_1=\mathrm{round}(n/2+0.15n^{3/4})`
    and :math:`n_2=n-n_1`; given ``x``, the successes in the first part are hypergeometric, and the
    Wilson formula is applied to the weighted estimator
    :math:`\tilde p=\tfrac12(Z/n_1+(x-Z)/n_2)` instead of :math:`x/n`. Randomised (``seed`` pins it).

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LSPW``, ``USPW`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    n1 = int(round(n / 2 + 0.15 * n**0.75))
    n1 = min(max(n1, 1), n - 1) if n > 1 else 1
    n2 = n - n1
    rng = np.random.default_rng(seed)
    x = np.arange(n + 1)
    if n > 1:
        z = rng.hypergeometric(x, n - x, n1)
        pt = 0.5 * (z / n1 + (x - z) / max(n2, 1))
    else:
        pt = x / n
    return table("SPW", *_wilson_from(np.clip(pt, 0.0, 1.0), n, alp))


def cisplitwilsonx(x, n, alp, seed=None):
    """Split-sample Wilson interval for a single observed ``x``."""
    n = validate(n, alp)
    return single(cisplitwilson(n, alp, seed=seed), check_x(x, n), "SPW")
