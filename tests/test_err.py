"""Tests for the 5xx error-failure family.

Deterministic (no simulation), so golden values and exact cross-path checks are
possible.

R example (man/errWD.Rd): n=20; alp=0.05; phi=0.05; f=-2
"""
import numpy as np
import pytest

import binomcikit as b

COLS = {"delalp", "theta", "Fail_Pass"}

BASE = {
    "wald": b.errwd, "score": b.errsc, "arcsine": b.erras,
    "lr": b.errlr, "logit": b.errlt, "waldt": b.errtw,
}


@pytest.mark.parametrize("name", list(BASE))
def test_runs_shape_and_ranges(name):
    df = BASE[name](20, 0.05, 0.5, -2)
    assert len(df) == 1
    assert COLS.issubset(df.columns)
    row = df.iloc[0]
    assert 0.0 <= row["theta"] <= 100.0
    assert row["Fail_Pass"] in ("success", "failure")


def test_wald_golden_value():
    # Deterministic reference: R errWD(20, 0.05, 0.05, -2).
    row = b.errwd(20, 0.05, 0.05, -2).iloc[0]
    assert row["delalp"] == pytest.approx(-31.11, abs=0.01)
    assert row["theta"] == pytest.approx(80.95, abs=0.01)
    assert row["Fail_Pass"] == "failure"


def test_failpass_threshold_logic():
    # Fail_Pass is "failure" iff delalp < f. Pick f just above/below delalp.
    row = b.errwd(20, 0.05, 0.05, -2).iloc[0]
    d = row["delalp"]
    assert b.errwd(20, 0.05, 0.05, d - 1).iloc[0]["Fail_Pass"] == "success"
    assert b.errwd(20, 0.05, 0.05, d + 1).iloc[0]["Fail_Pass"] == "failure"


def test_all_and_cc_method_sets():
    allm = b.errall(20, 0.05, 0.5, -2)
    assert set(allm["method"]) == {
        "Wald", "ArcSine", "Likelihood", "Score", "Wald-T", "Logit-Wald"}
    cc = b.errcall(20, 0.05, 0.5, 0.02, -2)
    assert set(cc["method"]) == {
        "Wald", "ArcSine", "Score", "Wald-T", "Logit-Wald"}  # no LR


def test_exact_and_adjusted_run():
    assert COLS.issubset(b.errex(20, 0.05, 0.5, -2, 0.5).columns)
    assert COLS.issubset(b.errawd(20, 0.05, 2, 0.5, -2).columns)
    assert set(b.erraall(20, 0.05, 2, 0.5, -2)["method"]) == {
        "Wald", "ArcSine", "Likelihood", "Score", "Wald-T", "Logit-Wald"}


def test_general_matches_base_on_same_limits():
    n, alp, phi, f = 20, 0.05, 0.3, -2
    wd = b.ciwd(n, alp)
    gen = b.errgen(n, wd["LWD"].values, wd["UWD"].values, alp, phi, f).iloc[0]
    base = b.errwd(n, alp, phi, f).iloc[0]
    assert gen["delalp"] == pytest.approx(base["delalp"])
    assert gen["theta"] == pytest.approx(base["theta"])
    assert gen["Fail_Pass"] == base["Fail_Pass"]


def test_plots_construct():
    from plotnine import ggplot
    wd = b.ciwd(20, 0.05)
    plots = [
        b.ploterrwd(20, 0.05, 0.05, -2),
        b.ploterrall(20, 0.05, 0.5, -2),
        b.ploterraall(20, 0.05, 2, 0.5, -2),
        b.ploterrcall(20, 0.05, 0.5, 0.02, -2),
        b.ploterrex(20, 0.05, 0.5, -2, 0.5),
        b.ploterrgen(20, wd["LWD"].values, wd["UWD"].values, 0.05, 0.5, -2),
    ]
    assert all(isinstance(p, ggplot) for p in plots)


def test_bad_inputs_raise():
    with pytest.raises(ValueError):
        b.errwd(-1, 0.05, 0.5, -2)
    with pytest.raises(ValueError):
        b.errwd(20, 0.05, 1.5, -2)      # phi out of range
    with pytest.raises(ValueError):
        b.errawd(20, 0.05, -1, 0.5, -2)  # h < 0
    with pytest.raises(ValueError):
        b.errgen(20, [0, 0], [1, 1], 0.05, 0.5, -2)  # limits too short
