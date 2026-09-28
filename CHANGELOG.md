# Changelog

All notable changes to **binomcikit** are recorded here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/); versions follow SemVer.

## [Unreleased] — Phase 1 (in progress)
### Research notes — real-world use case & positioning (2026-09-28)
Findings from grounding "is any of this actually used/researched" against current (2026) sources,
prompted by a request to assess the project's real-world relevance — recorded here since they inform
what to build next, not because they're a code change.
- **The underlying methods are already load-bearing, beyond the FDA/SAS/production-ranking evidence
  already in `planning/RESEARCH.md`:** Adobe's Experience Platform experimentation service and
  **Optimizely** (a major commercial A/B-testing platform) have both adopted always-valid p-values /
  betting-based confidence sequences for continuous experiment monitoring — production infrastructure,
  not academic curiosities.
- **New angle: LLM evaluation.** OpenAI Evals and EleutherAI's eval pipeline have started using
  confidence-sequence-based stopping for adaptive benchmark sizing. There is active, public frustration
  in the field (2026) about how badly binomial-proportion statistics are usually handled in benchmark
  reporting — e.g. a widely-discussed finding that 80% on 100 test cases has a 95% CI of roughly
  71–87%, and leaderboard models are routinely reported as different while their intervals overlap.
  Pass/fail-per-example is a binomial proportion; this is exactly binomcikit's domain.
- **Active research, not a settled field:** "safe anytime-valid inference" is described in the current
  literature as rapidly growing; a 2024 rare-event binomial-CI paper made it into *The American
  Statistician* (peer-reviewed), still comparing Wilson/Jeffreys/CP tradeoffs; the LLM-eval-statistics
  sub-area has multiple arXiv papers from recent months (benchmark CI width, measurement error in eval
  pipelines, effective-sample-size gains for adaptive evaluation).
- **The idea:** binomcikit fits a currently underserved niche it wasn't designed for — LLM benchmark
  sizing and comparison. "How many eval examples to reliably detect a 3-point accuracy gap between two
  models?" is exactly `sample_size()`/`power()` on a binomial proportion; people in that space currently
  roll ad hoc bootstrap-only CIs or naive normal approximations (the same Wald boundary pathology this
  package's own docs already explain) rather than reach for a real toolkit. A tutorial targeting this
  (`docs/tutorials/`) would cost near-zero — every tool it needs (`sample_size`, `power`, `compare`,
  Wilson-as-default) already exists — and could reposition the README/homepage alongside the existing
  clinical/quality-control framing.
- **Recommendation on sequencing:** slot that tutorial in *before* Phase 2 (Streamlit), not after — it's
  cheap given what's already built, and it may change what Phase 2 should even be (e.g. a
  benchmark-sizing calculator could matter more to this audience than a general Streamlit GUI). Decide
  Streamlit-vs-alternative after seeing whether the tutorial resonates, not before.

### Added
- **Sample-size / power planning — sub-phase 1.12, NEW code beyond R `proportion`**
  (`binomcikit.sample_size`/`power`, access layer). Sample-size determination is a *pre-data* design
  question outside the ported paper's estimation scope; the paper cites a dedicated R package
  (`binomSamSize`) rather than duplicating it. binomcikit adds both: `sample_size(width, alpha, p0,
  method)` finds the **exact smallest n** whose `(1-alpha)` CI is no wider than `width` (binary search,
  evaluated at the single `x` nearest `p0*n` via each method's own `x`-variant dispatcher — deliberately
  *not* the whole-table `_limits` call every other candidate design would reach for, since that would
  make the search cost `O(n_max)` instead of `O(log n_max)` for root-finding methods); `power(n, theta0,
  p_true, alpha, method)` is the exact (not simulated) CI-test-duality companion to 1.11's
  `pvalue`/`reject`. **Verification:** `sample_size(..., method="wald")` matches
  `statsmodels.stats.proportion.samplesize_confint_proportion` exactly across every tested case — a
  genuine independent oracle; every other method is checked against its own defining minimality property
  directly (`width(n) <= target`, `width(n-1) > target`). `power` is cross-checked against an independent
  brute-force sum built from `reject()` (matches to floating-point precision). New
  `docs/access_layer.md` section, 3 glossary terms, 25 tests (`tests/test_sample_size_power.py`).
  **Both exclude the bootstrap family**, same rationale as `pvalue`/`reject`.
  - Incidentally surfaced (via stress-testing `sample_size`'s search to `n_max=100,000`) a real,
    pre-existing bug in `cilrx`/`cilr` — root-caused and fixed in the same session; see **### Fixed**
    below.
- **Frequentist p-value tests — sub-phase 1.11, NEW code beyond R `proportion`**
  (`binomcikit.pvalue`/`reject`, access layer). The 2017 paper treats CIs and tests as interchangeable
  by CI-test duality and explicitly omits separate test functions; binomcikit adds them anyway, defined
  **directly from each method's own CI** (the smallest α at which θ₀ falls outside the `(1-α)` interval)
  — so `pvalue`/`reject` work for **any** registered method (Wald through Blaker), not just ones with a
  closed-form test formula, and are guaranteed by construction to agree with `bk.ci`. **Verification:**
  not checked against `scipy.stats.binomtest`'s default two-sided p-value — that uses a different
  ("minlike") convention that genuinely disagrees with the equal-tailed construction used here (locked
  in by a test asserting binomcikit's Clopper-Pearson p-value is exactly 2× scipy's at a case where they
  diverge). Instead verified against: (1) the standard closed-form equal-tailed formula
  `2*min(P(X<=x), P(X>=x))` for `method="exact"` (an independent, textbook formula); (2) the one-sided
  tail probabilities matching `scipy.stats.binomtest(alternative="less"/"greater")` exactly (the
  convention every implementation agrees on); (3) the CI-duality property itself, checked directly
  across 10 methods. Also **documents and tests a genuine, expected divergence**: Wald's p-value differs
  from Wilson's/Clopper-Pearson's by ~2-3 orders of magnitude for the same `(x, n, theta0)`, because
  Wald's variance is estimated at p̂ rather than θ₀ — exactly the "duality is only approximate for some
  methods" gap ROADMAP.md names as the reason to add these functions at all. New `docs/access_layer.md`
  section + 2 glossary terms (`CI-test duality`; `p-value`/`null hypothesis` already existed). 30 new
  tests (`tests/test_pvalue.py`). **Performance note:** each call re-evaluates the method's whole CI
  table via bisection on α — near-instant for closed-form methods, noticeably slower (documented in the
  `pvalue` docstring) for methods that root-find per row internally (Clopper-Pearson/Mid-P, LR, Blaker).
- **Bootstrap confidence intervals — sub-phase 1.10, a NEW method beyond R `proportion`**
  (`binomcikit.ci.bootstrap`, `ciboot`/`cibootx`, `method="boot"`). Three variants behind one `kind`
  parameter: `"percentile"`/`"bca"` — the ordinary nonparametric bootstrap, a thin wrapper around
  `scipy.stats.bootstrap` (oracle-verified: matches scipy's own output exactly, same seed in → same
  limits out) — and `"smooth"` (default) — Wang & Hutson's (2013) smooth-quantile bootstrap [25],
  implemented directly from the paper's primary text (Section 2, verified via
  [PMC4789773](https://pmc.ncbi.nlm.nih.gov/articles/PMC4789773/), not a secondary summary), including
  its median-unbiased estimator (Eq. 8, checked against the paper's own closed-form boundary formulas
  as an exact identity) and its fixed cubic B-spline (Eq. 7, knots/coefficients transcribed exactly).
  **No third-party oracle exists for `kind="smooth"`** — this is flagged explicitly in
  `docs/methods/bootstrap.md` and `docs/under_the_hood.md`, and verified instead by (1) the MUE
  boundary identity, (2) rough agreement with the oracle-verified percentile/BCa away from the
  boundary, and (3) the specific property it exists for: a **non-degenerate interval at x = 0 / x = n**,
  exactly where the ordinary bootstrap (verified to) collapse to zero width. Wired into the full metric
  suite (`covpboot`, `lengthboot`, `pcopbiboot`, `errboot`), the `ci()` dispatcher, and the Plotly
  layer (`"boot"`, `"boot-percentile"`, `"boot-bca"`); deliberately **excluded** from
  `compare()`/`recommend()`'s default method list (stochastic + much slower than every closed-form
  method — pass `methods=[..., "boot"]` explicitly). Also added `point_estimate(x, n, "mue")`, the
  median-unbiased estimator, to the access layer. New `docs/methods/bootstrap.md` (two-core page,
  worked example reproducing the boundary contrast) and `bootstrap_coverage.png` (percentile vs.
  smooth vs. Wilson — the smooth variant tracks Wilson; percentile plunges to ~0.85 coverage near
  θ ≈ 0.1/0.9). Seven new glossary terms (`bootstrap`, `resampling`, `percentile interval`, `BCa`,
  `median-unbiased estimator`, `smooth quantile function`, `B-spline`). 25 new tests
  (`tests/test_bootstrap.py`): the MUE identity, scipy-oracle equality for percentile/BCa, the
  boundary-collapse property, cross-agreement away from the boundary, dispatch, and metric-suite
  inheritance.
- **Coverage measurement in CI.** Added a dedicated `coverage` GitHub Actions job (`pytest-cov`,
  branch coverage, Python 3.12/Ubuntu) that uploads the XML report as a build artifact and fails
  the build below 60%. Baseline measured 2026-09-28: **64.8% branch coverage** (4,171 statements,
  1,464 branches); the legacy plotnine `*_graph.py` modules (4–8% covered, slated for retirement)
  are the main drag — the numeric core is meaningfully higher. `pytest-cov` moved from `[dev]`-only
  into the `[test]` extra; `[tool.coverage.run]`/`[tool.coverage.report]` added to `pyproject.toml`.
  README gained a coverage badge; documented in `docs/under_the_hood.md` ("Coverage").

### Fixed
- **The Likelihood-Ratio interval (`cilrx`/`cilr`) silently returned an almost-`[0, 1]` interval for
  large `n`** (confirmed broken between `n=25,800` and `n=26,000`; every documented/tested case before
  this was `n <= 30`). Root cause: the MLE step minimized the *raw* likelihood
  (`scipy.stats.binom.pmf`), which underflows to exactly `0.0` for large `n` away from the true value —
  `scipy.optimize.minimize_scalar` then converged to an arbitrary point in that flat zero region
  (observed: `p≈1.0` for a true value of `0.5`), corrupting the whole interval. Found incidentally while
  stress-testing sub-phase 1.12's `sample_size` search up to `n_max=100,000`; a systematic audit of every
  `scipy.optimize` call in the package then found the identical pattern in `cialr` (`adj_n.py`, the
  *adjusted* LR) and confirmed its single-`x` sibling `cialrx` (`adj_n_x.py`) was **not** affected (it
  already used the log-likelihood for this step). **Fix, both places:** the binomial MLE has a closed
  form (`x/n`, or `(x+h)/(n+2h)` adjusted) — no optimization needed — and the two endpoints are now found
  via `scipy.optimize.brentq` on the signed log-likelihood, which underflow cannot fool the way
  minimizing an absolute difference can. Verified correct to `n=1,000,000`; also faster (~2ms/call
  regardless of `n`). New regression tests in `tests/test_golden_paper.py`; the `n=5` golden-value tests
  are unaffected. `cialr`/`cialrx` also gained their first test coverage in this fix (previously zero).
  Full writeup: `docs/under_the_hood.md` "Sample-size / power".
- **Known issue, found during the audit above, not fixed (low severity):** `ciblaker`/`ciblakerx` raise
  instead of returning a result for `alpha` roughly above `1 - 1e-10` — an essentially meaningless
  confidence level nothing in this package ever requests; `pvalue`/`reject`/`sample_size`/`power` already
  guard against it defensively. See `docs/under_the_hood.md`.

### Changed
- **Executable documentation (MyST-NB).** Worked examples in the docs now run at build time against the
  installed package (```{code-cell}``` blocks), so the tables and numbers shown are generated from the
  real `binomcikit` and cannot drift from the code (a broken example fails the build). Set up the theme
  fixes alongside: removed the "edit this page" / "view source" links, and made the five sidebar section
  headers collapsible (`docs/_static/custom.{css,js}`). RTD now installs the package so it can execute.
- **Docs content depth — a "probability from zero" Foundations series and a growing theory track.**
  Rebuilt `foundations/` from one thin page into a five-page beginner course (proportion & p̂ → the
  binomial pmf → sampling variability → what a confidence interval *really* means → coverage), each an
  *executed* page ending in a "Check yourself" quiz, with a repeated-sampling caterpillar simulation and
  a from-scratch exact-coverage computation. Extended the **"Methods & Mathematics"** theory track: after
  the normal-approximation page, added fully worked, executed pages on **test inversion** — deriving the
  Wilson (score) and likelihood-ratio intervals as *the values a hypothesis test does not reject*, showing
  numerically that both beat Wald and share the χ²₁ cutoff — and on **exact methods & discreteness** —
  why binomial coverage is a jagged step function, Clopper–Pearson vs Mid-P vs Blaker, with Blaker's
  acceptability function γ(x,θ) reproduced from scratch and shown to nest inside (dominate) Clopper–Pearson —
  and on **variance-stabilising / transformed intervals** — the delta method as the engine (deriving that
  arcsin√p is *the* stabiliser), arcsine's constant-width interval and its zero-width collapse at the
  boundary, and the logit/expit interval that stays inside (0,1) — and on **the Bayesian view** — Beta–Binomial
  conjugacy, the standard priors, credible-vs-confidence intervals, and the convergence result that the
  Jeffreys credible interval matches Wilson's *frequentist* coverage — and closes with a **coverage-theory**
  capstone: mean vs minimum coverage (why the mean lies), the slow non-convergence of worst-case coverage
  (Brown–Cai–DasGupta), one-sided vs two-sided miss rates, and the adjustment (h) and continuity (c) repairs.
  The **"Methods & Mathematics" theory track is now a complete seven-chapter series**, so every method page's
  "deeper maths" link resolves. Also deepened Foundations into a five-page "probability from zero" beginner
  series, and added a **Tutorials & cookbook** section — worked, executable scenarios (A/B test, quality
  control via posterior probability, the zero-events rule of three, and choosing a method with
  `compare`/`recommend`) plus a copy-paste recipe cookbook. New colourblind-safe teaching figures and four
  new glossary terms (`hypothesis test`, `discreteness`, `conjugate prior`, `sampling variability`). Full
  site still builds clean under `-W`.
- **Documentation overhaul.** Switched the docs theme to **Furo** — a collapsible left-sidebar nav
  (hamburger on mobile) with a deliberately minimal top bar, replacing pydata-sphinx-theme's crowded
  top navbar. Reorganized the site into five clear groups (*Start here · Guides · Methods · The maths ·
  Reference*), consolidated redundant pages (merged the three "which method" / Bayesian / intro
  surfaces, removed the `user_guide/` folder), rebuilt the landing page as a six-card hub, and added an
  "at a glance" method cheat-sheet table. Fixed a homepage layout bug (a raw `<div align="center">`
  followed by a blank line broke the article nesting) by emitting the banner via `{raw} html`. Pinned
  the docs toolchain (`sphinx<10`, `sphinx-design<1`, `furo`) so builds stay reproducible. Full site
  builds clean under `-W`.

### Added
- **PEP 561 typing** — a `py.typed` marker (shipped via package-data) plus inline type hints on the
  public surface: the `ci()` dispatcher, `plot_ci` / `plot_coverage`, and the whole `access` layer, so
  downstream type checkers pick up binomcikit's signatures. (The internal 1xx–6xx grid functions share
  uniform `(n, alpha, …)→DataFrame` signatures and are hinted incrementally.)
- **Access / usability layer** (`binomcikit.access`) — modern conveniences the R original lacks, none
  adding new statistics: `from_data` / `from_counts` (build `(x, n)` from raw 0/1 data), `point_estimate`
  (mle / Agresti–Coull / Jeffreys / Laplace), `posterior` + `prior` (Beta-posterior summaries and
  named-prior lookup), `coverage_curve` / `length_curve` (the numbers behind the plots, as tidy
  DataFrames), `compare` (every method's interval for one x, side by side) and `recommend` (rank methods
  by measuring them on the metric engine — narrowest *among adequately-covering* methods, closest
  coverage, or highest guaranteed coverage). Documented in `docs/access_layer.md`; `tests/test_access.py`.
- **Blaker's exact interval — a NEW method, beyond the R `proportion` package** (sub-phase 1.9,
  `binomcikit.ci.blaker`). An exact interval whose coverage is guaranteed ≥ 1 − α and that is provably
  **nested inside Clopper–Pearson** (never wider, usually shorter) — it *dominates* Clopper–Pearson.
  Implemented as `ciblaker` / `ciblakerx` from Blaker (2000) [15] by root-finding the acceptability
  function, wired into the `ci()` dispatcher, the Plotly layer, and — via the shared limit-producer
  contract — the full metric suite (`covpblaker`, `lengthblaker`, `pcopbiblaker`, `errblaker`) with no
  per-method metric code. Verified by its two defining theorems (nesting ⊆ CP; coverage ≥ 1 − α on a θ
  grid) plus frozen `BLAKER_N5` limits (`tests/test_blaker.py`). Two new glossary terms
  (`acceptability function`, `nested interval`) and a `docs/methods/blaker.md` page flagged as new.
- **High-level `ci(x, n, method=…)` dispatcher** over every CI method (`binomcikit.ci`).
- **Optional `[fast]` numba accelerator** (`_accel.py`) for the large-*n* coverage kernel, with a
  transparent numpy fallback and a test proving they agree to 1e-9. Rationale + numbers:
  `benchmarks/` (numba reaches compiled-native speed — 176 ms vs Haskell 380 ms vs numpy 7762 ms).
- **Documentation scaffold**: a "probability-from-zero" Foundations track, a Glossary that links
  every technical term, the first method page (**Wald**, `docs/methods/wald.md`) with an embedded
  coverage figure, and a method-selection guide.
- **Wilson (Score) method page** (`docs/methods/wilson.md`, sub-phase 1.2) — two-core *Use it /
  Understand it* page with the score-test derivation, a Wald-vs-Wilson coverage figure, and three new
  glossary terms (`null hypothesis`, `score test`, `test inversion`). Wilson is the recommended
  default and now leads the method-selection table.
- **ArcSine method page** (`docs/methods/arcsine.md`, sub-phase 1.3) — two-core page with the
  delta-method derivation of the variance-stabilising transform (and why the `sin²(φ)` back-transform,
  *not* `sin²(φ/2)`, is correct), a Wald-vs-ArcSine-vs-Wilson coverage figure, and two new glossary
  terms (`variance-stabilising transformation`, `back-transformation`). **Added an independent golden
  oracle for ArcSine** (`ARCSINE_N5` in `tests/cases.py`, two tests in `tests/test_golden_paper.py`)
  — no third-party library implements arcsine, and one test pins its signature boundary collapse.
- **Logit-Wald method page** (`docs/methods/logit.md`, sub-phase 1.4) — two-core page with the
  delta-method derivation on the log-odds scale (SE = 1/√(n·p̂·q̂)) and the exact one-sided
  Clopper–Pearson substitution used at x = 0, n where logit is undefined; a Wald-vs-Logit-vs-Wilson
  coverage figure showing logit's mild conservatism; four new glossary terms (`odds`, `log-odds`,
  `expit`, `Clopper–Pearson`). **Added an independent golden oracle for Logit** (`LOGIT_N5`, two tests)
  — no third-party library implements it, and one test pins the boundary substitution + no-ZWI property.
- **Wald-T method page** (`docs/methods/waldt.md`, sub-phase 1.5) — two-core page with the Pan (2002)
  Satterthwaite-d.o.f. derivation (a Student-*t* quantile replacing the normal `z`, plus the
  `(x+2)/(n+4)` boundary modification); a Wald-vs-Wald-T-vs-Wilson coverage figure showing it fixes
  Wald's sag but over-covers at the edges; three new glossary terms (`t-distribution`,
  `degrees of freedom`, `Satterthwaite approximation`). **Added an independent golden oracle for
  Wald-T** (`WALDT_N5`, two tests) — verified against a fresh reimplementation of the Pan formula;
  one test pins the *t*-widening (wider than Wald) and no-ZWI properties.
- **Likelihood-ratio method page** (`docs/methods/lr.md`, sub-phase 1.6) — two-core page with the
  test-inversion derivation (Wilks' theorem, the z² cutoff, and why LR has **no continuity-corrected
  variant**); a Wald-vs-LR-vs-Wilson coverage figure showing LR tracks Wilson closely; three new
  glossary terms (`likelihood`, `likelihood-ratio statistic`, `Wilks' theorem`). **Added an
  independent golden oracle for LR** (`LR_N5`, two tests) — the numerical limits are cross-checked
  against an independent `brentq` root-find, plus a test that the interval brackets the MLE.
- **Exact interval method page** (`docs/methods/exact.md`, sub-phase 1.7) — two-core page for the
  tunable exact family: Clopper–Pearson (`e = 1`), Mid-P (`e = 0.5`), and the tail equations they
  solve; a Clopper–Pearson-vs-Mid-P-vs-Wilson coverage figure; three new glossary terms
  (`tail probability`, `Mid-P`, and an expanded `Clopper–Pearson`). Added a statsmodels cross-check
  (`e = 1` reproduces `method="beta"` exactly) and a Mid-P golden oracle (`MIDP_N5`, narrower than CP).
- **Plotly plotting layer now supports the exact family** (`plot_ci`/`plot_coverage` accept `exact`,
  `cp`, `clopper-pearson`, `midp`, `mid-p`), with parametrized regression tests over every ported method.
- **Bayesian credible-interval method page** (`docs/methods/bayes.md`, sub-phase 1.8) — two-core page
  on the Beta(x+a, n−x+b) posterior, the quantile vs HPD interval, the Jeffreys prior, and a
  Jeffreys-vs-flat-vs-Wilson coverage figure. Added a statsmodels cross-check (Jeffreys quantile CI
  reproduces `method="jeffreys"` exactly) and an HPD-properties test (1 − α mass, never wider than the
  quantile interval). Seven new glossary terms (`credible interval`, `posterior mean`,
  `highest posterior density interval`, `Bayes factor`, `empirical Bayes`, `posterior probability`,
  `posterior predictive`).
- **New "Bayesian toolbox" documentation page** (`docs/bayesian_toolbox.md`) — a tour of the package's
  headline novelty: the credible interval, empirical Bayes, the six Bayes-factor formulations,
  posterior probabilities, and the posterior predictive, with a when-to-use-what table. Wired into the
  main nav; the Plotly layer also gained `bayes`/`jeffreys` coverage support.
- **Plotly plotting layer** (`binomcikit.plot_ci`, `binomcikit.plot_coverage`) — the forward,
  interactive path that replaces plotnine method-by-method; lazy-imports plotly (optional).
- **"Under the hood" technical docs** (`docs/under_the_hood.md`) logging the validation strategy
  (four oracles + the numba==numpy agreement test), the numba acceleration and threshold, the
  plotting migration, the install extras, reproducibility, and CI.
- **CI**: OS × Py 3.9–3.13 matrix with ruff + black, a core-import-without-plotnine job, a `[fast]`
  job, and a Trusted-Publishing (OIDC) release workflow.
### Changed
- **Vectorized the coverage & expected-length metric engines** over the (x, θ) grid — test suite
  ~3× faster, numerically identical.
- **Plotting is now optional**: `plotnine` moved to the `[plots]` extra; the core install imports
  with no plotting stack.
### Decided
- Language/backend: **Python core + optional numba**; no Rust/C++/Haskell rewrite (see `benchmarks/`).

## [3.0.8] — 2026-07-23
### Changed
- **Corrected the `empericalBA` / `empericalBAx` misspelling** inherited from the R
  package. The public names are now **`empiricalba` / `empiricalbax` only**; the
  misspelled R-parity aliases have been removed. The R spelling is retained purely as
  provenance (docstrings and `tests/r_exports.txt`).
- **Packaging metadata overhaul:** added `keywords`, scientific `classifiers`,
  dependency floors (`numpy>=1.22`, `scipy>=1.8`, `pandas>=1.4`, `plotnine>=0.10`),
  and split authors into individual entries.
- Version set to **3.0.8** across `pyproject.toml`, `binomcikit.__version__`, and
  `CITATION.cff`.

### Added
- **Phase-0 test hardening (E):** canonical reference cases (`tests/cases.py`),
  golden values transcribed from the source paper's Table 2
  (`tests/test_golden_paper.py`), and property-based tests via Hypothesis
  (`tests/test_properties.py`).
- `viz` optional dependency extra (`plotly`) for the interactive backend.
- Test/dev extras now include `hypothesis`.

### Decided (implementation scheduled for Phase 1)
- **Plotting will migrate from `plotnine` to `plotly`** — a better fit for the
  Streamlit app (goal 2) and PyQt embedding (goal 3), and interactive. The code
  migration and moving plotting to an optional extra are coupled to the per-plot
  rewrite (which needs visual verification), so `plotnine` remains the plotting
  engine until Phase 1.

### Deferred to post-completion (Phase 0 parts A/B/C)
- **A** — rotate the once-plaintext credentials.
- **B** — fix the ArcSine back-transform formula in `README.md` (code is already correct).
- **C** — relicense to GPL-2 (upstream `proportion` is GPL-2-only) + author attribution.
  These were moved to *after* the package is complete, per project decision.

## [2.0.9] and earlier
- Surface-complete Python port of the R `proportion` package (all 305 exports; six
  families: CI, coverage probability, expected length, p-confidence/p-bias, error,
  Bayesian), validated against `statsmodels` with golden + smoke + completeness tests.
