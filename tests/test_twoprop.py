"""Difference of two independent proportions: oracle, equation, property and coverage checks."""

import math
import warnings

import numpy as np
import pandas as pd
import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from scipy import stats

import binomcikit as bk
from binomcikit import twoprop

sm_prop = pytest.importorskip("statsmodels.stats.proportion")

TABLES = [
    (7, 10, 3, 12),
    (56, 70, 48, 80),
    (0, 10, 0, 10),
    (10, 10, 0, 10),
    (0, 20, 5, 20),
    (1, 30, 29, 30),
    (15, 15, 14, 15),
    (2, 5, 0, 7),
    (50, 100, 40, 100),
    (200, 1000, 150, 1200),
    (0, 1, 1, 1),
    (3, 4, 2, 3),
]
ALL = list(twoprop.list_diff_methods()["method"])


def _sm(method, t, alpha=0.05):
    lo, hi = sm_prop.confint_proportions_2indep(
        t[0], t[1], t[2], t[3], method=method, compare="diff", alpha=alpha
    )
    return max(lo, -1.0), min(hi, 1.0)


@pytest.mark.parametrize(
    "ours,theirs", [("wald", "wald"), ("agresti-caffo", "agresti-caffo"), ("newcombe", "newcomb")]
)
@pytest.mark.parametrize("alpha", [0.01, 0.05, 0.2])
def test_matches_statsmodels(ours, theirs, alpha):
    for t in TABLES:
        a = bk.diff_interval(*t, alpha, ours)
        b = _sm(theirs, t, alpha)
        assert a == pytest.approx(b, abs=1e-12), (ours, t)


def test_newcombe_cc_and_wald_cc_match_dbci():
    dbci = pytest.importorskip("diff_binom_confint")
    for method in ("wald-cc", "newcombe-cc"):
        for t in TABLES:
            r = dbci.compute_difference_confidence_interval(*t, 0.95, method)
            exp = (max(r.lower_bound, -1.0), min(r.upper_bound, 1.0))
            assert bk.diff_interval(*t, 0.05, method) == pytest.approx(exp, abs=1e-9), (method, t)


@pytest.mark.parametrize("method,mn", [("mee", False), ("miettinen-nurminen", True)])
def test_score_limits_solve_the_defining_equation(method, mn):
    """The score statistic equals z^2 at each interior limit (to root-finder precision)."""
    z = stats.norm.ppf(0.975)
    for t in TABLES:
        lo, hi = bk.diff_interval(*t, 0.05, method)
        factor = (t[1] + t[3]) / (t[1] + t[3] - 1) if mn else 1.0
        for lim in (lo, hi):
            if abs(lim) >= 1.0:  # boundary: the equation need not be met
                continue
            stat = twoprop._score_stat2(*t, lim, factor)
            assert stat == pytest.approx(z * z, abs=1e-8), (method, t, lim)


def test_known_values_for_one_table():
    """A regression anchor: five methods on 56/70 vs 48/80 (agree with statsmodels / DBCI)."""
    t = (56, 70, 48, 80)
    exp = {
        "wald": (0.0575, 0.3425),
        "newcombe": (0.0524, 0.3339),
        "newcombe-cc": (0.0428, 0.3422),
        "mee": (0.0533, 0.3377),
        "miettinen-nurminen": (0.0528, 0.3382),
    }
    for m, e in exp.items():
        assert bk.diff_interval(*t, 0.05, m) == pytest.approx(e, abs=5e-5), m


def test_aliases_and_catalogue():
    t = (7, 10, 3, 12)
    assert bk.diff_interval(*t, 0.05, "mn") == bk.diff_interval(*t, 0.05, "miettinen-nurminen")
    assert bk.diff_interval(*t, 0.05, "hybrid-score") == bk.diff_interval(*t, 0.05, "newcombe")
    cat = bk.list_diff_methods()
    assert isinstance(cat, pd.DataFrame) and {"wald", "newcombe", "mee"} <= set(ALL)
    assert len(cat) == 7


def test_diff_ci_table():
    df = bk.diff_ci(7, 10, 3, 12, 0.05, "newcombe")
    cols = ["method", "x1", "n1", "x2", "n2", "estimate", "lower", "upper", "width"]
    assert list(df.columns) == cols
    row = df.iloc[0]
    assert row["estimate"] == pytest.approx(7 / 10 - 3 / 12)
    assert row["width"] == pytest.approx(row["upper"] - row["lower"])


def test_array_inputs_broadcast():
    x1 = np.array([7, 56, 0])
    n1 = np.array([10, 70, 10])
    lo, hi = bk.diff_interval(x1, n1, 3, 12, 0.05, "newcombe")
    for i in range(3):
        s = bk.diff_interval(int(x1[i]), int(n1[i]), 3, 12, 0.05, "newcombe")
        assert (lo[i], hi[i]) == pytest.approx(s)


@pytest.mark.parametrize(
    "args",
    [
        dict(x1=-1, n1=10, x2=3, n2=12),
        dict(x1=11, n1=10, x2=3, n2=12),
        dict(x1=1, n1=0, x2=3, n2=12),
        dict(x1=1.5, n1=10, x2=3, n2=12),
        dict(x1=1, n1=10, x2=3, n2=12, alpha=0.0),
        dict(x1=1, n1=10, x2=3, n2=12, alpha=1.0),
        dict(x1=1, n1=10, x2=3, n2=12, method="nope"),
    ],
)
def test_input_errors(args):
    with pytest.raises(ValueError):
        bk.diff_interval(**args)


SETTINGS = dict(max_examples=60, deadline=None, suppress_health_check=[HealthCheck.too_slow])


@settings(**SETTINGS)
@given(
    n1=st.integers(1, 40),
    n2=st.integers(1, 40),
    alpha=st.sampled_from([0.01, 0.05, 0.2]),
    method=st.sampled_from(ALL),
    data=st.data(),
)
def test_interval_properties(n1, n2, alpha, method, data):
    x1 = data.draw(st.integers(0, n1))
    x2 = data.draw(st.integers(0, n2))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        lo, hi = bk.diff_interval(x1, n1, x2, n2, alpha, method)
        slo, shi = bk.diff_interval(x2, n2, x1, n1, alpha, method)
    assert -1.0 <= lo <= hi <= 1.0
    # swapping the samples negates the difference, so it mirrors the interval
    assert (slo, shi) == pytest.approx((-hi, -lo), abs=1e-9)
    d = x1 / n1 - x2 / n2
    if method not in ("wald", "wald-cc", "agresti-caffo"):  # these can exclude the estimate
        assert lo - 1e-9 <= d <= hi + 1e-9


@settings(**SETTINGS)
@given(
    n1=st.integers(2, 30),
    n2=st.integers(2, 30),
    method=st.sampled_from(ALL),
    data=st.data(),
)
def test_narrower_at_lower_confidence(n1, n2, method, data):
    x1 = data.draw(st.integers(0, n1))
    x2 = data.draw(st.integers(0, n2))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        a = bk.diff_interval(x1, n1, x2, n2, 0.2, method)
        b = bk.diff_interval(x1, n1, x2, n2, 0.01, method)
    assert b[0] <= a[0] + 1e-9 and a[1] <= b[1] + 1e-9


def _exact_coverage(method, n1, n2, p1, p2, alpha=0.05):
    pm1 = stats.binom.pmf(np.arange(n1 + 1), n1, p1)
    pm2 = stats.binom.pmf(np.arange(n2 + 1), n2, p2)
    delta = p1 - p2
    cov = 0.0
    for x1 in range(n1 + 1):
        for x2 in range(n2 + 1):
            lo, hi = bk.diff_interval(x1, n1, x2, n2, alpha, method)
            if lo - 1e-12 <= delta <= hi + 1e-12:
                cov += pm1[x1] * pm2[x2]
    return cov


@pytest.mark.parametrize("method", ["newcombe", "miettinen-nurminen", "mee", "agresti-caffo"])
def test_exact_coverage_is_near_nominal(method):
    """Average exact coverage over a small grid of (p1, p2) at n1 = n2 = 15 stays close to 95%."""
    grid = [(0.3, 0.2), (0.5, 0.5), (0.7, 0.4), (0.15, 0.1), (0.9, 0.8)]
    covs = [_exact_coverage(method, 15, 15, a, b) for a, b in grid]
    assert 0.92 <= float(np.mean(covs)) <= 0.99, (method, covs)
    assert min(covs) >= 0.88, (method, covs)


def test_wald_undercovers_more_than_newcombe():
    grid = [(0.3, 0.2), (0.15, 0.1), (0.9, 0.8)]
    wald = np.mean([_exact_coverage("wald", 15, 15, a, b) for a, b in grid])
    newc = np.mean([_exact_coverage("newcombe", 15, 15, a, b) for a, b in grid])
    assert newc > wald
    assert math.isfinite(wald)


@pytest.mark.parametrize("method,mn", [("mee", False), ("miettinen-nurminen", True)])
def test_score_methods_are_stable_at_large_n(method, mn):
    """No cliff at large n (the failure mode of the old likelihood-ratio code): the width shrinks like
    1/sqrt(n) and the limits still solve the defining equation."""
    z = stats.norm.ppf(0.975)
    widths = []
    for n in (1_000, 26_000, 1_000_000, 10_000_000):
        t = (int(0.3 * n), n, int(0.2 * n), n)
        lo, hi = bk.diff_interval(*t, 0.05, method)
        widths.append(hi - lo)
        factor = 2 * n / (2 * n - 1) if mn else 1.0
        for lim in (lo, hi):
            assert twoprop._score_stat2(*t, lim, factor) == pytest.approx(z * z, abs=1e-8)
    assert all(a > b for a, b in zip(widths, widths[1:]))
    # 1/sqrt(n): a 26x increase in n should shrink the width by about sqrt(26)
    assert widths[0] / widths[1] == pytest.approx(math.sqrt(26), rel=0.05)


def test_extreme_tables_at_large_n_do_not_fail():
    n = 1_000_000
    for t in [(0, n, 0, n), (n, n, 0, n), (0, n, n, n), (1, n, 0, n), (n, n, n - 1, n)]:
        for m in ALL:
            lo, hi = bk.diff_interval(*t, 0.05, m)
            assert -1.0 <= lo <= hi <= 1.0, (m, t)


# Published values (4 decimals): Newcombe (1998) Table II and SAS PROC FREQ output, as transcribed in the test data of
# the DBCI package (MIT licence). They are independent of every implementation compared in this repository. A blank
# entry in the source (a limit beyond +-1) is recorded here as the clipped bound.
PUBLISHED = [
    ((0, 10, 0, 10), "mee", -0.2775, 0.2775),
    ((0, 10, 0, 10), "miettinen-nurminen", -0.2879, 0.2879),
    ((0, 10, 0, 10), "newcombe", -0.2775, 0.2775),
    ((0, 10, 0, 10), "newcombe-cc", -0.3445, 0.3445),
    ((0, 10, 0, 10), "wald", 0.0, 0.0),
    ((0, 10, 0, 10), "wald-cc", -0.1, 0.1),
    ((0, 10, 0, 20), "mee", -0.1611, 0.2775),
    ((0, 10, 0, 20), "miettinen-nurminen", -0.1658, 0.2844),
    ((0, 10, 0, 20), "newcombe", -0.1611, 0.2775),
    ((0, 10, 0, 20), "newcombe-cc", -0.2005, 0.3445),
    ((0, 10, 0, 20), "wald", 0.0, 0.0),
    ((0, 10, 0, 20), "wald-cc", -0.075, 0.075),
    ((5, 56, 0, 29), "mee", -0.0313, 0.1926),
    ((5, 56, 0, 29), "miettinen-nurminen", -0.0326, 0.1933),
    ((5, 56, 0, 29), "newcombe", -0.0381, 0.1926),
    ((5, 56, 0, 29), "newcombe-cc", -0.0667, 0.2037),
    ((5, 56, 0, 29), "wald", 0.0146, 0.164),
    ((5, 56, 0, 29), "wald-cc", -0.0116, 0.1901),
    ((6, 7, 2, 7), "mee", 0.0544, 0.8478),
    ((6, 7, 2, 7), "miettinen-nurminen", 0.0342, 0.8534),
    ((6, 7, 2, 7), "newcombe", 0.0582, 0.8062),
    ((6, 7, 2, 7), "newcombe-cc", -0.029, 0.8423),
    ((6, 7, 2, 7), "wald", 0.1481, 0.9947),
    ((6, 7, 2, 7), "wald-cc", 0.0053, 1.0),
    ((9, 10, 3, 10), "agresti-caffo", 0.16, 0.84),
    ((9, 10, 3, 10), "mee", 0.1821, 0.837),
    ((9, 10, 3, 10), "miettinen-nurminen", 0.17, 0.8406),
    ((9, 10, 3, 10), "newcombe", 0.1705, 0.809),
    ((9, 10, 3, 10), "newcombe-cc", 0.1013, 0.8387),
    ((9, 10, 3, 10), "wald", 0.2605, 0.9395),
    ((9, 10, 3, 10), "wald-cc", 0.1605, 1.0),
    ((10, 10, 0, 10), "mee", 0.6777, 1.0),
    ((10, 10, 0, 10), "miettinen-nurminen", 0.6636, 1.0),
    ((10, 10, 0, 10), "newcombe", 0.6075, 1.0),
    ((10, 10, 0, 10), "newcombe-cc", 0.5128, 1.0),
    ((10, 10, 0, 10), "wald", 1.0, 1.0),
    ((10, 10, 0, 10), "wald-cc", 0.9, 1.0),
    ((10, 10, 0, 20), "agresti-caffo", 0.6922, 1.0),
    ((10, 10, 0, 20), "mee", 0.7225, 1.0),
    ((10, 10, 0, 20), "miettinen-nurminen", 0.7156, 1.0),
    ((10, 10, 0, 20), "newcombe", 0.6791, 1.0),
    ((10, 10, 0, 20), "newcombe-cc", 0.6014, 1.0),
    ((10, 10, 0, 20), "wald", 1.0, 1.0),
    ((10, 10, 0, 20), "wald-cc", 0.925, 1.0),
    ((56, 70, 48, 80), "agresti-caffo", 0.0525, 0.3358),
    ((56, 70, 48, 80), "mee", 0.0533, 0.3377),
    ((56, 70, 48, 80), "miettinen-nurminen", 0.0528, 0.3382),
    ((56, 70, 48, 80), "newcombe", 0.0524, 0.3339),
    ((56, 70, 48, 80), "newcombe-cc", 0.0428, 0.3422),
    ((56, 70, 48, 80), "wald", 0.0575, 0.3425),
    ((56, 70, 48, 80), "wald-cc", 0.0441, 0.3559),
    ((84, 101, 89, 105), "agresti-caffo", -0.1168, 0.085),
    ((84, 101, 89, 105), "mee", -0.1188, 0.0857),
    ((84, 101, 89, 105), "miettinen-nurminen", -0.1191, 0.086),
    ((84, 101, 89, 105), "newcombe", -0.1177, 0.0851),
    ((84, 101, 89, 105), "newcombe-cc", -0.1245, 0.0918),
    ((84, 101, 89, 105), "wald", -0.1162, 0.0843),
    ((84, 101, 89, 105), "wald-cc", -0.1259, 0.094),
]


@pytest.mark.parametrize("table,method,lo,hi", PUBLISHED)
def test_matches_published_tables(table, method, lo, hi):
    a, b = bk.diff_interval(*table, 0.05, method)
    assert a == pytest.approx(lo, abs=5.5e-5), (table, method)
    assert b == pytest.approx(hi, abs=5.5e-5), (table, method)
