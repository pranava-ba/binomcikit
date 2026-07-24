"""Tests for the 4xx p-confidence / p-bias family.

These quantities are deterministic (no simulation), so we can assert exact
golden values as well as structural and statistical properties.

R example (man/pCOpBIWD.Rd): n=5; alp=0.05
"""

import numpy as np
import pytest

import binomcikit as b

COLS = {"x1", "pconf", "pbias"}

BASE = {
    "wald": b.pcopbiwd,
    "score": b.pcopbisc,
    "arcsine": b.pcopbias,
    "lr": b.pcopbilr,
    "logit": b.pcopbilt,
    "waldt": b.pcopbitw,
}


@pytest.mark.parametrize("name", list(BASE))
def test_runs_shape_and_ranges(name):
    df = BASE[name](5, 0.05)
    assert COLS.issubset(df.columns)
    assert list(df["x1"]) == [1, 2, 3, 4]  # interior successes 1..n-1
    assert (df["pconf"] >= -1e-9).all() and (df["pconf"] <= 100 + 1e-9).all()
    assert (df["pbias"] >= -1e-9).all()


def test_wald_golden_values():
    # Deterministic reference (Wald, n=5, alp=0.05). Locks the tail/index
    # translation from R's pbinom(..., lower.tail=...) to scipy.
    df = b.pcopbiwd(5, 0.05)
    assert list(np.round(df["pconf"], 3)) == [73.878, 92.438, 92.438, 73.878]
    assert list(np.round(df["pbias"], 3)) == [26.122, 7.562, 7.562, 26.122]


def test_symmetric_method_is_palindromic():
    # Wald / Score / ArcSine are symmetric in x, so p-confidence read forwards
    # equals p-confidence read backwards.
    for fn in (b.pcopbiwd, b.pcopbisc, b.pcopbias):
        pconf = fn(20, 0.05)["pconf"].to_numpy()
        assert np.allclose(pconf, pconf[::-1])


def test_all_and_cc_method_sets():
    allm = b.pcopbiall(5, 0.05)
    assert set(allm["method"]) == {"Wald", "ArcSine", "Likelihood", "Score", "Wald-T", "Logit-Wald"}
    cc = b.pcopbicall(5, 0.05, 0.1)
    assert set(cc["method"]) == {"Wald", "ArcSine", "Score", "Wald-T", "Logit-Wald"}  # no LR


def test_exact_and_adjusted_run():
    assert COLS.issubset(b.pcopbiex(5, 0.05, 0.5).columns)
    assert COLS.issubset(b.pcopbiawd(5, 0.05, 2).columns)
    assert set(b.pcopbiaall(5, 0.05, 2)["method"]) == {
        "Wald",
        "ArcSine",
        "Likelihood",
        "Score",
        "Wald-T",
        "Logit-Wald",
    }


def test_general_matches_base_on_same_limits():
    # pcopbigen with the Wald limits must reproduce pcopbiwd exactly.
    n, alp = 8, 0.05
    wd = b.ciwd(n, alp)
    gen = b.pcopbigen(n, wd["LWD"].values, wd["UWD"].values)
    base = b.pcopbiwd(n, alp)
    assert np.allclose(gen["pconf"], base["pconf"])
    assert np.allclose(gen["pbias"], base["pbias"])


def test_plots_construct():
    from plotnine import ggplot

    wd = b.ciwd(5, 0.05)
    plots = [
        b.plotpcopbiwd(5, 0.05),
        b.plotpcopbiall(5, 0.05),
        b.plotpcopbiaall(5, 0.05, 2),
        b.plotpcopbicall(5, 0.05, 0.1),
        b.plotpcopbiex(5, 0.05, 0.5),
        b.plotpcopbigen(5, wd["LWD"].values, wd["UWD"].values),
    ]
    assert all(isinstance(p, ggplot) for p in plots)


def test_bad_inputs_raise():
    with pytest.raises(ValueError):
        b.pcopbiwd(-1, 0.05)
    with pytest.raises(ValueError):
        b.pcopbiwd(5, 1.5)
    with pytest.raises(ValueError):
        b.pcopbiawd(5, 0.05, -1)  # h < 0
    with pytest.raises(ValueError):
        b.pcopbigen(5, [0, 0, 0], [1, 1, 1])  # limits too short
