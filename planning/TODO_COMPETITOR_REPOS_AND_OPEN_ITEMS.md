# TODO (not started): competitor-repo deep dive, and everything still open

> Written 2026-10-01 at the user's request. **Section 1 was carried out on 2026-10-03: see `planning/COMPETITOR_REPOS.md` (not done: dependents/libraries.io/citations, R-only packages other than DescTools, commercial tools, large-n 10^5-10^6 speed runs, extra-language oracle checks).** Section 2 collects every open item
> from the 2026-10-01 session so none is lost.

## 1. Competitor repository deep dive (planned)

**Goal:** clone every comparable package from GitHub (DBCI first), measure how alive and used each one is, run a SWOT on each,
and turn the weaknesses into concrete improvements for binomcikit.

### 1.1 Scope: the packages to clone

| Package | Notes |
|---|---|
| DBCI (`diff_binom_confint`) | the closest competitor (16 methods); first priority |
| `binomial_cis` | closed at pyOpenSci pre-review as "uncertain scope" |
| `pynomial` | PyPI name is a different package; locate the right GitHub repo |
| `binoculars` | its "wilson" is not identical to standard Wilson (parity 6e-7 to 2e-6) |
| `confseq` | betting/confidence sequences; pip build failed here |
| `statsmodels` (`proportion_confint`) | clone only the relevant modules, not the whole repo |
| `astropy.stats` (binom_conf_interval) | same |
| `scipy.stats` (`binomtest`, `proportion_ci`) | same |
| R/other-language references (`proportion`, `binom`, `DescTools::BinomCI`, `exactci`, `binGroup`) | for oracles and defects; not Python competitors |
| Anything else found by searching GitHub topics (`binomial-proportion`, `confidence-interval`, `clopper-pearson`, `wilson-score`) | catalogue before cloning |

Use `gh` / git clones into a scratch directory outside the repo (never commit the clones). Pin the commit SHA and date of each clone.

### 1.2 Activity and usage log (per repo, with date measured)

* Commit history: first/last commit, commits in last 12 months, release cadence, tags, median days between releases.
* Contributors: count, bus factor (share of commits by top contributor), issue/PR response time, open vs closed issues, stale PRs.
* Usage: stars, forks, watchers, GitHub dependents, PyPI/conda downloads (pepy, PyPI Stats, BigQuery if needed), reverse
  dependencies (libraries.io), citations (OpenAlex/Google Scholar), mentions in Stack Overflow/Cross Validated.
* Health: CI status, test count and coverage, supported Python/numpy versions, licence, last supported-Python bump, deprecation warnings on current Python.
* Record everything in a dated table (`docs/` or `planning/`) with the exact query/command used so it can be re-run.

### 1.3 Technical measurements (run, don't assume)

* **Methods:** list of intervals offered; for each, check against our oracles and published tables; log every defect with a minimal repro (known so far: DBCI modified-Wilson, Pratt, Witting, Blaker 1e-5 stepping; DescTools Pratt/Witting).
* **Speed:** extend `benchmarks/bench_competitors.py` to every cloned package: single interval, whole table, coverage curve, large n (10^5, 10^6), cold-import time, first-call (JIT) latency.
* **Memory / storage:** peak RSS during a table at several n (`tracemalloc`/`psutil`), installed size on disk (wheel size, site-packages footprint), dependency count and total dependency size, import time, sdist/wheel size.
* **Accuracy:** parity vs high-precision references (mpmath) at extreme p, x=0, x=n, n tiny and n huge; edge-case and error-handling behaviour (invalid input, NaN, arrays).
* **API / usability:** vectorisation, DataFrame output, typing, docs quality, examples, install friction (build steps, compilers), platform support.
* **Licence compatibility:** GPL vs MIT/BSD implications for reuse and for our own licence decision.

### 1.4 SWOT per package

For each package: Strengths, Weaknesses, Opportunities, Threats, **and a "how binomcikit improves on it" list**, each item tied to
a measurement from 1.2/1.3 (no claim without a number or a repro). Include an honest "where they beat us" column (for example
`bk.ci()` DataFrame overhead versus statsmodels/astropy).

### 1.5 Deliverables

* `docs/competitors/` (one page per package + a summary matrix) or one `planning/COMPETITOR_REPOS.md`.
* Extended `benchmarks/RESULTS.md` and `docs/benchmarks.md` (including memory and storage tables).
* Updated `docs/comparison.md` and `planning/NOVELTY_AND_COMPARISON.md`.
* Defect reports drafted (not filed) for the user to approve before anything is sent upstream.
* A prioritised improvement backlog feeding `planning/ROADMAP.md`.
* Feed the findings to the paper explorer (new anchors/competitor flags).

Rules: verify every number against the raw source; don't implement from memory; don't commit clones; don't file upstream issues without approval.

## 2. Everything still open from the 2026-10-01 session

### Methods not implemented (primary text unavailable)
- [ ] Andersson–Nerman
- [ ] Schilling–Doi LCO
- [ ] Wang
- [ ] Guan
- [ ] McGrath–Burke

### Performance
- [x] Speed up Sterne (n=1000 ≈ 3.3 s, n=5000 ≈ 82 s) and Blyth–Still–Casella using `scipy.special` ufuncs / numba
- [x] Speed up the full-table hedged betting interval (n=1000 ≈ 80 s)
- [x] Vectorise the remaining adjusted logit / Wald-T / LR (`cialt`, `ciatw`, `cialr`) and continuity-corrected logit / Wald-T (`ciclt`, `cictw`)
- [ ] Reduce `bk.ci()` DataFrame overhead for closed-form methods (currently slower than statsmodels/astropy) and Jeffreys through `ci()` (about 7–8× slower than statsmodels) — partly: flag columns by lookup (Wilson n=10,000 4 ms to 0.5 ms); the rest is pandas frame construction (2026-10-03)
- [x] Add a scheduled benchmark workflow that fails on a >2× regression — done, untested on GitHub (`benchmarks/regression_check.py`, `.github/workflows/benchmark.yml`)

### Unverified items
- [x] Investigate why pynomial (4e-4 to 1e-2) and binoculars (~1e-6) differ from standard Wilson/Wald/AC; astropy Wald differs by ~1e-3 — done: harness mistakes and conventions, see `planning/COMPETITOR_REPOS.md` section 5
- [ ] Commercial-tool rows still marked unverified: JMP, nQuery, Epi Info, StatXact
- [ ] SAS documentation PDF could not be downloaded; planning parity relies on the sources already read, so re-verify against the PDF

### Docs / release / signals (see `planning/ADOPTION_PLAN.md`, all need the user's decision)
- [ ] Release 3.1.0 to PyPI (bump version in `pyproject.toml`, `CITATION.cff`, `docs/conf.py`, `__init__`); Trusted Publishing
- [ ] Zenodo DOI; conda-forge feedstock
- [ ] Update `paper.md` (replace "first in Python"; add verification table, benchmark, Blaker finding); consider an arXiv stat.CO preprint — draft rewritten 2026-10-03 for the authors to review; arXiv preprint not started
- [ ] pyOpenSci review → JOSS
- [ ] File upstream issues (DBCI, DescTools) after approval
- [ ] Three notebooks/posts; Cross Validated / Stack Overflow answers; newsletter pitches — partly: the A/B tutorial now uses `bk.diff_interval`; notebooks/posts not started
- [ ] Niche integrations: LLM-eval snippet, A/B-testing notebook, zero-failure plan guide
- [ ] Licence decision (GPL-3.0 inherited from the R package); Streamlit app decision
- [ ] Engineering signals: coverage 65% → 80%, contribution scaffolding, Dependabot/pre-commit, SemVer policy, mypy, security review, docs search — coverage 84.7% (floor 80), CONTRIBUTING/SECURITY/templates, Dependabot, mypy gate, proposed SemVer policy (`docs/versioning.md`); not done: security review, docs search

### Housekeeping
- [x] Commit the session's work (committed on `main`, not pushed). Still to respect: never commit `previous-work/*.pdf`
- [ ] Re-run `paper-explorer/scripts/build_corpus.py` periodically; it needs `paper-explorer/.env` (never move the key into tracked files)
- [ ] The scorer reads abstracts only; confirm "strong" papers in the full text before citing
