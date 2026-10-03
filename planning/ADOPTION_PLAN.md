# Improving binomcikit's adoption signals — plan

> 2026-10-01. Answers: *"how do we improve our adoption signals?"* Everything outward-facing (publishing, filing
> issues, submitting to a journal) is **listed for you to decide — nothing in this plan has been done on your behalf.**
> What is marked ✅ is repository work already completed in this session.

## 0. Where the signals stand today

| Signal | Today | Note |
|---|---|---|
| PyPI release | **3.0.8 is not released** (PyPI still serves an old 0.0.5) | the single biggest gap: nobody can `pip install` the real package |
| Size / maturity | ≈ 13 k LOC source, 96 doc pages, 721 tests, CI on 3 OSes × 5 Pythons; 68 commits since Jan 2025 | solid for JOSS's "substantial scholarly effort" bar |
| Citation | `CITATION.cff` present; **no Zenodo DOI**; no conda-forge package | |
| Licence | GPL-3.0 | inherited from the GPL R package it ports; a real friction for corporate users (see §6) |
| Visibility | no benchmarks page, no comparisons that third parties can verify | ✅ both now exist (below) |
| Incumbents | `statsmodels` ≈ 40 M downloads/month, `scipy` ≈ 367 M ([PyPI Stats](https://pypistats.org/packages/statsmodels), [pepy](https://pepy.tech/project/scipy)) | we will not displace them; the niche is *decision support and evaluation* |

**Positioning that survives scrutiny** (the earlier "first in Python" claim does not — `DBCI` ships 16 methods): *the only tool that
puts classical + exact + Bayesian + betting intervals, an evaluation layer, and PASS/SAS-style planning under one roof, with each
method verified against an independent oracle.* Lead with that and with the **verification record**, not with a method count.

## 1. Credibility assets built in this session ✅

These are the things a sceptical statistician checks first; each is now concrete and reproducible.

| Asset | Where | Why it moves signals |
|---|---|---|
| **Verification record** — PASS Chapter 115 (15/15 published sample sizes), Garthwaite et al. Tables A1/A2 (540/540 limits), Dümbgen's worked example, Thulin Table 1 + example, confseq (1e-16) | `docs/methods/extended.md`, `planning/MISSING_METHODS.md` | "verified against X" is what gets a package cited in methods papers |
| **Reproducible benchmarks** vs statsmodels, scipy, astropy, DBCI, pynomial, binoculars, confseq (with parity columns) | `benchmarks/bench_competitors.py`, `benchmarks/RESULTS.md`, `docs/benchmarks.md` | a number people can re-run and quote |
| **Defects found in other packages**, each with a minimal repro in a test | DescTools Pratt/Witting; DBCI modified-Wilson/Pratt/Witting/Blaker tolerance | the basis for goodwill upstream issues (§2.4) |
| **A real correctness fix in our own code** (Blaker's inner-crossing bug) with regression tests | `tests/test_blaker.py`, CHANGELOG | shows the verification culture is real |
| **Industry use-case page** with the products people use today | `docs/use_cases_by_industry.md` | gives each industry a reason to try it |
| **PASS/SAS planning layer** | `docs/planning.md` | converts "I use PASS/SAS for sample size" users |
| Faster than every loop-based package (tens to thousands ×, equal answers); `bk.interval()` is 2–6 µs; *not* faster than statsmodels/astropy through `bk.ci()` for closed-form methods (lean path is) | `docs/benchmarks.md` | removes the "it's slow" objection |

## 2. Prioritised actions (you decide; effort in working days)

### 2.1 Ship it — highest impact, ~1 day
1. **Release 3.1.0 to PyPI** (the tests are green; update version in `pyproject.toml`, `CITATION.cff`, `docs/conf.py`, `__init__`). Use Trusted Publishing from GitHub Actions; build an sdist + universal wheel.
2. **Zenodo DOI**: connect the GitHub repo to Zenodo, cut a GitHub release → a citable DOI; put the DOI badge in the README and `CITATION.cff`.
3. **conda-forge feedstock** (a recipe PR to `staged-recipes`): reaches Anaconda users and gives download stats.
4. README: lead with the verification record + benchmark table (screenshots of `RESULTS.md`'s headline rows), and the three-line install/use.

### 2.2 Credibility via review — ~1–3 days of effort, weeks of calendar
5. **pyOpenSci software review** → if accepted and in scope, **fast-tracked through JOSS** ([pyOpenSci–JOSS partnership](https://pyopensci.discourse.group/t/isabel-zimmerman-pyopenscis-winter-2024-software-peer-review-editor-in-chief/430)).
   JOSS's bar ([submission guide](https://joss.readthedocs.io/en/latest/submitting.html)): ≥ ~3 months of work, >1000 LOC, feature-complete, a research application, *not* a "minor utility".
   **Scope risk is real:** `binomial_cis` (a much smaller package) was closed at pre-review as "uncertain scope". binomcikit's defence is exactly what this session built — a *method-comparison and verification platform* with new methods, a published-oracle record and planning tools — so the paper must say so explicitly.
6. **Update `paper.md`**: (a) replace "first in Python" with the three-layer claim; (b) cite DBCI/binomial_cis/confseq honestly; (c) add the 34 methods, the verification table, the benchmark, and the Blaker finding (a *new result*: the standard single-root search can return an interior crossing and under-cover). Consider also an **arXiv (stat.CO) preprint** of that content.

### 2.3 Content people actually find — ~3–5 days
7. **Three short posts** (each a notebook with "Open in Colab"):
   * *"Your 95% interval isn't 95%"* — Wilson is not locally correct; the Blaker bug story; `bk.locally_correct`.
   * *"Stop peeking: anytime-valid intervals in 20 lines"* — the peeking experiment from `docs/methods/betting.md`.
   * *"Replicating PASS and SAS PROC POWER in Python"* — the 15/15 table.
8. **Answer existing questions** where the audience already is: Cross Validated / Stack Overflow ("Wilson vs Clopper–Pearson in Python", "binomial CI for zero events", "A/B test peeking"), linking the relevant doc page. Disclose affiliation.
9. **Newsletters / venues:** PyCoder's Weekly, Python Weekly, Scientific Python newsletter, a SciPy-conference lightning talk.

### 2.4 Constructive upstream engagement — ~1 day (needs your approval)
10. File **minimal-repro issues**: `DescTools::BinomCI` (`pratt` lower limit drifts up to 0.126 from exact CP at n=20; `witting` uses α not α/2 per tail), `DBCI` (`modified-wilson` upper limit lacks `1 −`; `pratt`; `witting`; Blaker's 1e-5 stepping). Link the tests. This both helps them and is the best advertisement for the verification culture.
11. Offer `statsmodels`/`scipy` documentation "See also" cross-references (they will rarely accept new methods; a doc link costs them little).

### 2.5 Niches with a built-in audience — ~2–3 days each
12. **LLM / ML evaluation:** a short integration snippet for the common eval harnesses (a `ci` helper using `bk.interval`) and an issue/PR offering it. The existing tutorial + `cibetseq` for growing leaderboards are the hook ([relevant paper](https://arxiv.org/pdf/2503.01747)).
13. **A/B testing & experimentation:** a "bring your own conversion counts" notebook comparing a fixed-n interval to the confidence sequence under peeking.
14. **Regulated industries / QC:** a one-page "zero-failure and success-run plans" guide (`sample_size_upper_bound`) — a frequently Googled question.

## 3. Engineering signals (cheap, compounding)

| Item | Detail |
|---|---|
| Raise branch coverage from 65% → 80% | the legacy plotnine `*_graph.py` modules (4–8%) are slated for retirement; excluding them lifts the number honestly |
| Contribution scaffolding | `CONTRIBUTING.md`, issue/PR templates, `CODE_OF_CONDUCT.md`, GitHub Discussions, 5–10 labelled *good first issues* (e.g. "add a method from `MISSING_METHODS.md` §7") |
| Automation | Dependabot, pre-commit (ruff/black), a **scheduled benchmark workflow** that fails on a >2× regression |
| API stability policy | document SemVer, deprecation window; mark `bk.ext.*` as stable-API |
| Typing | complete the hints on the internal grid functions; run `mypy` in CI |
| Security | run the `security-review` pass before the first public release |
| Docs | search, an "Edit on GitHub" link, a changelog page in the nav, per-industry landing pages (the use-case page is the seed) |

## 4. Measure it

| Metric | Source | Cadence |
|---|---|---|
| Downloads | [pepy.tech](https://pepy.tech), PyPI Stats, conda-forge | weekly |
| Stars / forks / unique clones | GitHub Insights | weekly |
| Citations | OpenAlex alerts for the 2017 SoftwareX paper and ours | monthly |
| Docs traffic & top pages | Read the Docs analytics | monthly |
| Dependents | GitHub dependency graph / libraries.io | monthly |
| Issues opened by *others* | GitHub | monthly |

Set targets only after the first release gives a baseline; a plausible first-year aim for a niche statistics package is hundreds of monthly downloads and a handful of citations — not parity with `statsmodels`.

## 5. Sequencing (suggested)

1. **Week 1:** release 3.1.0 + Zenodo DOI + README rewrite (§2.1). Run the benchmark workflow once in CI.
2. **Weeks 2–3:** paper update, pyOpenSci submission (§2.2); the three notebooks (§2.3).
3. **Weeks 3–5:** upstream issues (with your sign-off), forum answers, newsletter pitches.
4. **Ongoing:** engineering signals (§3); pick **one** niche (§2.5) — LLM-eval is the best fit — and go deep rather than wide.

## 6. Decisions that are yours

* **Licence.** GPL-3.0 is inherited from the GPL R package binomcikit ports, so the ported code cannot simply be relicensed. A permissive licence would require either the original authors' consent or a clean-room rewrite of the ported parts; the new code in `ext/`, `planning.py`, `limits.py` is original and could be dual-licensed *only* if it can be separated from the GPL-derived modules (legal advice recommended). Until then, say plainly in the README what GPL means for users.
* **Whether to build the Streamlit app** (`planning/ROADMAP.md` §10.3). Adoption data should decide; a hosted playground is a strong *discovery* channel but adds maintenance. Defer until the 3.1.0 baseline exists.
* **Naming/positioning** of the extended-methods claim (the three-layer sentence above).
