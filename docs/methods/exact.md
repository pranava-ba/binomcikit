# Exact interval (Clopper–Pearson & Mid-P)

> **In one line:** the only interval here that makes a **guarantee** — by counting exact binomial
> probabilities instead of approximating, {term}`Clopper–Pearson` never drops below its promised
> {term}`coverage`. The price is width; it over-covers. A single knob `e` slides from the cautious
> Clopper–Pearson (`e = 1`) to the leaner {term}`Mid-P` (`e = 0.5`).

*New here?* Read {doc}`../foundations/index` first — it explains proportions, trials, and what a
confidence interval means, with no maths. Every technical word below is a link to the
{doc}`../glossary`.

This page has two parts: **Use it** (how to call it) and **Understand it** (the maths behind it).

---

## Use it

### Import and call
```python
import binomcikit as bk

# Clopper-Pearson (the default exact interval, e = 1):
bk.ci(x=3, n=20, method="exact")     # aliases: "cp", "clopper-pearson"

# Mid-P (less conservative, e = 0.5):
bk.ci(x=3, n=20, method="midp")      # alias: "mid-p"

# any tail-tuning value in between:
bk.ci(n=20, method="exact", e=0.7)

# the flat function takes e as a list (one block of rows per value):
bk.ciex(20, 0.05, [1.0])             # Clopper-Pearson
```

### Parameters
| name | plain English | formal |
|---|---|---|
| `x` | how many successes you saw (optional; omit for all x) | the observed count, 0 ≤ x ≤ n |
| `n` | how many trials in total | the number of {term}`Bernoulli trial`s |
| `alpha` | your error budget; `0.05` gives a 95% interval | {term}`alpha` (α); confidence is 1 − α |
| `e` | tail knob: `1` = Clopper–Pearson, `0.5` = Mid-P | fraction of the observed point's {term}`tail probability` kept |

### What you get back
A table (pandas `DataFrame`). For each `x` it gives the lower and upper limits `LEX`, `UEX`, the
usual flags, and an `e` column recording which tail setting produced the row:

| column | meaning |
|---|---|
| `LEX`, `UEX` | the lower and upper ends of the **EX**act interval |
| `e` | the tail-tuning value used for this block of rows |
| `ZWI` | **{term}`zero-width interval`** flag |
| `LABB`, `UABB` | **{term}`aberration`** flags |

### Examples
The paper's worked example, `n = 5`, `alpha = 0.05`. Clopper–Pearson (`e = 1`) matches
`statsmodels` `proportion_confint(method="beta")` exactly; Mid-P (`e = 0.5`) matches
`tests/cases.py::MIDP_N5`:

| x | Clopper–Pearson | Mid-P | note |
|---:|---|---|---|
| 0 | [0.000, 0.522] | [0.000, 0.451] | Mid-P is narrower |
| 1 | [0.005, 0.716] | [0.010, 0.666] | |
| 2 | [0.053, 0.853] | [0.074, 0.818] | |
| 3 | [0.147, 0.947] | [0.182, 0.926] | |
| 4 | [0.284, 0.995] | [0.334, 0.990] | |
| 5 | [0.478, 1.000] | [0.549, 1.000] | |

At **every** row Mid-P sits inside Clopper–Pearson — that is the meaning of "less conservative".

### Recipes
- **No adjusted or CC variant.** The exact family is **base-only**: there is no `h`-adjusted or
  continuity-corrected form (passing `h=` or `c=` raises an error). This is a structural fact of the
  method, mirrored from the R package.
- **Sweep the tail knob:** `bk.ciex(20, 0.05, [1.0, 0.5, 0.0])` returns three stacked blocks (CP,
  Mid-P, and the fully "exclusive" tail) in one DataFrame, tagged by the `e` column.
- **Compare its {term}`coverage`:** feed the limits to the `covp*` family (see
  {doc}`../user_guide/index`), or read the figure below.
- **Plot it (interactive, Plotly):** `bk.plot_ci(n=20, method="exact")` (or `"midp"`) draws the
  interval for every `x`; `bk.plot_coverage(n=20, methods=["exact", "midp", "wilson"])` overlays
  coverage curves. Plotting needs `pip install binomcikit[plots]`.

### Gotchas
- **It over-covers on purpose.** Clopper–Pearson's guarantee (coverage ≥ 1 − α for *every* θ) forces
  it to be wide. If you want intervals centred near nominal rather than a hard floor, prefer **Wilson**
  or **Mid-P**.
- **`e` is passed as a list to the flat `ciex`** (e.g. `[1.0]`), but as a plain number to the
  high-level `bk.ci(..., e=1.0)`.

---

## Understand it

### The idea, before any symbols
Every other method on this site approximates the binomial with a smooth curve. The exact interval
refuses to approximate. It asks, for each candidate {term}`theta`: *if this θ were true, how often
would I see a count as extreme as mine?* That is an exact {term}`tail probability`, computed from the
binomial itself. Keep every θ for which your result is not too surprising, and you have the interval —
with a genuine {term}`coverage` guarantee. The knob `e` decides how to treat the *observed* count
sitting on the tail's edge: count it fully (`e = 1`, cautious Clopper–Pearson) or only halfway
(`e = 0.5`, {term}`Mid-P`).

### The formula
The limits are the θ that solve the tail equations (found by root-finding):
$$e\Pr(X = x\mid\theta) + \Pr(X < x\mid\theta) = \tfrac{\alpha}{2}\quad(\text{upper}),\qquad
(1-e)\Pr(X = x\mid\theta) + \Pr(X < x\mid\theta) = 1-\tfrac{\alpha}{2}\quad(\text{lower}).$$

Reading each piece:
- $\Pr(X = x\mid\theta)$, $\Pr(X < x\mid\theta)$ — exact binomial probabilities: the point mass at the
  observed count and the {term}`tail probability` below it.
- $e$ — the fraction of the observed point's mass assigned to the tail. `e = 1` puts it all in (giving
  the equal-tailed exact test, i.e. {term}`Clopper–Pearson`); `e = 0.5` puts in half ({term}`Mid-P`).
- Setting each tail to $\alpha/2$ and solving for θ gives the two limits.

:::{dropdown} Where it comes from (the derivation)
This is a {term}`test inversion` — but of the **exact** binomial test, not an approximation. For a
candidate θ₀, the equal-tailed p-value is built from the exact tail sums above; the interval is every
θ₀ the test does not reject. With `e = 1` the upper limit solves $\Pr(X\le x)=\alpha/2$ and the lower
solves $\Pr(X\ge x)=\alpha/2$, which have the closed **Beta-quantile** form
$L = B^{-1}(\alpha/2;\,x,\,n-x+1)$ and $U = B^{-1}(1-\alpha/2;\,x+1,\,n-x)$ — this is exactly
`statsmodels`' `method="beta"`, which binomcikit reproduces to machine precision. Because the binomial
is discrete, forcing coverage to be *at least* $1-\alpha$ for every θ makes it *strictly greater* for
most θ — the unavoidable conservatism. {term}`Mid-P` (`e = 0.5`) counts only half the boundary mass,
shrinking that excess at the cost of dropping the hard guarantee. The unifying `e` knob is a
contribution of the R `proportion` package.
:::

### When it works — and when it doesn't
Use {term}`Clopper–Pearson` when you must **guarantee** coverage never falls below the nominal level —
regulated submissions, safety thresholds, tiny samples where you cannot afford an approximation's
optimism. Its cost is width: it is the widest interval here and over-covers everywhere. {term}`Mid-P`
is the pragmatic compromise — most of the exactness, much less of the waste — when you want an
exact-flavoured interval without the full conservatism.

```{figure} ../_static/exact_coverage.png
:alt: Coverage probability versus theta for Clopper-Pearson, Mid-P and Wilson at n=20
:width: 100%

**The guarantee, and the price.** True {term}`coverage` against θ for n = 20, α = 0.05 (produced by
binomcikit's own metric engine). Clopper–Pearson (blue) stays **above** the nominal 0.95 line
everywhere — its guarantee — but that is over-coverage: wider intervals than needed. Mid-P (orange)
pulls down toward nominal, and Wilson (green) oscillates around it. Reproduce with
`bk.plot_coverage(n=20, methods=["exact", "midp", "wilson"])`.
```

### Relatives
- **{doc}`Logit <logit>`** borrows Clopper–Pearson's one-sided form at x = 0 and x = n (where its own
  formula is undefined) — so the exact limits appear there too.
- **Blaker's exact interval** (a later sub-phase) is a different exact construction that is never wider
  than Clopper–Pearson while keeping the guarantee.

### References
The exact interval is due to Clopper & Pearson (1934) [2]; the Mid-P correction traces to Lancaster
(1961). The unifying tail parameter `e` is a feature of the source R package [36]. Full citations: the
project's `planning/RESEARCH.md` §11. Deeper maths: {doc}`../theory/index`.

---

:::{admonition} Terms used on this page
:class: seealso
{term}`proportion` · {term}`theta` · {term}`trial` · {term}`Bernoulli trial` · {term}`success` ·
{term}`estimate` · {term}`confidence interval` · {term}`coverage` · {term}`alpha` ·
{term}`tail probability` · {term}`Clopper–Pearson` · {term}`Mid-P` · {term}`test inversion` ·
{term}`zero-width interval` · {term}`aberration`
:::
