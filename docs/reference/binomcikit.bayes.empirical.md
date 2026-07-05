# `bayes.empirical`

```{eval-rst}
.. module:: binomcikit.bayes.empirical
```

**Empirical Bayes credible intervals** (6xx family). Instead of fixing the
`Beta(a, b)` prior, these functions **estimate it from the data**: for each `x`
they find the prior parameters that maximise the Beta-Binomial marginal
likelihood (subject to bounds `[sL, sU]`), then report the resulting posterior
credible intervals — both quantile-based and HPD — plus the posterior mean.

The R spelling `empericalBA`/`empericalBAx` (a typo in the original package) is
kept as an alias; the correctly-spelled `empiricalba`/`empiricalbax` are the
canonical names.

```{contents} Functions in this module
:local:
:depth: 1
```

---

## `empiricalba`

```{eval-rst}
.. autofunction:: binomcikit.bayes.empirical.empiricalba
```

**In plain words** — Like {py:func}`ciba <binomcikit.ci.bayes_n.ciba>`, but the
prior isn't chosen by you — it's fitted to the data by maximum marginal
likelihood. Reported for every `x = 0…n`: posterior mean, quantile interval
`(LEBAQ, UEBAQ)` and HPD interval `(LEBAH, UEBAH)`.

**The maths** — For each `x`, maximise the Beta-Binomial marginal likelihood

$$\mathcal{L}(a, b) = \binom{n}{x}\frac{B(x+a,\, n-x+b)}{B(a, b)}$$

over `a, b ∈ [sL, sU]`, then summarise the `Beta(x + â, n − x + b̂)` posterior.

**Example**

```python
import binomcikit as bk
bk.empiricalba(5, 0.05, 0.1, 10)     # bounds sL=0.1, sU=10
#    x  pomean   LEBAQ   UEBAQ   LEBAH   UEBAH
# 0  0  0.0066  0.0000  0.0650  0.0000  0.0391
# ...                                          (rounded to 4 dp, as in R)
```

**R source** — [`R/611.Empirical.R`](https://github.com/RajeswaranV/proportion/blob/master/R/611.Empirical.R), function `empericalBA`

```r
likelhd = function(y){ a<-y[1]; b<-y[2]
  -(choose(n,x[i])/beta(a,b))*beta(x[i]+a, n-x[i]+b) }
mle = stats::optim(c(0.1,0.1), likelhd, method="L-BFGS-B",
                   lower=sL, upper=sU)$par
# ... then qbeta / TeachingDemos::hpd on Beta(x+av, n-x+bv) ...
```

**What the R code does** — For each `x`, minimises the negative marginal
likelihood with `optim` (L-BFGS-B, bounded), then computes the quantile limits
(`qbeta`) and HPD limits (`TeachingDemos::hpd`) of the fitted posterior;
rounds to 4 dp.

**Python source** — `binomcikit.bayes.empirical.empiricalba`

```python
def empiricalba(n, alp, sL, sU):
    for i in range(n + 1):
        a, b = _mle_ab(n, x[i], sL, sU)     # scipy.optimize.minimize, L-BFGS-B
        s1, s2 = x[i] + a, n - x[i] + b
        pomean[i] = (x[i] + a) / (n + a + b)
        lq[i], uq[i] = stats.beta.ppf([alp/2, 1-alp/2], s1, s2)
        lh[i], uh[i] = hpd_beta(s1, s2, conf=1 - alp)
    return df.round(4)
```

**What the Python code does** — Fits `(a, b)` per `x` with
`scipy.optimize.minimize` (L-BFGS-B, same bounds), then uses
`scipy.stats.beta.ppf` and `binomcikit._hpd.hpd_beta` for the interval limits.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. `optim` →
`scipy.optimize.minimize`; `TeachingDemos::hpd` → `_hpd.hpd_beta`. Because the
optimiser start/tolerances differ slightly, the fitted `(a, b)` can differ at
the last decimals; results are rounded to 4 dp as in R.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `empiricalbax`

```{eval-rst}
.. autofunction:: binomcikit.bayes.empirical.empiricalbax
```

**In plain words** — The empirical-Bayes credible interval for a **single
observed `x`**.

**The maths** — The same marginal-likelihood fit and posterior summary as
`empiricalba`, for one `x`.

**Example**

```python
import binomcikit as bk
bk.empiricalbax(2, 5, 0.05, 0.1, 10)
```

**R source** — [`R/612.Empirical_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/612.Empirical_x.R), function `empericalBAx`

**What the R code does** — Fits `(a, b)` for the single `x` and reports the
posterior mean and the quantile/HPD limits.

**Python source** — `binomcikit.bayes.empirical.empiricalbax` — the one-`x` fit
and summary, columns `LEBAQx`/`UEBAQx`/`LEBAHx`/`UEBAHx`.

**What the Python code does** — Same as `empiricalba` for a single `x`.

**R → Py changes** — Naming lowercased; pandas `DataFrame`; `optim` →
`scipy.optimize.minimize`; `TeachingDemos::hpd` → `_hpd.hpd_beta`.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`
