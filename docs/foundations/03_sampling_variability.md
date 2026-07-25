---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Sampling variability

## In words

Here is the fact that makes statistics necessary at all: **run the same experiment twice and you get two
different answers.** Poll 20 people today and 6 say yes ($\hat p = 0.30$); poll 20 *different* people
tomorrow and 8 say yes ($\hat p = 0.40$). Nothing changed about the true rate — the wobble is just the
luck of *which* 20 people you happened to sample. This wobble is **sampling variability**, and it is not
a nuisance to be apologised for; it is the thing a confidence interval is built to describe.

Two things are worth pinning down. First, *how big* is the wobble? Second, and more usefully, *how fast
does it shrink* as you collect more data? The answers are simple, exact, and the reason more data helps.

## The symbols

| Symbol | Reads as | Means |
|---|---|---|
| $\theta$ | "theta" | the true rate — fixed while we sample (here 0.3) |
| $\hat p$ | "p-hat" | the {term}`estimate` from one sample; a {term}`random variable`, it changes sample to sample |
| $n$ | "n" | the sample size |
| $\operatorname{SE}(\hat p)$ | "standard error" | the typical size of the wobble in $\hat p$ |

## Definition

The spread of $\hat p$ across repeated samples has an exact formula, the **{term}`standard error`**:

$$\operatorname{SE}(\hat p) \;=\; \sqrt{\dfrac{\theta(1-\theta)}{n}}.$$

Two readings of it carry the whole lesson. The wobble grows with $\theta(1-\theta)$ — largest at
$\theta = 0.5$, smallest near the edges. And it shrinks like $1/\sqrt{n}$: to **halve** the wobble you
need **four times** the data. That $\sqrt{n}$ is why precision is expensive, and why "just collect a bit
more" has diminishing returns.

## Examples

Draw ten samples of size 20 from a true rate of $\theta = 0.3$ and look at the ten estimates. They
scatter around 0.3 — none is "wrong," they are just different draws:

```{code-cell} python
import numpy as np

rng = np.random.default_rng(0)          # seeded, so these numbers are reproducible
samples = rng.binomial(n=20, p=0.3, size=10)
[round(x / 20, 2) for x in samples]     # ten values of p-hat
```

Now draw 100 000 samples and compare the *actual* spread to the formula. The match is the point:

```{code-cell} python
theta, n = 0.3, 20
phat = rng.binomial(n, theta, size=100_000) / n
simulated_sd = phat.std()
formula_se = np.sqrt(theta * (1 - theta) / n)
{"mean of p-hat": round(phat.mean(), 4),
 "simulated spread": round(simulated_sd, 4),
 "formula SE": round(formula_se, 4)}
```

The mean of $\hat p$ sits on $\theta = 0.3$ (the estimate is unbiased), and the simulated spread matches
$\sqrt{0.3 \times 0.7 / 20} \approx 0.1025$ almost exactly. Here is the whole distribution of $\hat p$ —
one true rate, a hundred thousand samples, and where they land:

```{figure} ../_static/foundations_sampling.png
:alt: Histogram of p-hat over 100000 samples of size 20 from theta = 0.3
:width: 100%

Sampling variability made visible. Every sample has the *same* true rate $\theta = 0.3$ (orange line),
yet $\hat p$ ranges from below 0.1 to above 0.5. The histogram is centred on $\theta$ with a spread of
about $0.10$ — exactly the {term}`standard error`. A confidence interval is, in effect, a ruler sized to
this spread.
```

The $1/\sqrt{n}$ shrinkage, made concrete — quadruple $n$, halve the wobble:

```{code-cell} python
theta = 0.3
{n: round(np.sqrt(theta * (1 - theta) / n), 4) for n in [20, 80, 320, 1280]}
```

Each fourfold jump in $n$ roughly halves the {term}`standard error` (0.1025 → 0.0512 → 0.0256 → 0.0128).

## Check yourself

**Q1.** At which true rate is $\hat p$ *most* variable for a fixed $n$: $\theta = 0.1$, $0.5$, or $0.9$?

:::{dropdown} Show answer
$\theta = 0.5$. The {term}`standard error` is $\sqrt{\theta(1-\theta)/n}$, and $\theta(1-\theta)$ is
largest at $0.5$ (giving $0.25$) and smaller toward the edges ($0.1 \times 0.9 = 0.09$). A 50/50 rate is
the hardest to estimate precisely; rates near 0 or 1 wobble less.
:::

**Q2.** You have $n = 100$ and want to *halve* your standard error. How many observations do you need?

:::{dropdown} Show answer
**400.** The {term}`standard error` shrinks like $1/\sqrt{n}$, so halving it needs $2^2 = 4$ times the
data. Going from 100 to 200 only shrinks it by a factor of $\sqrt{2} \approx 1.41$, not 2.
```python
import numpy as np
np.sqrt(0.5 * 0.5 / 100), np.sqrt(0.5 * 0.5 / 400)   # -> 0.05, 0.025
```
:::

**Q3.** Someone says "my sample gave $\hat p = 0.34$, so the true rate is 0.34." What is wrong with that?

:::{dropdown} Show answer
It ignores sampling variability. $\hat p = 0.34$ is *one draw* from a distribution centred on the
unknown {term}`theta` with spread $\operatorname{SE}(\hat p)$; a different sample would give a different
number. The honest statement is a **range** around 0.34 wide enough to account for that wobble — a
{term}`confidence interval`, which the {doc}`next page <04_confidence_interval>` builds.
:::

---

:::{admonition} Terms used on this page
:class: seealso
{term}`theta` · {term}`estimate` · {term}`random variable` · {term}`standard error` ·
{term}`confidence interval`
:::

*New here? Back to {doc}`the proportion <01_proportion>`. Next: {doc}`what a confidence interval really
means <04_confidence_interval>`. Deeper: {doc}`the normal approximation <../theory/02_normal_approximation>`.*
