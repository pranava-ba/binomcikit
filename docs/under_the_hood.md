# Under the hood

How binomcikit computes, how fast it is, and how we know the numbers are right. This page **logs
the technical machinery** — validation, acceleration, plotting, packaging, CI — so it is transparent
and kept current as the package grows (every method sub-phase updates the relevant sections).

## Correctness — four independent oracles

binomcikit's results are checked against several *independent* sources of truth, so a bug would have
to fool all of them at once:

1. **Golden values from the source paper.** The Wald limits for `n = 5` are asserted against Table 2
   of Subbiah & Rajeswaran (2017) — an oracle independent of *any* software
   (`tests/test_golden_paper.py`, values in `tests/cases.py`).
2. **Cross-check vs `statsmodels`.** Wald, Wilson (Score) and Clopper–Pearson match
   `statsmodels.stats.proportion.proportion_confint` to **1e-9** (`tests/test_ci.py`).
3. **Completeness vs the R package.** Every one of the R `proportion` package's **305** exported
   functions must exist in binomcikit — checked against the vendored R NAMESPACE
   (`tests/test_completeness.py`, list in `tests/r_exports.txt`).
4. **Property-based tests (Hypothesis).** For *all* valid inputs — not just a fixed grid — limits
   stay in [0, 1], lower ≤ upper, and symmetric methods satisfy L(x) = 1 − U(n−x)
   (`tests/test_properties.py`).

**The accelerator can't change answers.** The optional numba fast-path is asserted **identical to
the numpy path to 1e-9** (`tests/test_accel.py`), so results never depend on whether `[fast]` is
installed. The full suite (**164 tests**) runs on every push across Python 3.9–3.13 on
Linux / macOS / Windows.

*As each method sub-phase lands, its rare-method + metric outputs get golden fixtures generated from
R, extending oracle #1/#3.*

## Performance — vectorized numpy, optional numba

The heavy work (coverage probability, expected length over a θ grid) is **vectorized in numpy**, so
it runs at C/Fortran speed for the common case — no Python loop over the grid. This is excellent for
the typical small-to-moderate `n`.

For **large `n`**, the vectorized form has to build a dense `|θ-grid| × (n+1)` PMF matrix and slows
down. There, an optional **numba** kernel (compiled to native code, skipping the uncovered `x`) is
**2–48× faster** on the coverage kernel and **33–62×** on root-finding.

- **How it's used:** if `numba` is installed (`pip install binomcikit[fast]`), it is selected
  **automatically** for large workloads (dense grid ≥ ~2,000,000 cells; roughly `n ≥ 400` with the
  default grid). Below that, numpy is used — it is faster there and avoids numba's compile warm-up.
  Everything **falls back to numpy** when numba is absent (`src/binomcikit/_accel.py`).
- **Why numba and not a rewrite:** we benchmarked it. numba reaches compiled-native speed — on the
  hardest case it *beat* idiomatic Haskell (176 ms vs 380 ms; numpy 7762 ms), i.e. within ~2–3× of
  any compiled language, from inside Python. A Rust/C++ rewrite would be *heavier* (a compiled build
  + per-platform wheels), not lighter, and would lose the scientific-Python ecosystem. Full numbers
  and reproducible scripts are in `benchmarks/` in the repository.

## Plotting — plotnine today, Plotly tomorrow

Two plotting paths coexist during the migration:

- **Plotly (the forward path):** `binomcikit.plot_ci` and `binomcikit.plot_coverage` return
  interactive `plotly` figures (used in the docs, the Streamlit app, and the PyQt GUI). Plotly is
  imported *lazily*, so the core package never depends on it.
- **plotnine (legacy):** the R-named `plot*` functions (`plotciwd`, …) still render static ggplot
  figures; they are retired method-by-method as each is migrated.

Plotting is **optional** — `pip install binomcikit[plots]` — and the core install imports with no
plotting stack at all (verified in CI).

## Install options (extras)

| install | you get |
|---|---|
| `pip install binomcikit` | **core** — numpy, scipy, pandas (all computation; no plotting) |
| `pip install binomcikit[fast]` | + **numba** accelerator for large-`n` metrics |
| `pip install binomcikit[plots]` | + **plotnine & plotly** for figures |
| `pip install binomcikit[test]` | + pytest, hypothesis, statsmodels, plotnine (to run the suite) |
| `pip install binomcikit[dev]` | + the above plus ruff, black, build, twine |

The `[fast]` extra carries a Python-version marker so it *degrades gracefully* (skips numba, no
install error) on a Python too new for numba to support yet.

## Reproducibility

Stochastic functions (Monte-Carlo coverage/length, empirical Bayes, and the future bootstrap /
betting methods) take a `seed=` argument and use numpy's `Generator`. Note: we **cannot** match R's
random draws bit-for-bit, so property/statistical assertions are used for those functions rather than
exact equality with R.

## Continuous integration

Every push runs, via GitHub Actions:
- the **test matrix** — Python 3.9–3.13 × Linux/macOS/Windows;
- **lint** — `ruff` + `black`;
- **`import-core`** — proves the package imports with **no** plotting stack (the optional-plotting guarantee);
- **`test-fast`** — installs `[fast]` and runs the suite against the numba path;
- **release** — publishes to PyPI on a GitHub Release via **Trusted Publishing (OIDC)**, no stored tokens.

---

*This page is the technical record. The full engineering contract, benchmarks, and per-method plan
live in the repository's `planning/` and `benchmarks/` directories.*
