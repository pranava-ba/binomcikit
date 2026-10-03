"""The methods of Pires & Amado (2008) that R ``proportion`` and the first port did not have.

Pires & Amado, *Interval estimators for a binomial proportion: comparison of twenty methods*,
REVSTAT 6(2), 165-197, define twenty central intervals (Tables 1 and 2). binomcikit already had
Clopper-Pearson, the uniform-prior Bayes interval, Score and Score-cc (Wilson), Wald and Wald-cc,
the arcsine interval and its continuity-corrected form, Add-4 (Agresti-Coull with ``h = 2``) and the
Wald-t / Add-4-t intervals. The ones added here complete the set:

=========  ==========================================================  ====================
Method     Interval                                                    Function
=========  ==========================================================  ====================
VII/VIII   Wald with the exact Clopper-Pearson rows at x = 0 and x = n  ``ciwaldi`` / ``ciwaldicc``
IX/X       the same, *recentred* at the Wilson centre                   ``ciwaldrec`` / ``ciwaldreccc``
XI/XII     analytic percentile bootstrap (no Monte Carlo) and its cc    ``cibootp`` / ``cibootpcc``
XIII/XIV   analytic bias-corrected percentile bootstrap and its cc      ``cibcp`` / ``cibcpcc``
XVII       arcsine with continuity and Anscombe's correction            ``ciarcsineans``
=========  ==========================================================  ====================

Every formula is transcribed from the paper's Tables 1-2 (reproduced as independent scalar code in
``tests/test_ext_pires_thulin.py``). Their headline finding -- reproduced by the tests -- is that
the arcsine-cc-Anscombe interval and Score-cc are *strictly conservative* (coverage never below
``1 - alpha - 0.005`` for n >= 10) while Add-4 is correct on average.
"""

from __future__ import annotations

import numpy as np
import scipy.stats as stats

from ._common import check_x, single, table, validate


def _cp_rows(n, alp, lower, upper):
    """Clopper-Pearson closed-form boundary rows (the paper's convention for all of VII-XIV)."""
    lower[0] = 0.0
    upper[0] = 1 - (alp / 2) ** (1 / n)
    lower[n] = (alp / 2) ** (1 / n)
    upper[n] = 1.0
    return lower, upper


def _z(alp):
    return stats.norm.ppf(1 - alp / 2)


def ciscorecc(n, alp):
    r"""Score interval with continuity correction (Newcombe 1998 method 4; Pires & Amado method IV).

    .. math::
        \frac{2x+c^2-1-c\sqrt{c^2-(2+1/n)+4x(1-x/n+1/n)}}{2(n+c^2)},\qquad
        \frac{2x+c^2+1+c\sqrt{c^2+(2-1/n)+4x(1-x/n-1/n)}}{2(n+c^2)},

    with the boundary rows set to ``L(0) = 0`` and ``U(n) = 1``. This is the interval PASS calls
    "Score with continuity correction". (The original ``cicsc`` port leaves the two boundary rows
    uncorrected, so its coverage collapses as :math:`\theta\to0` or :math:`1`; this one does not.)
    Pires & Amado find it *strictly conservative* (coverage never below :math:`1-\alpha-0.005`
    for :math:`n\ge10`).

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LSCC``, ``USCC`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    c = _z(alp)
    x = np.arange(n + 1, dtype=float)
    d = 2 * (n + c * c)
    with np.errstate(invalid="ignore"):
        lower = (
            2 * x
            + c * c
            - 1
            - c * np.sqrt(np.maximum(c * c - (2 + 1 / n) + 4 * x * (1 - x / n + 1 / n), 0.0))
        ) / d
        upper = (
            2 * x
            + c * c
            + 1
            + c * np.sqrt(np.maximum(c * c + (2 - 1 / n) + 4 * x * (1 - x / n - 1 / n), 0.0))
        ) / d
    lower[0] = 0.0
    upper[n] = 1.0
    return table("SCC", lower, upper)


def _wald_family(n, alp, recentre, cc):
    c = _z(alp)
    x = np.arange(n + 1)
    p = x / n
    half = c * np.sqrt(x / n**2 * (1 - x / n)) + (1 / (2 * n) if cc else 0.0)
    centre = (x + c * c / 2) / (n + c * c) if recentre else p
    lower, upper = centre - half, centre + half
    lower, upper = _cp_rows(n, alp, lower, upper)
    return np.maximum(lower, 0.0), np.minimum(upper, 1.0)


def ciwaldi(n, alp):
    r"""Wald-I interval (Pires & Amado method VII): Wald with exact rows at ``x = 0`` and ``x = n``.

    The Wald interval has zero width at the boundary, which no practitioner would report;
    Vollset (1993) replaces just those two rows by the exact Clopper-Pearson closed forms
    :math:`[0, 1-(\alpha/2)^{1/n}]` and :math:`[(\alpha/2)^{1/n}, 1]`. Elsewhere it is plain Wald.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LWDI``, ``UWDI`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    return table("WDI", *_wald_family(n, alp, recentre=False, cc=False))


def ciwaldicc(n, alp):
    r"""Wald-I with continuity correction :math:`\pm 1/(2n)` (Pires & Amado method VIII).

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LWIC``, ``UWIC`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    return table("WIC", *_wald_family(n, alp, recentre=False, cc=True))


def ciwaldrec(n, alp):
    r"""Recentred Wald-I (Pires & Amado method IX).

    The Wald half-width :math:`z\sqrt{\hat p\hat q/n}` around the Wilson centre
    :math:`(x+z^2/2)/(n+z^2)` (a correction mentioned by Brown, Cai & DasGupta 2002), with the
    exact Clopper-Pearson boundary rows.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LWRC``, ``UWRC`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    return table("WRC", *_wald_family(n, alp, recentre=True, cc=False))


def ciwaldreccc(n, alp):
    r"""Recentred Wald-I with continuity correction (Pires & Amado method X).

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LWRK``, ``UWRK`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    return table("WRK", *_wald_family(n, alp, recentre=True, cc=True))


def _boot_family(n, alp, bias_corrected, cc):
    """Analytic bootstrap: quantiles of ``Binomial(n, x/n)`` -- the bootstrap law is *exactly* that."""
    x = np.arange(n + 1)
    p = np.where((x > 0) & (x < n), x / n, 0.5)  # boundary rows are overwritten below
    a_lo = np.full(n + 1, alp / 2)
    a_hi = np.full(n + 1, 1 - alp / 2)
    if bias_corrected:
        kb = 0.5 * (stats.binom.cdf(x, n, p) + stats.binom.cdf(x - 1, n, p))
        shift = 2 * stats.norm.ppf(np.clip(kb, 1e-300, 1 - 1e-16))
        a_lo = stats.norm.cdf(stats.norm.ppf(alp / 2) + shift)
        a_hi = stats.norm.cdf(stats.norm.ppf(1 - alp / 2) + shift)
    lower = stats.binom.ppf(a_lo, n, p) / n
    upper = stats.binom.ppf(a_hi, n, p) / n
    if cc:
        lower, upper = lower - 1 / (2 * n), upper + 1 / (2 * n)
    lower, upper = _cp_rows(n, alp, lower, upper)
    return np.maximum(lower, 0.0), np.minimum(upper, 1.0)


def cibootp(n, alp):
    r"""Analytic percentile-bootstrap interval (Pires & Amado method XI), no Monte Carlo.

    The bootstrap distribution of :math:`n\hat p` is exactly :math:`\mathrm{Bin}(n, x/n)`, so the
    percentile interval is just the :math:`\alpha/2` and :math:`1-\alpha/2` quantiles of that
    distribution divided by ``n`` -- deterministic and instantaneous (cf. :func:`binomcikit.ciboot`,
    which resamples). Boundary rows are the exact Clopper-Pearson forms.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LBTP``, ``UBTP`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    return table("BTP", *_boot_family(n, alp, bias_corrected=False, cc=False))


def cibootpcc(n, alp):
    r"""Percentile bootstrap with continuity correction :math:`\pm1/(2n)` (method XII).

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LBPC``, ``UBPC`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    return table("BPC", *_boot_family(n, alp, bias_corrected=False, cc=True))


def cibcp(n, alp):
    r"""Analytic bias-corrected percentile bootstrap (Pires & Amado method XIII).

    Replaces the percentiles :math:`\alpha/2`, :math:`1-\alpha/2` by
    :math:`\Phi(z_{\alpha/2}+2\Phi^{-1}(K_B))` and :math:`\Phi(z_{1-\alpha/2}+2\Phi^{-1}(K_B))`,
    with :math:`K_B=\tfrac12[F(x)+F(x-1)]` the mid-distribution of the bootstrap law.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LBCP``, ``UBCP`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    return table("BCP", *_boot_family(n, alp, bias_corrected=True, cc=False))


def cibcpcc(n, alp):
    r"""Bias-corrected percentile bootstrap with continuity correction (method XIV).

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LBCC``, ``UBCC`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    return table("BCC", *_boot_family(n, alp, bias_corrected=True, cc=True))


def ciarcsineans(n, alp, clamp=False):
    r"""Arcsine interval with continuity *and* Anscombe's correction (Pires & Amado method XVII).

    :math:`\sin^2\!\bigl(\arcsin\sqrt{(3/8+x\mp1/2)/(n+3/4)}\;\mp\;c/(2\sqrt{n+1/2})\bigr)`
    with the lower limit set to 0 at :math:`x=0` and the upper to 1 at :math:`x=n` -- exactly the
    paper's Table 2. Pires & Amado find it, with Score-cc, one of the only *strictly conservative*
    approximate intervals (coverage never meaningfully below nominal), at a much shorter length than
    Clopper-Pearson.

    Parameters
    ----------
    n, alp : see :func:`binomcikit.cisc`.
    clamp : bool, default False
        The printed formula is applied literally (``clamp=False``): when the shifted angle leaves
        :math:`[0,\pi/2]` (only for ``x`` next to a boundary) :math:`\sin^2` folds back and gives a tiny
        non-monotone value (e.g. 0.00023 at ``n=7, x=1``). ``clamp=True`` pins such limits to 0 / 1
        instead, which keeps the limits monotone and can only widen the interval.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LANS``, ``UANS`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    c = _z(alp)
    x = np.arange(n + 1)
    shift = c / (2 * np.sqrt(n + 0.5))
    a_lo = np.arcsin(np.sqrt(np.clip((3 / 8 + x - 0.5) / (n + 0.75), 0, 1))) - shift
    a_hi = np.arcsin(np.sqrt(np.clip((3 / 8 + x + 0.5) / (n + 0.75), 0, 1))) + shift
    lower = np.sin(a_lo) ** 2
    upper = np.sin(a_hi) ** 2
    if clamp:
        lower = np.where(a_lo > 0, lower, 0.0)
        upper = np.where(a_hi < np.pi / 2, upper, 1.0)
    lower[0] = 0.0
    upper[n] = 1.0
    return table("ANS", lower, upper)


def _single(fn, code):
    def f(x, n, alp, **kw):
        n = validate(n, alp)
        return single(fn(n, alp, **kw), check_x(x, n), code)

    return f


ciscoreccx = _single(ciscorecc, "SCC")
ciwaldix = _single(ciwaldi, "WDI")
ciwaldiccx = _single(ciwaldicc, "WIC")
ciwaldrecx = _single(ciwaldrec, "WRC")
ciwaldrecccx = _single(ciwaldreccc, "WRK")
cibootpx = _single(cibootp, "BTP")
cibootpccx = _single(cibootpcc, "BPC")
cibcpx = _single(cibcp, "BCP")
cibcpccx = _single(cibcpcc, "BCC")
ciarcsineansx = _single(ciarcsineans, "ANS")
