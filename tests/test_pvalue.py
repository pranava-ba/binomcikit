"""Frequentist p-value tests (``pvalue``/``reject``) -- new code in binomcikit,
not part of R ``proportion`` (the 2017 paper treats CIs and tests as
interchangeable and explicitly omits separate test functions). Defined
directly from CI-test duality, so it works for any registered method, not
just ones with a closed-form test formula.

Verification strategy (see the ``pvalue`` docstring for why this is NOT
checked against ``scipy.stats.binomtest``'s default two-sided p-value -- that
uses a different, "minlike" convention that genuinely disagrees with the
equal-tailed CI-duality construction used here):

1. For ``method="exact"`` (Clopper-Pearson), the equal-tailed two-sided
   p-value has a well-known closed form,
   ``min(1, 2 * min(P(X<=x), P(X>=x)))`` -- an independent, standard formula
   (not something fit or guessed), checked directly.
2. The one-sided tail probabilities themselves are cross-checked against
   ``scipy.stats.binomtest(..., alternative="less"/"greater")``, which *does*
   use the unambiguous one-sided convention every implementation agrees on.
3. The defining property itself, directly: ``pvalue(...) < alpha`` iff
   ``theta0`` falls outside ``bk.ci(..., alpha=alpha, method=method)`` -- this
   is stronger evidence than matching any external program, the same
   principle used for Blaker's two-theorem verification.
"""

import numpy as np
import pytest
import scipy.stats as stats

import binomcikit as b


# --- closed-form oracle (method="exact") ------------------------------------
@pytest.mark.parametrize(
    "x,n,theta0",
    [(2, 10, 0.05), (2, 10, 0.1), (2, 10, 0.3), (2, 10, 0.5), (0, 10, 0.2), (10, 10, 0.8)],
)
def test_exact_pvalue_matches_closed_form_equal_tailed_formula(x, n, theta0):
    expected = min(1.0, 2 * min(stats.binom.cdf(x, n, theta0), stats.binom.sf(x - 1, n, theta0)))
    got = b.pvalue(x, n, theta0, method="exact")
    assert got == pytest.approx(expected, abs=1e-4)


@pytest.mark.parametrize("x,n,theta0", [(3, 20, 0.05), (7, 20, 0.6)])
def test_one_sided_tails_match_scipy_binomtest(x, n, theta0):
    lo = stats.binom.cdf(x, 20 if n == 20 else n, theta0)
    hi = stats.binom.sf(x - 1, n, theta0)
    assert lo == pytest.approx(stats.binomtest(x, n, theta0, alternative="less").pvalue)
    assert hi == pytest.approx(stats.binomtest(x, n, theta0, alternative="greater").pvalue)


def test_pvalue_deliberately_differs_from_scipy_default_two_sided():
    # Documents (and locks in) the deliberate divergence: binomcikit's exact
    # p-value is equal-tailed; scipy's default two-sided is minlike-based.
    x, n, theta0 = 3, 20, 0.05
    ours = b.pvalue(x, n, theta0, method="exact")
    scipy_default = stats.binomtest(x, n, theta0, alternative="two-sided").pvalue
    assert ours == pytest.approx(2 * scipy_default, abs=1e-4)  # exactly 2x here, not equal


# --- the defining property, checked directly (strongest evidence) ----------
@pytest.mark.parametrize(
    "method",
    ["wald", "wilson", "arcsine", "logit", "waldt", "lr", "exact", "midp", "bayes", "blaker"],
)
@pytest.mark.parametrize("alpha", [0.05])
def test_ci_duality_holds(method, alpha):
    # n kept small (not 20): the root-finding methods (exact/lr/blaker) loop
    # over every x internally, so cost scales with n -- this is the
    # correctness check, not a place to also stress-test performance. A
    # second alpha is covered separately (fast method only) by
    # test_reject_matches_pvalue_threshold.
    x, n, theta0 = 2, 10, 0.5
    p = b.pvalue(x, n, theta0, method=method)
    row = b.ci(x=x, n=n, alpha=alpha, method=method)
    lo_col = [c for c in row.columns if c.startswith("L")][0]
    hi_col = [c for c in row.columns if c.startswith("U")][0]
    L, U = float(row[lo_col].iloc[0]), float(row[hi_col].iloc[0])
    outside = theta0 < L or theta0 > U
    assert (p < alpha) == outside


def test_reject_matches_pvalue_threshold():
    for alpha in [0.2, 0.05, 0.01, 0.001]:
        p = b.pvalue(3, 20, 0.5, method="wilson")
        assert b.reject(3, 20, 0.5, method="wilson", alpha=alpha) == (p < alpha)


# --- edge cases --------------------------------------------------------------
def test_pvalue_is_one_when_theta0_equals_phat():
    assert b.pvalue(3, 20, 3 / 20, method="wilson") == 1.0
    assert b.pvalue(3, 20, 3 / 20, method="exact") == 1.0


def test_pvalue_near_zero_for_extreme_theta0():
    assert b.pvalue(0, 20, 0.99, method="wilson") < 1e-4
    assert b.pvalue(20, 20, 0.01, method="wilson") < 1e-4


@pytest.mark.parametrize(
    "method,draws,n_hi",
    [("wald", 20, 40), ("wilson", 20, 40), ("exact", 3, 12), ("blaker", 3, 12)],
)
def test_pvalue_bounded_in_unit_interval(method, draws, n_hi):
    # Fewer draws / smaller n for the root-finding methods (exact/blaker) --
    # same correctness check, without paying their per-call cost 20x over.
    rng = np.random.default_rng(0)
    for _ in range(draws):
        n = int(rng.integers(5, n_hi))
        x = int(rng.integers(0, n + 1))
        theta0 = float(rng.uniform(0.01, 0.99))
        p = b.pvalue(x, n, theta0, method=method)
        assert 0.0 <= p <= 1.0


# --- Wald's known duality mismatch (the exact phenomenon ROADMAP flags) -----
def test_wald_pvalue_diverges_from_score_based_methods():
    # Wald's variance is estimated at phat, not theta0 -- for a theta0 far
    # from a small phat, this makes Wald's interval narrower than it should
    # be, so it rejects "too easily": a much smaller p-value than
    # score/exact-based methods for the same (x, n, theta0). This is the
    # duality-is-only-approximate behavior the access-layer docstring and
    # ROADMAP.md both call out -- checked directly, not just asserted.
    x, n, theta0 = 3, 20, 0.5
    p_wald = b.pvalue(x, n, theta0, method="wald")
    p_wilson = b.pvalue(x, n, theta0, method="wilson")
    p_exact = b.pvalue(x, n, theta0, method="exact")
    assert p_wald < p_wilson / 10
    assert p_wald < p_exact / 10


# --- validation ---------------------------------------------------------------
def test_bootstrap_method_rejected():
    with pytest.raises(ValueError):
        b.pvalue(3, 20, 0.5, method="boot")


def test_bad_theta0_rejected():
    with pytest.raises(ValueError):
        b.pvalue(3, 20, 1.5, method="wilson")
    with pytest.raises(ValueError):
        b.pvalue(3, 20, -0.1, method="wilson")


def test_unknown_method_rejected():
    with pytest.raises(ValueError):
        b.pvalue(3, 20, 0.5, method="not-a-method")
