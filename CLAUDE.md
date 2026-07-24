# CLAUDE.md — binomcikit project instructions

binomcikit is a Python port of the R `proportion` package (single binomial-proportion inference:
confidence intervals + evaluation metrics + Bayesian tools). Four goals: **PyPI → Streamlit → PyQt
exe → journal paper.** We are in **Phase 1**, building it out **one method sub-phase at a time**.

## Start every session here
1. **Read `planning/CONTINUE_HERE.md` first** — the current state, the next sub-phase, sanity-check
   commands, conventions, and the manual GitHub-upload steps.
2. Run the sanity checks it lists (`pytest` / `ruff` / `black` / docs build) before changing anything.

## Doing a method sub-phase → use the skill
For any Phase-1 method work — start / continue / finish a method (Wilson, ArcSine, Logit, Wald-T,
LR, Exact/Mid-P, Bayesian, Blaker, Bootstrap) — **invoke the `binomcikit-subphase` skill.** It
encodes the full recipe: audit → functions → two-core docs → figure → verify → log → upload. Copy
`docs/methods/wald.md` as the docs template.

## Conventions (full detail in `planning/ROADMAP.md` §5–7)
- **Docs are a hard gate.** Every method needs a two-core page (*Use it* / *Understand it*) with
  every technical term linked to `docs/glossary.md`, plus a coverage figure; the docs build must be clean.
- **Reuse the shared metric engine** — never reimplement `covp*/expl*/pconf*/err*` per method.
- **Performance:** numpy core; optional `[fast]` numba for large-n (benchmarked — no compiled-language
  rewrite). **Plotting:** optional; Plotly (`plot_ci` / `plot_coverage`) is the forward path.
- **Quality:** `ruff` + `black` clean; tests = oracle (`statsmodels`) + golden (paper/R) + Hypothesis
  property + completeness. Run `/code-review` per sub-phase; `security-review` before public release.
- **Figures / dashboards:** consider the `dataviz` skill for quality.
- **Git:** the assistant cannot push (Git Credential Manager) — give the user the upload block; never
  commit `previous-work/*.pdf` (copyright; gitignored).

## The science & the record
`planning/RESEARCH.md` — per-method math + origin papers + refs (§6), competitive/novelty analysis,
and the Blaker / Bootstrap / betting constructions (§8–9). `docs/under_the_hood.md` — the technical log.
