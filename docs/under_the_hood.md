# Under the hood

How binomcikit computes, how fast it is, and how we know the numbers are right. This page **logs
the technical machinery** — validation, acceleration, plotting, packaging, CI — so it is transparent
and kept current as the package grows (every method sub-phase updates the relevant sections).

## Correctness — four independent oracles

binomcikit's results are checked against several *independent* sources of truth, so a bug would have
to fool all of them at once:

1. **Golden values from the source paper / closed form.** The Wald limits for `n = 5` are asserted
   against Table 2 of Subbiah & Rajeswaran (2017) — an oracle independent of *any* software. The
   **ArcSine** (`ARCSINE_N5`), **Logit-Wald** (`LOGIT_N5`), **Wald-T** (`WALDT_N5`) and
   **Likelihood-ratio** (`LR_N5`) limits for
   `n = 5` get the same treatment: no third-party library implements these methods, so these frozen
   constants from the published closed forms are their independent oracle, with companion tests
   pinning the structural quirk each method is known for — arcsine's boundary collapse, logit's exact
   one-sided substitution at x = 0, n, Wald-T's *t*-widening + no-ZWI boundary modification, and the
   LR interval bracketing the MLE (its numerical limits also cross-checked against an independent
   `brentq` root-find). (`tests/test_golden_paper.py`, values in `tests/cases.py`.)
2. **Cross-check vs `statsmodels`.** Wald, Wilson (Score) and Clopper–Pearson match
   `statsmodels.stats.proportion.proportion_confint` to **1e-9** (`tests/test_ci.py`); the exact
   family at `e = 1` reproduces `method="beta"` exactly; the Bayesian quantile interval with a Jeffreys
   prior (`a = b = 0.5`) reproduces `method="jeffreys"` exactly; and companion tests confirm Mid-P
   (`e = 0.5`) is never wider than Clopper–Pearson and that the Bayesian HPD carries 1 − α posterior
   mass while staying no wider than the quantile interval (`tests/test_golden_paper.py`).
3. **Completeness vs the R package.** Every one of the R `proportion` package's **305** exported
   functions must exist in binomcikit — checked against the vendored R NAMESPACE
   (`tests/test_completeness.py`, list in `tests/r_exports.txt`).
4. **Property-based tests (Hypothesis).** For *all* valid inputs — not just a fixed grid — limits
   stay in [0, 1], lower ≤ upper, and symmetric methods satisfy L(x) = 1 − U(n−x)
   (`tests/test_properties.py`).

**The accelerator can't change answers.** The optional numba fast-path is asserted **identical to
the numpy path to 1e-9** (`tests/test_accel.py`), so results never depend on whether `[fast]` is
installed. The full suite (**234 tests**) runs on every push across Python 3.9–3.13 on
Linux / macOS / Windows.

*As each method sub-phase lands, its rare-method + metric outputs get golden fixtures generated from
R, extending oracle #1/#3.*

**New methods verified by their defining theorems.** Blaker's interval (§ new in binomcikit, not in R
`proportion`) has no bundled reference implementation, so it is checked against the two properties that
*define* its value — it is **nested inside Clopper–Pearson** (never wider) and its **coverage is
≥ 1 − α** on a fine θ grid — plus an acceptance-boundary identity and frozen `BLAKER_N5` limits
(`tests/test_blaker.py`). Passing both theorems is stronger evidence than matching another program.

**Bootstrap — two verification strategies for two different risk levels.** `ciboot`'s
`kind="percentile"`/`"bca"` are thin wrappers around `scipy.stats.bootstrap`, so they are checked to
match scipy's own output **exactly, same seed in → same limits out** — scipy's own testing becomes the
oracle. `kind="smooth"` (Wang & Hutson 2013 [25]) is genuinely new code with **no third-party oracle**:
it is checked instead against (1) the paper's own closed-form boundary formulas for the
median-unbiased estimator, confirmed as an exact algebraic identity (not a fit); (2) rough agreement
with the oracle-verified percentile/BCa bootstrap away from `x = 0, n`; and (3) the specific property
the method exists for — a **non-degenerate interval exactly where the naive bootstrap collapses**
(`tests/test_bootstrap.py`). This is weaker evidence than golden-value or two-theorem verification, and
is flagged as such in `docs/methods/bootstrap.md` — the honest position is "good-faith verified," not
"gold-standard verified," for this one method.

**p-value tests — verified against the right oracle, not the obvious one.** `pvalue`/`reject` are
defined by CI-test duality (θ₀ rejected at level α iff it falls outside the method's `(1-α)` CI), so the
"obvious" oracle would be `scipy.stats.binomtest`. It is the wrong one: scipy's default two-sided
p-value uses a different ("minlike", smallest-probability) convention that genuinely disagrees with the
equal-tailed construction dual to binomcikit's own CIs — `tests/test_pvalue.py` locks in a case where
binomcikit's Clopper-Pearson p-value is exactly **2×** scipy's, on purpose. Verified instead against:
(1) the standard closed-form equal-tailed p-value formula for `method="exact"` (an independent, textbook
formula, not scipy); (2) the one-sided tail probabilities, which *do* match
`scipy.stats.binomtest(alternative="less"/"greater")` exactly (the one convention everyone agrees on);
and (3) the CI-duality property itself, checked directly against `bk.ci` across ten methods — the
strongest of the three, since it is literally the property that defines correctness here. Also locks in
a real, expected divergence: Wald's p-value differs from Wilson's/Clopper-Pearson's by 2-3 orders of
magnitude for the same `(x, n, theta0)`, because Wald's variance is estimated at p̂ rather than θ₀ — see
`docs/access_layer.md`.

**Sample-size / power — an independent oracle for Wald, the defining property for everything else.**
`sample_size(..., method="wald")` matches `statsmodels.stats.proportion.samplesize_confint_proportion`
**exactly** (both round to the same integer n across every tested width/p0) — a genuine, independent,
well-known closed-form oracle. For every other method, `sample_size` is checked against its own defining
property directly: the returned n's CI width is `<= width`, and `n - 1`'s is not — the smallest n that
actually satisfies the target, not an approximation. `power` is checked against an independent brute-
force construction built from `reject()` (already-verified, sub-phase 1.11) summed by hand over every
`x` — two independently-written paths to the same number, matching to floating-point precision.

**Known issue, discovered incidentally (not yet fixed): `cilrx`/`cilr` (the Likelihood-Ratio interval)
breaks at large n.** Stress-testing `sample_size`'s search up to `n_max = 100_000` surfaced a real,
pre-existing numerical bug unrelated to sample-size/power themselves: LR's root-find snaps to
essentially `[0, 1]` somewhere between `n = 25,800` (correct: width ≈ 0.0122, centered at 0.5) and
`n = 26,000` (broken: `L ≈ 6e-6, U ≈ 0.999996`) — a sharp cliff, not a gradual drift, suggesting a fixed
bracket or grid resolution hit rather than a slow precision loss. Every other method was checked well
past this range with no issue. `sample_size`/`power`'s own tests avoid the affected region (documented
inline in `tests/test_sample_size_power.py`) rather than silently working around it — this needs its own
investigation and fix in a future sub-phase; see `planning/CONTINUE_HERE.md` "Known issues".

## Coverage — measured, not just counted

Passing tests answers "does the suite pass"; it says nothing about how much of the source the suite
actually exercises. As of **2026-09-28**, `pytest --cov=binomcikit` (branch coverage) reports:

| | |
|---|---|
| **Total** | **64.8%** branch coverage (4,171 statements, 1,464 branches) |
| Best covered | `_accel.py`, `__init__.py` — 100%; most `ci`/`covp`/`err`/`expl`/`pconf` numeric modules sit 65–95% |
| Worst covered | the **legacy plotnine** `*_graph.py` modules (`adj_n_graph.py`, `base_n_graph.py`, `cc_n_graph.py`, `base_n_x_graph.py`) at **4–8%** — they render static figures that aren't asserted, and are slated for retirement once the Plotly migration (§ Plotting, below) finishes. They're the single biggest drag on the total; the numeric core is meaningfully higher than the headline number suggests. **Not excluded from the report** on purpose — the number stays honest rather than flattered.

The `coverage` CI job (`.github/workflows/ci.yml`) runs this on every push (Python 3.12, Ubuntu),
uploads the XML report as a build artifact, and **fails the build below 60%** — a regression floor
set under the current baseline, not a target to hit. Raise the floor as real coverage grows; never
lower it just to turn a red build green. Config lives in `pyproject.toml`'s `[tool.coverage.*]`
tables (`source = ["binomcikit"]`, `branch = true`).

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
- **`coverage`** — runs the suite under `pytest-cov`, uploads the XML report, and fails below 60% branch coverage (see Coverage, above);
- **release** — publishes to PyPI on a GitHub Release via **Trusted Publishing (OIDC)**, no stored tokens.

---

*This page is the technical record. The full engineering contract, benchmarks, and per-method plan
live in the repository's `planning/` and `benchmarks/` directories.*
