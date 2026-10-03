"""Betting and confidence-sequence intervals (the post-2017 paradigm).

A *test martingale* turns hypothesis testing into betting: for each candidate mean ``m``
run a gambler whose capital is a nonnegative martingale if ``theta = m``; by Ville's
inequality ``P(capital ever reaches 1/alpha) <= alpha``, so the set of ``m`` the gambler
fails to bankrupt is a ``(1 - alpha)`` confidence set -- valid at **every** sample size at
once when read as a confidence *sequence*.

Three constructions are provided:

``cimixture``
    Beta-binomial **mixture** confidence sequence (Robbins 1970; Howard et al. 2021). For
    Bernoulli data the mixture capital is a closed-form function of ``(x, n)`` alone, so it
    drops into the ordinary limits table, no randomisation needed.
``cibetting``
    The **hedged-capital** betting interval of Waudby-Smith & Ramdas (2024, JRSS-B): numerically
    the tightest known and variance-adaptive. It depends on the *order* of the 0/1 sequence,
    so the table version *derandomises* it by averaging the capital over ``B`` random
    permutations (their Section on derandomisation; valid by Markov's inequality).
``cibetseq``
    The genuine streaming confidence sequence on a user-supplied 0/1 stream (hedged capital,
    mixture, sub-Gaussian normal mixture, or the closed-form PrPl-EB).

References
----------
* Waudby-Smith & Ramdas (2024), *Estimating means of bounded random variables by betting*,
  JRSS-B 86 (arXiv:2010.09686).
* Howard, Ramdas, McAuliffe & Sekhon (2021), *Time-uniform, nonparametric, nonasymptotic
  confidence sequences*, Ann. Statist. 49.
* Robbins (1970), *Statistical methods related to the law of the iterated logarithm*.
"""

from __future__ import annotations

import importlib.util

import numpy as np
import pandas as pd
from scipy.special import betaln

from ._common import bisect_monotone, check_x, single, table, validate

# optional acceleration (results are identical without it); numba is imported lazily, on first use
HAS_NUMBA = importlib.util.find_spec("numba") is not None

_EDGE = 1e-12


# -------------------------------------------------------------------- mixture (exact)
def cimixture(n, alp, a=0.5, b=0.5):
    r"""Beta-binomial mixture confidence-sequence interval, for every ``x``.

    Mixes the Bernoulli likelihood-ratio capital over a Beta(``a``, ``b``) prior on the
    alternative. The mixture capital is
    :math:`M_n(m)=\frac{B(a+x,\,b+n-x)}{B(a,b)}\,m^{-x}(1-m)^{-(n-x)}`, so the interval
    :math:`\{m: M_n(m)<1/\alpha\}` is cut out by a unimodal function of :math:`m` and its
    limits are two scalar roots. By Ville's inequality it is a valid ``(1-alpha)`` interval
    **simultaneously at every ``n``** (an anytime-valid confidence sequence), which is why it
    is wider than a fixed-``n`` interval: that is the price of optional stopping. Depends on
    ``(x, n)`` only.

    Parameters
    ----------
    n : int
        Number of trials.
    alp : float
        Significance level (the *total* miscoverage ``alpha``, not ``alpha/2``).
    a, b : float, default 0.5
        Beta prior shape of the mixing distribution (Jeffreys by default).

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LMIX``, ``UMIX`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    if a <= 0 or b <= 0:
        raise ValueError("'a' and 'b' have to be positive")
    if alp <= 0:
        raise ValueError("'alpha' has to be greater than 0")
    x = np.arange(n + 1)
    p = x / n
    # accept m  <=>  x ln m + (n-x) ln(1-m) > c
    c = np.log(alp) + betaln(a + x, b + n - x) - betaln(a, b)

    lower = np.zeros(n + 1)
    upper = np.ones(n + 1)
    rows = x > 0
    if rows.any():
        xr = x[rows]
        root = bisect_monotone(
            lambda m: xr * np.log(m) + (n - xr) * np.log1p(-m) - c[rows],
            np.full(xr.shape, _EDGE),
            p[rows],
            increasing=True,
        )
        lower[rows] = np.where(root <= 2 * _EDGE, 0.0, root)
    rows = x < n
    if rows.any():
        xr = x[rows]
        root = bisect_monotone(
            lambda m: xr * np.log(m) + (n - xr) * np.log1p(-m) - c[rows],
            p[rows],
            np.full(xr.shape, 1 - _EDGE),
            increasing=False,
        )
        upper[rows] = np.where(root >= 1 - 2 * _EDGE, 1.0, root)
    return table("MIX", lower, upper)


def cimixturex(x, n, alp, a=0.5, b=0.5):
    """Beta-binomial mixture interval for a single observed ``x``."""
    n = validate(n, alp)
    return single(cimixture(n, alp, a, b), check_x(x, n), "MIX")


def cinormalmix(n, alp, n_opt=None):
    r"""Sub-Gaussian normal-mixture confidence-sequence interval, for every ``x``.

    The classical Robbins normal-mixture boundary with Hoeffding's variance proxy
    :math:`\sigma^2=1/4` for a Bernoulli:
    :math:`|\hat p-\theta|<\frac1n\sqrt{(n\sigma^2+\rho)\ln\frac{n\sigma^2+\rho}{\rho\alpha^2}}`.
    A closed form, anytime-valid, and variance-*blind* (so wide near 0 or 1) -- the
    baseline the variance-adaptive betting intervals improve on.

    Parameters
    ----------
    n, alp : see :func:`cimixture`.
    n_opt : int, optional
        Sample size the mixing variance ``rho`` is tuned for (default ``n``).

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LNMX``, ``UNMX`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    if alp <= 0:
        raise ValueError("'alpha' has to be greater than 0")
    s2 = 0.25
    t0 = float(n_opt if n_opt is not None else n)
    la = np.log(1.0 / alp)
    rho = t0 * s2 / (2 * la + np.log(1 + 2 * la))
    half = np.sqrt((n * s2 + rho) * np.log((n * s2 + rho) / (rho * alp**2))) / n
    p = np.arange(n + 1) / n
    return table("NMX", p - half, p + half)


def cinormalmixx(x, n, alp, n_opt=None):
    """Normal-mixture interval for a single observed ``x``."""
    n = validate(n, alp)
    return single(cinormalmix(n, alp, n_opt), check_x(x, n), "NMX")


# ------------------------------------------------------------ predictable plug-in bets
def _lambda_predmix_eb(x, alpha, fixed_n=None, prior_mean=0.5, prior_variance=0.25, fake_obs=1):
    """Predictable plug-in bet sizes (WSR eq. 26), identical to ``confseq.lambda_predmix_eb``.

    Row-wise on a 2-D ``x`` (sequences along the last axis).
    """
    x = np.atleast_2d(np.asarray(x, dtype=float))
    t = np.arange(1, x.shape[-1] + 1)
    mu_t = np.minimum((fake_obs * prior_mean + np.cumsum(x, axis=-1)) / (t + fake_obs), 1.0)
    s2_t = (fake_obs * prior_variance + np.cumsum((x - mu_t) ** 2, axis=-1)) / (t + fake_obs)
    s2_prev = np.concatenate([np.full((x.shape[0], 1), prior_variance), s2_t[:, :-1]], axis=-1)
    la = np.log(1.0 / alpha)
    if fixed_n is None:
        lam = np.sqrt(2 * la / (t * np.log(1 + t) * s2_prev))
    else:
        lam = np.sqrt(2 * la / (fixed_n * s2_prev))
    return np.where(np.isnan(lam), 0.0, lam)


def _log_capital(m, x, lam, c, logth, log1mth):
    """``log`` of the hedged capital ``max(theta K+, (1-theta) K-)`` for each row of ``x``."""
    lp = np.minimum(lam, c / m)
    ln = np.minimum(lam, c / (1 - m))
    d = x - m
    kp = np.log1p(lp * d).sum(axis=-1)
    kn = np.log1p(-ln * d).sum(axis=-1)
    return np.maximum(logth + kp, log1mth + kn)


def _log_mean_capital_np(m, x, lam, c, logth, log1mth):
    lk = _log_capital(m, x, lam, c, logth, log1mth)
    mx = lk.max()
    return mx + np.log(np.exp(lk - mx).sum()) - np.log(lk.size)


if True:  # plain-Python kernels; compiled lazily by _compile()

    def _log_mean_capital_nb(m, x, lam, c, logth, log1mth):  # pragma: no cover - compiled
        bsz, n = x.shape
        lk = np.empty(bsz)
        capp = c / m
        capn = c / (1.0 - m)
        for b in range(bsz):
            sp = 0.0
            sn = 0.0
            for t in range(n):
                l = lam[b, t]
                lpt = l if l < capp else capp
                lnt = l if l < capn else capn
                d = x[b, t] - m
                sp += np.log1p(lpt * d)
                sn += np.log1p(-lnt * d)
            a1 = logth + sp
            a2 = log1mth + sn
            lk[b] = a1 if a1 > a2 else a2
        mx = lk.max()
        s = 0.0
        for b in range(bsz):
            s += np.exp(lk[b] - mx)
        return mx + np.log(s) - np.log(bsz)

    def _bet_limits_nb(xs, lam, c, logth, log1mth, thresh, phat, iters):  # pragma: no cover
        """Bisection for both limits of ``{m : mean capital < 1/alpha}`` (compiled)."""
        edge = 1e-12
        lower = 0.0
        upper = 1.0
        if (
            _log_mean_capital_nb(min(max(phat, edge), 1 - edge), xs, lam, c, logth, log1mth)
            >= thresh
        ):
            return phat, phat  # even the MLE is rejected (only at absurd alpha)
        if phat > 0.0:
            lo, hi = edge, phat
            for _ in range(iters):
                mid = 0.5 * (lo + hi)
                if _log_mean_capital_nb(mid, xs, lam, c, logth, log1mth) >= thresh:
                    lo = mid
                else:
                    hi = mid
            lower = hi if hi > 2.0 * edge else 0.0  # never rejected down to the edge => 0
        if phat < 1.0:
            lo, hi = phat, 1.0 - edge
            for _ in range(iters):
                mid = 0.5 * (lo + hi)
                if _log_mean_capital_nb(mid, xs, lam, c, logth, log1mth) >= thresh:
                    hi = mid
                else:
                    lo = mid
            upper = lo if lo < 1.0 - 2.0 * edge else 1.0
        return lower, upper


def _bet_chunk_py(
    xs3, lam3, c, logth, log1mth, thresh, phats, iters, lower, upper
):  # pragma: no cover
    """Both limits for a chunk of rows, one row per thread (compiled with ``prange``)."""
    for i in prange(xs3.shape[0]):  # noqa: F821 - prange is injected by _compile()
        lower[i], upper[i] = _bet_limits_nb(
            xs3[i], lam3[i], c, logth, log1mth, thresh, phats[i], iters
        )


_COMPILED = False
_bet_chunk_nb = None


def _compile():
    """Compile the kernels once (numba imported here, not at package import)."""
    global _COMPILED, _log_mean_capital_nb, _bet_limits_nb, _bet_chunk_nb
    if _COMPILED:
        return
    from numba import njit, prange

    _bet_chunk_py.__globals__["prange"] = prange

    _log_mean_capital_nb = njit(cache=True)(_log_mean_capital_nb)
    _bet_limits_nb = njit(cache=True)(_bet_limits_nb)
    _bet_chunk_nb = njit(cache=True, parallel=True)(_bet_chunk_py)
    _COMPILED = True


def _bet_limits_np(xs, lam, c, logth, log1mth, thresh, phat, iters):
    lower, upper = 0.0, 1.0
    f = lambda m: _log_mean_capital_np(m, xs, lam, c, logth, log1mth)  # noqa: E731
    if f(min(max(phat, _EDGE), 1 - _EDGE)) >= thresh:
        return phat, phat
    if phat > 0.0:
        lo, hi = _EDGE, phat
        for _ in range(iters):
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if f(mid) >= thresh else (lo, mid)
        lower = hi if hi > 2.0 * _EDGE else 0.0  # never rejected down to the edge => 0
    if phat < 1.0:
        lo, hi = phat, 1.0 - _EDGE
        for _ in range(iters):
            mid = 0.5 * (lo + hi)
            lo, hi = (lo, mid) if f(mid) >= thresh else (mid, hi)
        upper = lo if lo < 1.0 - 2.0 * _EDGE else 1.0
    return lower, upper


def cibetting(n, alp, B=50, seed=0, theta=0.5, trunc=0.5, use_numba=None):
    r"""Hedged-capital betting interval (Waudby-Smith & Ramdas 2024), derandomised, for every ``x``.

    For each ``x``: draw ``B`` random orderings of the ``x`` ones and ``n - x`` zeros, run the
    **hedged capital process** on each (a bet that the mean is *above* ``m`` and one that it is
    *below*, combined by ``max(theta K+, (1-theta) K-)`` with the predictable plug-in bets of
    their eq. 26), **average** the capital over the ``B`` orderings, and return
    :math:`\{m: \bar K_n(m) < 1/\alpha\}`. Each ordering's capital is a test supermartingale
    under :math:`\theta=m`, so by Markov's inequality the averaged set has coverage
    :math:`\ge1-\alpha` -- no randomness remains in the *guarantee*, only in the exact
    endpoints, which are pinned by ``seed``.

    This is a numerically **tighter** interval than Clopper-Pearson / Wilson's conservative
    side and is variance-adaptive; its cost is :math:`O(B\,n^2)` per table, so it is the
    slowest method in the package (numba gives ~10x).

    Parameters
    ----------
    n : int
        Number of trials.
    alp : float
        Significance level.
    B : int, default 50
        Number of random orderings averaged.
    seed : int, default 0
        RNG seed (the table is deterministic given it).
    theta : float, default 0.5
        Weight of the "mean above ``m``" bet versus the "below" bet.
    trunc : float, default 0.5
        Truncation of the bets (``trunc/m`` and ``trunc/(1-m)``), in ``(0, 1)``.
    use_numba : bool, optional
        Force or forbid the compiled kernel (default: use it when available).

    Returns
    -------
    pandas.DataFrame
        ``x``, ``LBET``, ``UBET`` and the flags ``LABB``, ``UABB``, ``ZWI``.
    """
    n = validate(n, alp)
    if alp <= 0:
        raise ValueError("'alpha' has to be greater than 0")
    if not 0 < theta < 1:
        raise ValueError("'theta' has to be between 0 and 1")
    if not 0 < trunc < 1:
        raise ValueError("'trunc' has to be between 0 and 1")
    if int(B) < 1:
        raise ValueError("'B' has to be at least 1")
    B = int(B)
    use_nb = HAS_NUMBA if use_numba is None else (bool(use_numba) and HAS_NUMBA)
    if use_nb:
        _compile()
    rng = np.random.default_rng(seed)
    logth, log1mth = np.log(theta), np.log1p(-theta)
    thresh = np.log(1.0 / alp)
    lower = np.zeros(n + 1)
    upper = np.ones(n + 1)

    def draw(x):  # B random orderings of x ones and n - x zeros (RNG consumed in x order)
        base = np.zeros(n)
        base[:x] = 1.0
        return rng.permuted(np.tile(base, (B, 1)), axis=1)

    if use_nb:
        # Rows are independent, so run chunks of them in parallel; orderings are drawn serially
        # in x order, so the table is identical to the serial computation for a given seed.
        chunk = max(16, 4_000_000 // (B * n))
        for start in range(0, n + 1, chunk):
            xr = range(start, min(start + chunk, n + 1))
            xs3 = np.stack([draw(x) for x in xr])
            lam3 = np.stack([_lambda_predmix_eb(xs, alp * theta, fixed_n=n) for xs in xs3])
            phats = np.array([x / n for x in xr])
            lo_c = np.empty(len(xr))
            up_c = np.empty(len(xr))
            _bet_chunk_nb(xs3, lam3, trunc, logth, log1mth, thresh, phats, 52, lo_c, up_c)
            lower[start : start + len(xr)] = lo_c
            upper[start : start + len(xr)] = up_c
    else:
        for x in range(n + 1):
            xs = draw(x)
            lam = _lambda_predmix_eb(xs, alp * theta, fixed_n=n)
            lower[x], upper[x] = _bet_limits_np(xs, lam, trunc, logth, log1mth, thresh, x / n, 52)
    return table("BET", lower, upper)


def cibettingx(x, n, alp, B=50, seed=0, theta=0.5, trunc=0.5):
    """Betting interval for a single observed ``x`` (see :func:`cibetting`)."""
    n = validate(n, alp)
    return single(cibetting(n, alp, B=B, seed=seed, theta=theta, trunc=trunc), check_x(x, n), "BET")


# ----------------------------------------------------------------- streaming sequences
def _hedged_cs(x, alpha, theta, c, breaks):
    """Hedged-capital confidence sequence on a grid (WSR; matches ``confseq.hedged_cs``)."""
    x = np.asarray(x, dtype=float)
    lam = _lambda_predmix_eb(x[None, :], alpha * theta)[0]
    grid = np.arange(0, breaks + 1) / breaks
    thresh = np.log(1.0 / alpha)
    logth, log1mth = np.log(theta), np.log1p(-theta)
    ok = np.empty((grid.size, x.size), dtype=bool)  # ok[j, t]: m_j still in the set at time t
    with np.errstate(divide="ignore", invalid="ignore"):
        for j, m in enumerate(grid):
            lp = np.minimum(lam, c / m if m > 0 else np.inf)
            ln = np.minimum(lam, c / (1 - m) if m < 1 else np.inf)
            d = x - m
            kp = np.cumsum(np.log1p(lp * d))
            kn = np.cumsum(np.log1p(-ln * d))
            ok[j] = np.maximum(logth + kp, log1mth + kn) <= thresh
    seen = ok.any(axis=0)
    first = ok.argmax(axis=0)
    last = grid.size - 1 - ok[::-1].argmax(axis=0)
    lo = np.where(seen, grid[first], 0.0)
    hi = np.where(seen, grid[last], 1.0)
    return np.maximum(0.0, lo - 1.0 / breaks), np.minimum(1.0, hi + 1.0 / breaks)


def _mixture_cs(x, alpha, a, b):
    """Beta-binomial mixture confidence sequence along a stream."""
    s = np.cumsum(x)
    t = np.arange(1, x.size + 1)
    p = s / t
    c = np.log(alpha) + betaln(a + s, b + t - s) - betaln(a, b)
    lo = np.zeros(x.size)
    hi = np.ones(x.size)
    r = s > 0
    if r.any():
        sr, tr = s[r], t[r]
        lo[r] = bisect_monotone(
            lambda m: sr * np.log(m) + (tr - sr) * np.log1p(-m) - c[r],
            np.full(sr.shape, _EDGE),
            p[r],
            True,
        )
    r = s < t
    if r.any():
        sr, tr = s[r], t[r]
        hi[r] = bisect_monotone(
            lambda m: sr * np.log(m) + (tr - sr) * np.log1p(-m) - c[r],
            p[r],
            np.full(sr.shape, 1 - _EDGE),
            False,
        )
    return lo, hi


def _normal_cs(x, alpha, n_opt):
    t = np.arange(1, x.size + 1)
    s2 = 0.25
    la = np.log(1.0 / alpha)
    rho = n_opt * s2 / (2 * la + np.log(1 + 2 * la))
    half = np.sqrt((t * s2 + rho) * np.log((t * s2 + rho) / (rho * alpha**2))) / t
    p = np.cumsum(x) / t
    return np.maximum(p - half, 0.0), np.minimum(p + half, 1.0)


def _preb_cs(x, alpha, c):
    """Closed-form predictable-plug-in empirical-Bernstein CS (WSR Thm 2; ``confseq`` form)."""
    t = np.arange(1, x.size + 1)

    def lower_cs(y):
        lam = np.minimum(_lambda_predmix_eb(y[None, :], alpha / 2.0)[0], c)
        mu_t = np.cumsum(y) / t
        mu_prev = np.concatenate([[0.0], mu_t[:-1]])
        v = (y - mu_prev) ** 2
        psi = -np.log(1 - lam) - lam
        margin = (np.log(2.0 / alpha) + np.cumsum(v * psi)) / np.cumsum(lam)
        centre = np.cumsum(lam * y) / np.cumsum(lam)
        return np.maximum(centre - margin, 0.0)

    lo = lower_cs(x)
    hi = 1.0 - lower_cs(1.0 - x)
    return lo, hi


def cibetseq(data, alpha=0.05, method="hedged", running_intersection=True, **params):
    r"""Anytime-valid confidence **sequence** for a 0/1 stream.

    A confidence sequence is a ``(L_t, U_t)`` for every ``t = 1, 2, ...`` such that **all
    of them hold simultaneously with probability** :math:`\ge1-\alpha` -- so you may peek
    after every observation and stop whenever you like (A/B tests, online monitoring, LLM
    evaluation) without inflating the error rate.

    Parameters
    ----------
    data : array-like of 0/1
        The ordered observations.
    alpha : float, default 0.05
        Total miscoverage over *all* times.
    method : {"hedged", "mixture", "normal", "preb"}
        ``"hedged"`` -- hedged-capital betting CS (tightest; grid-based, ``breaks`` controls
        resolution, default 1000, plus ``theta``, ``trunc``); ``"mixture"`` -- exact beta-binomial
        mixture (``a``, ``b``); ``"normal"`` -- sub-Gaussian normal mixture (``n_opt``);
        ``"preb"`` -- closed-form predictable-plug-in empirical Bernstein (``trunc``).
    running_intersection : bool, default True
        Intersect the intervals over time (still valid, and never wider than any past one).
    **params
        Method-specific options listed above.

    Returns
    -------
    pandas.DataFrame
        ``t``, ``phat``, ``lower``, ``upper`` for every prefix of the stream.
    """
    x = np.asarray(list(data), dtype=float)
    if x.size == 0:
        raise ValueError("'data' is empty")
    if not np.isin(x, (0.0, 1.0)).all():
        raise ValueError("'data' must contain only 0/1 values")
    if not 0 < alpha < 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    key = str(method).lower().strip()
    if key == "hedged":
        lo, hi = _hedged_cs(
            x,
            alpha,
            params.get("theta", 0.5),
            params.get("trunc", 0.5),
            int(params.get("breaks", 1000)),
        )
    elif key in ("mixture", "mix"):
        lo, hi = _mixture_cs(x, alpha, params.get("a", 0.5), params.get("b", 0.5))
    elif key in ("normal", "normal-mixture"):
        lo, hi = _normal_cs(x, alpha, params.get("n_opt", max(x.size, 1)))
    elif key in ("preb", "pr-pl-eb", "empirical-bernstein"):
        lo, hi = _preb_cs(x, alpha, params.get("trunc", 0.5))
    else:
        raise ValueError(f"unknown method {method!r}; choose hedged, mixture, normal or preb")
    if running_intersection:
        lo, hi = np.maximum.accumulate(lo), np.minimum.accumulate(hi)
    t = np.arange(1, x.size + 1)
    return pd.DataFrame({"t": t, "phat": np.cumsum(x) / t, "lower": lo, "upper": hi})
