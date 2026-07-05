# `_hpd`

```{eval-rst}
.. module:: binomcikit._hpd
```

A small internal helper that reimplements R's `TeachingDemos::hpd` for a Beta
distribution. The R package uses `TeachingDemos::hpd` in every Bayesian
computation (the credible interval `ciba`/`cibax`, empirical Bayes, and the
Bayesian variants of coverage/length/p-confidence/error). Since that R package
has no Python equivalent, `hpd_beta` provides the same **highest-posterior-density
interval** using SciPy.

```{contents} Functions in this module
:local:
:depth: 1
```

---

## `hpd_beta`

```{eval-rst}
.. autofunction:: binomcikit._hpd.hpd_beta
```

**In plain words** — Returns the **shortest** interval that contains a given
probability mass (`conf`) of a `Beta(a, b)` distribution. For a skewed
posterior this is tighter than the equal-tailed (quantile) interval, and it is
what the Bayesian functions report as their HPD limits.

**The maths** — Among all intervals `[ℓ, u]` with `Beta`-mass `conf`, the HPD
interval is the one of minimum width. Parameterising by the lower-tail
probability `p`, it minimises

$$w(p) = F^{-1}(p + \text{conf}) - F^{-1}(p), \qquad p \in [0,\,1-\text{conf}],$$

where `F⁻¹` is the Beta inverse-CDF. The minimiser gives the HPD endpoints.

**Example**

```python
from binomcikit._hpd import hpd_beta
hpd_beta(2 + 1, 8 + 1, conf=0.95)   # HPD of Beta(3, 9) at 95%
# (lower, upper) — never wider than the equal-tailed quantile interval
```

**R source** — R uses [`TeachingDemos::hpd`](https://cran.r-project.org/package=TeachingDemos)
called as `TeachingDemos::hpd(stats::qbeta, shape1=..., shape2=..., conf=1-alp)`.

**What the R code does** — `TeachingDemos::hpd` numerically minimises the
interval width `qbeta(p + conf) − qbeta(p)` over the lower-tail probability `p`,
returning the two endpoints.

**Python source** — `binomcikit._hpd.hpd_beta`

```python
def hpd_beta(a, b, conf=0.95):
    alpha = 1.0 - conf
    def width(p):
        return beta.ppf(p + conf, a, b) - beta.ppf(p, a, b)
    p = minimize_scalar(width, bounds=(0.0, alpha), method="bounded").x
    lo, hi = beta.ppf(p, a, b), beta.ppf(p + conf, a, b)
    return (0.0 if not np.isfinite(lo) else lo,
            1.0 if not np.isfinite(hi) else hi)
```

**What the Python code does** — Performs the same bounded 1-D minimisation with
`scipy.optimize.minimize_scalar`, evaluating Beta quantiles via
`scipy.stats.beta.ppf`, and guards the degenerate-prior boundary cases.

**R → Py changes** — `TeachingDemos::hpd` (external R package) reimplemented from
scratch in SciPy. The defining property is verified in the test suite: the HPD
width is never greater than the quantile-interval width.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`
