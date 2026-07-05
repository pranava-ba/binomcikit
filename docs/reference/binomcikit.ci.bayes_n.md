# `ci.bayes_n`

```{eval-rst}
.. module:: binomcikit.ci.bayes_n
```

The **Bayesian credible interval** for a single binomial proportion, for every
`x = 0…n`. With a `Beta(a, b)` prior and `x` successes in `n` trials, the
posterior for `p` is `Beta(x + a, n − x + b)`, and this function summarises it
two ways:

- **Quantile-based** interval `(LBAQ, UBAQ)` — the central `1 − α` interval, cut
  at the `α/2` and `1 − α/2` posterior quantiles.
- **HPD** (highest-posterior-density) interval `(LBAH, UBAH)` — the *shortest*
  interval containing `1 − α` of the posterior mass.

It also returns the **posterior mean** `pomean = (x + a)/(n + a + b)`.

```{contents} Functions in this module
:local:
:depth: 1
```

---

## `ciba`

```{eval-rst}
.. autofunction:: binomcikit.ci.bayes_n.ciba
```

**In plain words** — Turns a `Beta(a, b)` prior belief about the proportion into
posterior credible intervals after observing each possible `x`. The quantile
interval is easy to read; the HPD interval is the tightest interval at the same
credibility and never wider than the quantile one.

**The maths** — Posterior `p | x ∼ Beta(x + a, n − x + b)`.

$$\text{Quantile: } \big(F^{-1}(\alpha/2),\; F^{-1}(1-\alpha/2)\big), \qquad
\text{HPD: } \operatorname*{arg\,min}_{[\ell,u]}\;(u-\ell)\ \text{s.t.}\
\int_{\ell}^{u} f = 1-\alpha,$$

where `f`/`F` are the Beta density/CDF. `a` and `b` may be scalars (one prior
for all `x`) or length-`(n+1)` vectors (a per-`x` prior — R's `ciBAD` path).

**Example**

```python
import binomcikit as bk
bk.ciba(5, 0.05, 0.5, 0.5)         # Jeffreys prior Beta(0.5, 0.5)
#    x  pomean    LBAQ    UBAQ    LBAH    UBAH
# 0  0  0.0833  0.0001  0.3794  0.0000  0.3057   <- HPD narrower than quantile
# ...
```

**R source** — [`R/101.Confidence_base_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/101.Confidence_base_n.R), functions `ciBA` / `ciBAD`

```r
LBAQ[i]=stats::qbeta(alp/2, x[i]+a, n-x[i]+b)
UBAQ[i]=stats::qbeta(1-(alp/2), x[i]+a, n-x[i]+b)
LBAH[i]=TeachingDemos::hpd(stats::qbeta, shape1=x[i]+a, shape2=n-x[i]+b, conf=1-alp)[1]
UBAH[i]=TeachingDemos::hpd(stats::qbeta, shape1=x[i]+a, shape2=n-x[i]+b, conf=1-alp)[2]
```

**What the R code does** — For each `x`, reads the quantile limits from
`stats::qbeta` and the HPD limits from `TeachingDemos::hpd`, and records the
posterior mean. `ciBAD` is the same but with vector priors `a[i]`, `b[i]`.

**Python source** — `binomcikit.ci.bayes_n.ciba`

```python
def ciba(n, alp, a, b):
    a_vec = np.broadcast_to(np.asarray(a, float), (n + 1,))   # scalar or vector prior
    b_vec = np.broadcast_to(np.asarray(b, float), (n + 1,))
    for i in range(n + 1):
        s1, s2 = x[i] + a_vec[i], n - x[i] + b_vec[i]
        pomean[i] = (x[i] + a_vec[i]) / (n + a_vec[i] + b_vec[i])
        lbaq[i] = stats.beta.ppf(alp / 2, s1, s2)
        ubaq[i] = stats.beta.ppf(1 - alp / 2, s1, s2)
        lbah[i], ubah[i] = hpd_beta(s1, s2, conf=1 - alp)     # _hpd.hpd_beta
```

**What the Python code does** — Uses `scipy.stats.beta.ppf` for the quantile
limits and the ported `binomcikit._hpd.hpd_beta` for the HPD limits, handling
scalar and vector priors via NumPy broadcasting (so `ciBA` and `ciBAD` collapse
into one function).

**R → Py changes** — Naming lowercased; pandas `DataFrame`. **`TeachingDemos::hpd`
reimplemented** in SciPy (`_hpd.hpd_beta`, a shortest-interval search). **`ciBAD`
merged into `ciba`** via broadcasting. Verified: HPD width ≤ quantile width at
every `x`.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`
