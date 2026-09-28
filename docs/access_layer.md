# The access layer

The statistical core mirrors the peer-reviewed R `proportion` package function-for-function. On top of
it, binomcikit adds a small **usability layer** the R original never had — conveniences for getting data
in, pulling out estimates and curves, and comparing methods in one call. None of these add new
statistics; they just make the engine easier to reach.

Every linked term goes to the {doc}`glossary`.

---

## Getting data in — `from_data`, `from_counts`
The whole package works from the sufficient statistic `(x, n)`. If you have raw 0/1 data instead, turn
it into counts:

```python
import binomcikit as bk

x, n = bk.from_data([1, 0, 1, 1, 0, 0, 1])   # -> (4, 7)
bk.ci(x, n=n, method="wilson")

bk.from_counts(3, 20)                          # -> (3, 20), with validation
```

`from_data` accepts any 0/1 or `True`/`False` sequence; `from_counts` is a guard that returns clean
integers and rejects impossible pairs (like x > n).

## Point estimates — `point_estimate`
A single best guess for {term}`theta`, in whichever flavour you need:

```python
bk.point_estimate(3, 20, "mle")        # 0.15  — the sample proportion x/n
bk.point_estimate(0, 20, "laplace")    # 0.045 — flat-prior posterior mean (nonzero at x = 0!)
bk.point_estimate(3, 20, "jeffreys")   # Jeffreys posterior mean
bk.point_estimate(3, 20, "ac")         # Agresti–Coull centre (x + z²/2)/(n + z²)
```

Unlike the raw {term}`maximum likelihood estimate` x/n, the Bayesian and Agresti–Coull estimates are
pulled gently toward ½, so they stay sensible at the boundary.

## The Beta posterior — `posterior`, `prior`
Summarise the full {term}`posterior` for a Bayesian analysis:

```python
post = bk.posterior(3, 20, a=1, b=1)
post["mean"], post["mode"], post["sd"]         # point summaries
post["quantile_interval"]                      # equal-tailed credible interval
post["hpd_interval"]                           # shortest (HPD) credible interval

bk.prior("jeffreys")                           # (0.5, 0.5) — named-prior lookup
```

Named priors: `jeffreys` (½, ½), `laplace`/`uniform` (1, 1), `haldane` (0, 0). See {doc}`methods/bayes`
and the {doc}`bayesian_toolbox` for the full Bayesian feature set.

## The curves behind the plots — `coverage_curve`, `length_curve`
{doc}`plot_coverage <methods/wald>` draws a picture; these hand you the numbers as a tidy `DataFrame`,
so you can analyse the {term}`coverage` and {term}`expected length` yourself:

```python
bk.coverage_curve(n=20, method="wilson")       # DataFrame(theta, coverage)
bk.length_curve(n=20, method="blaker")         # DataFrame(theta, expected_length)
```

No plotting stack required — this is pure data.

## Comparing methods — `compare`
"I observed `x` of `n`; what does each method actually give me?" — one table, sorted narrowest to widest:

```python
bk.compare(x=3, n=20)
#            method    lower    upper    width
#           ArcSine    0.032    0.335    0.303
#          Jeffreys    0.044    0.349    0.304
#               ...      ...      ...      ...
#   Clopper-Pearson    0.032    0.379    0.347
```

## Letting the package choose — `recommend`
Turn the {doc}`method-selection guide <method_selection>` into code: `recommend` measures every method
on the metric engine (over a grid of the true proportion) and ranks them.

```python
bk.recommend(n=20, by="length")         # narrowest — among methods that actually cover
bk.recommend(n=20, by="coverage")       # closest mean coverage to nominal
bk.recommend(n=20, by="min_coverage")   # highest guaranteed coverage (exact methods win)
```

`by="length"` is careful: it ranks by width **but only among adequately-covering methods**, so a
method that is narrow merely because it {term}`under-covers <coverage>` (Wald, ArcSine) never wins on a
technicality. The returned table carries `mean_coverage`, `min_coverage`, `mean_length` and an
`adequate` flag so you can see the trade-off yourself.

## Testing a hypothesis — `pvalue`, `reject`

:::{admonition} New in binomcikit
:class: important
**Not part of R `proportion`.** By {term}`CI-test duality`, a confidence interval and a two-sided test
say the same thing — the 2017 paper treats them as interchangeable and explicitly does not add separate
test functions. binomcikit adds them anyway, both for convenience and because the duality is only
*approximate* for some methods (see Wald below) — worth exposing rather than leaving implicit.
:::

*"Is `theta0` a plausible value, given what I observed?"* — `pvalue` answers it for **any** method
binomcikit ships, by finding the smallest α at which `theta0` falls outside that method's `(1-α)` CI:

```python
bk.pvalue(3, 20, 0.5, method="exact")      # 0.0026 -- theta0 = 0.5 is very implausible for x=3, n=20
bk.pvalue(3, 20, 3 / 20, method="wilson")  # 1.0    -- theta0 == phat is never rejected

bk.reject(3, 20, 0.5, method="exact", alpha=0.05)   # True
```

`reject` is a one-line convenience: `pvalue(...) < alpha`. Both are defined **directly from the CI**,
so — unlike a bolted-on test formula — they are guaranteed by construction to agree with
{doc}`bk.ci <methods/index>`: `theta0` is rejected at level α if and only if it sits outside
`bk.ci(x=x, n=n, alpha=alpha, method=method)`. Not supported for the bootstrap family (`method="boot"`
and its `kind` variants) — a stochastic CI makes "the α where the boundary crosses `theta0`" ill-defined
without pinning one seed across the whole search.

:::{admonition} Wald disagrees with everyone else here — on purpose, and it's real
:class: warning
`bk.pvalue(3, 20, 0.5, method="wald")` comes out **~500× smaller** than the same test under Wilson or
Clopper–Pearson. This is not a bug: Wald's width is set by the variance at `phat` (here `0.15`), not at
the `theta0` being tested (`0.5`), so it under-estimates its own uncertainty whenever `phat` and `theta0`
are far apart — the interval is too narrow, so the dual test rejects too eagerly. It is exactly the
"duality is only approximate for some methods" gap this feature exists to expose; see
`tests/test_pvalue.py::test_wald_pvalue_diverges_from_score_based_methods`.
:::

:::{admonition} This is not `scipy.stats.binomtest`
:class: note
`bk.pvalue`'s two-sided p-value is **equal-tailed** — `2 * min(P(X≤x), P(X≥x))`, capped at 1, the
convention dual to binomcikit's own equal-tailed CIs (Clopper–Pearson, Wilson, …). `scipy.stats.binomtest`'s
default two-sided p-value uses a different ("minlike", smallest-probability) convention, and the two
genuinely disagree away from `theta0 ≈ phat` — at `x=3, n=20, theta0=0.05` binomcikit gives exactly
**2×** scipy's number. Both are legitimate; they are not the same test. binomcikit's choice is the one
that stays consistent with its own CIs.
:::

## Planning a study — `sample_size`, `power`

:::{admonition} New in binomcikit
:class: important
**Not part of R `proportion`.** {term}`Sample size` determination is a *pre-data* design question,
outside the scope of interval *estimation* — the 2017 paper cites a dedicated R package
(`binomSamSize`) rather than duplicating it. binomcikit adds both here because they're the natural
questions to ask *before* collecting data, and because — unlike the textbook Wald-only formula —
`sample_size` works for **any** method.
:::

*"How many trials do I need?"* and *"if I run this study, how likely am I to actually detect the
effect?"* — the two questions you ask before collecting any data:

```python
bk.sample_size(0.1, method="wilson")            # 381 -- trials needed for CI width <= 0.1 at p0=0.5
bk.sample_size(0.2, method="wilson")             # 93  -- a looser target needs far fewer

bk.power(100, 0.5, 0.65, method="wilson")        # 0.875 -- P(detect p=0.65 vs H0: p=0.5), n=100
bk.power(100, 0.5, 0.50, method="wilson")        # 0.057 -- at p_true == theta0: this IS the test's size
```

`sample_size(width, alpha=0.05, p0=0.5, method="wilson")` finds the **smallest n** whose `(1-alpha)` CI
is no wider than `width`, evaluated at the `x` nearest `p0 * n` — the standard planning convention:
guess a proportion `p0` (default `0.5`, the worst case — every method's CI is widest there), and ask how
big a sample makes its CI tight enough. Found by binary search (width shrinks monotonically in `n`), so
it's the *exact* answer for that method's real CI, not an approximation borrowed from Wald.

`power(n, theta0, p_true, alpha=0.05, method="wilson")` is the {term}`CI-test duality` companion to
{doc}`pvalue <access_layer>` above: the probability of rejecting `theta0` if the *true* proportion is
`p_true`. Computed exactly (not simulated) — `method`'s CI is built once for the whole `x = 0..n` grid,
then summed against the Binomial(n, p_true) probability of each `x` that would reject.

:::{admonition} Reading `power(100, 0.5, 0.50, ...) = 0.057`, not 0.05
:class: note
Evaluating `power` exactly at `p_true == theta0` isn't "power" in the usual sense (there's no real
effect to detect) — it's the test's actual **size**: how often it wrongly rejects a *true* null, purely
from sampling variation. It sits close to the nominal `alpha=0.05` but rarely exact, because x is
discrete — the same discreteness behind every {term}`aberration` flag elsewhere in the package.
:::

Neither function supports the bootstrap family, for the same reason `pvalue`/`reject` don't: a
stochastic CI has no well-defined "width at n" or "rejects at alpha" without pinning one seed across
the whole search.

:::{admonition} Terms used on this page
:class: seealso
{term}`proportion` · {term}`theta` · {term}`estimate` · {term}`maximum likelihood estimate` ·
{term}`confidence interval` · {term}`coverage` · {term}`expected length` · {term}`prior` ·
{term}`posterior` · {term}`posterior mean` · {term}`credible interval` ·
{term}`highest posterior density interval` · {term}`CI-test duality` · {term}`p-value` ·
{term}`null hypothesis` · {term}`sample size` · {term}`statistical power` · {term}`effect size` ·
{term}`aberration`
:::
