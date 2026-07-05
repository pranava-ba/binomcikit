# `bayes.posterior`

```{eval-rst}
.. module:: binomcikit.bayes.posterior
```

**Posterior probabilities** (6xx family). Given `x` successes in `n` trials and a
`Beta(a, b)` prior, the posterior for the proportion is `Beta(x + a, n − x + b)`.
These functions report the posterior probability that the proportion lies **below
a threshold `th`** — i.e. the posterior CDF evaluated at `th`.

```{contents} Functions in this module
:local:
:depth: 1
```

---

## `probpos`

```{eval-rst}
.. autofunction:: binomcikit.bayes.posterior.probpos
```

**In plain words** — For every possible `x = 0…n`, the posterior probability
that the true proportion is **less than `th`**, under a `Beta(a, b)` prior. A
Bayesian one-sided statement: "how sure are we, after seeing `x`, that `p < th`?"

**The maths** — Posterior `p | x ∼ Beta(x + a, n − x + b)`; the reported value is

$$\Pr(p < \text{th} \mid x) = F_{\text{Beta}(x+a,\,n-x+b)}(\text{th}).$$

**Example**

```python
import binomcikit as bk
bk.probpos(10, 1, 1, 0.5)     # P(p < 0.5) for each x, uniform prior
#    x  PosProb
# 0  0   0.9844   <- with 0 successes, almost surely p < 0.5
# ...
# 10 10  0.0156
```

**R source** — [`R/641.PosteriorProbs.R`](https://github.com/RajeswaranV/proportion/blob/master/R/641.PosteriorProbs.R), function `probPOS`

```r
for(i in 1:k){
  bet=function(p) stats::dbeta(p, shape1=x[i]+a, shape2=n-x[i]+b)
  PosProb[i]=stats::integrate(bet, 0, th)$value
}
```

**What the R code does** — For each `x`, integrates the Beta posterior density
from 0 to `th` (i.e. computes the posterior CDF at `th`) and returns `x` and
`PosProb`.

**Python source** — `binomcikit.bayes.posterior.probpos`

```python
def probpos(n, a, b, th):
    x = np.arange(n + 1)
    posprob = stats.beta.cdf(th, x + a, n - x + b)
    return pd.DataFrame({'x': x, 'PosProb': posprob})
```

**What the Python code does** — Uses the closed-form Beta CDF
(`scipy.stats.beta.cdf`) instead of numerical integration — exact and vectorised
over all `x`.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. `stats::integrate` of
the Beta density → the analytic `scipy.stats.beta.cdf` (same value, exact).

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `probposx`

```{eval-rst}
.. autofunction:: binomcikit.bayes.posterior.probposx
```

**In plain words** — The same posterior probability `P(p < th)`, but for a
**single observed `x`**.

**The maths** — `Pr(p < th | x) = F_{Beta(x+a, n−x+b)}(th)`.

**Example**

```python
import binomcikit as bk
bk.probposx(5, 8, 2, 3, 0.4)     # x = 5 of 8, prior Beta(2, 3), threshold 0.4
```

**R source** — [`R/642.PosteriorProbs_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/642.PosteriorProbs_x.R), function `probPOSx`

**What the R code does** — Integrates the Beta posterior density from 0 to `th`
for the single `x`.

**Python source** — `binomcikit.bayes.posterior.probposx` — the Beta CDF at `th`
for one `x`, returned as a one-row `DataFrame`.

**What the Python code does** — Evaluates `scipy.stats.beta.cdf(th, x+a, n−x+b)`.

**R → Py changes** — Naming lowercased; pandas `DataFrame`; analytic CDF instead
of `stats::integrate`.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`
