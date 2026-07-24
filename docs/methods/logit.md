# Logit-Wald interval

> **In one line:** a confidence interval for a {term}`proportion` built on the **log-odds** scale
> instead of the raw 0–1 scale. Because that scale is unbounded, the interval can never spill past 0
> or 1 and never collapses to a point — it handles extreme p̂ gracefully. Its {term}`coverage` is
> reliable but tends to run a little **conservative** (slightly wide). A solid alternative to **Wilson**.

*New here?* Read {doc}`../foundations/index` first — it explains proportions, trials, and what a
confidence interval means, with no maths. Every technical word below is a link to the
{doc}`../glossary`.

This page has two parts: **Use it** (how to call it) and **Understand it** (the maths behind it).

---

## Use it

### Import and call
```python
import binomcikit as bk

# one interval, for x successes in n trials:
bk.ci(x=3, n=20, method="logit")   # "logit-wald" is an alias and identical

# the interval for every possible x = 0, 1, ..., n:
bk.ci(n=20, method="logit")

# the flat function does the same thing:
bk.cilt(20, 0.05)
```

### Parameters
| name | plain English | formal |
|---|---|---|
| `x` | how many successes you saw (optional; omit for all x) | the observed count, 0 ≤ x ≤ n |
| `n` | how many trials in total | the number of {term}`Bernoulli trial`s |
| `alpha` | your error budget; `0.05` gives a 95% interval | {term}`alpha` (α); confidence is 1 − α |

### What you get back
A table (pandas `DataFrame`). For each `x` it gives the lower and upper limits `LLT`, `ULT`, plus
three diagnostic flags:

| column | meaning |
|---|---|
| `LLT`, `ULT` | the lower and upper ends of the **L**ogi**T** interval (always inside (0, 1) in the interior) |
| `ZWI` | **{term}`zero-width interval`** — `YES` if the interval collapses to a point. Logit **never** does. |
| `LABB`, `UABB` | **{term}`aberration`** flags — `YES` when a limit runs past a sensible boundary |

### Examples
The paper's worked example, `n = 5`, `alpha = 0.05` (values match the closed form and the golden
oracle in `tests/cases.py::LOGIT_N5`):

| x | LLT | ULT | note |
|---:|---:|---:|---|
| 0 | 0.000 | 0.522 | boundary row — the exact one-sided {term}`Clopper–Pearson` interval |
| 1 | 0.027 | 0.691 | |
| 2 | 0.100 | 0.800 | |
| 3 | 0.200 | 0.900 | interior — `expit(logit(p̂) ± z·SE)` |
| 4 | 0.309 | 0.973 | |
| 5 | 0.478 | 1.000 | boundary row — exact one-sided interval |

Notice there is **no `ZWI` anywhere** — not even at x = 0 or x = n, where Wald gives the useless
`[0, 0]` / `[1, 1]` and arcsine collapses to a stray point. Logit reports a genuine interval for every
count.

### Recipes
- **Adjusted form (`h`):** `bk.ci(x=3, n=20, method="logit", h=2)` adds `h` pseudo-successes and `h`
  pseudo-failures before taking the log-odds — another way to keep the logit away from ±∞.
- **With a {term}`continuity correction`:** `bk.ci(n=20, method="logit", c=0.5)` widens the interval
  slightly to respect the discreteness of the counts.
- **Compare its {term}`coverage` against other methods:** feed the limits to the `covp*` family
  (see {doc}`../user_guide/index`), or read the figure below.
- **Plot it (interactive, Plotly):** `bk.plot_ci(n=20, method="logit")` draws the interval for every
  `x`; `bk.plot_coverage(n=20, methods=["logit", "wilson"])` overlays coverage curves. Plotting needs
  `pip install binomcikit[plots]`.

### Gotchas
- **Slightly conservative.** Logit's coverage usually sits a touch *above* the nominal level, so its
  intervals are a little wider than Wilson's. Safe, but not the tightest.
- **Raw logit is undefined at the boundary.** At x = 0 or x = n, `logit(p̂)` would be `log(0) = −∞`.
  binomcikit handles this for you by substituting the exact one-sided interval there (see below) — but
  it is why the method needs special care, and why the `h`-adjusted form exists.

---

## Understand it

### The idea, before any symbols
Wald builds a symmetric interval directly on the 0–1 scale, which is why it can wander below 0, above
1, or collapse at the edges. Logit fixes this by moving to a different ruler. Instead of the
probability p̂, it works with the **{term}`log-odds`** — take the {term}`odds` p̂/(1−p̂), then its
logarithm. That ruler runs from −∞ to +∞ with no walls, and it is roughly symmetric, so an ordinary
Wald interval behaves well on it. Build the interval there, then **squash it back** onto 0–1 with the
{term}`expit` function. Because expit always lands in (0, 1), the interval physically *cannot* leave
the valid range or shrink to a point.

### The formula
$$\operatorname{expit}\!\left(\ln\frac{\hat p}{\hat q}\;\pm\;z_{1-\alpha/2}\,\frac{1}{\sqrt{n\,\hat p\,\hat q}}\right),\qquad \operatorname{expit}(u)=\frac{1}{1+e^{-u}}$$

Reading each piece:
- $\hat p = x/n$, $\hat q = 1-\hat p$ — the observed {term}`proportion` and its complement.
- $\ln(\hat p/\hat q)$ — the **{term}`log-odds`** of p̂: the estimate, moved onto the unbounded scale.
- $\dfrac{1}{\sqrt{n\,\hat p\,\hat q}}$ — the {term}`standard error` **of the log-odds** (from the delta
  method). Note it *grows* as p̂ nears 0 or 1, which correctly widens the interval where data are thin.
- $z_{1-\alpha/2}$ — the **{term}`critical value`** (≈ 1.96 for 95%), a {term}`quantile` of the normal curve.
- $\operatorname{expit}(\cdot)$ — the {term}`expit` {term}`back-transformation` back to a proportion.

:::{dropdown} Where it comes from (the derivation)
Let $g(p)=\ln\!\big(p/(1-p)\big)$ be the {term}`log-odds`. By the delta method, the variance of
$g(\hat p)$ is $g'(\theta)^2\,\theta(1-\theta)/n$. Since $g'(p)=\dfrac{1}{p(1-p)}$, this is
$\dfrac{1}{\theta^2(1-\theta)^2}\cdot\dfrac{\theta(1-\theta)}{n}=\dfrac{1}{n\,\theta(1-\theta)}$, so the
{term}`standard error` on the logit scale is $1/\sqrt{n\,\hat p\,\hat q}$. Apply the ordinary Wald recipe
there — $g(\hat p)\pm z\cdot\mathrm{SE}$ — and map both ends back with $g^{-1}=\operatorname{expit}$.

**The boundary.** At $x=0$ or $x=n$, $\hat p\in\{0,1\}$ and $\ln(\hat p/\hat q)=\pm\infty$: the recipe
breaks. binomcikit does **not** fudge this with a normal approximation. Instead it substitutes the
**exact one-sided {term}`Clopper–Pearson` interval**, whose closed form at the edges is simple:
$[\,0,\;1-(\alpha/2)^{1/n}\,]$ at $x=0$ and $[\,(\alpha/2)^{1/n},\;1\,]$ at $x=n$. That is why the x = 0
and x = n rows in the table above are exact, not approximate.
:::

### When it works — and when it doesn't
Logit is well behaved across the whole range of {term}`theta`: because it lives on an unbounded scale
its intervals stay inside (0, 1), never collapse, and its {term}`coverage` holds up near the boundary
where raw **Wald** fails badly. The trade-off is that it is mildly **conservative** — coverage tends to
sit above nominal, so intervals are a little wider than **Wilson**'s. It is the natural interval to
reach for when you are modelling on the log-odds scale anyway (e.g. logistic regression).

```{figure} ../_static/logit_coverage.png
:alt: Coverage probability versus theta for Wald, Logit and Wilson at n=20
:width: 100%

**Reliable, and a little cautious.** True {term}`coverage` against θ for n = 20, α = 0.05 (produced by
binomcikit's own metric engine). Logit (orange) stays at or *above* the nominal 0.95 line across the
whole range — including the boundaries, where Wald (blue) plunges — but sits a touch higher than Wilson
(green), the signature of its mild conservatism. Reproduce with
`bk.plot_coverage(n=20, methods=["wald", "logit", "wilson"])`.
```

### Relatives
- **Complementary log-log** and **probit** intervals apply the same trick with a different unbounded
  transform; they are cousins of logit (packaged in R's `binom`, not in the source `proportion`).
- **{term}`Clopper–Pearson`** — the exact interval logit borrows at the boundary; documented on its own
  page in a later sub-phase.

### References
The logit interval is the Wald method applied on the log-odds scale; transformations of this kind are
discussed in Brown, Cai & DasGupta (2001) [16]. Full citations: the project's `planning/RESEARCH.md`
§11. Deeper maths: {doc}`../theory/index`.

---

:::{admonition} Terms used on this page
:class: seealso
{term}`proportion` · {term}`theta` · {term}`trial` · {term}`Bernoulli trial` · {term}`success` ·
{term}`estimate` · {term}`confidence interval` · {term}`coverage` · {term}`alpha` ·
{term}`standard error` · {term}`critical value` · {term}`quantile` · {term}`odds` ·
{term}`log-odds` · {term}`expit` · {term}`back-transformation` · {term}`Clopper–Pearson` ·
{term}`continuity correction` · {term}`zero-width interval` · {term}`aberration`
:::
