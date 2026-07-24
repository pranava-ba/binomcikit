---
name: binomcikit-subphase
description: >-
  Runs one binomcikit Phase-1 method sub-phase end to end (Wilson, Agresti–Coull, ArcSine, Logit,
  Wald-T, Likelihood-ratio, Exact/Mid-P, Bayesian, and the new Blaker / Bootstrap): orient from
  planning/CONTINUE_HERE.md, audit the method against its oracles, confirm/add functions, write the
  two-core docs page by copying docs/methods/wald.md, add glossary terms, generate a plot_coverage
  figure, verify (pytest/ruff/black/docs build), update the handoff log, and produce the GitHub
  upload block. USE THIS SKILL whenever the user is working in the binomcikit repo and asks to start,
  continue, do, or finish a method sub-phase or a specific method (e.g. "start 1.2 Wilson", "do
  ArcSine", "next sub-phase", "continue binomcikit", "finish Bayesian"), even if they don't name the
  skill. Being in the binomcikit project on Phase 1 is itself a strong signal to use it.
---

# binomcikit — run a method sub-phase

You are executing one **Phase-1 method sub-phase** of **binomcikit** (a Python port of the R
`proportion` package). Take one method — Wilson, ArcSine, Logit, Wald-T, LR, Exact/Mid-P, Bayesian,
or the new Blaker / Bootstrap — from audit to *documented, verified, and ready to upload*, following
the template Wald established. Docs are a hard gate: a sub-phase is not done until its two-core page,
glossary terms, and figure exist and the docs build is clean.

## 0. Orient first
Read **`planning/CONTINUE_HERE.md`** — it has the current state (which sub-phase is NEXT), the
conventions, and the verify commands. Then read only what you need:
- `planning/ROADMAP.md` — §3 sub-phases, §3.2 workflow, §3.5 functions-to-add, §4 docs architecture,
  §5–7 engineering contract, §10 open decisions.
- `planning/RESEARCH.md` — §6 for this method's math + origin paper + reference number `[n]`;
  **§9 for the Blaker / Bootstrap constructions** (needed only for 1.9 / 1.10).
- `docs/methods/wald.md` — the page template you will copy.
- `docs/under_the_hood.md` — the technical log to keep current.

## 1. Sanity-check the starting point (must be green before you change anything)
From the repo root:
```bash
python -m pytest -q               # expect all passing (164+, grows per sub-phase)
python -m ruff check src tests    # All checks passed!
python -m black --check src tests
```
Windows environment; for direct imports use `PYTHONPATH=src` (pytest already sets it). numba, plotly,
kaleido, hypothesis, statsmodels, sphinx are installed in dev.

## 2. Audit (R ↔ Python)
The port is complete, so usually **confirm** rather than write: the method's functions already exist
and the base is oracle-tested (vs `statsmodels` and the paper's golden values). Record the structural
facts — LR has no continuity-corrected variant; Exact & Bayesian have no adjusted/CC variants.
**New methods (Blaker 1.9, Bootstrap 1.10) are the exception:** you must build the limit-producer and
its family grid from the construction in RESEARCH §9, then register it so the shared metric engine
(`covp*/length*/pcopbi*/err*`) picks it up automatically — never reimplement metrics per method.

## 3. Functions
Confirm the full grid (base + given-x, adjusted, CC where applicable, plots, and the four metric
families) plus the `ci()` dispatcher entry. Add only what is genuinely missing; the planned
access-layer additions (curve accessors, `recommend`, `compare`, …) are in ROADMAP §3.5 — add those
deliberately, not by reflex.

## 4. Documentation — the real deliverable (copy Wald)
Create **`docs/methods/<method>.md`** mirroring `docs/methods/wald.md`'s two cores:
- **Use it** — import; each parameter in plain + formal terms; the return schema; a tiny worked
  example; recipes (including `bk.plot_ci` / `bk.plot_coverage`); gotchas.
- **Understand it** — plain intuition *first* (a coin-flip story), then the formula with **every
  technical symbol written as a `{term}` glossary link**, a `:::{dropdown}` derivation, when-it-works
  / when-it-fails, and the reference `[n]` from RESEARCH §11. End with a "Terms used" admonition.

Add any new technical words to **`docs/glossary.md`** (inside the `:::{glossary}` block), each defined
plainly with a tiny example and cross-linked with `{term}`. Write for someone who has *not* learned
basic probability — progressive disclosure, hand-checkable numbers. Consider invoking the **`dataviz`**
skill for figure quality.

## 5. Figure
Generate the method's coverage comparison and embed it:
```bash
python -c "import sys;sys.path.insert(0,'src');import binomcikit as b; b.plot_coverage(n=20, methods=['wald','<method>']).write_image('docs/_static/<method>_coverage.png', width=820, height=460, scale=2)"
```
Embed with a MyST ```` ```{figure} ```` directive (see wald.md). Choose the comparison that tells the
method's story (e.g. Wilson hugging the nominal line where Wald sagged).

## 6. Wire + log
- Add `<method>` to the toctree in `docs/methods/index.md`; add a row to `docs/method_selection.md`.
- Fix any placeholder references to this method elsewhere (e.g. Wald's "documented in sub-phase 1.x").
- Update `docs/under_the_hood.md` if the sub-phase added tests, an acceleration, or a golden fixture.

## 7. Verify (everything green)
```bash
python -m pytest -q ; python -m ruff check src tests ; python -m black --check src tests
cd docs && python -m sphinx -b html . _build/x -q && cd .. && rm -rf docs/_build/x   # expect clean
```
Add tests for any new code (oracle/golden + Hypothesis property; `seed=` if stochastic). **Run the
code review once, by default** — perform the review inline yourself (do not ask first; `/code-review`
local isn't assistant-invokable and `ultra` is user-triggered). Run `security-review` before any
public release.

## 8. Finish — update the log and hand off
- Update `planning/CONTINUE_HERE.md` §1: mark this sub-phase done, set NEXT to the following one.
- Update `CHANGELOG.md` `[Unreleased]` and the project memory (the goals-and-JOSS note).
- Confirm work is push-ready: `git status` must **not** list the copyrighted PDF (`previous-work/*.pdf`,
  gitignored). **Do NOT print git/upload commands** — the user pushes manually and will ask for the
  commands when they want them (per [[workflow-preferences]]). Just report the done/verified state.

## Principles
- Reuse the shared engine; match the surrounding code/doc style; keep it lean (YAGNI).
- One method, fully finished (code + docs + figure + green build), then stop and hand off — so each
  chat stays self-contained and the next session can continue from `CONTINUE_HERE.md`.
