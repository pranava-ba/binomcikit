# Upstream reports: DRAFTS (nothing has been filed)

> Drafted 2026-10-03 from `planning/COMPETITOR_REPOS.md`. **Every item below except #8 was reproduced on 2026-10-03 and none has been sent anywhere.**
> Filing is outward-facing (it publishes text under your GitHub account), so each draft waits for your approval, and you may want to
> edit tone and wording first. Runnable repros: `planning/upstream_repro/dbci_repros.py` (DBCI; identical on PyPI 0.1.0 and `main`
> at `39b0fdb`). Duplicate check done against each repo's issue list on 2026-10-03: no existing issue covers any of these.

Environment used for every repro: Windows 11 (10.0.26200), Python 3.13.5, numpy 2.3.2, scipy 1.16.1, numba 0.65.1 (not used by these calls).

| # | Target | Title | Severity | Evidence strength |
|--:|---|---|---|---|
| 1 | DeepPSP/DBCI | `modified-wilson` / `modified-newcombe`: upper limit below the lower limit for x close to n | high (wrong answer, no error) | code reading + numeric repro |
| 2 | DeepPSP/DBCI | `make_risk_report` raises `UnicodeEncodeError` on Windows | low | reproduced in their own test |
| 3 | DeepPSP/DBCI | `mee` / `miettinen-nurminen` / `blaker` limits are only accurate to ~1e-5 | low (enhancement) | numeric repro; cause hedged |
| 4 | nolanbconaway/binoculars | `binomial_confidence(0, n, method="clopper-pearson")` returns a NaN lower limit | medium | numeric repro |
| 5 | nolanbconaway/binoculars | enhancement: `z` is hard-coded to 1.96 | very low | numeric |
| 6 | DeepPSP/DBCI | `pratt`: lower limit is off by up to 0.13 from the exact limit its own upper formula tracks to <1e-3 | high (wrong answer, no error) | numeric; one offset (`n-x-1` for `n-x+1`) restores the accuracy |
| 7 | DeepPSP/DBCI | `witting`: nominal 95% interval covers only ~90%, and `x = 0` can raise `ValueError` | high | simulation (coverage is the defining property) |
| 8 | AndriSignorell/DescTools | `BinomCI(method="pratt")` lower limit (same formula as #6) | high | DescTools' own output as captured in DBCI's test data; **R not run here** |
| — | statsmodels | *no report needed* | — | see the last section |

**Repo health, so you can judge the odds of a reply:** DBCI is active (69 commits in the last 12 months, bug template, a maintainer who
closed all three previous issues). binoculars has had no commit since 2021-10 and one issue ever (closed), so #4–#5 are likely
to sit unanswered; they are still accurate, and #4 would be a one-line fix if anyone forks it.

---

## 1. DBCI — `modified-wilson` upper limit is wrong for x near n

Target: https://github.com/DeepPSP/DBCI/issues/new?template=bug_report.md · Labels: bug

**Title:** `[BUG]` `modified-wilson` (and its alias `modified-newcombe`) gives upper < lower for x close to n

**Describe the bug**

For observed counts close to `n_total`, the `modified-wilson` upper limit is the *lower*-tail expression without the `1 -`, so it
comes out smaller than the lower limit.

```python
from diff_binom_confint import compute_confidence_interval

for x in (1, 59):
    r = compute_confidence_interval(x, 60, 0.95, "modified-wilson")
    print(x, r.lower_bound, r.upper_bound)
# 1  0.000422  0.088551
# 59 0.911449  0.000422      <- upper (0.000422) < lower (0.911449)
```

By symmetry the interval for x = 59 should be the mirror image of the one for x = 1, i.e. upper = 1 − 0.000422 = 0.999578.

**Where it comes from** (`diff_binom_confint/_binom_confint.py`, the `"modified-wilson"` / `"modified-newcombe"` branch):

```python
if (n_total <= 50 and n_negative in [1, 2]) or (n_total >= 51 and n_negative in [1, 2, 3]):
    upper = 0.5 * qchisq(margin, 2 * n_negative, 0) / n_total      # <- looks like it needs `1 -`
```

The lower-limit branch just above it (`lower = 0.5 * qchisq(margin, 2 * n_positive, 0) / n_total`) is the right shape for a
lower limit; for the upper limit with `n_negative` failures the mirrored expression is
`1 - 0.5 * qchisq(margin, 2 * n_negative, 0) / n_total`. (This matches the usual statement of the modified Wilson interval,
where the boundary adjustment is applied symmetrically; please check it against Brown, Cai & DasGupta (2001) before relying on my reading.)

**OS:** Windows 11 · **Package Version:** 0.1.0 (PyPI) and `master` at `39b0fdb` — same result · **Python:** 3.13.5 · **Numpy:** 2.3.2 ·
**SciPy:** 1.16.1 · **Pandas:** 2.3.3

**Suggested fix:** add `1 -` (and a regression test asserting `upper(x, n) == 1 - lower(n - x, n)` for the modified-Wilson family).

---

## 2. DBCI — `make_risk_report` fails on Windows with `UnicodeEncodeError`

Target: same template.

**Title:** `[BUG]` `make_risk_report`: `UnicodeEncodeError` when writing the `.tex` file on Windows

**Describe the bug**

`make_risk_report` writes the LaTeX table with `Path.write_text(...)` and no `encoding`, so on Windows (default code page cp1252) it
raises as soon as the text contains a character outside that code page.

```text
diff_binom_confint\_applications.py:341: in make_risk_report
    save_path.with_suffix(".tex").write_text(ret_lines)
UnicodeEncodeError: 'charmap' codec can't encode characters in position 787-788: character maps to <undefined>
```

Reproduce with the project's own test: `python -m pytest test/test_applications.py::test_make_risk_report` (fails on Windows; passes with
`PYTHONUTF8=1`).

**OS:** Windows 11 · **Package Version:** `master` at `39b0fdb` · **Python:** 3.13.5

**Suggested fix:** `write_text(ret_lines, encoding="utf-8")`.

---

## 3. DBCI — `mee`, `miettinen-nurminen` and `blaker` limits carry ~1e-5 error (enhancement)

Target: same template, or a normal issue. Worth sending only if you want it; low priority.

**Title:** `mee` / `miettinen-nurminen` / `blaker`: limits are only accurate to about 1e-5

**Describe**

For `(x1, n1, x2, n2) = (56, 70, 48, 80)` at 95%:

| method | DBCI | root-found on the same statistic | Z² residual at DBCI's limits |
|---|---|---|---|
| `mee` | [0.053340, 0.337720] | [0.053334, 0.337729] | 3.1e-4, 5.5e-4 |
| `miettinen-nurminen` | [0.052830, 0.338170] | [0.052830, 0.338173] | 1.5e-5, 1.7e-4 |

(Z² is the score statistic with the restricted MLE variance; at an exact limit it equals z² = 1.96².) For single-proportion
`blaker`, the code walks the limit in `tol = 1e-5` steps (`while _acceptbin(...) < 1 - conf_level: lower += tol`), so limits are
within 1e-5 of the true ones; at n = 20 the largest gap over x = 1..19 is 9.9e-6.

These are small and the intervals are still usable, so this is a precision enhancement rather than a bug. I haven't looked at how the
score search is implemented, so I can't say whether it is the same fixed step. A bracketed root-finder (`scipy.optimize.brentq`)
on the same function would give limits to full double precision; the restricted MLE is the unique maximiser of a concave
log-likelihood in one variable, so it is safe to solve by bracketing.

Repro: `planning/upstream_repro/dbci_repros.py`, sections 2 and 3 (self-contained; uses only scipy for the reference values).

---

## 4. binoculars — Clopper–Pearson lower limit is NaN at `x = 0`

Target: https://github.com/nolanbconaway/binoculars/issues/new

**Title:** `binomial_confidence(0, n, method="clopper-pearson")` returns NaN for the lower limit

**Describe the bug**

```python
import binoculars

print(binoculars.binomial_confidence(0 / 10, 10, method="clopper-pearson"))
# (nan, 0.30850293008372687)
```

The lower limit of the Clopper–Pearson interval is exactly 0 when `x = 0`; the function returns NaN (the underlying
`scipy.stats.beta.ppf` is called with a zero shape parameter). I saw the same for n = 1, 2, 1000 and 100000 (x = 0). Presumably the
mirror case (`x = n`, upper limit) is intended to be 1 and should be checked too.

**Package version:** 0.1.3 · **Python:** 3.13.5 · **SciPy:** 1.16.1 · **Numpy:** 2.3.2

**Suggested fix:** special-case `p == 0` (lower = 0.0) and `p == 1` (upper = 1.0).

---

## 5. binoculars — the confidence level is hard-coded as `z = 1.96` (enhancement)

**Title:** Allow a confidence level (or exact `z`) instead of the 1.96 default

`binomial_confidence(p, n, tail=None, z=1.96, method=...)` takes `z`, defaulting to 1.96. The exact 97.5% normal quantile is
1.959964, so every "95%" interval differs from the exact one in the 6th decimal place: Wilson at 50/100 gives a lower limit of
0.403830 against the exact 0.403832; across 20 test cases (n up to 10^5) the largest difference from a 30-digit reference is
8.3e-6. An `alpha`/`confidence` argument (or defaulting `z` to `scipy.stats.norm.ppf(0.975)`) would remove it. Fine to close as
"works as documented".

---

## 6. DBCI — `pratt` lower limit does not approximate the exact limit

Target: same template · Labels: bug

**Title:** `[BUG]` `pratt`: lower limit differs from the Clopper–Pearson limit by up to 0.13 (the upper limit is accurate to < 1e-3)

**Describe the bug**

Pratt's method is a closed-form *normal approximation to the exact (Clopper–Pearson) limits*. In `compute_confidence_interval(..., "pratt")`
the upper limit does track the exact limit (max error 8.6e-4 at n = 20, 1.7e-4 at n = 101, 3.5e-5 at n = 500, interior x), but the
lower limit does not:

| n | max abs error of the upper limit | max abs error of the lower limit |
|--:|--:|--:|
| 20 | 8.6e-4 | **1.3e-1** |
| 101 | 1.7e-4 | **3.3e-2** |
| 500 | 3.5e-5 | **7.0e-3** |

```python
from scipy import stats
from diff_binom_confint import compute_confidence_interval

r = compute_confidence_interval(84, 101, 0.95, "pratt")
print(r.lower_bound, stats.beta.ppf(0.025, 84, 101 - 84 + 1))   # 0.7617  vs  0.7442 (exact)
```

The two limits are also not mirror images (`L(x) != 1 - U(n - x)`, max difference 2.9e-2 at n = 101), although the binomial problem is
symmetric.

**Where it comes from** (`_binom_confint.py`, the final `else` of the `"pratt"` branch):

```python
a = (n_positive / (n_negative - 1)) ** 2
b = 81 * n_positive * (n_negative - 1) - 9 * n_total - 8
c = 3 * zeta * np.sqrt(9 * n_positive * (n_negative - 1) * (9 * n_total + 5 - zeta**2) + n_total + 1)
d = 81 * n_positive**2 - 9 * n_positive * (2 + zeta**2) + 1
lower = 1 / (1 + a * ((b + c) / d) ** 3)
```

Replacing `(n_negative - 1)` by `(n_negative + 1)` in `a`, `b` and `c` (leaving `d` as is) brings the maximum error against the exact lower limit to
8.6e-4 (n = 20) and 1.7e-4 (n = 101), i.e. the same accuracy as the upper limit. I arrived at that by testing variants against the exact limit, not
from Pratt's paper, so please check it against Pratt (1968, JASA 63, 1457) before applying it. (Mirroring the upper limit, `L(x) = 1 - U(n - x)`, gives
the same accuracy.)

**Package Version:** 0.1.0 (PyPI) and `master` at `39b0fdb` — same result. Repro: `planning/upstream_repro/dbci_repros.py`, section 5.

---

## 7. DBCI — `witting` interval covers only about 90% at nominal 95%

Target: same template · Labels: bug

**Title:** `[BUG]` `witting`: the nominal 95% interval has about 90% coverage (looks like α instead of α/2 per tail); `x = 0` can raise `ValueError`

**Describe the bug**

Witting's randomised interval is meant to have *exactly* the nominal coverage at every θ. Simulating the DBCI implementation
(`n = 30`, 4000 binomial draws per θ, a fresh random call per draw):

| θ | observed coverage of the "95%" interval |
|--:|--:|
| 0.1 | 0.901 |
| 0.3 | 0.900 |
| 0.5 | 0.899 |

That is the coverage of a **90%** interval, which is what you get if each tail is given probability `1 - conf_level` instead of
`(1 - conf_level) / 2` (in the code: `_qbinom_abscont(1 - _conf_level, ...)`). An independent implementation of the randomised
interval gives 0.949–0.952 at the same θ and n.

Separately, some draws at `x = 0` raise `ValueError: f(a) and f(b) must have different signs` from `uniroot` inside `_qbinom_abscont`
(2 of 4000 calls at θ = 0.1; this is the same family as the closed issue #5, `compute_confidence_interval(2, 2, conf_level=0.975, method="witting")`).

**Package Version:** 0.1.0 (PyPI) and `master` at `39b0fdb` · Repro: `planning/upstream_repro/dbci_repros.py`, section 6 (about a minute).

**Caveat:** I compared against my own randomised implementation, not against Witting's text; the coverage figures do not depend on it, because
coverage is what a "95% interval" promises.

---

## 8. DescTools — `BinomCI(method = "pratt")` lower limit (same formula as DBCI #6)

Target: https://github.com/AndriSignorell/DescTools/issues/new · **I could not run R here**, so this rests on DescTools' output as stored in
DBCI's test data (`test/test-data/example-84-101.csv`, generated by `DescTools::BinomCI(84, 101, method = m)` according to DBCI's README).

**Title:** `BinomCI(x, n, method = "pratt")`: lower limit is far from the exact limit (0.7617 vs 0.7442 for 84/101)

```r
library(DescTools)
BinomCI(84, 101, method = "pratt")     # lwr.ci recorded as 0.7617 in DBCI's test data
BinomCI(84, 101, method = "clopper-pearson")   # lwr.ci 0.7442 (same file)
```

The recorded `pratt` upper limit is 0.8988, equal to the Clopper–Pearson upper limit to four digits, while the lower limit differs by 0.017.
The DBCI formula in #6 reproduces the recorded DescTools numbers exactly, so the same offset (`n - x - 1` where `n - x + 1` is needed) is the
likely cause. Please run the R lines above before filing; I have not.

(DescTools' `witting` is the source DBCI ported; whether it has the same 90% coverage is **not tested** — R unavailable.)

---

## Not reported, and why

* **statsmodels** — `confint_proportions_2indep(..., method="score")` (compare="diff") is wrong in 0.14.5 and 0.15.0 (the
  Miettinen–Nurminen constrained-MLE cubic uses `count0 * diff` instead of `nobs0 * diff`), but `main` already contains the fix and
  the issue is closed upstream (statsmodels #10269). I confirmed independently that the corrected cubic equals a brute-force
  likelihood maximisation to six digits. Nothing for us to file.
* **DescTools `witting`** — not tested (needs R); DBCI's version is reported in #7 on the strength of a simulation.
* **pynomial, astropy, DBCI `arcsine`/`logit` boundary** — investigated; the deviations are conventions or a different
  published variant, not defects (`planning/COMPETITOR_REPOS.md`, section 5).
* **A request for a DBCI release** — PyPI 0.1.0 is from 2025-08-15 and `main` has merged fixes since (the Wang plateau logic,
  build and CI changes). A friendly "any plans for 0.1.1?" would be fine as a comment on one of the issues above, not a separate issue.

## Before filing

1. Re-run `python planning/upstream_repro/dbci_repros.py` against the then-current DBCI (they may have fixed it by then).
2. Decide whether to file as yourself (`pranava-ba`); the `gh` CLI is authenticated, so I can file them for you on request, one at a time.
3. Do not mention binomcikit unless you want to: nothing here depends on it, and the reports read as ordinary bug reports.
