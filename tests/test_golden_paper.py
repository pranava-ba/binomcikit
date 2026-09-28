"""Golden values taken directly from the source paper (Subbiah & Rajeswaran,
SoftwareX 6, 2017), Table 2 — an oracle independent of statsmodels and R.
"""

import pytest
from cases import ALPHA, ARCSINE_N5, LOGIT_N5, LR_N5, MIDP_N5, WALD_N5, WALDT_N5, N

import binomcikit as b

try:
    from statsmodels.stats.proportion import proportion_confint as _sm_ci
except ImportError:  # statsmodels is a test-only dependency
    _sm_ci = None


def test_wald_n5_matches_paper_table2():
    df = b.ciwd(N, ALPHA)
    for x, (lo, hi) in WALD_N5.items():
        assert df.LWD[x] == pytest.approx(lo, abs=5e-4)
        assert df.UWD[x] == pytest.approx(hi, abs=5e-4)


def test_wald_n5_zwi_only_at_boundaries():
    df = b.ciwd(N, ALPHA)
    zwi = {x for x in range(N + 1) if df.LWD[x] == df.UWD[x]}
    assert zwi == {0, N}


def test_arcsine_n5_matches_closed_form():
    df = b.cias(N, ALPHA)
    for x, (lo, hi) in ARCSINE_N5.items():
        assert df.LAS[x] == pytest.approx(lo, abs=5e-4)
        assert df.UAS[x] == pytest.approx(hi, abs=5e-4)


def test_arcsine_boundary_excludes_observed_proportion():
    # ArcSine's signature failure: at the boundaries the interval collapses to a
    # nonzero-width-zero point that does NOT include the observed proportion
    # (0 at x = 0, 1 at x = n). The width is ~0 up to floating-point noise.
    df = b.cias(N, ALPHA)
    assert df.UAS[0] - df.LAS[0] < 1e-9 and df.LAS[0] > 0.01
    assert df.UAS[N] - df.LAS[N] < 1e-9 and df.UAS[N] < 0.99


def test_logit_n5_matches_closed_form():
    df = b.cilt(N, ALPHA)
    for x, (lo, hi) in LOGIT_N5.items():
        assert df.LLT[x] == pytest.approx(lo, abs=5e-4)
        assert df.ULT[x] == pytest.approx(hi, abs=5e-4)


def test_logit_boundary_uses_exact_one_sided_substitution():
    # logit(0)/logit(1) are undefined, so at x = 0, n the method substitutes the
    # exact one-sided (Clopper-Pearson) interval instead of a normal approximation.
    df = b.cilt(N, ALPHA)
    assert df.LLT[0] == 0.0 and df.ULT[0] == pytest.approx(1 - (ALPHA / 2) ** (1 / N))
    assert df.ULT[N] == 1.0 and df.LLT[N] == pytest.approx((ALPHA / 2) ** (1 / N))
    # And unlike Wald/ArcSine, logit produces no zero-width interval anywhere.
    assert not (df.LLT == df.ULT).any()


def test_waldt_n5_matches_closed_form():
    df = b.citw(N, ALPHA)
    for x, (lo, hi) in WALDT_N5.items():
        assert df.LTW[x] == pytest.approx(lo, abs=5e-4)
        assert df.UTW[x] == pytest.approx(hi, abs=5e-4)


def test_waldt_widens_vs_wald_and_has_no_zwi():
    # The Student-t quantile (finite Satterthwaite d.o.f.) always exceeds the normal z,
    # so at an interior x with no clamping the Wald-T interval is strictly wider than Wald.
    n = 20
    tw = b.citw(n, ALPHA)
    wd = b.ciwd(n, ALPHA)
    x = 10  # p_hat = 0.5, neither interval clamps here
    assert (tw.UTW[x] - tw.LTW[x]) > (wd.UWD[x] - wd.LWD[x])
    # The boundary modification (centre = (x+2)/(n+4)) means no zero-width interval anywhere.
    assert not (b.citw(N, ALPHA).LTW == b.citw(N, ALPHA).UTW).any()


def test_lr_n5_matches_closed_form():
    df = b.cilr(N, ALPHA)
    for x, (lo, hi) in LR_N5.items():
        assert df.LLR[x] == pytest.approx(lo, abs=5e-4)
        assert df.ULR[x] == pytest.approx(hi, abs=5e-4)


def test_lr_brackets_the_mle():
    # The likelihood-ratio interval is centred on the fit: for interior x it must
    # contain the MLE p_hat = x/n (the value that maximises the likelihood).
    df = b.cilr(N, ALPHA)
    for x in range(1, N):
        assert df.LLR[x] < x / N < df.ULR[x]


@pytest.mark.parametrize("n,x", [(26000, 13000), (50000, 25000), (100000, 50000)])
def test_lr_correct_at_large_n(n, x):
    # Regression test: cilrx used to find the MLE by numerically minimizing the
    # RAW (non-log) likelihood, which underflows to exactly 0.0 for large n away
    # from the mode -- minimize_scalar could then converge to a wrong "MLE" (was
    # observed snapping to ~1.0 for x/n=0.5 at n=26000), corrupting the whole
    # interval (was returning ~[0, 1] instead of a tight interval around 0.5).
    # Fixed by using the closed-form MLE (x/n) and a proper brentq root-find.
    row = b.ci(x=x, n=n, method="lr")
    phat = x / n
    assert row["LLRx"].iloc[0] == pytest.approx(phat, abs=0.01)
    assert row["ULRx"].iloc[0] == pytest.approx(phat, abs=0.01)
    width = row["ULRx"].iloc[0] - row["LLRx"].iloc[0]
    assert width < 0.02  # a 95% CI at n>=26000 around p=0.5 should be a few % wide, not ~1.0


def test_lr_full_table_matches_single_x():
    # cilr() (base_n.py, all-x) had the identical flawed MLE pattern in its own
    # per-x loop as cilrx() (base_n_x.py, single-x) -- fixed identically. n kept
    # modest here (the full table is an O(n) Python loop, expensive at the
    # n~26,000 scale where the original bug actually triggered; that scale is
    # already covered, via the much cheaper single-x path, by
    # test_lr_correct_at_large_n above): this just confirms the two code paths
    # agree with each other after the fix.
    n = 2000
    df = b.cilr(n, ALPHA)
    for x in [0, 1, n // 2, n - 1, n]:
        row_x = b.cilrx(x, n, ALPHA)
        row_all = df[df["x"] == x].iloc[0]
        assert row_all["LLR"] == pytest.approx(row_x["LLRx"].iloc[0], abs=1e-9)
        assert row_all["ULR"] == pytest.approx(row_x["ULRx"].iloc[0], abs=1e-9)


@pytest.mark.skipif(_sm_ci is None, reason="statsmodels not installed")
@pytest.mark.parametrize("n", [5, 13, 30])
def test_exact_cp_matches_statsmodels(n):
    # The exact family at e = 1 is the Clopper-Pearson interval, which statsmodels
    # provides as method="beta" (via Beta quantiles). binomcikit computes it by
    # root-finding on the binomial tails, yet the two agree to machine precision.
    df = b.ciex(n, ALPHA, [1.0])
    for x in range(n + 1):
        lo, hi = _sm_ci(x, n, alpha=ALPHA, method="beta")
        row = df[df["x"] == x].iloc[0]
        assert row["LEX"] == pytest.approx(lo, abs=1e-9)
        assert row["UEX"] == pytest.approx(hi, abs=1e-9)


def test_midp_matches_golden_and_is_narrower_than_cp():
    mp = b.ciex(N, ALPHA, [0.5])
    cp = b.ciex(N, ALPHA, [1.0])
    for x, (lo, hi) in MIDP_N5.items():
        row = mp[mp["x"] == x].iloc[0]
        assert row["LEX"] == pytest.approx(lo, abs=5e-4)
        assert row["UEX"] == pytest.approx(hi, abs=5e-4)
    # Mid-P puts only half the point mass in the tail, so it is never wider than CP.
    for x in range(N + 1):
        mw = mp[mp["x"] == x].iloc[0]
        cw = cp[cp["x"] == x].iloc[0]
        assert (mw["UEX"] - mw["LEX"]) <= (cw["UEX"] - cw["LEX"]) + 1e-12


@pytest.mark.skipif(_sm_ci is None, reason="statsmodels not installed")
@pytest.mark.parametrize("n", [5, 13, 30])
def test_bayes_jeffreys_matches_statsmodels(n):
    # The Bayesian quantile credible interval with a Jeffreys prior Beta(0.5, 0.5)
    # is exactly statsmodels' method="jeffreys" (Beta-quantile interval).
    df = b.ciba(n, ALPHA, 0.5, 0.5)
    for x in range(n + 1):
        lo, hi = _sm_ci(x, n, alpha=ALPHA, method="jeffreys")
        assert df.LBAQ[x] == pytest.approx(lo, abs=1e-9)
        assert df.UBAQ[x] == pytest.approx(hi, abs=1e-9)


def test_lr_dispatch_supports_adjusted():
    # Not previously tested anywhere -- cialr/cialrx had zero test coverage
    # before the large-n bug fix below surfaced them.
    assert b.ci(n=10, method="lr", h=2).equals(b.cialr(10, ALPHA, 2))
    assert b.ci(x=3, n=10, method="lr", h=2).equals(b.cialrx(3, 10, ALPHA, 2))


@pytest.mark.parametrize("h", [0, 1, 3])
def test_cialr_brackets_the_adjusted_mle(h):
    n = 20
    df = b.cialr(n, ALPHA, h)
    n1 = n + 2 * h
    for x in range(n + 1):
        y1 = x + h
        if 0 < y1 < n1:
            assert df.LALR[x] < y1 / n1 < df.UALR[x]


@pytest.mark.parametrize("n,h", [(20, 2), (50, 1)])
def test_cialr_matches_cialrx(n, h):
    # cialr's root is now found via brentq; cialrx's (unaffected by the bug
    # below, left as-is) via minimize_scalar -- two different numerical
    # methods agree closely but not to full float precision, same as the
    # documented ~4e-6 brentq-vs-minimize_scalar gap noted for unadjusted LR
    # in cases.py.
    df = b.cialr(n, ALPHA, h)
    for x in [0, 1, n // 3, n // 2, n - 1, n]:
        row = b.cialrx(x, n, ALPHA, h)
        assert df.LALR[x] == pytest.approx(row.LALRx.iloc[0], abs=1e-4)
        assert df.UALR[x] == pytest.approx(row.UALRx.iloc[0], abs=1e-4)


@pytest.mark.parametrize("n,x,h", [(26000, 13000, 1), (50000, 25000, 2)])
def test_cialrx_correct_at_large_n(n, x, h):
    # cialrx (adj_n_x.py, single-x) already used the log-likelihood for its
    # MLE step and was confirmed unaffected by the cialr bug below (checked
    # directly, not just inferred) -- this just locks that in. Via the fast
    # single-x path, not the O(n) full table.
    row = b.cialrx(x, n, ALPHA, h)
    phat = (x + h) / (n + 2 * h)
    assert row.LALRx.iloc[0] == pytest.approx(phat, abs=0.01)
    assert row.UALRx.iloc[0] == pytest.approx(phat, abs=0.01)


def test_cialr_correct_at_moderately_large_n():
    # Regression test: adj_n.py's cialr (all-x adjusted LR) had the identical
    # flawed pattern as the unadjusted cilr -- minimizing the RAW likelihood
    # to find the MLE, which underflows to 0.0 for large n away from the
    # mode (confirmed broken at n=26000; that full table costs ~2 minutes
    # even fixed -- an O(n) Python loop -- so this checks the same code path
    # at a still-meaningful but affordable n=3000, ~5s).
    n, h = 3000, 1
    df = b.cialr(n, ALPHA, h)
    x = n // 2
    phat = (x + h) / (n + 2 * h)
    row = df[df["x"] == x].iloc[0]
    assert row.LALR == pytest.approx(phat, abs=0.02)
    assert row.UALR == pytest.approx(phat, abs=0.02)


def test_bayes_hpd_has_correct_mass_and_is_shortest():
    import scipy.stats as stats

    n = 20
    df = b.ciba(n, ALPHA, 1, 1)  # flat Beta(1, 1) prior
    for x in range(n + 1):
        s1, s2 = x + 1, n - x + 1
        mass = stats.beta.cdf(df.UBAH[x], s1, s2) - stats.beta.cdf(df.LBAH[x], s1, s2)
        assert mass == pytest.approx(1 - ALPHA, abs=1e-4)
        # The HPD is the shortest credible interval, so never wider than the quantile one.
        assert (df.UBAH[x] - df.LBAH[x]) <= (df.UBAQ[x] - df.LBAQ[x]) + 1e-9
