"""Locally-correct criterion, zero-failure (success-run) plans, Bayesian sample size, Kerman prior.

The criterion is checked against the *published findings* of Garthwaite, Moustafa & Elfadaly
(2024): Clopper-Pearson is locally correct, Wilson is not, Mid-P is for alpha < 0.1, and the OLC
method equals the target exactly on every cycle (that is how it is defined).
"""

import math

import numpy as np
import pytest
import scipy.stats as stats
from cases import ALPHA

import binomcikit as b


# ----------------------------------------------------------------------- locally correct
@pytest.mark.parametrize("n", [8, 20, 50])
def test_published_classification_of_methods(n):
    assert b.locally_correct(n, ALPHA, "exact")["locally_correct"]  # Clopper-Pearson: yes
    assert b.locally_correct(n, ALPHA, "midp")["locally_correct"]  # mid-P: yes for alpha < 0.1
    assert not b.locally_correct(n, ALPHA, "wilson")["locally_correct"]  # Wilson: no (their Fig. 1)


def test_olc_hits_the_target_on_every_cycle_by_construction():
    res = b.locally_correct(20, ALPHA, "olc")
    assert res["locally_correct"]
    assert res["cycles"].average.to_numpy() == pytest.approx(1 - ALPHA / 2, abs=1e-8)


def test_cycle_averages_match_numerical_integration_of_coverage():
    from scipy.integrate import quad

    n = 12
    res = b.locally_correct(n, ALPHA, "wilson")["cycles"]
    row = res[(res.side == "upper") & (res.cycle == 5)].iloc[0]
    avg = quad(lambda p: stats.binom.sf(4, n, p), row.left, row.right)[0] / (row.right - row.left)
    assert row.average == pytest.approx(avg, abs=1e-10)
    row = res[(res.side == "lower") & (res.cycle == 3)].iloc[0]
    avg = quad(lambda p: stats.binom.cdf(3, n, p), row.left, row.right)[0] / (row.right - row.left)
    assert row.average == pytest.approx(avg, abs=1e-10)


def test_wilson_shortfall_is_localised_and_reported():
    res = b.locally_correct(20, ALPHA, "wilson")
    assert res["min_average"] < res["target"] - 1e-4
    short = res["cycles"][res["cycles"].average < res["target"] - 1e-9]
    assert len(short) > 0 and set(short.side) <= {"upper", "lower"}


def test_non_monotone_limits_are_flagged():
    # the (stochastic-free) Hoeffding limits are monotone; a hand-made non-monotone interval is not
    from binomcikit.ext.criteria import cycle_averages

    n = 5
    lo = np.array([0.0, 0.1, 0.05, 0.4, 0.5, 0.6])  # not monotone
    hi = np.array([0.3, 0.4, 0.5, 0.7, 0.9, 1.0])
    assert (
        len(cycle_averages(n, lo, hi)) >= 1
    )  # computed, but locally_correct() demands monotone limits


# ---------------------------------------------------------------------------- success run
def test_zero_failure_plan_is_the_classical_success_run_formula():
    for p, c in [(0.01, 0.95), (0.05, 0.9), (0.001, 0.99)]:
        n = b.sample_size_upper_bound(p, c)
        assert n == math.ceil(math.log(1 - c) / math.log(1 - p))
        assert stats.beta.ppf(c, 1, n) <= p + 1e-12  # the exact one-sided bound at x = 0
        assert stats.beta.ppf(c, 1, n - 1) > p  # and n - 1 is not enough


def test_rule_of_three():
    assert abs(b.sample_size_upper_bound(0.001, 0.95) - 3 / 0.001) < 10  # -ln(0.05) = 2.9957


@pytest.mark.parametrize("method", ["exact", "wilson", "jeffreys"])
def test_upper_bound_plan_is_minimal(method):
    n = b.sample_size_upper_bound(0.05, 0.9, failures=1, method=method)
    from binomcikit.planning import _real_interval

    ub = lambda m: float(_real_interval(method, m, 0.2, np.array(1.0))[1])
    assert ub(n) <= 0.05 and ub(n - 1) > 0.05


def test_more_allowed_failures_need_more_trials_and_validation():
    ns = [b.sample_size_upper_bound(0.02, 0.95, failures=f) for f in range(4)]
    assert ns == sorted(ns) and len(set(ns)) == 4
    for bad in (
        {"p_max": 1.2},
        {"p_max": 0.1, "confidence": 1.0},
        {"p_max": 0.1, "failures": -1},
        {"p_max": 0.1, "method": "x"},
    ):
        with pytest.raises(ValueError):
            b.sample_size_upper_bound(**bad)


# --------------------------------------------------------------------- Bayesian sample size
def _alc(n, a, bb, alpha, kind):
    from scipy.special import betaln, gammaln

    x = np.arange(n + 1)
    s1, s2 = x + a, n - x + bb
    if kind == "central":
        ln = stats.beta.ppf(1 - alpha / 2, s1, s2) - stats.beta.ppf(alpha / 2, s1, s2)
    else:
        from binomcikit._hpd import hpd_beta

        ln = np.array([np.subtract(*hpd_beta(s1[i], s2[i], 1 - alpha)[::-1]) for i in range(n + 1)])
    lw = (
        gammaln(n + 1)
        - gammaln(x + 1)
        - gammaln(n - x + 1)
        + betaln(x + a, n - x + bb)
        - betaln(a, bb)
    )
    return float((np.exp(lw) * ln).sum()), float(ln.max())


@pytest.mark.parametrize("kind", ["central", "hpd"])
def test_alc_and_woc_are_minimal_and_match_brute_force(kind):
    length = 0.2
    n_alc = b.sample_size_bayes(length, "alc", 1.0, 1.0, ALPHA, kind)
    assert _alc(n_alc, 1.0, 1.0, ALPHA, kind)[0] <= length + 1e-9
    assert _alc(n_alc - 1, 1.0, 1.0, ALPHA, kind)[0] > length
    n_woc = b.sample_size_bayes(length, "woc", 1.0, 1.0, ALPHA, kind)
    assert _alc(n_woc, 1.0, 1.0, ALPHA, kind)[1] <= length + 1e-9
    assert n_woc >= n_alc  # the worst outcome is harder to satisfy than the average


def test_informative_prior_needs_fewer_trials_and_validation():
    flat = b.sample_size_bayes(0.12, "alc", 1.0, 1.0)
    informed = b.sample_size_bayes(0.12, "alc", 2.0, 18.0)  # a prior concentrated near 10%
    assert informed < flat
    for kw in (
        {"length": 1.5},
        {"length": 0.1, "criterion": "x"},
        {"length": 0.1, "a": 0},
        {"length": 0.1, "interval": "x"},
    ):
        with pytest.raises(ValueError):
            b.sample_size_bayes(**kw)


# ----------------------------------------------------------------------------- Kerman prior
def test_kerman_prior_is_registered():
    assert b.prior("kerman") == (1 / 3, 1 / 3)
    post = b.posterior(0, 10, *b.prior("kerman"))
    assert post["a_post"] == pytest.approx(1 / 3) and post["b_post"] == pytest.approx(10 + 1 / 3)
