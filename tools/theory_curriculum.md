# Theory series — curriculum spec (source of truth for the daily routine)

This file drives the **Methods & Mathematics** series in `docs/theory/`. It is a
tools-only spec: it is **not** part of the documentation build and must never be
added to a toctree.

A scheduled routine publishes **one page per day**. This file gives each page its
filename, title, learning goal, and — critically — the **exact, correct
formulas** it must contain, so the writing agent explains and expands rather than
re-derives (which is where a wrong formula could slip in).

## How the daily routine uses this file

1. `git pull` the latest `main`.
2. List `docs/theory/NN_*.md` pages that already exist (ignore `index.md`). The
   next day to write is `N = (count of numbered pages) + 1`.
3. If `N > 20`, the series is complete — do nothing, do not commit.
4. Otherwise write `docs/theory/<filename for day N>` following that day's spec
   below. Match the **style, depth, and formatting of Day 1**
   (`01_the_problem.md`): MyST Markdown, `$…$` / `$$…$$` math (the `dollarmath`
   extension is enabled), a short "In code" block using `import binomcikit as bk`,
   and a one-line "Next:" footer pointing at the following day.
5. Where a closed form is fiddly (Wald-T, LR, p-confidence/p-bias, error,
   aberrations), **read the actual implementation** under `src/binomcikit/` and
   describe what the code does, so the page matches the shipped behaviour. Prefer
   the code's exact expressions over a textbook variant.
6. Append the new page's slug (without `.md`) to the `{toctree}` in
   `docs/theory/index.md`.
7. Commit **only** the new page and the edited `docs/theory/index.md` with a
   message like `docs(theory): day N — <topic>`, then push to `origin/main`.

Notation used below: $z = z_{1-\alpha/2}$ is the standard-normal quantile
(`scipy.stats.norm.ppf(1 - alp/2)`); $\hat\theta = x/n$; $q = 1-\theta$.

---

## Day 1 — The problem, the estimate, and why it is hard  ✅ published
`01_the_problem.md`. Already written; use as the style reference.

## Day 2 — Wald
`02_wald.md` — code: `bk.ciwd`, `src/binomcikit/ci/base_n.py`.
- Point estimate $\hat\theta = x/n$; standard error $\text{SE} = \sqrt{\hat\theta(1-\hat\theta)/n}$.
- Interval: $\hat\theta \pm z\,\sqrt{\dfrac{\hat\theta(1-\hat\theta)}{n}}$, clipped to $[0,1]$.
- Key point: SE is evaluated **at the estimate** $\hat\theta$ — contrast with Score (Day 3).
- Failure modes: zero-width interval at $x=0$ and $x=n$ (since $\hat\theta(1-\hat\theta)=0$); systematic under-coverage; limits can fall outside $[0,1]$ before clipping.

## Day 3 — Score (Wilson)
`03_score_wilson.md` — code: `bk.cisc`, `base_n.py`.
- Invert the score test, SE evaluated **under the null** $\theta$: $\dfrac{\hat\theta-\theta}{\sqrt{\theta(1-\theta)/n}} = \pm z$.
- Squaring gives a quadratic in $\theta$; solve it:
  $$ L,\,U = \frac{\left(x + \tfrac{z^2}{2}\right) \pm z\sqrt{\dfrac{x(n-x)}{n} + \dfrac{z^2}{4}}}{n + z^2}. $$
- Centre $= (x + z^2/2)/(n + z^2)$, pulled toward $\tfrac12$. Always inside $[0,1]$; good small-$n$ coverage. This is the recommended default.

## Day 4 — ArcSine
`04_arcsine.md` — code: `bk.cias`, `base_n.py`.
- Variance-stabilising transform $\varphi = \arcsin\!\sqrt{\theta}$. By the delta method $\operatorname{Var}(\arcsin\!\sqrt{\hat\theta}) \approx \dfrac{1}{4n}$, free of $\theta$.
- Interval on the $\varphi$ scale: $\arcsin\!\sqrt{\hat\theta} \pm \dfrac{z}{2\sqrt{n}}$.
- Back-transform with $\theta = \sin^2(\varphi)$:
  $$ L,U = \sin^2\!\left(\arcsin\!\sqrt{\hat\theta} \mp \frac{z}{2\sqrt n}\right), \text{ clipped to } [0,1]. $$
- **Correction to flag on this page:** the old `Formulae and Explanation.md`
  back-transformed with $\sin^2(\varphi/2)$. That $\tfrac12$ is only correct for
  the *other* convention $\varphi = 2\arcsin\!\sqrt\theta$ (variance $1/n$). With
  the convention used here, $\varphi = \arcsin\!\sqrt\theta$, the back-transform
  is $\sin^2(\varphi)$ with **no** $\tfrac12$. State this explicitly.

## Day 5 — Logit-Wald
`05_logit_wald.md` — code: `bk.cilt`, `base_n.py`.
- Log-odds transform $\varphi = \operatorname{logit}(\theta) = \log\dfrac{\theta}{1-\theta}$, unbounded. Estimate $\hat\varphi = \log\dfrac{x}{n-x}$.
- Delta method: $\operatorname{Var}(\hat\varphi) \approx \dfrac{1}{n\hat\theta(1-\hat\theta)} = \dfrac{n}{x(n-x)}$, so $\text{SE} = \sqrt{n/(x(n-x))}$.
- Interval on the logit scale $\hat\varphi \pm z\,\text{SE}$, back-transform with the logistic $\theta = \dfrac{e^{\varphi}}{1+e^{\varphi}}$ (`expit`).
- Undefined at $x=0$ or $x=n$ (log of $0$); needs the $h$-adjustment there (Day 10).

## Day 6 — Wald-T
`06_wald_t.md` — code: `bk.citw`, **read `base_n.py` for the exact form**. Pan (2002), ref [22].
- Motivation: for small $n$ the standardised estimator is closer to Student-$t$ than to normal.
- Structure: replace $z$ with a $t$ critical value at estimated degrees of freedom, use the modified standard error the code computes, and apply the explicit boundary modifications at $x=0$ and $x=n$ described by Pan.
- Do **not** invent a closed form — mirror what `base_n.py` implements and explain each piece.

## Day 7 — Likelihood Ratio
`07_likelihood_ratio.md` — code: `bk.cilr`, `base_n.py`.
- LR statistic $G^2(\theta) = 2\left[x\log\dfrac{\hat\theta}{\theta} + (n-x)\log\dfrac{1-\hat\theta}{1-\theta}\right]$ (with $0\log 0 = 0$ at the edges).
- Interval $= \{\theta : G^2(\theta) \le \chi^2_{1,\,1-\alpha}\}$, and $\chi^2_{1,\,1-\alpha} = z^2$.
- No closed form: solve $G^2(\theta) = z^2$ numerically for one root in $(0,\hat\theta)$ and one in $(\hat\theta,1)$. Respects the likelihood's true shape; well-behaved at the boundary.

## Day 8 — Exact family (parameter $e$)
`08_exact_family.md` — code: `bk.ciex`, `base_n.py`.
- Invert the equal-tailed binomial test. Two-sided $p$-value at candidate $\theta$:
  $$ p(\theta) = 2\Big[\, e\,\Pr(X=x\mid\theta) + \min\{\Pr(X<x\mid\theta),\ \Pr(X>x\mid\theta)\} \,\Big], \quad 0 \le e \le 1. $$
- Interval $= \{\theta : p(\theta) \ge \alpha\}$; lower/upper limits solve the tail equations numerically.
- $e = 1$ → **Clopper–Pearson**, closed form via Beta quantiles: $L = \text{Beta}^{-1}_{\alpha/2}(x,\,n-x+1)$, $U = \text{Beta}^{-1}_{1-\alpha/2}(x+1,\,n-x)$; with $x=0$ set $L=0$, with $x=n$ set $U=1$.
- $e = 0.5$ → **Mid-P**. The knob $e$ = the fraction of the boundary atom $\Pr(X=x)$ that is counted; smaller $e$ trades guaranteed coverage for shorter intervals.

## Day 9 — Bayesian credible intervals
`09_bayesian_intervals.md` — code: `bk.cibayes`, `src/binomcikit/_hpd.py`.
- Conjugacy: prior $\theta \sim \text{Beta}(a,b)$, likelihood $\propto \theta^x(1-\theta)^{n-x}$, so posterior $\theta\mid x \sim \text{Beta}(a+x,\ b+n-x)$ (show the product of kernels).
- **Equal-tailed**: $\big[\text{Beta}^{-1}_{\alpha/2}(a+x,b+n-x),\ \text{Beta}^{-1}_{1-\alpha/2}(a+x,b+n-x)\big]$.
- **HPD**: shortest $[L,U]$ with posterior mass $1-\alpha$; solve $f(L)=f(U)$ subject to $F(U)-F(L)=1-\alpha$ numerically (this is `_hpd.py`).
- Priors with meaning: $a=b=1$ uniform/Laplace, $a=b=\tfrac12$ Jeffreys.

## Day 10 — Adjustment factor $h$ and Agresti–Coull
`10_adjustment_h.md` — code: `bk.cia*`, `src/binomcikit/ci/adj_n.py`.
- General idea: replace $x \to x+h$ and $n \to n+2h$ (pseudo-counts), then apply any base method — pulls $\hat\theta$ off the boundary.
- **Agresti–Coull** is the special case $h = z^2/2$: $\tilde\theta = \dfrac{x + z^2/2}{n+z^2}$, $\tilde n = n+z^2$, interval $\tilde\theta \pm z\sqrt{\tilde\theta(1-\tilde\theta)/\tilde n}$. With $z\approx1.96$, $z^2/2\approx1.92$ — the "add two successes and two failures" rule. Note its centre equals the Wilson centre from Day 3.

## Day 11 — Continuity correction $c$
`11_continuity_correction.md` — code: `bk.cic*`, `src/binomcikit/ci/cc_n.py`.
- Widen each limit by a small $c$ (with $c \le 1/(2n)$) to compensate for approximating a discrete distribution by a continuous one. Wald example: $\hat\theta \pm \big(z\sqrt{\hat\theta(1-\hat\theta)/n} + c\big)$. Yates' correction is $c = 1/(2n)$.
- Caveat (Pires 2008): the continuity-corrected Score misbehaves near $x = n/2$.

## Day 12 — Coverage probability
`12_coverage_probability.md` — code: `src/binomcikit/covp/`.
- $\text{CP}(\theta) = \sum_{x=0}^{n} \Pr(X=x\mid\theta)\,\mathbb{1}[\,L(x) \le \theta \le U(x)\,]$.
- A step function of $\theta$; target $\ge 1-\alpha$ everywhere. Summaries over a $\theta$-grid: mean CP, **minimum** CP, and RMSE from nominal. This is the primary scoreboard for a method.

## Day 13 — Expected length
`13_expected_length.md` — code: `src/binomcikit/expl/`.
- $\text{EL}(\theta) = \sum_{x=0}^{n} \Pr(X=x\mid\theta)\,\big(U(x)-L(x)\big)$; summaries mean / SD / max. Frames the coverage-vs-width trade-off: exact methods buy coverage with length.

## Day 14 — p-confidence and p-bias
`14_pconf_pbias.md` — Vos & Hudson (2005); code: `src/binomcikit/pconf/` — **read it**.
- Per-$x$ *directional* diagnostics that a mean coverage hides: p-confidence measures the confidence actually delivered at each $x$; p-bias measures the imbalance between the two tail errors. Give the conceptual definition, then state the exact expressions the `pconf` module computes.

## Day 15 — Error and long-term power
`15_error_power.md` — Martín-Andrés & Álvarez (2014), ref [13]; code: `src/binomcikit/err/` — **read it**.
- Difference between nominal $\alpha$ and the actual error rate; the percentage of the $n+1$ intervals that breach the limit; a pass/fail flag. Worked value from the paper: Clopper–Pearson with $n=5,\alpha=0.05,\theta=0.05,f=-2$ gives error difference $2.74$, $66.67\%$ of cases, verdict "success".

## Day 16 — Aberrations (LABB / UABB) and zero-width intervals
`16_aberrations_zwi.md` — code: the `LABB`/`UABB`/`ZWI` columns in `src/binomcikit/ci/` output.
- LABB / UABB: lower- and upper-bound anomaly flags (a limit that violates $[0,1]$ or the expected monotone ordering). ZWI: the zero-width-interval flag, raised when $U(x)=L(x)$ (the $x=0,n$ Wald collapse from Day 2). Show how they appear alongside a Wald table (paper Table 2).

## Day 17 — Monte-Carlo evaluation over a Beta-distributed $\theta$
`17_monte_carlo_beta.md` — code: `src/binomcikit/covp/general` (`covpgen`).
- Instead of a fixed $\theta$-grid, evaluate metrics by averaging over $\theta \sim \text{Beta}(a,b)$ (uniform is the special case $a=b=1$), or weight a sub-region via `t1, t2`. Lets a researcher weight *where* in $[0,1]$ accuracy matters. Mirror the `covpgen(n, LL, UL, alp, hp, t1, t2)` signature.

## Day 18 — Bayes factor
`18_bayes_factor.md` — code: `src/binomcikit/bayes/bayesfactors.py`.
- Range/directional hypotheses, e.g. $H_0: \theta < \theta_1$ vs $H_1: \theta \ge \theta_2$. Bayes factor $= m_1/m_0$, each $m_i = \int \Pr(x\mid\theta)\,\pi_i(\theta)\,d\theta$ over the restricted region under a (possibly distinct) Beta prior $\pi_i$. Worked value: $\text{BF}=7.79$ for $\theta<0.5$ vs $\theta>0.9$, $n=9$, $x=6$, priors $(1,1)$ and $(0.5,0.5)$.

## Day 19 — Empirical Bayes
`19_empirical_bayes.md` — code: `src/binomcikit/bayes/empirical.py`.
- Estimate the prior $(a,b)$ **from the data** (method-of-moments / marginal-likelihood) instead of fixing it, then form the credible interval from the resulting posterior. Mirror `empericalBA(n, alp, sL, sU)`; contrast honestly with a fully-specified prior.

## Day 20 — Posterior predictive and posterior probabilities
`20_predictive_posterior.md` — code: `src/binomcikit/bayes/predictive.py`, `posterior.py`.
- Posterior predictive for $m$ new trials is Beta-Binomial: $\Pr(X_{\text{new}}=k) = \dbinom{m}{k}\dfrac{B(k+a+x,\ m-k+b+n-x)}{B(a+x,\ b+n-x)}$ (matches `scipy.stats.betabinom`). Mirror `probPRE(n, m, a1, a2)` with a Jeffreys prior.
- Posterior probabilities: evaluate the $\text{Beta}(a+x,b+n-x)$ CDF/PDF for statements about $\theta$. Close the series with a short recap linking back to Day 1.
