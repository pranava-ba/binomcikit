# binomcikit — Delivery Roadmap & Engineering Contract

> The "how we build" doc: the four goals, the phased plan (with **Phase 1 broken into
> method-by-method sub-phases**), the coding contract, and the **documentation architecture**.
> The *science* (gaps, novelty, per-method literature, deep dives) lives in
> [RESEARCH.md](RESEARCH.md). Index: [README.md](README.md).

## 0. Status — 2026-07-23
- Surface-complete Python port of R `proportion` (all 305 exports, six families).
- **Version 3.0.8**; **153 tests passing**.
- **Phase 0 D (packaging) + E (test hardening): DONE.** Phase 0 **A/B/C DEFERRED** (§8).
- **Sub-phase 1.0 (infrastructure) essentially DONE:** ① high-level `ci()` dispatcher (+ tests);
  ② docs scaffold (`docs/foundations/` + `docs/glossary.md`, wired in); ③ **vectorized (x, θ)
  metric engines** (coverage + expected-length — suite ~3× faster: ~60s → 20s, numerically
  identical); ④ **plotting made optional** (guarded imports; `plotnine` → `[plots]` extra; core
  install verified to import with plotnine *blocked*); ⑤ **CI** (OS × Py 3.9–3.13 matrix, ruff +
  black, core-import job) + **Trusted-Publishing** workflow. **159 tests pass; ruff + black clean.**
  Remaining before 1.1 Wald: type hints + `py.typed` (incremental, per method).
- **numba `[fast]` accelerator added** (`_accel.py`: compiled coverage kernel, numpy fallback,
  auto-dispatched by workload; tested to 1e-9; CI `test-fast` job). Decision-of-record: Python core
  + optional numba, **no compiled-language rewrite** (benchmarks in `../benchmarks/`).
- **Sub-phase 1.1 (Wald) in progress:** audit green (base = statsmodels + paper golden; AC + CC
  present, closed-form). **Docs exemplar shipped** — `docs/methods/wald.md` (two cores: *Use it* /
  *Understand it*), 6 new glossary terms, method-selection guide, all wired + **docs build clean**.
  Established the **Plotly plotting layer** (`plotly_viz.py`: `plot_ci`, `plot_coverage`; lazy
  import; tested) — the forward path that replaces plotnine method-by-method — and embedded the
  generated Wald-vs-Wilson-vs-ArcSine **coverage figure** (`docs/_static/wald_coverage.png`) in the
  docs. **164 tests pass; ruff + black + docs build clean. → Sub-phase 1.1 (Wald) COMPLETE.**

## 1. The four goals
1. **PyPI** — a well-documented, mathematically rigorous package.
2. **Streamlit** — a live hosted app.
3. **PyQt** — a desktop `.exe`.
4. **Paper** — a journal submission.

**Design principle: one core engine, three front-ends** — never fork the logic.

---

## 2. Phased delivery (overview)
- **Phase 0** — pre-release hardening (D/E done; A/B/C deferred, §8).
- **Phase 1** — Goal ① PyPI, run **method-by-method** (§3): infrastructure, then Wald →
  Wilson → … → Bootstrap, each finished *and documented* before the next.
- **Phase 2** — Goal ② Streamlit app (reuses the finished core). **Ship a lock file** pinning a
  numba-validated Python + numpy + numba trio and `binomcikit[fast]`, so the hosted app is always
  fast and reproducible (this is where "pin to numba-validated versions" correctly belongs).
- **Phase 3** — Goal ③ PyQt `.exe` (PyInstaller/Nuitka; same core). Bundle `binomcikit[fast]` with
  the **same pinned/validated** numba + numpy, so the desktop build ships the accelerator baked in.
- **Phase 4** — Goal ④ paper (rewrite `paper.md`; venue TBD; scope open).

---

## 3. Phase 1 — method-by-method sub-phases

Each sub-phase takes **one method** all the way to done (audit → complete functions →
optimize → test → **document** → benchmark) before the next begins. Agresti–Coull is the
*adjusted Wald* case, so it is covered inside the Wald sub-phase; likewise each method's
adjusted (`h`) and continuity-corrected (`c`) variants are handled within that method.

### 3.1 The sub-phases
| # | Sub-phase | Scope (variants owned) |
|---|---|---|
| **1.0** | **Infrastructure** (cross-cutting) | high-level `ci(x, n, method=…)` dispatcher; vectorized (x, θ) metric engine (perf Tier-1); plotnine→**plotly** migration; docs scaffold (§4); `py.typed` + type-hint conventions; CI matrix + Trusted-Publishing |
| **1.1** | **Wald** | Wald + **Agresti–Coull (=adjusted Wald)** + CC-Wald; ×{CI, covp, expl, pconf, err, plots} |
| **1.2** | **Score / Wilson** | + adjusted + CC |
| **1.3** | **ArcSine** | + adjusted + CC — *also fix the `p=sin²(φ)` doc formula* |
| **1.4** | **Logit-Wald** | + adjusted + CC |
| **1.5** | **Wald-T** | + adjusted + CC |
| **1.6** | **Likelihood Ratio** | + adjusted; **no CC** (matches R) |
| **1.7** | **Exact** | Clopper–Pearson + **Mid-P (e=0.5)** + generalized-`e`; base only (no adj/cc) |
| **1.8** | **Bayesian** | credible (equal-tailed + HPD) + 6xx toolbox: Empirical Bayes, posterior predictive, posterior probabilities, Bayes factors |
| **1.9** | **Blaker** ★ NEW | build the full family grid from scratch (RESEARCH §9.1) |
| **1.10** | **Bootstrap** ★ NEW | smooth (Wang–Hutson) + parametric/BCa (RESEARCH §9.2) |
| **1.11** | **Frequentist tests** ★ NEW | `binom_test`-style p-values per method (committed 2026-07-23; see §3.5) |
| **1.12** | **Sample-size / power** ★ NEW | planning functions for CI-width / power (committed 2026-07-23; see §3.5) |
| *(1.13)* | *(Betting / confidence-sequence — optional stretch; RESEARCH §8)* | *the "port + 2024 contribution" candidate; schedule if the paper wants it* |

### 3.2 The per-sub-phase workflow (run every time, in order)
1. **Audit — R ↔ Python compare & contrast.** Enumerate the R functions for the method
   (from `tests/r_exports.txt` / the R NAMESPACE), map each to its Python counterpart,
   **verify numeric equivalence** (oracle vs `statsmodels` where possible; golden vs R and vs
   the paper otherwise), and record any structural differences (e.g. LR has no CC; Exact/
   Bayesian have no adj/cc) and any behavioural differences (clamping, RNG).
2. **Sufficiency & additions.** Confirm the full family grid exists — base + given-x, adjusted
   (+h) + x, CC (+c) + x, and the four metric families (covp/expl/pconf/err) + all `plot*`.
   **Create what's missing or new** (see §3.3): the dispatcher entry, new-method grids
   (1.9/1.10), and any convenience wrappers (named Mid-P, named Jeffreys/AC, etc.).
3. **Performance.** Apply the §6 Tier-1 rules to *this* method's compute (closed form over
   root-finding; vectorize the (x, θ) grid; build DataFrames once). Add Numba (`[fast]`) only
   if a hot loop remains.
4. **Testing.** Oracle + golden(R/paper) + Hypothesis property tests + completeness; `seed=`
   for anything stochastic. Meet the Definition of Done (§7.10).
5. **Documentation.** Ship the two core pages for the method — **"Use it"** and **"Understand
   it"** — and add/link every new technical term in the **glossary** (§4). This is a hard gate:
   *no sub-phase is "done" until its docs exist.*
6. **Example + benchmark.** One worked example (the canonical n=5, α=0.05 case) and one
   comparison figure produced *by binomcikit's own metric suite* (this method vs the others on
   CP/EL) — which doubles as a paper figure.
7. **Bookkeeping.** `CHANGELOG.md` entry; API-consistency lint (naming, column schema,
   docstring completeness); update the growing **method-selection guide**.
8. **Review gate.** `ruff` + `black` + full `pytest` + docs build all green → proceed.

### 3.3 Per-method function audit (R ↔ Python) — is there enough, and what to add?
Verified against the code (2026-07-23). "Grid" = base + given-x (`x`) across all families.
Every existing method is a **faithful, complete mirror of R** — the gaps are the *new methods*
and the *cross-cutting conveniences*.

| Method | CI (base/x, adj/x, cc/x, plots) | covp / expl / pconf / err | adj? | cc? | vs R | New functions to add |
|---|---|---|:--:|:--:|---|---|
| **Wald** | ✅ full | ✅ base+adj+cc | ✅ | ✅ | complete | dispatcher entry `ci(...,method="wald")` |
| **Score/Wilson** | ✅ full | ✅ base+adj+cc | ✅ | ✅ | complete | dispatcher entry |
| **ArcSine** | ✅ full | ✅ base+adj+cc | ✅ | ✅ | complete | dispatcher entry; *fix doc formula* |
| **Logit-Wald** | ✅ full | ✅ base+adj+cc | ✅ | ✅ | complete | dispatcher entry |
| **Wald-T** | ✅ full | ✅ base+adj+cc | ✅ | ✅ | complete | dispatcher entry |
| **LR** | ✅ base/adj (no cc) | ✅ base+adj (no cc) | ✅ | — | complete (R excludes CC-LR) | dispatcher; consider exact-LR (Somerville–Brown [24]) |
| **Exact** | ✅ base + generalized-`e` | ✅ base | — | — | complete (R excludes adj/cc) | named `cimidp` (e=0.5) & `cicp` (e=1) convenience |
| **Bayesian** | ✅ `ciba`/`cibax` + 6xx toolbox | ✅ base (covpba/lengthba/pcopbiba/errba) | — | — | complete | named-prior presets (Jeffreys/Laplace/Haldane); HPD-for-arbitrary-prior helper |
| **Blaker** ★ | ❌ none | ❌ none | — | — | **absent (build)** | full grid: `ciblaker`/x + covp/expl/pconf/err + plots |
| **Bootstrap** ★ | ❌ none | ❌ none | — | — | **absent (build)** | `ciboot`/x (kinds: smooth/parametric/BCa) + metrics + plots; `seed=`,`B=` |

**Cross-cutting new functions (Sub-phase 1.0):**
- `ci(x, n, alpha, method=…, adjust=None, cc=None)` — one dispatcher over all methods.
- `compare(n, alpha, methods=…)` — run several methods + all metrics into one tidy table and
  one figure (the reproducible comparison the paper needs).
- vectorized internal engines (`_coverage_*`, `_expl_*`, …) rewritten per §6 Tier-1.

### 3.4 What else to do systematically (beyond the 8 steps)
Add these standing gates so quality compounds sub-phase over sub-phase:
- **Accessibility review** — a plain-language readability pass on each new doc page (§4.3).
- **Glossary-completeness check** — a docs-lint that flags any technical term not wrapped in a
  `:term:` link (§4.2); no page ships with an undefined technical word.
- **Benchmark regression** — keep a master CP/EL comparison table/figure; each sub-phase adds
  its method and re-runs it, catching accidental numeric drift.
- **API-consistency check** — signatures, column schema, and return types conform to §7; a
  small test asserts the schema per function.
- **Reproducibility** — `seed=` on every stochastic function; deterministic tests.
- **CI green** — matrix (Py 3.9–3.12 × Linux/macOS/Windows) + coverage gate + lint + docs build
  on every merge.
- **Versioning** — a minor bump + `CHANGELOG.md` entry per completed sub-phase.
- **Method-selection guide** — a living page that gains a "when to use / avoid" row per method.
- **Technical-notes log** — keep `docs/under_the_hood.md` current: whenever a sub-phase adds tests,
  an acceleration, a plot, or a golden fixture, log it there (numba behaviour, oracles, CI, extras).

### 3.5 Additional functions to add (completeness audit — beyond grids & cross-cutting)
Careful pass on "is the API robust/enough?" The method + metric + Bayesian **coverage** is
complete (it mirrors the peer-reviewed R package, verified 305/305), so nothing is missing
*there*. But a robust modern package needs a **usability & access layer** the R original lacks.

**Build (recommended):**
1. **Data-input layer** — `from_counts(x, n)` and `from_data(seq)` (derive x, n from a raw 0/1
   sequence); let `ci()` accept either. Required by bootstrap/betting (which need the sequence)
   and much better UX.
2. **Curve accessors** — `coverage_curve / length_curve / pconf_curve / error_curve(...)` return
   the underlying (θ, value) arrays that today are computed only *inside* `plot*` (the private
   `_coverage_curve` / `_expl_curve`). Real gap; near-zero effort (data already exists).
3. **Point estimators** — `point_estimate(x, n, method="mle"|"bayes"|"mue"|"ac"|"shrinkage")`
   (median-unbiased is needed by the bootstrap; unifies estimators scattered across methods).
4. **Method recommender** — `recommend(n, alpha, by="coverage"|"length"|"error", theta=Beta(a,b))`
   ranks methods via the metric engine — turns the selection guide into code (a novel feature).
5. **`compare(n, alpha, methods=…)`** — one tidy multi-method × multi-metric table + figure.
6. **Aggregator extension** — when new methods land, extend `ciall / covpall / lengthall /
   pcopbiall / errall` (+ plot-all) to include them, so comparisons stay complete.
7. **Bayesian conveniences** — named-prior presets (Jeffreys/Laplace/Haldane/custom);
   `posterior(x, n, a, b)` returning the Beta posterior + summaries; HPD-for-arbitrary-prior;
   a prior-sensitivity helper.

**Committed extensions (user decision 2026-07-23) — added as sub-phases 1.11–1.12:**
- **Frequentist p-value tests** per method (`binom_test`-style) — *Sub-phase 1.11*.
  *Why the original paper omitted them:* by **CI–test duality**, a two-sided level-α test and a
  (1−α) confidence interval are equivalent — θ₀ is rejected exactly when θ₀ falls outside the
  interval — so the CIs already *encode* the tests, and the authors treated explicit test functions
  as redundant (they state the duality "excludes adding additional functions"). We add them anyway
  because they are more convenient for users who think in tests, and because duality is only
  *approximate* for some methods (e.g. Wald), so an explicit test can differ subtly and is worth
  exposing.
- **Sample-size / power** planning — *Sub-phase 1.12*.
  *Why the paper omitted it:* sample-size is a *pre-data design* question, outside the paper's
  stated scope (post-data *estimation* + evaluation + Bayesian computation), and a dedicated package
  (`binomSamSize`) already existed, which the paper cites in its landscape rather than duplicating.
  We include it because it is high-value for practitioners planning a study.

**Planned as a SEPARATE next package (sequel) — NOT part of binomcikit:**
- **Two-proportion inference** (difference / ratio of two proportions) — the 2017 paper's own named
  next direction; a large area with its own literature and R packages. It will be its **own package**
  built on the same engine, *after* binomcikit's single-proportion scope is complete.

**Deferred (nice-to-have):** batch mode over arrays of (x, n).

**Not needed:** CC-LR / adjusted-exact / adjusted-Bayesian — R excludes these deliberately and
they are not standard; skipping them is correct, not a gap.

**Verdict:** the six families (1.0–1.9) are the complete statistical *core*; with the new
methods (Blaker, bootstrap, betting) plus the access layer above, the package becomes robust
and *more* than the R original — nothing essential is missing.

---

## 4. Documentation architecture

**Goal (the user's bar):** documentation so robust that *someone who has not yet learned basic
probability* can follow along and learn from it. Every method's docs have **two cores** — how
to *use* it and the *maths/theory* behind it — plus a **glossary that links every technical
term**, and an **accessibility ladder** that starts from zero.

### 4.1 Two cores per method/metric page
Each page (per method, per metric, per Bayesian tool) has two clearly separated parts:

**A — "Use it" (the how).**
- install / import; the function signature and every parameter (plain-English + formal);
- the return schema (columns, index, types) with a rendered example table;
- runnable, copy-pasteable examples (start with the tiny n=5 canonical case);
- common recipes ("get just the interval for x successes", "compare two methods", "plot it");
- gotchas / edge cases (x=0, x=n, small n) and error messages.

**B — "Understand it" (the why/maths).**
- a one-sentence plain-English "what this is";
- the **intuition** before any symbol (a coin-flip story);
- the **formula**, with *every symbol defined and linked* to the glossary;
- a short derivation / where it comes from; assumptions; when it works and when it fails;
- how it compares to neighbours (link the RESEARCH §6 verdict);
- the reference `[n]` (RESEARCH §11) and the `docs/theory/` deep page.

### 4.2 Glossary — link every technical term (explicit requirement)
- A single **`glossary`** page (Sphinx `.. glossary::` directive) defines **every** technical
  term once, in plain language, with a tiny example (e.g. *proportion, trial, Bernoulli,
  random variable, probability, confidence interval, coverage, quantile, prior, posterior,
  likelihood, continuity correction, Beta distribution, …*).
- **Every occurrence** of a technical term anywhere in the docs is written as
  `` :term:`coverage` `` so it hyperlinks to its glossary entry. Optional `sphinx-hoverxref`
  shows the definition on hover.
- **Enforcement:** a docs-lint (CI check) scans pages against the curated term list and fails
  the build if a listed term appears un-linked — this operationalises "link out every single
  word or definition that might be technical."
- Each page ends with a **"Terms used"** box listing its glossary links, as a quick index.

### 4.3 Accessibility ladder — "probability from zero"
- A **Foundations** track (its own top-level section) builds from nothing: *what is a
  proportion → what is a trial / a coin flip → randomness & sampling → what a confidence
  interval really means (and what it does not) → why coverage matters → why methods differ.*
  Plain language, tiny numbers, pictures; **prerequisites: none**.
- **Progressive disclosure** on every page: the plain explanation is always first; formulas
  and proofs live in collapsible "For the curious / The maths" admonitions so a beginner can
  skip them and an expert can expand them.
- A **guided path** ("New here? Start with Foundations → Wald → …") and a one-line "what you'll
  learn / what you need to know first (nothing)" header on each page.
- Visual intuition everywhere (interactive plotly once migrated); worked numeric examples with
  numbers small enough to check by hand.

### 4.4 Site structure & tooling (Sphinx)
```
Foundations/        probability from zero (§4.3)          [read first]
Methods/            one page per method, each Use it + Understand it (§4.1)
Evaluation metrics/ coverage, length, p-confidence, error — Use it + Understand it
Bayesian toolbox/   credible intervals, EB, predictive, Bayes factors
Method-selection guide   "which interval when" (grows each sub-phase)
Theory series/      the existing docs/theory deep maths
Glossary            every technical term, auto-linked (§4.2)
API reference       autodoc of every public function
```
Tooling: Sphinx + MyST (Markdown), `:term:` glossary, `sphinx-copybutton`, `sphinx-hoverxref`,
doctest on examples, Read the Docs build in CI.

### 4.5 Per-sub-phase documentation deliverable (the gate in §3.2 step 5)
When a sub-phase closes, it must have shipped: the method's **Use it** + **Understand it**
pages, its **glossary** entries (linked), one **worked example**, one **comparison figure**,
and a row in the **method-selection guide** — all building on the shared **Foundations** track.

---

## 5. Plotting decision — migrate to Plotly
**Decision:** replace `plotnine` with **`plotly`** — native to Streamlit (goal 2), embeddable in
PyQt via QWebEngineView (goal 3), interactive, one library for both front-ends. Done as a **split**
so no effort is wasted:
- **Infrastructure — DONE (the safer fix):** plotting imports are **guarded** in every family
  `__init__`, and `plotnine` moved to the optional **`[plots]`** extra (with `plotly`). The core
  install is numeric-only and imports **without any plotting stack** — CI's `import-core` job
  verifies it. No plot was rewritten, so nothing was thrown away.
- **Per-plot rewrite — deferred to each sub-phase:** converting a method's `plot*` functions from
  plotnine (ggplot) to plotly happens when we do that method, where the figure can be seen and
  checked. `plotnine` stays the renderer for not-yet-migrated plots; the `[plots]` extra carries
  both during the transition.

---

## 6. Performance plan — benchmarked (see [`../benchmarks/`](../benchmarks/README.md))

**Language decision (2026-07-23): Python core + optional `numba`; NO Rust/C++/Haskell rewrite, and
no need to install Rust.** numba reaches compiled-native speed — **176 ms** vs Haskell GHC ‑O2
**380 ms** vs numpy **7762 ms** on the n=500 coverage kernel (within ~2–3× of any compiled language,
from inside Python, prebuilt wheels, numpy fallback). A Rust/PyO3 rewrite would be *heavier*
(compiled artifact + per-platform wheel matrix), not lighter; the ~218 MB / ~1.9 s install weight is
numpy+scipy+pandas, kept for the DataFrame / `scipy.stats` / ecosystem deliverables. Measured: numba
is **2–48×** over numpy on the coverage kernel and **33–62×** on root-finding. Caveat: vectorized
numpy is great for small n (the common case) but **degrades at large n** (dense `S×(n+1)` matrix) —
numba (Tier 2) is the large-n path. Full numbers + rationale: `benchmarks/README.md`.

**Tier 1 (do first, pure Python):** (1) closed form over root-finding — Beta quantiles for
Exact/CP/Mid-P, closed forms for Wilson/AC/ArcSine/Logit, `brentq` only for LR/generalized-`e`;
(2) **vectorize metric engines over the (x, θ) grid** (broadcast PMF matrix; no Python θ-loop);
(3) build DataFrames once from arrays. **Tier 2:** `numba @njit` on residual scalar loops
(`[fast]` extra). **Tier 3:** Rust (PyO3)/JAX/polars only after profiling. **Tier 4:** lazy +
optional plotting; cache z/Beta quantiles. **Per-PR checklist:** ☐ no θ-loop ☐ no per-row
DataFrame growth ☐ closed form where it exists ☐ no plotting import at module top ☐ vectorized PMF.

---

## 7. Engineering contract (coding rules)
Grounded in an audit of `src/binomcikit/`. **[current]** = how the code is; **[new]** = adopt in the overhaul.

**7.1 Layout.** Six family subpackages (`ci`/`covp`/`expl`/`pconf`/`err`/`bayes`); numeric in
`base_all.py`/`base_n.py`, graphics in `plots.py`/`*_graph.py`; flat public API via `__all__`
re-exports. A new method is a module exposing a limit-producer (7.4), wired into `__all__`.

**7.2 Naming.** `[plot]` + `ci` + `{wd/sc/as/lt/tw/lr/ex/ba/all}` + `{x, a, c}` → `ciwd`,
`ciawd`, `cicwdx`, `plotciall`. Columns `L{CODE}/U{CODE}`; flags `LABB/UABB/ZWI`. Metric
families `covp*/length*/pcopbi*/err*`. Candidate codes: `blaker`, `boot`, `bet`, `pratt`, `cll`/`probit`.

**7.3 Sample data.** None — inputs are `(x, n, α, priors)`. Canonical cases in `tests/cases.py`.

**7.4 Shared engine / limit-producer contract.** Each family's `base_all.py` has a
method-agnostic engine (`_pconf_pbias`, `_error`, `_expl_*`, `_coverage_*`) + `_validate*` +
`_base/_adj/_cc` dispatchers. **A new method supplies `x ↦ (L[x], U[x])` (+ ZWI/LABB/UABB);
register it in the dispatchers, and it inherits `covp*/length*/pcopbi*/err*` + all `plot*` with
no new engine code.** Never reimplement metrics per method.

**7.5 Testing.** (i) oracle vs `statsmodels`; (ii) smoke from R `@examples`; (iii) `hypothesis`
property tests; + golden (paper Table 2; **[new]** golden-vs-R for rare methods/metrics) +
completeness vs `tests/r_exports.txt`.

**7.6 Dependencies.** Core `numpy>=1.22`, `scipy>=1.8`, `pandas>=1.4`. Plotting `plotnine`
(→ `plotly` `viz`, 1.0). Optional `[fast]` numba. Dev/test `pytest`,`hypothesis`,`statsmodels`
(test-only),`ruff`,`black`. Add `py.typed`.

**7.7 Return & validation.** pandas `DataFrame` (all-x = `n+1` rows indexed x=0…n; documented
schema) + the new `ci()` dispatcher + type hints. Clamp to `[0,1]`; `ZWI` at x=0,n; `LABB/UABB`.
`_validate*` raises on domain errors (`n>0`,`x∈{0…n}`,`0<α<1`,`a,b>0`,`h≥0`,`c≥0`,`0≤e≤1`).

**7.8 Reproducibility.** `seed=` (numpy `Generator`); cannot match R RNG draw-for-draw — test properties.

**7.9 Style.** `ruff` (`F`,`I`) + `black`, line 100, py39; NumPy-style docstrings with formula,
example, and the RESEARCH §11 reference `[n]`.

**7.10 Definition of Done (any new method/metric).** ☐ 7.2 naming + registered ☐ `_validate*` +
clamp + flags ☐ reuses engine (7.4) ☐ type hints + docstring w/ formula + ref ☐ tests
(oracle/golden + smoke + property; `seed=` if stochastic) ☐ §6 perf checklist ☐ **docs: Use it +
Understand it + glossary (§4)** ☐ no import-time heavy dep ☐ `CHANGELOG.md` entry ☐
`ruff`+`black`+`pytest`+docs-build green.

---

## 8. Deferred hardening (Phase 0 A/B/C — after the package is complete)
- **A — Rotate the once-plaintext credentials** (history already clean; rotate as precaution).
- **B — Fix the ArcSine README formula** (`sin²(φ/2)` → `p = sin²(φ)`; code already correct). Done inside Sub-phase 1.3's docs, or here — docs-only.
- **C — Relicense to GPL-2** (upstream `proportion` is GPL-2-only) + attribution to Subbiah &
  Rajeswaran. Until done, `pyproject`/`CITATION` remain GPL-3.0.

---

## 9. Immediate next actions
1. **Sub-phase 1.0 (infrastructure):** `ci()` dispatcher + type hints; the vectorized (x, θ)
   metric engine (Tier-1); the plotnine→plotly migration; the Sphinx docs scaffold (§4:
   Foundations skeleton + glossary + the Use-it/Understand-it page template); CI + Trusted
   Publishing.
2. **Sub-phase 1.1 (Wald):** run the §3.2 workflow end to end — the template for all the rest.
3. Then 1.2 → 1.10 in order, documenting each before moving on.

---

## 10. Open decisions (awaiting your call)

### 10.1 How "done" is a method's plotting?
Wald established a **new Plotly layer** (`plot_ci`, `plot_coverage`), but the R-named plotnine plot
functions (`plotciwd`, `plotcovpwd`, `plotexplwd`, `plotpcopbiwd`, `ploterrwd` + adj/cc — ~15) still
return `ggplot`. Two options, to apply to **every** method:
- **(A) Interim — recommended.** Treat the generic Plotly `plot_ci`/`plot_coverage` as each method's
  plotting deliverable; **retire the whole plotnine `plot*` family in one later batch** (they share
  helpers, so converting them per-method is the expensive path we agreed to avoid). Also defer
  `py.typed` + type hints to one incremental pass.
- **(B) Fully close each method now.** Convert that method's plotnine `plot*` functions to Plotly
  (which means converting the shared plotnine helpers) **and** add type hints, before moving on.
  More thorough, much slower; only worth it if per-method plotnine parity matters.
*Until this is settled, a sub-phase is marked "docs+figure done", not "DoD-complete".*

### 10.2 Should numba be installed & used by default?
Currently numba is the optional `[fast]` extra, auto-used only for large-n metrics (numpy otherwise).
- **(A) Keep optional — recommended.** numba pulls `llvmlite` (a ~30–40 MB compiled LLVM binding) and
  historically **lags new Python/numpy releases** (it can pin `numpy<X` and block installs on the
  newest Python for months). A hard dependency would risk "can't `pip install binomcikit` on the
  newest Python yet" — bad for a package whose value is broad availability (goals 1–3). And for
  **small n numpy is faster** than numba (which also pays a 1–2 s first-JIT cost), so always-on would
  hurt the common case.
- **(B) Make numba a core dependency** (installed by default) **but keep the size threshold** so it
  auto-accelerates large-n out of the box while numpy still handles small n. Gives "fast without
  thinking about it" at the cost of the heavier/fragile install above. *(Not* "always use numba" —
  that would slow the common small-n case.)
Either way, results are identical; only speed and install weight change.

**Sweet spot (recommended resolution) — "applications pin, libraries stay flexible."**
- **Library (goal 1):** numba stays **optional** (`[fast]`) so the *core install never constrains
  numpy* → installs on every Python; the runtime auto-falls back to numpy, so it **never breaks**
  (done). This is the non-negotiable part.
- **Apps / exe (goals 2–3):** ship a **lock file** pinning a numba-validated Python + numpy + numba
  trio — this is exactly where "pin to Numba-validated versions" belongs (a controlled environment
  where reproducible + guaranteed-fast is correct).
- **Maintainer:** the `test-fast` CI job exercises the numba path; the main `test` matrix already
  proves the core installs on every Python *without* numba; check numba's release timeline before
  bumping the base Python. (Build-from-source is a maintainer-only escape hatch, not a user story.)
- **Optional polish:** an environment marker on `[fast]` (`numba>=…; python_version < "3.x"`) so
  `pip install binomcikit[fast]` **degrades gracefully** instead of erroring on a too-new Python.
