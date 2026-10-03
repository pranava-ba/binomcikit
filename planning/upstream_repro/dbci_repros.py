"""Self-contained repros for the DBCI reports in planning/UPSTREAM_REPORTS_DRAFT.md.

Run against DBCI 0.1.0 (PyPI) and against `main` (commit 39b0fdb): the behaviour is identical.

    python dbci_repros.py
"""

import math

import diff_binom_confint as d
import numpy as np
from scipy import optimize

print("diff_binom_confint from", d.__file__)

# ---------------------------------------------------------------- report 1: modified-wilson
print("\n1) modified-wilson upper limit (n = 60)")
for x in (1, 59):
    r = d.compute_confidence_interval(x, 60, 0.95, "modified-wilson")
    print(f"   x={x:2d}: lower={r.lower_bound:.6f} upper={r.upper_bound:.6f}")
r1 = d.compute_confidence_interval(1, 60, 0.95, "modified-wilson")
r59 = d.compute_confidence_interval(59, 60, 0.95, "modified-wilson")
print("   by symmetry upper(59) should equal 1 - lower(1) =", round(1 - r1.lower_bound, 6))
print("   actual upper(59) < lower(59):", r59.upper_bound < r59.lower_bound)

# ----------------------------------------------- report 2: score intervals (Mee, Miettinen-Nurminen)
print("\n2) score intervals: does Z^2(limit) equal z^2?  (x1, n1, x2, n2) = (56, 70, 48, 80)")
x1, n1, x2, n2 = 56, 70, 48, 80
z2 = 1.959963984540054**2


def restricted_mle(delta):
    """Maximise the restricted log-likelihood in p1 (it is concave), p2 = p1 - delta."""
    lo, hi = max(0.0, delta), min(1.0, 1.0 + delta)

    def negll(p):
        return -(
            x1 * math.log(p)
            + (n1 - x1) * math.log(1 - p)
            + x2 * math.log(p - delta)
            + (n2 - x2) * math.log(1 - p + delta)
        )

    p1 = optimize.minimize_scalar(
        negll, bounds=(lo + 1e-12, hi - 1e-12), method="bounded", options={"xatol": 1e-14}
    ).x
    return p1, p1 - delta


def z2_at(delta, factor):
    q1, q2 = restricted_mle(delta)
    var = factor * (q1 * (1 - q1) / n1 + q2 * (1 - q2) / n2)
    return (x1 / n1 - x2 / n2 - delta) ** 2 / var


for name, factor in (("mee", 1.0), ("miettinen-nurminen", (n1 + n2) / (n1 + n2 - 1))):
    r = d.compute_difference_confidence_interval(x1, n1, x2, n2, 0.95, name)
    lo, hi = r.lower_bound, r.upper_bound
    # exact limits from root-finding on the same statistic
    est = x1 / n1 - x2 / n2
    exact_lo = optimize.brentq(lambda t: z2_at(t, factor) - z2, -0.99, est, xtol=1e-14)
    exact_hi = optimize.brentq(lambda t: z2_at(t, factor) - z2, est, 0.99, xtol=1e-14)
    print(
        f"   {name:20s} DBCI [{lo:.6f}, {hi:.6f}]  root-found [{exact_lo:.6f}, {exact_hi:.6f}]"
        f"  |dZ^2| at DBCI limits = {abs(z2_at(lo, factor) - z2):.1e}, {abs(z2_at(hi, factor) - z2):.1e}"
    )

# ------------------------------------------------------------- report 3: Blaker resolution
print("\n3) Blaker limits move in steps of 1e-5 (n = 20)")
exact_gap = []
try:
    from binomcikit.ci.blaker import _blaker_table  # optional: only to show the exact limits

    lo_b, hi_b = _blaker_table(20, 0.05)
    for x in range(1, 20):
        r = d.compute_confidence_interval(x, 20, 0.95, "blaker")
        exact_gap.append(max(abs(r.lower_bound - lo_b[x]), abs(r.upper_bound - hi_b[x])))
    print(f"   largest |DBCI - exact| over x = 1..19: {max(exact_gap):.2e}")
except ImportError:
    print("   (binomcikit not installed: skipped; the loop in _binom_confint.py uses tol = 1e-5)")

# ----------------------------------------------------- report 4: Windows encoding (informational)
print("\n4) make_risk_report writes LaTeX with Path.write_text(...) and no encoding;")
print("   on Windows (cp1252) that raises UnicodeEncodeError unless PYTHONUTF8=1 is set.")
print("   Reproduce: python -m pytest test/test_applications.py::test_make_risk_report")
print("   Location: diff_binom_confint/_applications.py, line 341.")

# --------------------------------------------------------------------- report 5: Pratt lower limit
print("\n5) Pratt lower limit vs the exact Clopper-Pearson limit (alpha = 0.05)")
from scipy import stats  # noqa: E402

for n in (20, 101, 500):
    worst_lo = worst_hi = 0.0
    for x in range(2, n - 1):
        r = d.compute_confidence_interval(x, n, 0.95, "pratt")
        worst_lo = max(worst_lo, abs(r.lower_bound - stats.beta.ppf(0.025, x, n - x + 1)))
        worst_hi = max(worst_hi, abs(r.upper_bound - stats.beta.ppf(0.975, x + 1, n - x)))
    print(f"   n={n:3d}: max |Pratt - exact|  lower {worst_lo:.1e}   upper {worst_hi:.1e}")
r = d.compute_confidence_interval(84, 101, 0.95, "pratt")
print(
    f"   84/101: DBCI lower {r.lower_bound:.4f}; exact Clopper-Pearson lower {stats.beta.ppf(0.025, 84, 18):.4f}"
)
print("   (DescTools::BinomCI(84, 101, method='pratt') is recorded in DBCI's test-data file")
print("    example-84-101.csv with the same lower limit, 0.7617.)")

# ---------------------------------------------------------------------- report 6: Witting coverage
print("\n6) Witting: coverage of the nominal 95% interval (n = 30; 4000 draws per theta)")
rng = np.random.default_rng(1)
n = 30
for theta in (0.1, 0.3, 0.5):
    cov = ok = 0
    errs = set()
    for x in rng.binomial(n, theta, 4000):
        try:
            r = d.compute_confidence_interval(int(x), n, 0.95, "witting")
            cov += r.lower_bound <= theta <= r.upper_bound
            ok += 1
        except ValueError:
            errs.add(int(x))
    print(f"   theta={theta}: coverage {cov / ok:.3f}   (ValueError for x in {sorted(errs)})")
print("   expected about 0.95; about 0.90 means each tail uses alpha rather than alpha / 2.")
