# Wald-T interval

> **In one line:** the **Wald** interval with one honest fix — since the standard error is only
> *estimated*, it swaps the normal `z` for a slightly larger Student-**t** value and modifies the
> boundary. That widens the interval just enough to cure Wald's under-coverage. Reliable, though it
> turns **very conservative** near 0 and 1. A principled, niche alternative to **Wilson**.

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
bk.ci(x=3, n=20, method="waldt")   # "wald-t" is an alias and identical

# the interval for every possible x = 0, 1, ..., n:
bk.ci(n=20, method="waldt")

# the flat function does the same thing:
bk.citw(20, 0.05)
```

### Parameters
| name | plain English | formal |
|---|---|---|
| `x` | how many successes you saw (optional; omit for all x) | the observed count, 0 ≤ x ≤ n |
| `n` | how many trials in total | the number of {term}`Bernoulli trial`s |
| `alpha` | your error budget; `0.05` gives a 95% interval | {term}`alpha` (α); confidence is 1 − α |

### What you get back
A table (pandas `DataFrame`). For each `x` it gives the lower and upper limits `LTW`, `UTW`, plus
three diagnostic flags:

| column | meaning |
|---|---|
| `LTW`, `UTW` | the lower and upper ends of the Wald-**T** interval (clamped to lie in [0, 1]) |
| `ZWI` | **{term}`zero-width interval`** — `YES` if the interval collapses to a point. Wald-T **never** does. |
| `LABB`, `UABB` | **{term}`aberration`** flags — `YES` when a limit runs past a sensible boundary (then it is clamped) |

### Examples
The paper's worked example, `n = 5`, `alpha = 0.05` (values match the closed form and the golden
oracle in `tests/cases.py::WALDT_N5`):

| x | LTW | UTW | note |
|---:|---:|---:|---|
| 0 | 0.000 | 0.664 | boundary row — centred on (x+2)/(n+4), not on 0 |
| 1 | 0.000 | 0.644 | lower clamped up to 0 (`LABB`) |
| 2 | 0.000 | 0.853 | |
| 3 | 0.147 | 1.000 | upper clamped down to 1 (`UABB`) |
| 4 | 0.356 | 1.000 | |
| 5 | 0.336 | 1.000 | boundary row — centred on (x+2)/(n+4), not on 1 |

Every row is a genuine interval — there is **no `ZWI`**, even at x = 0 and x = n where plain Wald
gives the useless `[0, 0]` / `[1, 1]`. Compare any interior row with the {doc}`Wald <wald>` page: the
Wald-T interval is always a little **wider**, which is the whole point.

### Recipes
- **Adjusted form (`h`):** `bk.ci(x=3, n=20, method="waldt", h=2)` adds `h` pseudo-successes and `h`
  pseudo-failures before computing.
- **With a {term}`continuity correction`:** `bk.ci(n=20, method="waldt", c=0.5)` widens the interval
  further to respect the discreteness of the counts.
- **Compare its {term}`coverage` against other methods:** feed the limits to the `covp*` family
  (see {doc}`../user_guide/index`), or read the figure below.
- **Plot it (interactive, Plotly):** `bk.plot_ci(n=20, method="waldt")` draws the interval for every
  `x`; `bk.plot_coverage(n=20, methods=["wald", "waldt"])` overlays coverage curves. Plotting needs
  `pip install binomcikit[plots]`.

### Gotchas
- **Very conservative near the edges.** For {term}`theta` near 0 or 1 the interval over-covers badly
  (coverage climbs toward 1), so the intervals there are wide. It fixes Wald's *under*-coverage by
  sometimes swinging to the opposite extreme.
- The limits are still **symmetric** around the centre (like Wald), so at small `x` the lower limit
  can go below 0 and get clamped (flagged `LABB`).

---

## Understand it

### The idea, before any symbols
Plain **Wald** has a hidden cheat: it plugs the *estimated* wobble √(p̂q̂/n) into the formula but then
treats it as if it were the *exact*, known wobble — so it uses the normal multiplier `z ≈ 1.96`. When
you estimate the wobble from a small sample, that is too optimistic; the honest thing, familiar from
the t-test, is to use a slightly larger **Student-{term}`t-distribution`** multiplier that accounts for
the extra uncertainty. Wald-T does exactly that. It also refuses to let the interval die at the edges:
at x = 0 or x = n it recentres on a nudged estimate instead of on 0 or 1.

### The formula
$$\hat p \;\pm\; t_{\nu,\,1-\alpha/2}\,\sqrt{\frac{\hat p\,\hat q}{n}}$$

Reading each piece:
- $\hat p = x/n$ — the observed {term}`proportion` (at x = 0 or n, replaced by the
  {term}`Agresti–Coull`-style $(x+2)/(n+4)$ so the interval does not collapse).
- $\sqrt{\hat p\hat q/n}$ — the usual {term}`standard error`, the *estimated* wobble.
- $t_{\nu,\,1-\alpha/2}$ — the **{term}`critical value`** from a {term}`t-distribution`, not the normal.
  Because it has finite {term}`degrees of freedom` $\nu$, it is always **larger** than `z`, so the
  interval is wider.
- $\nu$ — data-dependent {term}`degrees of freedom`, chosen by the {term}`Satterthwaite approximation`
  (below).

:::{dropdown} Where it comes from (the derivation)
The variance estimator $V=\hat p\hat q/n$ is itself random. Pan (2002) treats it like a scaled
chi-squared and applies the {term}`Satterthwaite approximation`: match its first two moments to get an
effective {term}`degrees of freedom`
$$\nu = \frac{2\,V^2}{\widehat{\operatorname{Var}}(V)},$$
where $\widehat{\operatorname{Var}}(V)$ is Pan's estimate of the variance of $V$ (a polynomial in
$\hat p$ and $n$). The interval is then the ordinary Wald form but with the normal quantile replaced by
$t_{\nu,1-\alpha/2}$. As $n\to\infty$, $\nu\to\infty$ and the *t* collapses back to the normal — so
Wald-T is just Wald with a small-sample correction. The **boundary modification** (recentre on
$(x+2)/(n+4)$ at x = 0, n) is the two-tailed form of Martín-Andrés & Álvarez-Hernández (2014), and is
what removes the {term}`zero-width interval`.
:::

### When it works — and when it doesn't
Wald-T repairs Wald's central weakness: across the interior its widened interval lifts {term}`coverage`
back to the nominal level, competitive with **Wilson**. Its failing is the opposite of Wald's — near
θ = 0 or 1 it becomes **strongly conservative**, over-covering and producing needlessly wide intervals.
It is a principled but niche method (Pan 2002 [18]; Martín-Andrés & Álvarez-Hernández 2014 [26]),
worth knowing when you specifically want a *t*-based small-sample correction.

```{figure} ../_static/waldt_coverage.png
:alt: Coverage probability versus theta for Wald, Wald-T and Wilson at n=20
:width: 100%

**Fixes the sag, overshoots at the edges.** True {term}`coverage` against θ for n = 20, α = 0.05
(produced by binomcikit's own metric engine). Wald-T (orange) pulls coverage up from Wald's (blue) sag
to at-or-above the nominal 0.95 line, tracking Wilson (green) through the interior — but near the
boundaries it climbs toward 1.0, the signature of its conservatism. Reproduce with
`bk.plot_coverage(n=20, methods=["wald", "waldt", "wilson"])`.
```

### Relatives
- **{term}`Agresti–Coull`** shares the same boundary trick — the $(x+2)/(n+4)$ nudge — but keeps the
  normal `z` instead of a *t* value.
- Plain **{doc}`Wald <wald>`** is the `ν → ∞` limit of this method.

### References
Wald-T is the Satterthwaite/*t*-approximation of the variance estimator, due to Pan (2002) [18]; the
two-tailed version with the boundary corrections used here is Martín-Andrés & Álvarez-Hernández (2014)
[26]. Full citations: the project's `planning/RESEARCH.md` §11. Deeper maths: {doc}`../theory/index`.

---

:::{admonition} Terms used on this page
:class: seealso
{term}`proportion` · {term}`theta` · {term}`trial` · {term}`Bernoulli trial` · {term}`success` ·
{term}`estimate` · {term}`confidence interval` · {term}`coverage` · {term}`alpha` ·
{term}`standard error` · {term}`critical value` · {term}`quantile` · {term}`t-distribution` ·
{term}`degrees of freedom` · {term}`Satterthwaite approximation` · {term}`Agresti–Coull` ·
{term}`continuity correction` · {term}`zero-width interval` · {term}`aberration`
:::
