"""Pires & Amado (2008) methods, Thulin (2014) coverage-adjusted CP, noise-smoothed Wilson.

Oracles
-------
* Pires & Amado Tables 1-2 are re-implemented here as *independent scalar code* (one ``x`` at a time,
  straight from the printed formulas) and compared with the vectorised implementation.
* Their published conclusion -- Score-cc and arcsine-cc-Anscombe are *strictly conservative*
  (min coverage >= 1 - alpha - 0.005 for n >= 10), Add-4 is correct on average -- is checked
  by exact enumeration.
* Thulin Table 1 (alpha' for the Beta(1,1)-prior correction) and his worked example (n=96, x=4).
  The paper's table was produced with a bisection tolerance of ~1e-4, so agreement is asserted to
  4e-4; *exactness* is asserted separately by integrating Thulin's own definition numerically.
"""

import numpy as np
import pytest
import scipy.stats as stats
from cases import ALPHA
from scipy.integrate import quad

import binomcikit as b
from binomcikit.ext import adjusted as A

Z = stats.norm.ppf(1 - ALPHA / 2)


def coverage_stats(lo, hi, n, points=2500):
    k = np.arange(n + 1)
    th = np.linspace(1e-4, 1 - 1e-4, points)
    pm = stats.binom.pmf(k[None, :], n, th[:, None])
    cov = (pm * ((lo[None, :] < th[:, None]) & (th[:, None] < hi[None, :]))).sum(axis=1)
    return cov.min(), cov.mean()


# ------------------------------------------------------- Pires & Amado, scalar re-derivations
def scalar_waldi(x, n, a, recentre=False, cc=False):
    c = stats.norm.ppf(1 - a / 2)
    if x == 0:
        return 0.0, 1 - (a / 2) ** (1 / n)
    if x == n:
        return (a / 2) ** (1 / n), 1.0
    centre = (x + c * c / 2) / (n + c * c) if recentre else x / n
    half = c * np.sqrt(x / n**2 * (1 - x / n)) + (1 / (2 * n) if cc else 0.0)
    return max(centre - half, 0.0), min(centre + half, 1.0)


def scalar_boot(x, n, a, bcp=False, cc=False):
    if x == 0:
        return 0.0, 1 - (a / 2) ** (1 / n)
    if x == n:
        return (a / 2) ** (1 / n), 1.0
    p = x / n
    al, ah = a / 2, 1 - a / 2
    if bcp:
        kb = 0.5 * (stats.binom.cdf(x, n, p) + stats.binom.cdf(x - 1, n, p))
        al = stats.norm.cdf(stats.norm.ppf(a / 2) + 2 * stats.norm.ppf(kb))
        ah = stats.norm.cdf(stats.norm.ppf(1 - a / 2) + 2 * stats.norm.ppf(kb))
    lo, hi = stats.binom.ppf(al, n, p) / n, stats.binom.ppf(ah, n, p) / n
    if cc:
        lo, hi = max(lo - 1 / (2 * n), 0.0), min(hi + 1 / (2 * n), 1.0)
    return lo, hi


def scalar_ans(x, n, a):
    c = stats.norm.ppf(1 - a / 2)
    lo = (
        0.0
        if x == 0
        else np.sin(
            np.arcsin(np.sqrt((3 / 8 + x - 0.5) / (n + 3 / 4))) - c / (2 * np.sqrt(n + 0.5))
        )
        ** 2
    )
    hi = (
        1.0
        if x == n
        else np.sin(
            np.arcsin(np.sqrt((3 / 8 + x + 0.5) / (n + 3 / 4))) + c / (2 * np.sqrt(n + 0.5))
        )
        ** 2
    )
    return lo, hi


@pytest.mark.parametrize("n", [7, 25, 60])
@pytest.mark.parametrize(
    "fn,col,scalar",
    [
        (b.ciwaldi, ("LWDI", "UWDI"), lambda x, n, a: scalar_waldi(x, n, a)),
        (b.ciwaldicc, ("LWIC", "UWIC"), lambda x, n, a: scalar_waldi(x, n, a, cc=True)),
        (b.ciwaldrec, ("LWRC", "UWRC"), lambda x, n, a: scalar_waldi(x, n, a, recentre=True)),
        (
            b.ciwaldreccc,
            ("LWRK", "UWRK"),
            lambda x, n, a: scalar_waldi(x, n, a, recentre=True, cc=True),
        ),
        (b.cibootp, ("LBTP", "UBTP"), lambda x, n, a: scalar_boot(x, n, a)),
        (b.cibootpcc, ("LBPC", "UBPC"), lambda x, n, a: scalar_boot(x, n, a, cc=True)),
        (b.cibcp, ("LBCP", "UBCP"), lambda x, n, a: scalar_boot(x, n, a, bcp=True)),
        (b.cibcpcc, ("LBCC", "UBCC"), lambda x, n, a: scalar_boot(x, n, a, bcp=True, cc=True)),
        (b.ciarcsineans, ("LANS", "UANS"), scalar_ans),
    ],
)
def test_vectorised_equals_scalar_transcription_of_the_paper_tables(fn, col, scalar, n):
    df = fn(n, ALPHA)
    for x in range(n + 1):
        lo, hi = scalar(x, n, ALPHA)
        assert df[col[0]][x] == pytest.approx(lo, abs=1e-12), (x, n)
        assert df[col[1]][x] == pytest.approx(hi, abs=1e-12), (x, n)


def test_arcsine_anscombe_clamp_option_only_changes_limits_that_left_the_range():
    n = 7
    lit, clp = b.ciarcsineans(n, ALPHA), b.ciarcsineans(n, ALPHA, clamp=True)
    assert lit.LANS[1] == pytest.approx(0.00022982789636, abs=1e-12) and clp.LANS[1] == 0.0
    assert np.all(
        clp.LANS.to_numpy() <= lit.LANS.to_numpy() + 1e-15
    )  # clamping lowers the lower limit
    assert np.all(
        clp.UANS.to_numpy() >= lit.UANS.to_numpy() - 1e-15
    )  # ... and raises the upper limit
    assert np.all(np.diff(clp.LANS.to_numpy()) >= 0) and np.all(np.diff(clp.UANS.to_numpy()) >= 0)


def test_wald_i_equals_wald_off_the_boundary_and_exact_on_it():
    n = 30
    wi, wd = b.ciwaldi(n, ALPHA), b.ciwd(n, ALPHA)
    for x in range(1, n):
        assert wi.LWDI[x] == pytest.approx(wd.LWD[x]) and wi.UWDI[x] == pytest.approx(wd.UWD[x])
    assert wi.UWDI[0] == pytest.approx(1 - (ALPHA / 2) ** (1 / n)) and wi.LWDI[n] == pytest.approx(
        (ALPHA / 2) ** (1 / n)
    )
    assert wd.UWD[0] == 0  # plain Wald has the zero-width row Wald-I repairs


def test_analytic_bootstrap_is_the_exact_law_the_monte_carlo_bootstrap_estimates():
    """The percentile bootstrap needs no resampling: its law is Binomial(n, x/n) exactly."""
    n, x = 40, 12
    rng = np.random.default_rng(0)
    mc = rng.binomial(n, x / n, 400_000) / n
    df = b.cibootp(n, ALPHA)
    assert df.LBTP[x] == pytest.approx(np.quantile(mc, ALPHA / 2, method="lower"), abs=1 / n)
    assert df.UBTP[x] == pytest.approx(np.quantile(mc, 1 - ALPHA / 2, method="higher"), abs=1 / n)


# ----------------------------- the paper's published coverage classification (exact enumeration)
def scalar_score_cc(x, n, a):
    c = stats.norm.ppf(1 - a / 2)
    lo = (
        0.0
        if x == 0
        else (2 * x + c * c - 1 - c * np.sqrt(c * c - (2 + 1 / n) + 4 * x * (1 - x / n + 1 / n)))
        / (2 * (n + c * c))
    )
    hi = (
        1.0
        if x == n
        else (2 * x + c * c + 1 + c * np.sqrt(c * c + (2 - 1 / n) + 4 * x * (1 - x / n - 1 / n)))
        / (2 * (n + c * c))
    )
    return lo, hi


@pytest.mark.parametrize("n", [7, 25, 60])
def test_score_cc_equals_table_1_method_iv_and_the_pass_formula(n):
    from binomcikit import planning as pl

    df = b.ciscorecc(n, ALPHA)
    for x in range(n + 1):
        lo, hi = scalar_score_cc(x, n, ALPHA)
        assert df.LSCC[x] == pytest.approx(lo, abs=1e-12) and df.USCC[x] == pytest.approx(
            hi, abs=1e-12
        )
    # the PASS (NCSS) chapter-115 formula, implemented independently in planning.py, must agree
    lo, hi = pl._real_interval("wilson-cc", n, ALPHA, np.arange(n + 1, dtype=float))
    assert df.LSCC.to_numpy() == pytest.approx(
        lo, abs=1e-12
    ) and df.USCC.to_numpy() == pytest.approx(hi, abs=1e-12)


@pytest.mark.parametrize("n", [10, 25, 80])
def test_strictly_conservative_group_matches_pires_and_amado(n):
    """Pires & Amado's Group 1: min coverage >= 1 - alpha - 0.005 for all n >= 10."""
    ans = b.ciarcsineans(n, ALPHA)
    mn, _ = coverage_stats(ans.LANS.to_numpy(), ans.UANS.to_numpy(), n)
    assert mn >= 1 - ALPHA - 0.005
    scc = b.ciscorecc(n, ALPHA)
    mn2, _ = coverage_stats(scc.LSCC.to_numpy(), scc.USCC.to_numpy(), n)
    assert mn2 >= 1 - ALPHA - 0.005


def test_original_cicsc_port_lacks_the_boundary_rows_pires_and_amado_repair():
    """The R-port ``cicsc`` has L(0) > 0, so coverage -> 0 as theta -> 0; Score-cc (method IV) does not."""
    n = 25
    old = b.cicsc(n, ALPHA, 1 / (2 * n))
    assert old.LCS[0] > 0 and b.ciscorecc(n, ALPHA).LSCC[0] == 0


@pytest.mark.parametrize("n", [25, 80])
def test_wald_variants_are_not_conservative(n):
    wi = b.ciwaldi(n, ALPHA)
    mn, mean = coverage_stats(wi.LWDI.to_numpy(), wi.UWDI.to_numpy(), n)
    assert 0.8 < mn < 0.9 and mean < 1 - ALPHA  # Wald-I (their Fig. 3-4): min coverage ~0.83-0.85


def test_arcsine_anscombe_is_about_as_long_as_clopper_pearson():
    """It sits with Clopper-Pearson in the conservative group, at essentially the same length."""
    n = 40
    ans, cp = b.ciarcsineans(n, ALPHA), b.ci(n=n, alpha=ALPHA, method="exact")
    ratio = (ans.UANS - ans.LANS).mean() / (cp.UEX - cp.LEX).mean()
    assert 0.98 < ratio < 1.05


# ------------------------------------------------------------------------------- Thulin
THULIN_TABLE_1 = {  # n: (alpha' for alpha=0.05, alpha' for alpha=0.01) -- prior Beta(1,1)
    5: (0.1772, 0.0516),
    10: (0.128, 0.0331),
    15: (0.1095, 0.0269),
    20: (0.0995, 0.0237),
    25: (0.0931, 0.0218),
    30: (0.0885, 0.0204),
    35: (0.0851, 0.0194),
    40: (0.0825, 0.0186),
    45: (0.0803, 0.018),
    50: (0.0785, 0.0175),
    55: (0.0769, 0.0171),
    60: (0.0756, 0.0167),
    65: (0.0745, 0.0164),
    70: (0.0735, 0.0161),
    75: (0.0726, 0.0159),
    80: (0.0718, 0.0156),
    85: (0.071, 0.0154),
    90: (0.0704, 0.0153),
    95: (0.0698, 0.0151),
    100: (0.0692, 0.015),
    110: (0.0682, 0.0147),
    120: (0.0674, 0.0145),
    130: (0.0666, 0.0143),
    140: (0.066, 0.0141),
    150: (0.0654, 0.0139),
    160: (0.0649, 0.0138),
    170: (0.0644, 0.0137),
    180: (0.064, 0.0135),
    190: (0.0636, 0.0134),
    200: (0.0632, 0.0133),
}


@pytest.mark.parametrize("n", sorted(THULIN_TABLE_1))
def test_adjusted_alpha_matches_thulin_table_1(n):
    a05, a01 = THULIN_TABLE_1[n]
    assert A.adjusted_alpha(n, 0.05, 1.0) == pytest.approx(a05, abs=4e-4)
    assert A.adjusted_alpha(n, 0.01, 1.0) == pytest.approx(a01, abs=4e-4)


def _mean_coverage_by_integration(n, a):
    """Thulin's definition (eq. 3), integrated numerically -- independent of the closed form."""
    k = np.arange(n + 1)
    lo = np.where(k > 0, stats.beta.ppf(a / 2, np.maximum(k, 1), n - k + 1), 0.0)
    hi = np.where(k < n, stats.beta.ppf(1 - a / 2, k + 1, np.maximum(n - k, 1)), 1.0)
    pts = np.unique(np.concatenate([lo, hi, [0.0, 1.0]]))
    total = 0.0
    for l, h in zip(pts[:-1], pts[1:]):
        covered = (lo < 0.5 * (l + h)) & (0.5 * (l + h) < hi)
        if covered.any():
            total += quad(
                lambda p: stats.binom.pmf(k[covered], n, p).sum(), l, h, epsabs=1e-13, epsrel=1e-13
            )[0]
    return total


@pytest.mark.parametrize("n", [5, 20, 96])
def test_adjusted_alpha_gives_exactly_the_target_mean_coverage(n):
    a = A.adjusted_alpha(n, 0.05, 1.0)
    assert A.mean_coverage(n, a, 1.0) == pytest.approx(0.95, abs=1e-10)  # closed form
    assert _mean_coverage_by_integration(n, a) == pytest.approx(
        0.95, abs=1e-9
    )  # definition, by quadrature


def test_thulin_worked_example_n96_x4():
    prior = b.cigcpx(4, 96, 0.05, r=1.0, kind="prior")
    assert prior.alpha_adj[0] == pytest.approx(0.06967, abs=2e-4)
    assert (prior.LGCPx[0], prior.UGCPx[0]) == (
        pytest.approx(0.013, abs=6e-4),
        pytest.approx(0.098, abs=6e-4),
    )
    post = b.cigcpx(4, 96, 0.05, r=0.5, kind="posterior")
    assert post.alpha_adj[0] == pytest.approx(0.09385, abs=2e-4)
    assert (post.LGCPx[0], post.UGCPx[0]) == (
        pytest.approx(0.014, abs=6e-4),
        pytest.approx(0.094, abs=6e-4),
    )


def test_thulin_published_interval_examples_n20():
    """Table 2: n=20, x=1: CP (0.0012, 0.2487); prior Beta(1,1) (0.0025, 0.2163) at alpha = 0.05."""
    cp = b.ci(x=1, n=20, alpha=0.05, method="exact")
    # (Thulin truncates to four decimals: 0.001265 is printed 0.0012)
    assert (cp.iloc[0, 1], cp.iloc[0, 2]) == (
        pytest.approx(0.0012, abs=8e-5),
        pytest.approx(0.2487, abs=1e-4),
    )
    g = b.cigcpx(1, 20, 0.05, r=1.0, kind="prior")
    assert (g.LGCPx[0], g.UGCPx[0]) == (
        pytest.approx(0.0025, abs=3e-4),
        pytest.approx(0.2163, abs=3e-4),
    )


@pytest.mark.parametrize("kind", ["prior", "posterior"])
def test_adjusted_cp_is_nested_in_cp_equivariant_and_shorter(kind):
    n = 18
    g = b.cigcp(n, ALPHA, r=1.0, kind=kind)
    cp = b.ci(n=n, alpha=ALPHA, method="exact")
    assert np.all(g.LGCP.to_numpy() >= cp.LEX.to_numpy() - 1e-12)
    assert np.all(g.UGCP.to_numpy() <= cp.UEX.to_numpy() + 1e-12)
    assert (g.UGCP - g.LGCP).sum() < (cp.UEX - cp.LEX).sum()
    if kind == "prior":  # the symmetric prior makes the single alpha' equivariant
        assert g.LGCP.to_numpy() == pytest.approx(1 - g.UGCP.to_numpy()[::-1], abs=1e-10)
    assert (g.alpha_adj >= ALPHA).all()


def test_prior_adjusted_cp_has_nominal_mean_coverage_but_not_guaranteed_minimum():
    n = 30
    g = b.cigcp(n, ALPHA, r=1.0, kind="prior")
    th = np.linspace(1e-5, 1 - 1e-5, 20001)
    k = np.arange(n + 1)
    pm = stats.binom.pmf(k[None, :], n, th[:, None])
    cov = (
        pm
        * ((g.LGCP.to_numpy()[None, :] < th[:, None]) & (th[:, None] < g.UGCP.to_numpy()[None, :]))
    ).sum(axis=1)
    assert cov.mean() == pytest.approx(0.95, abs=2e-3)  # uniform weight == mean over theta
    assert cov.min() >= 1 - g.alpha_adj[0] - 1e-9  # Thulin: minimum coverage >= 1 - alpha'
    assert cov.min() < 0.95  # ... and it does dip below nominal (that is the trade-off)


def test_gcp_validation():
    with pytest.raises(ValueError):
        b.cigcp(10, ALPHA, kind="bogus")
    with pytest.raises(ValueError):
        b.cigcp(10, ALPHA, r=0.0)
    with pytest.raises(ValueError):
        b.cigcp(10, 0.0)


# ------------------------------------------------------------------------------- noise Wilson
def test_uniform_noise_wilson_with_zero_noise_is_plain_wilson():
    n = 25
    w, z = b.cisc(n, ALPHA), b.ciunifwilson(n, ALPHA, u=0.0)
    assert z.LUNW.to_numpy() == pytest.approx(w.LSC.to_numpy(), abs=1e-12)
    assert z.UUNW.to_numpy() == pytest.approx(w.USC.to_numpy(), abs=1e-12)


def test_noise_wilson_is_seeded_and_bounded():
    a = b.ciunifwilson(30, ALPHA, seed=5)
    assert a.equals(b.ciunifwilson(30, ALPHA, seed=5)) and not a.equals(
        b.ciunifwilson(30, ALPHA, seed=6)
    )
    s = b.cisplitwilson(30, ALPHA, seed=5)
    assert s.equals(b.cisplitwilson(30, ALPHA, seed=5))
    for df, lo, hi in ((a, "LUNW", "UUNW"), (s, "LSPW", "USPW")):
        assert (
            df[lo].between(0, 1).all() and df[hi].between(0, 1).all() and (df[hi] >= df[lo]).all()
        )
    with pytest.raises(ValueError):
        b.ciunifwilson(30, ALPHA, u=0.9)


def test_split_sample_estimator_averages_back_to_phat():
    """E[p-tilde | x] = x/n (hypergeometric mean), so the average split interval is close to Wilson."""
    n = 80
    runs = np.mean([b.cisplitwilson(n, ALPHA, seed=s).LSPW.to_numpy() for s in range(200)], axis=0)
    assert runs == pytest.approx(b.cisc(n, ALPHA).LSC.to_numpy(), abs=0.01)


def test_new_methods_are_registered_and_usable_everywhere():
    for key in (
        "coverage-adjusted",
        "arcsine-anscombe",
        "analytic-bcp-cc",
        "wald-recentred",
        "stevens",
        "split-wilson",
    ):
        spec = b.methods.lookup(key)
        assert spec is not None
        assert len(b.ci(n=9, alpha=ALPHA, method=key)) == 10
    cmp = b.compare(3, 20, methods=["wilson", "coverage-adjusted", "arcsine-anscombe", "exact"])
    assert (cmp.width > 0).all()
