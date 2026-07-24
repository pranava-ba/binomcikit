# Blaker's exact interval

:::{admonition} New in binomcikit
:class: important
**This method is *not* in the original R `proportion` package.** Blaker's interval is an addition
binomcikit makes beyond the package it ports — an exact interval that keeps Clopper–Pearson's coverage
**guarantee** while being provably **narrower**. The source package's authors flagged exact
alternatives like this as future work; implementing it closes a gap that exists even against R.
:::

> **In one line:** the exact interval you should usually prefer over {term}`Clopper–Pearson`. It gives
> the *same* guarantee — {term}`coverage` never below 1 − α — but is **{term}`nested <nested interval>`
> inside** Clopper–Pearson, so it is never wider and usually shorter. The cost is that its limits are
> computed numerically.

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
bk.ci(x=3, n=20, method="blaker")

# the interval for every possible x = 0, 1, ..., n:
bk.ci(n=20, method="blaker")

# the flat function does the same thing:
bk.ciblaker(20, 0.05)
```

### Parameters
| name | plain English | formal |
|---|---|---|
| `x` | how many successes you saw (optional; omit for all x) | the observed count, 0 ≤ x ≤ n |
| `n` | how many trials in total | the number of {term}`Bernoulli trial`s |
| `alpha` | your error budget; `0.05` gives a 95% interval | {term}`alpha` (α); confidence is 1 − α |

### What you get back
A table (pandas `DataFrame`). For each `x` it gives the lower and upper limits `LBK`, `UBK`, plus the
three standard flags:

| column | meaning |
|---|---|
| `LBK`, `UBK` | the lower and upper ends of the **B**la**K**er interval (always inside [0, 1]) |
| `ZWI` | **{term}`zero-width interval`** flag — Blaker never produces one |
| `LABB`, `UABB` | **{term}`aberration`** flags |

### Examples
The paper's worked example, `n = 5`, `alpha = 0.05` (values match the golden fixture in
`tests/cases.py::BLAKER_N5`), shown next to {term}`Clopper–Pearson` so you can see the nesting:

| x | Blaker | Clopper–Pearson | note |
|---:|---|---|---|
| 0 | [0.000, 0.500] | [0.000, 0.522] | Blaker upper is tighter |
| 1 | [0.010, 0.657] | [0.005, 0.716] | |
| 2 | [0.076, 0.811] | [0.053, 0.853] | |
| 3 | [0.189, 0.924] | [0.147, 0.947] | |
| 4 | [0.343, 0.990] | [0.284, 0.995] | |
| 5 | [0.500, 1.000] | [0.478, 1.000] | Blaker lower is tighter |

Every Blaker interval sits **inside** the Clopper–Pearson one — that is the nesting theorem, and the
reason to prefer it when you want an exact guarantee without the full Clopper–Pearson width.

### Recipes
- **No adjusted or CC variant.** Like the other exact methods, Blaker is **base-only**; `h=` and `c=`
  raise an error.
- **It still gets the whole diagnostic suite.** Because Blaker plugs into binomcikit's shared engine as
  a limit-producer, every metric works out of the box: `bk.covpblaker(...)`, `bk.lengthblaker(...)`,
  `bk.pcopbiblaker(...)`, `bk.errblaker(...)`.
- **Plot it (interactive, Plotly):** `bk.plot_ci(n=20, method="blaker")`;
  `bk.plot_coverage(n=20, methods=["exact", "blaker", "wilson"])`. Plotting needs
  `pip install binomcikit[plots]`.

### Gotchas
- **Numerical, not closed-form.** Each limit is a small root-find, so Blaker is a touch slower than the
  algebraic methods for very large `n` (irrelevant for typical sizes).
- **Still conservative — just less so.** It is an *exact* method: coverage stays ≥ nominal, so it is
  wider than approximate intervals like **Wilson**. Choose it when you specifically want the guarantee.

---

## Understand it

### The idea, before any symbols
{term}`Clopper–Pearson` is safe but wasteful: it treats the two tails separately, which double-counts
uncertainty and makes the interval wider than it needs to be. Blaker's insight is to judge an outcome by
its **smaller** tail, then fold in the largest opposite tail that is no bigger. This "two-sided
acceptability" throws away less, so the set of θ that stay plausible is smaller — a shorter interval —
yet the exact coverage guarantee still holds. The interval you get always sits inside Clopper–Pearson.

### The formula
For the binomial CDF `F(k; θ) = P_θ(X ≤ k)`, define the smaller-tail function and the
{term}`acceptability function`:
$$g(x,\theta) = \min\{\,F(x;\theta),\; 1 - F(x-1;\theta)\,\}, \qquad \gamma(x,\theta) = P_\theta\!\big(g(X,\theta) \le g(x,\theta)\big).$$
The 1 − α **Blaker interval** is
$$\{\,\theta : \gamma(x,\theta) \ge \alpha\,\},$$
reported as `[LBK, UBK]`, whose ends solve `γ(x, θ) = α`.

Reading each piece:
- `F(x;θ)` and `1 − F(x−1;θ)` — the lower {term}`tail probability` `P(X≤x)` and the upper one `P(X≥x)`.
- `g(x,θ)` — the **smaller** of those two tails.
- `γ(x,θ)` — the {term}`acceptability function`: the chance, under θ, of an outcome at least as extreme
  (by the smaller-tail measure) as the one observed.

:::{dropdown} Where it comes from (the derivation)
Blaker (2000) [15] inverts an exact two-sided test whose p-value is `γ(x, θ)`. Because `γ` folds the
opposite tail into the smaller one, it is never larger than Clopper–Pearson's equal-tailed p-value, so
the acceptance set `{θ : γ ≥ α}` is a **subset** of Clopper–Pearson — the nesting (and shorter-length)
property, with coverage still ≥ 1 − α.

binomcikit computes `γ` directly from its definition (summing the binomial mass over every outcome `k`
with `g(k, θ) ≤ g(x, θ)`) and finds each limit by root-finding **inward from the Clopper–Pearson
bound** to the estimate p̂ (a safe bracket, since Blaker ⊆ Clopper–Pearson). One subtlety: `γ(·, θ)`
can be **non-{term}`quantile`-smooth** — it jumps as the set of counted outcomes changes with θ, and is
not perfectly unimodal (Klaschka 2010 [22] "unimodalises" it for the exact edge cases). The reported
interval is the connected acceptance region containing p̂; its correctness is confirmed not by matching
another program but by the two theorems that define the method — **nesting inside Clopper–Pearson** and
**coverage ≥ 1 − α** — both checked directly in the test suite across a grid of θ.
:::

### When it works — and when it doesn't
Use Blaker whenever you would reach for {term}`Clopper–Pearson` — regulated work, safety thresholds,
guaranteed coverage — because it gives the **same guarantee with less width**, dominating it. Like all
exact methods it is conservative relative to **Wilson**, so if you want intervals centred on nominal
rather than a hard floor, Wilson or Mid-P are better. It is an established method (Blaker 2000 [15];
computation refined by Klaschka 2010 [22]) that the R `proportion` package never included.

```{figure} ../_static/blaker_coverage.png
:alt: Coverage probability versus theta for Clopper-Pearson, Blaker and Wilson at n=20
:width: 100%

**Same guarantee, less waste.** True {term}`coverage` against θ for n = 20, α = 0.05 (produced by
binomcikit's own metric engine). Blaker (orange) stays **≥ the nominal 0.95 line** everywhere, exactly
like Clopper–Pearson (blue) — but hugs closer to it, the visible sign of its shorter intervals. Wilson
(green) oscillates around nominal, dipping below. Reproduce with
`bk.plot_coverage(n=20, methods=["exact", "blaker", "wilson"])`.
```

### References
Blaker, H. (2000), "Confidence curves and improved exact confidence intervals for discrete
distributions" [15]; computational improvements in Klaschka (2010) [22]. Full citations: the project's
`planning/RESEARCH.md` §11 (and the construction is written out in §9.1). Deeper maths:
{doc}`../theory/index`.

---

:::{admonition} Terms used on this page
:class: seealso
{term}`proportion` · {term}`theta` · {term}`trial` · {term}`Bernoulli trial` · {term}`success` ·
{term}`estimate` · {term}`confidence interval` · {term}`coverage` · {term}`alpha` · {term}`quantile` ·
{term}`tail probability` · {term}`acceptability function` · {term}`nested interval` ·
{term}`Clopper–Pearson` · {term}`zero-width interval` · {term}`aberration`
:::
