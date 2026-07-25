---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Quality control: is the defect rate below 1%?

**The situation.** Your contract promises a defect rate under **1%**. You pull a random sample of **500**
units off the line and find **2** defective. The observed rate, 0.4%, is comfortably under 1% — but with
only 2 defects, how sure can you be that the *true* rate clears the bar?

**The question.** Not "what is the interval?" but a **decision**: *how much confidence do I have that
θ < 1%?* That phrasing is a hint that the {doc}`Bayesian <../theory/06_bayesian_view>` tools fit best — they
turn the data into a direct probability about θ.

## Choosing a method

Two complementary reads:

1. A {term}`confidence interval` (Wilson) — the frequentist range of plausible rates.
2. A {term}`posterior probability` — with a {term}`Beta distribution` {term}`prior`, compute
   $\Pr(\theta < 0.01 \mid \text{data})$ directly. This answers the decision question in one number.

## Running it

First the confidence interval:

```{code-cell} python
import binomcikit as bk

bk.ci(2, 500)      # Wilson 95% interval for 2 defects in 500
```

Now the posterior. With a uniform {term}`prior`, {term}`conjugate prior` arithmetic gives a
$\text{Beta}(1+2,\,1+498) = \text{Beta}(3, 499)$ posterior; the chance the true rate is below 1% is the
posterior probability mass to the left of 0.01:

```{code-cell} python
from scipy.stats import beta

post = bk.posterior(2, 500, a=1, b=1)          # Beta(3, 499)
p_below_uniform = beta.cdf(0.01, post["a_post"], post["b_post"])

postJ = bk.posterior(2, 500, a=0.5, b=0.5)     # Jeffreys prior -> Beta(2.5, 498.5)
p_below_jeffreys = beta.cdf(0.01, postJ["a_post"], postJ["b_post"])

{"P(theta < 1%), uniform prior":  round(float(p_below_uniform), 3),
 "P(theta < 1%), Jeffreys prior": round(float(p_below_jeffreys), 3)}
```

## Reading the result

Two facts that seem to disagree but do not:

- The **95% confidence interval** runs to about **1.4%** on the upper end — it *includes* values above 1%.
  So at the 95% level you **cannot** declare "θ < 1%": the data are still consistent with a rate slightly
  over the threshold.
- The **posterior probability** that θ < 1% is about **88%** (uniform prior) to **93%** (Jeffreys). Most of
  your belief sits under the bar, but not overwhelmingly.

Both are correct; they answer different questions. The interval asks "which rates can I not rule out at
95%?"; the posterior asks "what's the probability I'm under the limit?" For a *decision*, the posterior is
the more direct input — and 88% may or may not be good enough depending on the cost of being wrong.

```{figure} ../_static/tutorial_qc.png
:alt: Posterior Beta(3,499) with the region below 1% shaded
:width: 100%

The posterior for the true defect rate after seeing 2 in 500. The shaded area to the left of the 1% line
is $\Pr(\theta < 1\%) \approx 88\%$. Notice the posterior has real mass *above* 1% too — which is why the
95% interval's upper limit crosses the threshold.
```

## How to report it

> In a sample of 500 units, 2 were defective (0.4%; Wilson 95% CI 0.1–1.4%). Under a uniform prior, the
> posterior probability that the true defect rate is below the 1% contractual limit is 88%. The interval
> does not exclude rates slightly above 1%, so a larger sample is advisable before certifying conformance.

## What could go wrong

- **Reading the CI as a probability.** "95% CI up to 1.4%" is *not* "1.4% chance of exceeding..." — that
  frequentist interval makes no probability statement about this θ. Only the {term}`posterior probability`
  does, and only relative to a stated {term}`prior`.
- **Prior sensitivity at small counts.** With just 2 defects the answer moves with the prior (88% vs 93%).
  Report the prior you used; if a stakeholder objects, the Jeffreys prior is the standard neutral default.
- **One-sided vs two-sided.** You only care about the *upper* side (is θ too high?), so a one-sided 95%
  bound is the natural frequentist companion to the posterior — see {doc}`the zero-events tutorial
  <zero_events>` for how binomcikit produces one.

## Try it yourself

Your supplier improves and the next sample of 500 has **0** defects. What is $\Pr(\theta < 1\%)$ now under
a uniform prior?

:::{dropdown} Solution
```python
import binomcikit as bk
from scipy.stats import beta
post = bk.posterior(0, 500, a=1, b=1)          # Beta(1, 501)
beta.cdf(0.01, post["a_post"], post["b_post"])  # -> about 0.993
```
About **99.3%** — with zero defects the posterior piles up near 0 and almost all the belief clears the 1%
bar. The evidence is now strong, even though *one* clean sample can never make it a certainty.
:::

---

:::{admonition} Terms used on this page
:class: seealso
{term}`confidence interval` · {term}`posterior` · {term}`posterior probability` · {term}`prior` ·
{term}`conjugate prior` · {term}`Beta distribution` · {term}`Bayesian`
:::

*See also: {doc}`The Bayesian toolbox <../bayesian_toolbox>` · {doc}`The Bayesian view (theory)
<../theory/06_bayesian_view>` · {doc}`Zero events <zero_events>`.*
