---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Cookbook: copy-paste recipes

Short, self-contained answers to common tasks. Each recipe runs when the docs are built, so the output is
real. Copy one, swap in your numbers.

## An interval from counts

*Problem.* You have $x$ successes in $n$ trials and want a 95% interval.

```{code-cell} python
import binomcikit as bk

bk.ci(27, 100)      # default: Wilson (score) 95% interval
```

*Result.* One row: the lower/upper limits (`LSCx`/`USCx`) and the boundary/`ZWI` flags.

*See also:* {doc}`../methods/wilson` · {doc}`Choosing a method <choosing_a_method>`.

## An interval from raw 0/1 data

*Problem.* You have a list of outcomes, not a count.

```{code-cell} python
data = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1]     # 1 = success
x, n = bk.from_data(data)
bk.ci(x, n)
```

*Result.* `from_data` reduces the list to `(x, n) = (6, 10)`, then `ci` takes over.

*See also:* {doc}`../access_layer`.

## A different method or confidence level

*Problem.* You want Blaker instead of Wilson, or a 90% interval.

```{code-cell} python
{"blaker 95%": tuple(round(float(v), 4) for v in bk.ci(27, 100, method="blaker").iloc[0, 1:3]),
 "wilson 90%": tuple(round(float(v), 4) for v in bk.ci(27, 100, alpha=0.10).iloc[0, 1:3])}
```

*Result.* Any of the twelve methods via `method=`; any level via `alpha=` (0.10 → 90%).

*See also:* {doc}`../method_selection`.

## The probability the rate is below a threshold

*Problem.* A Bayesian "how sure am I that θ < t?" question.

```{code-cell} python
from scipy.stats import beta

post = bk.posterior(4, 200, a=1, b=1)                 # uniform prior -> Beta(5, 197)
round(float(beta.cdf(0.05, post["a_post"], post["b_post"])), 3)   # P(theta < 5%)
```

*Result.* The {term}`posterior probability` mass below the threshold — a direct decision input.

*See also:* {doc}`Quality control <quality_control>` · {doc}`../bayesian_toolbox`.

## A point estimate (and its variants)

*Problem.* Just the single best-guess rate.

```{code-cell} python
{m: round(bk.point_estimate(4, 200, m), 4) for m in ["mle", "ac", "jeffreys", "laplace"]}
```

*Result.* `mle` is the raw $x/n$; the others shrink slightly off the boundary (useful when $x = 0$ or $n$).

*See also:* {doc}`../access_layer`.

## The coverage curve behind the plots

*Problem.* You want the numbers, not a picture.

```{code-cell} python
cov = bk.coverage_curve(50, method="wilson")
cov["coverage"].agg(["mean", "min"]).round(3)
```

*Result.* A tidy DataFrame of {term}`coverage` versus θ; summarise it however you like.

*See also:* {doc}`../evaluating_intervals` · {doc}`coverage theory <../theory/07_coverage_theory>`.

## Every method at once

*Problem.* See how much the method choice moves *your* answer.

```{code-cell} python
bk.compare(27, 100)[["method", "lower", "upper", "width"]].head(5)
```

*Result.* All methods for one count, sorted by width. Pair with `recommend(n, by=...)` to pick one.

*See also:* {doc}`Choosing a method <choosing_a_method>`.

---

:::{admonition} Terms used on this page
:class: seealso
{term}`confidence interval` · {term}`posterior probability` · {term}`coverage` · {term}`maximum likelihood estimate`
:::
