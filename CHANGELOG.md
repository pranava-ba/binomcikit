# Changelog

All notable changes to **binomcikit** are recorded here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/); versions follow SemVer.

## [Unreleased] — Phase 1 (in progress)
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
