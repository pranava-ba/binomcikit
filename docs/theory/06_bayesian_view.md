---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# The Bayesian view — priors, posteriors, credible intervals

Every method so far has been **frequentist**: the true rate {term}`theta` is a fixed unknown constant, the
data are random, and an interval is judged by its {term}`coverage` over repeated experiments. This page
takes the other great tradition. The **{term}`Bayesian`** view treats $\theta$ *itself* as uncertain —
described by a {term}`prior` distribution — and uses the data to *update* that belief into a
{term}`posterior`. The interval is then read straight off the posterior. It answers a subtly different
question, and — the punchline of this page — with the right prior it *also* achieves excellent frequentist
coverage, so the two traditions quietly meet.

Every code block here is **executed when the docs are built**.

## Conjugacy: Beta prior in, Beta posterior out

Bayes' rule multiplies the prior by the likelihood. For a {term}`binomial`, the likelihood is
$\propto \theta^x(1-\theta)^{n-x}$; if the prior is a **{term}`Beta distribution`** $\text{Beta}(a,b)
\propto \theta^{a-1}(1-\theta)^{b-1}$, the product is *another* Beta. That is **{term}`conjugate prior`**
magic — the update becomes pure arithmetic:

$$\text{Beta}(a,b) \;\xrightarrow{\;x \text{ successes, } n-x \text{ failures}\;}\; \text{Beta}(a+x,\;
b+n-x).$$

Add the successes to $a$, the failures to $b$. That is the whole update.

```{code-cell} python
import binomcikit as bk

# Uniform prior Beta(1,1); observe x = 3 of n = 5:
post = bk.posterior(3, 5, a=1, b=1)
{k: post[k] for k in ["a_post", "b_post", "mean", "mode"]}
```

The posterior is $\text{Beta}(1+3,\,1+2) = \text{Beta}(4,3)$, exactly as the rule predicts. Its **mode is
0.6** — identical to the {term}`maximum likelihood estimate` $\hat p = 3/5$ — while its **{term}`posterior
mean`** $4/7 \approx 0.571$ is pulled a little toward the centre by the prior. Picture the update:

```{figure} ../_static/bayesian_posterior.png
:alt: Uniform prior and the Beta(4,3) and Beta(3.5,2.5) posteriors after 3 of 5
:width: 100%

The Bayesian update. The {term}`prior` $\text{Beta}(1,1)$ (dashed) is *flat* — every rate equally
plausible before data. After 3 successes in 5 trials it becomes the peaked {term}`posterior`
$\text{Beta}(4,3)$ (blue), concentrated near the observed $\hat p = 0.6$ (orange line); the shaded band is
its 95% {term}`credible interval`. The Jeffreys-prior posterior $\text{Beta}(3.5,2.5)$ (green) is barely
different — with this much data the likelihood dominates the prior.
```

## Choosing a prior

The prior encodes what you believe before the data. `binomcikit` knows the standard "objective" choices —
priors designed to *let the data speak* rather than inject opinion:

```{code-cell} python
{name: bk.prior(name) for name in ["uniform", "jeffreys", "haldane"]}
```

- **Uniform** $\text{Beta}(1,1)$ (Laplace) — flat; every rate equally likely a priori.
- **Jeffreys** $\text{Beta}(0.5,0.5)$ — the *invariant* choice, U-shaped, gently favouring the extremes;
  the one with the best frequentist properties (below).
- **Haldane** $\text{Beta}(0,0)$ — maximally non-informative, so the posterior mean equals $\hat p$.

Feeding a different prior just changes the two numbers you add. Jeffreys, for instance, gives a
$\text{Beta}(3.5,2.5)$ posterior for our data:

```{code-cell} python
a, b = bk.prior("jeffreys")
pj = bk.posterior(3, 5, a=a, b=b)
pj["a_post"], pj["b_post"]
```

## Reading an interval off the posterior: credible intervals

A **{term}`credible interval`** is any range holding 95% of the posterior probability. Two natural choices:
the **equal-tailed** interval (chop 2.5% off each tail — the posterior {term}`quantile`s) and the
**{term}`highest posterior density interval`** (HPD, the *shortest* range containing 95%). binomcikit
returns both:

```{code-cell} python
{"equal-tailed": tuple(round(float(v), 4) for v in post["quantile_interval"]),
 "HPD":          tuple(round(float(v), 4) for v in post["hpd_interval"])}
```

They differ because the $\text{Beta}(4,3)$ posterior is slightly skewed — the HPD shifts toward the denser
side and is a touch shorter. Because these are just posterior quantiles, you can reproduce the equal-tailed
one directly from the Beta distribution:

```{code-cell} python
from scipy.stats import beta
lo, hi = beta.ppf(0.025, 4, 3), beta.ppf(0.975, 4, 3)
print("from scipy   :", round(lo, 6), round(hi, 6))
print("from posterior:", *(round(v, 6) for v in post["quantile_interval"]))
```

## Credible ≠ confidence — the meaning is different

This is the crux. The {doc}`foundations page <../foundations/04_confidence_interval>` was emphatic that a
frequentist 95% interval does **not** let you say "95% chance $\theta$ is in here." A **credible** interval
*does* — that is exactly its meaning: *given your prior and the data*, there is a 95%
{term}`posterior probability` that $\theta$ lies inside. The price is the prior: the statement is only as
defensible as the belief you started from. Frequentist intervals need no prior but make only a statement
about the long-run *procedure*; Bayesian intervals make a direct probability statement about *this*
$\theta$ but require you to declare a prior. Same data, two honest but different sentences.

## Why Jeffreys has good frequentist coverage

Here is where the traditions converge. A credible interval is built with no regard for
{term}`coverage` — yet we can still *measure* its coverage, treating it as if it were a frequentist recipe.
Do that at $n = 40$:

```{code-cell} python
import numpy as np, pandas as pd
rows = {}
for m, lab in [("jeffreys", "Jeffreys credible"), ("bayes", "Uniform-prior credible"),
               ("wilson", "Wilson (frequentist)")]:
    c = bk.coverage_curve(40, method=m)["coverage"]
    rows[lab] = {"mean": round(float(c.mean()), 3), "min": round(float(c.min()), 3)}
pd.DataFrame(rows).T
```

The **Jeffreys** credible interval has frequentist coverage essentially *identical* to {doc}`Wilson
<../methods/wilson>` (mean ≈ 0.952 vs 0.953) — even though it was never designed to. The uniform-prior
interval is noticeably worse. This is not a coincidence: the Jeffreys prior is a **matching prior**, chosen
by an invariance principle that happens to make its credible intervals track their nominal level under
repeated sampling. Asymptotically, **Bernstein–von Mises** guarantees it — as $n$ grows the posterior
becomes {term}`normal distribution`-shaped and centred on the {term}`maximum likelihood estimate`, so the
credible interval and the frequentist interval converge — but Jeffreys does well even at small $n$. It is
why Jeffreys is a first-rate interval whichever tradition you belong to.

## How this connects

- {doc}`The Bayesian method page <../methods/bayes>` (`ciba` / `cibax`) computes these credible intervals;
  the {doc}`Bayesian toolbox <../bayesian_toolbox>` goes further — Bayes factors, empirical Bayes,
  posterior-predictive computation.
- The access layer's `posterior()` and `prior()` (used above) are the convenient front door.
- Next — and last — in the series: {doc}`coverage theory <07_coverage_theory>` itself, a closer look at
  what all these oscillating coverage curves, frequentist and Bayesian alike, are really telling us.

## Check yourself

**Q1.** With a $\text{Beta}(2,2)$ prior, you observe 7 successes in 10 trials. What is the posterior, and
what is its mode?

:::{dropdown} Show answer
By {term}`conjugate prior` arithmetic, add successes to $a$ and failures to $b$:
$\text{Beta}(2+7,\,2+3) = \mathbf{\text{Beta}(9,5)}$. Its mode is $(a-1)/(a+b-2) = 8/12 \approx 0.667$.
```python
bk.posterior(7, 10, a=2, b=2)["mode"]      # -> 0.6667
```
:::

**Q2.** A colleague says "my 95% credible interval means there's a 95% probability the true rate is in it."
Are they right — and how does that differ from a 95% *confidence* interval?

:::{dropdown} Show answer
For a {term}`credible interval` they are (essentially) right — *given the prior and data*, the
{term}`posterior probability` that $\theta$ is inside is 95%; it is a statement about $\theta$. A
frequentist {term}`confidence interval` does **not** support that sentence: its 95% is a property of the
*procedure* over repeated samples, not of the one interval in hand. The credible reading buys the direct
probability statement at the cost of committing to a {term}`prior`.
:::

**Q3.** Why does the Jeffreys credible interval end up with good *frequentist* coverage, despite being a
Bayesian construction?

:::{dropdown} Show answer
The Jeffreys {term}`prior` is a *matching prior*: derived from an invariance principle, it makes the
resulting credible intervals track their nominal {term}`coverage` under repeated sampling. Asymptotically,
**Bernstein–von Mises** ensures the {term}`posterior` becomes {term}`normal distribution`-shaped around the
{term}`maximum likelihood estimate`, so credible and confidence intervals coincide; Jeffreys keeps coverage
close to nominal even at small $n$. Measured at $n=40$, its coverage matches Wilson's almost exactly.
:::

---

:::{admonition} Terms used on this page
:class: seealso
{term}`theta` · {term}`Bayesian` · {term}`prior` · {term}`posterior` · {term}`Beta distribution` ·
{term}`conjugate prior` · {term}`binomial` · {term}`maximum likelihood estimate` · {term}`posterior mean` ·
{term}`credible interval` · {term}`highest posterior density interval` · {term}`quantile` ·
{term}`posterior probability` · {term}`coverage` · {term}`confidence interval` · {term}`normal distribution`
:::

*New here? Start at {doc}`the foundations <../foundations/index>`. Previous: {doc}`transformed intervals
<05_transformed_intervals>`. Next in the series: coverage theory — what the oscillating curves really mean.*
