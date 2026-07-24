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

:::{admonition} Terms used on this page
:class: seealso
{term}`proportion` · {term}`theta` · {term}`estimate` · {term}`maximum likelihood estimate` ·
{term}`confidence interval` · {term}`coverage` · {term}`expected length` · {term}`prior` ·
{term}`posterior` · {term}`posterior mean` · {term}`credible interval` ·
{term}`highest posterior density interval`
:::
