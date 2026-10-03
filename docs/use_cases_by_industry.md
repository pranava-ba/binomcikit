# Use cases by industry — and what people use today

A binomial proportion is anything you count as *yes/no out of n*: a defect, a response, a click, a correct
answer, a default. This page answers three questions for each industry: **what do they actually need to know,
what do they use now,** and **where does binomcikit fit** (and where it doesn't).

> **How to read the "what exists today" column.** ✓ = confirmed from a source linked here, on 2026-10-01.
> ○ = well-known but not re-checked in this pass — treat as a lead, not a fact. Nothing here is a ranking or an
> endorsement: most of these tools are excellent at what they are for. The point is the *gap* each leaves.

*(An earlier, generic prose version of this page — industries and typical questions, with no products or sources — lived
in the project's `previous-work/` notes. This replaces it.)*

## At a glance

| Industry | The question | Typical method today | Existing tools | binomcikit adds |
|---|---|---|---|---|
| **Clinical trials & pharma** | adverse-event rate, response rate (single arm), sample size | Clopper–Pearson (regulatory default) | SAS PROC FREQ ✓, PASS ✓, StatXact ○, nQuery ○, R `binom`/`PropCIs` ✓ | **choose among 47 methods with measured coverage**; PASS/SAS-parity planning; zero-event bounds |
| **Diagnostics & medical devices** | sensitivity / specificity / accuracy with a CI | exact (Clopper–Pearson) or Wilson | MedCalc ✓, R `epiR` ✓, web calculators ✓ | tighter *exact-or-better* intervals (Sterne/BSC/OLC), assured-width planning |
| **Manufacturing, QC & reliability** | defect rate; "zero failures in n proves p < …" | Clopper–Pearson / success-run | Minitab acceptance sampling ✓, ISO 2859 ✓, R `AccSamplingDesign` ✓ | `sample_size_upper_bound`, OC-style planning, exact bounds |
| **Online experiments (A/B)** | conversion lift, with continuous monitoring | always-valid / sequential tests | Adobe Experience Platform ✓, Optimizely ✓, GrowthBook ✓ | open **confidence sequences** you can run and inspect, anytime-valid intervals from `(x, n)` |
| **LLM & ML evaluation** | accuracy of a model on *n* items; is A better than B? | Wilson / Clopper–Pearson / bootstrap | `evalci` ✓, ad-hoc in harnesses, research code ✓ | one tool to *compare* the intervals and show which under-covers at your n |
| **Finance & credit risk** | probability of default, esp. **low-default portfolios** | upper confidence bound ("most prudent estimation") | SAS ○, in-house models ✓ (literature) | exact/Jeffreys bounds at x = 0, rare-event (Garwood) interval |
| **Elections & audits** | is the reported outcome right? (risk-limiting audits) | betting / martingale tests | SHANGRLA ✓, RiLACS ✓, BRAVO/ALPHA ✓ | the Bernoulli special case, exposed and benchmarked |
| **Financial & compliance audit** | deviation rate in a control test; upper precision limit | attribute-sampling upper limit | ACL / Galvanize ✓, IDEA ○ | exact bounds, assured sample sizes |
| **Public health & epidemiology** | prevalence, vaccine response | Wilson / Clopper–Pearson | OpenEpi ✓, Epi Info ○, R `epiR` ✓ | a compare-all-methods table, Bayesian credible intervals |
| **Surveys & polling** | share supporting X, margin of error | Wald (the "±3%") — known to be poor | ○ (R `survey`, Stata `svy`, vendor software) | Wilson/Agresti–Coull/Jeffreys with the honest coverage picture |
| **Sports & analytics** | free-throw %, conversion rate, small samples | raw % ± Wald | ○ | Bayesian shrinkage, Wilson-lower-bound ranking |
| **Agriculture & ecology** | germination / survival / detection rate | Wilson / exact | ○ | rare-event and small-n methods |

---

## Clinical trials, pharma and regulatory work

**The question.** In a single-arm study or a safety table: *what proportion of patients had the event, and how sure are we?*
Plus the planning question: *how many patients?*

**Standard practice.** The exact (Clopper–Pearson) interval is the regulatory default where under-coverage is unacceptable:
FDA's [statistical guidance for diagnostic tests](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/statistical-guidance-reporting-results-studies-evaluating-diagnostic-tests-guidance-industry-and-fda)
specifies exact binomial intervals, and current ClinicalTrials.gov statistical analysis plans compute them for adverse-event and safety endpoints
(e.g. [NCT01296555](https://cdn.clinicaltrials.gov/large-docs/55/NCT01296555/Prot_SAP_000.pdf),
[NCT03676972](https://cdn.clinicaltrials.gov/large-docs/72/NCT03676972/SAP_001.pdf)).

**What exists today.**
* ✓ **SAS** `PROC FREQ … / BINOMIAL` — Wald and exact by default, plus Agresti–Coull, Blaker, Jeffreys, mid-P, likelihood-ratio, logit and Wilson
  ([documentation](https://documentation.sas.com/doc/en/procstat/9.4/procstat_freq_details37.htm)); `PROC POWER ONESAMPLEFREQ` for power and CI precision.
* ✓ **PASS (NCSS)** — "over 1200" sample-size and CI scenarios; five CI methods for one proportion
  ([chapter 115](https://www.ncss.com/software/pass/one-proportion-in-pass/)).
* ○ **StatXact / East (Cytel)**, **nQuery** — exact inference and design software; not re-checked here.
* ✓ R: `binom`, `PropCIs`, `exactci`, `binGroup`, `DescTools`, and the 2026 CRAN `binomCI`.

**Where binomcikit fits.** It does not replace validated SAS for a regulated submission. It is the place to *decide* which interval to
ask SAS for: `bk.recommend(n)` shows, at your sample size, how much length Blaker/Sterne/BSC/OLC save over Clopper–Pearson while keeping
(or knowingly relaxing) the guarantee; `bk.sample_size(..., plug_in="continuous")` reproduces PASS's numbers; `sample_size_upper_bound` gives the
zero-event bound for rare adverse events; `locally_correct` audits a candidate method against the 2024 criterion.

## Diagnostics and medical devices

**The question.** Sensitivity, specificity and accuracy of a test — each a proportion — with a confidence interval; sample sizes for verification studies.

**What exists today.** ✓ [MedCalc](https://www.medcalc.org/en/manual/diagnostic-test.php) reports exact Clopper–Pearson intervals for sensitivity,
specificity and accuracy and logit intervals for predictive values; ✓ R `epiR::epi.tests`; ✓ browser tools such as the
[University of Melbourne diagnostic-test calculator](https://shiny.vet.unimelb.edu.au/epi/dx.tests/). CLSI EP12 and FDA performance-evaluation
guidance govern the study design ○.

**Where binomcikit fits.** For a verification study with a pass/fail threshold, the *interval choice* matters at n ≈ 30–200. The assured-width planner
(`sample_size_assurance`) answers "how many to be 90% sure the interval is narrow enough?", and the exact-but-shorter intervals (`"bsc"`, `"sterne"`)
keep the guarantee while tightening it.

## Manufacturing, quality control and reliability

**The question.** What is the defect rate? *If I inspect n and find zero failures, what can I claim?* How many samples must I test to demonstrate a reliability target?

**What exists today.** ✓ Minitab's *Acceptance Sampling by Attributes* works from an acceptable and a rejectable quality level
([Minitab](https://support.minitab.com/en-us/minitab/help-and-how-to/quality-and-process-improvement/acceptance-sampling/supporting-topics/acceptance-sampling-in-minitab/));
✓ the ISO 2859 / ISO 28590 family of attribute-sampling standards; ✓ the CRAN package
[`AccSamplingDesign`](https://mirror.linux.duke.edu/pub/cran/web/packages/AccSamplingDesign/readme/README.html).

**Where binomcikit fits.** `sample_size_upper_bound(p_max, confidence, failures)` is the exact success-run/zero-failure calculation (299 trials at 0 failures prove
< 1% at 95%), with Wilson/Jeffreys alternatives. `bk.interval()` gives a microsecond-scale exact bound for in-line process monitoring. It does *not* design
full OC curves/AQL schemes — use the standards-based tools above for that.

## Online experiments (A/B testing)

**The question.** Conversion is a proportion; teams watch the dashboard continuously and stop early — which breaks fixed-n intervals.

**What exists today.** ✓ Adobe's Experience Platform experimentation service is built on **anytime-valid confidence sequences**, co-authored with the method's inventors
([arXiv:2302.10108](https://arxiv.org/pdf/2302.10108)); ✓ Optimizely's engine uses *always-valid* inference
([Johari et al., arXiv:1512.04922](https://arxiv.org/pdf/1512.04922)); ✓ GrowthBook publishes a guide to sequential testing
([GrowthBook](https://www.growthbook.io/insights/sequential-testing)). Statsig and Eppo ○ — not confirmed in this pass.

**Where binomcikit fits.** The *open, inspectable* version of the same machinery for the single-proportion case: `"mixture"` as an ordinary `(x, n)` table,
`bk.cibetseq` for a stream, hedged betting (verified against the authors' `confseq` to 1e-16). You can *measure* what peeking costs a naive interval
(see {doc}`methods/betting`) before you trust a vendor's.

## LLM and ML evaluation

**The question.** A model scores 78/100 on a benchmark; another scores 83/100. Is that a real difference — and what is the honest error bar?

**What exists today.** ✓ Recent work shows CLT-based and bootstrap intervals are badly calibrated at small n and recommends Wilson or Clopper–Pearson
([*Position: Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints*](https://arxiv.org/pdf/2503.01747)); ✓ many benchmark papers report Wilson intervals
and percentile/BCa bootstraps; ✓ PyPI's [`evalci`](https://pypi.org/project/evalci/) and distributed frameworks such as
[Spark-LLM-Eval](https://arxiv.org/pdf/2603.28769). Whether `lm-evaluation-harness`, `inspect` or OpenAI Evals ship binomial intervals ○ was not re-checked.

**Where binomcikit fits.** A worked tutorial exists ({doc}`tutorials/llm_eval_benchmark`); this release adds the anytime-valid intervals for *growing* leaderboards,
`compare`/`recommend` to show which interval under-covers at your n, and `sample_size_assurance` for "how many questions do I need?"

## Finance and credit risk

**The question.** Estimating a probability of default, especially for **low-default portfolios** where observed defaults are 0–3.

**What exists today.** ✓ The literature treats this as a confidence-interval problem: upper confidence bounds under the *most prudent estimation principle*
(Pluto & Tasche), the choice of binomial interval changing risk weights materially (Lawrenz), Bayesian low-default estimators
([arXiv:1112.5550](https://arxiv.org/pdf/1112.5550)). SAS and in-house validation libraries ○ — practice, not re-checked.

**Where binomcikit fits.** Exact one-sided bounds at x = 0, Jeffreys/Bayesian credible intervals, the rare-event Garwood interval, and `sample_size_upper_bound` — all with
a reproducible evaluation of how each behaves at the sample sizes banks actually have.

## Elections and audits

**The question.** After an election, how many ballots must be hand-checked to be confident the reported outcome is right?

**What exists today.** ✓ Risk-limiting audits have moved from BRAVO to **betting and martingale** methods: [SHANGRLA](https://www.arxiv.org/pdf/2201.02707) (with a Python library),
[RiLACS — risk-limiting audits via confidence sequences](https://arxiv.org/pdf/2107.11323), and
[ALPHA](https://projecteuclid.org/journals/annals-of-applied-statistics/volume-17/issue-1/ALPHA-Audit-that-learns-from-previously-hand-audited-ballots/10.1214/22-AOAS1646.full).

**Where binomcikit fits.** The *Bernoulli* special case (a two-candidate contest, a sampled yes/no) is exactly `cibetseq` — you can see the same mathematics as an interval table. It is
**not** an RLA framework (no ballot-polling logic, stratification or social-choice rules).

## Financial and compliance audit

**The question.** In a test of controls, a sample shows k deviations in n items; what is the *upper precision limit* of the true deviation rate, and how big must the sample be?

**What exists today.** ✓ Attribute sampling in audit software such as ACL (Galvanize) reports an **upper limit rate of deviation** and sample size from tolerable and expected
rates ([overview](https://www.academia.edu/79099534/Audit_Sampling_Using_ACL)); IDEA ○.

**Where binomcikit fits.** The one-sided exact bound is `bk.interval(..., "exact")` at the right α; `sample_size_upper_bound(tolerable_rate, confidence, failures=expected)` is the standard sizing.

## Public health, surveys, sports, ecology

* **Epidemiology.** ✓ OpenEpi offers six confidence intervals for a proportion ([OpenEpi](https://en.wikipedia.org/wiki/OpenEpi)); R `epiR`. binomcikit adds the compare-everything table and Bayesian intervals.
* **Surveys & polling.** The "±3%" margin of error is the Wald interval — the one the literature warns about ([Brown, Cai & DasGupta 2001](https://projecteuclid.org/euclid.ss/1009213286)). Wilson, Agresti–Coull and Jeffreys
  fix most of it; binomcikit shows the coverage so you can see it.
* **Sports analytics.** Small samples and many comparisons: Wilson-lower-bound ranking and Bayesian shrinkage (`bk.posterior`).
* **Agriculture & ecology.** Germination, survival, detection: small n, often rare — `"poisson"`, `"modified-jeffreys"`, exact intervals.

## What binomcikit is *not*

It is **single-proportion** inference. It does not do two-sample comparisons (risk differences/ratios), regression, stratified or clustered data, full acceptance-sampling schemes, or regulatory-validated reporting.
For those, the established tools above remain the right choice — binomcikit's job is to be the best, most transparent answer to *"which interval, and how many samples?"* for one proportion.
