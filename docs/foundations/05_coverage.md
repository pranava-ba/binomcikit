---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Coverage — the promise kept or broken

## In words

The last page said a 95% method should trap the truth about 95% of the time. **Coverage** is that
"about 95%" made exact and measurable: for a given true rate, the fraction of samples whose interval
actually contains it. It is the single number that says whether a method keeps its promise — and,
because the count is a whole number, we can compute it *exactly*, no simulation needed, by summing over
the {doc}`binomial distribution <02_binomial>` from page 2.

Here is the twist that motivates this entire package. You would hope a well-built 95% method has coverage
sitting flat at 0.95 for every true rate. It does not. Coverage **wobbles** as the true rate moves —
sometimes above 0.95, sometimes below — because the count can only land on whole numbers. The bad methods
wobble far below the line and stay there; the good ones hug it. You cannot see this from a formula or a
single dataset. You have to *measure* it, which is what `binomcikit` is built to do.

## The symbols

| Symbol | Reads as | Means |
|---|---|---|
| $\theta$ | "theta" | a true rate we evaluate the method at |
| $1-\alpha$ | "one minus alpha" | the {term}`confidence level` promised (nominal), e.g. 0.95 |
| $\alpha$ | "alpha" | the promised miss rate, e.g. 0.05 |
| $[L(x), U(x)]$ | "L to U" | the interval the method returns for count $x$ |
| $\text{Coverage}(\theta)$ | "coverage at theta" | the true fraction of samples whose interval covers $\theta$ |

**Nominal** is the level you asked for ($1-\alpha$); **coverage** is what you actually get. A method is
good when the second stays close to the first.

## Definition

$$\text{Coverage}(\theta) \;=\; \sum_{x=0}^{n} \mathbf{1}\!\left[\,L(x) \le \theta \le U(x)\,\right]\;
\binom{n}{x}\,\theta^{x}(1-\theta)^{\,n-x}.$$

In words: for every possible count $x$, check whether that count's interval traps $\theta$ (the
indicator $\mathbf{1}[\cdot]$ is 1 if yes, 0 if no); weight it by how likely that count is under $\theta$
— its {term}`binomial` {term}`probability`; add them up. This is an exact sum over the finitely many
counts, using the {term}`confidence level` as the target. A method **achieves nominal coverage** when
$\text{Coverage}(\theta) \ge 1-\alpha$.

## Examples

Compute coverage the way the formula says — by hand-summing the binomial — for Wilson at $\theta = 0.3$,
$n = 40$. Notice the result matches the 10 000-experiment simulation from the {doc}`previous page
<04_confidence_interval>` (it estimated exactly this number):

```{code-cell} python
from math import comb
import binomcikit as bk

def coverage(theta, n, grid, lcol, ucol):
    g = grid.set_index("x")
    return float(sum(
        comb(n, x) * theta**x * (1 - theta) ** (n - x)
        for x in range(n + 1)
        if g.loc[x, lcol] <= theta <= g.loc[x, ucol]
    ))

wilson = bk.cisc(40, 0.05)
round(coverage(0.30, 40, wilson, "LSC", "USC"), 4)      # -> 0.9443, matching the simulation
```

Now the wobble. Evaluate the *same* method at three nearby true rates and watch coverage move even though
nothing about the method changed:

```{code-cell} python
{theta: round(coverage(theta, 40, wilson, "LSC", "USC"), 4)
 for theta in [0.20, 0.25, 0.30]}
```

Coverage swings from below 0.93 to above 0.95 over a tiny change in $\theta$. That jaggedness is
{term}`discreteness` — the count jumps at whole numbers, so the interval's endpoints do too. No method
can hold *exactly* 0.95 everywhere; the goal is to stay *near* it.

`binomcikit` sweeps the whole range of $\theta$ for you and summarises it. Compare the honest Wilson
default against Wald:

```{code-cell} python
import pandas as pd
summary = {
    m: bk.coverage_curve(40, method=m)["coverage"].agg(["mean", "min"]).round(3).to_dict()
    for m in ["wilson", "wald"]
}
pd.DataFrame(summary).T          # mean and worst-case coverage across theta
```

Two numbers tell the story. Wilson's **mean** coverage sits at 0.95 with a worst case of 0.92 — it wobbles
but stays honest. Wald averages 0.89 and its **minimum** collapses toward 0 (the {term}`zero-width
interval` at the edges). The picture:

```{figure} ../_static/foundations_coverage.png
:alt: Coverage of Wald and Wilson against the true rate at n = 40
:width: 100%

Actual {term}`coverage` versus the true rate at $n = 40$, nominal 95% (dashed). **Wilson** (blue) wobbles
tightly around the line; **Wald** (orange) sags well below it, worst near 0 and 1. The wobble in *both*
is {term}`discreteness`; the *systematic sag* in Wald is its real defect. This gap is why the library
offers many methods and, above all, the tools to measure them.
```

:::{dropdown} Over-covering is not "extra safe"
It is tempting to want coverage always *above* 0.95 — surely more is safer? But coverage far above
nominal (like {term}`Clopper–Pearson`, which guarantees $\ge 0.95$ everywhere) is bought with **wider
intervals** than the problem needs — you lose precision to buy safety you did not ask for. The ideal is
coverage *close to* 0.95, wobbling gently around it, not pinned above it. "Good" means honest **and**
sharp, which is the {term}`expected length` trade-off the {doc}`method-selection guide
<../method_selection>` weighs.
:::

## Check yourself

**Q1.** A method reports mean coverage 0.995 at $n = 20$. Is that better than one reporting 0.951?

:::{dropdown} Show answer
Not for a 95% target — 0.995 is *over*-covering. It means the intervals are wider than necessary
(conservative), spending precision to exceed a promise you only needed to *meet*. Coverage of 0.951 is
closer to the goal. The aim is *near* nominal, not far above it; being too cautious costs
{term}`expected length`.
:::

**Q2.** Why can no binomial interval method have coverage exactly 0.95 at *every* $\theta$?

:::{dropdown} Show answer
Because of {term}`discreteness`: the count $X$ takes only whole values $0, 1, \dots, n$, so an interval's
endpoints — and therefore which counts "cover" a given $\theta$ — jump abruptly as $\theta$ moves.
$\text{Coverage}(\theta)$ is a step function that can only take finitely many values, so it cannot equal
0.95 continuously. The best a method can do is oscillate close to nominal.
:::

**Q3.** Using the `coverage` function above, is Wald's coverage at $\theta = 0.3$, $n = 40$ above or
below nominal? Compute it.

:::{dropdown} Show answer
Below — about **0.930**, under the 0.95 promise.
```python
wald = bk.ciwd(40, 0.05)
coverage(0.30, 40, wald, "LWD", "UWD")      # -> 0.9299
```
Wald under-covers here, and far worse near the boundaries; Wilson at the same point was 0.944.
:::

---

You now have the whole arc: a true rate $\theta$ you cannot see, an estimate $\hat p$ that wobbles by
$1/\sqrt{n}$, an interval that trades width against catching the truth, and **coverage** as the yardstick
for whether it does. From here, open any {doc}`method page <../methods/index>` to meet a specific
interval, use {doc}`../method_selection` to choose one, or go to the {doc}`../theory/index` track for the
mathematics behind each construction.

:::{admonition} Terms used on this page
:class: seealso
{term}`theta` · {term}`confidence level` · {term}`alpha` · {term}`coverage` · {term}`binomial` ·
{term}`probability` · {term}`discreteness` · {term}`expected length` · {term}`zero-width interval` ·
{term}`Clopper–Pearson`
:::

*New here? Back to {doc}`what a confidence interval means <04_confidence_interval>`. Go deeper:
{doc}`../evaluating_intervals` and the {doc}`coverage-theory maths <../theory/02_normal_approximation>`.*
