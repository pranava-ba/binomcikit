# binomcikit — Novelty, Codebase Comparison & Real-World Usage

> Generated 2026-09-20. Answers three questions directly: (1) what is actually novel about
> binomcikit, stated so it survives scrutiny; (2) method-by-method, is each piece of the
> codebase already present in some *other* package (R or Python) — a large, verified table;
> (3) which of the implemented methods are actually used in practice today, and by whom.
> Builds on and tightens `RESEARCH.md` §§2–9 with additional packages RESEARCH.md's tables
> didn't cover (R `binom`, `PropCIs`, `DescTools`, `Hmisc`, `BayesFactor`) — verified against
> live CRAN/GitHub documentation on 2026-09-20, not just the 2026-07 scan `RESEARCH.md` cites.
> The companion paper repository referenced in §4 lives in `paper-explorer/repository/`.

---

## 1. The novelty, stated plainly

**Not novel:** any single confidence-interval *formula* in binomcikit. Wald, Wilson,
Agresti–Coull, Clopper–Pearson, Jeffreys, ArcSine, Logit-Wald, Wald-T, Mid-P, and even **Blaker**
and **Witting** all have a packaged implementation *somewhere* already (§2 below spells out
exactly where — mostly spread across four different R packages). If the pitch were "a Python
package with the Wilson interval," it would be redundant with `statsmodels` in one line of code.

**What's actually novel — three claims, each checked against the codebase you have today:**

1. **No single package — R or Python — bundles this specific set of ~14 base methods, their
   continuity-corrected/adjusted variants, *and* a reusable evaluation layer, *and* a Bayesian
   toolbox, in one tool.** The closest R packages each cover one slice: `DescTools::BinomCI`
   has ~16 CI methods but zero evaluation functions and zero Bayesian toolbox; `binom` has a
   *narrower* set of ~11 methods *plus* a real `binom.coverage()`/`binom.length()` evaluation
   pair (RESEARCH.md's claim that only `proportion` has reusable coverage/length functions is
   **incomplete** — `binom` has one too, just for its smaller method set, and it has no
   p-confidence/p-bias, error/power, aberrations, ZWI, or MC θ-space evaluation); `PropCIs`
   covers six single-proportion methods (Wald, Wilson/score, two Agresti–Coull variants,
   Clopper–Pearson exact, **Mid-P**, and Blaker — verified directly against its function index,
   correcting an earlier draft of this table that missed `midPci`) but has no evaluation layer
   and no Bayesian toolbox beyond a two-sample Bayesian function. binomcikit is the only
   package — Python or R — that has *all three layers at once* for a single proportion.
2. **In Python specifically, none of this exists at all.** `statsmodels`/`scipy`/`astropy` give
   you 3–6 common intervals and stop; there is no Python package with ArcSine, Wald-T, Mid-P,
   the generalized-*e* exact continuum, the *h*-adjustment framework, or any of the evaluation
   or Bayesian-toolbox functions (verified again 2026-09-20 — nothing new registered on PyPI
   that changes this). binomcikit is a genuine first for the Python ecosystem, not an
   incremental addition to it.
3. **The reference tool it revives is dead.** R `proportion` was archived from CRAN
   2022-04-27 for unresolved check failures and is not installable via `install.packages()`
   — confirmed still archived as of 2026-09-20 (source still on GitHub,
   github.com/RajeswaranV/proportion, unmaintained). binomcikit is the only actively-developed,
   tested, typed successor to that capability in *any* language.

**Two claims from earlier drafts that do NOT survive this check — corrected here:**

- ❌ *"Blaker is absent from the entire ecosystem outside R proportion."* **False.** `PropCIs::blakerci`
  and `DescTools::BinomCI(method="blaker")` both ship it, and both are actively maintained CRAN
  packages (unlike archived `proportion`). Blaker is new to **Python**, not new, period.
- ❌ *"Betting/confidence-sequence CIs would make binomcikit the first Python package with them."*
  **False.** Waudby-Smith, Ramdas & Howard already ship `confseq` on PyPI
  (github.com/gostevehoward/confseq) implementing exactly this — their own reference
  implementation, since 2021. Its own README calls it "early-stage, should not be considered
  stable," and it's a general bounded-random-variable/streaming toolkit with no
  binomial-proportion ergonomics and no integration with any coverage/length/Bayesian
  evaluation suite. The defensible claim is narrower: binomcikit would be the first to put
  **classical + exact + Bayesian + betting** methods for a single proportion under *one*
  evaluation roof with head-to-head coverage/length benchmarking — not "first with betting CIs."

**Bottom line for the JOSS resubmission:** lead with claim 1 (the three-layer bundle) and claim 2
(Python-first), not with any individual method. The paper should say, in as many words, "every
piece exists somewhere; nothing else assembles them," and should explicitly concede Blaker's
prior existence in R and `confseq`'s prior existence for betting CIs — reviewers who check GitHub
will find both in under a minute, so getting there first reads as rigor, not weakness.

---

## 2. Master comparison table — every method/capability × every comparable package

✅ = packaged, one function call · ❌ = reviewed docs do not list it (strong evidence of absence
for these small, well-documented packages, though not an exhaustive audit of every package's full
source) · ➖ = exists in a different, non-reusable form. R packages verified against their live
CRAN/GitHub reference pages on 2026-09-20; Python columns carry over RESEARCH.md's 2026-07
verification (statsmodels/scipy/astropy/pynomial/binomial_cis), re-spot-checked here.

### 2a. Base interval methods

| Method | R `binom` | R `PropCIs` | R `DescTools` | R `Hmisc` | R `proportion`¹ | Py `statsmodels` | Py `scipy` | Py `astropy` | Py `pynomial` | Py `binomial_cis` | **binomcikit** |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Wald | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ |
| Wilson / Score | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| Agresti–Coull | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ |
| Clopper–Pearson (exact) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅² | ✅ |
| Jeffreys | ➖³ | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ | ➖ | ❌ | ✅ |
| Likelihood-ratio (LR) | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| Logit-Wald | ✅ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| **ArcSine** | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Complementary log-log | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌⁴ |
| Probit | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌⁴ |
| **Wald-T** (Pan 2002) | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Mid-P** (exact e=0.5) | ❌ | ✅ (`midPci`) | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Generalized exact** (any *e* ∈ [0,1]) | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Blaker** (exact, ⊆ CP) | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Witting** (1985, randomized-optimal) | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌⁴ |
| **Pratt** (closed-form approx.) | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌⁴ |
| Sterne / minlike | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌⁴ |
| Blyth–Still–Casella | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌⁴ |
| Andersson–Nerman (2024) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌⁴ |
| Bootstrap (any variant) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌⁴ |
| Betting / confidence-sequence | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌⁴ (Py has `confseq`, see §1) |
| Continuity-corrected variants (Wald/Wilson/ArcSine/Logit/Wald-T) | ➖ (Wald & Wilson only, via `prop.test`) | ❌ | ➖ (Wald & Wilson only: `waldcc`/`wilsoncc`) | ❌ | ✅ (all five) | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ (all five) |
| Adjustment-factor *h* framework (generalized operator, not fixed presets) | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Bayesian equal-tailed, Beta(a,b) any prior | ➖ (fixed prior via args) | ❌ | ➖ (Jeffreys prior fixed) | ❌ | ✅ | ➖ | ❌ | ✅ | ➖ | ❌ | ✅ |
| Bayesian HPD | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

¹ Archived from CRAN 2022-04-27; source still on GitHub, unmaintained since.
² `binomial_cis` returns one *length-optimal* interval subject to exact coverage, not Clopper–Pearson per se.
³ R `binom`'s `"bayes"` method takes an arbitrary `prior.shape1`/`prior.shape2`, so Jeffreys (0.5, 0.5) is
reachable but not a named preset.
⁴ **Honest reverse-gap**: binomcikit does not (yet) have this method, and at least one other package does —
Witting and Pratt exist today only in R `DescTools`; cloglog/probit only in R `binom`; Blaker/Blaker's
cousins Sterne, Blyth–Still–Casella, Andersson–Nerman, bootstrap and betting exist nowhere as a *packaged
binomial-proportion* function except where noted (RESEARCH.md §7–9 has the build plan for the ones worth
adding — Blaker is already built as of Sub-phase 1.9).

### 2b. Evaluation / diagnostic layer (the actual differentiator)

| Capability | R `binom` | R `PropCIs` | R `DescTools` | R `Hmisc` | R `proportion` | Py `statsmodels`/`scipy`/`astropy`/`pynomial` | **binomcikit** |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Coverage probability, reusable fn (`binom.coverage`-style) | ✅ (11 methods only) | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| Expected length, reusable fn | ✅ (11 methods only) | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| **p-confidence / p-bias** (Vos–Hudson) | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| **Error / long-term power** (Martín-Andrés) | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| Aberrations (LABB/UABB) | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| Zero-width interval (ZWI) flag | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| MC evaluation over θ ~ Beta(a,b) (vs. a fixed grid) | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| Method-recommendation helper (`recommend`) | ➖ (`binom.optim` picks *one* method to minimize error, not a ranked table) | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Comparison plots for all of the above | ➖ (per-method plots exist) | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ (interactive Plotly) |

### 2c. Bayesian toolbox

| Capability | Py `pingouin` | R `BayesFactor` | R `proportion` | **binomcikit** |
|---|:--:|:--:|:--:|:--:|
| Bayes factor, point-null (p = p₀) | ✅ | ✅ | ✅ | ✅ |
| Bayes factor, **directional/interval** (p < p₁ vs p ≥ p₂) | ❌ | ✅ (`nullInterval=`) | ✅ (6 variants, `hypotestbaf1`–`6`) | ✅ |
| Empirical Bayes (beta-binomial marginal MLE/MoM/EM) | ❌ | ❌ | ✅ | ✅ |
| Posterior predictive (Beta-Binomial) | ➖ (`scipy.betabinom` gives the density, no packaged predictive routine) | ❌ | ✅ | ✅ |
| Posterior probabilities of θ\|X | ➖ | ➖ (posterior samples only) | ✅ | ✅ |

**Correction to RESEARCH.md §3.2 footnote 4**: `pingouin.bayesfactor_binom` is point-null only, as
previously noted — but **R's actively-maintained `BayesFactor::proportionBF`** already does the
directional/interval test via its `nullInterval` argument, which is a stronger, more current
competitor on this one capability than the archived `proportion` package. binomcikit still leads
because empirical Bayes and posterior predictive are absent from `BayesFactor` entirely.

---

## 3. What this means, method by method

- **Genuinely uncontested (nothing else has it, anywhere, in any language):** the *combination*
  of p-confidence/p-bias, error/long-term power, aberrations, ZWI, and MC θ-space evaluation as
  reusable functions; empirical Bayes + posterior predictive + posterior probabilities as a
  bundle; the generalized *e*-continuum and *h*-adjustment-factor abstractions as explicit APIs
  (not just as one-off formulas).
- **New to Python, not new absolutely:** ArcSine, Wald-T, Mid-P, Blaker, the full
  continuity-corrected family, HPD intervals.
- **Exists elsewhere too, keep humble:** Wald/Wilson/Agresti-Coull/Clopper-Pearson/Jeffreys/LR/
  Logit (spread across `binom`/`DescTools`/`statsmodels`), Blaker (`PropCIs`, `DescTools`),
  directional Bayes factors (`BayesFactor`).
- **binomcikit doesn't have yet, and should stop implying it's first to plan:** cloglog/probit
  (`binom` has them), Witting/Pratt (`DescTools` has them), betting/confidence-sequences
  (`confseq` has them, if immaturely) — RESEARCH.md §7–9's build-order already has most of these
  queued; this table is the citation-ready evidence for why each is worth adding (closes a gap
  even vs. the *narrowest* competitor) rather than a novelty claim in itself.

---

## 4. Paper repository

**Location:** `paper-explorer/repository/` (`seed_references.bib`, `.csv`, `.json`) — built by
running the paper-explorer's own `export.py`/`analyze.py` against the 36 references already
verified in `RESEARCH.md` §11 (Wilson 1927 through the 2024 betting/locally-correct/Andersson–
Nerman/rare-events cluster). This seeds the bibliography now, in the exact format a live search
would produce, from data already fact-checked in this project.

**Live OpenAlex search — initially blocked, then unblocked mid-session.** `openalex.search_core()`
and raw hits to `api.openalex.org` returned HTTP 429 with `"dailyRemainingUsd": 0` for most of this
session (this network's shared free-tier OpenAlex budget was exhausted, unrelated to the tool's
code). Two things happened before it was resolved: (1) a Crossref-based stand-in pull, described
below, and (2) the user then supplied a personal `OPENALEX_API_KEY`, which unblocked real OpenAlex
access immediately (verified with a direct API hit: HTTP 200). `paper-explorer/repository/openalex_live_pull.json`
is the result — 72 papers (6 per sub-topic across all 12 presets), with real reconstructed abstracts,
scored through the tool's actual `analyze.py` logic: 1 strong, 18 ok, 10 weak, 43 unknown. This is
the highest-quality file in the repository (real abstracts let the relevance scorer actually work)
and the one to prefer going forward. Re-run with a larger `limit` and pull `references()`/`citations()`
for a chosen core paper (e.g. Blaker 2000, Waudby-Smith & Ramdas 2024) to get the citing/cited-by
graphs this initial pass didn't request, to control API cost.

**Live pull done via Crossref as a stand-in, before the API key arrived.**
`references.bib` / `references.csv` / `papers_index.json` in `repository/` were built from a live
Crossref search — one query per sub-topic preset plus a targeted re-fetch of all 21 landmark papers
in §2's sources, run through the tool's actual scoring logic. Result: **66 unique papers with real,
current DOIs and citation counts**, and independent confirmation of 15 of the 21 landmark
references (6 didn't return a confident Crossref match). Caveat: Crossref's metadata is
title-heavy and abstract-sparse compared to OpenAlex's reconstructed abstracts, so the relevance
bands in this file under-detect "strong"/"ok" (0 "strong" out of 66) — read `references.bib`/`.csv`
as DOI/citation-count verification of the literature, not as a relevance-scored run.
`seed_references.*` remains the primary, hand-verified bibliography from `RESEARCH.md` §11.

---

## 5. Real-world usage — is each method actually used today?

*Not "who cites the paper" (that's §11 of RESEARCH.md) — actual adoption in industry, regulatory
guidance, and current software defaults. Verdicts are honest about thin evidence; nothing below
is invented.*

| Method | Verdict | Evidence |
|---|---|---|
| **Wald** | Superseded in guidance, but still a live *software default*. Academically discredited since Brown–Cai–DasGupta (2001), yet SAS `PROC FREQ`'s `BINOMIAL` option and R's `binom`/`Hmisc` all still ship it as one of the standard outputs — it survives because it's the simplest formula, not because anyone recommends it. | SAS 9.3 `PROC FREQ` ships Wald by default alongside exact ([lexjansen.com NESUG paper](https://www.lexjansen.com/nesug/nesug13/41_Final_Paper.pdf)) |
| **Wilson score** | **Actively used in production today**, not just textbooks. Evan Miller's 2009 "How Not To Sort By Average Rating" popularized ranking by the Wilson lower bound instead of raw average, and it's cited as the reason Reddit-style ranking systems use it; a maintained open-source `wilson_score` utility exists in Instacart's GitHub org. | [Evan Miller, evanmiller.org](https://www.evanmiller.org/how-not-to-sort-by-average-rating.html); [github.com/instacart/wilson_score](https://github.com/instacart/wilson_score) |
| **Agresti–Coull** | Current textbook/software default for "simple but reliable," specifically recommended by Brown–Cai–DasGupta (2001) for n > 40; shipped as a standard SAS `PROC FREQ (ALL)` output. | [SAS PROC FREQ methods list, lexjansen.com](https://www.lexjansen.com/nesug/nesug13/41_Final_Paper.pdf) |
| **Clopper–Pearson (exact)** | **Regulatory-standard, actively used today.** FDA statistical guidance for diagnostic-test and adverse-event reporting specifies exact binomial intervals; multiple current ClinicalTrials.gov protocol/SAP documents compute Clopper–Pearson CIs for adverse-event and safety-endpoint rates. Its guaranteed-coverage property is exactly why it's mandated where under-coverage is unacceptable. | [FDA: Statistical Guidance on Reporting Results from Studies Evaluating Diagnostic Tests](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/statistical-guidance-reporting-results-studies-evaluating-diagnostic-tests-guidance-industry-and-fda); e.g. [NCT01296555 protocol/SAP](https://cdn.clinicaltrials.gov/large-docs/55/NCT01296555/Prot_SAP_000.pdf) |
| **Jeffreys** | Current recommended default for small n (Brown–Cai–DasGupta), shipped in SAS `PROC FREQ (ALL)` and R `DescTools`/`astropy`; less common as an application *default* than Wilson but standard as an available option in current software. | Same SAS/Brown-Cai-DasGupta sources as above |
| **Blaker** | Niche but current: available today in two actively-maintained R packages (`PropCIs::blakerci`, `DescTools::BinomCI(method="blaker")`), and still recommended in 2020s applied-statistics discussions as the tightest guaranteed-coverage exact interval. No evidence of mainstream production/industry adoption (it's a specialist choice, not a default anywhere) — "used by statisticians who know to ask for it," not a household method. | CRAN docs for `PropCIs`/`DescTools` (§2 sources above) |
| **Betting / confidence-sequence (anytime-valid) CIs** | **This is the one with the clearest, most current industry adoption of anything on this list.** Adobe's Experience Platform experimentation service is built on anytime-valid confidence sequences (published at ACM Web Conference 2023) specifically to let A/B tests be monitored continuously without inflating false-positive rates; GrowthBook (a real, currently-operated A/B-testing product) publishes a guide recommending sequential/anytime-valid testing for the same reason. This is a live, growing industry practice, not a theoretical curiosity — which makes it the strongest "still-current, still-growing" story of any method binomcikit could add. | [Anytime-Valid Confidence Sequences in an Enterprise A/B Testing Platform, ACM Web Conf. 2023](https://arxiv.org/pdf/2302.10108); [GrowthBook: What Is Sequential Testing?](https://www.growthbook.io/insights/sequential-testing) |
| **R `proportion` package itself** | Confirmed at least one real downstream dependency (Julia's `ClinicalTrialUtilities` package cites it in its references) despite CRAN archival in 2022; broader reverse-dependency data would need CRAN's own archive page for a full count, which this pass didn't pull. Thin evidence either way beyond that one confirmed case — treat as "some real use, not widely measured," not as "no one used it." | [ClinicalTrialUtilities references](https://docs.juliahub.com/ClinicalTrialUtilities/lEJUs/0.3.1/ref/) |

**Reading this table for the paper:** the strongest "this matters today" story isn't a classical
method at all — it's the betting/confidence-sequence family, which is being adopted in production
A/B-testing infrastructure right now (Adobe, GrowthBook) for exactly the reason binomcikit's
evaluation suite exists (to let a practitioner *check* a method's real coverage behavior rather
than trust a default). Pairing "here's live industry adoption of the 2024 paradigm" with "here's a
package that can benchmark it against every classical alternative" is a stronger paper hook than
any individual CI formula's provenance.

---

## Sources & methodology

R package method lists verified against their CRAN/GitHub reference documentation, accessed
2026-09-20: `binom` (cran.r-project.org/web/packages/binom), `PropCIs`
(cran.r-project.org/web/packages/PropCIs), `DescTools::BinomCI`
(rdrr.io/cran/DescTools/man/BinomCI.html), `Hmisc::binconf`
(github.com/harrelfe/Hmisc/blob/master/R/binconf.s), `BayesFactor::proportionBF`
(rdrr.io/cran/BayesFactor/man/proportionBF.html), `confseq`
(github.com/gostevehoward/confseq, pypi.org/project/confseq), R `proportion` archival status
(cran.r-project.org/web/packages/proportion). Python package coverage (`statsmodels`, `scipy`,
`astropy`, `pynomial`, `binomial_cis`, `pingouin`) carried over from `RESEARCH.md` §3's 2026-07
verification. This is web-search-depth verification (official docs pages), not a full source-code
audit of every package — treat ❌ as strong evidence, not a formal proof of absence.

**Independent re-verification (2026-09-20, separate from the research above):** this report was
produced by two parallel research passes; before accepting their conclusions, the coordinating
session independently re-fetched and re-checked the highest-stakes claims directly against
official sources: `PropCIs::blakerci` (confirmed via rdrr.io man page — and, in doing so, found
and corrected a table error: `PropCIs::midPci` provides Mid-P, which an earlier draft of §2a had
marked ❌); `DescTools::BinomCI`'s exact `method=` argument list (confirmed verbatim from its docs,
including `witting`, `pratt`, and `blaker`); R `proportion`'s CRAN archival notice (confirmed
verbatim, "Archived on 2022-04-27"); `binom.coverage`/`binom.length` (confirmed as real exported
functions in `binom`'s man-page index); the `confseq` PyPI package (confirmed real, v0.0.11,
maintained by PyPI accounts `gostevehoward` and `wannabesmith` — GitHub handles matching Steven
Howard and Ian Waudby-Smith, the actual authors of the betting/confidence-sequence papers); and the
Adobe anytime-valid A/B testing paper (confirmed on arXiv, 2302.10108 — and its author list
includes Ian Waudby-Smith and Aaditya Ramdas themselves alongside the Adobe-affiliated authors,
which is stronger evidence than "an Adobe team cited the method" — the method's own inventors
co-authored the production deployment). Not independently re-checked: the SAS `PROC FREQ` claims,
the GrowthBook page, the Evan Miller/Instacart claims, the FDA guidance document and ClinicalTrials.gov
protocol citations, `Hmisc::binconf`'s exact method list, and `BayesFactor::proportionBF`'s
`nullInterval` argument — these came from one or both research passes independently (not
cross-verified by the coordinating session) and, while specific and plausible, should get a look
before being stated as fact in a submitted paper.
