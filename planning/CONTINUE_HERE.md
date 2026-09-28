# CONTINUE HERE — session handoff (read this first)

> **New chat?** Read this page top to bottom and you're oriented. It is the single source of
> "where we are, how to continue, how to verify, what to upload." **Update the "Current state" and
> "Upload" sections at the END of every sub-phase** so the next session starts clean.

---

## 1. Current state — updated 2026-09-28
- **Version:** 3.0.8 (pre first real PyPI release; PyPI still has an old 0.0.5).
- **Tests:** **302 passing**; `ruff` + `black` clean; **Sphinx docs build clean with `-W`** (run it with
  `PYTHONPATH=../src` locally — see the T4/T5 build note below and `DOCS_CHECKLIST.md §1`).
- **Editable install was stale, now fixed (2026-09-28):** `pip show binomcikit` pointed at
  `Desktop/Projects/binomcikit` (no `archived/`) — a path that no longer exists, left over from before
  the repo moved under `archived/`. This silently broke the MyST-NB docs build's kernel subprocess
  (`ModuleNotFoundError: binomcikit`, even with `PYTHONPATH` set, since the kernel reads the installed
  package metadata, not the ambient env var). Fixed via `pip install -e ".[test]"` from this repo root.
  If a fresh clone/session hits the same docs-build error, re-run that.
- **Coverage gap closed (2026-09-28):** new `coverage` CI job (`pytest-cov`, branch coverage) —
  baseline **64.8%**, CI floor set at 60% (regression gate, not a target). `pytest-cov` now in the
  `[test]` extra; config in `pyproject.toml`'s `[tool.coverage.*]`; documented in
  `docs/under_the_hood.md` ("Coverage"); README got a coverage badge. Worst-covered modules are the
  legacy plotnine `*_graph.py` files (4–8%, slated for retirement — see §8 plotting decision).
- **`previous-work/` and `paper-explorer/` are now gitignored (2026-09-28)** — side tooling (lit-review
  corpus, prior-work notes), not part of the installable package. The 8 previously-tracked
  `previous-work/*.md` files were untracked (`git rm --cached`; still on disk, just not in the repo
  going forward).
- **Phase 1 progress:** 1.0 infra · 1.1 Wald · 1.2 Wilson · 1.3 ArcSine · 1.4 Logit · 1.5 Wald-T · 1.6 LR · 1.7 Exact/Mid-P · 1.8 Bayesian+6xx · 1.9 Blaker (NEW method) · 1.10 Bootstrap (NEW method) · 1.11 Frequentist p-value tests · **1.12 Sample-size/power DONE — all of Phase 1's committed method/feature work is now done**. Remaining Phase-1 items are cross-cutting polish only (see below).
- **Bug found AND fixed (2026-09-28):** `cilrx`/`cilr` (Likelihood-Ratio interval) broke at large n —
  root-find snapped to ~`[0, 1]` somewhere between `n=25,800` (correct) and `n=26,000` (broken). Found
  incidentally while stress-testing `sample_size`'s search, then root-caused (MLE step minimized the raw
  likelihood, which underflows to 0.0 for large n; the numerical optimizer converged to an arbitrary
  wrong point) and fixed (closed-form MLE + `brentq`, not `minimize_scalar`) the same session — see
  **### Fixed** in `CHANGELOG.md` and `docs/under_the_hood.md` "Sample-size / power" for the full
  writeup. A systematic audit of every `scipy.optimize` call in the package (prompted by this bug) found
  the identical pattern in `cialr` (`adj_n.py`) — also fixed — and confirmed 3 other candidates
  (`cialrx`, `_hpd.py`'s HPD search, the exact/Mid-P family's `root_scalar`/bisect calls) were **not**
  affected, verified empirically up to n=1,000,000 each, not just assumed safe.
- **Known issue, found during that same audit, NOT fixed (low severity):** `ciblaker`/`ciblakerx` raise
  `ValueError` instead of returning a result for `alpha` above roughly `1 - 1e-10` — a confidence level
  with no practical meaning; nothing in the package ever requests it, and `pvalue`/`reject`/
  `sample_size`/`power` already guard against it defensively. Left open — different root cause from the
  LR bug, low impact, not investigated further this session. Details: `docs/under_the_hood.md`.
- **1.12 sample-size/power (2026-09-28):** `sample_size`/`power` in `src/binomcikit/access.py` — exact
  smallest-n search (via each method's single-`x` dispatcher, not the whole-table `_limits`, to keep the
  search `O(log n_max)` not `O(n_max)`) and exact (not simulated) CI-duality power, reusing 1.11's
  `reject()` construction for cross-verification. `sample_size(method="wald")` matches
  `statsmodels.samplesize_confint_proportion` exactly; other methods checked against their own
  minimality property. `docs/access_layer.md` section, 3 glossary terms, 25 tests
  (`tests/test_sample_size_power.py`). Excludes bootstrap, same as `pvalue`/`reject`.
- **1.11 p-value tests (2026-09-28):** `pvalue`/`reject` in `src/binomcikit/access.py` — CI-test
  duality (θ₀ rejected at level α iff outside the method's `(1-α)` CI; bisection on α), works for any
  registered method except the bootstrap family (raises a clear error there). **Not verified against
  `scipy.stats.binomtest`** — its default two-sided p-value uses a different ("minlike") convention that
  genuinely disagrees with the equal-tailed construction here; verified instead against the closed-form
  equal-tailed formula for `"exact"`, scipy's one-sided tails, and the CI-duality property directly
  across methods. New `docs/access_layer.md` section (incl. a documented Wald-vs-everyone-else
  divergence — expected, not a bug), 1 new glossary term, 30 tests (`tests/test_pvalue.py`).
  **Perf note:** kept the bisection budget to 16 iterations on purpose — root-finding methods
  (exact/LR/Blaker) re-run their whole CI table per iteration, so this alone added ~45s to the suite;
  see the `pvalue` docstring's Notes section before raising it.
- **1.10 Bootstrap (2026-09-28):** `src/binomcikit/ci/bootstrap.py` (`ciboot`/`cibootx`,
  `method="boot"`) — three variants via `kind`: `"percentile"`/`"bca"` (thin wrapper around
  `scipy.stats.bootstrap`, oracle-verified exactly) and `"smooth"` (default; Wang & Hutson 2013 [25],
  implemented from the paper's primary text — no third-party oracle, verified instead by the MUE
  boundary identity + rough cross-agreement with percentile/BCa + the boundary non-degeneracy property
  the method exists for). 4 metric wrappers (`covpboot`/`lengthboot`/`pcopbiboot`/`errboot`), dispatcher
  + Plotly wiring, `point_estimate(..., "mue")`, `docs/methods/bootstrap.md`, 7 glossary terms, 25 tests
  (`tests/test_bootstrap.py`). **Deferral note from 2026-07-24 is superseded** — this was previously
  deferred for lacking an oracle; the user explicitly decided to proceed on 2026-09-28, accepting that
  risk for `kind="smooth"` specifically (not for `"percentile"`/`"bca"`, which are fully oracle-verified).
  Full details/rationale: this session's chat, and the "Coverage" section additions in
  `docs/under_the_hood.md`.
- **Access/usability layer DONE** (`src/binomcikit/access.py`, `tests/test_access.py`, `docs/access_layer.md`):
  `from_counts`/`from_data`, `point_estimate`, `posterior`/`prior`, `coverage_curve`/`length_curve`,
  `compare`, `recommend` (reuses the Plotly `_limits` registry). **Docs finalized**: `access_layer` +
  `bayesian_toolbox` in the Learn nav; API reference gained `binomcikit.access` + `binomcikit.ci.blaker`;
  full site builds clean under `-W`. **Typing:** `py.typed` (PEP 561, in package-data) + hints on the
  public surface (`ci`, `plot_ci`, `plot_coverage`, all of `access`); internal grid functions unhinted
  (incremental follow-up).
- **Repo checkpoint:** 1.0 + 1.1 pushed to **`origin/main`** at **`c299b2f`**. **1.2–1.9 are complete
  locally and awaiting the user's manual push** (see §7). 1.2 docs-only; 1.3–1.8 docs+figure+glossary+
  oracle each; **1.9 Blaker = genuinely new code** (`src/binomcikit/ci/blaker.py` + 4 metric wrappers +
  dispatcher + Plotly + `tests/test_blaker.py`, 15 tests). Oracles/checks: `ARCSINE_N5`/`LOGIT_N5`/
  `WALDT_N5`/`LR_N5`/`MIDP_N5`/`BLAKER_N5` + statsmodels cross-checks + Blaker's two theorems
  (test count 164→201). Plotly layer also gained exact/midp/bayes/jeffreys/blaker. `docs/bayesian_toolbox.md`
  added (1.8). R→Python mapping page already complete.
- **➡️ ACTIVE GOAL (set 2026-07-25): the docs content-depth initiative** — the docs *structure* is
  settled (Furo theme, five collapsible sidebar groups; edit-button removed), but the *content* is thin
  in specific places (the `theory/` "Methods & Mathematics" track is one page; `foundations/` is thin;
  no tutorials/cookbook/FAQ; the unusual metrics get a paragraph each). **READ `planning/DOCS_CHECKLIST.md`
  FIRST** — the detailed actionable checklist (local preview via sphinx-autobuild, the `-W` build gate,
  per-page done-definition, the MyST-NB executable-page front matter, a page-by-page status table, and
  the granular T1–T5 backlog); higher-level rationale in `planning/DOCS_CONTENT_PLAN.md`. **Infra DONE:**
  Furo + collapsible sidebar + edit-button removed + **executable MyST-NB docs**.
  **Content progress (2026-07-25 docs rebuild):** **T2 Foundations series DONE** — `foundations/index`
  rewritten as a landing hub over five new *executable* beginner pages (`01_proportion`, `02_binomial`,
  `03_sampling_variability`, `04_confidence_interval`, `05_coverage`), each ending in a "Check yourself"
  quiz. **T1 theory** grew by `theory/03_test_inversion.md` (Wilson score + LR as test inversion),
  `theory/04_exact_and_discreteness.md` (CP/Mid-P/Blaker, discreteness, acceptability γ(x,θ)),
  `theory/05_transformed_intervals.md` (delta method; arcsine's constant variance + ZWI boundary collapse;
  logit/expit), `theory/06_bayesian_view.md` (Beta conjugacy, priors, credible vs confidence, Jeffreys'
  frequentist coverage) and `theory/07_coverage_theory.md` (mean vs min coverage, oscillation persistence,
  one-/two-sided, h & c repairs — the capstone). Glossary +`hypothesis test`, +`discreteness`,
  +`conjugate prior`. Nine matplotlib figures (dataviz palette). **Full `-W` build confirmed clean.**
  Docs-only changes awaiting the user's manual push (§7). **✅ T1 THEORY TRACK COMPLETE (7/7 pages)** —
  every method page's "Deeper maths → theory" now resolves.
- **✅ T3 TUTORIALS/COOKBOOK COMPLETE (2026-07-25):** new `docs/tutorials/` group — `index` hub +
  `ab_test`, `quality_control`, `zero_events`, `choosing_a_method`, `cookbook` (all executable) + a
  `:caption: Tutorials` toctree group and homepage card. Three new figures (`tutorial_{ab,qc,zero}.png`);
  glossary +`sampling variability`. **Full `-W` build confirmed clean.**
- **✅ T4 + T5 DONE (2026-09-01) — docs content-depth initiative essentially complete.**
  - **T4 method pages (all 9):** each `docs/methods/*.md` gained a *Worked example — n = 5, x = 3*
    executable cell that reproduces the shipped limits from `scipy`/`numpy` (closed forms for
    Wald/Wilson/ArcSine/Logit; Satterthwaite ν for Wald-T; `brentq` root-finds for LR and Blaker's
    acceptability γ; Beta quantiles for Exact/Bayes) and confirms against `bk.ci`, plus an
    *Interpretation & pitfalls* admonition. Pages are now executable (jupytext front matter added).
  - **T4 `evaluating_intervals.md`:** fully rewritten & executable — a Monte-Carlo coverage sim
    (Wald 0.877 vs Wilson 0.956 at θ=0.1), and p-confidence/p-bias/error derived from first principles
    and reproduced from `scipy` (match `pcopbiwd`/`errwd` exactly) + new `evaluating_tradeoff.png`
    (2-panel coverage vs length, Okabe–Ito palette) + a quiz.
  - **T5:** new `docs/faq.md` (troubleshooting Q&A) and `docs/comparison.md` (binomcikit vs
    scipy/statsmodels/R, proving matching numbers for Wald/Wilson/CP/Jeffreys + a when-to-use matrix).
    Both wired into the Guides toctree + homepage cards. Glossary +`p-value`.
  - **Build note (important):** locally the `-W` build must run with **`PYTHONPATH=../src`** so the
    MyST-NB kernel can import binomcikit (conf.py's `sys.path` only reaches the Sphinx process, not the
    kernel subprocess); RTD is unaffected (`pip install .`). See `DOCS_CHECKLIST.md §1`.
  - **Still open (optional):** T4 concept-explainer hub (largely covered by `theory/`); annotated refs
    with DOIs; a `dataviz` styling pass. These are polish, not blockers.
  - **Docs-only; awaiting the user's manual push (§7).**
- **➡️ NEXT: nothing committed remains in Phase 1's method/feature list, and the `cilrx`/`cialr` bug is
  now fixed too (§1 "Known issues" — one low-severity Blaker edge case remains open).** What's left is
  cross-cutting polish (below) + Phase-0 relicense. Check in with the user before picking one — they
  asked for bootstrap/p-value-tests/sample-size "one by one" and to stop after that list; the LR bug fix
  and audit were a separate, explicit follow-up request, not an invitation to keep going unprompted.

### Remaining Phase-1 work
- ~~**1.10 Bootstrap**~~ ✅ **DONE 2026-09-28** (see §1 above) — previously deferred 2026-07-24 for
  lacking an oracle; the user explicitly accepted that risk for `kind="smooth"` and asked for it
  cross-checked as rigorously as possible instead of skipped. `kind="percentile"`/`"bca"` are fully
  oracle-verified (scipy).
- ~~**1.11 Frequentist p-value tests**~~ ✅ **DONE 2026-09-28** (see §1 above) — **correction to this
  doc's own prior plan:** ROADMAP §3.5 called `scipy.stats.binomtest` "the oracle", but its default
  two-sided p-value uses a different convention (minlike) than the equal-tailed CI-duality construction
  this doc's own rationale calls for (§3.5's "θ₀ rejected exactly when outside the interval"). Verified
  against the correct closed-form + one-sided-tail + duality-property checks instead — see §1.
- ~~**1.12 Sample-size / power**~~ ✅ **DONE 2026-09-28** (see §1 above) — also surfaced the `cilrx`
  large-n bug noted above, purely incidentally (stress-testing the search range).
- ~~**Access / usability layer**~~ ✅ **DONE 2026-07-24** (see §1). `point_estimate` gained the `"mue"`
  variant with 1.10 (see §1). Still open from ROADMAP §3.5 (optional): `point_estimate` "shrinkage"
  variant; aggregator extension (add Blaker/Bootstrap to `ciall`/`covpall`/… — skipped so the R-mirror
  set stays intact); empirical-Bayes / prior-sensitivity conveniences.
- **Cross-cutting / polish:** ~~finalize + rebuild docs~~ ✅ DONE (clean `-W` build); **type hints** —
  public surface + `py.typed` ✅ DONE, internal grid functions still unhinted (incremental); resolve the
  two open ROADMAP §10 decisions (plotnine→plotly retirement; numba default); deferred Phase-0 items
  (A creds rotation, B README ArcSine `sin²(φ)` fix, C GPL-3→GPL-2 relicense).
- **Then:** Phase 2 Streamlit app · Phase 3 PyQt `.exe` · Phase 4 paper rewrite. (Two-proportion
  inference is a SEPARATE sequel package, not part of binomcikit.)
- Done infra: `ci()` dispatcher, vectorized metric engines, optional numba `[fast]` accel, optional
  plotting (`plotnine`→`plotly` layer started), CI + Trusted-Publishing, docs scaffold + `under_the_hood`.

## 2. Sanity-check the repo (run these first in a new session)
From the repo root (`…/binomcikit`):
```bash
python -m pytest -q                 # expect: 302 passed (grows as methods add tests; ~5 min — the
                                     # pvalue/sample_size/power tests exercise root-finding methods
                                     # (exact/LR/Blaker) repeatedly by design; see their docstrings)
python -m ruff check src tests      # expect: All checks passed!
python -m black --check src tests   # expect: no changes
python -c "import sys;sys.path.insert(0,'src');import binomcikit as b;print(b.__version__, len(b.__all__))"
```
Docs build check (optional): `cd docs && python -m sphinx -b html . _build/x -q && cd .. && rm -rf docs/_build/x`
**Environment:** Windows; PowerShell + Bash tools. For direct imports use `PYTHONPATH=src` (pytest
already sets it). Installed here: numba, plotly, kaleido, hypothesis, statsmodels, sphinx.
**Git push: no longer assumed blocked (corrected 2026-09-28).** Earlier sessions assumed Git Credential
Manager blocks the assistant from pushing and always handed the user a manual upload block (§7). That
assumption was never actually re-tested until 2026-09-28, when the user explicitly asked the assistant
to push directly — `git push origin main` worked with no credential prompt or error. Default to pushing
directly when the user asks for it; §7's manual block is still there as a fallback if push ever does
fail in a given environment.

## 3. Read these for context (in order)
1. **this file**
2. `planning/ROADMAP.md` — the plan: **§3** sub-phases + **§3.2** the per-sub-phase workflow +
   **§3.5** functions-to-add + **§4** docs architecture + **§5–7** engineering contract + **§10** open decisions.
3. `planning/RESEARCH.md` — the science: **§6** per-method math + origin papers + refs; Tables 3.1/3.2.
4. `docs/under_the_hood.md` — the technical machinery (test oracles, numba, extras, CI).
5. `docs/methods/wald.md` — **the template every method page copies.**

## 4. How to do a method sub-phase (the recipe)
**Easiest: invoke the `binomcikit-subphase` skill** — it runs this exact recipe (audit → docs →
figure → verify → log → upload). The steps below are the same thing, written out as a fallback.
Run the workflow from ROADMAP §3.2. Concretely, per method (using Wald as the worked example):
1. **Audit R↔Py** — the port is complete, so usually just *confirm* the method's functions exist and
   match the oracles (base already tested vs `statsmodels`/paper golden). Note structural facts
   (LR has no CC; Exact/Bayes have no adj/cc).
2. **Functions** — confirm the full grid + dispatcher entry; add only what's genuinely missing
   (see ROADMAP §3.5 for the access-layer additions like curve accessors, `recommend`, `compare`).
3. **Perf** — closed-form methods need nothing; metrics already use the numba-accelerated engine.
4. **Docs (the real deliverable)** — see §5 below.
5. **Verify** — the §2 commands all green.
6. **Log + wire** — update `docs/under_the_hood.md` if new tests/accel; add a method-selection row.
7. **Update this file's §1 + §7**, then hand to the user to upload.

## 5. The per-method docs deliverable (copy Wald's structure)
For method `<m>` (e.g. wilson):
- **Create `docs/methods/<m>.md`** — copy the two-core structure of `docs/methods/wald.md`:
  *Use it* (call/params/returns/examples/recipes/gotchas) + *Understand it* (intuition → formula
  with **every symbol a `{term}` glossary link** → dropdown derivation → when-it-works/fails →
  references). End with a "Terms used" box.
- **Add new glossary terms** to `docs/glossary.md` (inside the `:::{glossary}` block), each defined
  plainly with a tiny example, cross-linked with `{term}`.
- **Generate its figure:** `python -c "import sys;sys.path.insert(0,'src');import binomcikit as b;
  b.plot_coverage(n=20,methods=['wald','<m>']).write_image('docs/_static/<m>_coverage.png',width=820,height=460,scale=2)"`
  then embed with a `{figure}` directive.
- **Wire it in:** add `<m>` to the toctree in `docs/methods/index.md`; add a row to
  `docs/method_selection.md`.
- **Confirm the docs build is clean** (no undefined `{term}`, no broken links).

## 6. Order of sub-phases — ALL DONE
1.2 Wilson → 1.3 ArcSine → 1.4 Logit → 1.5 Wald-T → 1.6 LR (no CC) → 1.7 Exact/Mid-P →
1.8 Bayesian (+6xx toolbox) → 1.9 **Blaker (new)** ✅ → 1.10 **Bootstrap (new)** ✅ → 1.11 **p-value
tests** ✅ → 1.12 **sample-size/power** ✅. (1.9/1.10/1.11/1.12 built new code beyond the R port;
RESEARCH §9 has the Blaker/Bootstrap constructions.) Every committed Phase-1 method/feature is done as
of 2026-09-28, and the `cilrx`/`cialr` large-n bug found along the way is fixed too — what's left is
cross-cutting polish (§1) and the low-severity Blaker extreme-alpha edge case (§1 "Known issues").

## 7. When a sub-phase is done — commit + push
Per §2's correction, the assistant can push directly when asked — no longer assumed blocked. Default
flow (commit only when the user asks; push only when the user asks, per this repo's normal git-safety
rules, same as any other repo):
```bash
git status                 # sanity: the copyrighted PDF must NOT appear (it's gitignored)
git add -A
git commit -m "Sub-phase 1.x (<method>): <one-line summary>"
git push origin main
```
- **Never commit** `previous-work/*.pdf` (copyright) — now covered by `.gitignore` (`*.pdf`).
  Build artifacts (`docs/_build/`, `dist/`, `__pycache__`, caches) are already ignored.
- The **first** upload (this session: 1.0 + 1.1) is large; later sub-phases add only a handful of files.

## 8. Open decisions (ROADMAP §10) — current stance
- **Plotting completeness:** *interim accepted* — the new Plotly `plot_ci`/`plot_coverage` are each
  method's plotting deliverable; the legacy plotnine `plot*` functions get retired in one later batch.
- **numba default:** *layered* — library keeps numba optional; the Streamlit app & PyQt exe (Phase
  2/3) ship lock files that pin `[fast]`. `[fast]` has a graceful `python_version < '3.14'` marker
  (**bump that bound** when numba supports a newer Python).
- **Type hints / `py.typed`:** deferred to one incremental pass (not per-method).
