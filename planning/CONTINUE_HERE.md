# CONTINUE HERE — session handoff (read this first)

> **New chat?** Read this page top to bottom and you're oriented. It is the single source of
> "where we are, how to continue, how to verify, what to upload." **Update the "Current state" and
> "Upload" sections at the END of every sub-phase** so the next session starts clean.

---

## 1. Current state — updated 2026-07-23
- **Version:** 3.0.8 (pre first real PyPI release; PyPI still has an old 0.0.5).
- **Tests:** **164 passing**; `ruff` + `black` clean; Sphinx docs build clean.
- **Phase 1 progress:** 1.0 infrastructure **DONE** · 1.1 **Wald DONE**.
- **➡️ NEXT: Sub-phase 1.2 — Wilson (Score).**
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
