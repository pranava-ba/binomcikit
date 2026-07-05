"""Tests for the 2xx coverage-probability family (base methods).

These functions are simulation-based (5000 Beta draws), so exact equivalence to
R is impossible (different RNGs). We test statistical properties and structural
contracts instead, with a fixed seed for reproducibility.

R example (from man/covpWD.Rd): n=5; alp=0.05; a=1; b=1; t1=0.93; t2=0.97
"""
import pytest

import binomcikit as b

ARGS = dict(n=5, alp=0.05, a=1, b=1, t1=0.93, t2=0.97)
COLS = {"mcp", "micp", "RMSE_N", "RMSE_M", "RMSE_MI", "tol"}

BASE = {
    "wald": b.covpwd, "score": b.covpsc, "arcsine": b.covpas,
    "lr": b.covplr, "waldt": b.covptw, "logit": b.covplt,
}


@pytest.mark.parametrize("name", list(BASE))
def test_runs_and_has_columns(name):
    df = BASE[name](seed=0, **ARGS)
    assert len(df) == 1
    assert COLS.issubset(df.columns)


@pytest.mark.parametrize("name", list(BASE))
def test_coverage_is_a_probability(name):
    row = BASE[name](seed=0, **ARGS).iloc[0]
    assert 0.0 <= row["micp"] <= row["mcp"] <= 1.0
    assert 0.0 <= row["tol"] <= 100.0
    assert row["RMSE_N"] >= 0.0


def test_reproducible_with_seed():
    a = b.covpwd(seed=42, **ARGS).iloc[0]["mcp"]
    c = b.covpwd(seed=42, **ARGS).iloc[0]["mcp"]
    assert a == c


def test_wald_undercovers_relative_to_score():
    # Well-known statistical fact: the Wald interval under-covers compared to
    # the Score (Wilson) interval on average.
    wald = b.covpwd(seed=7, **ARGS).iloc[0]["mcp"]
    score = b.covpsc(seed=7, **ARGS).iloc[0]["mcp"]
    assert wald <= score + 1e-9


def test_covpall_has_six_methods():
    df = b.covpall(seed=0, **ARGS)
    assert set(df["method"]) == {
        "Wald", "ArcSine", "Likelihood", "Score", "Wald-T", "Logit-Wald"}


def test_bad_inputs_raise():
    with pytest.raises(ValueError):
        b.covpwd(n=5, alp=0.05, a=1, b=1, t1=0.97, t2=0.93)  # t1 > t2
    with pytest.raises(ValueError):
        b.covpwd(n=-1, alp=0.05, a=1, b=1, t1=0.93, t2=0.97)
    with pytest.raises(ValueError):
        b.covpwd(n=5, alp=0.05, a=-1, b=1, t1=0.93, t2=0.97)


# --------------------------------------------------------------------------- #
# Adjusted and continuity-corrected variants                                  #
# --------------------------------------------------------------------------- #
ADJ = {
    "wald": b.covpawd, "score": b.covpasc, "arcsine": b.covpaas,
    "lr": b.covpalr, "waldt": b.covpatw, "logit": b.covpalt,
}
CC = {
    "wald": b.covpcwd, "score": b.covpcsc, "arcsine": b.covpcas,
    "waldt": b.covpctw, "logit": b.covpclt,
}


@pytest.mark.parametrize("name", list(ADJ))
def test_adjusted_is_a_probability(name):
    row = ADJ[name](n=5, alp=0.05, h=2, a=1, b=1, t1=0.93, t2=0.97,
                    seed=0).iloc[0]
    assert COLS.issubset(row.index)
    assert 0.0 <= row["micp"] <= row["mcp"] <= 1.0


@pytest.mark.parametrize("name", list(CC))
def test_cc_is_a_probability(name):
    row = CC[name](n=5, alp=0.05, c=0.1, a=1, b=1, t1=0.93, t2=0.97,
                   seed=0).iloc[0]
    assert COLS.issubset(row.index)
    assert 0.0 <= row["micp"] <= row["mcp"] <= 1.0


def test_adjusted_wald_improves_coverage_over_plain_wald():
    # Adding pseudo-counts (h>0) is known to raise Wald coverage toward nominal.
    plain = b.covpwd(seed=1, **ARGS).iloc[0]["mcp"]
    adj = b.covpawd(n=5, alp=0.05, h=2, a=1, b=1, t1=0.93, t2=0.97,
                    seed=1).iloc[0]["mcp"]
    assert adj > plain


def test_covpaall_and_covpcall_method_sets():
    aall = b.covpaall(n=5, alp=0.05, h=2, a=1, b=1, t1=0.93, t2=0.97, seed=0)
    assert set(aall["method"]) == {
        "Wald", "ArcSine", "Likelihood", "Score", "Wald-T", "Logit-Wald"}
    call = b.covpcall(n=5, alp=0.05, c=0.1, a=1, b=1, t1=0.93, t2=0.97, seed=0)
    assert set(call["method"]) == {
        "Wald", "ArcSine", "Score", "Wald-T", "Logit-Wald"}  # no LR for CC


# --------------------------------------------------------------------------- #
# General (given / simulated p)                                               #
# --------------------------------------------------------------------------- #
def test_covpgen_matches_covpwd_on_same_hp():
    # covpwd is covpgen with the Wald limits and the same hp draws, so the
    # per-hp coverage — and thus mcp — must agree exactly.
    import numpy as np
    from binomcikit.covp.base_all import _coverage
    n, alp = 5, 0.05
    wd = b.ciwd(n, alp)
    hp = np.sort(np.random.default_rng(3).beta(1, 1, 200))
    gen = b.covpgen(n, wd["LWD"].values, wd["UWD"].values, alp, hp, 0.93, 0.97)
    # Recreate the same hp inside covpwd via the shared engine:
    direct = _coverage(n, alp, 1, 1, 0.93, 0.97, wd["LWD"], wd["UWD"],
                       seed=3, s=200)
    assert gen.iloc[0]["mcp"] == pytest.approx(direct.iloc[0]["mcp"], abs=1e-12)


def test_covpgen_validates_limit_length():
    with pytest.raises(ValueError):
        b.covpgen(5, [0, 0, 0], [1, 1, 1], 0.05, [0.5], 0.93, 0.97)


def test_covpsim_runs():
    wd = b.ciwd(5, 0.05)
    df = b.covpsim(5, wd["LWD"].values, wd["UWD"].values, 0.05, 500, 1, 1,
                   0.93, 0.97, seed=0)
    assert COLS.issubset(df.columns)


# --------------------------------------------------------------------------- #
# Plots construct without error                                               #
# --------------------------------------------------------------------------- #
def test_plots_construct():
    from plotnine import ggplot
    assert isinstance(b.plotcovpwd(seed=0, **ARGS), ggplot)
    assert isinstance(b.plotcovpall(seed=0, **ARGS), ggplot)
    assert isinstance(
        b.plotcovpawd(n=5, alp=0.05, h=2, a=1, b=1, t1=0.93, t2=0.97, seed=0),
        ggplot)
    assert isinstance(
        b.plotcovpcall(n=5, alp=0.05, c=0.1, a=1, b=1, t1=0.93, t2=0.97, seed=0),
        ggplot)
    wd = b.ciwd(5, 0.05)
    assert isinstance(
        b.plotcovpgen(5, wd["LWD"].values, wd["UWD"].values, 0.05,
                      [0.2, 0.5, 0.8], 0.93, 0.97), ggplot)


def test_exact_and_bayesian_coverage():
    # Exact interval coverage
    ex = b.covpex(5, 0.05, 0.5, 1, 1, 0.93, 0.97, seed=0).iloc[0]
    assert 0.0 <= ex["micp"] <= ex["mcp"] <= 1.0
    # Bayesian coverage reports both quantile and HPD intervals
    ba = b.covpba(5, 0.05, 1, 1, 0.93, 0.97, 0.5, 0.5, seed=0)
    assert set(ba["method"]) == {"Quantile", "HPD"}
    from plotnine import ggplot
    assert isinstance(
        b.plotcovpex(5, 0.05, 0.5, 1, 1, 0.93, 0.97, seed=0), ggplot)
    assert isinstance(
        b.plotcovpba(5, 0.05, 1, 1, 0.93, 0.97, 0.5, 0.5, seed=0), ggplot)
