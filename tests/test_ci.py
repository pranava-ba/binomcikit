"""Tests for the 1xx confidence-interval family.

Three kinds of checks, matching the porting strategy:

1. Numeric equivalence against an independent oracle (statsmodels) for the
   methods statsmodels also implements: Wald, Wilson (Score), Clopper-Pearson
   (Exact at e=1).
2. Smoke tests derived from the R package's @examples: every function runs and
   returns the documented columns.
3. Property tests: limits stay in [0, 1], lower <= upper, and the interval
   brackets the point estimate p-hat where the method guarantees it.
"""
import pytest
from statsmodels.stats.proportion import proportion_confint as sm_ci

import binomcikit as b

ALP = 0.05
TOL = 1e-9


# --------------------------------------------------------------------------- #
# 1. Numeric equivalence vs statsmodels                                       #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("n", [10, 50, 100])
def test_wald_matches_statsmodels(n):
    df = b.ciwd(n, ALP)
    for x in range(n + 1):
        lo, hi = sm_ci(x, n, alpha=ALP, method="normal")
        # statsmodels does not clamp; binomcikit clamps to [0, 1]
        assert df.LWD[x] == pytest.approx(max(lo, 0.0), abs=TOL)
        assert df.UWD[x] == pytest.approx(min(hi, 1.0), abs=TOL)


@pytest.mark.parametrize("n", [10, 50, 100])
def test_score_matches_statsmodels(n):
    df = b.cisc(n, ALP)
    for x in range(n + 1):
        lo, hi = sm_ci(x, n, alpha=ALP, method="wilson")
        assert df.LSC[x] == pytest.approx(lo, abs=1e-9)
        assert df.USC[x] == pytest.approx(hi, abs=1e-9)


@pytest.mark.parametrize("n", [10, 50])
def test_exact_e1_matches_clopper_pearson(n):
    df = b.ciex(n, ALP, [1])
    for x in range(n + 1):
        lo, hi = sm_ci(x, n, alpha=ALP, method="beta")
        assert df.LEX[x] == pytest.approx(lo, abs=1e-6)
        assert df.UEX[x] == pytest.approx(hi, abs=1e-6)


# --------------------------------------------------------------------------- #
# 2. Smoke tests from the R @examples                                         #
# --------------------------------------------------------------------------- #
N_METHODS_ALL = {  # (function for all-x, given-x function, x/e args)
    "wald": (b.ciwd, b.ciwdx, ("LWD", "UWD"), ("LWDx", "UWDx")),
    "score": (b.cisc, b.ciscx, ("LSC", "USC"), ("LSCx", "USCx")),
    "arcsine": (b.cias, b.ciasx, ("LAS", "UAS"), ("LASx", "UASx")),
    "lr": (b.cilr, b.cilrx, ("LLR", "ULR"), ("LLRx", "ULRx")),
    "logit": (b.cilt, b.ciltx, ("LLT", "ULT"), ("LLTx", "ULTx")),
    "waldt": (b.citw, b.citwx, ("LTW", "UTW"), ("LTWx", "UTWx")),
}


@pytest.mark.parametrize("name", list(N_METHODS_ALL))
def test_all_x_runs_and_has_columns(name):
    fn_all, _, (lo, hi), _ = N_METHODS_ALL[name]
    df = fn_all(5, ALP)  # R example: n=5; alp=0.05
    assert len(df) == 6  # x = 0..5
    for col in ("x", lo, hi, "LABB", "UABB", "ZWI"):
        assert col in df.columns


@pytest.mark.parametrize("name", list(N_METHODS_ALL))
def test_given_x_runs_and_has_columns(name):
    _, fn_x, _, (lo, hi) = N_METHODS_ALL[name]
    df = fn_x(3, 5, ALP)  # R example: x=3; n=5; alp=0.05
    assert len(df) == 1
    for col in ("x", lo, hi, "LABB", "UABB", "ZWI"):
        assert col in df.columns


def test_ciall_combines_six_methods():
    df = b.ciall(5, ALP)
    assert set(df["method"]) == {
        "Wald", "ArcSine", "Likelihood", "Score", "Wald-T", "Logit-Wald"}
    assert len(df) == 6 * 6  # 6 methods x (n+1)=6 rows


def test_ciallx_combines_six_methods():
    df = b.ciallx(2, 10, ALP)
    assert set(df["method"]) == {
        "Wald", "ArcSine", "Likelihood", "Score", "Wald-T", "Logit-Wald"}
    assert len(df) == 6


def test_exact_and_given_x():
    df = b.ciexx(2, 10, ALP, [0.1, 0.5, 1.0])
    assert list(df["e"]) == [0.1, 0.5, 1.0]
    assert {"LEXx", "UEXx"}.issubset(df.columns)


# --------------------------------------------------------------------------- #
# 3. Property tests                                                           #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("name", list(N_METHODS_ALL))
def test_limits_within_unit_interval(name):
    fn_all, _, (lo, hi), _ = N_METHODS_ALL[name]
    df = fn_all(20, ALP)
    assert (df[lo] >= -TOL).all()
    assert (df[hi] <= 1 + TOL).all()
    assert (df[hi] >= df[lo] - TOL).all()


def test_wald_brackets_phat_interior():
    n = 50
    df = b.ciwd(n, ALP)
    for x in range(1, n):  # interior points, no clamping
        phat = x / n
        assert df.LWD[x] <= phat <= df.UWD[x]


# --------------------------------------------------------------------------- #
# Input validation                                                            #
# --------------------------------------------------------------------------- #
def test_missing_and_bad_inputs_raise():
    with pytest.raises(ValueError):
        b.ciwd(None, ALP)
    with pytest.raises(ValueError):
        b.ciwd(5, None)
    with pytest.raises(ValueError):
        b.ciwd(5, 1.5)
    with pytest.raises(ValueError):
        b.ciwd(-1, ALP)
    with pytest.raises(ValueError):
        b.ciwdx(11, 10, ALP)  # x > n
