---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# What a confidence interval really means

## In words

This is the most misunderstood idea in statistics, so we will not just assert it — we will *simulate* it
and watch it happen.

A **95% confidence interval** is **not** "there is a 95% chance the true rate is inside *this*
interval." Once you have computed a specific interval like $[0.22, 0.51]$, the true rate either is in it
or it is not — there is no chance left to speak of. The "95%" describes the **procedure, not the
interval**: if you repeated the whole experiment many times, building a fresh interval each time, about
95% of *those* intervals would contain the true rate. It is a statement about the *factory* that makes
intervals, not about any single interval that rolls off the line.

The mental picture: each experiment produces one interval, drawn as a horizontal bar. Stack up the bars
from many experiments and draw a vertical line at the true rate. A good 95% method is one where about 95%
of the bars cross that line — and, crucially, you never know *which* of your own bars is one of the
unlucky 5% that miss.

## The symbols

| Symbol | Reads as | Means |
|---|---|---|
| $\theta$ | "theta" | the true rate (in the simulation we *set* it, so we can check who covers) |
| $[L(x), U(x)]$ | "L to U" | the interval the method returns for an observed count $x$ |
| $1-\alpha$ | "one minus alpha" | the {term}`confidence level` promised, e.g. 0.95 |
| $\alpha$ | "alpha" | the allowed miss rate, e.g. 0.05 |

## Definition

An interval procedure has {term}`confidence level` $1-\alpha$ if, across repeated samples from any fixed
$\theta$,

$$\Pr\!\big(\,L(X) \le \theta \le U(X)\,\big) \;\ge\; 1-\alpha.$$

Read the probability as "over repeated experiments." $L(X)$ and $U(X)$ are random — they move with the
data — while $\theta$ stays put; the interval is what jiggles across that fixed target. A
{term}`confidence interval` keeps its promise when this holds; whether it *actually* does is
{term}`coverage`, the {doc}`next page <05_coverage>`.

## Examples

Let us *be* the true rate. Set $\theta = 0.3$, $n = 40$, and run 40 experiments. For each, we draw a
count and build the {doc}`Wilson <../methods/wilson>` interval, then check whether it traps $0.3$:

```{code-cell} python
import numpy as np
import binomcikit as bk

theta, n, N = 0.3, 40, 40
rng = np.random.default_rng(42)
counts = rng.binomial(n, theta, size=N)

grid = bk.cisc(n, 0.05).set_index("x")          # Wilson limits for every possible count
lo = grid.loc[counts, "LSC"].to_numpy()
hi = grid.loc[counts, "USC"].to_numpy()
covers = (lo <= theta) & (theta <= hi)

int(covers.sum()), N                            # how many of the 40 trapped the truth
```

38 of the 40 intervals contain $\theta = 0.3$. Look at the first three experiments individually — each
is a perfectly ordinary interval; nothing marks the ones that will miss:

```{code-cell} python
import pandas as pd
pd.DataFrame({
    "x": counts[:3],
    "lower": lo[:3].round(3),
    "upper": hi[:3].round(3),
    "covers 0.3?": covers[:3],
})
```

Stacking all 40 as bars gives the picture the definition is really about:

```{figure} ../_static/foundations_ci_repeated.png
:alt: 40 confidence intervals from 40 experiments, with the true theta marked
:width: 100%

40 experiments, 40 Wilson intervals, true $\theta = 0.3$ (dashed line). **38 bars cross the line**
(blue); **2 miss** (orange) — one landing entirely above 0.3, one entirely below. Each experiment saw
only its own bar and could not tell whether it was lucky. "95% confident" means *this* — about 19 in 20
of the bars catch the truth — not that any single bar is 95% right.
```

Forty experiments is too few to land on exactly 95%. Push it to 10 000 and the fraction settles down:

```{code-cell} python
theta, n, N = 0.3, 40, 10_000
rng = np.random.default_rng(7)
counts = rng.binomial(n, theta, size=N)
lo = grid.loc[counts, "LSC"].to_numpy()
hi = grid.loc[counts, "USC"].to_numpy()
round(float(np.mean((lo <= theta) & (theta <= hi))), 4)
```

About **0.944** — close to the promised 0.95, but not exactly it. That small gap is not sampling noise;
it is real, and it depends on $\theta$. Explaining *why* a careful 95% method still does not deliver
exactly 95% is the whole point of the {doc}`next page <05_coverage>`.

:::{dropdown} "95% chance the truth is in my interval" — why it is wrong, carefully
Before you run the experiment, the *random* interval $[L(X), U(X)]$ has a 95% chance of covering
$\theta$ — that statement is fine, because $L(X)$ and $U(X)$ are still random. **After** you observe
$x = 14$ and compute $[0.22, 0.51]$, nothing is random any more: $\theta$ is a fixed number and either
sits in $[0.22, 0.51]$ or does not. The 95% lived in the randomness of the *procedure*, and you spent it
when you looked at the data. To attach a probability to *this* interval you must adopt the
{term}`Bayesian` view and a {term}`prior`, which yields a {term}`credible interval` — a genuinely
different object with a genuinely different meaning. Both are in this library; the {doc}`Bayesian toolbox
<../bayesian_toolbox>` covers the credible-interval reading.
:::

## Check yourself

**Q1.** You compute a single 95% interval $[0.18, 0.42]$. Is the statement "there's a 95% probability
$\theta$ is between 0.18 and 0.42" correct?

:::{dropdown} Show answer
No (in the frequentist sense these intervals use). Once computed, the interval is fixed and $\theta$ is
fixed, so $\theta$ is either in it or not — no probability remains. The 95% refers to the *procedure*:
over many experiments, about 95% of the intervals it builds cover $\theta$. A probability *about this
particular interval* requires a {term}`Bayesian` {term}`credible interval`.
:::

**Q2.** In the simulation, 2 of 40 intervals missed $\theta$. Does a miss mean the method failed?

:::{dropdown} Show answer
No — misses are *expected*. A 95% method is *supposed* to miss about 5% of the time; 2 of 40 (5%) is
right on target. A method that never missed would be over-covering — its intervals wider than necessary.
The misses are the price of intervals that are not needlessly wide.
:::

**Q3.** Re-run the 10 000-experiment simulation with $\theta = 0.5$ instead of $0.3$. Roughly what
covered fraction do you expect, and is it exactly 0.95?

:::{dropdown} Show answer
Somewhere close to 0.95 but not exactly — likely a bit above, since Wilson tends to slightly over-cover
near $\theta = 0.5$ at this $n$. The exact value depends on $\theta$ because of {term}`discreteness`
(next page). Try it:
```python
import numpy as np, binomcikit as bk
grid = bk.cisc(40, 0.05).set_index("x")
rng = np.random.default_rng(7)
counts = rng.binomial(40, 0.5, size=10_000)
lo = grid.loc[counts, "LSC"].to_numpy(); hi = grid.loc[counts, "USC"].to_numpy()
np.mean((lo <= 0.5) & (0.5 <= hi))
```
:::

---

:::{admonition} Terms used on this page
:class: seealso
{term}`theta` · {term}`confidence interval` · {term}`confidence level` · {term}`alpha` ·
{term}`coverage` · {term}`Bayesian` · {term}`prior` · {term}`credible interval` · {term}`discreteness`
:::

*New here? Back to {doc}`sampling variability <03_sampling_variability>`. Next: {doc}`coverage — the
promise kept or broken <05_coverage>`. Deeper: {doc}`the estimation problem <../theory/01_the_problem>`.*
