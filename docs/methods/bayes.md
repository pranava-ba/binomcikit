# Bayesian credible interval

> **In one line:** a different *kind* of interval. Instead of a frequentist guarantee, it reports where
> {term}`theta` probably lies **given your data and a {term}`prior` belief** — a statement you can read
> directly ("95% chance θ is in here"). With the Jeffreys {term}`prior` its frequentist {term}`coverage`
> is also excellent, so it doubles as one of the best-behaved intervals on this site.

*New here?* Read {doc}`../foundations/index` first — it explains proportions, trials, and what a
confidence interval means, with no maths. Every technical word below is a link to the
{doc}`../glossary`. This page covers the credible **interval**; the wider Bayesian toolbox (Bayes
factors, empirical Bayes, posterior predictive) has its own page: {doc}`../bayesian_toolbox`.

This page has two parts: **Use it** (how to call it) and **Understand it** (the maths behind it).

---

## Use it

### Import and call
```python
import binomcikit as bk

# flat Beta(1, 1) prior (uniform):
bk.ci(x=3, n=20, method="bayes")

# the Jeffreys prior Beta(0.5, 0.5) — the recommended objective choice:
bk.ci(x=3, n=20, method="jeffreys")

# any Beta(a, b) prior via the flat function:
bk.ciba(20, 0.05, a=2, b=2)
```

### Parameters
| name | plain English | formal |
|---|---|---|
| `x` | how many successes you saw (optional; omit for all x) | the observed count, 0 ≤ x ≤ n |
| `n` | how many trials in total | the number of {term}`Bernoulli trial`s |
| `alpha` | your error budget; `0.05` gives a 95% interval | {term}`alpha` (α); credibility is 1 − α |
| `a`, `b` | the {term}`prior` Beta shape — `1, 1` is uniform, `0.5, 0.5` is Jeffreys | Beta(a, b) {term}`prior` |

### What you get back
A table (pandas `DataFrame`) with the posterior summary and **two** intervals per `x`:

| column | meaning |
|---|---|
| `pomean` | the **{term}`posterior mean`** (x+a)/(n+a+b) — the Bayesian point {term}`estimate` |
| `LBAQ`, `UBAQ` | the equal-tailed (**q**uantile) {term}`credible interval` |
| `LBAH`, `UBAH` | the **{term}`highest posterior density interval`** (HPD) — the shortest credible interval |

### Examples
The paper's worked example, `n = 5`, `alpha = 0.05`, flat Beta(1, 1) prior:

| x | pomean | quantile [LBAQ, UBAQ] | HPD [LBAH, UBAH] |
|---:|---:|---|---|
| 0 | 0.143 | [0.004, 0.459] | [0.000, 0.393] |
| 1 | 0.286 | [0.043, 0.641] | [0.018, 0.591] |
| 2 | 0.429 | [0.118, 0.777] | [0.105, 0.761] |
| 3 | 0.571 | [0.223, 0.882] | [0.239, 0.895] |
| 4 | 0.714 | [0.359, 0.957] | [0.409, 0.982] |
| 5 | 0.857 | [0.541, 0.996] | [0.607, 1.000] |

Two things stand out. At **x = 0** the posterior mean is 0.143, *not* 0 — the {term}`prior` keeps θ
away from the impossible-to-defend value of exactly 0. And the **HPD** interval is never wider than the
quantile one (at x = 0 it becomes one-sided, `[0, 0.393]`), because it is by definition the shortest.

### Recipes
- **Jeffreys interval:** `method="jeffreys"` (a = b = 0.5) — its equal-tailed limits equal
  `statsmodels`' `method="jeffreys"` exactly, and its frequentist coverage is excellent.
- **No adjusted or CC variant.** Like the exact family, the Bayesian interval is **base-only**; `h=`
  and `c=` do not apply.
- **The rest of the toolbox:** {term}`Bayes factor`s, {term}`empirical Bayes`, posterior probabilities
  and the {term}`posterior predictive` all live on the {doc}`../bayesian_toolbox` page.
- **Plot it (interactive, Plotly):** `bk.plot_coverage(n=20, methods=["jeffreys", "bayes", "wilson"])`.

### Gotchas
- **It answers a different question.** A credible interval is a probability statement about θ *given*
  your prior; a {term}`confidence interval` is a statement about the long-run behaviour of the
  procedure. They often look similar but mean different things — say which you are reporting.
- **The prior matters most when data are scarce.** At small `n` the choice of `a, b` visibly moves the
  interval; at large `n` the data dominate and the prior washes out.

---

## Understand it

### The idea, before any symbols
Start with a {term}`prior` — what you believe about {term}`theta` before seeing data, written as a
{term}`Beta distribution`. Run your trials. {term}`Bayesian` updating (Bayes' rule) combines the two
into a {term}`posterior`: a full probability distribution for θ *after* the data. Everything follows
from that curve — its centre is your estimate, and the middle 95% of its area is your interval. Because
the posterior of a {term}`binomial` with a Beta prior is *again* a Beta, all of this is exact and quick.

### The formula
With a {term}`prior` Beta(a, b) and x successes in n trials, the {term}`posterior` is
$$\theta \mid x \;\sim\; \mathrm{Beta}(x+a,\; n-x+b).$$
From it:
- **{term}`posterior mean`:** $\dfrac{x+a}{n+a+b}$.
- **quantile {term}`credible interval`:** the α/2 and 1−α/2 {term}`quantile`s of that Beta (`LBAQ`, `UBAQ`).
- **{term}`highest posterior density interval`:** the shortest interval holding 1−α of the Beta's area
  (`LBAH`, `UBAH`), found numerically.

:::{dropdown} Where it comes from (the derivation)
Bayes' rule says posterior ∝ {term}`likelihood` × {term}`prior`. The binomial likelihood is
∝ θ^x (1−θ)^{n−x}; the Beta(a, b) prior is ∝ θ^{a−1}(1−θ)^{b−1}. Their product is
∝ θ^{x+a−1}(1−θ)^{n−x+b−1} — the kernel of a Beta(x+a, n−x+b). This "Beta prior → Beta posterior"
convenience is called **conjugacy**. The equal-tailed interval just reads off two {term}`quantile`s;
the {term}`highest posterior density interval` instead slides a horizontal line down the density until
the region above it captures 1−α of the area — the shortest such interval, which binomcikit computes
with a small optimiser (`_hpd.hpd_beta`, replacing R's `TeachingDemos::hpd`). The two coincide when the
posterior is symmetric and differ when it is skewed (small x, or x near n).
:::

### When it works — and when it doesn't
The Bayesian interval is always well defined, never collapses, and — with the **Jeffreys** prior — has
{term}`coverage` as good as **Wilson**, which is why Brown, Cai & DasGupta [16] list Jeffreys among
their recommended intervals. Its "weakness" is conceptual, not numerical: the answer depends on the
{term}`prior`, and with very little data a strong prior can dominate. Choose the prior deliberately
(uniform or Jeffreys are safe defaults) and report it.

```{figure} ../_static/bayes_coverage.png
:alt: Coverage probability versus theta for Jeffreys, flat Bayesian and Wilson at n=20
:width: 100%

**Bayesian intervals with excellent frequentist coverage.** True {term}`coverage` against θ for
n = 20, α = 0.05 (produced by binomcikit's own metric engine). The Jeffreys (blue) and flat-prior
(orange) credible intervals oscillate tightly around the nominal 0.95 line, tracking Wilson (green) —
a Bayesian construction that also satisfies the frequentist. Reproduce with
`bk.plot_coverage(n=20, methods=["jeffreys", "bayes", "wilson"])`.
```

### References
The Bayesian credible interval for a proportion and the Jeffreys prior's strong frequentist behaviour
are discussed in Brown, Cai & DasGupta (2001) [16]. The full Bayesian feature set — Bayes factors,
empirical Bayes, posterior predictive — is the novelty of the source R package (Subbiah &
Rajeswaran 2017 [36]); see {doc}`../bayesian_toolbox`. Deeper maths: {doc}`../theory/index`.

---

:::{admonition} Terms used on this page
:class: seealso
{term}`proportion` · {term}`theta` · {term}`trial` · {term}`Bernoulli trial` · {term}`success` ·
{term}`estimate` · {term}`confidence interval` · {term}`coverage` · {term}`alpha` · {term}`quantile` ·
{term}`likelihood` · {term}`prior` · {term}`posterior` · {term}`Bayesian` · {term}`Beta distribution` ·
{term}`credible interval` · {term}`posterior mean` · {term}`highest posterior density interval` ·
{term}`Bayes factor` · {term}`empirical Bayes` · {term}`posterior predictive`
:::
