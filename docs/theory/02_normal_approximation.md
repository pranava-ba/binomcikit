---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# The normal approximation, and why Wald fails

The previous page framed the goal: turn a count $x$ out of $n$ into a range of plausible values for the
true rate {term}`theta`. This page builds the **first, simplest** interval — the {doc}`Wald
<../methods/wald>` interval — from the {term}`central limit theorem`, and then shows, with numbers you
can reproduce, the two distinct ways it breaks. Understanding *why* it breaks is the motivation for
every other method in the library.

Every code block on this page is **executed when the docs are built**, so the tables and numbers you
see are produced by the real package.

## Where Wald comes from

Write the observed {term}`proportion` as $\hat p = x/n$. Each trial is a {term}`Bernoulli trial` with
success probability $\theta$, so $x$ is a sum of $n$ independent 0/1 variables. The **central limit
theorem** says a sum of many independent pieces is approximately {term}`normal distribution`-shaped, so
for large $n$

$$\hat p \;\approx\; \text{Normal}\!\left(\theta,\; \frac{\theta(1-\theta)}{n}\right).$$

Standardise and invert, and you get a symmetric interval centred on $\hat p$:

$$\hat p \;\pm\; z_{1-\alpha/2}\,\sqrt{\frac{\hat p\,(1-\hat p)}{n}},$$

where $z_{1-\alpha/2}\approx 1.96$ for 95%. That is the Wald interval. It is one line of algebra, which
is exactly why it is taught first — and, as we will see, why it misbehaves.

```{code-cell} python
import binomcikit as bk

# Wald 95% interval for every possible count x = 0..5, when n = 5:
bk.ciwd(5, 0.05)
```

Read the `LWD`/`UWD` columns (the lower and upper limits). Two rows already look wrong — keep them in
mind: **x = 0 gives `[0, 0]`** and **x = 5 gives `[1, 1]`**. We return to those below.

## Failure 1 — the shortcut in the standard error

The CLT statement above uses the **true** variance $\theta(1-\theta)/n$. But $\theta$ is unknown, so
Wald plugs in the estimate $\hat p$ and uses $\hat p(1-\hat p)/n$ instead. That plug-in is a
{term}`maximum likelihood estimate` of the {term}`standard error`, and it is where the honesty leaks
out: near the edges $\hat p(1-\hat p)$ is *too small*, so the interval is *too narrow*, so it misses
$\theta$ more often than the promised 5%.

We can measure that directly. binomcikit's coverage engine computes the **true** {term}`coverage` — how
often the interval actually traps $\theta$ — by averaging over the binomial distribution:

```{code-cell} python
# Mean and minimum true coverage of the Wald interval at n = 20 (nominal 0.95):
bk.covpwd(20, 0.05, a=1, b=1, t1=0.93, t2=0.97, seed=0)[["mcp", "micp"]]
```

The **mean coverage `mcp`** sits *below* 0.95, and the **minimum coverage `micp`** is far below it — at
some values of $\theta$ the "95%" interval covers only a fraction of the time. A 95% procedure that
routinely delivers less than 95% is the core defect.

:::{dropdown} The delta method — why the plug-in variance is the culprit
For a smooth function $g$, the {term}`delta method` says $\operatorname{Var}(g(\hat p)) \approx
g'(\theta)^2\,\operatorname{Var}(\hat p)$. Wald takes $g$ to be the identity, so it needs
$\operatorname{Var}(\hat p)=\theta(1-\theta)/n$ evaluated **at $\theta$**. Replacing $\theta$ with
$\hat p$ is a second approximation stacked on the CLT, and the error is worst exactly where
$\theta(1-\theta)$ changes fastest — near 0 and 1. Methods that avoid this shortcut do so in different
ways: **Wilson** keeps $\theta$ (not $\hat p$) inside the standard error and solves a quadratic;
**arcsine** and **logit** first transform to a scale where the variance no longer depends on $\theta$.
:::

## Failure 2 — collapse at the boundary

The second failure is not statistical subtlety, it is arithmetic. At $x = 0$, $\hat p = 0$, so the
standard error $\sqrt{\hat p(1-\hat p)/n} = 0$, and the interval degenerates to the single point
$[0, 0]$ — a **{term}`zero-width interval`**. It claims *perfect certainty* that $\theta = 0$ from a
sample that is perfectly consistent with, say, $\theta = 0.1$.

```{code-cell} python
n = 5
wald = bk.ciwd(n, 0.05)
zero_width = wald.loc[wald["LWD"] == wald["UWD"], ["x", "LWD", "UWD", "ZWI"]]
zero_width
```

The `ZWI` flag marks it. This is the clearest symptom of Wald's weakness, and it is common: with small
$n$, seeing zero (or all) successes is not unusual, and precisely then the interval is useless.

## What the fixes will do

Everything else in the library is a response to one or both failures:

| Fix | Failure it targets | How |
|---|---|---|
| {doc}`Wilson <../methods/wilson>` | the standard-error shortcut | evaluate the SE at $\theta$; solve a quadratic |
| {doc}`ArcSine <../methods/arcsine>`, {doc}`Logit <../methods/logit>` | the standard-error shortcut | transform to a variance-stabilised scale |
| {doc}`Agresti–Coull <../method_selection>` | boundary collapse | add pseudo-counts so $\hat p$ is never exactly 0 or 1 |
| {doc}`Exact & Blaker <../methods/exact>` | both | drop the normal approximation entirely |

You can watch the improvement in a single call — Wald sagging below the line, Wilson tracking it:

```{code-cell} python
# The numbers behind the coverage figure (coverage of each method vs the true theta):
cov = bk.coverage_curve(20, method="wald").rename(columns={"coverage": "wald"})
cov["wilson"] = bk.coverage_curve(20, method="wilson")["coverage"]
cov.iloc[::40].round(3)          # a slice of the full curve
```

Across the sampled points, `wald` dips well under 0.95 while `wilson` stays close to it — the visual
version is on the {doc}`Wald page <../methods/wald>`. The next pages build these fixes properly, starting
with **test inversion** — the idea behind Wilson and the likelihood-ratio interval.

## Check yourself

**Q1.** In one sentence, what *two* approximations does the Wald interval stack on top of each other?

:::{dropdown} Show answer
(1) The {term}`central limit theorem` — treating the {term}`proportion` $\hat p$ as
{term}`normal distribution`-shaped; and (2) the plug-in — evaluating the {term}`standard error` at
$\hat p$ instead of at the true $\theta$. The second is what makes coverage worst near 0 and 1.
:::

**Q2.** You survey 8 people and 0 say "yes." What interval does Wald give, and why is it indefensible?
Check your reasoning against the code.

:::{dropdown} Show answer
```python
import binomcikit as bk
bk.ciwd(8, 0.05).iloc[0]   # the x = 0 row
```
It returns `[0, 0]` — a {term}`zero-width interval`. The standard error √(p̂(1−p̂)/n) is 0 when p̂ = 0,
so the interval collapses to a point and claims θ is *exactly* 0, though the data are perfectly
consistent with θ = 0.2 or more.
:::

**Q3.** Wald's mean coverage at n = 20 comes out *below* 0.95. Is a method that under-covers more
dangerous than one that over-covers? Why?

:::{dropdown} Show answer
Usually yes. Under-covering means your "95% interval" traps the truth *less* than 95% of the time — you
are **overconfident**, and decisions based on it fail more often than advertised. Over-covering (e.g.
Clopper–Pearson) is merely wasteful — the interval is wider than needed but still honest. Being too sure
is worse than being too cautious.
:::

---

:::{admonition} Terms used on this page
:class: seealso
{term}`proportion` · {term}`theta` · {term}`Bernoulli trial` · {term}`central limit theorem` ·
{term}`normal distribution` · {term}`standard error` · {term}`maximum likelihood estimate` ·
{term}`delta method` · {term}`coverage` · {term}`zero-width interval`
:::
