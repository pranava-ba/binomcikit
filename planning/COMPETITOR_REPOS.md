# Competitor repositories: activity, footprint, accuracy, SWOT

> Measured **2026-10-03** on Windows 11, Python 3.13.5, one machine. Raw data and the scripts that produced it are in
> `benchmarks/competitors/` (re-runnable; data in `benchmarks/competitors/data/`). Clones were made into a scratch directory
> outside the repo and are **not** committed. Anything not measured is marked *not measured*; there are no estimates in here.
>
> **Corrections made after the first version of this report (same day):** (1) the `pynomial` that the benchmarks actually call is
> `Dpananos/pynomial`, installed from GitHub; the first version described the unrelated PyPI project of the same name. (2) The
> `pynomial` / `astropy` "parity gaps" were harness mistakes, not defects (section 5). (3) `binoculars`' Clopper–Pearson problem is a
> NaN *lower* limit at x = 0, not NaN in both limits.

## 0. What changed our picture (read this first)

1. **DBCI is alive, and its scope includes a whole problem we did not cover.** Its method catalogue is **16 distinct
   single-proportion methods** (19 names: `wilson`, `wilson-cc` and `modified-wilson` are aliases of the `newcombe` forms) **and 15
   distinct two-proportion methods** (20 names; `wilson`, `wilson-cc`, `score`, `score-cc` and `brown-li-jeffrey` are aliases), the
   same in PyPI 0.1.0 and in `main` (commit `39b0fdb`, 2026-09-02; last push 2026-09-28). The earlier note of "16" was right; the
   difference-of-proportions half had not been recorded. binomcikit had **no two-proportion inference**; as of this pass it has
   seven (section 7, item 1).
2. **Everyone we compared against is accurate to ~1e-16 on Wilson and Clopper–Pearson, except `binoculars`** (about 1e-6 to 8e-6
   because its default `z` is the hard-coded 1.96; and its Clopper–Pearson lower limit is NaN at `x = 0`). Accuracy is not where we
   differ; scope, evaluation tooling and speed are.
3. **Where we lose, plainly.** `bk.ci()` through a DataFrame is still slower than statsmodels/astropy for closed-form methods at
   small `n` (168 µs vs 97 µs for Wilson at n = 100; about three-quarters of the time is pandas building the frame). We import
   more slowly than `scipy.stats` (1.22 s vs 0.85 s) and `astropy.stats` (0.29 s) because we depend on pandas. And our adoption is
   the smallest in the table (13 downloads/month; PyPI still serves a stale 0.0.5).
4. **Licence:** binomcikit is GPL-3.0 (inherited from the R package). Every maintained Python competitor is MIT or BSD. Whether that
   limits adoption is a decision for the maintainer; it is flagged here, not recommended.
5. **statsmodels' two-proportion `score` interval is wrong in the released versions and already fixed on `main`.** In 0.14.5 and
   0.15.0 the Miettinen–Nurminen constrained-MLE cubic uses `count0 * diff` where the paper has `N0 * diff`
   (upstream issue #10269, closed; `main` now has `nobs0 * diff`). We confirmed it independently: with `nobs0` the closed form
   reproduces a brute-force maximisation of the restricted likelihood to six digits, and with `count0` it does not. The released
   versions return wrong limits for some tables and raise `ValueError` for others (for example 7/10 vs 3/12, or 0/10 vs 0/10).
   Nothing to report upstream.

## 1. Scope: what was examined

| Package | Repo | Cloned @ | Role |
|---|---|---|---|
| DBCI (`diff-binom-confint`) | DeepPSP/DBCI | `39b0fdb` (2026-09-02) | closest competitor |
| binomial_cis | TRI-ML/binomial_cis | `8a2d6eb` (2025-04-23) | exact/optimal intervals |
| pynomial | Dpananos/pynomial | `4042798` (2025-08-29) | the one benchmarked; **GitHub only, not on PyPI** |
| pynomial (PyPI name) | Silver-Creek/pynomial | `aeab980` (2020-10-29) | unrelated package that owns the PyPI name; README is a stub |
| binoculars | nolanbconaway/binoculars | `9b8a7d7` (2021-07-03) | 4 simple intervals |
| confseq | gostevehoward/confseq | `5ffe733` (2026-01-06) | betting / confidence sequences |
| statsmodels, astropy, scipy | upstream | API metrics only | the default tools people actually use |
| DescTools (R) | AndriSignorell/DescTools | API metrics only | `BinomCI` has ~16 methods |

GitHub search (`gh search repos`; queries: binomial confidence interval, clopper-pearson, wilson score interval, pynomial,
binomial_cis, confseq) found **no additional maintained Python package** with comparable scope; hits were single-file student
projects (0–1 stars). Not looked at in this pass: `binom`, `PropCIs`, `exactci`, `binGroup` (R, CRAN-only) and commercial tools.

## 2. Activity and usage (2026-10-03)

Source: `benchmarks/competitors/collect.py` (GitHub REST API via `gh`, PyPI JSON, pypistats.org). "12 m" = since 2025-10-03.
Downloads are PyPI last-30-days from pypistats and include mirrors and bots.

| Package | Stars | Forks | Contributors | Commits 12 m | Last push | PyPI latest (date) | Releases 12 m | Open / closed issues | Open / closed PRs | Downloads / month | Licence |
|---|--:|--:|--:|--:|---|---|--:|--:|--:|--:|---|
| DBCI | 2 | 0 | 4 | 69 | 2026-09-28 | 0.1.0 (2025-08-15) | 0 | 0 / 3 | 1 / 32 | 74 | MIT |
| binomial_cis | 15 | 2 | 4 | 0 | 2025-04-23 | 0.0.12 (2025-04-23) | 0 | 0 / 0 | 0 / 6 | 299 | MIT |
| pynomial (Dpananos) | 0 | 0 | 1 | 0 | 2025-08-29 | not on PyPI | n/a | 0 / 0 | 0 / 0 | n/a | none declared |
| binoculars | 4 | 1 | 1 | 0 | 2021-10-08 | 0.1.3 (2021-07-03) | 0 | 0 / 1 | 0 / 5 | 74 | MIT |
| confseq | 85 | 4 | 3 | 1 | 2026-01-07 | 0.0.11 (2023-01-26) | 0 | 1 / 3 | 0 / 19 | 543 | MIT |
| DescTools (R) | 95 | 21 | 9 | 19 | 2026-01-26 | n/a (CRAN) | n/a | 27 / 121 | 2 / 33 | n/a | not declared via API |
| statsmodels | 11,668 | 3,614 | 589 | 1,827 | 2026-10-02 | 0.15.0 (2026-08-27) | 2 | 2,629 / 3,062 | 181 / 4,483 | 31,394,993 | BSD-3 |
| astropy | 5,324 | 2,187 | 646 | 1,750 | 2026-10-02 | 8.0.1 (2026-07-05) | 11 | 1,272 / 5,571 | 152 / 13,482 | 2,401,598 | BSD-3 |
| scipy | 15,072 | 5,985 | 1,997 | 2,401 | 2026-10-02 | 1.18.1 (2026-08-21) | 9 | 1,439 / n/a | 423 / n/a | 286,276,241 | BSD-3 |
| **binomcikit** | 1 | 0 | 1 | 27 | 2026-09-28 | 0.0.5 (2025-02-23) | 0 | 0 / 0 | 0 / 0 | 13 | GPL-3.0 |

(The unrelated PyPI `pynomial` by Silver-Creek: 0 stars, 3 contributors, last push 2020-10-29, GPL-3.0, 9 downloads/month.)

Bus factor from the clones' full history (top contributor's share of commits): DBCI 275/304 (90%), binomial_cis 63/74 (85%),
confseq 191/227 (84%), binoculars 21/21 (100%), pynomial (Dpananos) 17/17 (100%), binomcikit 72/72 (100%, `git shortlog`).

Not measured: GitHub dependents counts, libraries.io reverse dependencies, conda downloads, citation counts, Stack Overflow /
Cross Validated mentions (no API access configured). The scipy closed-issue and closed-PR totals came back empty from the search API.

Reading it: DBCI is the only direct competitor with real momentum (69 commits in 12 months, pre-commit.ci, 6 GitHub workflows,
hatch-vcs versioning) but it has not cut a release in 14 months, while `main` has merged fixes since (Wang plateau logic, build and CI changes) that PyPI users do not get. `binomial_cis`, `binoculars` and `pynomial` are effectively dormant (`pynomial` is three days of
commits in August 2025). `confseq` is the reference for betting sequences, with no PyPI release since January 2023. The mainstream
libraries are not competitors on scope but set the speed and install-friction bar.

## 3. Footprint (measured)

**Import time** (`benchmarks/competitors/import_time.py`: fresh interpreter per sample, packages sampled round-robin, 9 rounds,
bare-interpreter time subtracted). The machine is noisy, so both the minimum and the median are shown.

| Package | Import, min | Import, median |
|---|--:|--:|
| astropy.stats | 0.29 s | 0.42 s |
| scipy.stats | 0.85 s | 1.03 s |
| binoculars | 0.87 s | 1.04 s |
| pynomial (Dpananos) | 0.85 s | 1.13 s |
| `import pandas, scipy.stats` (the floor for binomcikit) | 1.20 s | 1.35 s |
| **binomcikit** | **1.22 s** | **1.56 s** |
| statsmodels (proportion) | 1.29 s | 1.52 s |
| DBCI | 1.51 s | 1.90 s |
| binomial_cis | 2.34 s | 2.86 s |

Before the 2026-10-03 change, a paired same-state measurement of old versus new `import binomcikit` gave 1.88 s to 1.54 s (min)
and 2.07 s to 1.62 s (median): `plotnine` is now imported on first use of a plotting function instead of at `import binomcikit`.
What remains is the cost of pandas and `scipy.stats`, which 25 of our modules import eagerly, so ~1.2 s is the floor for this
dependency set. A core install **works without plotnine/plotly** (verified by blocking both imports; `tests/test_lazy_plotting.py`).

**Size and dependencies** (`footprint.py`; size = the distribution plus its transitive dependencies; numpy, scipy and pandas dominate
every closure, so only the *own* column and the package count say anything about the package itself). binomcikit is installed
editable here, so its own size was measured from `src/binomcikit` instead: **469 KB** of source.

| Package | Own size | Dependency closure | Packages in closure |
|---|--:|--:|--:|
| binomcikit | 469 KB | 251 MB | 8 |
| DBCI | 202 KB | 255 MB | 17 |
| binomial_cis | 97 KB | 369 MB | 15 |
| pynomial (Dpananos) | 53 KB | 209 MB | 19 (pulls IPython; pins numpy ≥ 2.3.2, scipy ≥ 1.16.1, Python ≥ 3.12) |
| binoculars | 13 KB | 185 MB | 3 |
| statsmodels (proportion) | 46 MB | 299 MB | 10 |
| astropy.stats | 41 MB | 106 MB | 6 |
| scipy.stats | 134 MB | 185 MB | 2 |

**Peak memory** for one whole table (single cold call, `psutil` peak working set above post-import RSS): every package stays under
4 MB extra (binomcikit `ci()` 2.7 MB for Wilson at n = 10,000; `limits()` 0.4 MB; statsmodels 0.5 MB), except astropy (26 MB for
the same table). Post-import resident size: binomcikit 144 MB, statsmodels 136 MB, DBCI 163 MB, scipy 95 MB, binoculars 95 MB,
astropy 46 MB. Memory is not a differentiator.

## 4. Accuracy against a 30-digit mpmath reference

`benchmarks/competitors/accuracy.py`: Wilson (closed form) and Clopper–Pearson (bisection on the exact binomial tail), α = 0.05,
19 cases including x = 0, x = n, n = 1, 2, 5, 10, 1000 and 10^5. Largest absolute error in either limit:

| | Wilson | Clopper–Pearson |
|---|--:|--:|
| binomcikit | 2.2e-16 | 2.2e-16 |
| statsmodels | 2.2e-16 | 2.2e-16 |
| astropy | 2.2e-16 | no exact interval |
| scipy | 2.2e-16 | 3.8e-13 (at x = 99,999, n = 10^5) |
| DBCI | 2.2e-16 | 2.2e-16 |
| binoculars | **8.3e-6** | **6.4e-6**, and a **NaN lower limit** at x = 0 for n = 1, 2, 10, 1000, 10^5 |

The 10^5 midpoint case was dropped (the mpmath tail sum was impractically slow). `pynomial` was not run through this harness; in the
benchmark's parity column it matches standard Wilson (with `correct_continuity=False`), Wald, Agresti–Coull and Clopper–Pearson to
1e-16 once its outputs are clamped to [0, 1]. `binomial_cis` computes a different family (optimal randomised intervals) and was not
compared numerically.

## 5. Methods, deviations explained, and defects

**Deviations that looked like defects but are not** (found while root-causing the earlier "unexplained" parity gaps):

| Observation | Cause | Verdict |
|---|---|---|
| `pynomial.wilson` 8e-3 from standard Wilson | `wilson(x, n, correct_continuity=True)` is continuity-corrected **by default** | by design; harness now passes `False` |
| `pynomial` Wald / Agresti–Coull 4e-3–1e-2 off | limits are not clamped to [0, 1] (x = 1: lower −0.0095) | convention; equal to ours after clamping (0.0) |
| `astropy` Wald 9.5e-3 off at n = 100 | same: unclamped lower limit | convention; equal to ours after clamping (1e-16) |
| DBCI `arcsine` 0.03 off (n = 20) | DBCI's arcsine is `sin²(asin√((x+3/8)/(n+3/4)) ± z/(2√n))`, an Anscombe-shifted centre; binomcikit's `arcsine` is the plain one, and our `arcsine-anscombe` is Pires & Amado's cc + Anscombe variant, a different width | different method; DBCI's exact variant is **not** available in binomcikit (reproduced exactly from its source to 0.0) |
| DBCI `logit` boundary diff 0.17 | DBCI returns `[0, 0]` / `[1, 1]` at x = 0 / n | convention |

**Real defects, each reproduced** (scripts: `planning/upstream_repro/`; drafts: `planning/UPSTREAM_REPORTS_DRAFT.md`):

| Package | Defect | Evidence |
|---|---|---|
| DBCI (0.1.0 and `main`) | `modified-wilson` / `modified-newcombe` upper limit for x near n omits `1 -` (code: `upper = 0.5 * qchisq(...) / n_total` where the lower-tail expression is needed) | 59/60 gives lower 0.9114, **upper 0.0004**; by symmetry it should be 0.9996 |
| DBCI (0.1.0 and `main`) | score-type intervals (`mee`, `miettinen-nurminen`) satisfy their defining equation only to 1e-4–1e-5 (limits 1e-5 off); `blaker` steps the parameter in a `tol = 1e-5` loop | Z² residuals 3e-4 / 5e-4 (Mee) at 56/70 vs 48/80; Blaker limits off by up to 9.9e-6 at n = 20 |
| DBCI (0.1.0 and `main`) | `make_risk_report` writes LaTeX with `Path.write_text(...)` and no encoding: `UnicodeEncodeError` on Windows unless `PYTHONUTF8=1` | `test_make_risk_report` fails (reproduced; `_applications.py:341`) |
| binoculars 0.1.3 | `binomial_confidence(0, n, method="clopper-pearson")` returns a NaN lower limit (should be 0); `z` defaults to the hard-coded 1.96 | reproduced; ~1e-6–8e-6 off the exact 95% limits |
| statsmodels 0.14.5 / 0.15.0 | two-proportion `score`: wrong constrained MLE (`count0` for `nobs0`) | **already fixed on `main`** (issue #10269); not for us to report |

Carried over from earlier sessions and **not re-derived today**, so not drafted: DBCI `pratt` (differs from ours by 5.3e-2 at n = 60),
DBCI `witting` (randomised, so run-to-run differences are expected), DescTools Pratt/Witting.

**DBCI tests:** 19 tests pass in 12 m 52 s on Windows (740 s of it two randomised tests). `test_specials.py` needs `rpy2` and an R
install (not run). DBCI vs binomcikit, 28 method/size checks: Wilson, Wald, Agresti–Coull, Jeffreys, Clopper–Pearson, logit, Mid-P and
likelihood-ratio agree to ≤ 5e-13 (interior x). `PyPI 0.1.0` and `main` gave identical numbers apart from the randomised Witting rows.

## 6. SWOT per package (each item tied to a number above)

### DBCI
* **Strengths:** broadest direct overlap (16 single + 15 two-proportion methods, aliases excluded); active (69 commits / 12 m, 6 workflows,
  pre-commit.ci); MIT; tests against SAS/PASS/DescTools outputs; Streamlit app; 19 passing tests.
* **Weaknesses:** no release in 14 months while `main` has merged fixes; 90% single-author; loop-based API (a whole exact table at n = 1000
  takes ~260 ms vs 2–3 ms for us); the defects above; 17 dependencies incl. `openpyxl`, `jinja2`; slower import (1.51 s vs 1.22 s).
* **Opportunities (for us):** it has no evaluation layer (coverage, p-confidence, aberrations), no planning, no betting, no Bayesian
  toolbox, no exact Sterne/BSC/OLC.
* **Threats:** it covers the difference-of-proportions problem more broadly (15 distinct methods vs our 7).
* **Where it beats us:** more two-proportion methods (incl. Wang's exact interval, Haldane, Brown–Li, Carlin–Louis); note its `score` is an alias of Newcombe's hybrid, while ours (like statsmodels') is Miettinen–Nurminen; MIT licence;
  active release tooling; its arcsine variant.

### binomial_cis (TRI-ML)
* **Strengths:** optimal (UMAU/UMPU, minimal-excess-length) exact intervals; a `joss/` folder in the repo; MIT; 299 downloads/month
  (highest of the niche packages).
* **Weaknesses:** one family of methods; dormant (0 commits in 12 m); slowest import (2.34 s min; pulls numba + matplotlib); tests are notebooks.
* **Opportunities:** we can cite it for the minimal-excess-length idea and benchmark OLC/BSC against it (not done).
* **Threats:** low; single-purpose.
* **Where it beats us:** randomised exact UMAU/UMPU intervals as a documented product (we ship Witting, not the same construction); not benchmarked here.

### pynomial (Dpananos, GitHub only)
* **Strengths:** eight methods with a test file each (Wald, Agresti–Coull, arcsine, Bayesian beta/HPD, Clopper–Pearson, Wilson ±cc,
  logit, cloglog); vectorised inputs; matches the standard formulas to 1e-16 once clamped; small import (0.85 s min).
* **Weaknesses:** three days of commits (2025-08-27 to 08-29), one author, never released to PyPI (the PyPI name belongs to an
  unrelated package); **no licence file**, so by default it cannot be reused; pins numpy ≥ 2.3.2, scipy ≥ 1.16.1 and Python ≥ 3.12;
  pulls IPython; loop-only table building in practice (~110 ms vs 28 µs at n = 1000).
* **Opportunities / threats:** none material.
* **Where it beats us:** import time; `wilson(..., correct_continuity=True)` default.

### binoculars
* **Strengths:** tiny (13 KB, 3 packages in closure, 0.87 s import), MIT, readable.
* **Weaknesses:** four intervals; `z` hard-coded to 1.96; NaN lower limit at x = 0 for Clopper–Pearson; abandoned since 2021; single author.
* **Where it beats us:** smallest install and import time.

### confseq
* **Strengths:** the authors' reference implementation of betting confidence sequences; 85 stars; MIT; our oracle (agreement to 1e-16).
* **Weaknesses:** no PyPI release since 2023-01-26; needs a C++ toolchain (pip build failed here; we import its Python sources with
  `np.float_` patched for numpy ≥ 2); 84% single author.
* **Opportunities:** our hedged betting sequence is **6.4–8.7×** faster on 1,000 observations (2026-10-03 run: 4.6 vs 40.2 ms and
  49.5 vs 318.2 ms).
* **Threats:** it is the canonical citation for the method; we must not claim novelty on it.
* **Where it beats us:** C++ uniform boundaries and the full set of confidence-sequence families beyond what we ported.

### statsmodels
* **Strengths:** installed everywhere (31 M downloads / month); vectorised and fast (Wilson table at n = 100: ~97 µs vs our `ci()`
  168 µs); BSD; four two-proportion methods.
* **Weaknesses:** six one-proportion methods and no evaluation or Blaker/Sterne; its released two-proportion `score` interval is
  wrong (fixed on `main`, unreleased).
* **Opportunities:** `bk.limits()` is 2–7.6× faster than it on the same tables.
* **Threats:** a new interval added upstream would remove a reason to install us.
* **Where it beats us:** raw `ci()`-style speed for closed forms at small n, zero extra install; import time is about equal (1.29 s vs 1.22 s min).

### astropy.stats
* **Strengths:** 0.29 s import, fastest vectorised Wilson/Jeffreys/Wald; BSD.
* **Weaknesses:** `binom_conf_interval` offers only wilson, jeffreys, flat and wald (no Clopper–Pearson); Wald limits are not clamped.
* **Where it beats us:** import time and bare-table speed.

### scipy.stats
* **Strengths:** ubiquitous; Wilson and exact in `binomtest(...).proportion_ci`; BSD.
* **Weaknesses:** one interval per call (1000-row table: 0.78 s Wilson, 3.2 s exact); exact limit off by 3.8e-13 at n = 10^5.
* **Where it beats us:** availability; no install.

### DescTools (R, for oracle/defect purposes)
* **Strengths:** `BinomCI` with ~16 methods; 19 commits in 12 m; used as an oracle in earlier sessions.
* **Weaknesses:** earlier sessions found Pratt and Witting defects (not re-run today); R only.

## 7. Improvement backlog and status

| # | Item | Status (2026-10-03) |
|--:|---|---|
| 1 | **Two-proportion intervals** | **Done:** `bk.diff_interval` / `diff_ci` / `list_diff_methods` — Wald, Wald-cc, Agresti–Caffo, Newcombe (±cc), Mee, Miettinen–Nurminen; 30 tests; matches statsmodels (1e-12) and DBCI (1e-9, score methods exact where DBCI is not). Still missing vs DBCI: Haldane, Jeffreys–Perks, Brown–Li (and its Miettinen–Nurminen variant), Carlin–Louis, Hauck–Anderson, true-profile, Wang's exact interval (8 of DBCI's 15 distinct methods) |
| 2 | Lazy-import plotnine to cut import time | **Done:** 1.88 → 1.54 s (paired min); now at the pandas + scipy.stats floor (~1.2 s). Going lower needs dropping pandas/`scipy.stats` from the import path (25 modules import it) |
| 3 | Cut `bk.ci()` DataFrame overhead | **Partly done:** flag columns by lookup (Wilson n = 10,000: ~4 ms → 0.5 ms; n = 100: ~250 → ~150–170 µs). The remaining gap to statsmodels at small n is pandas frame construction (~75% of `ci()`); `bk.limits()` is the fast path |
| 4 | Release a real PyPI version (3.1.0) | **Not done — needs your decision** (PyPI 0.0.5 is 20 months old; 13 downloads/month vs DBCI 74) |
| 5 | Licence decision | **Not done — needs your decision** (GPL-3.0 vs MIT/BSD competitors) |
| 6 | Scheduled benchmark workflow (> 2× regression) | **Done, untested on GitHub:** `benchmarks/regression_check.py`, `baseline.json` (recorded on this Windows machine), `.github/workflows/benchmark.yml`. The first scheduled/manual run on `ubuntu-latest` may need `workflow_dispatch` with *update* ticked to re-record the baseline for that runner |
| 7 | Root-cause `pynomial`, `astropy`, DBCI arcsine deviations | **Done** (section 5): two harness mistakes (fixed), one convention, one different arcsine variant |
| 8 | Randomised / property tests for `limits` vs `ci` vs `interval` | **Done:** `tests/test_limits_ci_property.py` (+ an exhaustive grid check, 0 failures) |
| 9 | Adopt `hatch-vcs` + pre-commit | **Half done:** `.pre-commit-config.yaml` added and validated (`pre-commit run --all-files` passes). `hatch-vcs` **not adopted**: it replaces the hand-set version string, which interacts with the pending release decision (item 4) and with `CITATION.cff` / docs version sync |
| 10 | *(new)* add DBCI's arcsine variant (3/8-shifted centre, 1/(2√n) width) | open, small |

## 8. Upstream reports

Drafts (not filed, awaiting approval) are in `planning/UPSTREAM_REPORTS_DRAFT.md`, with runnable repros in `planning/upstream_repro/`.

## 9. Caveats

* One machine, one day. Two benchmark passes earlier on 2026-10-03 were contaminated by a CPU-heavy process; the published numbers
  are from a clean third pass, and import times use round-robin sampling to spread the machine's noise.
* Library versions are the installed ones (statsmodels 0.14.5, scipy 1.16.1, astropy 8.0.1, DBCI 0.1.0), not the latest on PyPI
  (statsmodels 0.15.0, scipy 1.18.1). DBCI `main` was used for the test run, the parity comparison and the repros;
  statsmodels 0.15.0 was used (from a temporary install directory) to confirm the two-proportion `score` behaviour.
* Downloads and stars measure reach, not quality.
