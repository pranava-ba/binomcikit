---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Bootstrap

:::{admonition} New in binomcikit
:class: important
**This method is *not* in the original R `proportion` package.** The paper binomcikit ports
(Subbiah & Rajeswaran 2017) names bootstrap intervals explicitly as future work. binomcikit ships
**three** variants behind one function, selected by `kind`: the ordinary nonparametric bootstrap
(`"percentile"`, `"bca"`) and Wang & Hutson's (2013) **smooth** bootstrap (`"smooth"`, the default),
which fixes the ordinary bootstrap's worst failure mode near the boundary — see *Understand it* below.
:::

> **In one line:** builds the interval by *simulating* many resampled datasets rather than a formula.
> The plain version (`"percentile"`/`"bca"`) is easy to reason about but **breaks down near x = 0 or
> x = n**; the `"smooth"` default fixes exactly that, at the cost of having no independent oracle to
> check it against (see *Interpretation & pitfalls*).

*New here?* Read {doc}`../foundations/index` first — it explains proportions, trials, and what a
confidence interval means, with no maths. Every technical word below is a link to the
{doc}`../glossary`.

This page has two parts: **Use it** (how to call it) and **Understand it** (the maths behind it).

---

## Use it

### Import and call
```python
import binomcikit as bk

# one interval, for x successes in n trials (the default, smooth, kind):
bk.ci(x=3, n=20, method="boot")

# the interval for every possible x = 0, 1, ..., n:
bk.ci(n=20, method="boot")

# the flat function, with every knob explicit:
bk.ciboot(20, 0.05, B=2000, seed=1, kind="smooth")

# the ordinary bootstrap instead (oracle-verified, but breaks at the boundary):
bk.ciboot(20, 0.05, B=2000, seed=1, kind="percentile")
bk.ciboot(20, 0.05, B=2000, seed=1, kind="bca")
```

### Parameters
| name | plain English | formal |
|---|---|---|
| `x` | how many successes you saw (optional; omit for all x) | the observed count, 0 ≤ x ≤ n |
| `n` | how many trials in total | the number of {term}`Bernoulli trial`s |
| `alpha` | your error budget; `0.05` gives a 95% interval | {term}`alpha` (α); confidence is 1 − α |
| `B` | how many {term}`resampling` replicates to simulate (default 2000) | bootstrap replicate count |
| `seed` | fixes the random draws so the result is reproducible | RNG seed, passed to `numpy.random.default_rng` |
| `kind` | which construction: `"smooth"` (default), `"percentile"`, or `"bca"` | see *Understand it* |

### What you get back
A table (pandas `DataFrame`). For each `x` it gives the lower and upper limits `LBOOT`, `UBOOT`, plus
the three standard flags:

| column | meaning |
|---|---|
| `LBOOT`, `UBOOT` | the lower and upper ends of the bootstrap interval (always inside [0, 1]) |
| `ZWI` | **{term}`zero-width interval`** flag — common for `"percentile"`/`"bca"` at x = 0, n; rare for `"smooth"` |
| `LABB`, `UABB` | **{term}`aberration`** flags |

### Examples
The property the smooth variant exists for — a real interval where the ordinary bootstrap collapses:

```python
>>> bk.ciboot(20, 0.05, B=2000, seed=1, kind="percentile").iloc[0]     # x = 0
x         0
LBOOT   0.0
UBOOT   0.0            # zero width -- every resample of an all-0 sample is all-0
...
>>> bk.ciboot(20, 0.05, B=2000, seed=1, kind="smooth").iloc[0]         # x = 0
x         0
LBOOT   0.0
UBOOT   0.11...         # non-degenerate -- the smooth quantile function fixes this
```

### Recipes
- **No adjusted or CC variant.** Bootstrap is **base-only**; `h=` and `c=` raise an error.
- **It still gets the whole diagnostic suite.** As a limit-producer, every metric works out of the box:
  `bk.covpboot(...)`, `bk.lengthboot(...)`, `bk.pcopbiboot(...)`, `bk.errboot(...)` — each also takes
  `seed=`, `B=`, `kind=`.
- **Plot it (interactive, Plotly):** `bk.plot_ci(n=20, method="boot")`;
  `bk.plot_coverage(n=20, methods=["boot-percentile", "boot", "wilson"])` (`"boot"`/`"bootstrap"` plot
  the smooth kind; `"boot-percentile"`/`"boot-bca"` plot the other two). Plotting needs
  `pip install binomcikit[plots]`.
- **A median-unbiased point estimate**, the value the smooth bootstrap resamples from, is also exposed
  directly: `bk.point_estimate(x, n, method="mue")`.

### Gotchas
- **Stochastic, not exact.** Unlike every other method in binomcikit, results depend on `seed` and `B`
  — always pass `seed=` if you need reproducibility, and raise `B` for smoother tail estimates
  (2000 is a reasonable default; the paper's own simulation study used comparable orders of magnitude).
- **Slower than the closed-form methods** — `B` resamples per `x`, so a full `ciboot(n, alpha)` table
  costs `O(n * B)` simulated draws. Not included in `binomcikit.compare()`/`recommend()`'s default
  method list for exactly this reason (pass `methods=[..., "boot"]` explicitly if you want it there).
- **`"percentile"`/`"bca"` collapse to zero width at x = 0 and x = n** — a known, documented limitation
  of the naive bootstrap for binomial data, not a bug. Use `kind="smooth"` (the default) if that matters
  to you.

---

## Understand it

### The idea, before any symbols
Most binomcikit methods invert a formula or a test. Bootstrap instead asks: "if I could repeat my
experiment many times, how much would my estimate wobble?" — and answers it by *simulating* repeats
from the one dataset you have, rather than deriving a formula for the wobble.

The catch, for a binomial: your "dataset" is just `x` ones and `n − x` zeros. Resample it the ordinary
way (draw n values from it, with replacement) and every possible resample's mean is one of only
`n + 1` values, `0/n, 1/n, ..., n/n` — a coarse, discrete spread. At `x = 0`, *every* resample is all
zeros: there is no spread at all, so the interval collapses to a single point. Wang & Hutson (2013)
[25] fix this by resampling from a **smoothed** stand-in for the data instead of the raw 0/1 values.

### The formula
Estimate θ by the **{term}`median-unbiased estimator`** $\hat\theta$ (solve
$P(X \ge x \mid \theta) = 0.5$ and $P(X \le x \mid \theta) = 0.5$ for $\theta_{L}$/$\theta_{R}$ via the
same incomplete-beta identity as {term}`Clopper–Pearson`, at the 50% level instead of α/2, then
average). The **{term}`smooth quantile function`** is
$$Q(u \mid \theta) = 1 - B_{3u,\,3(1-u)}(1-\theta), \qquad u \in (0,1),$$
where $B_{a,b}$ is the Beta$(a,b)$ CDF. For $b = 1 \ldots B$: draw $n$ iid $U^*_i \sim \text{Unif}(0,1)$,
map through $Q(\cdot \mid \hat\theta)$ to get pseudo-observations $X^*_i$, average them to $\bar X^*$,
and convert back to a proportion $\theta^*_b = g(\bar X^*)$ via a fitted **cubic {term}`B-spline`** $g$.
The interval is the empirical $(\alpha/2,\ 1-\alpha/2)$ {term}`quantile` of $\{\theta^*_b\}$.

Reading each piece:
- $\hat\theta$ (MUE) — a point estimate that is never exactly 0 or 1, unlike $\hat p = x/n$; needed
  because $Q(\cdot \mid \theta)$ requires $1 - \theta > 0$.
- $Q(u \mid \theta)$ — a continuous curve standing in for the discrete data, so resampling produces a
  smooth spread of pseudo-observations instead of only $k/n$ values.
- $g(\cdot)$ — the paper's own fitted spline correcting for the fact that $E_u[Q(u\mid\theta)]$ is not
  exactly $\theta$; it maps a simulated mean back to a proportion.

:::{dropdown} Where it comes from (the derivation)
binomcikit implements this directly from Wang & Hutson (2013) [25], Section 2 — read against the
paper's own text (not a secondary summary) to get the construction right:
[pmc.ncbi.nlm.nih.gov/articles/PMC4789773](https://pmc.ncbi.nlm.nih.gov/articles/PMC4789773/).

The spline $g$ is the paper's Equation 7: a cubic B-spline with knots
`(0, 0, 0, 0, 0.293, 0.498, 0.699, 1, 1, 1, 1)` and coefficients
`(0.005, -0.033, 0.159, 0.495, 0.835, 1.033, 0.996)` — transcribed exactly as printed, not refit, so
it is a fixed global function independent of `n`. The MUE's boundary special cases
($\hat\theta = \tfrac12(1-0.5^{1/n})$ at $x=0$; $\hat\theta = \tfrac12(1+0.5^{1/n})$ at $x=n$) are
also the paper's own formulas — checked as an exact identity in `tests/test_bootstrap.py`, since they
follow from the same incomplete-beta relationship as the general-`x` formula (an independent algebraic
check, not a fit to data).

**Why the ordinary bootstrap (`kind="percentile"`/`"bca"`) is a thin wrapper around
`scipy.stats.bootstrap`** rather than binomcikit's own resampling loop: it is a well-established,
already-correct implementation, so reusing it *is* the oracle — no need to duplicate scipy's own
correctness testing.
:::

### When it works — and when it doesn't
Reach for `kind="smooth"` when you specifically want a bootstrap-style interval and might see `x` near
0 or n; it behaves like Wilson in the coverage figure below, without the ordinary bootstrap's collapse.
Reach for `kind="percentile"`/`"bca"` only away from the boundary, or when you specifically want
scipy's own, independently-tested construction. For most everyday work, prefer a closed-form method
(**Wilson**, **Blaker**) — bootstrap is slower and, for `"smooth"`, unverified against a third party;
its value is as a general-purpose technique that extends beyond what a closed form can handle.

```{figure} ../_static/bootstrap_coverage.png
:alt: Coverage probability versus theta for percentile bootstrap, smooth bootstrap and Wilson at n=20
:width: 100%

**The failure mode, and the fix.** True {term}`coverage` against θ for n = 20, α = 0.05. The ordinary
bootstrap (`"percentile"`, blue) plunges toward **0.85** near θ ≈ 0.1 and θ ≈ 0.9 — the boundary
collapse described above. The smooth bootstrap (orange) tracks **Wilson** (green) closely across the
whole range, recovering most of the lost coverage. Reproduce with
`bk.plot_coverage(n=20, methods=["boot-percentile", "boot", "wilson"])`.
```

### Worked example — n = 20, x = 0

Reproduce the boundary contrast directly: the ordinary bootstrap collapses, the smooth one doesn't.

```{code-cell} python
import binomcikit as bk

x, n, alpha = 0, 20, 0.05

pct = bk.ciboot(n, alpha, B=2000, seed=1, kind="percentile")
smooth = bk.ciboot(n, alpha, B=2000, seed=1, kind="smooth")

print("percentile at x=0:", pct.loc[x, "LBOOT"], pct.loc[x, "UBOOT"])
print("smooth     at x=0:", round(smooth.loc[x, "LBOOT"], 4), round(smooth.loc[x, "UBOOT"], 4))
print("MUE (the smooth variant's plug-in estimate):", round(bk.point_estimate(x, n, "mue"), 4))
```

The percentile interval is exactly `(0.0, 0.0)` — literally every one of the 2000 resamples of an
all-zero sample is itself all zeros. The smooth interval is a real, non-degenerate range, because it
never resamples the raw 0/1 data at all.

:::{admonition} Interpretation & pitfalls
:class: warning
- **`kind="smooth"` has no third-party oracle.** binomcikit checks it against the paper's own
  closed-form boundary identities (an independent algebraic check), rough agreement with the
  oracle-verified `"percentile"`/`"bca"` away from the boundary, and the specific
  non-degenerate-at-the-boundary property demonstrated above — see `docs/under_the_hood.md`. This is
  weaker evidence than the golden-value or two-theorem checks the rest of the package relies on; treat
  `kind="smooth"` as good-faith-verified, not gold-standard-verified.
- **Set `seed=`** for reproducible results; without it, re-running gives a (slightly) different
  interval each time.
- **`kind="bca"` needs some spread** — it is mathematically undefined at x = 0 / n (handled explicitly:
  binomcikit returns the same `(0, 0)`/`(1, 1)` the percentile method gives there, rather than raising).
:::

### References
Wang, D. & Hutson, A. D. (2013), "Smooth bootstrap-based confidence intervals for one binomial
proportion and difference of two proportions," *Journal of Applied Statistics* 40(3) [25]. Full
citation: the project's `planning/RESEARCH.md` §11 (construction written out in §9.2). Deeper maths:
{doc}`../theory/index`.

---

:::{admonition} Terms used on this page
:class: seealso
{term}`proportion` · {term}`theta` · {term}`trial` · {term}`Bernoulli trial` · {term}`success` ·
{term}`estimate` · {term}`confidence interval` · {term}`coverage` · {term}`alpha` · {term}`quantile` ·
{term}`Clopper–Pearson` · {term}`zero-width interval` · {term}`aberration` · {term}`bootstrap` ·
{term}`resampling` · {term}`percentile interval` · {term}`BCa` · {term}`median-unbiased estimator` ·
{term}`smooth quantile function` · {term}`B-spline`
:::
