---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Difference of two proportions

> **In one line:** you ran two groups (a treatment and a control, version A and version B) and want a
> confidence interval for *how much larger one success rate is than the other* — the
> {term}`risk difference`. Use **Newcombe's hybrid score** by default; use a
> {term}`score interval` (Miettinen–Nurminen) when you want the most defensible interval for a
> regulatory or publication setting.

*New here?* Read {doc}`../foundations/index` first. Every technical word below links to the
{doc}`../glossary`. The rest of the package is about **one** {term}`proportion`; this page is about
**two independent** ones.

This page has two parts: **Use it** (how to call it) and **Understand it** (the maths behind it).

---

## Use it

### Import and call
```python
import binomcikit as bk

# 56 of 70 responded on the new treatment, 48 of 80 on the old one:
bk.diff_interval(56, 70, 48, 80)                       # (lower, upper), Newcombe by default
bk.diff_interval(56, 70, 48, 80, alpha=0.05, method="miettinen-nurminen")

bk.diff_ci(56, 70, 48, 80, method="newcombe")          # a one-row table: estimate, limits, width
bk.list_diff_methods()                                 # the catalogue
```

### Parameters
| name | plain English | formal |
|---|---|---|
| `x1`, `n1` | successes and trials in the first group | counts of the first sample, 0 ≤ x1 ≤ n1 |
| `x2`, `n2` | successes and trials in the second group | counts of the second sample, 0 ≤ x2 ≤ n2 |
| `alpha` | your error budget; `0.05` gives a 95% interval | {term}`alpha` (α), strictly between 0 and 1 |
| `method` | which interval to build | one of the names below |

The interval is for `p1 − p2`. Both limits are clipped into [−1, 1]. Scalars or arrays that
broadcast together are accepted.

### The methods
| `method` | what it is | when to reach for it |
|---|---|---|
| `"newcombe"` (default) | the two {term}`Wilson <score test>` intervals combined (Newcombe's *hybrid score*) | the all-round default: defined for every table, never leaves [−1, 1], near-nominal {term}`coverage` |
| `"newcombe-cc"` | the same from {term}`continuity correction`-widened Wilson intervals | when you must not under-cover (it is conservative) |
| `"miettinen-nurminen"` (`"mn"`, `"score"`) | invert the {term}`score test` for the difference | the recommended "gold-standard" interval; slower (root-finding) |
| `"mee"` | the score interval without the `N/(N−1)` factor | the classical Mee (1984) interval |
| `"agresti-caffo"` | add one success and one failure to each group, then Wald | a very simple, well-behaved closed form |
| `"wald"` | the textbook normal-approximation interval | teaching baseline only |
| `"wald-cc"` | Wald plus the Fleiss {term}`continuity correction` | a conservative Wald |
| `"haldane"` | Haldane's closed form (Newcombe's method 3) | a good closed form that handles zero cells |
| `"jeffreys-perks"` | Haldane's form with Jeffreys–Perks shrunken proportions (method 4) | as above, slightly more conservative at the edges |
| `"hauck-anderson"` | Wald with `n − 1` variances and a `1/(2·min(n1, n2))` correction | needs at least 2 trials per group |
| `"brown-li"` | Wald around the Jeffreys-shrunken proportions `(x + ½)/(n + 1)` | simple and well behaved at the boundaries |
| `"miettinen-nurminen-brown-li"` | two-thirds of the Miettinen–Nurminen limits plus one-third of the Brown–Li limits (Laud & Dane) | a blend that trades their errors against each other |

### What you get back
`diff_interval` returns `(lower, upper)`. `diff_ci` returns a one-row `DataFrame` with `method`,
the four counts, `estimate` (= p̂1 − p̂2), `lower`, `upper` and `width`.

### Examples
```{code-cell} python
import binomcikit as bk

for m in ["wald", "agresti-caffo", "newcombe", "newcombe-cc", "mee", "miettinen-nurminen"]:
    lo, hi = bk.diff_interval(56, 70, 48, 80, 0.05, m)
    print(f"{m:20s} [{lo:+.4f}, {hi:+.4f}]")
```

An empty cell is not a problem for the hybrid and score methods, but it is for Wald:

```{code-cell} python
# 0 of 10 versus 0 of 10: Wald collapses to a single point, Newcombe does not
print(bk.diff_interval(0, 10, 0, 10, 0.05, "wald"))
print(bk.diff_interval(0, 10, 0, 10, 0.05, "newcombe"))
```

### Gotchas
- This is the **difference** `p1 − p2`. Ratios and odds ratios are not covered here.
- The groups must be **independent** (not the same subjects measured twice — that is a paired
  design, which needs a different interval).
- **Wald** returns a zero-width interval when both groups have 0 (or all) successes, and its
  {term}`coverage` is the least reliable of the set.
- **Naming differs between packages.** Here (and in `statsmodels`) `"score"` means the Miettinen–Nurminen interval; in
  the `DBCI` package `"score"` is an alias of Newcombe's hybrid score.
- Swapping the groups negates the interval: `diff_interval(x2, n2, x1, n1)` returns
  `(−upper, −lower)`.

---

## Understand it

### The idea, before any symbols
Each group has its own wobble (see the {doc}`Wald <wald>` page). The difference of two wobbly
numbers wobbles more than either one alone. The cheap answer adds the two wobbles together and
stretches a symmetric interval around the difference — the **Wald** interval. It inherits Wald's
problems for each group. The better answers keep the idea but borrow a good single-group
interval (Wilson) or a good *test* (the {term}`score test`).

### Newcombe's hybrid score
Take the Wilson interval `(l1, u1)` for the first group and `(l2, u2)` for the second. With
`d = p̂1 − p̂2`:

$$L = d - \sqrt{(\hat p_1 - l_1)^2 + (u_2 - \hat p_2)^2}, \qquad
U = d + \sqrt{(u_1 - \hat p_1)^2 + (\hat p_2 - l_2)^2}.$$

The lower limit uses the *lower* distance of the first group and the *upper* distance of the
second, because the difference is smallest when `p1` is as small and `p2` as large as their
intervals allow. Combining distances in quadrature (not by adding) is what keeps the result
honest. The `-cc` version swaps in {term}`continuity correction` Wilson limits.

### Score intervals: Miettinen–Nurminen and Mee
For a hypothesised difference `δ`, find the {term}`restricted maximum likelihood estimate`
`(p̃1, p̃2)` — the most likely pair of rates *subject to* `p1 − p2 = δ` — and form

$$Z^2(\delta) = \frac{(\hat p_1 - \hat p_2 - \delta)^2}{\lambda\left(\tilde p_1\tilde q_1 / n_1 + \tilde p_2\tilde q_2 / n_2\right)}, \qquad q = 1 - p,$$

with `λ = 1` (Mee) or `λ = N/(N−1)`, `N = n1 + n2` (Miettinen–Nurminen). The interval is every
`δ` with `Z²(δ) ≤ z²`. There is no closed form, so the limits are found by root-finding on each
side of the estimate; the restricted estimate itself is found by solving a one-dimensional
equation (the log-likelihood is concave in `p̃1`, so the solution is unique).

:::{dropdown} How the code finds the limits
`_restricted_mle` solves the derivative of the restricted log-likelihood in `p̃1` on the allowed
range `[max(0, δ), min(1, 1 + δ)]` (it returns an endpoint when the derivative never changes sign,
which is what happens for zero cells). `_score_limits` then brackets the crossing
`Z²(δ) = z²` between the estimate `d` and the edge `±1` and calls Brent's method to full double
precision. If `Z²` never reaches `z²` before the edge, the limit is the edge itself.
:::

### How well do they work? Exact coverage
For two groups of 15, the exact {term}`coverage` (every possible table, weighted by its binomial
probability, at 95% nominal) at five representative `(p1, p2)` pairs:

```{code-cell} python
import numpy as np
from scipy import stats
import binomcikit as bk

def exact_coverage(method, n1, n2, p1, p2, alpha=0.05):
    w1 = stats.binom.pmf(np.arange(n1 + 1), n1, p1)
    w2 = stats.binom.pmf(np.arange(n2 + 1), n2, p2)
    delta, cov = p1 - p2, 0.0
    for x1 in range(n1 + 1):
        for x2 in range(n2 + 1):
            lo, hi = bk.diff_interval(x1, n1, x2, n2, alpha, method)
            cov += w1[x1] * w2[x2] * (lo - 1e-12 <= delta <= hi + 1e-12)
    return cov

grid = [(0.3, 0.2), (0.5, 0.5), (0.7, 0.4), (0.15, 0.1), (0.9, 0.8)]
rows = {m: [exact_coverage(m, 15, 15, a, b) for a, b in grid]
        for m in ["wald", "agresti-caffo", "newcombe", "newcombe-cc", "mee", "miettinen-nurminen"]}
import pandas as pd
pd.DataFrame(rows, index=[f"p1={a}, p2={b}" for a, b in grid]).round(3)
```

Reading the table: Wald dips below 0.95 at several pairs; the hybrid and score intervals sit
close to 0.95; the `-cc` version sits above it (conservative by design). This page has a
coverage **table** rather than a figure; for a figure of one method's whole coverage curve use
the single-proportion tools in {doc}`../evaluating_intervals`.

### Verified against
* **Published tables:** 88 intervals from Newcombe (1998), Table II (as recast in the SAS paper *Constructing Confidence Intervals for the
  Differences of Binomial Proportions in SAS*) and SAS output, for twelve methods (all of those above) on nine tables including the boundary ones (0/10 vs 0/20, 10/10 vs 0/10), all within the four printed
  decimals (`tests/test_twoprop.py::test_matches_published_tables`).
* **Software manuals:** the SAS paper and the PASS manual print the same definitions (Mee: `λ = 1`; Miettinen–Nurminen: `λ = N/(N−1)`
  and the closed-form constrained estimate; Newcombe's methods 10 and 11).
* **Other implementations:** `"wald"`, `"agresti-caffo"` and `"newcombe"` agree with `statsmodels.stats.proportion.
  confint_proportions_2indep` to 1e-12, and `"wald-cc"` / `"newcombe-cc"` agree with the `DBCI` package to 1e-9. The two score methods
  solve the defining equation `Z²(δ) = z²` to ~1e-15 at every interior limit (checked directly in the tests, because `DBCI`'s score
  limits are only accurate to ~1e-5 and the released `statsmodels` `score` option used the wrong constrained estimate, fixed on its
  `main`; see `planning/COMPETITOR_REPOS.md`).
* **Not yet:** a first-hand read of Newcombe (1998), Miettinen & Nurminen (1985) and Mee (1984) themselves; they are paywalled
  (`planning/PAPERS_TO_DOWNLOAD.md`). The Mee citation here (Biometrics 40) is from memory and should be confirmed.

### References
Newcombe (1998), *Statistics in Medicine* 17, 873–890 · Miettinen & Nurminen (1985), *Statistics
in Medicine* 4, 213–226 · Mee (1984), *Biometrics* 40, 1175–1176 · Agresti & Caffo (2000),
*The American Statistician* 54, 280–288 · Fagerland, Lydersen & Laake (2011), *Statistical Methods
in Medical Research* 24.
