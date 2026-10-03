"""Exact (Sterne, Blyth-Still-Casella, OLC, Witting) and betting/confidence-sequence methods.

Independent oracles used here:

* **OLC** -- the 540 limits published in Tables A1/A2 of Garthwaite, Moustafa & Elfadaly
  (2024, arXiv:2106.15521), n = 1..30 at 95% and 99% (fixtures in ``tests/data``).
* **Sterne** -- Duembgen (2021): n = 20, x = 5 gives (0.104, 0.475); plus a brute-force
  grid computation of the p-value hull.
* **Betting** -- frozen outputs of the authors' reference implementation, ``confseq``
  (Waudby-Smith & Ramdas), for a fixed 60-observation 0/1 sequence.
* Blyth-Still-Casella / Witting -- their *defining properties* (exact coverage touching
  1 - alpha / exactly 1 - alpha), by enumeration.
"""

import json
import pathlib

import numpy as np
import pytest
import scipy.stats as stats
from cases import ALPHA
from scipy.integrate import quad

import binomcikit as b
from binomcikit.ext import exact as ex

DATA = pathlib.Path(__file__).parent / "data"


def coverage_at(lo, hi, n, th):
    k = np.arange(n + 1)
    return stats.binom.pmf(k, n, th)[(lo < th) & (th < hi)].sum()


def min_coverage(lo, hi, n, points=3000):
    th = np.linspace(1e-4, 1 - 1e-4, points)
    return min(coverage_at(lo, hi, n, t) for t in th)


# ---------------------------------------------------------------------------------- OLC
@pytest.mark.parametrize(
    "fixture,alpha", [("olc_table_a1.json", 0.05), ("olc_table_a2.json", 0.01)]
)
def test_olc_matches_published_tables(fixture, alpha):
    table = json.loads((DATA / fixture).read_text())
    assert len(table) == 270
    cache = {}
    for key, (lo, hi) in table.items():
        n, x = map(int, key.split(","))
        df = cache.setdefault(n, b.ciolc(n, alpha))
        assert df.LOLC[x] == pytest.approx(lo, abs=6e-5), (n, x)
        assert df.UOLC[x] == pytest.approx(hi, abs=6e-5), (n, x)


@pytest.mark.parametrize("n", [6, 20])
def test_olc_is_locally_correct_by_construction(n):
    """Average coverage over each cycle between consecutive limits equals 1 - alpha/2."""
    df = b.ciolc(n, ALPHA)
    u = df.UOLC.to_numpy()
    for i in range(1, n + 1):  # upper tail: P(X >= i | p) averaged over (u_{i-1}, u_i)
        avg = quad(lambda p: stats.beta.cdf(p, i, n - i + 1), u[i - 1], u[i])[0] / (u[i] - u[i - 1])
        assert avg == pytest.approx(1 - ALPHA / 2, abs=1e-9)
    lo = df.LOLC.to_numpy()
    for i in range(n):  # lower tail: P(X <= i | p) averaged over (l_i, l_{i+1})
        avg = quad(lambda p: stats.beta.sf(p, i + 1, n - i), lo[i], lo[i + 1])[0] / (
            lo[i + 1] - lo[i]
        )
        assert avg == pytest.approx(1 - ALPHA / 2, abs=1e-9)


def test_olc_shorter_than_clopper_pearson_and_not_conservative():
    n = 20
    olc, cp = b.ciolc(n, ALPHA), b.ci(n=n, alpha=ALPHA, method="exact")
    assert (olc.UOLC - olc.LOLC).mean() < (cp.UEX - cp.LEX).mean() - 0.02
    th = np.linspace(1e-4, 1 - 1e-4, 4000)
    cov = np.array([coverage_at(olc.LOLC.to_numpy(), olc.UOLC.to_numpy(), n, t) for t in th])
    assert abs(cov.mean() - (1 - ALPHA)) < 0.01  # centred on nominal, unlike Clopper-Pearson


def test_olc_rejects_alpha_above_its_domain():
    with pytest.raises(ValueError, match="alpha/2 < 0.27"):
        b.ciolc(20, 0.6)
    assert len(b.ciolc(20, 0.5)) == 21  # inside the proved domain (one-sided level 0.25)


# -------------------------------------------------------------------------------- Sterne
def test_sterne_matches_duembgen_published_example():
    df = b.cisterne(20, ALPHA)
    assert df.LSTE[5] == pytest.approx(0.104, abs=6e-4)
    assert df.USTE[5] == pytest.approx(0.475, abs=6e-4)


def _brute_sterne(x, n, alpha, grid=60001):
    p = np.linspace(1e-6, 1 - 1e-6, grid)
    k = np.arange(n + 1)
    lf = stats.binom.logpmf(k[None, :], n, p[:, None])
    f = np.exp(lf)
    pv = (f * (lf <= lf[:, [x]] + 1e-9)).sum(axis=1)
    ok = p[pv > alpha]
    return ok.min(), ok.max()


@pytest.mark.parametrize("n", [8, 11])
def test_sterne_equals_brute_force_hull_of_pvalue(n):
    df = b.cisterne(n, ALPHA)
    for x in range(1, n):
        lo, hi = _brute_sterne(x, n, ALPHA)
        assert df.LSTE[x] == pytest.approx(lo, abs=3e-4)
        assert df.USTE[x] == pytest.approx(hi, abs=3e-4)


@pytest.mark.parametrize("n", [10, 25])
def test_sterne_guaranteed_coverage_and_shorter_on_average(n):
    df = b.cisterne(n, ALPHA)
    lo, hi = df.LSTE.to_numpy(), df.USTE.to_numpy()
    assert min_coverage(lo, hi, n) >= 1 - ALPHA - 1e-9
    cp = b.ci(n=n, alpha=ALPHA, method="exact")
    assert (hi - lo).sum() <= (cp.UEX - cp.LEX).sum() + 1e-9


def test_sterne_single_x_matches_table():
    full = b.cisterne(30, ALPHA)
    for x in (0, 4, 15, 30):
        row = b.cisternex(x, 30, ALPHA)
        assert row.LSTEx[0] == pytest.approx(full.LSTE[x], abs=1e-12)
        assert row.USTEx[0] == pytest.approx(full.USTE[x], abs=1e-12)


# --------------------------------------------------------------------- Blyth-Still-Casella
@pytest.mark.parametrize("n", [1, 2, 7, 15, 30])
def test_bsc_is_exact_and_touches_nominal_coverage(n):
    df = b.cibsc(n, ALPHA)
    lo, hi = df.LBSC.to_numpy(), df.UBSC.to_numpy()
    mn = min_coverage(lo, hi, n, points=4000)
    assert mn >= 1 - ALPHA - 1e-7  # exact
    if n >= 7:
        assert mn <= 1 - ALPHA + 5e-4  # ... and refined as far as exactness allows


@pytest.mark.parametrize("n", [10, 20])
def test_bsc_contained_in_cp_symmetric_and_shorter(n):
    df = b.cibsc(n, ALPHA)
    cp = b.ci(n=n, alpha=ALPHA, method="exact")
    assert np.all(df.LBSC.to_numpy() >= cp.LEX.to_numpy() - 1e-9)
    assert np.all(df.UBSC.to_numpy() <= cp.UEX.to_numpy() + 1e-9)
    assert df.LBSC.to_numpy() == pytest.approx(1 - df.UBSC.to_numpy()[::-1], abs=1e-9)
    assert (df.UBSC - df.LBSC).sum() < (cp.UEX - cp.LEX).sum()


def test_bsc_and_sterne_have_equal_total_length_at_n20():
    """Both minimise the acceptance-set cardinality at every theta => equal total length."""
    s, c = b.cisterne(20, ALPHA), b.cibsc(20, ALPHA)
    assert (s.USTE - s.LSTE).sum() == pytest.approx((c.UBSC - c.LBSC).sum(), abs=1e-6)


# ------------------------------------------------------------------------------- Witting
def _witting_coverage(n, alpha, th, grid=151):
    tot = 0.0
    k = np.arange(n + 1)
    pm = stats.binom.pmf(k, n, th)
    for u in (np.arange(grid) + 0.5) / grid:
        w = ex.ciwitting(n, alpha, u=u)
        tot += pm[(w.LWIT.to_numpy() < th) & (th < w.UWIT.to_numpy())].sum()
    return tot / grid


@pytest.mark.parametrize("th", [0.3, 0.91])
def test_witting_has_exact_coverage(th):
    # Averaged over the uniform draw the coverage is *exactly* 1 - alpha (a midpoint grid
    # of 151 draws resolves it to ~0.01); every non-randomised exact method sits well above.
    assert _witting_coverage(10, ALPHA, th) == pytest.approx(1 - ALPHA, abs=1e-2)


def test_witting_random_draw_is_seeded_and_bracketed_by_extremes():
    a1 = b.ciwitting(12, ALPHA, u=None, seed=7)
    a2 = b.ciwitting(12, ALPHA, u=None, seed=7)
    assert a1.equals(a2)
    lo_u, hi_u = b.ciwitting(12, ALPHA, u=0.0), b.ciwitting(12, ALPHA, u=1.0)
    assert np.all(a1.LWIT >= lo_u.LWIT - 1e-12) and np.all(a1.UWIT <= hi_u.UWIT + 1e-12)
    with pytest.raises(ValueError):
        b.ciwitting(12, ALPHA, u=1.5)


# ------------------------------------------------------------------- mixture CS (exact form)
@pytest.mark.parametrize("a_b", [(0.5, 0.5), (1.0, 1.0), (2.0, 5.0)])
def test_mixture_limits_satisfy_the_mixture_capital_equation(a_b):
    """The marginal likelihood ratio, integrated numerically, equals 1/alpha at each limit."""
    a, bb = a_b
    n = 25
    df = b.cimixture(n, ALPHA, a=a, b=bb)
    for x in (2, 9, 20):
        for m in (df.LMIX[x], df.UMIX[x]):
            cap = quad(
                lambda th: (th / m) ** x
                * ((1 - th) / (1 - m)) ** (n - x)
                * stats.beta.pdf(th, a, bb),
                0,
                1,
            )[0]
            assert cap == pytest.approx(1 / ALPHA, rel=1e-6)


def _stream_miscoverage(method, theta=0.3, T=120, reps=400, seed=11, **kw):
    rng = np.random.default_rng(seed)
    bad = 0
    for _ in range(reps):
        s = (rng.random(T) < theta).astype(int)
        cs = b.cibetseq(s, ALPHA, method=method, running_intersection=False, **kw)
        bad += bool(((cs.lower > theta) | (cs.upper < theta)).any())
    return bad / reps


@pytest.mark.parametrize("method,kw", [("mixture", {}), ("normal", {}), ("preb", {})])
def test_confidence_sequences_are_anytime_valid(method, kw):
    """P(the true theta ever leaves the sequence) <= alpha -- at *any* of the 120 looks."""
    assert _stream_miscoverage(method, **kw) <= ALPHA + 0.02


def test_hedged_sequence_is_anytime_valid():
    assert _stream_miscoverage("hedged", reps=120, breaks=200) <= ALPHA + 0.04


# ------------------------------------------------------ confseq (reference implementation) oracle
SEQ = "110010010100000010011010000010010010100100000001000101010001"
CONFSEQ_HEDGED = {10: (0.131, 0.911), 30: (0.151, 0.608), 60: (0.178, 0.514)}
CONFSEQ_PREB = {10: (0.0, 1.0), 30: (0.0, 0.67698), 60: (0.09549, 0.531736)}


def test_hedged_cs_matches_confseq():
    cs = b.cibetseq([int(c) for c in SEQ], 0.05, "hedged", running_intersection=False)
    for t, (lo, hi) in CONFSEQ_HEDGED.items():
        assert cs.lower[t - 1] == pytest.approx(lo, abs=1e-6)
        assert cs.upper[t - 1] == pytest.approx(hi, abs=1e-6)


def test_preb_cs_matches_confseq():
    cs = b.cibetseq([int(c) for c in SEQ], 0.05, "preb", running_intersection=False)
    for t, (lo, hi) in CONFSEQ_PREB.items():
        assert cs.lower[t - 1] == pytest.approx(lo, abs=1e-5)
        assert cs.upper[t - 1] == pytest.approx(hi, abs=1e-5)


def test_running_intersection_never_widens():
    s = [int(c) for c in SEQ]
    cs = b.cibetseq(s, 0.05, "mixture", running_intersection=True)
    assert np.all(np.diff(cs.lower) >= -1e-12) and np.all(np.diff(cs.upper) <= 1e-12)


def test_cibetseq_input_validation():
    with pytest.raises(ValueError):
        b.cibetseq([], 0.05)
    with pytest.raises(ValueError):
        b.cibetseq([0, 1, 2], 0.05)
    with pytest.raises(ValueError):
        b.cibetseq([0, 1], 0.05, method="nope")


# -------------------------------------------------------------------- hedged betting (table)
def test_betting_table_is_deterministic_and_numba_matches_numpy():
    t1 = b.cibetting(8, ALPHA, B=20, seed=3)
    t2 = b.cibetting(8, ALPHA, B=20, seed=3, use_numba=False)
    assert t1.equals(b.cibetting(8, ALPHA, B=20, seed=3))
    assert t1[["LBET", "UBET"]].to_numpy() == pytest.approx(
        t2[["LBET", "UBET"]].to_numpy(), abs=1e-9
    )


def test_betting_coverage_guarantee_and_exact_zero_limits():
    n = 10
    df = b.cibetting(n, ALPHA, B=30, seed=1)
    assert min_coverage(df.LBET.to_numpy(), df.UBET.to_numpy(), n, points=1500) >= 1 - ALPHA - 1e-9
    assert (df.LBET == 0).any() and (df.UBET == 1).any()  # no 1e-12 residue at the edges
    lo, hi = df.LBET.to_numpy(), df.UBET.to_numpy()
    assert np.all(lo <= np.arange(n + 1) / n + 1e-12) and np.all(hi >= np.arange(n + 1) / n - 1e-12)


def test_betting_parameter_validation():
    for kw in ({"theta": 0.0}, {"trunc": 1.0}, {"B": 0}):
        with pytest.raises(ValueError):
            b.cibetting(6, ALPHA, **kw)
    with pytest.raises(ValueError):
        b.cimixture(6, ALPHA, a=0.0)
