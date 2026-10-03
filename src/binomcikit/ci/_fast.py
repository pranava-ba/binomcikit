"""Vectorised kernels behind the base interval methods.

The original ``ci*`` functions are literal ports of the R package: a Python loop over every
``x`` with a scalar root-finder inside, which makes a whole table cost ``O(n)`` Python-level
iterations (and Clopper-Pearson ``O(n^2)`` pmf evaluations per row). The kernels here compute
the *same* limits for every ``x`` at once:

* closed-form methods are single array expressions;
* Clopper-Pearson (``e = 1``) is two beta-quantile calls;
* every other root (general exact ``e``, likelihood-ratio, the HPD search) is a **vectorised
  bisection** -- ``60`` halvings of all brackets together, ~``1e-18`` of the bracket, which is
  at least as tight as the scalar solvers they replace (``xtol = 2e-12``).

Semantics (boundary rows, flags, clamping) are unchanged, and every kernel is regression-tested
against the legacy scalar implementation it replaces.
"""

from __future__ import annotations

import numpy as np
import scipy.stats as stats
from scipy import special

_ITERS = 60


def zcrit(alp):
    """``z_{1 - alp/2}``: ``scipy.stats.norm.ppf`` without its ~100 us per-call overhead.

    ``norm.ppf`` *is* ``special.ndtri`` (with ``loc=0, scale=1``), so the value is bit-identical.
    """
    return float(special.ndtri(1 - alp / 2))


def beta_ppf(q, a, b):
    """``scipy.stats.beta.ppf`` for valid shapes, via the underlying ufunc (no argument-check cost)."""
    return special.betaincinv(a, b, q)


# ---------------------------------------------------------------- array-only closed forms
def wald_arrays(n, alp):
    x = np.arange(n + 1)
    p = x / n
    h = zcrit(alp) * np.sqrt(p * (1 - p) / n)
    return np.clip(p - h, 0.0, 1.0), np.clip(p + h, 0.0, 1.0)


def wilson_arrays(n, alp):
    z = zcrit(alp)
    p = np.arange(n + 1) / n
    se = np.sqrt(p * (1 - p) / n + (z / (2 * n)) ** 2)
    c = n / (n + z * z)
    mid = p + z * z / (2 * n)
    return np.clip(c * (mid - z * se), 0.0, 1.0), np.clip(c * (mid + z * se), 0.0, 1.0)


def agresti_coull_arrays(n, alp):
    z = zcrit(alp)
    x = np.arange(n + 1)
    nt = n + z * z
    pt = (x + z * z / 2) / nt
    h = z * np.sqrt(pt * (1 - pt) / nt)
    return np.clip(pt - h, 0.0, 1.0), np.clip(pt + h, 0.0, 1.0)


def arcsine_arrays(n, alp):
    p = np.arange(n + 1) / n
    se = zcrit(alp) / np.sqrt(4 * n)
    s = np.arcsin(np.sqrt(p))
    return np.clip(np.sin(s - se) ** 2, 0.0, 1.0), np.clip(np.sin(s + se) ** 2, 0.0, 1.0)


def logit_arrays(n, alp):
    z = zcrit(alp)
    lower = np.zeros(n + 1)
    upper = np.ones(n + 1)
    upper[0] = 1 - (alp / 2) ** (1 / n)
    lower[n] = (alp / 2) ** (1 / n)
    j = np.arange(1, n)
    p = j / n
    lg = np.log(p / (1 - p))
    se = np.sqrt(p * (1 - p) * n)
    lower[1:n] = 1 / (1 + np.exp(-lg + z / se))
    upper[1:n] = 1 / (1 + np.exp(-lg - z / se))
    return np.clip(lower, 0.0, 1.0), np.clip(upper, 0.0, 1.0)


def jeffreys_arrays(n, alp, a=0.5, b=0.5):
    x = np.arange(n + 1)
    lower = beta_ppf(alp / 2, x + a, n - x + b)
    if a == b:  # symmetric prior: U(x) = 1 - L(n - x) -- half the quantile evaluations
        return lower, 1.0 - lower[::-1]
    return lower, beta_ppf(1 - alp / 2, x + a, n - x + b)


def bisect(f, lo, hi, increasing, iters=_ITERS):
    """Vectorised bisection for a monotone ``f`` crossing zero in each ``[lo_i, hi_i]``."""
    lo = np.array(lo, dtype=float)
    hi = np.array(hi, dtype=float)
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        above = f(mid) > 0
        if increasing:
            hi = np.where(above, mid, hi)
            lo = np.where(above, lo, mid)
        else:
            lo = np.where(above, mid, lo)
            hi = np.where(above, hi, mid)
    return 0.5 * (lo + hi)


_NO_YES = np.array(["NO", "YES"], dtype=object)


def yes_no(mask):
    """``"YES"`` where ``mask`` else ``"NO"``, as an object array (3x faster than ``np.where(...).astype``)."""
    return _NO_YES[np.asarray(mask, dtype=bool).view(np.int8)]


def flags(lower, upper):
    """``LABB``/``UABB`` (raw limit outside [0, 1]) and ``ZWI`` (zero width after clamping)."""
    labb = yes_no(lower < 0)
    uabb = yes_no(upper > 1)
    lo = np.maximum(lower, 0.0)
    hi = np.minimum(upper, 1.0)
    zwi = yes_no(hi - lo == 0)
    return lo, hi, labb, uabb, zwi


# ------------------------------------------------------------------ exact (Clopper-Pearson / Mid-P)
def exact_limits(n, alp, e):
    """Lower/upper limits of the exact family for every ``x`` (``e = 1``: Clopper-Pearson).

    The family is equivariant -- ``U(x) = 1 - L(n - x)`` -- so only the *lower* limits are solved
    (half the work); the upper limits are their mirror image.
    """
    x = np.arange(n + 1)
    lower = np.zeros(n + 1)
    # boundary row exactly as the scalar code computes it (same expression, same errors)
    lower[n] = (alp / (2 * e)) ** (1 / n)
    inner = x[1:n]
    if inner.size:
        if e == 1:
            lower[inner] = beta_ppf(alp / 2, inner, n - inner + 1)
        else:
            zero = np.zeros(inner.shape)
            one = np.ones(inner.shape)

            def f1(
                p,
            ):  # lower limit: (1-e) f(x) + F(x-1) - (1 - alpha/2); F(x-1), f(x) from the cdf ufunc
                below = special.bdtr(inner - 1, n, p)
                return (1 - e) * (special.bdtr(inner, n, p) - below) + below - (1 - alp / 2)

            lower[inner] = bisect(f1, zero, one, increasing=False)
    return lower, 1.0 - lower[::-1]


# ------------------------------------------------------------------------------ likelihood ratio
def lr_limits(n, alp):
    """Likelihood-ratio limits for every ``x`` via the (underflow-free) deviance."""
    z2 = zcrit(alp) ** 2
    x = np.arange(n + 1)
    lower = np.zeros(n + 1)
    upper = np.ones(n + 1)
    # x = 0 / x = n: the deviance is -2 n log(1 - p) / -2 n log(p) -> closed form
    upper[0] = 1 - np.exp(-z2 / (2 * n))
    lower[n] = np.exp(-z2 / (2 * n))
    inner = x[1:n]
    if inner.size:
        xf = inner.astype(float)
        ph = xf / n
        eps = 1e-12

        def dev(p):
            return 2 * (xf * np.log(ph / p) + (n - xf) * np.log((1 - ph) / (1 - p))) - z2

        lower[inner] = bisect(dev, np.full(ph.shape, eps), ph, increasing=False)
        upper[inner] = bisect(dev, ph, np.full(ph.shape, 1 - eps), increasing=True)
    return lower, upper


def lr_limits_y(y, n1, alp):
    """Likelihood-ratio limits for ``y`` successes in ``n1`` trials (``y`` an array of any offset).

    The same deviance bisection as :func:`lr_limits`, for the pseudo-counts ``y = x + h``,
    ``n1 = n + 2h`` of the adjusted LR interval; ``y = 0`` / ``y = n1`` rows are closed form.
    """
    z2 = zcrit(alp) ** 2
    y = np.asarray(y, dtype=float)
    ph = y / n1
    eps = 1e-12
    lower = np.zeros(y.shape)
    upper = np.ones(y.shape)

    def dev(p):
        return 2 * (special.xlogy(y, ph / p) + special.xlogy(n1 - y, (1 - ph) / (1 - p))) - z2

    lo_b = y > 0
    hi_b = y < n1
    lower[lo_b] = bisect(dev, np.full(y.shape, eps), ph, increasing=False)[lo_b]
    upper[hi_b] = bisect(dev, ph, np.full(y.shape, 1 - eps), increasing=True)[hi_b]
    return lower, upper


# ------------------------------------------------------------------------------------------ HPD
def _hpd_newton(a, b, conf, iters=80):
    """HPD of unimodal ``Beta(a, b)`` (``a, b > 1``): the equal-density condition, by safeguarded Newton.

    The unknown is the lower limit ``q``; the upper limit follows from ``F(q_hi) = F(q) + conf``. The
    condition ``h(q) = log f(q) - log f(q_hi(q)) = 0`` has the derivative
    ``dh/dq = s(q) - s(q_hi) f(q)/f(q_hi)`` with ``s = (a-1)/q - (b-1)/(1-q)``. Newton steps that leave
    the bisection bracket are replaced by its midpoint. Rows converge at very different speeds (the
    extreme ``x`` take many steps), so the loop shrinks to the still-unconverged *active set*.
    """
    alpha = 1.0 - conf
    n = a.size
    q = special.betaincinv(a, b, alpha / 2)
    qlo = np.full(n, 1e-300)
    qhi = special.betaincinv(a, b, alpha)
    lbeta = special.betaln(a, b)
    active = np.arange(n)
    for _ in range(iters):
        aa, bb, lb = a[active], b[active], lbeta[active]
        qq = q[active]
        qh = special.betaincinv(aa, bb, special.betainc(aa, bb, qq) + conf)
        lf_q = (aa - 1) * np.log(qq) + (bb - 1) * np.log1p(-qq) - lb
        lf_h = (aa - 1) * np.log(qh) + (bb - 1) * np.log1p(-qh) - lb
        h = lf_q - lf_h
        pos = h > 0
        lo_, hi_ = qlo[active], qhi[active]
        hi_ = np.where(pos, qq, hi_)
        lo_ = np.where(pos, lo_, qq)
        d = ((aa - 1) / qq - (bb - 1) / (1 - qq)) - ((aa - 1) / qh - (bb - 1) / (1 - qh)) * np.exp(
            lf_q - lf_h
        )
        with np.errstate(all="ignore"):
            step = qq - h / d
        qn = np.where((step > lo_) & (step < hi_) & np.isfinite(step), step, 0.5 * (lo_ + hi_))
        qlo[active], qhi[active], q[active] = lo_, hi_, qn
        active = active[np.abs(qn - qq) > 1e-13 * qq]
        if active.size == 0:
            break
    return q, special.betaincinv(a, b, special.betainc(a, b, q) + conf)


def hpd_beta_vec(a, b, conf=0.95):
    """HPD intervals of ``Beta(a_i, b_i)`` for arrays of shapes, all at once.

    * unimodal shapes (``a, b > 1``): equal-density condition by safeguarded Newton (``_hpd_newton``);
    * monotone-density shapes: the closed forms ``[0, F^-1(conf)]`` (``a <= 1 < b``) and
      ``[F^-1(1-conf), 1]`` (``b <= 1 < a``);
    * the remaining shapes (``a, b <= 1``, U-shaped) minimise the width by a vectorised
      golden-section search over the lower-tail probability, the same objective as the scalar
      ``hpd_beta``.

    Degenerate shapes (``a <= 0`` or ``b <= 0``) are returned as NaN for the caller to fall back on.
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    out_lo = np.full(a.shape, np.nan)
    out_hi = np.full(a.shape, np.nan)
    ok = (a > 0) & (b > 0)
    if not ok.any():
        return out_lo, out_hi
    inner = ok & (a > 1) & (b > 1)
    if inner.any():
        out_lo[inner], out_hi[inner] = _hpd_newton(a[inner], b[inner], conf)
    left = ok & (a <= 1) & (b > 1)  # density decreasing from 0: the HPD starts at 0
    if left.any():
        out_lo[left], out_hi[left] = 0.0, special.betaincinv(a[left], b[left], conf)
    right = ok & (b <= 1) & (a > 1)  # density increasing to 1: the HPD ends at 1
    if right.any():
        out_lo[right], out_hi[right] = special.betaincinv(a[right], b[right], 1 - conf), 1.0
    rest = ok & ~inner & ~left & ~right
    if not rest.any():
        return out_lo, out_hi
    out_lo[rest], out_hi[rest] = _hpd_golden(a[rest], b[rest], conf)
    return out_lo, out_hi


def _hpd_golden(a, b, conf):
    """Width-minimising golden-section HPD (U-shaped / general fallback)."""
    out_lo = np.full(a.shape, np.nan)
    out_hi = np.full(a.shape, np.nan)
    ok = np.ones(a.shape, dtype=bool)
    aa, bb = a, b
    alpha = 1.0 - conf

    def width(p):
        return stats.beta.ppf(p + conf, aa, bb) - stats.beta.ppf(p, aa, bb)

    gr = (np.sqrt(5.0) - 1.0) / 2.0
    lo = np.zeros(aa.shape)
    hi = np.full(aa.shape, alpha)
    for _ in range(64):  # 0.618^64 ~ 4e-14 of the bracket
        c = hi - gr * (hi - lo)
        d = lo + gr * (hi - lo)
        left = width(c) < width(d)  # the minimum lies in [lo, d]
        hi = np.where(left, d, hi)
        lo = np.where(left, lo, c)
    p = 0.5 * (lo + hi)
    out_lo[ok] = stats.beta.ppf(p, aa, bb)
    out_hi[ok] = stats.beta.ppf(p + conf, aa, bb)
    # the minimum can sit exactly on a bracket end (U/J-shaped densities): compare the ends
    for edge in (0.0, alpha):
        w_edge = stats.beta.ppf(edge + conf, aa, bb) - stats.beta.ppf(edge, aa, bb)
        better = w_edge < (out_hi[ok] - out_lo[ok])
        cur_lo, cur_hi = out_lo[ok], out_hi[ok]
        out_lo[ok] = np.where(better, stats.beta.ppf(edge, aa, bb), cur_lo)
        out_hi[ok] = np.where(better, stats.beta.ppf(edge + conf, aa, bb), cur_hi)
    return out_lo, out_hi
