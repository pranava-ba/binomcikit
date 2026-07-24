# Likelihood-ratio interval

> **In one line:** instead of approximating, this interval keeps every {term}`theta` that the data do
> not *clearly* argue against — measured by how much the fit worsens away from the best estimate. Its
> {term}`coverage` is excellent, on par with **Wilson**, and it never collapses to a point. It is a
> strong, principled, and under-used method; its only cost is that the limits are found numerically.

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
bk.ci(x=3, n=20, method="lr")   # "likelihood" / "likelihood-ratio" are aliases

# the interval for every possible x = 0, 1, ..., n:
bk.ci(n=20, method="lr")

# the flat function does the same thing:
bk.cilr(20, 0.05)
```

### Parameters
| name | plain English | formal |
|---|---|---|
| `x` | how many successes you saw (optional; omit for all x) | the observed count, 0 ≤ x ≤ n |
| `n` | how many trials in total | the number of {term}`Bernoulli trial`s |
| `alpha` | your error budget; `0.05` gives a 95% interval | {term}`alpha` (α); confidence is 1 − α |

### What you get back
A table (pandas `DataFrame`). For each `x` it gives the lower and upper limits `LLR`, `ULR`, plus
three diagnostic flags:

| column | meaning |
|---|---|
| `LLR`, `ULR` | the lower and upper ends of the **L**ikelihood-**R**atio interval |
| `ZWI` | **{term}`zero-width interval`** — `YES` if the interval collapses to a point. LR **never** does. |
| `LABB`, `UABB` | **{term}`aberration`** flags — `YES` when a limit runs past a sensible boundary |

### Examples
The paper's worked example, `n = 5`, `alpha = 0.05` (values match the closed-form definition and the
golden oracle in `tests/cases.py::LR_N5`):

| x | LLR | ULR | note |
|---:|---:|---:|---|
| 0 | 0.000 | 0.319 | boundary — a real interval, no collapse |
| 1 | 0.013 | 0.628 | |
| 2 | 0.081 | 0.801 | |
| 3 | 0.199 | 0.919 | brackets the estimate p̂ = 0.6 |
| 4 | 0.372 | 0.987 | |
| 5 | 0.681 | 1.000 | boundary — a real interval, no collapse |

There is **no `ZWI`** — even at x = 0 and x = n, where Wald gives the useless `[0, 0]` / `[1, 1]`. Each
interval also *contains* the {term}`maximum likelihood estimate` p̂ = x/n, because it is built outward
from the best fit.

### Recipes
- **Adjusted form (`h`):** `bk.ci(x=3, n=20, method="lr", h=2)` adds `h` pseudo-successes and `h`
  pseudo-failures before fitting.
- **No {term}`continuity correction`.** Unlike the normal-approximation methods, LR has **no** CC
  variant — `bk.ci(n=20, method="lr", c=0.5)` raises an error. (This is a structural fact of the
  method, mirrored from the R package.)
- **Compare its {term}`coverage` against other methods:** feed the limits to the `covp*` family
  (see {doc}`../user_guide/index`), or read the figure below.
- **Plot it (interactive, Plotly):** `bk.plot_ci(n=20, method="lr")` draws the interval for every
  `x`; `bk.plot_coverage(n=20, methods=["lr", "wilson"])` overlays coverage curves. Plotting needs
  `pip install binomcikit[plots]`.

### Gotchas
- **The limits are computed numerically** (a small root-find per `x`), not from a closed formula. This
  is invisible in use — it just means LR is a touch slower than the algebraic methods for very large `n`.
- The interval is generally **asymmetric** around p̂, following the shape of the likelihood.

---

## Understand it

### The idea, before any symbols
Every candidate value of {term}`theta` explains your data with some {term}`likelihood` — how probable
your exact count would be if that θ were the truth. One value, the {term}`maximum likelihood estimate`
p̂ = x/n, explains it best. As you move θ away from p̂, the data become less likely; at some point they
become *so* unlikely that you would reject that θ. The likelihood-ratio interval is simply **all the θ
you would not reject** — the ones whose fit is within a set margin of the best fit. No normal curve, no
symmetry assumption: it follows the data's own likelihood.

### The formula
$$\Bigl\{\,\theta : 2\bigl[\ell(\hat p) - \ell(\theta)\bigr] \le z_{1-\alpha/2}^{2}\,\Bigr\},\qquad \ell(\theta) = x\ln\theta + (n-x)\ln(1-\theta)$$

Reading each piece:
- $\ell(\theta)$ — the **log-{term}`likelihood`**: how well θ explains the data.
- $\hat p = x/n$ — the {term}`maximum likelihood estimate`, where $\ell$ is largest.
- $2[\ell(\hat p) - \ell(\theta)]$ — the **{term}`likelihood-ratio statistic`**: how much fit you lose
  by using θ instead of the best value. Zero at p̂, rising on either side.
- $z_{1-\alpha/2}^2$ — the cutoff (≈ 1.96² = 3.84 for 95%), a chi-squared {term}`quantile`. The two θ
  where the statistic *equals* this cutoff are the lower and upper limits.

:::{dropdown} Where it comes from (the derivation)
The interval **inverts the likelihood-ratio test**. By {term}`Wilks' theorem`, under θ = θ₀ the
statistic $2[\ell(\hat p) - \ell(\theta_0)]$ is approximately chi-squared with one degree of freedom
for large n. Not rejecting θ₀ at level α means the statistic stays below the chi-squared cutoff — and
that cutoff is exactly $z_{1-\alpha/2}^2$ (the square of the normal {term}`quantile`). Collecting every
θ₀ that survives gives the set above. Because $\ell$ has no closed-form inverse, binomcikit finds the
two crossing points numerically (a bounded root-find on each side of p̂); an independent solver
reproduces the shipped limits to ~1e-5. There is **no {term}`continuity correction`** form — the method
inverts a test statistic rather than shifting a standardized quantity, so a `c` adjustment does not
apply.
:::

### When it works — and when it doesn't
LR is one of the **best-behaved** approximate intervals: its {term}`coverage` stays close to nominal
across the whole range of {term}`theta`, comparable to **Wilson**, and far better than **Wald**. It
never collapses at the boundary and always brackets the estimate. Its downsides are practical, not
statistical: no tidy formula (limits are numerical) and it is less familiar to practitioners. The exact
LR of Somerville & Brown (2013) [24] sharpens it further for regulated settings.

```{figure} ../_static/lr_coverage.png
:alt: Coverage probability versus theta for Wald, Likelihood-ratio and Wilson at n=20
:width: 100%

**As good as Wilson.** True {term}`coverage` against θ for n = 20, α = 0.05 (produced by binomcikit's
own metric engine). The Likelihood-ratio curve (orange) oscillates tightly around the nominal 0.95
line, tracking Wilson (green) almost step for step and clearly beating Wald (blue). Reproduce with
`bk.plot_coverage(n=20, methods=["wald", "lr", "wilson"])`.
```

### Relatives
- **Score / {doc}`Wilson <wilson>`** — another test-inversion interval; LR inverts the likelihood-ratio
  test, Wilson inverts the score test. They usually agree closely.
- **Exact LR** (Somerville & Brown 2013) — a coverage-guaranteeing refinement, not yet in binomcikit.

### References
The interval inverts the likelihood-ratio test (Wilks' theorem applied to the binomial); the exact
version and its recommendation for regulated work are in Somerville & Brown (2013) [24]. Full
citations: the project's `planning/RESEARCH.md` §11. Deeper maths: {doc}`../theory/index`.

---

:::{admonition} Terms used on this page
:class: seealso
{term}`proportion` · {term}`theta` · {term}`trial` · {term}`Bernoulli trial` · {term}`success` ·
{term}`estimate` · {term}`confidence interval` · {term}`coverage` · {term}`alpha` · {term}`quantile` ·
{term}`likelihood` · {term}`maximum likelihood estimate` · {term}`likelihood-ratio statistic` ·
{term}`Wilks' theorem` · {term}`continuity correction` · {term}`zero-width interval` · {term}`aberration`
:::
