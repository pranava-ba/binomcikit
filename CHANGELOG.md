# Changelog

All notable changes to **binomcikit** are recorded here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/); versions follow SemVer.

## [Unreleased] — Phase 1 (in progress)
### Added
- **High-level `ci(x, n, method=…)` dispatcher** over every CI method (`binomcikit.ci`).
- **Optional `[fast]` numba accelerator** (`_accel.py`) for the large-*n* coverage kernel, with a
  transparent numpy fallback and a test proving they agree to 1e-9. Rationale + numbers:
  `benchmarks/` (numba reaches compiled-native speed — 176 ms vs Haskell 380 ms vs numpy 7762 ms).
- **Documentation scaffold**: a "probability-from-zero" Foundations track, a Glossary that links
  every technical term, the first method page (**Wald**, `docs/methods/wald.md`) with an embedded
  coverage figure, and a method-selection guide.
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
