"""Property tests: the lean ``limits`` / ``interval`` paths must agree with the ``ci`` tables.

Three access paths compute the same interval -- ``bk.ci`` (labelled DataFrame), ``bk.limits``
(arrays) and ``bk.interval`` (one row). A regression in one of them (a vectorised kernel drifting
from its scalar twin, a clamp applied on one path only) shows up as a disagreement for some
``(n, alpha, method)``; random draws find those far better than hand-picked cases.
"""

import warnings

import numpy as np
import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

import binomcikit as bk

# methods with a lean kernel (limits) and a cheap table, at any n up to the sizes drawn below
CLASSIC = ["wald", "wilson", "agresti-coull", "arcsine", "logit", "exact", "midp", "jeffreys", "lr"]
# registry methods that are cheap enough to draw freely (the exact/betting family is checked separately)
CHEAP_EXTENDED = [
    "pratt",
    "cloglog",
    "probit",
    "modified-wilson",
    "modified-jeffreys",
    "poisson",
    "freeman-tukey",
    "hoeffding",
    "chernoff",
    "cressie-read",
    "lr-star",
    "score-cc",
    "arcsine-anscombe",
    "wald-i",
    "wald-recentred",
    "mixture",
]
ALPHAS = [0.01, 0.05, 0.1, 0.2]
SETTINGS = dict(
    max_examples=40, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture]
)


def _table_limits(df):
    cols = [c for c in df.columns if c[0] in "LU" and c not in ("LABB", "UABB")]
    return df[cols[0]].to_numpy(float), df[cols[1]].to_numpy(float)


@settings(**SETTINGS)
@given(n=st.integers(1, 60), alpha=st.sampled_from(ALPHAS), method=st.sampled_from(CLASSIC))
def test_limits_equal_ci_table(n, alpha, method):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        lo, hi = bk.limits(n, alpha, method)
        t_lo, t_hi = _table_limits(bk.ci(n=n, alpha=alpha, method=method))
    np.testing.assert_allclose(lo, t_lo, atol=1e-9, rtol=0)
    np.testing.assert_allclose(hi, t_hi, atol=1e-9, rtol=0)


@settings(**SETTINGS)
@given(
    n=st.integers(1, 60),
    alpha=st.sampled_from(ALPHAS),
    method=st.sampled_from(CLASSIC + CHEAP_EXTENDED),
    data=st.data(),
)
def test_interval_equals_limits_row(n, alpha, method, data):
    x = data.draw(st.integers(0, n))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        lo, hi = bk.limits(n, alpha, method)
        a, b = bk.interval(x, n, alpha, method)
    assert a == pytest.approx(lo[x], abs=1e-9)
    assert b == pytest.approx(hi[x], abs=1e-9)


@settings(**SETTINGS)
@given(
    n=st.integers(1, 60),
    alpha=st.sampled_from(ALPHAS),
    method=st.sampled_from(CLASSIC + CHEAP_EXTENDED),
)
def test_limits_are_ordered_and_inside_the_unit_interval(n, alpha, method):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        lo, hi = bk.limits(n, alpha, method)
    assert lo.shape == hi.shape == (n + 1,)
    assert np.all(np.isfinite(lo)) and np.all(np.isfinite(hi))
    assert np.all(lo >= 0) and np.all(hi <= 1)
    assert np.all(lo <= hi + 1e-12)


@settings(**SETTINGS)
@given(n=st.integers(1, 60), alpha=st.sampled_from(ALPHAS), method=st.sampled_from(CLASSIC))
def test_equivariance_under_swapping_successes_and_failures(n, alpha, method):
    """Symmetric methods satisfy L(x) = 1 - U(n - x); the likelihood and Wald family all do."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        lo, hi = bk.limits(n, alpha, method)
    np.testing.assert_allclose(lo, 1 - hi[::-1], atol=1e-9, rtol=0)
