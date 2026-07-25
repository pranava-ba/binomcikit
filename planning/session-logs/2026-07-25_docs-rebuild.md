# Session log — 2026-07-25 · Docs content rebuild (T1 test-inversion + T2 Foundations series)

> A faithful record of the working session: the user message verbatim, the assistant's generated prose,
> and a compact log of each tool action and its key result. Tool outputs are summarized to their salient
> facts (full command output is not reproduced) so the record stays readable. Model: Claude Opus 4.8.
> Repo: `binomcikit` (Phase 1). Goal for the session: the docs content-depth initiative (docs-only).

---

## Turn 1 — User: "refers the docs guides and start re building the docs"

**Assistant:** Read the three docs guides + the model page, verified the environment and every
hand-checkable number, generated colourblind-safe teaching figures, then wrote one theory page and a
five-page Foundations series, verifying a clean `-W` build and browser spot-checks throughout.

**Orientation & guides read:**
- `planning/CONTINUE_HERE.md`, `planning/DOCS_CONTENT_PLAN.md`, `planning/DOCS_STYLE_GUIDE.md`,
  `planning/DOCS_CHECKLIST.md` — the active goal is deepening docs *content*; recommended start is
  **T1 (theory track) + T2 (Foundations)**. Structure (Furo, collapsible sidebar, executable MyST-NB)
  is settled and not to be re-litigated.
- Model page `docs/theory/02_normal_approximation.md`; existing `foundations/index.md`, `theory/index.md`,
  `theory/01_the_problem.md`, `docs/index.md` toctrees, and the glossary term list.

**Environment / correctness checks (before writing any cell):**
- `binomcikit` v3.0.8 imports; confirmed all functions used exist (`ci`, `ciscx`, `cisc`, `cilr`,
  `cilrx`, `ciwd`, `coverage_curve`, `point_estimate`, `compare`, …).
- Captured real outputs and hand-verified: Wilson centre for x=3,n=5 = 0.556552 → `[0.230724, 0.882379]`
  (matches `ciscx`); LR deviance at both `cilrx(3,5)` endpoints = 3.8415 = χ²₁(0.95) = z²; binomial pmf
  P(X=2|n=5,θ=0.4)=0.3456; seeded sims — sampling SD 0.1024 vs theory 0.1025; caterpillar 38/40 cover
  at θ=0.3,n=40,seed42; big-N covered fraction 0.9443 (seed7,N=10000); exact Wilson coverage θ=0.3 = 0.9443
  (= the sim), Wald = 0.9299; curve means Wilson 0.953/min 0.92, Wald 0.887/min 0.004.
- **Figure pipeline:** Plotly+kaleido **fails here** (kaleido needs a browser that won't launch in the
  sandbox — `BrowserFailedError`). Switched to **matplotlib (Agg)**, styled with the `dataviz` skill's
  validated palette (blue `#2a78d6`, orange `#eb6834`, aqua `#1baf7a`; neutral ink; recessive grid).

**Baseline:** full `-W` docs build clean before any edits.

**Figures generated** (matplotlib → `docs/_static/`, eyeballed via Read):
`test_inversion_coverage.png` (Wald sags, Wilson+LR track, n=40), `foundations_binomial_pmf.png`
(n=10,θ=0.5 bars), `foundations_sampling.png` (100k-sample p̂ histogram), `foundations_ci_repeated.png`
(40-interval caterpillar, 38 cover / 2 miss), `foundations_coverage.png` (Wald vs Wilson coverage, n=40).
Fixed a legend label ("Lr"→"LR") and regenerated.

**Pages written (all executable MyST-NB, per the style guide):**
- **T1** `docs/theory/03_test_inversion.md` — score (Wilson) + likelihood-ratio intervals derived as
  *inverting a hypothesis test*; executed Wald-vs-Wilson grid, hand-checked Wilson centre, LR deviance
  sitting on the χ²₁ cutoff, the z²=χ²₁(0.95) identity, a coverage comparison + figure, dropdown
  derivation of the Wilson quadratic, "Check yourself" quiz, "Terms used" box. Added to `theory/index`
  toctree. Fixed two forward-references to the not-yet-written `04_exact_and_discreteness` (pointed at
  `methods/exact` / plain text) so `-W` stays clean.
- **T2** Foundations series — rewrote `foundations/index.md` into a landing/hub with a nested toctree,
  then wrote five concept pages following the words → symbols → definition → executed examples →
  "Check yourself" template:
  - `01_proportion.md` — θ vs p̂; the estimate is not the truth; boundary (0 successes ≠ θ=0).
  - `02_binomial.md` — Bernoulli trials & the binomial pmf, hand-worked (0.3456) + pmf figure + a
    dropdown tying the pmf to the coverage machinery.
  - `03_sampling_variability.md` — why two samples disagree; SE = √(θ(1−θ)/n); the 1/√n law; simulation
    + histogram figure.
  - `04_confidence_interval.md` — what a CI *really* means, shown by a repeated-sampling simulation
    (38/40 cover) + caterpillar figure + a big-N run (0.9443); dropdown on why "95% chance it's in this
    interval" is wrong (→ Bayesian credible interval).
  - `05_coverage.md` — coverage as an exact sum over the binomial (recomputes 0.9443, matching the sim),
    the wobble from discreteness, mean/min via `coverage_curve`, Wald-vs-Wilson figure, over-covering
    dropdown; closes the arc and links out to methods/theory.
- **Glossary:** added `hypothesis test` and `discreteness` (both used above; keeps `-W` clean).

**Verification:**
- Full `-W --keep-going` build **clean (exit 0)**; every new page's `{code-cell}` executed without error.
- Browser spot-check (served `_build/full` on :8901): `foundations/04` shows executed `(38, 40)`, the
  interval table, and `0.9443`; `theory/03` shows the Wald/Wilson grid and `by hand … = package …`
  (0.230724, 0.882379) matching exactly. Stopped the server after.

**Handoff updated:** `planning/DOCS_CHECKLIST.md` (status table + T1/T2 backlog + §8 uncommitted list),
`planning/DOCS_CONTENT_PLAN.md` (progress), `planning/CONTINUE_HERE.md` §1, `CHANGELOG.md`, and the
`docs-content-goal` memory. Per the user's workflow preference, no unsolicited git block was pasted —
the upload block lives in `CONTINUE_HERE.md` §7; changes are docs-only and ready to push.

---

## Turn 2 — User: "continue"

**Assistant:** Continued the T1 theory track with the next page, `theory/04_exact_and_discreteness.md`.

**Correctness checks first:** confirmed `ciex(n, alp, e)` takes `e` as a float/list (`e=1.0`
Clopper–Pearson, `e=0.5` Mid-P) — passing `e=1` as an int raises; `ciexx` needs `e` as a **list**; Blaker
grid columns are `LBK`/`UBK`; `coverage_curve` accepts `method` in {`exact`, `midp`, `blaker`, …}.
Implemented Blaker's **acceptability function** γ(x,θ) from scratch (min-tail construction) and verified it
reproduces the package's Blaker endpoints exactly — `accept(3, L, 5) = accept(3, U, 5) = 0.05 = α` — and
that `accept(3, 0.25, 5) = 0.1035 ≥ α` (0.25 inside). Locked the coverage table at n=40: CP mean 0.971/min
0.952 (always ≥0.95), Blaker 0.962/0.950 (always ≥0.95, tighter → dominates CP), Mid-P 0.957/0.928, Wilson
0.953/0.920; Blaker⊂CP nesting `True` at every x.

**Figure:** `exact_discreteness_coverage.png` (matplotlib, dataviz palette) — CP highest/widest, Blaker
between but still ≥95%, Wilson weaving through the line.

**Page written:** `theory/04_exact_and_discreteness.md` (executable) — discreteness → jagged coverage;
Clopper–Pearson (invert the exact test, conservative); Mid-P (shave the atom, loses the guarantee); Blaker
(acceptability γ, guaranteed *and* nested in CP); a guarantee-vs-width table; figure; "Check yourself"
quiz; "Terms used" box. Added to `theory/index` toctree; upgraded page 03's forward reference into a live
`{doc}` link. Fixed one `-W` warning (`{term}`Blaker`` → `{doc}` link — "Blaker" isn't a glossary
headword) and a `{term}`tail probability`s` pluralization (×2). **Final `-W` build clean**; browser
spot-check confirmed the executed acceptability/nesting/table cells render correctly. Handoff docs +
memory updated.

---

## Turn 3 — User: "continue"

**Assistant:** Wrote the next T1 page, `theory/05_transformed_intervals.md`.

**Correctness checks first:** confirmed `cias`/`ciasx` (arcsine, cols `LAS`/`UAS`) and `cilt`/`ciltx`
(logit, cols `LLT`/`ULT`); both signatures `(n, alp)` / `(x, n, alp)`. Hand-derived and matched the
package for x=3, n=5: arcsine `sin²(arcsin√p ± z/2√n)` = `[0.187487, 0.940478]`; logit
`expit(logit(p) ± z√(1/np̂q̂))` = `[0.200411, 0.899769]`. **Key finding — arcsine's boundary failure:**
`cias` flags `ZWI = YES` at x=0 and x=n because `sin²` is even, so `sin²(0−h) = sin²(0+h)` and the
interval collapses to a point; its coverage min at n=40 is **0.004**. **Logit's boundary:** undefined at
x=0/n (log 0), so the source substitutes the exact one-sided limit — at x=0, `[0, 1−(α/2)^{1/n}]` (verified
against `base_n.py:637-645`). Coverage n=40: ArcSine mean 0.898/min 0.004 (share≥0.95 = 0.25), Logit
0.959/0.938 (0.78), Wilson 0.953/0.920 (0.54).

**Figure:** `transformed_coverage.png` (matplotlib, dataviz palette) — ArcSine plunging to the axis at
both boundaries (annotated), Logit + Wilson tracking nominal.

**Page written:** `theory/05_transformed_intervals.md` (executable) — the delta method as the engine, a
dropdown deriving that `arcsin√p` is *the* variance-stabiliser (Var → 1/(4n)), arcsine with its
constant half-width and ZWI collapse, logit/expit staying inside (0,1) with the exact boundary limit, a
coverage table, the figure, "Check yourself" quiz, "Terms used" box. Added to the `theory/index` toctree
and upgraded page 04's forward reference into a live `{doc}` link. **Final `-W` build clean** (no term
warnings — all terms already in glossary); browser spot-check confirmed every executed cell renders
(hand-checks, the ZWI demo, the boundary-limit match, the table). Handoff docs + memory updated.

---

## Turn 4 — User: "continue"

**Assistant:** Wrote the next T1 page, `theory/06_bayesian_view.md`.

**Correctness checks first:** confirmed the Bayesian surface — `ciba`/`cibax(x,n,alp,a,b)` (cols `LBAQ`/`UBAQ`
equal-tailed + `LBAH`/`UBAH` HPD), `posterior(x,n,a,b)` (dict with `a_post`,`b_post`,`mean`,`mode`,
`quantile_interval`,`hpd_interval`), `prior(name)` → uniform/laplace (1,1), jeffreys (0.5,0.5), haldane (0,0).
Verified conjugacy by hand: `posterior(3,5)` → Beta(4,3), mode 0.6 = MLE, mean 4/7; Jeffreys →
Beta(3.5,2.5); `scipy.beta.ppf(0.025/0.975, 4, 3)` reproduces the package's equal-tailed interval exactly.
**Convergence punchline verified:** at n=40, Jeffreys credible coverage (mean 0.952/min 0.918) ≈ Wilson
(0.953/0.920), while uniform-prior ("bayes") is worse (0.940/min 0.000).

**Figure:** `bayesian_posterior.png` (matplotlib + scipy) — flat Beta(1,1) prior updating to the peaked
Beta(4,3) posterior (95% credible band shaded) with the Jeffreys Beta(3.5,2.5) posterior alongside and the
observed p̂ = 0.6 marked.

**Page written:** `theory/06_bayesian_view.md` (executable) — Beta conjugacy (add successes to a, failures
to b), the standard priors, equal-tailed vs HPD credible intervals (reproduced via scipy), the credible ≠
confidence distinction (tied back to foundations/04), and why Jeffreys is a matching prior with good
frequentist coverage (Bernstein–von Mises, in prose). Added glossary term `conjugate prior`; wired into the
toctree; upgraded page 05's forward link. Fixed a cosmetic `np.float64(...)` display (cast to `float`).
**Final `-W` build clean**; browser spot-check confirmed all executed cells render. Handoff docs + memory updated.

---

## Turn 5 — User: "yes, go ahead"

**Assistant:** Wrote the final T1 page, `theory/07_coverage_theory.md` — the capstone — **completing the
theory track**.

**Correctness checks first:** confirmed the h/c repair functions — `ciawd(n,alp,h)` (adj Wald, cols
`LAWD`/`UAWD`), `cicwd(n,alp,c)` (CC Wald, cols `LCW`/`UCW`), plus score variants; `coverage_curve`
methods are base-only (arcsine, bayes, blaker, cp/exact, jeffreys, logit, lr, midp, score, wald, waldt,
wilson) — **no adjusted/CC variants**, so their coverage is computed via the exact binomial sum on the
grids. Locked: two-summary table at n=40 (Wald 0.889/**0.004**, Wilson 0.952/0.871, exact 0.971/0.952,
Blaker 0.963/0.950); oscillation — Wilson min coverage crawls 0.837→0.857→0.897→0.904→0.938 as
n=20→40→80→200→500 while mean stays ~0.95 (Brown–Cai–DasGupta); one-sided split (exact) Wald at θ=0.05
→ (0.0034, 0.1285) lopsided, at θ=0.5 → (0.0403, 0.0403) balanced; repairs — adj Wald h=2 min 0.004→0.937,
CC Wald c=0.5 → coverage ≈ 1.0 everywhere (c=0.5 is the documented standard; it over-corrects).

**Figure:** `coverage_repairs.png` (matplotlib) — raw Wald (plunging), + adjustment h=2 (tracks nominal),
+ continuity c=0.5 (pinned at ~1.0), all at n=40.

**Page written:** `theory/07_coverage_theory.md` (executable) — mean vs minimum coverage ("never trust the
mean"), oscillation and its slow non-convergence, one-sided vs two-sided non-coverage, the h & c repairs,
and a one-paragraph synthesis of the entire series. Added to the toctree; rewrote `theory/index.md`'s intro
to frame the series as a complete arc (not "growing"); upgraded page 06's forward link. No new glossary
terms needed. **Final `-W` build clean**; browser spot-check confirmed the tables and split render.
**T1 theory track is complete (7/7).** Handoff docs + memory updated.

---

## Turn 6 — User: "t3"

**Assistant:** Built the **entire T3 tutorials/cookbook track** in one turn — a new `tutorials/` group.

**Correctness checks first:** `compare(x,n)` → ranked table (method/lower/upper/width); `recommend(n,by=)`
with `by` ∈ {length, coverage, min_coverage} → measured ranking with an `adequate` flag; `posterior(x,n,a,b)`
+ `scipy.beta.cdf` for tail probabilities; `from_data`/`from_counts`; `point_estimate` methods
mle/ac/jeffreys/laplace; single-x interval columns always positional (`iloc[0,1:3]` = lower/upper).
**binomcikit is single-proportion** (no two-sample test) → the A/B tutorial is framed honestly around
comparing each arm's interval + an explicit caveat. Locked numbers: A/B 32/500 [0.046,0.089] vs 45/500
[0.068,0.118] (overlap); QC 2/500 → P(θ<1%) 0.88 (uniform) / 0.93 (Jeffreys), Wilson CI upper 1.4%;
zero-events rule of three 3/100=0.030 vs exact one-sided 0.0295; `recommend(30)` picks LR (length) /
Jeffreys (coverage) / Clopper-Pearson (min_coverage).

**Figures ×3** (matplotlib): `tutorial_ab.png` (forest plot, overlap shaded), `tutorial_qc.png` (posterior
with P(θ<1%) tail shaded), `tutorial_zero.png` (rule of three tracking the exact bound vs n).

**Pages written** (all executable, following the style-guide tutorial skeleton — situation → question →
choosing → running → reading → figure → how to report → what could go wrong → try-it-yourself):
`tutorials/index.md` (hub), `ab_test.md`, `quality_control.md`, `zero_events.md`, `choosing_a_method.md`,
and `cookbook.md` (7 Problem→Recipe→Result→See-also recipes). Added glossary term `sampling variability`;
added a `:caption: Tutorials` toctree group + a Tutorials card to `index.md`. **Final `-W` build clean**;
browser spot-check confirmed the compare/recommend tables and strategy dict render. Handoff docs + memory updated.

---

## Deliverables summary

| Item | Path |
|---|---|
| Theory T1 track (**complete, 7 pages**) | `docs/theory/0{1..7}_*.md` (new this session: 03–07) + `theory/index.md` intro |
| Foundations T2 (**complete, 6 pages**) | `docs/foundations/index.md` (rewritten) + `0{1..5}_*.md` |
| Tutorials T3 (**complete, 6 pages**) | `docs/tutorials/{index,ab_test,quality_control,zero_events,choosing_a_method,cookbook}.md` |
| Glossary terms | +`hypothesis test`, +`discreteness`, +`conjugate prior`, +`sampling variability` |
| Figures ×12 | `docs/_static/{test_inversion_coverage,exact_discreteness_coverage,transformed_coverage,bayesian_posterior,coverage_repairs,tutorial_ab,tutorial_qc,tutorial_zero,foundations_binomial_pmf,foundations_sampling,foundations_ci_repeated,foundations_coverage}.png` |
| Homepage | `docs/index.md` — Tutorials toctree group + card |

**Build:** `cd docs && python -m sphinx -b html -W --keep-going . _build/html` → clean. Docs-only; RTD
rebuilds on push. **✅ T1 theory (7pp), T2 foundations (6pp), T3 tutorials (6pp) all complete. Next: T4 depth-on-existing-pages, T5 FAQ/comparison.**
