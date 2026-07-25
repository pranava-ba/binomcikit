---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Choosing a method for your own data

**The situation.** You have a real count — say **2 successes in 30 trials** — and the library offers a
dozen intervals. The {doc}`method-selection guide <../method_selection>` gives good defaults, but you'd
like the software to *measure* the options on data shaped like yours and tell you which is best. That is
exactly what `compare` and `recommend` are for.

**The question.** For *my* $n$, which method gives the best interval — and "best" by which yardstick?

## Choosing a method (with the tools)

Two functions, two jobs:

- **`compare(x, n)`** — every method's actual interval *for your specific count*, side by side. Good for
  seeing how much the choice moves the answer today.
- **`recommend(n, by=...)`** — measures each method's {term}`coverage` and {term}`expected length` across
  *all* counts at your $n$, then ranks them by a strategy you pick. Good for choosing a method *before* you
  even look at the data.

## Running it

Start with the intervals for your count:

```{code-cell} python
import binomcikit as bk

bk.compare(2, 30)      # every method's 95% interval for x = 2, n = 30, sorted by width
```

The narrowest row is **Wald** — but look at its `lower`: it is `0.000`, sitting right on the boundary (the
edge of the {term}`zero-width interval` collapse). *Narrowest is not best* if the method is cheating at the
edge. To separate genuine quality from a lucky-looking width, let `recommend` measure coverage too:

```{code-cell} python
bk.recommend(30, by="length").head(4)      # narrowest interval *among methods that cover adequately*
```

The `adequate` column flags methods whose {term}`coverage` is acceptably close to nominal; `recommend`
ranks only those, so Wald — which under-covers — never wins. You can switch the yardstick:

```{code-cell} python
strategies = {by: bk.recommend(30, by=by).iloc[0]["method"]
              for by in ["length", "coverage", "min_coverage"]}
strategies
```

## Reading the result

Three honest strategies, three (sometimes different) winners:

- **`by="length"`** — the *narrowest* interval among adequately-covering methods. Here it is the
  {doc}`likelihood-ratio <../methods/lr>` interval, with {doc}`Jeffreys <../methods/bayes>` and
  {doc}`Wilson <../methods/wilson>` close behind. Choose this when precision matters and slightly-below-95%
  worst-case coverage is acceptable.
- **`by="coverage"`** — the method whose coverage sits *closest to* 95% on average. {doc}`Jeffreys
  <../methods/bayes>` wins. Choose this when you want honesty over sharpness.
- **`by="min_coverage"`** — the best *worst-case* coverage, i.e. the strongest guarantee. {term}`Clopper–Pearson`
  and {doc}`Blaker <../methods/blaker>` win — they never dip below 95%, at the cost of being wider. Choose
  this when under-covering is unacceptable (safety, regulatory).

There is no single winner because "best" is a choice: tightness, calibration, or a guarantee. `recommend`
makes that choice explicit instead of hiding it.

## How to report it

> Method chosen in advance by `recommend(n=30, by="length")`: the likelihood-ratio interval, the narrowest
> among methods with adequate coverage at n = 30. For x = 2 it gives a 95% interval of 1.1–19.2%.

## What could go wrong

- **Picking a method after seeing which gives the answer you want.** Choose the *strategy* before the
  data (that is what `recommend(n, ...)` is for — it never looks at x). Cherry-picking the narrowest of the
  twelve *post hoc* inflates your error rate.
- **Trusting width alone.** Wald and Wald-T often look narrowest precisely because they under-cover; always
  read coverage alongside length, which is why `recommend` reports both.
- **Extrapolating across n.** The ranking can change with $n$; re-run `recommend` for your actual sample
  size rather than reusing a rule of thumb.

## Try it yourself

You will collect $n = 200$ and you cannot tolerate under-coverage. Which method does `recommend` pick, and
why is it wider than the `by="length"` choice?

:::{dropdown} Solution
```python
import binomcikit as bk
bk.recommend(200, by="min_coverage").iloc[0]["method"]     # -> "Clopper-Pearson"
```
{term}`Clopper–Pearson` — it is built to guarantee coverage ≥ 95% for *every* θ, so it wins the worst-case
yardstick. That guarantee is bought with width: it is deliberately conservative (see {doc}`the exact-methods
theory <../theory/04_exact_and_discreteness>`), so it will be wider than the `by="length"` pick, which only
needs *adequate* coverage.
:::

---

:::{admonition} Terms used on this page
:class: seealso
{term}`coverage` · {term}`expected length` · {term}`confidence interval` · {term}`zero-width interval` ·
{term}`Clopper–Pearson`
:::

*See also: {doc}`the method-selection guide <../method_selection>` · {doc}`the access layer
<../access_layer>` · {doc}`coverage theory <../theory/07_coverage_theory>`.*
