"""Tests for the 3xx expected-length family.

Simulation-based, so we check structural contracts, statistical properties, and
cross-path equivalence rather than draw-for-draw equality with R.

R example (man/lengthWD.Rd): n=5; alp=0.05; a=1; b=1
"""
import pytest

import binomcikit as b

COLS = {"sumLen", "explMean", "explSD", "explMax", "explLL", "explUL"}

BASE = {
    "wald": b.lengthwd, "score": b.lengthsc, "arcsine": b.lengthas,
    "logit": b.lengthlt, "waldt": b.lengthtw, "lr": b.lengthlr,
}


@pytest.mark.parametrize("name", list(BASE))
def test_base_runs_and_columns(name):
    df = BASE[name](5, 0.05, 1, 1, seed=0)
    assert len(df) == 1
    assert COLS.issubset(df.columns)


@pytest.mark.parametrize("name", list(BASE))
def test_lengths_are_nonnegative_and_consistent(name):
    row = BASE[name](5, 0.05, 1, 1, seed=0).iloc[0]
    assert row["sumLen"] >= 0
    assert row["explMax"] >= row["explMean"]          # max >= mean
    assert row["explLL"] <= row["explMean"] <= row["explUL"]
    assert 0 <= row["explMean"] <= 1                  # a length on [0,1] scale


def test_sumlen_equals_sum_of_interval_widths():
    # sumLen must equal the deterministic sum of (U - L) over x, independent of
    # the random draws.
    n, alp = 10, 0.05
    wd = b.ciwd(n, alp)
    expected = float((wd["UWD"] - wd["LWD"]).sum())
    assert b.lengthwd(n, alp, 1, 1, seed=0).iloc[0]["sumLen"] == pytest.approx(expected)


def test_exact_and_all_and_general():
    assert COLS.issubset(b.lengthex(5, 0.05, 0.5, 1, 1, seed=0).columns)
    la = b.lengthall(5, 0.05, 1, 1, seed=0)
    assert set(la["method"]) == {
        "Wald", "ArcSine", "Likelihood", "Score", "Wald-T", "Logit-Wald"}
    lc = b.lengthcall(5, 0.05, 0.1, 1, 1, seed=0)
    assert set(lc["method"]) == {
        "Wald", "ArcSine", "Score", "Wald-T", "Logit-Wald"}  # no LR


def test_lengthgen_matches_lengthwd_on_same_hp():
    # lengthgen with the Wald limits and the same hp draws must reproduce
    # lengthwd's expected-length summary exactly.
    from binomcikit.expl.base_all import _beta_hp
    n, alp = 5, 0.05
    wd = b.ciwd(n, alp)
    hp = _beta_hp(1, 1, seed=11)
    gen = b.lengthgen(n, wd["LWD"].values, wd["UWD"].values, hp)
    direct = b.lengthwd(n, alp, 1, 1, seed=11)
    assert gen.iloc[0]["explMean"] == pytest.approx(
        direct.iloc[0]["explMean"], abs=1e-12)
    assert gen.iloc[0]["sumLen"] == pytest.approx(direct.iloc[0]["sumLen"])


def test_adjusted_and_cc_run():
    assert COLS.issubset(b.lengthawd(5, 0.05, 2, 1, 1, seed=0).columns)
    assert COLS.issubset(b.lengthcwd(5, 0.05, 0.1, 1, 1, seed=0).columns)
    assert set(b.lengthaall(5, 0.05, 2, 1, 1, seed=0)["method"]) == {
        "Wald", "ArcSine", "Likelihood", "Score", "Wald-T", "Logit-Wald"}


def test_expl_curves_have_expected_columns():
    curve = b.explall(5, 0.05, 1, 1, seed=0)
    assert {"hp", "ew", "method"}.issubset(curve.columns)
    assert (curve["ew"] >= 0).all()


def test_plots_construct():
    from plotnine import ggplot
    wd = b.ciwd(5, 0.05)
    plots = [
        b.plotexplall(5, 0.05, 1, 1, seed=0),
        b.plotexplaall(5, 0.05, 2, 1, 1, seed=0),
        b.plotexplcall(5, 0.05, 0.1, 1, 1, seed=0),
        b.plotexplwd(5, 0.05, 1, 1, seed=0),
        b.plotexplex(5, 0.05, 0.5, 1, 1, seed=0),
        b.plotlengthall(5, 0.05, 1, 1, seed=0),
        b.plotlengthwd(5, 0.05, 1, 1, seed=0),
        b.plotexplgen(5, wd["LWD"].values, wd["UWD"].values, [0.2, 0.5, 0.8]),
        b.plotlengthsim(5, wd["LWD"].values, wd["UWD"].values, 500, 1, 1, seed=0),
    ]
    assert all(isinstance(p, ggplot) for p in plots)


def test_bad_inputs_raise():
    with pytest.raises(ValueError):
        b.lengthwd(-1, 0.05, 1, 1)
    with pytest.raises(ValueError):
        b.lengthwd(5, 1.5, 1, 1)
    with pytest.raises(ValueError):
        b.lengthawd(5, 0.05, -1, 1, 1)  # h < 0
    with pytest.raises(ValueError):
        b.lengthgen(5, [0, 0, 0], [1, 1, 1], [0.5])  # wrong limit length
