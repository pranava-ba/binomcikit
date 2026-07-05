# `ci.bayes_n_x`

```{eval-rst}
.. module:: binomcikit.ci.bayes_n_x
```

The **given-*x*** counterpart of the Bayesian credible interval in
{doc}`ci.bayes_n <binomcikit.ci.bayes_n>`: the same `Beta(x + a, n − x + b)`
posterior summary (quantile and HPD), but for a **single observed `x`**, returned
as one row.

```{contents} Functions in this module
:local:
:depth: 1
```

---

## `cibax`

```{eval-rst}
.. autofunction:: binomcikit.ci.bayes_n_x.cibax
```

**In plain words** — The Bayesian quantile and HPD credible intervals for the
one `x` you observed, under a `Beta(a, b)` prior. See
{py:func}`ciba <binomcikit.ci.bayes_n.ciba>` for the full explanation.

**The maths** — Posterior `Beta(x + a, n − x + b)`; quantile limits from its
inverse-CDF at `α/2` and `1 − α/2`, HPD limits from the shortest `1 − α`
interval.

**Example**

```python
import binomcikit as bk
bk.cibax(2, 10, 0.05, 1, 1)      # uniform prior Beta(1, 1)
#    x   LBAQx     UBAQx   LBAHx    UBAHx
# 0  2  0.0602    0.5178   0.0406   0.4837
```

**R source** — [`R/103.ConfidenceIntervals_BASE_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/103.ConfidenceIntervals_BASE_n_x.R), function `ciBAx`

```r
LBAQx=stats::qbeta(alp/2, x+a, n-x+b)
UBAQx=stats::qbeta(1-(alp/2), x+a, n-x+b)
LBAHx=TeachingDemos::hpd(stats::qbeta, shape1=x+a, shape2=n-x+b, conf=1-alp)[1]
UBAHx=TeachingDemos::hpd(stats::qbeta, shape1=x+a, shape2=n-x+b, conf=1-alp)[2]
```

**What the R code does** — Reads the quantile limits from `stats::qbeta` and the
HPD limits from `TeachingDemos::hpd` for the single `x`.

**Python source** — `binomcikit.ci.bayes_n_x.cibax`

```python
def cibax(x, n, alp, a, b):
    s1, s2 = x + a, n - x + b
    lbaqx = stats.beta.ppf(alp / 2, s1, s2)
    ubaqx = stats.beta.ppf(1 - alp / 2, s1, s2)
    lbahx, ubahx = hpd_beta(s1, s2, conf=1 - alp)
    return pd.DataFrame([{'x': x, 'LBAQx': lbaqx, 'UBAQx': ubaqx,
                          'LBAHx': lbahx, 'UBAHx': ubahx}])
```

**What the Python code does** — One-row quantile + HPD credible interval, using
`scipy.stats.beta.ppf` and `binomcikit._hpd.hpd_beta`.

**R → Py changes** — Naming lowercased; pandas `DataFrame`; `TeachingDemos::hpd`
reimplemented in SciPy (`_hpd.hpd_beta`). Numerically consistent with `ciba` at
that `x`.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`
