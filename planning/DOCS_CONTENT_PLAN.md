# Docs content-depth initiative — the current goal (set 2026-07-25)

The docs *structure* is settled (Furo, five collapsible groups). The **content** is thin in specific
places. This is now the active goal: deepen the explanations until the docs teach, not just list.

Measured thinness (line counts): `theory/` = 1 page; `foundations/index` = 71; `method_selection` = 36;
metric explanations = a paragraph each. Method pages are OK (~150 lines) but promise a "deeper maths"
track that barely exists.

## Progress
- ✅ **T5 infra — executable docs (MyST-NB) set up** (2026-07-25). Pages with a `jupytext`+`kernelspec`
  front-matter header run their ```{code-cell}``` blocks at build; `nb_execution_raise_on_error=True`
  fails the build on a broken example. `binomcikit` installed editable locally + via `.readthedocs.yaml`
  so the kernel/RTD can import it. Also done: edit-button removed, sidebar headers collapsible.
- ✅ **T1 page** `theory/02_normal_approximation.md` — the normal approximation & why Wald fails, with
  four *executed* examples (Wald's `[0,0]` collapse, its sub-nominal coverage, the delta-method dropdown).
- ✅ **T1 page** `theory/03_test_inversion.md` (2026-07-25) — score (Wilson) + likelihood-ratio intervals
  as *inverting a hypothesis test*; executed Wald-vs-Wilson-vs-LR comparison, hand-checked Wilson centre,
  LR deviance sitting on the χ²₁ cutoff, and the z² = χ²₁(0.95) identity. Figure `test_inversion_coverage.png`.
- ✅ **T2 Foundations series DONE** (2026-07-25) — `foundations/index` rewritten as a landing/hub over five
  new *executable* beginner pages: `01_proportion`, `02_binomial` (hand-worked pmf), `03_sampling_variability`
  (SE + simulation), `04_confidence_interval` (repeated-sampling sim + caterpillar figure), `05_coverage`
  (exact binomial-sum coverage). Four matplotlib figures in the dataviz palette.
- ✅ **T1 page** `theory/04_exact_and_discreteness.md` (2026-07-25) — why coverage is a jagged step
  function (discreteness), Clopper–Pearson (invert the exact test, conservative), Mid-P (shave the atom,
  loses the guarantee), and Blaker's **acceptability function** γ(x,θ) *reproduced from scratch* (its
  endpoints sit on γ=α) with the Blaker⊂CP nesting check and a guarantee-vs-width table. Figure
  `exact_discreteness_coverage.png`.
- ✅ **T1 page** `theory/05_transformed_intervals.md` (2026-07-25) — the delta method as a
  variance-stabiliser (derived that arcsin√p is *the* stabiliser, Var → 1/(4n)); arcsine with its
  constant half-width and its **ZWI boundary collapse** (sin² folds −h onto +h; coverage min ≈ 0.004);
  logit/expit staying inside (0,1) with the exact one-sided boundary limit. Figure `transformed_coverage.png`.
- ✅ **T1 page** `theory/06_bayesian_view.md` (2026-07-25) — Beta–Binomial conjugacy (Beta(a+x, b+n−x));
  uniform/Jeffreys/Haldane priors; equal-tailed vs HPD credible intervals; credible ≠ confidence; and the
  convergence punchline — the **Jeffreys credible interval matches Wilson's frequentist coverage**
  (matching prior + Bernstein–von Mises). Figure `bayesian_posterior.png`; glossary +`conjugate prior`.
- ✅ **T1 page** `theory/07_coverage_theory.md` (2026-07-25) — the capstone: mean vs minimum coverage
  (never trust the mean — Wald's mean 0.89 hides min 0.004); oscillation persistence (Wilson's minimum
  crawls 0.84→0.94 as n:20→500, Brown–Cai–DasGupta); one-sided vs two-sided non-coverage; and the two
  repairs — adjustment (h=2 re-centres, min 0.004→0.94) vs continuity (c=0.5 over-corrects to coverage≈1).
  Figure `coverage_repairs.png`. Closes with a one-paragraph synthesis of the whole track.
- ✅ **T1 THEORY TRACK COMPLETE** (7 pages: 01 problem · 02 normal-approx · 03 test-inversion ·
  04 exact & discreteness · 05 transformed · 06 Bayesian · 07 coverage). Every method page's "Deeper
  maths → theory/index" now resolves to a substantial chapter.
- ✅ **T3 TUTORIALS/COOKBOOK COMPLETE** (2026-07-25) — new `tutorials/` group: A/B test (overlap + honest
  single-proportion caveat), quality control (P(θ<1%) posterior), zero events (rule of three = one-sided
  exact bound), choosing a method (`compare`/`recommend`, three strategies), and a 7-recipe cookbook, plus
  a hub and homepage card. All executable; three new figures; glossary +`sampling variability`.
- ⏭️ Next track: **T4 depth-on-existing-pages** — per-method *executed* numeric worked derivations +
  "interpretation & pitfalls" boxes; explain the unusual metrics (p-confidence, p-bias, error/long-term
  power) from scratch in `evaluating_intervals`; short concept-explainer pages. Also outstanding: **T5**
  (FAQ/troubleshooting, binomcikit-vs-statsmodels/scipy/R comparison).

## The workflow (per content page, mirrors the method-subphase discipline)
**Executable pages need this front matter** (so MyST-NB runs the cells):
```yaml
---
jupytext: {text_representation: {extension: .md, format_name: myst}}
kernelspec: {display_name: Python 3, name: python3}
---
```
Use ```{code-cell} python``` for cells that should execute; plain ```python``` stays a static snippet.

Draft with **progressive disclosure** (plain intuition → formula → derivation), **hand-checkable
numbers**, a **figure** where it helps, **every technical term linked to the glossary**, runnable
copy-paste snippets, and a clean `-W` docs build. Consider the `dataviz` skill for figures.

## Tracks, in priority order

### T1 — Build out the "Methods & Mathematics" theory track  ★ biggest hole
`theory/` currently has one page. Grow it into the real explanatory series the method pages point to:
1. The estimation problem & the sufficient statistic (exists — polish).
2. The normal approximation, the CLT, and **why Wald fails** (with the delta method).
3. **Test inversion** — score (Wilson) and likelihood-ratio, worked numerically.
4. **Exact methods & discreteness** — why coverage is jagged; CP, Mid-P, Blaker's acceptability.
5. **Variance-stabilising & transformed** intervals (arcsine, logit) via the delta method.
6. **The Bayesian view** — conjugacy, priors, credible vs confidence, Bernstein–von Mises.
7. **Coverage theory** — what coverage *is*, oscillation, one-/two-sided, the h & c repairs.
Each page: intuition → maths → a hand-worked n = 5 example → figure → references.

### T2 — Deepen Foundations into a true "probability from zero" track
Expand `foundations/` from one thin page to a short beginner series: proportion; Bernoulli & the
binomial (hand-worked pmf); sampling variability (a simulation); **what a confidence interval really
means** (repeated-sampling, shown by simulation); α & confidence level; **coverage as the key idea**.
Hand-checkable numbers and small figures throughout; no assumed background.

### T3 — Tutorials / Cookbook (task-oriented, real scenarios)  ★ high practical value
A new `tutorials/` (or `cookbook/`) group with end-to-end worked cases:
- A/B test conversion rate (choose method, interpret, visualise, report).
- Quality control: "is the defect rate below 1%?" via posterior probability.
- **Zero events in n trials** — the rule of three and boundary behaviour.
- Choosing a method *for your own data* with `compare` / `recommend`.
- (Later) sample-size / power planning.
Each: real numbers → method choice → interpretation → figure → how to report it.

### T4 — Depth on existing pages
- **Per method**: a numeric worked derivation (plug n = 5, x = 3, show every step); an
  "interpretation & pitfalls" box; annotated references with DOIs.
- **Evaluation guide**: explain the unusual metrics (p-confidence, p-bias, error/long-term power) from
  scratch with runnable simulations; add a coverage-plot gallery for all methods side by side.
- **Concept explainers**: short focused pages for cross-cutting ideas (coverage vs confidence level,
  discreteness, boundary behaviour, continuity correction, the h-adjustment) — deeper than the
  one-line glossary entries.

### T5 — Docs infrastructure / quality
- **Executable docs (MyST-NB)**: run code cells at build so tables/values are generated and always
  match the code (kills doc-drift, shows real output). Needs `myst-nb` in `docs/requirements.txt`.
- **Richer, consistent visuals** (dataviz skill): interval plots, coverage heatmaps, length curves.
- **FAQ / troubleshooting** page: "why is my interval [0,0]?", "what is ZWI?", "how does this differ
  from statsmodels / scipy?", "frequentist vs Bayesian?".
- **binomcikit vs statsmodels / scipy / R** comparison + when-to-use matrix.

## Recommended start
**T1 (theory track) + T2 (foundations)** — they fill the actual "detailed explanations" hole the method
pages already advertise. T3 (tutorials) is the best next for practical adoption.

## Done-when
Every "Deeper maths" / "New here?" link resolves to a substantial page; a beginner can go Foundations →
Methods → Theory and understand *why*; at least one full worked tutorial per common use case; `-W` clean.
