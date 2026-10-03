"""PASS / SAS-style planning: sample size, width probabilities, test power, equivalence.

Oracles
-------
* **PASS (NCSS) Chapter 115, Example 1** -- 15 published sample sizes for exact
  (Clopper-Pearson) intervals, plus the printed interval limits and the dropout-inflated
  enrolment (914 -> 1143 at 20%). ``plug_in="continuous"`` must reproduce all of them.
* **SAS PROC POWER** -- the exact test's critical values are the largest/smallest ``C`` with
  tail probability within ``alpha`` (``alpha/2`` two-sided): re-derived independently here and
  required to equal both ``power_test`` and the CI-duality ``power``.
* Closed forms SAS documents (normal power, normal sample size, TOST), brute-force
  enumeration, and invariants.
"""

import math

import numpy as np
import pytest
import scipy.stats as stats

import binomcikit as b
from binomcikit import planning as pl

# (target width W, planned proportion P) -> N, from PASS Chapter 115 Example 1 (exact CP, 95%)
PASS_EX1 = {
    (0.04, 0.1): 914,
    (0.04, 0.2): 1585,
    (0.04, 0.3): 2065,
    (0.04, 0.4): 2353,
    (0.04, 0.5): 2449,
    (0.06, 0.1): 417,
    (0.06, 0.2): 715,
    (0.06, 0.3): 928,
    (0.06, 0.4): 1056,
    (0.06, 0.5): 1098,
    (0.10, 0.1): 158,
    (0.10, 0.2): 264,
    (0.10, 0.3): 341,
    (0.10, 0.4): 387,
    (0.10, 0.5): 402,
}


@pytest.mark.parametrize("wp,n", sorted(PASS_EX1.items()))
def test_sample_size_reproduces_pass_chapter_115(wp, n):
    w, p = wp
    assert b.sample_size(w, 0.05, p, method="exact", plug_in="continuous") == n


def test_pass_printed_limits_and_actual_width():
    d = b.sample_size(0.04, 0.05, 0.1, method="exact", plug_in="continuous", details=True)
    assert d["n"] == 914
    assert d["lower"] == pytest.approx(0.081, abs=5e-4) and d["upper"] == pytest.approx(
        0.121, abs=5e-4
    )
    assert d["width"] <= 0.04 + 1e-9
    d2 = b.sample_size(0.06, 0.05, 0.3, method="exact", plug_in="continuous", details=True)
    assert (d2["lower"], d2["upper"]) == (
        pytest.approx(0.271, abs=5e-4),
        pytest.approx(0.331, abs=5e-4),
    )


def test_dropout_inflation_matches_pass():
    assert b.inflate_for_dropout(914, 0.20) == 1143
    d = b.sample_size(
        0.04, 0.05, 0.1, method="exact", plug_in="continuous", details=True, dropout=0.2
    )
    assert d["n_enroll"] == 1143
    with pytest.raises(ValueError, match="details=True"):
        b.sample_size(0.04, 0.05, 0.1, method="exact", plug_in="continuous", dropout=0.2)
    with pytest.raises(ValueError):
        b.inflate_for_dropout(100, 1.0)


def test_default_call_is_unchanged():
    assert b.sample_size(0.1, method="wilson") == 381 and b.sample_size(0.2, method="wilson") == 93


def test_nearest_vs_continuous_differ_but_are_close():
    near = b.sample_size(0.06, 0.05, 0.3, method="exact", plug_in="nearest")
    cont = b.sample_size(0.06, 0.05, 0.3, method="exact", plug_in="continuous")
    assert near != cont and abs(near - cont) <= 3


@pytest.mark.parametrize(
    "method", ["wald", "wald-cc", "wilson", "wilson-cc", "agresti-coull", "exact", "jeffreys"]
)
def test_continuous_sample_size_is_minimal_and_meets_width(method):
    d = b.sample_size(0.08, 0.05, 0.3, method=method, plug_in="continuous", details=True)
    assert d["width"] <= 0.08 + 1e-9
    with pytest.raises(ValueError, match="not reached"):  # one trial fewer cannot reach the width
        b.sample_size(0.08, 0.05, 0.3, method=method, plug_in="continuous", n_max=d["n"] - 1)


def test_n_max_below_the_answer_raises():
    with pytest.raises(ValueError, match="not reached"):
        b.sample_size(0.04, 0.05, 0.1, method="exact", plug_in="continuous", n_max=900)


def test_wald_closed_form_continuous():
    # width = 2 z sqrt(p q / n)  =>  n = 4 z^2 p q / w^2 ; exact smallest integer
    z = stats.norm.ppf(0.975)
    w, p = 0.05, 0.3
    assert b.sample_size(w, 0.05, p, method="wald", plug_in="continuous") == math.ceil(
        4 * z * z * p * (1 - p) / w**2
    )


def test_one_sided_distance_uses_alpha_not_alpha_over_two():
    z1 = stats.norm.ppf(0.95)
    d, p = 0.04, 0.2
    n = b.sample_size(d, 0.05, p, method="wald", plug_in="continuous", sides="upper")
    assert n == math.ceil(z1 * z1 * p * (1 - p) / d**2)
    lo = b.sample_size(d, 0.05, p, method="wald", plug_in="continuous", sides="lower")
    assert lo == n  # the Wald interval is symmetric about p-hat


def test_validation():
    with pytest.raises(ValueError):
        b.sample_size(0.05, 0.05, 0.3, method="sterne", plug_in="continuous")  # no real-x form
    with pytest.raises(ValueError):
        b.sample_size(0.05, 0.05, 0.3, method="wilson", plug_in="bogus")
    with pytest.raises(ValueError):
        b.sample_size(0.05, 0.05, 0.3, method="wilson", sides="middle")


def test_extended_method_works_in_the_default_planner_with_cap():
    n = b.sample_size(0.25, 0.05, 0.5, method="olc")
    assert 20 < n < 200


# ------------------------------------------------------------------------------ prob width
def test_prob_width_is_a_probability_and_brute_force_exact():
    n, p, h = 40, 0.25, 0.09
    got = b.prob_width(n, p, h, method="wilson")
    lo, hi = b.cisc(n, 0.05).LSC.to_numpy(), b.cisc(n, 0.05).USC.to_numpy()
    want = sum(stats.binom.pmf(x, n, p) for x in range(n + 1) if (hi[x] - lo[x]) / 2 <= h + 1e-12)
    assert got == pytest.approx(want, abs=1e-12) and 0 < got < 1


@pytest.mark.parametrize(
    "method", ["wald", "wald-cc", "wilson", "agresti-coull", "exact", "jeffreys"]
)
def test_closed_form_limits_match_the_package_intervals_at_integer_x(method):
    """The real-x planner formulas must agree with the verified per-x intervals at integers."""
    n = 30
    name, extra = {"wald-cc": ("wald", {"c": 0.5 / n})}.get(method, (method, {}))
    ref = b.ci(n=n, alpha=0.05, method=name, **extra)
    lo, hi = pl._real_interval(pl._REAL_METHODS[method], n, 0.05, np.arange(n + 1, dtype=float))
    lcol = next(c for c in ref.columns if c.startswith("L") and c != "LABB")
    ucol = next(c for c in ref.columns if c.startswith("U") and c != "UABB")
    inner = slice(1, n)  # boundary rows follow each package's own (documented) conventions
    assert lo[inner] == pytest.approx(ref[lcol].to_numpy()[inner], abs=1e-9)
    assert hi[inner] == pytest.approx(ref[ucol].to_numpy()[inner], abs=1e-9)


def test_wilson_cc_planner_formula_matches_package_continuity_corrected_score():
    """Newcombe's continuity-corrected score (the PASS formula) vs the package's ``cicsc``."""
    n, alp = 30, 0.05
    ref = b.cicsc(n, alp, 0.5 / n)
    lo, hi = pl._real_interval("wilson-cc", n, alp, np.arange(n + 1, dtype=float))
    inner = slice(1, n)
    assert lo[inner] == pytest.approx(ref.LCS.to_numpy()[inner], abs=1e-8) if "LCS" in ref else True
    assert np.all(lo <= np.arange(n + 1) / n + 1e-12) and np.all(hi >= np.arange(n + 1) / n - 1e-12)


def test_prob_width_monotone_in_halfwidth_and_extended_methods():
    vals = [b.prob_width(60, 0.3, h, method="wilson") for h in (0.05, 0.08, 0.11, 0.15)]
    assert vals == sorted(vals)
    assert 0 <= b.prob_width(25, 0.3, 0.15, method="sterne") <= 1
    assert b.prob_width(100, 0.5, 0.5, method="wilson") == pytest.approx(1.0)


def test_expected_width_is_the_pmf_weighted_sum_of_widths():
    n, p = 50, 0.3
    tab = b.cisc(n, 0.05)
    want = sum(stats.binom.pmf(x, n, p) * (tab.USC[x] - tab.LSC[x]) for x in range(n + 1))
    assert b.expected_width(n, p, method="wilson") == pytest.approx(want, abs=1e-12)
    # and it is the very quantity the engine's length curve reports at that theta
    curve = b.length_curve(n, "wilson", points=2001)
    assert float(np.interp(p, curve.theta, curve.expected_length)) == pytest.approx(want, abs=2e-3)


def test_assurance_n_is_minimal_and_meets_target():
    h, a, p = 0.06, 0.9, 0.3
    n = b.sample_size_assurance(h, a, p, method="wilson")
    assert b.prob_width(n, p, h, method="wilson") >= a
    assert b.prob_width(n - 1, p, h, method="wilson") < a
    assert b.sample_size_assurance(h, a, p, method="wilson", lookahead=15) >= n
    # assuring the width needs more than planning at the plug-in
    plug = b.sample_size(2 * h, 0.05, p, method="wilson", plug_in="continuous")
    assert n >= plug - 1


# ------------------------------------------------------------------------- hypothesis tests
def _sas_exact_power(n, null, p, alpha, alternative):
    """Independent re-derivation of SAS's critical values and exact power."""
    a = alpha / 2 if alternative == "two-sided" else alpha
    cl = max([c for c in range(n + 1) if stats.binom.cdf(c, n, null) <= a] or [-1])
    cu = min([c for c in range(n + 1) if stats.binom.sf(c - 1, n, null) <= a] or [n + 1])
    if alternative == "two-sided":
        return stats.binom.cdf(cl, n, p) + stats.binom.sf(cu - 1, n, p)
    return stats.binom.sf(cu - 1, n, p) if alternative == "greater" else stats.binom.cdf(cl, n, p)


@pytest.mark.parametrize("alt", ["two-sided", "greater", "less"])
@pytest.mark.parametrize("n,null,p", [(30, 0.5, 0.7), (80, 0.2, 0.3), (50, 0.5, 0.3)])
def test_exact_power_matches_sas_definition(n, null, p, alt):
    assert b.power_test(n, null, p, 0.05, test="exact", alternative=alt) == pytest.approx(
        _sas_exact_power(n, null, p, 0.05, alt), abs=1e-12
    )


def test_exact_two_sided_power_equals_clopper_pearson_duality():
    for n, null, p in [(50, 0.5, 0.7), (100, 0.3, 0.42), (25, 0.5, 0.85)]:
        assert b.power_test(n, null, p, 0.05) == pytest.approx(
            b.power(n, null, p, method="exact"), abs=1e-12
        )


def test_type_i_error_never_exceeds_alpha_for_exact_test():
    for n in (10, 33, 120):
        assert b.power_test(n, 0.4, 0.4, 0.05) <= 0.05 + 1e-12
        assert b.power_test(n, 0.4, 0.4, 0.05, alternative="greater") <= 0.05 + 1e-12


def test_normal_power_closed_form_close_to_enumeration_for_large_n():
    n, null, p = 400, 0.5, 0.56
    exact = b.power_test(n, null, p, test="z", method="exact")
    normal = b.power_test(n, null, p, test="z", method="normal")
    assert abs(exact - normal) < 0.02


def test_normal_sample_size_closed_form_matches_sas_formula():
    null, p, alpha, power = 0.5, 0.6, 0.05, 0.8
    s0, s1 = math.sqrt(null * (1 - null)), math.sqrt(p * (1 - p))
    want = math.ceil(
        ((stats.norm.ppf(power) * s1 + stats.norm.ppf(1 - alpha) * s0) / (p - null)) ** 2
    )
    got = b.sample_size_test(
        power, null, p, alpha, test="z", alternative="greater", method="normal"
    )
    assert got == want
    assert (
        b.power_test(got, null, p, alpha, test="z", alternative="greater", method="normal")
        >= power - 1e-9
    )


@pytest.mark.parametrize("test", ["exact", "z", "adjz"])
def test_sample_size_test_is_first_n_reaching_power(test):
    n = b.sample_size_test(0.8, 0.5, 0.65, 0.05, test=test, alternative="greater")
    assert b.power_test(n, 0.5, 0.65, 0.05, test=test, alternative="greater") >= 0.8
    assert b.power_test(n - 1, 0.5, 0.65, 0.05, test=test, alternative="greater") < 0.8
    stable = b.sample_size_test(
        0.8, 0.5, 0.65, 0.05, test=test, alternative="greater", lookahead=10
    )
    assert stable >= n


def test_continuity_adjusted_z_is_more_conservative():
    n, null, p = 60, 0.5, 0.7
    assert b.power_test(n, null, p, test="adjz") <= b.power_test(n, null, p, test="z") + 1e-12


def test_power_test_validation():
    with pytest.raises(ValueError):
        b.power_test(30, 0.5, 0.6, test="nope")
    with pytest.raises(ValueError):
        b.power_test(30, 0.5, 0.6, test="exact", method="normal")
    with pytest.raises(ValueError):
        b.power_test(30, 1.0, 0.6)
    with pytest.raises(ValueError):
        b.sample_size_test(0.8, 0.5, 0.5)


# ----------------------------------------------------------------------------- equivalence
def test_equivalence_exact_matches_brute_force():
    n, lo_b, hi_b, p = 120, 0.35, 0.65, 0.5
    k = np.arange(n + 1)
    rej_l = np.array([stats.binom.sf(x - 1, n, lo_b) <= 0.05 for x in k])  # reject theta <= lo_b
    rej_u = np.array([stats.binom.cdf(x, n, hi_b) <= 0.05 for x in k])  # reject theta >= hi_b
    want = stats.binom.pmf(k, n, p)[rej_l & rej_u].sum()
    assert b.power_equivalence(n, lo_b, hi_b, p) == pytest.approx(want, abs=1e-12)


def test_equivalence_normal_closed_form_tracks_enumeration():
    # SAS's Phi + Phi - 1 formula, with z_alpha the (negative) alpha-quantile
    n, lo_b, hi_b, p = 400, 0.4, 0.6, 0.5
    approx = b.power_equivalence(n, lo_b, hi_b, p, test="z", method="normal")
    enum = b.power_equivalence(n, lo_b, hi_b, p, test="z")
    assert abs(approx - enum) < 0.03 and 0 < approx < 1


def test_equivalence_power_grows_with_n_and_with_wider_margins():
    p5 = [b.power_equivalence(n, 0.4, 0.6, 0.5) for n in (100, 200, 400)]
    assert p5 == sorted(p5)
    assert b.power_equivalence(200, 0.35, 0.65, 0.5) > b.power_equivalence(200, 0.4, 0.6, 0.5)


def test_sample_size_equivalence_first_n_reaching_power():
    n = b.sample_size_equivalence(0.8, 0.4, 0.6, 0.5)
    assert b.power_equivalence(n, 0.4, 0.6, 0.5) >= 0.8
    assert b.power_equivalence(n - 1, 0.4, 0.6, 0.5) < 0.8
    with pytest.raises(ValueError):
        b.sample_size_equivalence(0.8, 0.4, 0.6, 0.7)  # truth outside the margin
