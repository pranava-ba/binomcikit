---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Wald interval

> **In one line:** the simplest confidence interval for a {term}`proportion` — the one taught in
> most first statistics courses. It is fast and intuitive, but its {term}`coverage` is unreliable
> for small samples, so treat it as a **teaching baseline**, not a default. For real work, prefer
> the **{doc}`Wilson <wilson>`** interval.

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
bk.ci(x=3, n=20, method="wald")

# the interval for every possible x = 0, 1, ..., n:
bk.ci(n=20, method="wald")

# the R-style name works too and is identical:
bk.ciwd(20, 0.05)
```

### Parameters
| name | plain English | formal |
|---|---|---|
| `x` | how many successes you saw (optional; omit for all x) | the observed count, 0 ≤ x ≤ n |
| `n` | how many trials in total | the number of {term}`Bernoulli trial`s |
| `alpha` | your error budget; `0.05` gives a 95% interval | {term}`alpha` (α); confidence is 1 − α |

### What you get back
A table (pandas `DataFrame`). For each `x` it gives the lower and upper limits `LWD`, `UWD`, plus
three diagnostic flags:

| column | meaning |
|---|---|
| `LWD`, `UWD` | the lower and upper ends of the interval (both clamped to lie in [0, 1]) |
| `ZWI` | **{term}`zero-width interval`** — `YES` when the interval collapses to a point (happens at `x = 0` and `x = n`) |
| `LABB`, `UABB` | **aberration** flags — `YES` when a limit runs past a sensible boundary |

### Examples
The paper's worked example, `n = 5`, `alpha = 0.05` (values match Table 2 of Subbiah &
Rajeswaran 2017):

| x | LWD | UWD | note |
|---:|---:|---:|---|
| 0 | 0.000 | 0.000 | `ZWI` — collapses at the boundary |
| 1 | 0.000 | 0.551 | lower clamped up to 0 |
| 2 | 0.000 | 0.829 | |
| 3 | 0.171 | 1.000 | upper clamped down to 1 |
| 4 | 0.449 | 1.000 | |
| 5 | 1.000 | 1.000 | `ZWI` — collapses at the boundary |

### Recipes
- **Adjusted Wald (a.k.a. {term}`Agresti–Coull`), the recommended repair:**
  `bk.ci(n=20, method="agresti-coull")`.
- **With a {term}`continuity correction`:** `bk.ci(n=20, method="wald", c=0.5)`.
- **Compare its {term}`coverage` against other methods:** feed the limits to the `covp*` family
  (see {doc}`../evaluating_intervals`).
- **Plot it (interactive, Plotly):** `bk.plot_ci(n=20, method="wald")` draws the interval for every
  `x`; `bk.plot_coverage(n=20, methods=["wald", "wilson"])` overlays coverage curves. Plotting needs
  `pip install binomcikit[plots]`.

### Gotchas
- At `x = 0` or `x = n` the interval is a **single point** (`ZWI`) — it claims perfect certainty,
  which it does not have. This is the clearest symptom of Wald's weakness.
- For small `n`, the true {term}`coverage` can fall well below the 95% you asked for (see below).

---

## Understand it

### The idea, before any symbols
You flipped a coin `n` times and got `x` heads, so your best single guess for the coin's true
head-rate {term}`theta` is the observed {term}`proportion` p̂ = x/n. But p̂ wobbles from sample to
sample. The Wald interval just says: *take that wobble, assume it follows the bell-shaped normal
curve, and stretch out a symmetric interval around p̂ wide enough to cover 95% of the wobble.*

### The formula
$$\hat p \pm z_{1-\alpha/2}\,\sqrt{\frac{\hat p\,(1-\hat p)}{n}}$$

Reading each piece:
- $\hat p = x/n$ — the observed {term}`proportion` (an {term}`estimate` of {term}`theta`).
- $\sqrt{\hat p(1-\hat p)/n}$ — the **{term}`standard error`**: how much p̂ typically wobbles.
- $z_{1-\alpha/2}$ — the **{term}`critical value`**: a {term}`quantile` of the normal curve
  (≈ 1.96 for 95%) that sets how many standard errors wide to go.

:::{dropdown} Where it comes from (the derivation)
By the Central Limit Theorem, for large `n` the estimator p̂ is approximately normal with mean θ
and variance θ(1−θ)/n. Standardising, (p̂ − θ)/√(θ(1−θ)/n) ≈ standard normal. The Wald interval
*inverts* that statement, but takes one shortcut: it evaluates the {term}`standard error` at p̂
instead of at θ (a {term}`maximum likelihood estimate` plug-in). That shortcut is exactly what
makes it simple — and what makes its coverage misbehave near the boundary. The **Wilson**
interval avoids the shortcut and behaves far better.
:::

### When it works — and when it doesn't
Wald is reasonable when `n` is large **and** {term}`theta` is near 0.5. It fails when `n` is small
or θ is near 0 or 1: its true {term}`coverage` dips below the nominal level, sometimes badly, and
it produces the degenerate {term}`zero-width interval`s at the boundary. This is a classic,
well-documented cautionary tale (Brown, Cai & DasGupta 2001 [16]).

```{figure} ../_static/wald_coverage.png
:alt: Coverage probability versus theta for Wald, Wilson and ArcSine at n=20
:width: 100%

**Wald under-covers.** True {term}`coverage` against θ for n = 20, α = 0.05 (produced by
binomcikit's own metric engine). The Wald curve (blue) sits *below* the nominal 0.95 line almost
everywhere and collapses near the boundaries; Wilson (orange) tracks the target far better.
Reproduce with `bk.plot_coverage(n=20, methods=["wald", "wilson", "arcsine"])`.
```

### The fixes
- **{term}`Agresti–Coull` (adjusted Wald)** — pretend you saw a couple of extra successes and
  failures before computing the same formula. This tiny nudge fixes most of the coverage problem.
  Call it with `method="agresti-coull"`. *(Details on its own page in a later sub-phase.)*
- **{term}`continuity correction`** — widen the interval slightly to account for the fact that the
  binomial counts are discrete but the normal curve is smooth. Call it with `c=...`.

### Worked example — n = 5, x = 3

Watch the formula turn into the numbers the package ships. With p̂ = 3/5 = 0.6 and z ≈ 1.96:

```{code-cell} python
import binomcikit as bk, numpy as np, scipy.stats as st

x, n, alpha = 3, 5, 0.05
phat = x / n                                   # 0.6
z = st.norm.ppf(1 - alpha / 2)                 # 1.9600
se = np.sqrt(phat * (1 - phat) / n)            # standard error at p-hat
lo, hi = phat - z * se, phat + z * se

print(f"p-hat = {phat},  SE = {se:.4f},  z = {z:.4f}")
print(f"raw     : [{lo:.4f}, {hi:.4f}]")
print(f"clamped : [{max(0, lo):.4f}, {min(1, hi):.4f}]")
bk.ci(x=x, n=n, method="wald")                 # LWDx / UWDx match the clamped result
```

The upper limit came out above 1 and was clamped — an `UABB` **{term}`aberration`**, and a first sign
that the normal approximation is out of its depth here.

:::{admonition} Interpretation & pitfalls
:class: warning
- The interval is **symmetric** about p̂, so at small `n` a limit routinely lands outside `[0, 1]` and
  gets clamped (as the upper limit did here). Clamping hides how badly the raw formula overshot.
- At `x = 0` or `x = n` the {term}`standard error` is exactly 0, collapsing the interval to a
  {term}`zero-width interval` — the boundary trap. Reach for {doc}`Wilson <wilson>` or an exact method.
- Because the SE is evaluated at p̂ (not at the tested θ), true {term}`coverage` sags below the nominal
  level — see {doc}`../evaluating_intervals` and {doc}`../theory/02_normal_approximation`.
:::

### References
Wald is the textbook normal-approximation interval; its shortcomings and the recommended
alternatives are analysed in Brown, Cai & DasGupta (2001) and Agresti & Coull (1998). Full
citations: the project's `planning/RESEARCH.md` §11 (refs [16], [13]). Deeper maths: {doc}`../theory/index`.

---

:::{admonition} Terms used on this page
:class: seealso
{term}`proportion` · {term}`theta` · {term}`trial` · {term}`Bernoulli trial` · {term}`success` ·
{term}`estimate` · {term}`confidence interval` · {term}`coverage` · {term}`alpha` ·
{term}`standard error` · {term}`critical value` · {term}`quantile` ·
{term}`maximum likelihood estimate` · {term}`Agresti–Coull` · {term}`continuity correction` ·
{term}`zero-width interval`
:::
