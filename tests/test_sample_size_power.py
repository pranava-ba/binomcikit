"""Sample-size and power planning (``sample_size``/``power``) -- new code in
binomcikit, not part of R ``proportion`` (sample-size determination is a
pre-data design question outside the ported paper's scope; a dedicated R
package, `binomSamSize`, already existed and is cited rather than duplicated).

Verification strategy:

* ``sample_size(..., method="wald")`` is checked against
  ``statsmodels.stats.proportion.samplesize_confint_proportion`` -- a genuine,
  independent, well-known closed-form oracle for the Wald case specifically.
* For every method, the *defining* minimality property is checked directly:
  the returned n's width is <= target, and n-1's width is not -- the same
  "verify the property that defines correctness" standard used for Blaker's
  two theorems and pvalue's CI-duality identity.
* ``power`` is checked against an independent, brute-force construction built
  from the already-verified ``reject()`` (sub-phase 1.11) summed by hand over
  every x -- an internal cross-check between two independently-written paths
  to the same number.
"""

import math

import pytest
from scipy import stats
from statsmodels.stats.proportion import samplesize_confint_proportion

import binomcikit as b
from binomcikit.access import _NO_PVALUE, _width_at


# --- sample_size: oracle (Wald) ----------------------------------------------
@pytest.mark.parametrize("width,p0", [(0.1, 0.5), (0.2, 0.5), (0.15, 0.3), (0.1, 0.2)])
def test_sample_size_wald_matches_statsmodels_oracle(width, p0):
    ours = b.sample_size(width, p0=p0, method="wald")
    expected = math.ceil(samplesize_confint_proportion(p0, width / 2, alpha=0.05))
    assert ours == expected


# --- sample_size: the defining property, checked directly for every method --
@pytest.mark.parametrize(
    "method",
    ["wald", "wilson", "arcsine", "logit", "waldt", "lr", "exact", "midp", "bayes", "blaker"],
)
def test_sample_size_is_the_minimal_n(method):
    width, p0, alpha = 0.25, 0.5, 0.05
    # n_max kept well under ~26000: a pre-existing numerical bug in cilrx (the
    # LR method, unrelated to sample_size/power) makes its interval snap to
    # ~[0, 1] there -- discovered via this test, not yet fixed; see
    # planning/CONTINUE_HERE.md "Known issues". Every OTHER method reaches
    # width=0.25 at n well under 100, so this cap doesn't weaken their check.
    n = b.sample_size(width, alpha=alpha, p0=p0, method=method, n_max=5000)
    assert _width_at(method, n, alpha, p0) <= width
    assert _width_at(method, n - 1, alpha, p0) > width


def test_sample_size_monotone_in_width():
    # A tighter (smaller) target width needs a larger sample.
    n_loose = b.sample_size(0.3, method="wilson")
    n_tight = b.sample_size(0.1, method="wilson")
    assert n_tight > n_loose


def test_sample_size_monotone_in_p0_distance_from_half():
    # Width is worst (n needed is largest) planning around p0=0.5.
    n_half = b.sample_size(0.1, p0=0.5, method="wilson")
    n_extreme = b.sample_size(0.1, p0=0.1, method="wilson")
    assert n_half >= n_extreme


def test_sample_size_validation():
    with pytest.raises(ValueError):
        b.sample_size(0.1, method="boot")
    with pytest.raises(ValueError):
        b.sample_size(0.1, method="not-a-method")
    with pytest.raises(ValueError):
        b.sample_size(1.5, method="wilson")
    with pytest.raises(ValueError):
        b.sample_size(0.1, p0=1.5, method="wilson")
    with pytest.raises(ValueError):
        b.sample_size(1e-6, method="wilson", n_max=50)  # unreachable in 50


# --- power: independent brute-force cross-check ------------------------------
@pytest.mark.parametrize(
    "n,theta0,p_true,method",
    [(15, 0.4, 0.6, "wilson"), (20, 0.5, 0.5, "exact"), (10, 0.3, 0.8, "blaker")],
)
def test_power_matches_brute_force_over_reject(n, theta0, p_true, method):
    alpha = 0.05
    brute = sum(
        stats.binom.pmf(x, n, p_true) * b.reject(x, n, theta0, method=method, alpha=alpha)
        for x in range(n + 1)
    )
    fast = b.power(n, theta0, p_true, alpha=alpha, method=method)
    assert fast == pytest.approx(brute, abs=1e-9)


def test_power_at_p_true_equals_theta0_is_the_tests_size():
    # Power evaluated exactly at the null is the test's actual (possibly
    # discreteness-perturbed) size -- should sit close to nominal alpha.
    p = b.power(100, 0.5, 0.5, method="wilson", alpha=0.05)
    assert 0.02 < p < 0.10


def test_power_increases_with_effect_size():
    n, theta0 = 100, 0.5
    powers = [b.power(n, theta0, p, method="wilson") for p in [0.5, 0.55, 0.6, 0.65, 0.7]]
    assert all(p2 >= p1 for p1, p2 in zip(powers, powers[1:]))


def test_power_near_one_for_large_effect():
    assert b.power(50, 0.5, 0.99, method="wilson") > 0.999


def test_power_validation():
    with pytest.raises(ValueError):
        b.power(20, 0.5, 0.6, method="boot")
    with pytest.raises(ValueError):
        b.power(20, 1.5, 0.6, method="wilson")
    with pytest.raises(ValueError):
        b.power(20, 0.5, -0.1, method="wilson")


def test_no_pvalue_methods_blocked_consistently():
    # sample_size/power/pvalue/reject all share the same bootstrap exclusion.
    for m in _NO_PVALUE:
        with pytest.raises(ValueError):
            b.sample_size(0.1, method=m)
        with pytest.raises(ValueError):
            b.power(20, 0.5, 0.6, method=m)
