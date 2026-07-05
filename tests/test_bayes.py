"""Tests for the 6xx Bayesian family (plus ciba/cibax in the ci family and the
Bayesian variants of 3xx/4xx/5xx).

The credible-interval and posterior/predictive quantities are deterministic, so
we can assert exact and golden values; empirical Bayes involves an optimisation
but is still deterministic.
"""
import numpy as np
import pytest

import binomcikit as b


# --------------------------------------------------------------------------- #
# ciba / cibax (Bayesian credible interval, lives in the ci family)           #
# --------------------------------------------------------------------------- #
def test_ciba_columns_and_posterior_mean():
    df = b.ciba(5, 0.05, 1, 1)
    assert list(df.columns) == ['x', 'pomean', 'LBAQ', 'UBAQ', 'LBAH', 'UBAH']
    # posterior mean = (x + a) / (n + a + b)
    n, a, bp = 5, 1, 1
    expected = (df['x'] + a) / (n + a + bp)
    assert np.allclose(df['pomean'], expected)


def test_hpd_never_wider_than_quantile():
    df = b.ciba(20, 0.05, 0.5, 0.5)
    q = df['UBAQ'] - df['LBAQ']
    h = df['UBAH'] - df['LBAH']
    assert (h <= q + 1e-9).all()


def test_ciba_symmetric_prior_is_mirror():
    df = b.ciba(10, 0.05, 1, 1)
    # With a symmetric Beta(1,1) prior, lower limit at x mirrors upper at n-x.
    assert np.allclose(df['LBAQ'].values, (1 - df['UBAQ'].values)[::-1])


def test_cibax_matches_ciba_row():
    full = b.ciba(10, 0.05, 1, 1)
    one = b.cibax(3, 10, 0.05, 1, 1).iloc[0]
    assert one['LBAQx'] == pytest.approx(full['LBAQ'][3])
    assert one['UBAHx'] == pytest.approx(full['UBAH'][3])


# --------------------------------------------------------------------------- #
# Posterior probabilities                                                     #
# --------------------------------------------------------------------------- #
def test_probpos_decreasing_and_bounded():
    df = b.probpos(10, 1, 1, 0.5)
    assert (df['PosProb'] >= 0).all() and (df['PosProb'] <= 1).all()
    assert (np.diff(df['PosProb']) <= 1e-12).all()  # non-increasing in x


def test_probposx_matches_probpos():
    full = b.probpos(8, 2, 3, 0.4)
    one = b.probposx(5, 8, 2, 3, 0.4).iloc[0]['PosProb']
    assert one == pytest.approx(full['PosProb'][5])


# --------------------------------------------------------------------------- #
# Posterior predictive                                                        #
# --------------------------------------------------------------------------- #
def test_probpre_columns_are_proper_distributions():
    df = b.probpre(4, 3, 1, 1)
    # For each past x (column), predictive prob over xnew must sum to 1.
    for col in [str(i) for i in range(5)]:
        assert df[col].sum() == pytest.approx(1.0)


def test_probprex_matches_probpre_cell():
    full = b.probpre(6, 4, 1, 1)
    cell = b.probprex(2, 6, 1, 4, 1, 1).iloc[0]['preprb']
    assert cell == pytest.approx(full.loc[full['xnew'] == 1, '2'].iloc[0])


# --------------------------------------------------------------------------- #
# Empirical Bayes                                                             #
# --------------------------------------------------------------------------- #
def test_empiricalba_shape_and_hpd():
    df = b.empiricalba(5, 0.05, 0.1, 10)
    assert list(df.columns) == ['x', 'pomean', 'LEBAQ', 'UEBAQ', 'LEBAH', 'UEBAH']
    assert ((df['UEBAH'] - df['LEBAH']) <= (df['UEBAQ'] - df['LEBAQ']) + 1e-4).all()
    assert COLS_ROUNDED(df)


def COLS_ROUNDED(df):
    # empiricalBA rounds to 4 decimals in R; check nothing has more precision
    vals = df[['pomean', 'LEBAQ', 'UEBAQ']].to_numpy().ravel()
    return np.allclose(vals, np.round(vals, 4))


def test_empiricalbax_runs():
    df = b.empiricalbax(2, 5, 0.05, 0.1, 10)
    assert {'LEBAQx', 'UEBAQx', 'LEBAHx', 'UEBAHx'}.issubset(df.columns)


# --------------------------------------------------------------------------- #
# Bayes factors                                                               #
# --------------------------------------------------------------------------- #
BAF = {
    1: (b.hypotestbaf1, (5, 0.5, 1, 1)),
    2: (b.hypotestbaf2, (5, 0.5, 1, 1)),
    3: (b.hypotestbaf3, (5, 0.5, 1, 1)),
    4: (b.hypotestbaf4, (5, 0.5, 1, 1, 1, 1)),
    5: (b.hypotestbaf5, (5, 0.5, 1, 1, 1, 1)),
    6: (b.hypotestbaf6, (5, 0.4, 1, 1, 0.6, 1, 1)),
}


@pytest.mark.parametrize("k", list(BAF))
def test_bayesfactor_shape_and_interpretation(k):
    fn, args = BAF[k]
    df = fn(*args)
    assert list(df.columns) == ['x', 'BaFa01', 'Interpretation']
    assert len(df) == 6                      # x = 0..5
    assert (df['BaFa01'] >= 0).all()
    assert df['Interpretation'].str.contains("Evidence").all()


def test_baf1_symmetric_and_interpretation_flips():
    df = b.hypotestbaf1(5, 0.5, 1, 1)
    assert np.allclose(df['BaFa01'].values, df['BaFa01'].values[::-1])
    # BaFa01 >= 1 -> evidence against H1; < 1 -> against H0
    for bf, interp in zip(df['BaFa01'], df['Interpretation']):
        assert ("H1" in interp) == (bf >= 1)


def test_bafx_matches_full():
    full = b.hypotestbaf1(5, 0.5, 1, 1)
    one = b.hypotestbaf1x(3, 5, 0.5, 1, 1).iloc[0]['BaFa01']
    assert one == pytest.approx(full['BaFa01'][3])


# --------------------------------------------------------------------------- #
# Deferred Bayesian variants of 3xx / 4xx / 5xx, now wired up                 #
# --------------------------------------------------------------------------- #
def test_lengthba_reports_both_intervals_hpd_shortest():
    df = b.lengthba(5, 0.05, 1, 1, 0.5, 0.5, seed=0)
    assert set(df['method']) == {"Quantile", "HPD"}
    q = df.loc[df['method'] == "Quantile", 'sumLen'].iloc[0]
    h = df.loc[df['method'] == "HPD", 'sumLen'].iloc[0]
    assert h <= q + 1e-9   # HPD is the shortest interval


def test_pcopbiba_has_q_and_h_columns():
    df = b.pcopbiba(5, 0.05, 0.5, 0.5)
    assert {'x1', 'pconfQ', 'pbiasQ', 'pconfH', 'pbiasH'}.issubset(df.columns)


def test_errba_reports_both_intervals():
    df = b.errba(10, 0.05, 0.5, -2, 1, 1)
    assert set(df['method']) == {"Quantile", "HPD"}
    assert {'delalp', 'theta', 'Fail_Pass'}.issubset(df.columns)


def test_bad_inputs_raise():
    with pytest.raises(ValueError):
        b.ciba(-1, 0.05, 1, 1)
    with pytest.raises(ValueError):
        b.probpos(5, 1, 1, 1.5)      # th out of range
    with pytest.raises(ValueError):
        b.hypotestbaf1(5, 1.5, 1, 1)  # th0 out of range
