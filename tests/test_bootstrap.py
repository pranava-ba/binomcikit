"""Bootstrap CIs (``ciboot``/``cibootx``) -- new code in binomcikit, not part
of R ``proportion``. Two kinds, two different verification strategies:

* ``kind="percentile"``/``"bca"`` -- a thin wrapper around
  ``scipy.stats.bootstrap``, so it is checked to match scipy's own output
  exactly (an oracle, same rigor as every other method).
* ``kind="smooth"`` (Wang & Hutson 2013) -- no third-party oracle exists, so
  it is checked against: (1) the paper's own closed-form boundary formulas
  for the median-unbiased estimator (an independent identity, not a fit),
  (2) rough agreement with the oracle-verified percentile/BCa bootstrap away
  from the boundary, and (3) the specific property the method exists for --
  a non-degenerate interval at x = 0 / x = n, where the naive bootstrap
  collapses to zero width.
"""

import numpy as np
import pytest
import scipy.stats as stats
from cases import ALPHA

import binomcikit as b
from binomcikit.ci.bootstrap import _mue, _resample_ci, _smooth_ci

B_FAST = 400  # small B keeps the suite fast; not the library's own default (2000)


# --- median-unbiased estimator: an independent closed-form identity --------
@pytest.mark.parametrize("n", [5, 10, 20, 50])
def test_mue_matches_paper_boundary_formulas(n):
    # Wang & Hutson (2013) Eq. 8 special-cases x=0 and x=n explicitly;
    # our general two-sided-quantile formula must reduce to exactly those.
    assert _mue(0, n) == pytest.approx(0.5 * (1 - 0.5 ** (1 / n)))
    assert _mue(n, n) == pytest.approx(0.5 * (1 + 0.5 ** (1 / n)))


def test_mue_is_symmetric_and_monotone():
    n = 20
    vals = [_mue(x, n) for x in range(n + 1)]
    assert all(v1 < v2 for v1, v2 in zip(vals, vals[1:]))  # strictly increasing in x
    # symmetry: MUE(x) = 1 - MUE(n - x)
    for x in range(n + 1):
        assert _mue(x, n) == pytest.approx(1 - _mue(n - x, n), abs=1e-9)
    # never exactly 0 or 1 (the whole point -- keeps 1 - pihat safe downstream)
    assert 0 < vals[0] < 0.05
    assert 0.95 < vals[-1] < 1


# --- percentile / BCa: oracle is scipy.stats.bootstrap itself --------------
@pytest.mark.parametrize("x,n", [(3, 20), (1, 10), (15, 20)])
@pytest.mark.parametrize("method", ["percentile", "bca"])
def test_resample_ci_matches_scipy_oracle_exactly(x, n, method):
    rng1 = np.random.default_rng(7)
    lo, hi = _resample_ci(x, n, ALPHA, B_FAST, rng1, method)

    rng2 = np.random.default_rng(7)
    data = (np.concatenate([np.ones(x), np.zeros(n - x)]),)
    res = stats.bootstrap(
        data,
        np.mean,
        n_resamples=B_FAST,
        method=method,
        confidence_level=1 - ALPHA,
        random_state=rng2,
    )
    assert lo == pytest.approx(res.confidence_interval.low)
    assert hi == pytest.approx(res.confidence_interval.high)


@pytest.mark.parametrize("method", ["percentile", "bca"])
def test_naive_bootstrap_collapses_at_the_boundary(method):
    # The documented failure mode the smooth bootstrap exists to fix: every
    # resample of an all-0 (or all-1) sample is identical.
    rng = np.random.default_rng(1)
    assert _resample_ci(0, 20, ALPHA, B_FAST, rng, method) == (0.0, 0.0)
    assert _resample_ci(20, 20, ALPHA, B_FAST, rng, method) == (1.0, 1.0)


# --- smooth (Wang-Hutson): cross-checked, no direct oracle ------------------
def test_smooth_is_nondegenerate_at_the_boundary():
    # The property the whole method exists for: unlike percentile/BCa above,
    # x=0 and x=n get a real, non-zero-width interval.
    rng = np.random.default_rng(3)
    lo0, hi0 = _smooth_ci(0, 20, ALPHA, 2000, rng)
    assert hi0 - lo0 > 0.02
    rngn = np.random.default_rng(3)
    lon, hin = _smooth_ci(20, 20, ALPHA, 2000, rngn)
    assert hin - lon > 0.02


@pytest.mark.parametrize("x,n", [(5, 20), (10, 20), (15, 20)])
def test_smooth_roughly_agrees_with_percentile_away_from_boundary(x, n):
    # Not an exact match (different constructions), but the two should be in
    # the same ballpark at well-behaved (non-boundary) x -- a sanity check,
    # not proof of correctness on its own.
    rng_s = np.random.default_rng(11)
    lo_s, hi_s = _smooth_ci(x, n, ALPHA, 4000, rng_s)
    rng_p = np.random.default_rng(11)
    lo_p, hi_p = _resample_ci(x, n, ALPHA, 4000, rng_p, "percentile")
    assert lo_s == pytest.approx(lo_p, abs=0.12)
    assert hi_s == pytest.approx(hi_p, abs=0.12)


def test_smooth_ci_reproducible_with_same_seed():
    df1 = b.ciboot(15, ALPHA, B=B_FAST, seed=42, kind="smooth")
    df2 = b.ciboot(15, ALPHA, B=B_FAST, seed=42, kind="smooth")
    assert df1.equals(df2)


# --- shared structural properties (both kinds) ------------------------------
@pytest.mark.parametrize("kind", ["smooth", "percentile", "bca"])
def test_limits_in_unit_interval_and_ordered(kind):
    df = b.ciboot(20, ALPHA, B=B_FAST, seed=5, kind=kind)
    assert (df["LBOOT"] >= 0).all()
    assert (df["UBOOT"] <= 1).all()
    assert (df["LBOOT"] <= df["UBOOT"]).all()


def test_unknown_kind_raises():
    with pytest.raises(ValueError):
        b.ciboot(10, ALPHA, kind="nonsense")


def test_dispatch_and_base_only():
    df = b.ci(n=10, method="boot", B=B_FAST, seed=1)
    assert df.equals(b.ciboot(10, ALPHA, B=B_FAST, seed=1))
    dfx = b.ci(3, n=10, method="boot", B=B_FAST, seed=1)
    assert dfx.equals(b.cibootx(3, 10, ALPHA, B=B_FAST, seed=1))
    with pytest.raises(ValueError):  # base-only: no adjusted variant
        b.ci(n=10, method="boot", h=2)
    with pytest.raises(ValueError):  # base-only: no continuity-corrected variant
        b.ci(n=10, method="boot", c=0.5)


def test_inherits_metric_suite():
    # One limit-producer -> the whole diagnostic suite works with no extra code.
    assert b.covpboot(10, ALPHA, 1, 1, 0.93, 0.97, seed=1, B=B_FAST).shape[0] == 1
    assert len(b.lengthboot(10, ALPHA, 1, 1, seed=1, B=B_FAST)) >= 1
    assert len(b.pcopbiboot(10, ALPHA, seed=1, B=B_FAST)) == 9
    assert len(b.errboot(10, ALPHA, 0.05, 1, seed=1, B=B_FAST)) == 1


def test_point_estimate_mue_matches_bootstrap_module():
    assert b.point_estimate(3, 20, "mue") == pytest.approx(_mue(3, 20))
