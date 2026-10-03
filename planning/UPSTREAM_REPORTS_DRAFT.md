# Upstream reports: DRAFTS (nothing has been filed)

> Drafted 2026-10-03 from `planning/COMPETITOR_REPOS.md`. **Every item below was reproduced on 2026-10-03 and none has been sent anywhere.**
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

## Not reported, and why

* **statsmodels** — `confint_proportions_2indep(..., method="score")` (compare="diff") is wrong in 0.14.5 and 0.15.0 (the
  Miettinen–Nurminen constrained-MLE cubic uses `count0 * diff` instead of `nobs0 * diff`), but `main` already contains the fix and
  the issue is closed upstream (statsmodels #10269). I confirmed independently that the corrected cubic equals a brute-force
  likelihood maximisation to six digits. Nothing for us to file.
* **DBCI `pratt`, `witting`, and DescTools Pratt/Witting** — earlier sessions recorded discrepancies against binomcikit. I did not
  re-derive in this pass which side matches the primary sources, so they are not drafted. Re-derive first (primary text for Pratt
  1968 and Witting 1985) before filing anything.
* **pynomial, astropy, DBCI `arcsine`/`logit` boundary** — investigated; the deviations are conventions or a different
  published variant, not defects (`planning/COMPETITOR_REPOS.md`, section 5).
* **A request for a DBCI release** — PyPI 0.1.0 is from 2025-08-15 and `main` has merged fixes since (the Wang plateau logic,
  build and CI changes). A friendly "any plans for 0.1.1?" would be fine as a comment on one of the issues above, not a separate issue.

## Before filing

1. Re-run `python planning/upstream_repro/dbci_repros.py` against the then-current DBCI (they may have fixed it by then).
2. Decide whether to file as yourself (`pranava-ba`); the `gh` CLI is authenticated, so I can file them for you on request, one at a time.
3. Do not mention binomcikit unless you want to: nothing here depends on it, and the reports read as ordinary bug reports.
