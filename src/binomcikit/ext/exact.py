"""Exact and exact-flavoured intervals beyond Clopper-Pearson / Mid-P / Blaker.

* **Sterne (1954)** -- invert the probability-ordered ("minlike") test; computed with
  Duembgen's (2021) exact algorithm.
* **Blyth-Still-Casella (Casella 1986)** -- the shortest *exact* intervals, obtained by
  iteratively shrinking Clopper-Pearson until coverage touches ``1 - alpha``; ported
  from the reference algorithm in the R package ``rbscCI``.
* **Optimal locally correct (Garthwaite, Moustafa & Elfadaly 2024)** -- the shortest
  intervals whose coverage averages to ``1 - alpha`` between every pair of consecutive
  coverage "spikes"; closed-form integrals + one scalar root per row.
* **Witting (1985)** -- the randomised uniformly-most-accurate interval; *exact* coverage
  ``1 - alpha`` at every ``theta`` (the only interval here that is not conservative).

References
----------
* Sterne (1954), *Some remarks on confidence or fiducial limits*, Biometrika 41.
* Duembgen (2021), *Exact confidence bounds in discrete models -- algorithmic aspects
  of Sterne's method*, arXiv:2111.12937.
* Casella (1986), *Refining binomial confidence intervals*, Canad. J. Statist. 14;
  Blyth & Still (1983), JASA 78.
* Garthwaite, Moustafa & Elfadaly (2024), *Locally correct confidence intervals for a
  binomial proportion*, Scand. J. Statist. 51, 220-244 (arXiv:2106.15521).
* Witting (1985), *Mathematische Statistik I*, Teubner, Beispiel 2.106.
"""

from __future__ import annotations

import numpy as np
import scipy.stats as stats
from scipy import optimize
from scipy.special import bdtr, bdtrc, betainc, gammaln

from ._common import bisect_monotone, check_x, single, table, validate

# --------------------------------------------------------------------------- Sterne
_TIE = 1e-9  # tolerance for "f(y) <= f(x)" (ties occur exactly at the special points)


def _expit(t):
    return 1.0 / (1.0 + np.exp(-t))


def _sterne_upper(x, n, alp):
    """Upper limit of Sterne's interval for ``0 <= x < n`` (Duembgen 2021, Sec. 4.2)."""
    k_all = np.arange(n + 1)
    lw = gammaln(n + 1) - gammaln(k_all + 1) - gammaln(n - k_all + 1)  # log C(n, k)

    def p_special(k):  # the p at which f(k) = f(x), k != x
        return float(_expit((lw[x] - lw[k]) / (k - x)))

    rev = n - k_all

    def pi(p):  # Sterne's p-value pi(x, p); log-pmf from the precomputed log C(n, k)
        lf = lw + k_all * np.log(p) + rev * np.log1p(-p)
        return float(np.exp(lf[lf <= lf[x] + _TIE]).sum())

    # Stage 1: largest k > x with pi(x, p_{k,x}) >= alpha (binary search).
    if pi(p_special(n)) >= alp:
        k = n
    else:
        k, kp = x + 1, n
        while kp > k + 1:
            mid = (k + kp) // 2
            if pi(p_special(mid)) >= alp:
                k = mid
            else:
                kp = mid
    # Stage 2: locate the crossing on the piece (p_{k,x}, p_{k+1,x}).
    if k == n:
        b = p_special(n)
        if bdtr(x, n, b) <= alp:
            return b
        return float(stats.beta.ppf(1 - alp, x + 1, n - x))  # one-sided Clopper-Pearson

    def g(p):  # 1 - F(k) + F(x) - alpha: positive left of the root, negative right
        return bdtrc(k, n, p) + bdtr(x, n, p) - alp

    lo, hi = p_special(k), p_special(k + 1)
    if g(lo) <= 0:
        return lo
    return optimize.brentq(g, lo, hi, xtol=1e-14, rtol=1e-14)


def cisterne(n, alp):
    r"""Sterne's probability-ordered exact interval, for every ``x``.

    For each hypothesised :math:`\theta` the acceptance region collects the most
    probable outcomes first (smallest set with probability :math:`\ge1-\alpha`); the
    interval is the hull of the :math:`\theta` that accept ``x``. Guaranteed coverage
    :math:`\ge1-\alpha`, and on average much shorter than Clopper-Pearson, but **not**
    nested in it and not equal-tailed. Computed with Duembgen's exact algorithm
    (no grid): a binary search over the finitely many discontinuities of the p-value
    followed by one root-solve on a smooth piece.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LSTE``, ``USTE`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    ub = np.array([_sterne_upper(x, n, alp) for x in range(n)])  # x = 0..n-1
    upper = np.append(ub, 1.0)
    lower = np.empty(n + 1)
    lower[0] = 0.0
    lower[1:] = 1.0 - ub[::-1]  # equivariance: L(x) = 1 - U(n - x)
    return table("STE", lower, upper)


def cisternex(x, n, alp):
    """Sterne interval for a single observed ``x`` (does not build the full table)."""
    n = validate(n, alp)
    x = check_x(x, n)
    lo = 0.0 if x == 0 else 1.0 - _sterne_upper(n - x, n, alp)
    hi = 1.0 if x == n else _sterne_upper(x, n, alp)
    df = table("STE", [lo], [hi])
    df["x"] = x
    return df.rename(columns={"LSTE": "LSTEx", "USTE": "USTEx"})


# ------------------------------------------------------------ Blyth-Still-Casella
_CONV = 1e-13  # CONVERGENCE_GOAL in the reference implementation
_ITER = 100  # ITERATION_LIMIT


def _bsc_limits(n, alp):
    """Casella's (1986) refinement of Clopper-Pearson -- literal port of ``rbscCI``."""
    goal = 1 - alp
    k_all = np.arange(n + 1)
    lchoose = gammaln(n + 1) - gammaln(k_all + 1) - gammaln(n - k_all + 1)
    lower = np.zeros(n + 1)
    upper = np.ones(n + 1)
    lower[1:] = stats.beta.ppf(alp / 2, k_all[1:], n - k_all[1:] + 1)
    upper[:-1] = stats.beta.ppf(1 - alp / 2, k_all[:-1] + 1, n - k_all[:-1])

    def coverage(p):
        m = (lower < p) & (p < upper)
        kk = k_all[m]
        return float(np.exp(lchoose[m] + kk * np.log(p) + (n - kk) * np.log1p(-p)).sum())

    def search(width, orig, k):
        lo, hi = 0.0, width
        for _ in range(_ITER + 1):
            ret = 0.5 * (lo + hi)
            if hi - lo < _CONV:
                return ret
            lower[k] = orig + ret
            upper[n - k] = 1 - lower[k]
            val = coverage(lower[k])
            if val > goal:
                lo = ret
            elif val < goal:
                hi = ret
            else:
                return ret
        return ret

    for k in range(n, 0, -1):
        it = int(np.searchsorted(upper, lower[k], side="right"))
        if it >= n + 1:  # no upper limit above lower[k] (cannot happen for valid input)
            continue
        binding = upper[it]
        for _ in range(4 * n + 8):  # the reference loop; guarded against non-termination
            orig = lower[k]
            inc = search(binding - orig, orig, k)
            lower[k] = orig + inc
            upper[n - k] = 1 - lower[k]
            if lower[k] >= binding - 2 * _CONV:
                lower[k] = binding
                upper[n - k] = 1 - lower[k]
            if lower[k] == binding and coverage(lower[k]) >= goal:
                if it + 1 >= n + 1:
                    binding = 1.0
                else:
                    it += 1
                    binding = upper[it]
                continue
            break
    return lower, upper


def cibsc(n, alp):
    r"""Blyth-Still-Casella shortest exact interval, for every ``x``.

    Starts from Clopper-Pearson and, from the largest ``x`` downward, shrinks each
    interval (and its mirror) as far as possible while the coverage probability stays
    :math:`\ge 1-\alpha` at every :math:`\theta` (Casella 1986). The result is an
    **exact** interval with the smallest expected length among equivariant exact
    procedures -- the interval StatXact reports. It is generally not equal-tailed.
    Cost grows roughly as :math:`O(n^2)`; ``n`` in the low thousands is fine.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LBSC``, ``UBSC`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    lower, upper = _bsc_limits(n, alp)
    return table("BSC", lower, upper)


def cibscx(x, n, alp):
    """Blyth-Still-Casella interval for a single observed ``x`` (see :func:`cibsc`)."""
    n = validate(n, alp)
    return single(cibsc(n, alp), check_x(x, n), "BSC")


# ----------------------------------------------- optimal locally correct (Garthwaite)
def _olc_upper(n, alpha_one):
    """Upper-tail locally correct limits ``u_0 < ... < u_n = 1`` (Garthwaite et al. eq. 6).

    Uses the closed form ``G_i(p) = int_0^p P(X >= i | t) dt = p I_p(i, n-i+1) -
    i/(n+1) I_p(i+1, n-i+1)`` so each limit is one scalar root-find.
    """
    goal = 1.0 - alpha_one
    u = np.empty(n + 1)
    u[n] = 1.0
    gl_x, gl_w = np.polynomial.legendre.leggauss(6)
    fail = (
        "no admissible optimal-locally-correct limit found "
        f"(n={n}, alpha={2 * alpha_one:g}); the construction needs alpha/2 < 0.27"
    )
    gap = 0.5 / n  # running guess of u_i - u_{i-1} (warm start for the Newton solve)
    for i in range(n, 0, -1):
        ui = u[i]
        a1, b1 = i, n - i + 1

        def pg(v, i=i, a1=a1, b1=b1):  # (P(X >= i | v), G_i(v)) from two incomplete betas
            p_i = betainc(a1, b1, v)
            return p_i, v * p_i - i / (n + 1.0) * betainc(i + 1, b1, v)

        p_u, g_u = pg(ui)

        def avg(v, ui=ui, g_u=g_u, a1=a1, b1=b1):
            """Average coverage on ``(v, ui)`` and its derivative in ``v``, conditioned for ``v -> ui``."""
            d = ui - v
            p_v, g_v = pg(v)
            if d > 1e-3 * ui:
                a = (g_u - g_v) / d
            else:  # the difference quotient cancels: integrate the smooth integrand instead
                x = 0.5 * (v + ui) + 0.5 * d * gl_x
                a = 0.5 * float(np.dot(gl_w, betainc(a1, b1, x)))
            return a, (a - p_v) / d

        # f(v) = avg(v) - goal rises from f(0) < 0 to f(ui-) = P(X >= i | ui) - goal > 0
        if not (g_u / ui < goal <= p_u):
            raise ValueError(fail)
        lo, hi = 0.0, ui
        v = min(max(ui - gap, 0.0), ui * (1 - 1e-9))
        for _ in range(80):
            a, da = avg(v)
            f = a - goal
            if f < 0:
                lo = v
            else:
                hi = v
            step = v - f / da if da > 0 else np.nan
            vn = step if lo < step < hi else 0.5 * (lo + hi)
            if abs(vn - v) <= 1e-15 * (1.0 + v) or hi - lo <= 1e-16:
                v = vn
                break
            v = vn
        u[i - 1] = v
        gap = max(ui - v, 1e-12)
    return u


def ciolc(n, alp):
    r"""Optimal locally correct (OLC) interval (Garthwaite et al. 2024), for every ``x``.

    A *locally correct* interval has average coverage :math:`\ge 1-\alpha` between
    each pair of consecutive coverage spikes -- a weaker, more honest requirement than
    "coverage :math:`\ge 1-\alpha` everywhere" that removes Clopper-Pearson's
    conservatism. The OLC limits solve
    :math:`\frac{1}{u_i-u_{i-1}}\int_{u_{i-1}}^{u_i}P(X\ge i\mid p)\,dp=1-\alpha/2`
    from :math:`u_n=1` downward, and mirror for the lower tail, giving an equal-tailed
    interval proved to have the smallest average expected length of all locally correct
    procedures. The optimality is *proved* for :math:`n\le200` and a one-sided level
    :math:`\alpha/2<0.27` (two-sided :math:`\alpha<0.54`); the limits are computed for any
    ``n`` and verified against the authors' published tables (``n`` up to 30, 95% and 99%).

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LOLC``, ``UOLC`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    if alp / 2.0 >= 0.27:
        raise ValueError(
            "the optimal locally correct interval is defined for a one-sided level "
            f"alpha/2 < 0.27, i.e. alpha < 0.54 (got alpha={alp:g})"
        )
    u = _olc_upper(n, alp / 2.0)
    upper = u.copy()
    lower = 1.0 - u[::-1]
    return table("OLC", lower, upper)


def ciolcx(x, n, alp):
    """Optimal locally correct interval for a single observed ``x``."""
    n = validate(n, alp)
    return single(ciolc(n, alp), check_x(x, n), "OLC")


# -------------------------------------------------------------------------- Witting
def _abscont_cdf(q, n, theta):
    """CDF of ``X + U`` (``U ~ Uniform(0,1)``) at ``q`` -- Witting's smoothed variate."""
    v = np.floor(q)
    return stats.binom.cdf(v - 1, n, theta) + (q - v) * stats.binom.pmf(v, n, theta)


def ciwitting(n, alp, u=0.5, seed=None):
    r"""Witting's randomised uniformly-most-accurate interval, for every ``x``.

    Smooths the discrete count with an independent uniform: :math:`\tilde x=x+U`.
    The lower and upper limits solve :math:`F_\theta(\tilde x)=1-\alpha/2` and
    :math:`\alpha/2` for the continuous cdf of :math:`X+U`, so for a **genuinely
    random** ``U`` the interval has coverage *exactly* :math:`1-\alpha` at every
    :math:`\theta` (verified in the test-suite by exact integration), unlike every
    other exact method. The price is randomisation: two analysts can get different
    intervals from the same data.

    Parameters
    ----------
    n : int
        Number of trials.
    alp : float
        Significance level.
    u : float or None, default 0.5
        The uniform draw. A number in ``[0, 1]`` fixes it for every ``x`` (the
        default ``0.5`` is the deterministic *mid-randomised* version used for plots
        and comparisons); ``None`` draws an independent ``U`` per ``x``.
    seed : int, optional
        RNG seed, used only when ``u is None``.

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LWIT``, ``UWIT`` and the flags ``LABB``, ``UABB``, ``ZWI``.

    Notes
    -----
    ``DescTools::BinomCI(method="witting")`` places :math:`\alpha` (not
    :math:`\alpha/2`) in each tail, so it returns a :math:`1-2\alpha` interval; this
    function uses :math:`\alpha/2` per tail.
    """
    n = validate(n, alp)
    x = np.arange(n + 1, dtype=float)
    if u is None:
        uu = np.random.default_rng(seed).uniform(size=n + 1)
    else:
        if not 0.0 <= float(u) <= 1.0:
            raise ValueError("'u' has to be between 0 and 1")
        uu = np.full(n + 1, float(u))
    xt = x + uu
    zeros = np.zeros(n + 1)
    ones = np.ones(n + 1)

    # F_theta(xt) is decreasing in theta; its limits at theta = 0 / 1 decide existence.
    f0 = np.minimum(xt, 1.0)  # F_0(xt)
    f1 = np.maximum(xt - n, 0.0)  # F_1(xt)
    lo_exists = f0 > 1 - alp / 2
    hi_exists = f1 < alp / 2
    lower = np.zeros(n + 1)
    upper = np.ones(n + 1)
    if lo_exists.any():
        t = xt[lo_exists]
        lower[lo_exists] = bisect_monotone(
            lambda th: _abscont_cdf(t, n, th) - (1 - alp / 2),
            zeros[: t.size],
            ones[: t.size],
            False,
        )
    if hi_exists.any():
        t = xt[hi_exists]
        upper[hi_exists] = bisect_monotone(
            lambda th: _abscont_cdf(t, n, th) - alp / 2, zeros[: t.size], ones[: t.size], False
        )
    return table("WIT", lower, upper)


def ciwittingx(x, n, alp, u=0.5, seed=None):
    """Witting interval for a single observed ``x``."""
    n = validate(n, alp)
    return single(ciwitting(n, alp, u=u, seed=seed), check_x(x, n), "WIT")
