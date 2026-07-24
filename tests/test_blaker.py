"""Blaker's exact interval — new code in binomcikit (not in the R ``proportion``
package), so it gets property-based verification against its two defining theorems:

* **nesting** — the interval is contained in Clopper-Pearson (never wider), and
* **guaranteed coverage** — true coverage is >= 1 - alpha for every theta.

These are exactly the properties that make Blaker worth having, so checking them
is stronger evidence than matching some other implementation. Plus frozen
n = 5 golden limits and the construction identity gamma(x, limit) = alpha.
"""

import numpy as np
import pytest
import scipy.stats as stats
from cases import ALPHA, BLAKER_N5, N

import binomcikit as b
from binomcikit.ci.blaker import _blaker_gamma


def test_blaker_n5_matches_golden():
    df = b.ciblaker(N, ALPHA)
    for x, (lo, hi) in BLAKER_N5.items():
        assert df.LBK[x] == pytest.approx(lo, abs=5e-4)
        assert df.UBK[x] == pytest.approx(hi, abs=5e-4)


@pytest.mark.parametrize("n", [5, 10, 20, 30])
def test_blaker_nested_inside_clopper_pearson(n):
    # Theorem 1: Blaker is a subset of Clopper-Pearson (never wider).
    bk = b.ciblaker(n, ALPHA)
    cp = b.ciex(n, ALPHA, [1.0])
    for x in range(n + 1):
        c = cp[cp["x"] == x].iloc[0]
        assert bk.LBK[x] >= c["LEX"] - 1e-9
        assert bk.UBK[x] <= c["UEX"] + 1e-9


@pytest.mark.parametrize("n", [5, 10, 20])
def test_blaker_coverage_at_least_nominal(n):
    # Theorem 2: exact coverage >= 1 - alpha everywhere (the guarantee).
    df = b.ciblaker(n, ALPHA)
    lo = df.LBK.to_numpy()
    hi = df.UBK.to_numpy()
    k = np.arange(n + 1)
    thetas = np.linspace(1e-4, 1 - 1e-4, 1500)
    min_cov = 1.0
    for th in thetas:
        covered = (lo <= th) & (th <= hi)
        min_cov = min(min_cov, stats.binom.pmf(k, n, th)[covered].sum())
    assert min_cov >= (1 - ALPHA) - 1e-6


def test_blaker_strictly_improves_on_clopper_pearson():
    # The whole point: Blaker is genuinely narrower than CP for at least some x.
    n = 20
    bk = b.ciblaker(n, ALPHA)
    cp = b.ciex(n, ALPHA, [1.0])
    bk_w = (bk.UBK - bk.LBK).to_numpy()
    cp_w = np.array(
        [(cp[cp["x"] == x].iloc[0]["UEX"] - cp[cp["x"] == x].iloc[0]["LEX"]) for x in range(n + 1)]
    )
    assert np.all(bk_w <= cp_w + 1e-9)
    assert bk_w.sum() < cp_w.sum()  # strictly shorter overall


def test_blaker_brackets_mle_and_has_no_zwi():
    n = 20
    df = b.ciblaker(n, ALPHA)
    for x in range(1, n):
        assert df.LBK[x] < x / n < df.UBK[x]
    assert not (df.LBK == df.UBK).any()


@pytest.mark.parametrize("x", [1, 3, 7])
def test_blaker_limits_are_the_acceptance_boundary(x):
    # Construction identity: the limits bound {theta : gamma(x, theta) >= alpha}.
    # gamma is piecewise-continuous (it jumps as the acceptance set changes), so we
    # check the boundary directly: acceptable just inside, not acceptable just outside.
    n = 15
    eps = 1e-5  # >> brentq's convergence tolerance
    df = b.ciblaker(n, ALPHA)
    lo, hi = df.LBK[x], df.UBK[x]
    assert _blaker_gamma(x, n, lo + eps) >= ALPHA  # just inside the interval -> accepted
    assert _blaker_gamma(x, n, lo - eps) < ALPHA  # just below the lower limit -> rejected
    assert _blaker_gamma(x, n, hi - eps) >= ALPHA  # just inside -> accepted
    assert _blaker_gamma(x, n, hi + eps) < ALPHA  # just above the upper limit -> rejected


def test_blaker_dispatch_and_base_only():
    assert b.ci(n=10, method="blaker").equals(b.ciblaker(10, ALPHA))
    assert b.ci(3, n=10, method="blaker").equals(b.ciblakerx(3, 10, ALPHA))
    with pytest.raises(ValueError):  # base-only: no adjusted variant
        b.ci(n=10, method="blaker", h=2)
    with pytest.raises(ValueError):  # base-only: no continuity-corrected variant
        b.ci(n=10, method="blaker", c=0.5)


def test_blaker_inherits_metric_suite():
    # One limit-producer -> the whole diagnostic suite works with no extra code.
    assert b.covpblaker(10, ALPHA, 1, 1, 0.93, 0.97, seed=1).shape[0] == 1
    assert len(b.lengthblaker(10, ALPHA, 1, 1, seed=1)) >= 1
    assert len(b.pcopbiblaker(10, ALPHA)) == 9
    assert len(b.errblaker(10, ALPHA, 0.05, 1)) == 1
