# CONTINUE HERE — session handoff (read this first)

> **New chat?** Read this page top to bottom and you're oriented. It is the single source of
> "where we are, how to continue, how to verify, what to upload." **Update the "Current state" and
> "Upload" sections at the END of every sub-phase** so the next session starts clean.

---

## 1. Current state — updated 2026-07-24
- **Version:** 3.0.8 (pre first real PyPI release; PyPI still has an old 0.0.5).
- **Tests:** **209 passing**; `ruff` + `black` clean; **Sphinx docs build clean with `-W` (warnings-as-errors)**.
- **Phase 1 progress:** 1.0 infra · 1.1 Wald · 1.2 Wilson · 1.3 ArcSine · 1.4 Logit · 1.5 Wald-T · 1.6 LR · 1.7 Exact/Mid-P · 1.8 Bayesian+6xx · 1.9 **Blaker (NEW method)** · **access layer + docs finalize + typing DONE**.
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
- **➡️ NEXT: user to choose** from the remaining work below (menu presented 2026-07-24).

### Remaining Phase-1 work (nothing here is started)
- **1.10 Bootstrap — ⏸️ DEFERRED to future/to-do (user decision 2026-07-24).** The Wang–Hutson smooth
  bootstrap (RESEARCH §9.2) is under-specified in our notes (median-unbiased estimator + mean→π
  cubic-spline inversion) **and has no oracle in this environment**, so building it correctly is risky.
  Revisit when an R/reference oracle is available (`PropCIs`/`bootstrap`), or scope to the well-defined
  parametric/percentile/BCa variants. Needs the `from_counts`/`from_data` access layer + a
  median-unbiased `point_estimate` first.
- **1.11 Frequentist p-value tests** (NEW code) — `binom_test`-style two-sided p-values per method
  (CI–test duality; committed 2026-07-23, ROADMAP §3.5). Verifiable vs `scipy.stats.binomtest`.
- **1.12 Sample-size / power** (NEW code) — CI-width / power planning functions (committed; ROADMAP §3.5).
- ~~**Access / usability layer**~~ ✅ **DONE 2026-07-24** (see §1). Still open from ROADMAP §3.5 (optional):
  `point_estimate` "mue"/"shrinkage" variants (mue needs the deferred bootstrap); aggregator extension
  (add Blaker to `ciall`/`covpall`/… — skipped so the R-mirror set stays intact); empirical-Bayes /
  prior-sensitivity conveniences.
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
python -m pytest -q                 # expect: 164 passed (grows as methods add tests)
python -m ruff check src tests      # expect: All checks passed!
python -m black --check src tests   # expect: no changes
python -c "import sys;sys.path.insert(0,'src');import binomcikit as b;print(b.__version__, len(b.__all__))"
```
Docs build check (optional): `cd docs && python -m sphinx -b html . _build/x -q && cd .. && rm -rf docs/_build/x`
**Environment:** Windows; PowerShell + Bash tools. For direct imports use `PYTHONPATH=src` (pytest
already sets it). Installed here: numba, plotly, kaleido, hypothesis, statsmodels, sphinx.
**Git push is blocked for the assistant** (Git Credential Manager) — the **user pushes manually** (§7).

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

## 6. Order of remaining sub-phases
1.2 Wilson → 1.3 ArcSine → 1.4 Logit → 1.5 Wald-T → 1.6 LR (no CC) → 1.7 Exact/Mid-P →
1.8 Bayesian (+6xx toolbox) → 1.9 **Blaker (new)** → 1.10 **Bootstrap (new)** → 1.11 tests →
1.12 sample-size. (1.9/1.10 build new code; RESEARCH §9 has the constructions.)

## 7. When a sub-phase is done — upload to GitHub (the USER runs this)
The assistant cannot push (credential manager). Copy-paste, then push:
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
