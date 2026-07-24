# Binomial Proportion Inference — Methods Reference

Compiled from Subbiah & Rajeswaran (2017), *"proportion: A comprehensive R package for inference on single Binomial proportion and Bayesian computations,"* SoftwareX 6, 36–41.

This reference maps every mathematical method, metric, and Bayesian tool discussed in the paper to its implementation in the `proportion` R package, other R packages, and (where available) Python equivalents.

---

## 1. Base Confidence Interval Methods

| # | Method | Mathematical Basis | `proportion` (R) function | Other R packages | Python equivalent |
|---|--------|--------------------|-----------------------------|-------------------|--------------------|
| 1 | **Wald** | Inverts large-sample normal test; SE evaluated at MLE $\hat\theta$ | `ciWD(n, alp)` | `binom::binom.wald`, `binomCI`, `binGroup::binWald` | `statsmodels.stats.proportion.proportion_confint(method='normal')` |
| 2 | **Score (Wilson)** | Inverts test with SE evaluated at $H_0$ (Wilson, 1927) | `ciSD(n, alp)` (name illustrative — Score-based) | `binom::binom.wilson`, `binomCI`, `binGroup::binWilson`, `PropCIs` | `statsmodels.stats.proportion.proportion_confint(method='wilson')` |
| 3 | **ArcSine** | Wald-type interval on variance-stabilizing transform $\phi=\sin^{-1}(\sqrt\theta)$ | `ciTA(n, alp)` | `binomCI`, `binom` | ❌ None packaged — trivial manual implementation via `numpy.arcsin`/`numpy.sin` |
| 4 | **Logit-Wald** | Wald interval on $\phi=\log(\theta/(1-\theta))$, back-transformed | `ciLT(n, alp)` | `binomCI` (Wald logit), `binom` | ❌ None packaged (statsmodels/pynomial don't expose logit-Wald directly); manual via `scipy.special.logit`/`expit` |
| 5 | **Wald-T** | t-approximation of standardized estimator with boundary modification at $x=0,n$ | `ciWaldT(n, alp)` | Not found in major R CRAN packages (introduced/modified in this paper per Martín-Andrés & Álvarez 2014) | ❌ None found in any Python package |
| 6 | **Likelihood Ratio (LR)** | Inverts equation from log-likelihood ratio at $\hat\theta$ vs. full parameter space | `ciLR(n, alp)` | Documented in `contingencytables`; base `uniroot`-style manual R code | `pynomial` (GitHub: Dpananos/pynomial) — implements LR-test inversion |
| 7 | **Exact (Clopper–Pearson generalized, parameter $e$)** | Inverts equal-tailed binomial test; $2[e\,\Pr(X=x)+\min\{\Pr(X<x),\Pr(X>x)\}]$; $e=1$ → Clopper–Pearson, $e=0.5$ → Mid-P | `ciEX(n, alp, e)` | `binom::binom.exact`, `binomCI`, base R `binom.test` | `statsmodels.stats.proportion.proportion_confint(method='beta')` (only $e=1$/CP); `scipy.stats.binomtest(...).proportion_ci(method='exact')` |
| 8 | **Mid-P (special case, $e=0.5$)** | As above with $e=0.5$ | `ciEX(n, alp, e=0.5)` | `PropCIs::midPci`, `exactci` | ❌ None found — no packaged Mid-P in Python |
| 9 | **Bayesian (HPD & equal-tailed quantile), conjugate Beta(a,b)** | Posterior from Beta-Binomial conjugacy | `ciBAyes(n, alp, a, b)` | `binom::binom.bayes` (both HPD and equal-tailed), `PropCIs::diffci.bayes.hpd` | Equal-tailed: `scipy.stats.beta.interval()`, `statsmodels.stats.proportion.proportion_confint(method='jeffreys')` (fixed a=b=0.5 only); HPD: `arviz.hdi()` on posterior *samples* (not closed-form on PDF directly — needs `scipy.optimize` workaround); **`pynomial`** implements general Beta(a,b) equal-tailed credible interval |

---

## 2. Adjusted / Modified Variants

| # | Method | Mathematical Basis | `proportion` (R) function | Other R packages | Python equivalent |
|---|--------|--------------------|-----------------------------|-------------------|--------------------|
| 10 | **Agresti–Coull** | Adjusted Wald: $\tilde\theta = (x+z^2/2)/(n+z^2)$, "add successes/failures" | `ciAC(n, alp)` | `binom::binom.agresti.coull`, `binomCI` | `statsmodels.stats.proportion.proportion_confint(method='agresti_coull')` |
| 11 | **Continuity-Corrected (CC) Wald** | CC applied to base Wald | `ciWD(n, alp, c=...)` | `binomCI`, base R `prop.test` (Yates' CC) | ❌ None packaged; `statsmodels` has no CC toggle |
| 12 | **Continuity-Corrected Score** | CC applied to Wilson Score | `ciSD(n, alp, c=...)` | `prop.test` (partial CC, breaks near $x=n/2$ per Pires 2008) | ❌ None packaged |
| 13 | **Continuity-Corrected ArcSine** | CC applied to ArcSine | `ciTA(n, alp, c=...)` | Not commonly packaged | ❌ None packaged |
| 14 | **Continuity-Corrected Logit-Wald** | CC applied to Logit-Wald | `ciLT(n, alp, c=...)` | Not commonly packaged | ❌ None packaged |
| 15 | **Continuity-Corrected Wald-T** | CC applied to Wald-T | `ciWaldT(n, alp, c=...)` | Not found | ❌ None packaged |
| 16 | **Generalized Adjustment Factor ($h$)** | Adds constant $h$ to $x$ and adjusts $n$ before computing any base CI | Multiple `proportion` functions accept `h` argument | Not found as a generalized framework in any R package | ❌ None packaged anywhere |

---

## 3. Blaker & Other Exact Alternatives (Not in `proportion`, cited in related literature)

| Method | Mathematical Basis | R package | Python equivalent |
|--------|--------------------|------------|--------------------|
| **Blaker's exact interval** | Nested exact interval, narrower than Clopper–Pearson, based on acceptability function | `PropCIs::blakerci`, `BlakerCI`, `binGroup::binBlaker`, `contingencytables::Blaker_midP_CI_1x2` | ❌ None found in Python ecosystem |
| **Blyth–Still–Casella** | Shortest possible (non-nested) exact interval | Implemented in StatXact; S-PLUS code in Blaker (2000) | ❌ None found |
| **Sterne's exact / minlike method** | Confidence interval via inverted likelihood-ordering test | `exactci::binom.exact(tsmethod='minlike')` | ❌ None found |

---

## 4. Performance / Evaluation Metrics

| # | Metric | Mathematical Basis | `proportion` (R) function | Other R packages | Python equivalent |
|---|--------|--------------------|-----------------------------|-------------------|--------------------|
| 17 | **Coverage Probability (CP)** | $\sum_x \Pr(X=x\mid\theta)\cdot\mathbb{1}[\theta \in \text{CI}(x)]$, summarized via mean/min CP and RMSE from nominal | `covpWD`, `covpAC`, `covpGEN`, etc. | Not packaged as reusable metric functions elsewhere | ❌ None packaged — requires manual loop with `scipy.stats.binom.pmf` |
| 18 | **Expected Length (EL)** | Weighted average interval width across $x$, summarized via mean/SD/max | `lengthWD`, `lengthAC`, `PlotlengthEX`, etc. | Not packaged | ❌ None packaged — manual computation |
| 19 | **p-confidence, p-bias** (Vos & Hudson, 2005) | Deviation of actual coverage from nominal, directional bias measure | `PlotpCOpBIBA`, related functions | Cited in Vos & Hudson (2005); not packaged in R outside this paper | ❌ None packaged |
| 20 | **Error / Long-term power** (Martín-Andrés & Álvarez, 2014) | Difference between nominal $\alpha$ and actual error rate; % of $x$ causing error; success/failure indicator | `PloterrCAll`, `errCC`-type functions | Cited only in original paper; not packaged elsewhere | ❌ None packaged |
| 21 | **Aberrations (LABB / UABB)** | Lower/upper bound anomalies (e.g., non-monotonic behavior) | Reported alongside `ciWD` output (`Table 2`-style) | Discussed in Newcombe & Nurminen (2011); not packaged | ❌ None packaged |
| 22 | **Zero-Width Intervals (ZWI)** | Flag for degenerate (zero-length) CI at boundary $x=0$ or $x=n$ | Reported alongside CI output | Discussed in Newcombe (2011); not packaged | ❌ None packaged |
| 23 | **Monte Carlo (MC) evaluation over $\theta \sim \text{Beta}(a,b)$** | General evaluation framework replacing fixed-$\theta$ grid with MC draws from Beta (uniform is special case) | `covpGEN(n, LL, UL, alp, hp, t1, t2)` | Not packaged | Directly buildable using `scipy.stats.beta.rvs()` + `numpy` loop; no packaged equivalent |

---

## 5. Bayesian Toolbox

| # | Function | Mathematical Basis | `proportion` (R) function | Other R packages | Python equivalent |
|---|----------|--------------------|-----------------------------|-------------------|--------------------|
| 24 | **Bayes Factor** ($H_0: \theta<\theta_1$ vs. $H_1: \theta\ge\theta_2$) | Ratio of marginal likelihoods under Beta-Binomial model, distinct/equal priors | `hypotestBAF6x(x, n, th1, a1, b1, th2, a2, b2)` (1 of 12 related functions) | `BayesFactor` (R, logistic prior only, simpler hypothesis) | **`pingouin.bayesfactor_binom(k, n, p, a, b)`** — real closed-form BF for point-null $\theta=p$ vs. Beta($a,b$) alternative; structurally related but not identical to the paper's directional/range hypothesis |
| 25 | **Empirical Bayes (EB)** | Prior parameters estimated from data rather than fixed | `empericalBA(n, alp, sL, sU)` | Not found packaged elsewhere | ❌ None packaged; closest is manual `scipy.stats.beta.fit()` (not a true EB procedure) |
| 26 | **Posterior Predictive density** for new data $X_{\text{new}}(m,\theta)$ | Beta-Binomial predictive distribution, e.g. with Jeffreys prior | `probPRE(n, m, a1, a2)` | Not found packaged elsewhere as a dedicated function | `scipy.stats.betabinom.pmf(k, m, a, b)` — direct match |
| 27 | **Posterior probabilities** involving $\theta \mid X$ | Direct evaluation of Beta posterior CDF/PDF | Related function in Bayesian tool box (unnamed in text) | Not found packaged elsewhere | `scipy.stats.beta.cdf()` / `.pdf()` — direct match |

---

## 6. Summary Software Landscape (from paper's own literature review, Section 1)

| R Package | Methods Covered | Python status |
|-----------|-----------------|----------------|
| `binom` | Exact (Clopper–Pearson), Wald, Agresti–Coull, Wilson (no CC), transformed Wald (logit/complementary log/probit), Likelihood Ratio, Profile Likelihood, Bayes (conjugate beta, Jeffreys default), one-sided boundary intervals, CP/EL/RMSE plots | Partially covered: `pynomial` (explicit Python port of `binom`) covers Wald, Bayesian credible, exact, logit, LR |
| `binomSamSize` | Sample size determination; 2 exact/approximate methods | ❌ No direct Python equivalent found |
| `BlakerCI` | Blaker exact method only | ❌ No Python equivalent found |
| `epiR` | Score CI, Bayes with expert-opinion beta priors | Partial: Score via `statsmodels`; expert-prior Bayes buildable manually via `scipy.stats.beta` |
| `prevalence` | Wald, Agresti–Coull, Clopper–Pearson, Jeffreys, Score | Covered collectively by `statsmodels` (all five methods present) |
| `prop.comb.RR` | Score (w/ and w/o CC), Adjusted ArcSine, Adjusted Wald, Modified Score, Exact | Partial: only unadjusted Wald/Score/Exact covered; CC and adjusted variants absent |
| `PropCIs` | Score, Agresti–Coull (2 options), Blaker, Clopper–Pearson, Mid-P | Partial: Score, Agresti–Coull, Clopper–Pearson covered; Blaker and Mid-P absent from Python entirely |

---

## 7. Net Assessment

**Reasonably well-covered in Python** (via `statsmodels`, `scipy`, `pynomial`, `pingouin`):
Wald, Wilson/Score, Agresti–Coull, Clopper–Pearson/Exact, Jeffreys-type Bayesian interval, Likelihood Ratio (via `pynomial`), Beta-Binomial posterior predictive, posterior CDF/PDF evaluation, and a genuine closed-form Bayes Factor for binomial data.

**Not covered anywhere in the Python ecosystem** (confirmed via search):
ArcSine, Logit-Wald (as a packaged one-liner), Wald-T, Blaker's interval, Mid-P interval, all continuity-corrected variants, the generalized adjustment-factor ($h$) framework, and the entire performance-metrics suite (CP, EL, p-confidence, p-bias, error/long-term power, aberrations, ZWI) as reusable functions. Empirical Bayes and closed-form HPD-from-PDF (without sampling) are also absent as packaged, ready-to-use functions.

This gap is precisely where a comprehensive port such as `binomcikit` — replicating the `proportion` R package's full scope in Python — would fill a real, currently unaddressed need.
