---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# FAQ & troubleshooting

Short answers to the questions that come up most often — the ones people hit in the first hour, and
the ones that look like bugs but aren't. Each answer links to the page that explains it properly.

*New here?* Start with {doc}`foundations/index`. Choosing between methods? See
{doc}`method_selection`. Comparing to other libraries? See {doc}`comparison`.

---

## Getting started

### Which method should I use?

For most work, the default — **{doc}`Wilson <methods/wilson>`** — is the right answer. It has good
{term}`coverage` across the whole range of {term}`theta`, never collapses at the boundary, and is
fast. `binomcikit` uses it when you don't name a method:

```{code-cell} python
import binomcikit as bk
bk.ci(x=3, n=20)          # method="wilson" is the default
```

If you need a *guaranteed* coverage floor (regulatory or safety settings), use an exact method —
**{doc}`Blaker <methods/exact>`** or Clopper–Pearson. If you want the data to pick for you, let
`recommend` (see {doc}`access_layer`) rank the methods for your `n`:

```{code-cell} python
bk.recommend(n=30, by="coverage").head(3)[["method", "min_coverage", "mean_length"]]
```

The full decision guide is {doc}`method_selection`.

### How do I get an interval from raw 0/1 data, not a count?

Use `from_data` (part of the {doc}`access layer <access_layer>`). It counts the successes for you and
returns `(x, n)`, which you hand to `ci`:

```{code-cell} python
x, n = bk.from_data([1, 0, 1, 1, 0, 0, 1, 0])   # 4 successes in 8
bk.ci(x=x, n=n)
```

Booleans work too (`from_data([True, False, True])`), as does `from_counts(x, n)` when you already
have the count.

### Do I need any optional extras?

The core library needs only NumPy, SciPy and pandas. Two extras are optional:

- **`binomcikit[plots]`** — the interactive Plotly figures `plot_ci` / `plot_coverage`.
- **`binomcikit[fast]`** — a numba JIT that speeds up the coverage simulations for large `n`. The
  results are identical with or without it; it only changes the speed.

---

## Reading the output

### Why is my interval `[0, 0]` (or `[1, 1]`)?

That is a **{term}`zero-width interval`**, and it is almost always the {doc}`Wald <methods/wald>`
interval at `x = 0` or `x = n`. Wald's width is $z\sqrt{\hat p(1-\hat p)/n}$; when $\hat p = 0$ that
{term}`standard error` is exactly 0, so the interval collapses to a point and claims perfect certainty
it does not have.

```{code-cell} python
bk.ci(x=0, n=20, method="wald")     # ZWI = YES, the interval is [0, 0]
```

The fix is to use a method that doesn't degenerate at the boundary — the default Wilson gives a
sensible upper bound:

```{code-cell} python
bk.ci(x=0, n=20, method="wilson")   # [0, 0.161] — an honest one-sided statement
```

The {doc}`zero-events tutorial <tutorials/zero_events>` covers this case (and the "rule of three")
in full.

### What do the `ZWI`, `LABB` and `UABB` columns mean?

They are honesty flags on every interval:

- **`ZWI`** — *{term}`zero-width interval`*: `YES` when the interval collapsed to a single point.
- **`LABB` / `UABB`** — *{term}`aberration`* on the lower / upper limit: `YES` when a raw limit fell
  outside `[0, 1]` and had to be clamped back. It marks where the normal approximation broke the
  arithmetic, not just the statistics.

A method that never raises these flags (Wilson, the exact methods) is structurally better behaved
than one that does (Wald).

### My "95%" interval only covers 84% of the time. Is that a bug?

No — that is the single most important fact the library exists to show you. The **95%** is the
*nominal* {term}`confidence level`; the fraction of intervals that actually trap {term}`theta` is the
*true* {term}`coverage`, and for a discrete binomial it is never a flat line. Wald's mean coverage at
`n = 20` really is well below 0.95:

```{code-cell} python
bk.covpwd(n=20, alp=0.05, a=1, b=1, t1=0.9, t2=0.97, seed=0)[["mcp", "micp"]]
```

`mcp` is the mean, `micp` the worst case. Seeing the gap is the point — see
{doc}`foundations/05_coverage` for the idea and {doc}`theory/07_coverage_theory` for why the gap
never fully closes.

---

## Concepts that trip people up

### What's the difference between confidence level and coverage?

The **{term}`confidence level`** ($1-\alpha$) is what you *ask for* — a property of the procedure you
chose. The **{term}`coverage`** is what you *get* — the actual long-run fraction of intervals that
contain {term}`theta`, which depends on `n` and on the unknown θ itself. A good method keeps coverage
close to the level it promises; Wald does not. Full treatment: {doc}`theory/07_coverage_theory`.

### Frequentist or Bayesian — which should I report?

They answer different questions. A frequentist {term}`confidence interval` makes a statement about the
*procedure* ("95% of intervals built this way trap the truth"). A Bayesian {term}`credible interval`
makes a statement about *this* dataset given a {term}`prior` ("given a uniform prior, there's a 95%
posterior probability θ is in here"). `binomcikit` gives you both:

```{code-cell} python
post = bk.posterior(x=3, n=20)          # uniform prior by default
post["quantile_interval"], post["mean"]
```

Report whichever matches the claim you actually want to make — and say which one it is. The
{doc}`Bayesian toolbox <bayesian_toolbox>` and {doc}`theory/06_bayesian_view` go deeper; interestingly
the Jeffreys credible interval nearly matches Wilson's frequentist coverage.

### Can I get a p-value or run a hypothesis test?

Not as a dedicated function *yet* — a per-method p-value family is on the roadmap (§1.11). Two things
work today:

- **Confidence–test duality.** A two-sided test of $H_0: \theta = \theta_0$ at level α rejects exactly
  when $\theta_0$ falls outside the $1-\alpha$ interval. So `bk.ci(x, n)` already answers "is
  $\theta_0$ plausible?" — check whether it's inside.
- **SciPy for an exact p-value.** `scipy.stats.binomtest(x, n, theta0)` gives the exact binomial
  {term}`tail probability` and matches Clopper–Pearson's interval by construction.

---

## Reproducibility & validation

### Why don't my coverage numbers exactly match the R `proportion` package?

Because two of the four evaluation families **simulate**, and NumPy's random generator is not R's:

- **Simulation-based** (`covp*`, `length*`) — draw θ from a `Beta(a, b)` prior. Pass `seed=` for
  reproducibility, but expect a match to R only *in distribution*, not draw-for-draw.
- **Deterministic** (`pcopbi*`, `err*`) — pure binomial sums, no RNG. These match R (and the paper's
  golden values) exactly.

```{code-cell} python
bk.pcopbiwd(n=5, alp=0.05)     # deterministic — identical every run and matches R
```

### How do I know the intervals are correct?

Where an independent reference exists, `binomcikit` is checked against it. Wilson, Wald,
Clopper–Pearson and Jeffreys agree with `statsmodels` and `scipy` to the printed digits; the exact
Blaker interval is verified against its two defining theorems (nesting inside Clopper–Pearson, and the
acceptability identity). The side-by-side numbers are on the {doc}`comparison page <comparison>`.

---

:::{admonition} Terms used on this page
:class: seealso
{term}`theta` · {term}`coverage` · {term}`confidence level` · {term}`confidence interval` ·
{term}`credible interval` · {term}`prior` · {term}`standard error` · {term}`zero-width interval` ·
{term}`aberration` · {term}`tail probability` · {term}`p-value`
:::
