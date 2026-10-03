# Competitor repositories: activity, footprint, accuracy, SWOT

> Measured **2026-10-03** on Windows 11, Python 3.13.5, one machine. Raw data and the scripts that produced it are in
> `benchmarks/competitors/` (re-runnable; data in `benchmarks/competitors/data/`). Clones were made into a scratch directory
> outside the repo and are **not** committed. Anything not measured is marked *not measured*; there are no estimates in here.

## 0. What changed our picture (read this first)

1. **DBCI is alive and bigger than we had recorded.** `planning/NOVELTY_AND_COMPARISON.md` says it ships 16 intervals. That is
   the PyPI release (0.1.0, 2025-08-15). Its `main` branch (commit `39b0fdb`, 2026-09-02; last push 2026-09-28) lists **19**
   single-proportion methods (adds `modified-wilson`, `modified-newcombe`, `modified-jeffreys`) **and 17 difference-of-two-proportions
   methods** (Newcombe, Mee, Miettinen–Nurminen, Wang, Hauck–Anderson, Agresti–Caffo, ...). binomcikit has **no two-proportion
   inference at all**. That is our largest scope gap (it is already named as future work in `planning/ROADMAP.md`).
2. **Everyone we compared against is accurate to ~1e-16 on Wilson and Clopper–Pearson, except `binoculars`** (off by up to 8e-6
   because it hard-codes `z = 1.96`, and it returns NaN for Clopper–Pearson at `x = 0`). Accuracy is not where we differ; scope,
   evaluation tooling and speed are.
3. **Where we lose, plainly:** `import binomcikit` is slower than every comparator except `binomial_cis` (1.75 s vs 0.34 s for
   `astropy.stats`, 0.91 s for `scipy.stats`, 1.51 s for `statsmodels`). The `bk.ci()` DataFrame path is slower than
   statsmodels/astropy for closed-form methods (see `docs/benchmarks.md`). And our adoption is the smallest in the table
   (13 downloads/month; PyPI still serves a stale 0.0.5).
4. **Licence:** binomcikit is GPL-3.0 (inherited from the R package). Every maintained Python competitor is MIT or BSD. Whether that
   limits adoption is a decision for the maintainer; it is flagged here, not recommended.

## 1. Scope: what was examined

| Package | Repo | Cloned @ | Role |
|---|---|---|---|
| DBCI (`diff-binom-confint`) | DeepPSP/DBCI | `39b0fdb` (2026-09-02) | closest competitor |
| binomial_cis | TRI-ML/binomial_cis | `8a2d6eb` (2025-04-23) | exact/optimal intervals |
| pynomial | Silver-Creek/pynomial | `aeab980` (2020-10-29) | PyPI name `pynomial` 1.0.4; README is a stub |
| binoculars | nolanbconaway/binoculars | `9b8a7d7` (2021-07-03) | 4 simple intervals |
| confseq | gostevehoward/confseq | `5ffe733` (2026-01-06) | betting / confidence sequences |
| statsmodels, astropy, scipy | upstream | API metrics only | the default tools people actually use |
| DescTools (R) | AndriSignorell/DescTools | API metrics only | `BinomCI` has ~16 methods |

GitHub search (`gh search repos`, queries: binomial confidence interval, clopper-pearson, wilson score interval, pynomial, binomial_cis,
confseq) found **no additional maintained Python package** with comparable scope; hits were single-file student projects
(0-1 stars). Not looked at in this pass: `binom`, `PropCIs`, `exactci`, `binGroup` (R, CRAN-only) and commercial tools.

## 2. Activity and usage (2026-10-03)

Command source: `benchmarks/competitors/collect.py` (GitHub REST API via `gh`, PyPI JSON, pypistats.org). "12 m" = since 2025-10-03.
Downloads are PyPI last-30-days from pypistats and include mirrors and bots.

| Package | Stars | Forks | Contributors | Commits 12 m | Last push | PyPI latest (date) | Releases 12 m | Open / closed issues | Open / closed PRs | Downloads / month | Licence |
|---|--:|--:|--:|--:|---|---|--:|--:|--:|--:|---|
| DBCI | 2 | 0 | 4 | 69 | 2026-09-28 | 0.1.0 (2025-08-15) | 0 | 0 / 3 | 1 / 32 | 74 | MIT |
| binomial_cis | 15 | 2 | 4 | 0 | 2025-04-23 | 0.0.12 (2025-04-23) | 0 | 0 / 0 | 0 / 6 | 299 | MIT |
| pynomial | 0 | 0 | 3 | 0 | 2020-10-29 | 1.0.4 (2020-04-14) | 0 | 0 / 0 | 0 / 0 | 9 | GPL-3.0 |
| binoculars | 4 | 1 | 1 | 0 | 2021-10-08 | 0.1.3 (2021-07-03) | 0 | 0 / 1 | 0 / 5 | 74 | MIT |
| confseq | 85 | 4 | 3 | 1 | 2026-01-07 | 0.0.11 (2023-01-26) | 0 | 1 / 3 | 0 / 19 | 543 | MIT |
| DescTools (R) | 95 | 21 | 9 | 19 | 2026-01-26 | n/a (CRAN) | n/a | 27 / 121 | 2 / 33 | n/a | not declared via API |
| statsmodels | 11,668 | 3,614 | 589 | 1,827 | 2026-10-02 | 0.15.0 (2026-08-27) | 2 | 2,629 / 3,062 | 181 / 4,483 | 31,394,993 | BSD-3 |
| astropy | 5,324 | 2,187 | 646 | 1,750 | 2026-10-02 | 8.0.1 (2026-07-05) | 11 | 1,272 / 5,571 | 152 / 13,482 | 2,401,598 | BSD-3 |
| scipy | 15,072 | 5,985 | 1,997 | 2,401 | 2026-10-02 | 1.18.1 (2026-08-21) | 9 | 1,439 / n/a | 423 / n/a | 286,276,241 | BSD-3 |
| **binomcikit** | 1 | 0 | 1 | 27 | 2026-09-28 | 0.0.5 (2025-02-23) | 0 | 0 / 0 | 0 / 0 | 13 | GPL-3.0 |

Bus factor from the clones' full history (top contributor's share of commits): DBCI 275/304 (90%), binomial_cis 63/74 (85%),
confseq 191/227 (84%), binoculars 21/21 (100%), pynomial 6/11 (55%), binomcikit 72/72 (100%, `git shortlog`).

Not measured: GitHub dependents counts, libraries.io reverse dependencies, conda downloads, citation counts, Stack Overflow /
Cross Validated mentions (no API access configured). The scipy closed-issue and closed-PR totals came back empty from the search API.

Reading it: DBCI is the only direct competitor with real momentum (69 commits in 12 months, pre-commit.ci, CI workflows, hatch-vcs
versioning) but it has not cut a release in 14 months, so what users get from PyPI lags `main` by three methods. `binomial_cis`,
`binoculars` and `pynomial` are effectively dormant. `confseq` is the reference for betting sequences and has a modest following but
no PyPI release since January 2023. The mainstream libraries are not competitors on scope but set the speed and install-friction bar.

## 3. Footprint (measured)

`benchmarks/competitors/footprint.py`, `mem_child.py`. Import time = median of 5 fresh `python -c "import ..."` runs minus the bare
interpreter (0.067 s). Size = files of the distribution plus its transitive dependencies. numpy, scipy and pandas dominate every
closure, so only the *own* column and the dependency count say something about the package itself. binomcikit is installed in
editable mode here, so its own size was measured from `src/binomcikit` instead: **469 KB** of source (the 47 KB in the JSON is
the editable-install stub).

| Package | Import time | Own size | Dependency closure | Packages in closure |
|---|--:|--:|--:|--:|
| binomcikit | 1.75 s (1.18 s with plotnine/plotly absent) | 469 KB | 251 MB | 8 |
| DBCI | 1.80 s | 202 KB | 255 MB | 17 |
| binomial_cis | 2.60 s | 97 KB | 369 MB | 15 |
| pynomial | 1.01 s | 53 KB | 209 MB | 19 |
| binoculars | 0.98 s | 13 KB | 185 MB | 3 |
| statsmodels (proportion) | 1.51 s | 46 MB | 299 MB | 10 |
| astropy.stats | 0.34 s | 41 MB | 106 MB | 6 |
| scipy.stats | 0.91 s | 134 MB | 185 MB | 2 |

Findings on our own import time (`python -X importtime`): 1.41 s total, of which `binomcikit.bayes` pulls in `scipy.stats` and
pandas (1.14 s cumulative) and, when installed, the optional `plotnine` adds ~0.24 s through the legacy `*_graph` modules. A core
install **works without plotnine/plotly** (verified by blocking both imports; the guards in `ci/__init__.py` hold). So the cost
is avoidable with lazy imports, not a packaging bug.

Peak memory for one whole table (single cold call, `psutil` peak working set above post-import RSS): every package stays under
4 MB extra (binomcikit `ci()` 2.7 MB for Wilson at n = 10,000; `limits()` 0.4 MB; statsmodels 0.5 MB), except astropy
(26 MB for the same table). Post-import resident size: binomcikit 144 MB, statsmodels 136 MB, DBCI 163 MB, scipy 95 MB,
binoculars 95 MB, astropy 46 MB. Memory is not a differentiator; steady state is dominated by pandas/scipy.

## 4. Accuracy against a 30-digit mpmath reference

`benchmarks/competitors/accuracy.py`: Wilson (closed form) and Clopper–Pearson (bisection on the exact binomial tail), α = 0.05,
20 cases including x = 0, x = n, n = 1, 2, 5, 10, 1000 and 10^5. Largest absolute error in either limit:

| | Wilson | Clopper–Pearson |
|---|--:|--:|
| binomcikit | 2.2e-16 | 2.2e-16 |
| statsmodels | 2.2e-16 | 2.2e-16 |
| astropy | 2.2e-16 | no exact interval |
| scipy | 2.2e-16 | 3.8e-13 (at x = 99,999, n = 10^5) |
| DBCI | 2.2e-16 | 2.2e-16 |
| binoculars | **8.3e-6** | **6.4e-6**, and **NaN** at x = 0 for n = 1, 2, 10, 1000, 10^5 |

The 10^5 midpoint case was dropped from the reference set (the mpmath tail sum was impractically slow). Rows for `pynomial` and
`binomial_cis` were not run through this harness. Earlier benchmark parity (`docs/benchmarks.md`) shows `pynomial` 4e-4 to 1e-2
away from standard Wilson/Wald/Agresti–Coull; the cause is still uninvestigated.

## 5. Methods and defects

**DBCI vs binomcikit, 28 method/size checks** (`dbci_parity.py`, α = 0.05, n = 20 and 100, interior x; run against both PyPI 0.1.0
and `main` HEAD, which gave identical numbers apart from the randomised Witting rows). Agree to ≤ 5e-13: Wilson, Wald,
Agresti–Coull, Jeffreys, Clopper–Pearson, logit, Mid-P, likelihood-ratio. Disagree materially:

| DBCI method | Max interior diff vs binomcikit (n = 20 / 100) | Status |
|---|--:|---|
| Pratt | 0.126 / 0.033 | carried over: earlier session showed DBCI deviates from the Pratt definition; re-observed today, not re-derived |
| Witting | 0.075 / 0.021 | carried over; Witting is randomised, so rows vary run to run |
| Blaker | 1e-5 | carried over: DBCI's coarse stepping |
| arcsine | 0.028 / 0.007 | **new, undiagnosed**: probably a different variant of the transform; needs a primary-source check before any claim |
| modified-Wilson | not compared (no binomcikit counterpart) | carried over: upper limit missing `1 -` at n = 60, x = 59 |

(`wald-cc` could not be compared because binomcikit rejects that method name for `bk.limits`; not investigated.)

**DBCI tests:** 19 tests pass in 12 m 52 s on Windows, of which 740 s are two randomised tests. `test_specials.py` needs `rpy2` and
an R install (not run). Without `PYTHONUTF8=1`, `test_make_risk_report` fails on Windows with a `UnicodeEncodeError` (reproduced).

**binoculars:** hard-coded `z = 1.96` default and NaN at x = 0 (reproduced above).

None of these has been reported upstream. Drafts below are for approval only.

## 6. SWOT per package (each item tied to a number above)

### DBCI
* **Strengths:** broadest direct overlap (19 single + 17 two-proportion methods on `main`); active (69 commits / 12 m, 6 GitHub workflows
  + pre-commit.ci); MIT; tests against SAS/PASS/DescTools outputs; Streamlit app; 19 passing tests.
* **Weaknesses:** no release in 14 months, so PyPI lags `main`; 90% single-author; loop-based API (a whole table at n = 1000 takes
  ~200 ms for exact vs 2.6–4 ms for us (this run)); five method discrepancies listed above; Windows encoding failure; 17 dependencies incl. `openpyxl`, `jinja2`.
* **Opportunities (for us):** it has no evaluation layer (coverage, p-confidence, aberrations), no planning, no betting, no Bayesian
  toolbox, no exact Sterne/BSC/OLC.
* **Threats:** it already covers the two-proportion problem we lack, and its `main` is closing the single-proportion gap
  (modified-* methods).
* **Where it beats us:** two-proportion CIs; MIT licence; smaller import (1.80 s vs 1.75 s: roughly equal); active release tooling.

### binomial_cis (TRI-ML)
* **Strengths:** optimal (UMAU/UMPU, minimal-excess-length) exact intervals; a `joss/` folder in the repo; MIT; 299 downloads/month (highest of
  the niche packages).
* **Weaknesses:** one family of methods; dormant (0 commits in 12 m); slowest import (2.60 s, pulls numba + matplotlib); tests are notebooks.
* **Opportunities:** none direct; we can cite it for the minimal-excess-length idea and benchmark OLC/BSC against it.
* **Threats:** low; it is a single-purpose exact-interval tool.
* **Where it beats us:** randomised exact UMAU/UMPU intervals as a documented product (we ship Witting, not the same construction); not benchmarked here.

### pynomial
* **Strengths:** none that are measurable.
* **Weaknesses:** dormant since 2020; README is a stub; GPL-3.0; 19 packages in its dependency closure (IPython, Azure/ODBC data-source modules); 4e-4 to 1e-2 off standard Wilson/Wald.
* **Opportunities:** upstream-defect candidate once the 1e-2 deviation is root-caused.
* **Threats:** none.
* **Where it beats us:** import time (1.01 s).

### binoculars
* **Strengths:** tiny (13 KB, 3 packages in closure, 0.98 s import), MIT, readable.
* **Weaknesses:** four intervals; `z = 1.96` hard-coded (8e-6 error vs α = 0.05); NaN at x = 0 for Clopper–Pearson; abandoned since 2021; single author.
* **Opportunities:** none.
* **Threats:** none.
* **Where it beats us:** smallest install and import time.

### confseq
* **Strengths:** the authors' reference implementation of betting confidence sequences; 85 stars; MIT; used as our oracle (agreement to 1e-16, `benchmarks/RESULTS.md`).
* **Weaknesses:** no PyPI release since 2023-01-26; needs a C++ toolchain (pip build failed here; we imported its Python sources with `np.float_` patched for numpy ≥ 2); 84% single author.
* **Opportunities:** our hedged betting sequence is **7.3-7.7×** faster on 1,000 observations (`benchmarks/RESULTS.md`, 2026-10-03: 7.1 vs 52.0 ms and 65.3 vs 503.7 ms).
* **Threats:** it is the canonical citation for the method; we must not claim novelty on it.
* **Where it beats us:** C++ uniform boundaries and the full set of confidence-sequence families beyond what we ported.

### statsmodels
* **Strengths:** installed everywhere (31 M downloads / month); 6 methods; vectorised and fast: Wilson table at n = 100 in ~154 µs vs our `ci()` 295 µs; BSD.
* **Weaknesses:** no evaluation, planning of the kind we ship, exact beyond Clopper–Pearson, or Blaker/Sterne; Jeffreys etc. behind one function.
* **Opportunities:** it is the baseline users compare us to; `bk.limits()` is 1.8-5× faster than it on the same tables.
* **Threats:** a new interval added upstream would remove a reason to install us.
* **Where it beats us:** raw `ci()`-style speed for closed forms, import time (1.51 s vs 1.75 s), zero extra install.

### astropy.stats
* **Strengths:** 0.34 s import, fastest vectorised Wilson/Jeffreys/Wald; BSD.
* **Weaknesses:** `binom_conf_interval` offers only wilson, jeffreys, flat and wald (no Clopper–Pearson); its Wald differs from the standard Wald by ~1e-2 at n = 100 and ~1e-3 at n = 1000 (benchmark parity column; cause not investigated).
* **Where it beats us:** import time and bare-table speed.

### scipy.stats
* **Strengths:** ubiquitous; Wilson and exact in `binomtest(...).proportion_ci`; BSD.
* **Weaknesses:** one interval per call (1000-row table: 0.62 s Wilson, 2.5 s exact); exact limit off by 3.8e-13 at n = 10^5.
* **Where it beats us:** availability; no install.

### DescTools (R, for oracle/defect purposes)
* **Strengths:** `BinomCI` with ~16 methods; 19 commits in 12 m; used as an oracle in earlier sessions.
* **Weaknesses:** earlier sessions found Pratt and Witting defects (not re-run today); R only.
* **Opportunities:** upstream defect reports (needs approval).

## 7. Prioritised improvement backlog (feeds `planning/ROADMAP.md`)

| # | Item | Evidence | Size |
|--:|---|---|---|
| 1 | **Two-proportion intervals** (difference; start with Newcombe, Miettinen–Nurminen, Agresti–Caffo) | DBCI ships 17; we ship none | large (new module, oracles needed) |
| 2 | **Lazy-import `bayes` and the legacy plotnine modules** to bring `import binomcikit` from 1.75 s toward ~1.2 s | `-X importtime`: plotnine ~0.24 s, `bayes` → scipy.stats/pandas 1.14 s cumulative | small |
| 3 | **Cut `bk.ci()` DataFrame overhead** for closed forms | statsmodels 154 µs vs 295 µs at n = 100 (Wilson) | medium |
| 4 | **Release a real PyPI version** (3.1.0) | PyPI 0.0.5 is 20 months old; 13 downloads/month vs DBCI 74 | needs maintainer decision |
| 5 | **Licence decision** | all active Python competitors are MIT/BSD; we are GPL-3.0 | maintainer / legal decision |
| 6 | Scheduled **benchmark workflow** failing on > 2× regression | the 2026-10-03 re-run was 2× slower on every package, with nothing to flag it automatically | small |
| 7 | Root-cause `pynomial` (≤ 1e-2) and `astropy` Wald (~1e-2 at n = 100) deviations and DBCI arcsine | all three unexplained above | small each |
| 8 | Add a DBCI-style randomised/property test for our own `limits` vs `ci` paths | DBCI's two random tests catch regressions (740 s) | small |
| 9 | Adopt `hatch-vcs` + pre-commit.ci | DBCI's release tooling | small |

## 8. Drafted upstream reports (NOT filed; need your approval)

1. **binoculars:** "`binomial_confidence(..., method='clopper-pearson')` returns NaN for `x = 0`; default `z = 1.96` gives ~8e-6
   error for 95% intervals." Repro: `binoculars.binomial_confidence(0, 10, method='clopper-pearson')`.
2. **DBCI:** "`test_make_risk_report` raises `UnicodeEncodeError` on Windows unless `PYTHONUTF8=1`; no PyPI release since 0.1.0 while
   `main` has added three methods." Plus, once re-derived from the primary sources, the Pratt / Witting / modified-Wilson items.
3. **DBCI, arcsine:** do **not** file until the arcsine variant difference is checked against the primary source.

## 9. Caveats

* One machine, one day; absolute timings in this repo's benchmark re-run were ~2× slower than the 2026-10-01 run for every
  package, so only ratios between packages are comparable across runs.
* Library versions are the installed ones (statsmodels 0.14.5, scipy 1.16.1, astropy 8.0.1, DBCI 0.1.0), not the latest on PyPI
  (statsmodels 0.15.0, scipy 1.18.1). DBCI `main` was used only for the method list, the test run and the parity comparison.
* Downloads and stars measure reach, not quality.
