"""Extended methods (``binomcikit.ext``): registry-wide invariants + per-family oracles.

Strategy (per the project's oracle-vetting rule): where a *different* convention would make
an external oracle misleading we derive the quantity independently instead —

* Cressie-Read at ``lam = 1`` and ``lam = 0`` must reproduce the already-verified Wilson and
  Likelihood-Ratio intervals to machine precision (identity, not approximation);
* the concentration intervals must have coverage >= 1 - alpha by exact enumeration;
* cloglog is checked against the independent GitHub ``pynomial`` port of R ``binom``;
* Pratt's upper limit is the DescTools formula (transcribed) and tracks exact Clopper-Pearson
  to ~1e-3, whereas the DescTools *lower* formula is shown (below) to drift by > 0.1.
"""

import numpy as np
import pytest
import scipy.stats as stats
from cases import ALPHA

import binomcikit as b
from binomcikit import methods as M

N_SMALL = (5, 12, 25)
CHEAP = [
    s.key
    for s in M.REGISTRY.values()
    # randomised smoothing methods (noise Wilson) legitimately violate "contains p-hat" / equivariance
    if s.cost in ("closed-form", "vectorised-root") and s.deterministic
]
# cloglog and the Poisson approximation are inherently asymmetric in (success, failure).
SYMMETRIC = [k for k in CHEAP if k not in ("cloglog", "poisson")]


def exact_coverage(lo, hi, n, points=1500):
    """Min and mean coverage of limits ``(lo, hi)`` over a theta grid (exact enumeration)."""
    k = np.arange(n + 1)
    th = np.linspace(1e-4, 1 - 1e-4, points)
    pm = stats.binom.pmf(k[None, :], n, th[:, None])
    cov = (pm * ((lo[None, :] < th[:, None]) & (th[:, None] < hi[None, :]))).sum(axis=1)
    return cov.min(), cov.mean()


# ------------------------------------------------------------------ registry invariants
@pytest.mark.parametrize("key", CHEAP)
@pytest.mark.parametrize("n", N_SMALL)
def test_table_contract(key, n):
    s = M.REGISTRY[key]
    df = s.table(n, ALPHA)
    assert list(df.columns) == ["x", s.lo, s.hi, "LABB", "UABB", "ZWI"]
    assert len(df) == n + 1
    lo, hi = df[s.lo].to_numpy(), df[s.hi].to_numpy()
    assert np.all(lo >= 0) and np.all(hi <= 1) and np.all(lo <= hi)
    phat = np.arange(n + 1) / n
    assert np.all(lo <= phat + 1e-12) and np.all(hi >= phat - 1e-12)


@pytest.mark.parametrize("key", SYMMETRIC)
def test_equivariance(key):
    """L(x) = 1 - U(n - x): every deterministic method treats successes and failures alike."""
    s = M.REGISTRY[key]
    n = 17
    df = s.table(n, ALPHA)
    lo, hi = df[s.lo].to_numpy(), df[s.hi].to_numpy()
    assert lo == pytest.approx(1 - hi[::-1], abs=1e-8)


@pytest.mark.parametrize("key", CHEAP)
def test_dispatcher_and_single_x_agree_with_table(key):
    s = M.REGISTRY[key]
    n = 15
    full = b.ci(n=n, alpha=ALPHA, method=key)
    assert list(full.columns) == ["x", s.lo, s.hi, "LABB", "UABB", "ZWI"]
    for x in (0, 3, n):
        row = b.ci(x=x, n=n, alpha=ALPHA, method=key)
        assert row.iloc[0, 1] == pytest.approx(full[s.lo][x], abs=1e-12)
        assert row.iloc[0, 2] == pytest.approx(full[s.hi][x], abs=1e-12)


@pytest.mark.parametrize("key", CHEAP)
def test_wider_when_alpha_smaller(key):
    s = M.REGISTRY[key]
    n = 20
    w95 = (s.table(n, 0.05)[s.hi] - s.table(n, 0.05)[s.lo]).to_numpy()
    w99 = (s.table(n, 0.01)[s.hi] - s.table(n, 0.01)[s.lo]).to_numpy()
    assert np.all(w99 >= w95 - 1e-9)


def test_aliases_and_errors():
    assert b.ci(x=3, n=20, method="KL").equals(b.ci(x=3, n=20, method="chernoff"))
    assert b.ci(x=3, n=20, method="ft").equals(b.ci(x=3, n=20, method="freeman-tukey"))
    with pytest.raises(ValueError, match="does not take"):
        b.ci(x=3, n=20, method="pratt", lam=1.0)
    with pytest.raises(ValueError, match="no adjusted"):
        b.ci(x=3, n=20, method="pratt", h=1.0)
    with pytest.raises(TypeError):
        b.ci(x=3, n=20, method="wilson", lam=1.0)
    with pytest.raises(ValueError, match="unknown method"):
        b.ci(x=3, n=20, method="no-such-method")


def test_list_and_describe():
    df = b.list_methods()
    assert len(df) == len(M.REGISTRY) >= 34
    assert {"method", "guarantee", "cost", "reference"} <= set(df.columns)
    d = b.describe_method("KL")
    assert d["key"] == "chernoff" and "kl-ucb" in d["aliases"]
    with pytest.raises(ValueError):
        b.describe_method("nope")


def test_plugged_into_the_shared_metric_engine():
    """New methods flow through compare / recommend / coverage_curve with no extra wiring."""
    cmp = b.compare(3, 20, methods=["wilson", "pratt", "lr-star", "cressie-read", "sterne"])
    assert len(cmp) == 5 and (cmp.width > 0).all()
    rec = b.recommend(15, methods=["wilson", "olc", "hoeffding"])
    hoef = rec[rec.method == "Hoeffding"].iloc[0]
    assert hoef.min_coverage >= 1 - ALPHA - 1e-3  # guaranteed method really guarantees
    cc = b.coverage_curve(15, method="bsc", points=100)
    assert cc.coverage.min() >= 1 - ALPHA - 1e-6


# -------------------------------------------------------------- guaranteed-coverage group
@pytest.mark.parametrize(
    "key",
    ["hoeffding", "chernoff", "bernstein", "empirical-bernstein", "mixture", "normal-mixture"],
)
@pytest.mark.parametrize("n", [8, 20, 40])
def test_guaranteed_methods_never_undercover(key, n):
    s = M.REGISTRY[key]
    df = s.table(n, ALPHA)
    mn, _ = exact_coverage(df[s.lo].to_numpy(), df[s.hi].to_numpy(), n)
    assert mn >= 1 - ALPHA - 1e-9, f"{key} n={n}: min coverage {mn}"


def test_chernoff_never_wider_than_hoeffding():
    n = 30
    k, h = b.cikl(n, ALPHA), b.cihoeffding(n, ALPHA)
    assert np.all((k.UKLC - k.LKLC) <= (h.UHOE - h.LHOE) + 1e-9)


def test_bernstein_satisfies_its_defining_inequality():
    """At each limit the quadratic is tight: n (p - t)^2 = L (2 t (1-t) + 2/3 |p - t|)."""
    n, alp = 25, 0.05
    L = np.log(2 / alp)
    df = b.cibernstein(n, alp)
    for x in range(1, n):
        p = x / n
        for t in (df.LBRN[x], df.UBRN[x]):
            if t <= 0 or t >= 1:  # clamped to [0, 1]: the raw root lies outside the range
                continue
            lhs = n * (p - t) ** 2
            rhs = L * (2 * t * (1 - t) + (2 / 3) * abs(p - t))
            assert lhs == pytest.approx(rhs, rel=1e-9)


def test_kl_limits_satisfy_chernoff_equation():
    n, alp = 30, 0.05
    c = np.log(2 / alp) / n
    df = b.cikl(n, alp)
    for x in range(1, n):
        p = x / n
        for t in (df.LKLC[x], df.UKLC[x]):
            kl = p * np.log(p / t) + (1 - p) * np.log((1 - p) / (1 - t))
            assert kl == pytest.approx(c, rel=1e-8)


def test_empirical_bernstein_needs_two_trials():
    with pytest.raises(ValueError):
        b.ciempbern(1, ALPHA)


# ---------------------------------------------------------------------------- Cressie-Read
def test_cressie_read_reduces_to_wilson_and_lr():
    n = 20
    w, cr1 = b.cisc(n, ALPHA), b.cicressieread(n, ALPHA, lam=1.0)
    assert cr1.LCRD.to_numpy() == pytest.approx(w.LSC.to_numpy(), abs=1e-10)
    assert cr1.UCRD.to_numpy() == pytest.approx(w.USC.to_numpy(), abs=1e-10)
    lr, cr0 = b.cilr(n, ALPHA), b.cicressieread(n, ALPHA, lam=0.0)
    assert cr0.LCRD.to_numpy() == pytest.approx(lr.LLR.to_numpy(), abs=1e-9)
    assert cr0.UCRD.to_numpy() == pytest.approx(lr.ULR.to_numpy(), abs=1e-9)


@pytest.mark.parametrize("lam", [-0.5, 0.0, 2 / 3, 1.0, 2.0])
def test_cressie_read_limits_solve_the_statistic(lam):
    from binomcikit.ext.likelihood import _cr_stat

    n, x = 40, 9
    z2 = stats.norm.ppf(1 - ALPHA / 2) ** 2
    df = b.cicressieread(n, ALPHA, lam=lam)
    for t in (df.LCRD[x], df.UCRD[x]):
        assert float(_cr_stat(np.array(float(x)), n, np.array(t), lam)) == pytest.approx(
            z2, rel=1e-8
        )


def test_cressie_read_rejects_bad_lambda():
    with pytest.raises(ValueError):
        b.cicressieread(10, ALPHA, lam=-1.0)


# ----------------------------------------------------------------------------- r* (higher-order)
def test_rstar_is_close_to_nominal_coverage():
    n = 40
    df = b.cilrstar(n, ALPHA)
    _, mean = exact_coverage(df.LLRS.to_numpy(), df.ULRS.to_numpy(), n, points=2000)
    assert abs(mean - (1 - ALPHA)) < 0.012  # third-order accuracy: tighter than Wilson/LR


def test_rstar_limits_solve_rstar_equals_z():
    from binomcikit.ext.likelihood import _rstar

    n, x = 30, 7
    z = stats.norm.ppf(1 - ALPHA / 2)
    df = b.cilrstar(n, ALPHA)
    assert float(_rstar(x / n, n, df.LLRS[x])) == pytest.approx(z, rel=1e-7)
    assert float(_rstar(x / n, n, df.ULRS[x])) == pytest.approx(-z, rel=1e-7)


# ------------------------------------------------------------------------------------- Pratt
def _descTools_pratt(x, n, alpha):
    """Verbatim transcription of DescTools::BinomCI(method="pratt") for 2 <= x <= n-2."""
    z = stats.norm.ppf(1 - alpha / 2)
    A = ((x + 1) / (n - x)) ** 2
    B = 81 * (x + 1) * (n - x) - 9 * n - 8
    C = -3 * z * np.sqrt(9 * (x + 1) * (n - x) * (9 * n + 5 - z**2) + n + 1)
    D = 81 * (x + 1) ** 2 - 9 * (x + 1) * (2 + z**2) + 1
    upper = 1 / (1 + A * ((B + C) / D) ** 3)
    A = (x / (n - x - 1)) ** 2
    B = 81 * x * (n - x - 1) - 9 * n - 8
    C = 3 * z * np.sqrt(9 * x * (n - x - 1) * (9 * n + 5 - z**2) + n + 1)
    D = 81 * x**2 - 9 * x * (2 + z**2) + 1
    lower = 1 / (1 + A * ((B + C) / D) ** 3)
    return lower, upper


@pytest.mark.parametrize("n", [20, 100])
def test_pratt_upper_matches_desctools_and_tracks_exact(n):
    pr = b.ciprat(n, ALPHA)
    for x in range(2, n - 1):
        _, up = _descTools_pratt(x, n, ALPHA)
        assert pr.UPRA[x] == pytest.approx(up, abs=1e-12)
    cp_lo = stats.beta.ppf(ALPHA / 2, np.arange(1, n + 1), n - np.arange(1, n + 1) + 1)
    cp_hi = stats.beta.ppf(1 - ALPHA / 2, np.arange(n) + 1, n - np.arange(n))
    assert np.abs(pr.LPRA.to_numpy()[1:] - cp_lo).max() < 2e-3
    assert np.abs(pr.UPRA.to_numpy()[:-1] - cp_hi).max() < 2e-3


def test_desctools_pratt_lower_formula_drifts_from_exact():
    """Documents the upstream defect we deliberately do NOT replicate (see ciprat docs)."""
    n = 20
    worst = 0.0
    for x in range(2, n - 1):
        lo, _ = _descTools_pratt(x, n, ALPHA)
        worst = max(worst, abs(lo - stats.beta.ppf(ALPHA / 2, x, n - x + 1)))
    assert worst > 0.1  # DescTools-style lower limit is off by > 0.1 near x = n
    pr = b.ciprat(n, ALPHA)
    assert (
        np.abs(
            pr.LPRA[1:].to_numpy()
            - stats.beta.ppf(ALPHA / 2, np.arange(1, n + 1), n - np.arange(1, n + 1) + 1)
        ).max()
        < 2e-3
    )


def test_pratt_falls_back_to_exact_for_extreme_alpha():
    df = b.ciprat(30, 0.001)  # the closed form is invalid here (d <= 0 at x = 0/1)
    assert np.all(np.isfinite(df.UPRA)) and np.all(df.UPRA >= df.LPRA)


# --------------------------------------------------------------- transforms vs independent ports
def test_cloglog_matches_pynomial_port_of_R_binom():
    pynomial = pytest.importorskip("pynomial")
    if not hasattr(pynomial, "cloglog"):
        pytest.skip("not the GitHub Dpananos/pynomial package")
    n = 20
    df = b.cicloglog(n, ALPHA)
    for x in range(n + 1):
        ref = pynomial.cloglog(x, n)
        assert df.LCLL[x] == pytest.approx(float(ref.lower), abs=1e-12)
        assert df.UCLL[x] == pytest.approx(float(ref.upper), abs=1e-12)


def test_probit_is_a_delta_method_wald_on_the_probit_scale():
    n, x = 30, 11
    p = x / n
    z = stats.norm.ppf(1 - ALPHA / 2)
    q = stats.norm.ppf(p)
    sd = np.sqrt(p * (1 - p) / n) / stats.norm.pdf(q)
    df = b.ciprobit(n, ALPHA)
    assert df.LPRB[x] == pytest.approx(stats.norm.cdf(q - z * sd))
    assert df.UPRB[x] == pytest.approx(stats.norm.cdf(q + z * sd))


@pytest.mark.parametrize("key", ["cloglog", "probit"])
def test_transformed_boundary_rows_are_exact_closed_forms(key):
    n = 20
    df = M.REGISTRY[key].table(n, ALPHA)
    assert df[M.REGISTRY[key].lo][0] == 0.0
    assert df[M.REGISTRY[key].hi][0] == pytest.approx(1 - (ALPHA / 2) ** (1 / n))
    assert df[M.REGISTRY[key].lo][n] == pytest.approx((ALPHA / 2) ** (1 / n))


# ------------------------------------------------------------------- modified Brown-Cai-DasGupta
def test_modified_wilson_equals_wilson_in_the_interior_and_poisson_near_edges():
    n = 40
    mw, w = b.cimodwilson(n, ALPHA), b.cisc(n, ALPHA)
    for x in range(3, n - 2):
        assert mw.LMWS[x] == pytest.approx(w.LSC[x], abs=1e-12)
        assert mw.UMWS[x] == pytest.approx(w.USC[x], abs=1e-12)
    for x in (1, 2):  # n <= 50: x in {1, 2} is repaired
        assert mw.LMWS[x] == pytest.approx(0.5 * stats.chi2.ppf(ALPHA, 2 * x) / n)
        assert mw.UMWS[n - x] == pytest.approx(1 - 0.5 * stats.chi2.ppf(ALPHA, 2 * x) / n)


def test_modified_wilson_widens_the_repaired_range_with_n_over_50():
    n = 60  # x in {1, 2, 3} is repaired for n >= 51
    mw, w = b.cimodwilson(n, ALPHA), b.cisc(n, ALPHA)
    assert mw.LMWS[3] != pytest.approx(w.LSC[3], abs=1e-9)
    assert mw.LMWS[4] == pytest.approx(w.LSC[4], abs=1e-12)


def test_modified_jeffreys_boundary_rows():
    n = 20
    mj, jf = b.cimodjeffreys(n, ALPHA), b.ci(n=n, alpha=ALPHA, method="jeffreys")
    assert mj.LMJF[0] == 0 and mj.LMJF[1] == 0 and mj.UMJF[n] == 1 and mj.UMJF[n - 1] == 1
    assert mj.UMJF[0] == pytest.approx(1 - (ALPHA / 2) ** (1 / n))
    assert mj.LMJF[n] == pytest.approx((ALPHA / 2) ** (1 / n))
    for x in range(2, n - 1):
        assert mj.LMJF[x] == pytest.approx(jf.LBAQ[x]) and mj.UMJF[x] == pytest.approx(jf.UBAQ[x])


# ------------------------------------------------------------------------- Poisson / Freeman-Tukey / SOC
def test_garwood_formula_and_conservative_upper():
    n = 50
    df = b.cipoisson(n, ALPHA)
    x = 4
    assert df.LPOI[x] == pytest.approx(0.5 * stats.chi2.ppf(ALPHA / 2, 2 * x) / n)
    assert df.UPOI[x] == pytest.approx(0.5 * stats.chi2.ppf(1 - ALPHA / 2, 2 * x + 2) / n)
    cp = b.ci(n=n, alpha=ALPHA, method="exact")
    assert np.all(df.UPOI.to_numpy()[: n // 2] >= cp.UEX.to_numpy()[: n // 2] - 1e-9)


def test_freeman_tukey_limits_invert_the_transform():
    from binomcikit.ext.closed_form import _ft

    n = 30
    z = stats.norm.ppf(1 - ALPHA / 2)
    df = b.cifreemantukey(n, ALPHA)
    for x in range(2, n - 1):
        t0 = _ft(float(x), n)
        assert _ft(df.LFTK[x] * n, n) == pytest.approx(t0 - z / np.sqrt(n + 0.5), abs=1e-9)
        assert _ft(df.UFTK[x] * n, n) == pytest.approx(t0 + z / np.sqrt(n + 0.5), abs=1e-9)


def test_soc_formula_and_contains_phat():
    n, x = 30, 6
    k = stats.norm.ppf(1 - ALPHA / 2)
    eta = k**2 / 3 + 1 / 6
    g1 = -((13 / 18) * k**2 + 17 / 18)
    g2 = k**2 / 18 + 7 / 36
    p = x / n
    mid = (x + eta) / (n + 2 * eta)
    half = k * np.sqrt(p * (1 - p) + (g1 * p * (1 - p) + g2) / n) / np.sqrt(n)
    df = b.cisoc(n, ALPHA)
    assert df.LSOC[x] == pytest.approx(min(mid - half, p))
    assert df.USOC[x] == pytest.approx(max(mid + half, p))
    assert np.all(df.LSOC <= np.arange(n + 1) / n + 1e-12)


def test_arcsine_shifted_matches_desctools_and_dbci():
    """DescTools ``BinomCI(84, 101, method="arcsine")`` (recorded in DBCI's test data, R output) and the DBCI package."""
    lo, hi = b.interval(84, 101, 0.05, "arcsine-shifted", clamp=False)
    assert lo == pytest.approx(0.750073773401545, abs=1e-12)
    assert hi == pytest.approx(0.895920193052064, abs=1e-12)
    dbci = pytest.importorskip("diff_binom_confint")
    for n in (20, 101):
        lows, highs = b.limits(n, 0.05, "arcsine-shifted", clamp=False)
        for x in range(n + 1):
            r = dbci.compute_confidence_interval(x, n, 0.95, "arcsine")
            if not np.isnan(r.lower_bound):
                assert lows[x] == pytest.approx(r.lower_bound, abs=1e-12)
            if not np.isnan(r.upper_bound):
                assert highs[x] == pytest.approx(r.upper_bound, abs=1e-12)


# DescTools::BinomCI(84, 101, method = m) at 95% (R output, as stored in DBCI's test data): an independent oracle
DESCTOOLS_84_101 = {
    "wilson": (0.746887910813618, 0.892172254445884),
    "wald": (0.758715556204123, 0.90465078042954),
    "agresti-coull": (0.745915064553858, 0.893145100705643),
    "jeffreys": (0.749873617953982, 0.894811373510988),
    "modified-wilson": (0.746887910813618, 0.892172254445884),
    "modified-jeffreys": (0.749873617953982, 0.894811373510988),
    "exact": (0.744242147979102, 0.898781606243792),
    "logit": (0.745803605584389, 0.892722014912055),
    "midp": (0.749191662254284, 0.895391744074331),
    "lr": (0.750858699977225, 0.895899772033449),
    "blaker": (0.744842147979099, 0.894571606243811),
}


@pytest.mark.parametrize("method", sorted(DESCTOOLS_84_101))
def test_matches_desctools_binomci_at_84_of_101(method):
    lo, hi = b.interval(84, 101, 0.05, method)
    # R's uniroot default tolerance is ~1.2e-4, so the root-found methods agree to that, the rest to 1e-6
    tol = 1e-4 if method in ("midp", "blaker", "lr") else 1e-6
    assert lo == pytest.approx(DESCTOOLS_84_101[method][0], abs=tol), method
    assert hi == pytest.approx(DESCTOOLS_84_101[method][1], abs=tol), method
