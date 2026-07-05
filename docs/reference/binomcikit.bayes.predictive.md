# `bayes.predictive`

```{eval-rst}
.. module:: binomcikit.bayes.predictive
```

**Posterior predictive probabilities** (6xx family). After observing `x`
successes in `n` past trials under a `Beta(a1, a2)` prior, what is the
probability of seeing `xnew` successes in `m` **future** trials? Averaging the
binomial likelihood over the `Beta(x + a1, n − x + a2)` posterior gives the
**Beta-Binomial** predictive distribution.

```{contents} Functions in this module
:local:
:depth: 1
```

---

## `probpre`

```{eval-rst}
.. autofunction:: binomcikit.bayes.predictive.probpre
```

**In plain words** — A table of predictive probabilities: for each past outcome
`x = 0…n` (columns) and each future outcome `xnew = 0…m` (rows), the probability
of `xnew` future successes given `x` past successes. Each column is a proper
distribution over `xnew` (sums to 1).

**The maths** — The Beta-Binomial predictive probability

$$\Pr(x_{\text{new}} \mid x) = \binom{m}{x_{\text{new}}}\,
\frac{B(x_{\text{new}}+x+a_1,\; m+n-x_{\text{new}}-x+a_2)}{B(x+a_1,\; n-x+a_2)},$$

where `B` is the Beta function.

**Example**

```python
import binomcikit as bk
bk.probpre(3, 2, 1, 1)     # n=3 past, m=2 future, uniform prior
#    xnew       0    1    2       3
# 0     0  0.6667  0.4  0.2  0.0667
# 1     1  0.2667  0.4  0.4  0.2667
# 2     2  0.0667  0.2  0.4  0.6667    (each column sums to 1)
```

**R source** — [`R/621.Poster_Predictive.R`](https://github.com/RajeswaranV/proportion/blob/master/R/621.Poster_Predictive.R), function `probPRE`

```r
prepro[j,i]=(choose(m,xnew[j]))/(beta(x[i]+a1,n-x[i]+a2))*
            beta(xnew[j]+x[i]+a1, m+n-xnew[j]-x[i]+a2)
```

**What the R code does** — Fills a `(m+1) × (n+1)` matrix of Beta-Binomial
predictive probabilities and returns it with an `xnew` column and columns
labelled `0…n`.

**Python source** — `binomcikit.bayes.predictive.probpre`

```python
def probpre(n, m, a1, a2):
    xnew = np.arange(m + 1)
    data = {'xnew': xnew}
    for xi in range(n + 1):
        data[str(xi)] = (comb(m, xnew) / beta_fn(xi + a1, n - xi + a2)
                         * beta_fn(xnew + xi + a1, m + n - xnew - xi + a2))
    return pd.DataFrame(data)
```

**What the Python code does** — Builds the same table with
`scipy.special.comb` and `scipy.special.beta`, one column per past `x`.

**R → Py changes** — Naming lowercased; R matrix → pandas `DataFrame`;
`choose`/`beta` → `scipy.special.comb`/`scipy.special.beta`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `probprex`

```{eval-rst}
.. autofunction:: binomcikit.bayes.predictive.probprex
```

**In plain words** — A single predictive probability: the chance of exactly
`xnew` successes in `m` future trials, given `x` successes in `n` past trials.

**The maths** — The same Beta-Binomial formula as `probpre`, evaluated at one
`(x, xnew)`.

**Example**

```python
import binomcikit as bk
bk.probprex(2, 10, 1, 5, 1, 1)   # x=2/10 past, xnew=1 of m=5 future
#    x   n  xnew  m   preprb
# 0  2  10     1  5  0.33997
```

**R source** — [`R/622.Poster_Predictive_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/622.Poster_Predictive_x.R), function `probPREx`

**What the R code does** — Evaluates the Beta-Binomial predictive probability for
the single `(x, xnew)` and returns `x, n, xnew, m, preprb`.

**Python source** — `binomcikit.bayes.predictive.probprex` — the one-cell
computation with `scipy.special.comb`/`beta`.

**What the Python code does** — Returns the single predictive probability as a
one-row `DataFrame`.

**R → Py changes** — Naming lowercased; pandas `DataFrame`;
`choose`/`beta` → `scipy.special`. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`
