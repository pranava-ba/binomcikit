---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Variance-stabilising and transformed intervals

Three pages back we diagnosed {doc}`Wald's <02_normal_approximation>` core weakness: its
{term}`standard error` $\sqrt{\hat p(1-\hat p)/n}$ depends on where you are on the $[0,1]$ scale, and is
worst near the edges. {doc}`Test inversion <03_test_inversion>` fixed that by evaluating the standard
error at the candidate $\theta$; {doc}`exact methods <04_exact_and_discreteness>` dropped the
approximation entirely. This page takes a **third route**: don't fight the changing variance — *transform
to a scale where it stops changing*, build a plain symmetric interval there, and map back. Done well it
gives the **arcsine** and **logit** intervals. Done naively it produces a spectacular boundary failure,
which is exactly why it is worth understanding.

Every code block here is **executed when the docs are built**.

## The delta method, put to work

The tool is the {term}`delta method` from {doc}`page 2 <02_normal_approximation>`: for a smooth
transform $g$,

$$\operatorname{Var}\!\big(g(\hat p)\big) \;\approx\; g'(\theta)^2 \,\operatorname{Var}(\hat p)
\;=\; g'(\theta)^2\,\frac{\theta(1-\theta)}{n}.$$

The whole idea of a **{term}`variance-stabilising transformation`** is to *choose* $g$ so that this
product no longer depends on $\theta$. Then $g(\hat p)$ has (approximately) constant spread everywhere, a
symmetric $\pm z \cdot \text{SE}$ interval on the $g$-scale is honest everywhere, and we finish with a
**{term}`back-transformation`** $g^{-1}$ to return to a proportion.

:::{dropdown} Solving for the stabilising transform — where arcsine comes from
We want $g'(\theta)^2\,\theta(1-\theta)/n$ to be constant, i.e. $g'(\theta) \propto
\dfrac{1}{\sqrt{\theta(1-\theta)}}$. Integrating,

$$g(\theta) \;=\; \int \frac{d\theta}{\sqrt{\theta(1-\theta)}} \;=\; 2\arcsin\!\sqrt{\theta}.$$

So $\arcsin\sqrt{p}$ is not a lucky guess — it is *the* transform that flattens the binomial variance.
With it, $\operatorname{Var}(\arcsin\sqrt{\hat p}) \approx \tfrac{1}{4n}$, a constant with **no $\theta$
in it at all**. The logit is a different, softer choice that stabilises less perfectly but has other
virtues (below).
:::

## ArcSine: the variance made constant

Set $\varphi = \arcsin\sqrt{\hat p}$. Because its variance is a flat $1/(4n)$, the interval on the
$\varphi$-scale is $\varphi \pm z\cdot\tfrac{1}{2\sqrt n}$ — and note the half-width $\tfrac{z}{2\sqrt n}$
is the **same for every $x$**, unlike every method so far. Back-transform with $\sin^2$:

```{code-cell} python
import numpy as np
import binomcikit as bk

# ArcSine 95% intervals for every count at n = 5:
bk.cias(5, 0.05)[["x", "LAS", "UAS", "ZWI"]]
```

Confirm the construction by hand for $x=3,\,n=5$ ($\hat p = 0.6$): take $\arcsin\sqrt{0.6}$, step
$\pm z/(2\sqrt5)$, and square the sine.

```{code-cell} python
from scipy.stats import norm

x, n = 3, 5
z = norm.ppf(0.975)
phi = np.arcsin(np.sqrt(x / n))
half = z / (2 * np.sqrt(n))                       # same half-width for ANY x
print("by hand :", round(np.sin(phi - half) ** 2, 6), round(np.sin(phi + half) ** 2, 6))
print("package :", *bk.ciasx(x, n, 0.05)[["LASx", "UASx"]].iloc[0].round(6))
```

### Why arcsine fails at the boundary

Look again at the grid's `x = 0` and `x = 5` rows: both are flagged `ZWI` — a
**{term}`zero-width interval`**, the same pathology that plagued Wald, arriving here by a new route. At
$x=0$, $\varphi = \arcsin\sqrt0 = 0$, so the two endpoints are $\sin^2(0-h)$ and $\sin^2(0+h)$. But
$\sin^2$ is an *even* function — $\sin^2(-h) = \sin^2(h)$ — so **both** limits collapse onto the single
point $\sin^2(h)$:

```{code-cell} python
h = z / (2 * np.sqrt(5))
print("sin^2(-h) =", round(np.sin(-h) ** 2, 6), " sin^2(+h) =", round(np.sin(h) ** 2, 6))
# ...both equal the collapsed x=0 interval above.
```

The elegant symmetry that stabilised the variance in the interior is exactly what folds the interval
shut at the edge. The damage to {term}`coverage` is severe: near $\theta = 0$ and $\theta = 1$ the arcsine
interval covers almost never.

```{code-cell} python
c = bk.coverage_curve(40, method="arcsine")["coverage"]
{"mean coverage": round(float(c.mean()), 3), "minimum": round(float(c.min()), 3)}
```

A minimum coverage near **0.004** — the boundary collapse in one number. That `ZWI` flag and the
{term}`aberration` columns exist precisely to warn you when a transformed interval has misbehaved like
this. (The *adjusted* arcsine — add a couple of pseudo-counts so $\hat p$ is never exactly 0 or 1 — repairs
it, the same trick {term}`Agresti–Coull` uses.)

## Logit: transform to the log-odds, stay inside [0, 1]

The **logit** takes a different scale: the **{term}`log-odds`** $g(p) = \log\dfrac{p}{1-p}$, whose inverse
is the **{term}`expit`** $g^{-1}(y) = 1/(1+e^{-y})$. Its delta-method standard error works out to
$\sqrt{1/(n\hat p(1-\hat p))}$, so the interval is $\operatorname{logit}(\hat p) \pm z\,\sqrt{1/(n\hat
p\hat q)}$, mapped back through expit. Two payoffs: expit *always* lands in $(0,1)$, so — unlike Wald or
arcsine — the logit interval can **never** run past 0 or 1; and the {term}`odds` scale is the natural one
for much of applied statistics (logistic regression lives here).

```{code-cell} python
bk.cilt(5, 0.05)[["x", "LLT", "ULT", "ZWI"]]
```

Hand-check $x=3,\,n=5$: go to the log-odds, step $\pm z\cdot\text{SE}$, come back through expit.

```{code-cell} python
p = x / n
logit = np.log(p / (1 - p))
se = np.sqrt(1 / (n * p * (1 - p)))
expit = lambda y: 1 / (1 + np.exp(-y))
print("by hand :", round(expit(logit - z * se), 6), round(expit(logit + z * se), 6))
print("package :", *bk.ciltx(x, n, 0.05)[["LLTx", "ULTx"]].iloc[0].round(6))
```

The logit *is* undefined at the boundary — $\log(0/1) = -\infty$ — so a plain logit interval would fail at
$x=0$ and $x=n$ too. binomcikit sidesteps this by substituting the **exact one-sided limit** there rather
than returning $\pm\infty$: at $x=0$ the interval is $[\,0,\;1-(\alpha/2)^{1/n}\,]$, the exact upper bound
from $\Pr(X=0)=(1-\theta)^n$. No collapse, no aberration:

```{code-cell} python
alp = 0.05
print("logit x=0 upper (package):", round(float(bk.cilt(5, 0.05)["ULT"].iloc[0]), 6))
print("exact 1-(alp/2)**(1/n)  :", round(1 - (alp / 2) ** (1 / 5), 6))    # they match
```

## The two transforms, side by side

```{code-cell} python
import pandas as pd
rows = {}
for m, lab in [("arcsine", "ArcSine"), ("logit", "Logit"), ("wilson", "Wilson")]:
    c = bk.coverage_curve(40, method=m)["coverage"]
    rows[lab] = {"mean": round(float(c.mean()), 3),
                 "min": round(float(c.min()), 3),
                 "share ≥ 0.95": round(float(np.mean(c.to_numpy() >= 0.95)), 2)}
pd.DataFrame(rows).T
```

The verdict: **logit** is a genuinely good interval — well-centred, never leaves $[0,1]$, competitive with
{doc}`Wilson <../methods/wilson>`. **ArcSine** is a beautiful idea undone by its boundary — that `min`
near zero is the collapse, and it drags the whole method below the others. Variance stabilisation is a
powerful lever, but the {term}`back-transformation` has to be well-behaved at the edges, and $\sin^2$ is
not.

```{figure} ../_static/transformed_coverage.png
:alt: Coverage of ArcSine, Logit and Wilson against the true rate at n = 40
:width: 100%

Coverage at $n=40$. **ArcSine** (orange) plunges toward zero near $\theta=0$ and $\theta=1$ — the
{term}`zero-width interval` collapse — and sits low even in the interior. **Logit** (green) and **Wilson**
(blue) hold close to the 95% line across the range. The moral: a transform that stabilises the variance
in the middle can still betray you at the boundary.
```

## How this connects to the methods

- {doc}`ArcSine <../methods/arcsine>` (`cias`) — elegant in theory, but check the `ZWI` flag; prefer the
  adjusted variant, or another method, when $x$ can be 0 or $n$.
- {doc}`Logit <../methods/logit>` (`cilt`) — a solid default when you like the {term}`odds` scale or need
  the interval guaranteed to stay inside $(0,1)$.
- Both are {term}`delta method` constructions, cousins of {doc}`Wald <../methods/wald>` on a curved scale.
  The remaining theory pages turn to the {doc}`Bayesian view <06_bayesian_view>` of the same problem, and
  then to **coverage theory** itself — what all these oscillating curves are really telling us.

## Check yourself

**Q1.** What makes $\arcsin\sqrt{p}$ *the* variance-stabilising transform for the binomial, rather than an
arbitrary one?

:::{dropdown} Show answer
It is the transform whose derivative cancels the binomial's $\theta$-dependent variance. The
{term}`delta method` gives $\operatorname{Var}(g(\hat p)) \approx g'(\theta)^2\,\theta(1-\theta)/n$;
choosing $g'(\theta)\propto 1/\sqrt{\theta(1-\theta)}$ makes that constant, and integrating gives
$g(\theta)=2\arcsin\sqrt{\theta}$. The result, $\operatorname{Var}(\arcsin\sqrt{\hat p})\approx 1/(4n)$,
has no $\theta$ in it — the half-width $z/(2\sqrt n)$ is the same for every count.
:::

**Q2.** Why does the arcsine interval collapse to a point at $x=0$, and what flag warns you?

:::{dropdown} Show answer
At $x=0$, $\varphi=\arcsin\sqrt0=0$, so the endpoints are $\sin^2(-h)$ and $\sin^2(+h)$. Since $\sin^2$
is even, $\sin^2(-h)=\sin^2(+h)$, and both limits land on the same value — a {term}`zero-width interval`,
flagged `ZWI = YES`.
```python
h = z / (2 * np.sqrt(5))
np.sin(-h) ** 2, np.sin(h) ** 2      # identical -> collapse
```
:::

**Q3.** The logit interval can never fall outside $(0,1)$. Which part of its construction guarantees that?

:::{dropdown} Show answer
The {term}`back-transformation`, the {term}`expit` $1/(1+e^{-y})$. Whatever real number the log-odds
interval reaches, expit squashes it into $(0,1)$, so the returned limits are always valid proportions —
no {term}`aberration` past 0 or 1, unlike Wald (which is symmetric on the raw scale) or arcsine at the
edge.
:::

---

:::{admonition} Terms used on this page
:class: seealso
{term}`standard error` · {term}`delta method` · {term}`variance-stabilising transformation` ·
{term}`back-transformation` · {term}`odds` · {term}`log-odds` · {term}`expit` · {term}`coverage` ·
{term}`zero-width interval` · {term}`aberration` · {term}`Agresti–Coull` · {term}`quantile`
:::

*New here? Start at {doc}`the foundations <../foundations/index>`. Previous: {doc}`exact methods &
discreteness <04_exact_and_discreteness>`. Next in the series: the Bayesian view — priors, posteriors,
and credible intervals.*
