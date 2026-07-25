---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# A proportion, and its estimate

## In words

Almost every question this package answers has the same shape: *out of a group, what fraction has some
property?* What fraction of visitors click the button, of parts are defective, of patients recover, of
coins land heads. That underlying fraction — the one you would get if you could measure *everyone*,
forever — is a fixed number you never actually see. Call it the **true rate**.

What you *do* see is one sample: you tried the button on 40 visitors, 14 clicked. The fraction in that
sample, $14/40 = 0.35$, is your best guess at the true rate — but it is a *guess from a sample*, not the
true rate itself. Run the experiment again tomorrow with 40 different visitors and you would get a
slightly different fraction. Keeping these two ideas apart — the fixed truth you want, and the wobbly
estimate you have — is the first and most important step.

## The symbols

| Symbol | Reads as | Means |
|---|---|---|
| $\theta$ | "theta" | the **true rate** — the fixed, unknown fraction we want to know |
| $n$ | "n" | the number of trials in our sample (here 40) |
| $x$ | "x" | the number of successes we counted (here 14) |
| $\hat p$ | "p-hat" | the **estimate** of $\theta$ from the sample, $x/n$ |

The little hat on $\hat p$ is the convention for "estimated from data." It is a signal to stay humble:
$\hat p$ is what the sample told us, not the truth {term}`theta` itself.

## Definition

$$\hat p \;=\; \frac{x}{n}.$$

Here {term}`theta` is the true {term}`proportion` we are estimating; $x$ is the {term}`success` count; $n$
is the number of {term}`Bernoulli trial`s; and $\hat p$ is the observed proportion — the
{term}`estimate` of $\theta$. That is the whole formula. It is also, it turns out, the
{term}`maximum likelihood estimate` — the value that makes the data you saw most probable — which is why
it is the natural choice and not just an obvious one. (The {doc}`theory track <../theory/01_the_problem>`
proves that.)

## Examples

```{code-cell} python
import binomcikit as bk

# 14 of 40 visitors clicked — the estimated click rate:
bk.point_estimate(14, 40, "mle")
```

```{code-cell} python
# Same fraction, wildly different amounts of evidence.
# 3/5 and 300/500 both estimate 0.6 — but the second is far more trustworthy.
bk.point_estimate(3, 5, "mle"), bk.point_estimate(300, 500, "mle")
```

That second example is the seed of everything that follows: a point estimate on its own hides *how sure*
you are. Both give $\hat p = 0.6$, yet 3-out-of-5 is a shrug and 300-out-of-500 is strong evidence. To
carry that missing information we will need a whole **interval**, not a single number — which is the
subject of {doc}`page 4 <04_confidence_interval>`.

```{code-cell} python
# The boundary case: 0 successes. The estimate is 0 — but is the true rate really 0?
bk.point_estimate(0, 20, "mle")
```

Seeing 0 of 20 gives $\hat p = 0$, yet a true rate of, say, 0.05 would produce zero successes in 20
trials quite often. So "$\hat p = 0$" must not be read as "$\theta = 0$." This gap between the estimate
and the truth at the boundary is where the simplest interval method breaks, as you will see on the
{doc}`Wald page <../methods/wald>`.

## Check yourself

**Q1.** A factory inspects 250 parts and finds 8 defective. What is $\hat p$, and what does it estimate?

:::{dropdown} Show answer
$\hat p = 8/250 = \mathbf{0.032}$. It is the {term}`estimate` of $\theta$, the factory's *true* long-run
defect rate — the fraction we would see if we could inspect every part ever made. $\hat p$ is our best
single guess at $\theta$ from this sample, not $\theta$ itself.
```python
bk.point_estimate(8, 250, "mle")   # -> 0.032
```
:::

**Q2.** Two surveys both report $\hat p = 0.5$: one from 4 people, one from 4000. Are they equally
informative? Why or why not?

:::{dropdown} Show answer
No. Both estimate {term}`theta` as 0.5, but the survey of 4000 pins it down far more tightly — 2-of-4 is
easily produced by many true rates, while 2000-of-4000 is not. The point {term}`estimate` is identical;
the *uncertainty* around it is completely different, and only an interval (later pages) shows that.
:::

**Q3.** True or false: if $\hat p = 0$, then the true rate $\theta$ must be 0.

:::{dropdown} Show answer
**False.** A small positive rate can easily yield zero successes in a limited sample — 0 of 20 is
perfectly consistent with $\theta = 0.05$. The {term}`estimate` landing on the boundary does not push the
truth onto the boundary; this is exactly the trap the {term}`zero-width interval` falls into.
:::

---

:::{admonition} Terms used on this page
:class: seealso
{term}`proportion` · {term}`theta` · {term}`estimate` · {term}`success` · {term}`Bernoulli trial` ·
{term}`maximum likelihood estimate` · {term}`zero-width interval`
:::

*Next: {doc}`where the count $x$ comes from <02_binomial>` — trials and the binomial distribution.*
