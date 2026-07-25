# binomcikit — Docs checklist (read this first for any docs work)

A self-contained, detailed checklist for the **documentation content-depth goal**. Structure is
settled (Furo, collapsible sidebar, executable MyST-NB); the job now is to deepen the *content*.

**Three planning docs, three jobs:**
- **`DOCS_STYLE_GUIDE.md`** — *how to write* every page (the book vision; the per-topic template of
  words → symbols → definition → 2–3 varied examples → "Check yourself" quiz; page-type skeletons).
  **Read it before writing any page.**
- **`DOCS_CHECKLIST.md`** (this file) — *what to build & how to verify* (status table, backlog,
  build/preview commands, per-page done-definition).
- **`DOCS_CONTENT_PLAN.md`** — the higher-level rationale / track breakdown.

Reference page that matches the style guide end-to-end: `docs/theory/02_normal_approximation.md`
(executed examples + a "Check yourself" quiz).

---

## 0. How to preview the docs locally (without committing)

You never need to commit to see changes. Two ways:

### Best — live preview that auto-rebuilds on save
```bash
pip install sphinx-autobuild          # one-time
sphinx-autobuild docs docs/_build/preview --open-browser --port 8000
```
Edit any `.md`, save, and the browser refreshes automatically at <http://127.0.0.1:8000>.
(Executable pages re-run their `{code-cell}` blocks on save, so they take a few seconds longer.)

### Fallback — build once, then serve
```bash
cd docs
python -m sphinx -b html . _build/html          # build
python -m http.server 8000 -d _build/html       # serve -> http://localhost:8000
```
Re-run the build command after each edit. `_build/` is git-ignored — none of this is ever committed.

> Windows note: if a `rm -rf _build` fails with "Device or resource busy", a `http.server` is still
> holding it — stop that server first (Ctrl-C, or kill the process on its port).

---

## 1. The build gate (must pass before calling any page done)
```bash
cd docs && python -m sphinx -b html -W --keep-going . _build/html
```
`-W` turns warnings into errors — it catches **undefined `{term}` links, broken `{doc}`/`{ref}`
cross-references, orphan pages, and failed `{code-cell}` executions**. A clean `-W` build is the
definition of "the docs are not broken". Also run a spot check in the browser (§0) for layout.

---

## 2. Docs stack & conventions (settled — do not re-litigate)

- **Theme:** Furo (`html_theme = "furo"`). Minimal top bar; nav lives in the left sidebar.
- **Collapsible sidebar:** the five caption groups toggle via `docs/_static/custom.{css,js}`. If you
  add a new top-level `:caption:` group it becomes collapsible automatically.
- **No edit/source button:** `html_show_sourcelink = False`, no `source_*` theme options. Keep it that way.
- **Toolchain pinned** in `docs/requirements.txt` (`sphinx<10`, `sphinx-design<1`, `furo`, `myst-nb<2`).
  Do not loosen — unpinned versions are what broke the layout before.
- **Executable docs (MyST-NB):** see §4. The package is installed editable (`pip install -e .`) so the
  build kernel can `import binomcikit`; `.readthedocs.yaml` installs it on RTD too.
- **Homepage banner gotcha:** never put a bare `<div align="center">` followed by a blank line in a
  `.md` — CommonMark ends the raw-HTML block at the blank line and the orphaned `</div>` breaks the
  whole page's article nesting. Use a ```{raw} html``` block for any multi-line centered HTML
  (see `docs/index.md`).
- **Figures:** generate with the plot engine and commit the PNG, e.g.
  ```bash
  python -c "import sys;sys.path.insert(0,'src');import binomcikit as b; \
  b.plot_coverage(n=20, methods=['wald','wilson']).write_image('docs/_static/NAME.png', width=820, height=460, scale=2)"
  ```
  Embed with a MyST `{figure}` directive + an explanatory caption (see any method page).

---

## 3. Per-page "definition of done" (apply to every new/edited page)
- [ ] **Progressive disclosure:** plain intuition first → then the formula → then a `:::{dropdown}`
      derivation. A beginner can read the top; an expert can open the dropdown.
- [ ] **Hand-checkable numbers:** at least one worked example with real values (prefer an *executed*
      cell — §4 — so it can't drift).
- [ ] **Every technical term linked** to the glossary with `{term}` on first use. If a term is missing,
      **add it to `docs/glossary.md`** (plain definition + a tiny example, cross-linked with `{term}`).
- [ ] **A figure** where it clarifies (coverage curve, interval plot). Caption says what to look at.
- [ ] **Cross-links:** "New here? see `{doc}` foundations"; "Deeper maths: `{doc}` theory"; link sibling
      methods. Fix any link that now points at a moved/merged page.
- [ ] **"Terms used on this page"** `:::{admonition}` box at the end (see method pages).
- [ ] **`-W` build clean** (§1) and a browser spot-check (§0).

---

## 4. Writing an EXECUTABLE page (MyST-NB)
Add this front matter so MyST-NB runs the cells:
```yaml
---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---
```
- Use ` ```{code-cell} python ` for cells that should **execute** and show real output.
- Use plain ` ```python ` for cells that should stay **static** (illustrative, not run).
- `nb_execution_raise_on_error = True`: a cell that errors **fails the build** — good, it means the
  docs always match the code. Seed any stochastic call (`seed=`) for deterministic output.
- Avoid plotting inside `{code-cell}` (plotly/plotnine aren't installed in the doc env) — pre-generate
  figures as PNGs (§2) instead. Numeric/DataFrame output is fine.
- Reference model page: `docs/theory/02_normal_approximation.md`.

---

## 5. Current state inventory (status of every page)

| Page | Lines | Status | Action |
|---|---|---|---|
| `index.md` | 120 | ✅ hub | keep cards in sync with sections |
| `getting_started.md` | 88 | 🟡 ok | could add a fuller first-analysis walkthrough |
| `foundations/index.md` | 55 | ✅ hub | landing/overview for the new 5-page beginner series |
| `foundations/01_proportion.md` | ~120 | ✅ **done** (executable) | T2 — proportion & p̂ |
| `foundations/02_binomial.md` | ~140 | ✅ **done** (executable) | T2 — Bernoulli & binomial pmf (hand-worked + figure) |
| `foundations/03_sampling_variability.md` | ~120 | ✅ **done** (executable) | T2 — sampling variability + SE + figure |
| `foundations/04_confidence_interval.md` | ~145 | ✅ **done** (executable) | T2 — what a CI means (repeated-sampling sim + caterpillar figure) |
| `foundations/05_coverage.md` | ~140 | ✅ **done** (executable) | T2 — coverage as the central idea (exact binomial sum + figure) |
| `method_selection.md` | 36 | 🟡 ok | short by design; keep the table current |
| `methods/index.md` | 40 | ✅ cheat-sheet | keep table current |
| `methods/*.md` (9) | 142–165 | ✅ solid | **T4** — add a numeric worked derivation + pitfalls box each |
| `evaluating_intervals.md` | 89 | 🟡 ok | **T4** — explain p-confidence/p-bias/error from scratch + a sim |
| `bayesian_toolbox.md` | 103 | ✅ solid | optional worked Bayes-factor / predictive examples |
| `access_layer.md` | 100 | ✅ solid | make snippets executable cells |
| `gallery.md` | 80 | 🟡 ok | ensure Plotly figures render; add coverage-plot gallery |
| `theory/index.md` | 22 | 🟡 stub | toctree now lists 01–03; update as more land |
| `theory/01_the_problem.md` | 106 | ✅ ok | make its snippets executable |
| `theory/02_normal_approximation.md` | 126 | ✅ **done** (executable) | model for the rest |
| `theory/03_test_inversion.md` | ~215 | ✅ **done** (executable) | T1 — score (Wilson) + LR via test inversion + figure |
| `theory/04_exact_and_discreteness.md` | ~230 | ✅ **done** (executable) | T1 — discreteness, CP/Mid-P/Blaker, acceptability γ(x,θ) + figure |
| `theory/05_transformed_intervals.md` | ~220 | ✅ **done** (executable) | T1 — delta method, arcsine (constant variance + ZWI boundary fail), logit + figure |
| `theory/06_bayesian_view.md` | ~230 | ✅ **done** (executable) | T1 — Beta conjugacy, priors, credible vs confidence, Jeffreys' frequentist coverage + figure |
| `theory/07_coverage_theory.md` | ~215 | ✅ **done** (executable) | T1 — mean vs min coverage, oscillation persistence, one-/two-sided, h & c repairs + figure (**T1 track complete**) |
| `tutorials/index.md` | ~45 | ✅ hub | T3 — tutorials + cookbook landing |
| `tutorials/ab_test.md` | ~130 | ✅ **done** (executable) | T3 — A/B conversion; overlap + single-proportion caveat + figure |
| `tutorials/quality_control.md` | ~120 | ✅ **done** (executable) | T3 — "defect rate < 1%?" via posterior probability + figure |
| `tutorials/zero_events.md` | ~120 | ✅ **done** (executable) | T3 — rule of three, Wald `[0,0]` trap + figure |
| `tutorials/choosing_a_method.md` | ~120 | ✅ **done** (executable) | T3 — `compare` / `recommend`, three strategies |
| `tutorials/cookbook.md` | ~110 | ✅ **done** (executable) | T3 — 7 copy-paste recipes |
| `glossary.md` | 288 | ✅ good | +`hypothesis test`, +`discreteness`; grow as new terms appear |
| `migrating_from_r.md` | 31 | ✅ ok | fine |
| `r_to_python_mapping.md` | 863 | ✅ generated | do not hand-edit |
| `api/index.md` + `reference/*` | — | ✅ autodoc | regenerate only via `tools/gen_reference_pages.py` |

---

## 6. Content backlog (the checklist to work through)

### T1 — "Methods & Mathematics" theory track  ✅ COMPLETE 2026-07-25 (7 pages)
Each page: intuition → maths → an *executed* n = 5 worked example → figure → "Terms used" box.
- [x] `02_normal_approximation` — normal approx, Wald, the two failures, delta method.
- [x] `03_test_inversion` — inverting a hypothesis test; **Wilson** (score) as a quadratic solve, and
      the **likelihood-ratio** interval; shows numerically that both bracket p̂ and beat Wald, and that
      z² = χ²₁(0.95) is the shared cutoff. Figure: `test_inversion_coverage.png`.
- [x] `04_exact_and_discreteness` — why binomial coverage is a jagged step function; Clopper–Pearson,
      Mid-P, and **Blaker's acceptability** function γ(x,θ) reproduced from scratch (accept(3,L,5)=α),
      the Blaker⊂CP nesting check, and the coverage-guarantee vs width trade-off table. Figure:
      `exact_discreteness_coverage.png`.
- [x] `05_transformed_intervals` — variance-stabilising via the **delta method** (derived that arcsin√p
      is *the* stabiliser → Var 1/(4n)); arcsine (`sin²φ`, half-width constant) and its **ZWI boundary
      collapse** (sin² folds −h→+h; coverage min ≈ 0.004); logit/expit staying inside (0,1) with the exact
      one-sided boundary limit. Figure: `transformed_coverage.png`.
- [x] `06_bayesian_view` — Beta–Binomial conjugacy (Beta(a+x, b+n−x)); uniform/Jeffreys/Haldane priors;
      equal-tailed vs HPD credible intervals (reproduced via `scipy.beta.ppf`); credible ≠ confidence; and
      that the **Jeffreys credible interval matches Wilson's frequentist coverage** (0.952 vs 0.953 at
      n=40) — matching prior + Bernstein–von Mises. Figure: `bayesian_posterior.png`. Glossary +`conjugate prior`.
- [x] `07_coverage_theory` — mean vs minimum coverage (never trust the mean); oscillation persistence
      (Wilson min crawls 0.84→0.94 as n:20→500, Brown–Cai–DasGupta); one-sided vs two-sided non-coverage
      split; the `h` (adjustment, h=2→Agresti–Coull, min 0.004→0.94) and `c` (continuity, c=0.5→coverage≈1
      over-corrects) repairs. Figure: `coverage_repairs.png`. **Capstone — synthesises the whole track.**
- [x] Updated `theory/index.md` toctree + intro (series now framed as a complete arc, not "growing").

### T2 — Deepen Foundations (probability from zero)  ✅ DONE 2026-07-25
- [x] proportion & the sample estimate p̂ (`01_proportion`); [x] Bernoulli trials & the binomial pmf,
      hand-worked (`02_binomial`); [x] sampling variability, executed simulation + SE (`03_sampling_variability`);
- [x] **what a confidence interval really means**, repeated-sampling simulation + caterpillar figure
      (`04_confidence_interval`); [x] α & confidence level + [x] coverage as the central idea, exact
      binomial-sum computation (`05_coverage`). `foundations/index` is now the series landing/hub.
      Figures: `foundations_{binomial_pmf,sampling,ci_repeated,coverage}.png` (matplotlib, dataviz palette).

### T3 — Tutorials / Cookbook (new `tutorials/` group)  ✅ COMPLETE 2026-07-25
- [x] A/B-test conversion rate (Wilson per arm; overlap read; honest single-proportion caveat + forest figure).
- [x] Quality control: "is the defect rate below 1%?" via `posterior` / P(θ<0.01) ≈ 88–93% + tail figure.
- [x] **Zero events in n** — Wald `[0,0]` trap, Wilson/exact bound, rule of three 3/n = one-sided exact + figure.
- [x] "Choose a method for *your* data" using `compare` / `recommend` (three `by` strategies), executable.
- [x] Cookbook page (7 recipes) + `tutorials/index` hub + `:caption: Tutorials` toctree group + homepage card.

### T4 — Depth on existing pages
- [ ] Per method: an *executed* numeric derivation (n = 5, x = 3, every step) + an
      "Interpretation & pitfalls" admonition + annotated references with DOIs.
- [ ] `evaluating_intervals`: explain p-confidence, p-bias, error/long-term power from scratch with a
      runnable simulation; add a side-by-side coverage-plot gallery.
- [ ] Short **concept explainers** (deeper than glossary): coverage vs confidence level, discreteness,
      boundary behaviour, continuity correction, the h-adjustment.

### T5 — Infra / quality
- [x] Executable docs (MyST-NB) wired up; edit-button removed; sidebar collapsible.
- [ ] FAQ / troubleshooting page ("why is my interval [0,0]?", "what is ZWI?", "vs statsmodels/scipy?",
      "frequentist vs Bayesian?").
- [ ] `binomcikit` vs `statsmodels` / `scipy` / R comparison + when-to-use matrix.
- [ ] Consider the `dataviz` skill to standardise figure styling.

---

## 7. Things that break the build (avoid / check for)
- Undefined `{term}` → add the term to `glossary.md`.
- A `{doc}` link to a **moved/merged/deleted** page (the reorg removed `user_guide/`; point at
  `evaluating_intervals`, `method_selection`, `bayesian_toolbox`, or `foundations/index`).
- A `{code-cell}` that raises (or is missing the jupytext front matter → "unexpected code-cell" warning).
- A bare multi-line `<div>` in markdown (use `{raw} html`).
- A new page not added to any `{toctree}` → orphan warning under `-W`.
- Loosening the pinned theme versions in `docs/requirements.txt`.

## 8. Uncommitted right now (for the next session to commit)
Theme/UX: `docs/conf.py`, `docs/_static/custom.css`, `docs/_static/custom.js`, `docs/requirements.txt`,
`.readthedocs.yaml`. Content (earlier): `docs/theory/02_normal_approximation.md`, `docs/theory/index.md`,
`docs/glossary.md`, `CHANGELOG.md`, `planning/DOCS_CONTENT_PLAN.md`, this file.
**New this session (2026-07-25 docs rebuild):**
- Theory T1 (**complete track**): `docs/theory/03_test_inversion.md` + `04_exact_and_discreteness.md` +
  `05_transformed_intervals.md` + `06_bayesian_view.md` + `07_coverage_theory.md` (executable) +
  `theory/index.md` intro rewrite.
- **Tutorials T3 (complete)**: new `docs/tutorials/` dir — `index.md`, `ab_test.md`, `quality_control.md`,
  `zero_events.md`, `choosing_a_method.md`, `cookbook.md` (all executable) + `index.md` toctree group & card.
- Foundations T2 series: rewritten `docs/foundations/index.md` + `docs/foundations/01_proportion.md`,
  `02_binomial.md`, `03_sampling_variability.md`, `04_confidence_interval.md`, `05_coverage.md` (all executable).
- Glossary: added `hypothesis test`, `discreteness`, `conjugate prior`, `sampling variability` terms.
- Figures (matplotlib, dataviz palette): `docs/_static/test_inversion_coverage.png`,
  `exact_discreteness_coverage.png`, `transformed_coverage.png`, `bayesian_posterior.png`,
  `coverage_repairs.png`, `tutorial_ab.png`, `tutorial_qc.png`, `tutorial_zero.png`,
  `foundations_binomial_pmf.png`, `foundations_sampling.png`, `foundations_ci_repeated.png`, `foundations_coverage.png`.
- Homepage: `docs/index.md` gained a `:caption: Tutorials` toctree group + a Tutorials card.

Verify `-W` clean (§1) — **confirmed clean 2026-07-25** — then commit (docs-only) and push; RTD rebuilds automatically.
