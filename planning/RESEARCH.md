# binomcikit — Research & Methods (complete)

> The single, complete source of truth for the science behind binomcikit: the problem, the
> five research gaps, the competitive landscape and novelty, how binomcikit improves on the
> original R package, a fully-referenced per-method literature review, the post-2017
> developments and candidate-method menu, and full technical deep dives on the top candidate
> methods. Nothing is abbreviated here — this is the long reference. The delivery plan and
> coding contract live in [ROADMAP.md](ROADMAP.md).
> References are numbered `[n]` (§11). Verified via web scan 2026-07; the betting paper [31]
> and Wang–Hutson [25] were read from source.

## Contents
1. The problem & the core idea · 2. Research gaps · 3. Competitive landscape · 4. How
binomcikit improves on R `proportion` · 5. Novelty & positioning · 6. Methods literature
review · 7. New since 2017 & candidate-method menu · 8. Deep dive: betting / confidence
sequences · 9. Deep dive: Blaker, bootstrap & the rest · 10. Timeline · 11. References

---

## 1. The problem & the core idea

Estimate a single binomial proportion θ from *x* successes in *n* independent Bernoulli
trials, and — crucially — **evaluate** the estimator's quality. This is one of the oldest
problems in statistics, yet still actively researched, which is what makes a comprehensive
computational tool valuable rather than redundant. Three framing facts:

1. **No method is uniformly best.** The Wald interval is a textbook staple with famously
   erratic coverage (Brown, Cai & DasGupta [16]); Wilson, Agresti–Coull, Jeffreys, and the
   exact methods each win under some (n, θ) regimes and lose under others — Pires & Amado [21]
   compared **twenty** methods and found no dominator. The difficulty concentrates on **sparse
   data** and on **θ near the 0/1 boundary**.
2. **Even the evaluation criteria are unsettled.** Coverage probability (CP) and expected
   length (EL) are not enough: Vos & Hudson [19] introduced **p-confidence / p-bias** to
   capture directional error; Martín-Andrés & Álvarez [26] added an **error / long-term
   power** criterion; and the debate continues into the 2020s (the 2024 "locally correct"
   criterion [32]; the rare-events reframing [34]). A tool that *computes these criteria* is a
   research instrument, not a settled utility.
3. **The methodological frontier is open.** The 2017 paper itself names **bootstrap intervals**
   and **CP/EL-optimal exact methods** (Wang [28]; Thulin [27]) as extensions it did not build.
   **Blaker's** exact interval [15] — narrower than Clopper–Pearson — is absent from `proportion`
   entirely.

**Consequence:** the contribution is not "another CI function." It is a *unified, tested,
reproducible computational environment* for **choosing and evaluating** methods — delivered to
the Python ecosystem, where the original R tool never reached and where it is now, in effect,
unavailable (archived from CRAN 2022-04-27).

> ### The core idea (why binomcikit is a framework, not a calculator)
> **Decouple interval *construction* from interval *evaluation*.** A method contributes only
> a rule that maps each x ∈ {0,…,n} to limits (L, U); everything else — coverage probability,
> expected length, p-confidence / p-bias, error, aberrations, ZWI, and the comparison plots —
> is a **shared, method-agnostic engine**, parameterized by a θ-space Beta(a,b) (of which the
> uniform grid is a=b=1) and by three generalization operators: adjustment factor *h*,
> continuity correction *c*, and exact parameter *e*. **"Any method in → the same diagnostics
> out."** That is why adding a method (Blaker, bootstrap, betting, …) is cheap: write one
> limit-producer and it inherits the entire evaluation / graphics / Bayesian-comparison stack.
> *This is not aspirational — the code already implements it:* the engines (`_pconf_pbias`,
> `_error`, `_coverage_*`, `_expl_*` in each family's `base_all.py`) consume `(lower, upper)`
> and never know which method produced them. Tables **3.1** (methods — *what you plug in*) and
> **3.2** (diagnostics — *what you get out*) are the two halves of that idea.

---

## 2. Research gaps (the five-gap framework)

Each gap is a *domain-specific* claim (not a generic template), with its concrete manifestation,
the evidence it is real, and how binomcikit addresses it.

### 2.1 Evidence gap — *the comparative evidence is fragmented and non-reproducible*
**Claim.** Twenty-plus years of method-comparison studies exist, but as **static tables in
PDFs**, each generated with a *different* evaluation setup (different n-ranges, θ-grids,
weighting, and metrics). There is no single artifact that *regenerates* the comparison so a
practitioner can reproduce or re-parameterize it.
**Evidence.** Brown–Cai–DasGupta [16], Pires–Amado [21] (20 methods), Reiczigel, Newcombe [14,23]
— mutually inconsistent recommendations; none ships runnable comparison code, least of all in
Python.
**How binomcikit closes it.** A reusable evaluation harness (CP, EL, p-confidence, p-bias,
error) that regenerates head-to-head comparisons on demand, over a user-chosen θ-space, with
the comparison plots as first-class output.

### 2.2 Empirical gap — *Python practitioners have no diagnostic data for these methods*
**Claim.** The applied majority now works in Python (data science, ML, epidemiology pipelines),
but has **no Python-native, tested tooling** to produce coverage/length/error diagnostics for a
chosen interval. As a result, applied Python papers rarely report *any* CI-quality diagnostics —
they call `statsmodels` and move on.
**Evidence.** `statsmodels`, `scipy`, `astropy`, `pynomial`, `binoculars` all return *intervals*
but **none** returns coverage-probability or expected-length **as reusable metric functions** (§3).
The diagnostic layer simply does not exist for Python users.
**How binomcikit closes it.** Ships the metric layer, so Python users can *empirically* justify a
method on their own (n, α, prior) rather than trust a default.

### 2.3 Knowledge gap — *the advanced diagnostics never reached the Python/ML audience*
**Claim.** The concepts of **p-confidence, p-bias, error/long-term power, aberrations
(LABB/UABB), and zero-width intervals (ZWI)** are essentially unknown outside a small R
statistics circle, and absent from every mainstream Python library and most computational
textbook treatments.
**Evidence.** A targeted search for "p-confidence / p-bias" in software returns **only** the
Vos–Hudson [19] paper and derivatives — **zero** package implementations in any language except
the (archived) R `proportion`. The decision knowledge ("which interval, when, and how to *prove*
it") is undocumented for the Python audience.
**How binomcikit closes it.** Implements these diagnostics *and* documents the mathematics (the
`docs/theory/` "Methods & Mathematics" series), porting the knowledge, not just the code.

### 2.4 Theoretical / conceptual gap — *the unifying abstractions are un-formalized and un-implemented*
**Claim.** The literature treats each method as a separate recipe. Three unifying abstractions
are under-formalized and have **no reference implementation** outside the archived R package:
- the **adjustment factor *h*** as a *single operator* applied to any base method (add *h* to *x*,
  adjust *n*);
- the **exact parameter *e*** as a *continuum* from Mid-P (e=0.5) to Clopper–Pearson (e=1), with
  arbitrary e in between;
- a **general θ-space evaluation via Beta(a,b)** (the uniform grid is the special case a=b=1),
  plus an evaluation interface that scores limits from *any* method (incl. future/bootstrap).
**Evidence.** No Python package exposes any of these as a framework (§3); even in R they live only
in `proportion`.
**How binomcikit closes it.** Provides all three as explicit, composable, documented APIs — the
conceptual contribution, not just a method list.

### 2.5 Methodological gap — *prior implementations lack validation rigor, and two method families remain unbuilt*
**Claim.** Prior implementations (R **and** Python) largely lack automated correctness testing
against ground truth, and the paper's own stated extensions were never built.
**Evidence.**
- The original R `proportion` **shipped without a test suite** and was **archived from CRAN on
  2022-04-27 for unfixed check issues** — i.e. the reference implementation is itself unmaintained
  and no longer installable via `install.packages()`.
- Python ports of *pieces* (`pynomial`) cover none of the metrics.
- **Bootstrap CIs** (Wang & Hutson [25]) and **CP/EL-optimal exact intervals** (Wang [28]; Thulin
  [27]) — named as future work in the 2017 paper — remain unimplemented; **Blaker's** interval [15]
  is absent from `proportion`.
**How binomcikit closes it.** Adds validation rigor (tests vs `statsmodels`; golden files vs R;
property-based tests) **and** is positioned to implement the open frontier (Blaker, bootstrap,
optimality — §7, §9).

---

## 3. Competitive landscape (verified 2026-07)

### 3.1 Base confidence-interval methods — coverage by package
✅ = packaged one-call; ➖ = derivable but not packaged; ❌ = absent.

| Method | statsmodels | scipy.binomtest | astropy | pynomial | binoculars | binomial_cis | **R proportion** | **binomcikit** |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Wald | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| Wilson / Score | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| Agresti–Coull | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ |
| Clopper–Pearson (exact) | ✅ | ✅ | ❌ | ✅ | ❌ | ✅¹ | ✅ | ✅ |
| Jeffreys | ✅ | ❌ | ✅ | ➖ | ✅ | ❌ | ✅² | ✅² |
| Likelihood Ratio (LR) | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ |
| Logit-Wald | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ |
| **ArcSine** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Wald-T** (Pan 2002) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Mid-P** (exact e=0.5) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Generalized exact** (any *e*) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Bayesian HPD, Beta(a,b) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Bayesian equal-tailed, Beta(a,b) | ➖ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ | ✅ |
| **Continuity-corrected variants** (Wald/Score/ArcSine/Logit/Wald-T) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Adjustment-factor *h* framework** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Blaker (exact, narrower than CP) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌³ |
| Bootstrap | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌³ |

¹ `binomial_cis` returns a single *length-optimal* interval, not Clopper–Pearson per se.
² Jeffreys = Bayesian Beta(½,½) special case. ³ **Opportunity** — candidate to add (§7, §9).

### 3.2 Evaluation metrics & Bayesian toolbox — coverage by package
| Capability | statsmodels | scipy | pynomial | pingouin | **R proportion** | **binomcikit** |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| Coverage probability (reusable fn + summaries) | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Expected length (reusable fn + summaries) | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **p-confidence / p-bias** (Vos–Hudson) | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Error / long-term power** (Martín-Andrés) | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Aberrations (LABB / UABB) | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Zero-width intervals (ZWI) | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| MC evaluation over θ ~ Beta(a,b) | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Bayes factor (directional θ<θ₁ vs θ≥θ₂) | ❌ | ❌ | ❌ | ~⁴ | ✅ | ✅ |
| Empirical Bayes | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Posterior predictive (Beta-Binomial) | ➖⁵ | ➖⁵ | ❌ | ❌ | ✅ | ✅ |
| Posterior probabilities of θ\|X | ➖ | ➖ | ❌ | ❌ | ✅ | ✅ |
| Comparison plots for all of the above | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |

⁴ `pingouin.bayesfactor_binom` does a *point-null* BF only, not the directional/range test.
⁵ `scipy.stats.betabinom` gives the density but not a packaged predictive-inference routine.

### 3.3 The white space (one sentence)
**Everything in §3.2, plus ArcSine / Wald-T / Mid-P / generalized-exact / all continuity-corrected
variants / the *h*-framework from §3.1, is absent from the entire Python ecosystem** — and the one
tool that had it (R `proportion`) is archived. That intersection is binomcikit's uncontested
territory.

### 3.4 Closest "competitors," and why they don't overlap
- **`statsmodels` / `scipy` / `astropy`** — the *common* intervals only; no metrics, no rare
  methods, no Bayesian toolbox. binomcikit **validates against them** (they are the oracle for
  shared methods), not competes.
- **`pynomial`** — the nearest in spirit (a port of R `{binom}`), but `{binom}` ⊂ `proportion`;
  it has none of the metrics or the extended Bayesian/exact machinery.
- **`binomial_cis`** (JOSS-published) — solves a *different* problem: one interval that is
  length-optimal subject to exact coverage. That is "give me the best single interval," whereas
  binomcikit is "compare and diagnose many classical/Bayesian methods." Orthogonal; cite and
  differentiate.
- **R `DescTools::BinomCI`** — the strongest *current* R competitor (Wilson, Wald, ArcSine, Blaker,
  Mid-P, …), but it is R-only and is a *CI calculator*, not an evaluation suite; no
  p-confidence/p-bias/error, no Bayesian toolbox.

---

## 4. How binomcikit improves on the R `proportion` package

Not merely a translation. The concrete improvements, strongest first:

1. **Revives an abandoned reference tool.** `proportion` was **removed from CRAN (2022-04-27)** for
   unresolved check failures. The canonical implementation is effectively unavailable to new users;
   binomcikit restores and modernizes its capability.
2. **Brings it to the ecosystem that needs it.** Python is where most applied estimation now
   happens; binomcikit interoperates with `numpy`/`scipy`/`pandas`, installs with `pip`, and can be
   embedded in pipelines, notebooks, a Streamlit app, and a desktop GUI (goals #2–3) — reach the R
   original never had.
3. **Adds real validation.** The R package shipped **without automated tests** (and was archived for
   failing checks). binomcikit tests numeric output against `statsmodels` for shared methods, with
   golden values from the source paper's Table 2 and planned **golden-file** fixtures generated from
   R for the *rare* methods and *metrics*, plus **property-based** tests (L≤U, limits∈[0,1],
   monotonicity, x↔n−x symmetry, ZWI only at boundaries).
4. **Performance.** Replace per-*x* root-finding with closed forms where they exist (Beta-quantile
   exact/Mid-P; closed-form Wilson/AC/ArcSine/Logit) and **vectorize the metric engines** over the
   (x, θ) grid — order-of-magnitude speedups that also make the interactive app responsive (details
   in [ROADMAP.md](ROADMAP.md) §4).
5. **Modern software engineering.** Type hints + `py.typed`, a high-level `ci(x, n, method=…)`
   dispatcher alongside the R-style names, consistent typed returns, Sphinx API docs, CI/CD,
   semantic versioning — none of which the R package offered.
6. **Reproducibility & distribution.** Versioned PyPI releases, a reproducible figure/benchmark
   script that regenerates the comparison plots, and the mathematical exposition in `docs/theory/`.
7. **Correctness/clarity fixes.** e.g. the ArcSine back-transform is stated correctly in code and
   the documentation is being corrected to match (`p = sin²φ`, not `sin²(φ/2)`); the R package's
   misspelled `empericalBA` is corrected to `empiricalba`.
8. **Method frontier (proposed — turns "port" into "port + contribution").** Implement what even
   `proportion` lacks and what its own authors flagged as future work: **Blaker's exact interval**
   [15]; **Bootstrap CIs** (Wang & Hutson [25]) — the package already scores limits from *any*
   method, so bootstrap slots into the evaluation harness cleanly; **CP/EL-optimal / coverage-
   adjusted intervals** (Wang [28]; Thulin [27]); and the post-2017 **betting / confidence-sequence**
   family [31,29]. Any one lifts a resubmitted paper from "software port" to "software + novel
   methodological contribution."

---

## 5. Novelty statement & positioning

> **binomcikit is the only Python package to deliver the *complete* single-proportion toolkit of
> the (now-archived) R `proportion` package: rare interval methods absent from Python entirely
> (ArcSine, Logit-Wald one-liner, Wald-T, Mid-P, generalized-exact, all continuity-corrected
> variants, and the unified adjustment-factor framework); a full, reusable evaluation suite
> (coverage probability, expected length, p-confidence, p-bias, error/long-term power, aberrations,
> ZWI) with Monte-Carlo θ-space evaluation; and a Bayesian tool box (directional Bayes factors,
> Empirical Bayes, posterior predictive, posterior probabilities) — tested, typed, documented, and
> pip-installable.**

**Honesty guards (so reviewers trust the claim):**
- Do **not** claim novelty for the common CIs; state plainly they exist in `statsmodels`/etc. and
  that binomcikit validates against them.
- Position `binomial_cis` (optimal single interval) and `pynomial` (subset port) as adjacent, not
  competing.
- Foreground the **metric suite + rare methods + Bayesian toolbox** — the genuinely empty region of
  the Python ecosystem.

**JOSS "substantial scholarly effort" mitigation.** The v0.0.5 pre-review rejection (#7839) was fair
for a CI-only wrapper. The full-scope package (metrics + Bayesian toolbox + tests + docs), *ideally
plus one §7/§9 method extension*, is a different submission. If JOSS is retried, lead the paper with
the evaluation/Bayesian machinery and cite the archived-CRAN status as motivation.

---

## 6. Methods literature review

Each base-method block: **definition → origin → developments since → verdict**. R/Python name in
`code font`. Notation: p̂ = x/n, q̂ = 1−p̂; z = z_{1−α/2} the standard-normal quantile; B⁻¹(·;a,b)
the Beta quantile function; χ²_{1,1−α} = z²; "CC" = continuity correction.

### 6.1 Base interval methods

**Wald (asymptotic normal)** `ciwd`
- *Definition.* p̂ ± z·√(p̂q̂/n). SE evaluated at the MLE.
- *Origin.* The textbook large-sample interval; Laplace-era normal approximation.
- *Developments / verdict.* Comprehensively discredited: coverage is erratic and often far below
  nominal even for large *n*, and it collapses (zero width) at x = 0, n. Brown, Cai & DasGupta
  [16,17] made this the canonical cautionary tale; still used as a teaching "bad example."
  **Keep only for pedagogy / CC-comparison.**

**Score / Wilson** `cisc`
- *Definition.* (p̂ + z²/2n ± z·√(p̂q̂/n + z²/4n²)) / (1 + z²/n); SE evaluated under H₀.
- *Origin.* Wilson (1927) [1].
- *Developments since.* Repeatedly recommended as a default (Agresti & Coull 1998 [13]; Newcombe
  1998 [14]; Brown–Cai–DasGupta 2001 [16]). Active refinement continues: finite-population and
  mathematical-properties analyses (2021); **continuity-corrected Wilson** shown to be nested in and
  to lift coverage to ≥ nominal (2023–24); the **Andersson–Nerman** interval (2024) [33] proposed as
  a coverage-dominating (but wider) alternative. **Recommended default.**

**Agresti–Coull (adjusted Wald)** `ciac`
- *Definition.* p̃ = (x + z²/2)/(n + z²), ñ = n + z²; then p̃ ± z·√(p̃(1−p̃)/ñ). With z ≈ 1.96 this
  is the famous "add 2 successes and 2 failures."
- *Origin.* Agresti & Coull (1998) [13].
- *Developments / verdict.* A simple, well-behaved compromise between Wald and exact; coverage close
  to Wilson but slightly more conservative. **Recommended for teaching/simplicity.**

**ArcSine (variance-stabilizing)** `cias`
- *Definition.* φ̂ = arcsin(√p̂); interval arcsin(√p̂) ± z/(2√n); **back-transform p = sin²(φ)** (NOT
  sin²(φ/2) — this is the doc bug to fix). Var(φ̂) ≈ 1/(4n).
- *Origin.* Variance-stabilizing lineage: Bartlett (1936) [4], **Anscombe (1948)** [3], Freeman &
  Tukey (1950) [5]. Anscombe's refinement uses (x+3/8)/(n+3/4) with variance 1/(4n+2).
- *Developments / verdict.* Well behaved in the interior; degrades at the boundary. The
  Anscombe/Freeman–Tukey offset variants improve boundary behavior. **Useful, boundary-limited.**

**Logit-Wald** `cilt`
- *Definition.* logit(p̂) = ln(p̂/q̂); SE = 1/√(n·p̂q̂); interval logit(p̂) ± z·SE; back-transform with
  the logistic (expit).
- *Origin.* Wald applied on the log-odds scale (classic transformed-Wald family; see
  Brown–Cai–DasGupta [16] discussion of transformations).
- *Developments / verdict.* Handles extreme p̂ better than raw Wald but is undefined at x = 0, n
  (needs an offset). Complementary-log-log and probit transforms are cousins (packaged in R `binom`,
  absent from `proportion`). **Useful with boundary handling.**

**Wald-T (t-approximation)** `citw`
- *Definition.* p̂ ± t_{ν,1−α/2}·√(p̂q̂/n), with Satterthwaite degrees of freedom ν for the variance
  estimator; boundary modifications at x = 0, n.
- *Origin.* **Pan (2002)** [18] (Satterthwaite/χ² approximation of the variance estimator).
- *Developments since.* **Martín-Andrés & Álvarez-Hernández (2014)** [26] give the two-tailed
  asymptotic version with boundary corrections used in `proportion`. **Niche but principled.**

**Likelihood ratio (LR)** `cilr`
- *Definition.* {θ : 2[x·ln(x/nθ) + (n−x)·ln((n−x)/(n(1−θ)))] ≤ z²}, i.e. invert the
  log-likelihood-ratio statistic.
- *Origin.* Classical LR interval (Wilks' theorem applied to the binomial).
- *Developments since.* **Somerville & Brown (2013)** [24] give the **exact** LR and score intervals
  (coverage-preserving) and recommend the exact LR for regulated settings. **Strong, less well known.**

**Exact — generalized `e` (Mid-P ↔ Clopper–Pearson)** `ciex`
- *Definition.* Invert the equal-tailed binomial test with two-sided p-value
  2[e·Pr(X=x) + min{Pr(X<x), Pr(X>x)}], 0 ≤ e ≤ 1. Clopper–Pearson at **e = 1**; Mid-P at **e = 0.5**.
  Closed forms via Beta quantiles: CP lower = B⁻¹(α/2; x, n−x+1), upper = B⁻¹(1−α/2; x+1, n−x).
- *Origin.* **Clopper & Pearson (1934)** [2]; Mid-P (Lancaster 1961; Berry & Armitage reviews). The
  unifying *e* parameter is a contribution of the `proportion` package [36].
- *Developments since.* CP is exact-but-conservative; Mid-P and **Blaker (2000)** [15] reduce the
  conservatism while (Blaker) retaining guaranteed coverage; Thulin (2014) [27] quantified the
  "cost" of strict exactness. **CP for regulated/guaranteed coverage; Mid-P or Blaker to reduce waste.**

**Bayesian — conjugate Beta(a, b), equal-tailed + HPD** `ciba`
- *Definition.* Posterior θ | x ~ Beta(x+a, n−x+b). **Equal-tailed:** quantiles α/2 and 1−α/2. **HPD:**
  the shortest interval carrying posterior mass 1−α.
- *Priors.* Bayes–Laplace uniform a=b=1 (Laplace 1812); **Jeffreys** a=b=½ (Jeffreys 1946 [6]);
  **Haldane** a=b=0 (Haldane 1948 [7]).
- *Developments since.* Brown–Cai–DasGupta [16] show the Jeffreys equal-tailed interval has excellent
  frequentist coverage and recommend it generally; **Tuyl, Gerlach & Mengersen (2008)** [20] analyze
  the delicate **zero-events** case and prior choice. HPD is harder to compute and slightly worse on
  coverage than equal-tailed Jeffreys. **Jeffreys equal-tailed recommended; HPD when a shortest
  credible interval is wanted.**

### 6.2 Generalization operators (apply across methods)

| Operator | What it does | Notes / literature |
|---|---|---|
| **Continuity correction *c*** | Adds ±c to the standardized statistic before inverting | Yates-type; for **CC-Wilson**, recent work (2023–24) proves nesting and coverage ≥ nominal; Pires & Amado [21] note CC-score breaks near n/2 |
| **Adjustment factor *h*** | Add *h* to *x*, adjust *n*, then apply any base method | The `proportion` unification [36]; Agresti–Coull is the special case h = z²/2 on Wald |
| **Exact parameter *e*** | Continuum from Mid-P (e=0.5) to Clopper–Pearson (e=1) | `proportion` allows arbitrary e ∈ [0,1] |

### 6.3 Evaluation criteria (the differentiator)

| Criterion | Definition | Origin / key reference |
|---|---|---|
| **Coverage probability (CP)** | C(θ) = Σₓ Pr(X=x\|θ)·1[θ ∈ CI(x)]; summarized by mean/min CP and RMSE-from-nominal | Standard; Brown–Cai–DasGupta [16] |
| **Expected length (EL)** | E[U−L\|θ] = Σₓ Pr(X=x\|θ)(U(x)−L(x)); mean/SD/max | Standard |
| **p-confidence / p-bias** | Interval = non-rejected θ in a test; directional error measures | **Vos & Hudson (2005)** [19] |
| **Error / long-term power** | Δ between nominal α and actual error; % of x causing error; pass/fail | **Martín-Andrés & Álvarez (2014)** [26] |
| **Aberrations (LABB/UABB)** | Lower/upper bound anomalies (non-monotonic behavior) | Newcombe (2011) [23] |
| **Zero-width intervals (ZWI)** | Flag degenerate zero-length CI at x = 0, n | Newcombe [14, 23] |
| **MC θ-space evaluation** | Replace fixed θ-grid with draws θ ~ Beta(a,b) (uniform = a=b=1) | `proportion` [36] |
| **NEW: "locally correct" criterion** | Formalizes that some "recommended" intervals aren't true CIs (coverage dips below nominal); proposes a new validity criterion | **Garthwaite et al. (2024)** [32] |
| **NEW: rare-event relative MoE** | Margin of error defined *relative to θ's magnitude* for rare events | McGrath & Burke (2024) [34] |

### 6.4 Bayesian tool box (beyond credible intervals)

- **Priors as presets.** Bayes–Laplace, Jeffreys [6], Haldane [7]; probability-matching priors;
  robust/mixture priors.
- **Bayes factors.** Ratio of marginal likelihoods under the Beta-Binomial model; the package
  supports directional/range hypotheses θ<θ₁ vs θ≥θ₂. Foundational: **Kass & Raftery (1995)** [12]
  (note: BF sensitivity to the prior persists even in large samples).
- **Empirical Bayes (EB).** Estimate prior (a,b) from the data via the **beta-binomial marginal**
  (MLE / method-of-moments / EM). Foundational: **Robbins (1956)** [35].
- **Posterior predictive.** X_new(m,θ) follows the Beta-Binomial predictive; in Python this is
  `scipy.stats.betabinom` — a direct match.
- **Posterior probabilities.** Direct evaluation of the Beta posterior CDF/PDF.

---

## 7. New developments since 2017 & the candidate-method menu

The 2017 paper predates a genuinely active decade. Two kinds of things happened: **new interval
methods**, and — directly relevant to this package's evaluation focus — **new evaluation criteria**.

### 7.1 What's new since the original paper (verified 2026-07)
| Development | Year / venue | One-line idea | Type |
|---|---|---|---|
| **Betting / hedged-capital intervals** (Waudby-Smith & Ramdas) | 2024, *JRSS-B* (with discussion) [31] | Game-theoretic / martingale CIs for bounded means; numerically the tightest known; Bernoulli is the canonical case | **New paradigm** (method) |
| **Confidence sequences / anytime-valid** (Howard et al.; WSR) | 2021 *Ann. Statist.* [29] → 2024 | Time-uniform intervals valid at *every* n at once (streaming / optional stopping) | New paradigm (method) |
| **Closed-form empirical-Bernstein CS** | 2025, arXiv | Closed-form (no per-step optimization) betting-style confidence sequence | Method (fast variant) |
| **"Locally correct" criterion + method** (Garthwaite et al.) | 2024, *Scand. J. Statist.* [32] | Shows several "recommended" intervals aren't true CIs; proposes new criterion + interval | **New criterion** + method |
| **Andersson–Nerman interval** | 2024, *Stat* [33] | Wilson competitor; coverage ≥ Wilson everywhere, at the cost of larger expected length | Method |
| **Shrinkage-estimator intervals** (Almendra-Arao et al.) | 2022–23, *Open Math.* [30] | CIs built on a shrinkage point estimator | Method family |
| **Rare-event relative margin-of-error** (McGrath & Burke) | 2024, *Amer. Statist.* [34] | Reframes margin of error relative to θ's magnitude | Interpretation / criterion |

**Headline:** the **betting / confidence-sequence** family [31] is the real breakthrough since 2017 —
a different mathematical foundation (test-by-betting martingales) from every method in `proportion`
(which all invert a test or use a prior). Adding it would make binomcikit the first tool to put the
**classical + exact + Bayesian + betting/anytime-valid** families under one evaluation roof.

### 7.2 Candidate methods to add (categorized menu)
Every item is **absent from all Python packages *and* from R `proportion`** (unless noted) — i.e. each
is a fresh row of ❌'s in Tables 3.1 / 3.2.

**A. Classical / exact intervals the original omitted**
- **Blaker (2000)** [15] — nested exact interval, always ⊆ Clopper–Pearson (shorter, still ≥ nominal);
  computation improved by **Klaschka (2010)** [22] (R `BlakerCI`).
- **Blyth–Still–Casella** [10,11] — shortest exact (non-nested).
- **Sterne / minlike** [8] — likelihood-ordering exact interval.
- **Pratt (1968)** [9] — closed-form approximation to the exact interval.
- **Complementary-log-log & probit** transformed Walds (in R `binom`, not `proportion`).
- **Second-order / Cornish–Fisher** corrected normal intervals.

**B. Bootstrap family** (the 2017 paper's own stated future work)
- Nonparametric percentile, parametric, **smooth bootstrap** (Wang & Hutson 2013 [25]), BCa — each
  drops straight into the existing "score any limits" evaluation harness.

**C. Post-2017 paradigms**
- **Betting / hedged-capital** fixed-n interval [31]; **predictable-plug-in empirical-Bernstein**
  confidence *sequence* (anytime-valid) [29]; **Andersson–Nerman** [33]; **shrinkage-based** [30].

**D. New evaluation criteria** (these extend Table 3.2, not 3.1)
- **"Locally correct" coverage criterion** [32]; **rare-event relative margin-of-error** [34].

**E. Bayesian extensions**
- Named priors as presets: **Haldane** Beta(0,0), **Bayes–Laplace** Beta(1,1), **Jeffreys** Beta(½,½);
  **probability-matching** priors; **robust / mixture** priors. **Numerical HPD for arbitrary user
  priors**; **Bayesian bootstrap**.

**F. Adjacent scope — flag before committing (this widens the package)**
- **Difference / ratio of two proportions** — the 2017 paper names this as its own next direction; it
  has a large literature and R packages of its own, so treat as a *sequel*. **Sample-size / power**
  determination (cf. `binomSamSize`).

### 7.3 Recommended priority (novelty ÷ effort)
1. **Blaker** — small, self-contained, well-specified; closes a gap even vs. R.
2. **Bootstrap (smooth)** — the authors' own stated extension; near-free given the harness.
3. **Betting / confidence-sequence** — the genuine post-2017 breakthrough and the strongest single
   claim for a "port + contribution" paper; pairs naturally with the evaluation suite.
4. **"Locally correct" criterion** — cheap to add as one more diagnostic; keeps the evaluation suite
   current with 2024 theory.

*(Paper scope / which methods to commit to: intentionally left open.)*

---

## 8. Deep dive: betting / confidence-sequence intervals [31, 29]

Formulas transcribed **directly from the source** (WSR, arXiv:2010.09686v7, 25 Aug 2022; §§2–4) and
cross-checked page-by-page.

### 8.1 Why this is the headline candidate
- **Different mathematics from everything in `proportion`.** Every method in the R package inverts a
  test or uses a prior. This one is a **game-theoretic / nonnegative-martingale** construction ("testing
  by betting"): bet against each candidate mean *m*; if you get rich, exclude *m*. It generalizes and
  strictly improves the Chernoff/Hoeffding method (WSR §2.3).
- **Numerically the tightest known** CIs for bounded means, and **variance-adaptive** — for θ near 0 or 1
  (low variance) the interval is much shorter than Hoeffding/Wald. Bernoulli is the canonical [0,1]-bounded
  case, so it applies to us directly.
- **It unlocks a capability no binomial-CI package has:** an **anytime-valid confidence sequence** — valid
  simultaneously at every *n* (streaming data, optional stopping).
- **It pairs perfectly with binomcikit's evaluation suite:** because the betting method just produces
  limits (L, U), you can *demonstrate* it dominating Wald/Wilson/exact on coverage and expected length
  using your own §6.3 metrics. That figure is the paper.

### 8.2 The construction (verified formulas)
**Setup.** X₁, X₂, … ∈ [0,1] with conditional mean μ (for Bernoulli, Xᵢ ∈ {0,1}, μ = θ). Goal: a (1−α)
confidence set for μ.

**The 4-step recipe (Theorem 1).** For each candidate mean *m* ∈ [0,1] build a nonnegative process Mₜᵐ
that is a **test (super)martingale** under H₀ᵐ: "true mean = m". Reject *m* when Mₜᵐ ≥ 1/α. The confidence
set is everything not rejected:
```
C_t = { m ∈ [0,1] : M_t^m < 1/α }.
```
Validity is **Ville's inequality**: for a nonnegative (super)martingale with M₀ = 1,
P(∃t : Mₜ ≥ 1/α) ≤ α. A fixed-*n* CI is C_n; a confidence *sequence* is (C_t)_{t≥1}.

**The capital (betting) process (Eq. 23).** For candidate *m*,
```
𝒦_t(m) = ∏_{i=1}^{t} ( 1 + λ_i(m)·(X_i − m) ),    𝒦_0(m) = 1,
```
where the betting fractions λ_i(m) are **predictable** (depend only on X₁…X_{i−1}) and take values in
(−1/(1−m), 1/m) so every factor stays ≥ 0. Under μ = m this is a test martingale (Proposition 2), and —
remarkably — **every** test martingale for the class has this form (Proposition 3, universal representation).

**The hedged capital process (Eq. 24, the recommended method).** Run one bet that μ ≥ m and one that μ < m,
and take the max:
```
𝒦_t^±(m) = max{ θ·𝒦_t^+(m),  (1−θ)·𝒦_t^-(m) },     θ ∈ [0,1] (default ½)
𝒦_t^+(m) = ∏_{i≤t} ( 1 + λ_i^+(m)·(X_i − m) )      # bets μ ≥ m
𝒦_t^-(m) = ∏_{i≤t} ( 1 − λ_i^-(m)·(X_i − m) )      # bets μ < m
```
It is upper-bounded by the martingale ℳ_t^± = θ𝒦_t^+ + (1−θ)𝒦_t^- (which gives a slightly **tighter** CS,
Remark 2).

**Confidence set (Theorem 3, "Hedged").** With real predictable λ̃_t^+, λ̃_t^- (not depending on m), set
the *m*-dependent, truncated fractions
```
λ_t^+(m) = |λ̃_t^+| ∧ c/m,     λ_t^-(m) = |λ̃_t^-| ∧ c/(1−m),     c ∈ [0,1) (default ½ or ¾).
```
Then 𝔅_t^± = { m : 𝒦_t^±(m) < 1/α } is a (1−α)-CS for μ, **and is guaranteed to be an interval** for each t.
Its running intersection ⋂_{i≤t} 𝔅_i^± is also valid.

**The recommended predictable plug-in (Eq. 26).** Running, regularized mean & variance (note the ½ and ¼
"priors" that keep things defined at the boundary):
```
μ̂_t   = ( ½ + Σ_{i≤t} X_i ) / ( t + 1 )
σ̂²_t  = ( ¼ + Σ_{i≤t} (X_i − μ̂_i)² ) / ( t + 1 )
λ̃_t^± = sqrt( 2·log(2/α) / ( σ̂²_{t−1} · t · log(t+1) ) )  ∧  c          # confidence SEQUENCE
```
**Fixed-sample-size CI (Remark 3, "Hedged-CI"):** use ⋂_{i≤n} 𝔅_i^± with
```
λ̃_t^± = sqrt( 2·log(2/α) / ( n · σ̂²_{t−1} ) )                          # fixed-n CI
```

**A closed-form cousin — PrPl-EB (Theorem 2 / Remark 1).** If you want a *closed-form* (no grid/root-finding)
interval, the predictable-plug-in empirical-Bernstein CI is
```
C_t^{PrPl-EB} = ( Σλ_iX_i / Σλ_i )  ±  ( log(2/α) + Σ v_i·ψ_E(λ_i) ) / Σλ_i,
   v_i = 4(X_i − μ̂_{i−1})²,   ψ_E(λ) = (−log(1−λ) − λ)/4,   λ_t = λ̃_t as above.
```
WSR report it is **~500× faster** than the conjugate-mixture empirical-Bernstein CS (which needs
root-finding), at nearly identical width. The betting (Hedged) CI is a bit tighter; the PrPl-EB CI is a bit
faster. **Offer both.**

### 8.3 The one subtlety that matters for us: sequence-dependence
Wald/Wilson/exact/Bayes are functions of the **sufficient statistic (x, n)** only. The betting interval is a
function of the **ordered sequence** X₁…X_n, because λ_t depends on the running μ̂_{t−1}. For a fixed (x, n),
different orderings of the x ones and (n−x) zeros give (slightly) different intervals. Three ways to produce a
single deterministic interval per x — needed to slot into binomcikit's "limits for each x ∈ {0,…,n}" table:

1. **Derandomize (WSR's own remedy).** Average the capital process over B random permutations of the 0/1
   sequence: M̃_n(m) = (1/B)Σ_b 𝒦_{n,b}^±(m); by Markov's inequality { m : M̃_n(m) < 1/α } is a valid (1−α)
   CI. *Principled but not closed-form, and uses Markov not Ville.* Recommended default for the (x, n) summary.
2. **Canonical ordering.** Fix one representative order. Deterministic and fast; validity still holds for that
   realized sequence, but the choice of order is a modeling decision to document.
3. **Streaming API.** Expose the genuine confidence *sequence* on a user-supplied 0/1 stream — the anytime-valid
   use case; does not reduce to (x, n).

**Design decision for binomcikit:** implement (1) as the summary limit-producer `cibet(n, α)` (→ L[x], U[x]
for x = 0…n, feeds the whole evaluation engine), and (3) as a separate `cibetseq(stream, α)` for the
streaming/anytime-valid capability. (2) is an optional fast mode.

### 8.4 How it maps onto binomcikit's architecture
The betting CI fits as a new **limit-producer**, after which coverage, expected length, p-confidence/p-bias,
error, plots, and the Bayesian comparison all work *unchanged*.
```
cibet(n, alpha, grid_g=1000, c=3/4, B=50):
    for x in 0..n:
        # derandomized capital over B permutations of x ones and (n-x) zeros
        define K_pm(m):  average over b of  hedged_capital(seq_b, m, alpha, c)   # Eq. 24–26
        # 𝔅 is an interval ⇒ find its two edges by bisection on the grid (0,1)
        L[x] = smallest m with K_pm(m) < 1/alpha
        U[x] = largest  m with K_pm(m) < 1/alpha
    return table(x, L, U)          # identical shape to ciwd/cisc/ciex → drop into covp/expl/...
```
- **No new engine code.** `covp*`, `length*`, `pcopbi*`, `err*`, and every `plot*` consume the (L, U) table
  already. So the betting method automatically gets the full diagnostic suite — how you produce the "betting
  dominates on CP/EL" figure.
- **Cost.** Per x: B permutations × grid/bisection over m × O(n) product. Vectorizable in numpy over the grid;
  Numba helps the inner product loop.

### 8.5 Implementation options
| Option | What | Trade-off |
|---|---|---|
| **Reuse `confseq`** | WSR ship a reference Python package, `confseq` (github.com/gostevehoward/confseq), whose `betting` module implements these exact algorithms (C++ core + Python bindings) | Fastest to correct results; adds a compiled dependency; check its license before vendoring/depending |
| **Reimplement in numpy** | Port Eqs. 23–26 directly (a product, a grid/bisection, a permutation average) | Pure-Python, no new build dep, matches binomcikit's stack; validate against `confseq` as oracle |

**Recommendation:** reimplement in numpy for the core (keeps the dependency footprint clean and gives a golden
oracle in `confseq` for tests), gated behind a `[betting]`/`[fast]` extra if Numba is used.

### 8.6 What it adds to the paper and the coverage tables
- **New rows in Table 3.1** (all ❌ across every existing Python package *and* R `proportion`): *Betting /
  hedged-capital CI*, *PrPl-EB CI*, and *anytime-valid confidence sequence*.
- **Turns "port" into "port + 2024 contribution":** binomcikit becomes the **first package to put classical +
  exact + Bayesian + betting/anytime-valid methods under one evaluation roof**, and — using its own metric
  suite — the first to *systematically benchmark* betting intervals against the classical zoo on
  CP/EL/p-confidence.
- **Honest scoping:** the betting CI needs the sequence (or derandomization), unlike the (x, n)-only classical
  methods; state this plainly. The confidence-sequence variant is a genuinely new *capability* (optional
  stopping), not just a tighter interval.

---

## 9. Deep dive: Blaker, bootstrap & the rest

**Architecture test for any candidate:** *(a)* is the interval a function of (x, n) only (→ drops straight
into the x-table)? *(b)* closed-form, root-finding, or simulation? *(c)* monotone/nested (→ a clean,
well-ordered table)?

### 9.1 Blaker's exact acceptability interval [15]  ★ top pick
**Idea.** Reduce the wastefulness of Clopper–Pearson while *keeping* guaranteed coverage, by inverting a
smarter (two-sided, "acceptability") exact test.

**Construction.** For the binomial CDF F(k; θ) = P_θ(X ≤ k), define the smaller-tail function
```
g(x, θ) = min{ F(x; θ),  1 − F(x−1; θ) }      # min of lower tail P(X≤x) and upper tail P(X≥x)
```
and the **acceptability function**
```
γ(x, θ) = P_θ( g(X, θ) ≤ g(x, θ) ).
```
(Equivalently: take the smaller tail at x and add the *largest opposite tail not exceeding it*.) The 1−α
**Blaker interval** is the set of θ for which x is acceptable: `{ θ ∈ [0,1] : γ(x, θ) ≥ α }`, reported as
[θ_L, θ_U]. θ_L, θ_U solve γ(x, θ) = α. Because γ(·, θ) can be **non-unimodal** in θ, the exact limits need
careful root-finding; Klaschka's `BlakerCI` [22] "unimodalizes" the acceptability function to do this
correctly, and Lecoutre & Poitevineau (2014) gave further computational results.

**Properties.** Provably **nested** and **⊆ Clopper–Pearson** (never longer), coverage ≥ 1−α, and empirically
shorter than Wald/Wilson/Agresti–Coull. Known caveat (Klaschka & Reitmeir 2014, *Comput. Stat.*): a mild
test-vs-CI inconsistency from non-unimodality.

**Architecture fit.** ✅ Function of **(x, n)** only; ✅ **nested/monotone** → a clean x-table; root-finding on
γ(x,θ)=α (one solve per side per x). Drops straight into the engine as `ciblaker(n, α)` and immediately gets
the full diagnostic suite. **Oracle:** R `BlakerCI::binom.blaker.limits` or `PropCIs::blakerci`. **Effort:**
small–moderate. **Payoff:** closes a gap even vs. R `proportion`.

### 9.2 Bootstrap family — Wang–Hutson smooth bootstrap [25]  ★ authors' own future work
**Why the naïve bootstrap fails here.** Ordinary nonparametric bootstrap resamples the 0/1 data, so the
resampled proportion only takes values k/n — the bootstrap distribution stays **discrete and degenerate**,
giving poor percentile CIs (worst near θ ≈ 0, 1 and small n).

**Wang–Hutson fix (smooth quantile via fractional order statistics).** Replace the discrete data's quantile
function with a smooth one built from a Beta CDF:
```
Q_X(u | π) = 1 − B_{3u, 3(1−u)}(1 − π),     u ∈ (0,1),
```
where B_{a,b}(·) is the Beta(a, b) CDF. The sample version plugs in an estimator π̂ (they use the
**median-unbiased estimator**): Q̂_X(u) = 1 − B_{3u,3(1−u)}(1 − π̂).

**Algorithm (produces the CI).**
```
1. π̂ ← median-unbiased estimate from (x, n)
2. for b = 1..B:
     U* ← n iid Uniform(0,1)
     X* ← Q̂_X(U* | π̂)                      # smooth resample
     invert mean(X*) → π̂*_b  (via a cubic B-spline of the mean–π relation)
3. CI = ( percentile_{α/2}(π̂*),  percentile_{1−α/2}(π̂*) )
```
**Other bootstrap variants worth exposing.** Parametric bootstrap (resample Binomial(n, p̂)); percentile /
BCa (bias-corrected accelerated). All compatible.

**Architecture fit.** ✅ Function of **(x, n)** (via π̂); **simulation-based** (like the existing
`covpsim`/`lengthsim` paths), so it needs a `seed=` for reproducibility and a `B=` control; produces (L, U)
per x and feeds the engine normally as `ciboot(n, α, B, seed, kind="smooth")`. **Effort:** moderate.
**Payoff:** the 2017 authors explicitly named bootstrap as future work.

### 9.3 Other exact / near-exact intervals
| Method | Idea | Origin | Architecture fit | Effort |
|---|---|---|---|---|
| **Blyth–Still–Casella** | The **shortest** exact interval, chosen by a length-minimizing construction (not by inverting an equal-tailed test) | [10,11] | (x,n) only, but **NON-nested** → not a clean monotone table; combinatorial search | **High** |
| **Sterne / minlike** | Invert the test whose acceptance region is the *most probable* outcomes (probability ordering) summing to ≥ 1−α | [8] | (x,n) only; nested with care; root-finding | Moderate |
| **Pratt** | **Closed-form** normal approximation to the Clopper–Pearson (F-distribution) limits — accurate, no root-finding | [9] | (x,n) only; **closed-form** → trivial & fast | **Small** |

### 9.4 Other approximate / transformed intervals
| Method | Idea | Origin | Fit / effort |
|---|---|---|---|
| **Andersson–Nerman** | A Wilson-type interval whose coverage is **≥ Wilson everywhere** (at the cost of larger length) | [33] | (x,n), ~closed-form; **small** (need the exact pivot formula from the paper) |
| **Complementary-log-log & probit** | Wald on g(p)=log(−log(1−p)) or Φ⁻¹(p), back-transformed (cousins of Logit-Wald) | transformed-Wald family | (x,n), **closed-form**; **small** |
| **Second-order / Cornish–Fisher** | Edgeworth/Cornish–Fisher correction to the z-quantile to fix coverage to second order | classical asymptotics | (x,n), closed-form; small–moderate |
| **Coverage-adjusted** | Post-adjust an interval so its **minimum** coverage meets nominal (removes conservatism) | Thulin [27] | wraps any base method; moderate |
| **Iterative optimal** | Iteratively construct the shortest interval with guaranteed coverage (admissible; refines Blyth–Still–Casella) | Wang [28] | (x,n), iterative optimization; **high** |

### 9.5 Shrinkage-based intervals [30]
Build the interval around a **shrinkage** point estimator (π̂ pulled toward ½). (x, n) only; roughly
closed-form; **small–moderate** effort. Least mature of the candidates — verify [30]'s details before relying.

### 9.6 A new *evaluation criterion*, not a method: "locally correct" [32]
Garthwaite, Moustafa & Elfadaly (2024) show several "recommended" intervals **fail the definition of a
confidence interval** because coverage dips below nominal for some θ. They propose a **"locally correct"**
criterion and a method that is **shortest among all methods meeting it** (mid-p also satisfies it). For
binomcikit this is two things: (i) a **new Table 3.2 diagnostic** — flag, for any interval, the θ-regions
where it violates local correctness; and (ii) an optional **limit-producer** (their method). Adding (i) keeps
the evaluation suite current with 2024 theory at low cost.

### 9.7 Summary: architecture fit & priority
| Candidate | (x,n) only? | Form | Nested? | Effort | Novelty payoff |
|---|:--:|---|:--:|:--:|---|
| **Betting / conf-sequence** (§8) | ✗ (sequence) | grid/bisection | — | Med | ★★★ (2024 paradigm; anytime-valid) |
| **Blaker** | ✓ | root-find | ✓ | S–M | ★★ (gap even vs R) |
| **Bootstrap (smooth)** | ✓ | simulation | ✓ | Med | ★★ (authors' stated future work) |
| **Pratt** | ✓ | closed-form | ✓ | S | ★ (fast, clean) |
| **cloglog / probit** | ✓ | closed-form | ✓ | S | ★ (rounds out transforms) |
| **Andersson–Nerman** | ✓ | ~closed-form | ✓ | S | ★★ (2024, coverage-dominates Wilson) |
| **"Locally correct" criterion** | n/a | diagnostic | n/a | S | ★★ (new 2024 criterion for the suite) |
| **Sterne / minlike** | ✓ | root-find | ✓ | Med | ★ |
| **Coverage-adjusted** | ✓ | wrapper | ✓ | Med | ★ |
| **Second-order / Cornish–Fisher** | ✓ | closed-form | ✓ | S–M | ★ |
| **Shrinkage** | ✓ | ~closed-form | ✓ | S–M | ★ (immature) |
| **Blyth–Still–Casella** | ✓ | search | ✗ | High | ★ (shortest exact, but non-nested) |
| **Iterative optimal (Wang)** | ✓ | iterative | ✓ | High | ★ |

**Reading of the table.** The **easy, high-value cluster** is Blaker + Pratt + cloglog/probit +
Andersson–Nerman + the "locally correct" criterion — all (x, n)-only, mostly closed-form or a single
root-solve, and each a fresh ❌-row across the Python ecosystem. **Bootstrap** is a moderate, headline-friendly
add (the authors' own future work). **Betting** remains the single strongest "port + 2024 contribution" claim.
Blyth–Still–Casella and Wang's iterative method are **high-effort / lower-marginal-payoff** and can wait.

**Suggested build order for a method contribution:** Blaker → smooth bootstrap → betting/CS → the closed-form
quick wins (Pratt, cloglog/probit, Andersson–Nerman) → the "locally correct" criterion. Every one inherits the
full CP/EL/p-confidence/error/plot suite for free — so each also becomes a new *benchmark*, not just a function.

---

## 10. Timeline (1927 → 2025)

| Year | Method / criterion | Ref |
|---|---|---|
| 1927 | Wilson score | [1] |
| 1934 | Clopper–Pearson exact | [2] |
| 1946/48 | Jeffreys / Haldane priors; Anscombe arcsine | [6][7][3] |
| 1954 | Sterne minlike | [8] |
| 1968 | Pratt approximation | [9] |
| 1983/86 | Blyth–Still / Casella shortest exact | [10][11] |
| 1995 | Kass–Raftery Bayes factors | [12] |
| 1998 | Agresti–Coull; Newcombe 7-method comparison | [13][14] |
| 2000 | Blaker exact | [15] |
| 2001/02 | Brown–Cai–DasGupta (interval + expansions); Pan Wald-t | [16][17][18] |
| 2005 | Vos–Hudson p-confidence/p-bias | [19] |
| 2008 | Tuyl et al. zero events; Pires–Amado 20-method | [20][21] |
| 2013 | Somerville–Brown exact LR/score; Wang–Hutson smooth bootstrap | [24][25] |
| 2014 | Martín-Andrés error criterion; Thulin coverage-adjusted; Wang iterative | [26][27][28] |
| **2017** | **Subbiah–Rajeswaran `proportion` (the package we port)** | [36] |
| 2021 | Howard et al. confidence sequences | [29] |
| 2022/23 | Shrinkage-based intervals | [30] |
| 2024 | **Betting/hedged-capital (WSR)**; Garthwaite locally-correct; Andersson–Nerman; rare-events | [31][32][33][34] |

**Everything from 2018 onward postdates the R package** — which is precisely why "revive in Python **and**
extend with post-2017 methods/criteria" is a live research contribution, not a restoration.

---

## 11. References

[1] Wilson, E. B. (1927). Probable inference, the law of succession, and statistical inference. *JASA* 22(158), 209–212.
[2] Clopper, C. J. & Pearson, E. S. (1934). The use of confidence or fiducial limits illustrated in the case of the binomial. *Biometrika* 26(4), 404–413.
[3] Anscombe, F. J. (1948). The transformation of Poisson, binomial and negative-binomial data. *Biometrika* 35(3/4), 246–254.
[4] Bartlett, M. S. (1936). The square root transformation in analysis of variance. *JRSS Suppl.* 3(1), 68–78.
[5] Freeman, M. F. & Tukey, J. W. (1950). Transformations related to the angular and the square root. *Ann. Math. Statist.* 21(4), 607–611.
[6] Jeffreys, H. (1946). An invariant form for the prior probability in estimation problems. *Proc. R. Soc. Lond. A* 186(1007), 453–461.
[7] Haldane, J. B. S. (1948). The precision of observed values of small frequencies. *Biometrika* 35(3/4), 297–300.
[8] Sterne, T. E. (1954). Some remarks on confidence or fiducial limits. *Biometrika* 41(1/2), 275–278.
[9] Pratt, J. W. (1968). A normal approximation for binomial, F, beta, and other common, related tail probabilities. *JASA* 63(324), 1457–1483.
[10] Blyth, C. R. & Still, H. A. (1983). Binomial confidence intervals. *JASA* 78(381), 108–116.
[11] Casella, G. (1986). Refining binomial confidence intervals. *Canadian Journal of Statistics* 14(2), 113–129.
[12] Kass, R. E. & Raftery, A. E. (1995). Bayes factors. *JASA* 90(430), 773–795.
[13] Agresti, A. & Coull, B. A. (1998). Approximate is better than "exact" for interval estimation of binomial proportions. *The American Statistician* 52(2), 119–126. doi:10.1080/00031305.1998.10480550.
[14] Newcombe, R. G. (1998). Two-sided confidence intervals for the single proportion: comparison of seven methods. *Statistics in Medicine* 17(8), 857–872.
[15] Blaker, H. (2000). Confidence curves and improved exact confidence intervals for discrete distributions. *Canadian Journal of Statistics* 28(4), 783–798 (corrigendum 29, 681).
[16] Brown, L. D., Cai, T. T. & DasGupta, A. (2001). Interval estimation for a binomial proportion. *Statistical Science* 16(2), 101–133.
[17] Brown, L. D., Cai, T. T. & DasGupta, A. (2002). Confidence intervals for a binomial proportion and asymptotic expansions. *Annals of Statistics* 30(1), 160–201.
[18] Pan, W. (2002). Approximate confidence intervals for one proportion and difference of two proportions. *Computational Statistics & Data Analysis* 40(1), 143–157.
[19] Vos, P. W. & Hudson, S. (2005). Evaluation criteria for discrete confidence intervals: beyond coverage and length. *The American Statistician* 59(2), 137–142.
[20] Tuyl, F., Gerlach, R. & Mengersen, K. (2008). A comparison of Bayes–Laplace, Jeffreys, and other priors: the case of zero events. *The American Statistician* 62(1), 40–44.
[21] Pires, A. M. & Amado, C. (2008). Interval estimators for a binomial proportion: comparison of twenty methods. *REVSTAT* 6(2), 165–197.
[22] Klaschka, J. (2010). *BlakerCI: Blaker's binomial and Poisson confidence limits* (R package; computational improvements to Blaker's algorithm).
[23] Newcombe, R. G. (2011). Measures of location for confidence intervals for proportions. *Communications in Statistics – Theory and Methods* 40(10), 1743–1767. (See also Newcombe & Nurminen 2011.)
[24] Somerville, M. C. & Brown, R. S. (2013). Exact likelihood ratio and score confidence intervals for the binomial proportion. *Pharmaceutical Statistics* 12(2), 120–128. doi:10.1002/pst.1560.
[25] Wang, D. & Hutson, A. D. (2013). Smooth bootstrap-based confidence intervals for one binomial proportion and difference of two proportions. *Journal of Applied Statistics* 40(3), 614–625. doi:10.1080/02664763.2012.750283.
[26] Martín-Andrés, A. & Álvarez-Hernández, M. (2014). Two-tailed asymptotic inferences for a proportion. *Journal of Applied Statistics* 41(7), 1516–1529 (erratum: *Statistics and Computing* 26(3), 743–744, 2016).
[27] Thulin, M. (2014). The cost of using exact confidence intervals for a binomial proportion. *Electronic Journal of Statistics* 8(1), 817–840. (See also Thulin, M. (2014), Coverage-adjusted confidence intervals, *Scandinavian Journal of Statistics* 41(2), 291–300.)
[28] Wang, W. (2014). An iterative construction of confidence intervals for a proportion. *Statistica Sinica* 24(3), 1389–1410.
[29] Howard, S. R., Ramdas, A., McAuliffe, J. & Sekhon, J. (2021). Time-uniform, nonparametric, nonasymptotic confidence sequences. *Annals of Statistics* 49(2), 1055–1080. (arXiv:1810.08240.)
[30] Almendra-Arao, F., Reyes-Cervantes, H. J. et al. (2022/23). A comparison of some confidence intervals for a binomial proportion based on a shrinkage estimator. *Open Mathematics*. doi:10.1515/math-2022-0588.
[31] Waudby-Smith, I. & Ramdas, A. (2024). Estimating means of bounded random variables by betting. *Journal of the Royal Statistical Society Series B* 86(1), 1–27 (with discussion). doi:10.1093/jrsssb/qkad009. (arXiv:2010.09686.)
[32] Garthwaite, P. H., Moustafa, M. W. & Elfadaly, F. G. (2024). Locally correct confidence intervals for a binomial proportion: a new criterion for an interval estimator. *Scandinavian Journal of Statistics* (arXiv:2106.15521). doi:10.1111/sjos.12672.
[33] Andersson, P. G. (2024). A note on confidence intervals for a binomial p: Andersson–Nerman vs. Wilson. *Stat* 13(1), e70027.
[34] McGrath, O. & Burke, K. (2024). Binomial confidence intervals for rare events: importance of defining margin of error relative to magnitude of proportion. *The American Statistician* (arXiv:2109.02516). doi:10.1080/00031305.2024.2350445.
[35] Robbins, H. (1956). An empirical Bayes approach to statistics. *Proc. 3rd Berkeley Symposium* 1, 157–163.
[36] Subbiah, M. & Rajeswaran, V. (2017). proportion: A comprehensive R package for inference on single binomial proportion and Bayesian computations. *SoftwareX* 6, 36–41. doi:10.1016/j.softx.2017.01.001.

> **Verification note.** Origin papers [1–19] and the 2017 package [36] are well-established and
> cross-checked. Recent items [29–34] were verified against publisher/preprint pages in the 2026-07 web
> scan; [31] (WSR) was read directly (arXiv:2010.09686v7 → JRSS-B 2024); [32] (Garthwaite, Moustafa &
> Elfadaly) and [34] (McGrath & Burke) confirmed from the arXiv source. Only [30] (Almendra-Arao et al.,
> shrinkage) still has an unconfirmed full author list / page range — double-check that DOI at citation time.
