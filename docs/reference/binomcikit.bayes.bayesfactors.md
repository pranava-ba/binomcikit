# `bayes.bayesfactors`

```{eval-rst}
.. module:: binomcikit.bayes.bayesfactors
```

**Bayesian hypothesis testing via Bayes factors** (6xx family). A Bayes factor
`BaFa01` weighs the evidence for a null hypothesis `H0` against an alternative
`H1`. Six formulations (`hypotestbaf1…6`) cover point, one-sided and interval
hypotheses with various prior choices; each returns, for every `x = 0…n`, the
factor and a **Jeffreys-scale interpretation**:

| `BaFa01` range | interpretation |
|---|---|
| ≥ 150 | Evidence against H1 is very strong |
| 20 – 150 | Evidence against H1 is strong |
| 3 – 20 | Evidence against H1 is positive |
| 1 – 3 | Evidence against H1 is not worth more than a bare mention |
| 1/3 – 1 | Evidence against H0 is not worth more than a bare mention |
| 1/20 – 1/3 | Evidence against H0 is positive |
| 1/150 – 1/20 | Evidence against H0 is strong |
| < 1/150 | Evidence against H0 is very strong |

Every function has a plain form (all `x`) and an `x` form (single `x`). The Beta
integrals reduce to the Beta CDF/SF, so no numerical integration is needed. R
source: [`R/631.BayesFactors.R`](https://github.com/RajeswaranV/proportion/blob/master/R/631.BayesFactors.R)
and [`R/632.BayesFactors_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/632.BayesFactors_x.R).

```{contents} Functions in this module
:local:
:depth: 1
```

---

## `hypotestbaf1`

```{eval-rst}
.. autofunction:: binomcikit.bayes.bayesfactors.hypotestbaf1
```

**In plain words** — Bayes factor for a **point null** `H0: p = th0` against a
`Beta(a1, b1)` **alternative**, for every `x`.

**The maths** —

$$\text{BaFa01} = \frac{B(a_1,b_1)}{B(x+a_1,\,n-x+b_1)}\,
\text{th0}^{x}\,(1-\text{th0})^{n-x}.$$

**Example**

```python
import binomcikit as bk
bk.hypotestbaf1(5, 0.5, 1, 1)     # th0 = 0.5, uniform alternative
#    x  BaFa01                                          Interpretation
# 0  0  0.1875                     Evidence against H0 is positive
# ...
```

**R source** — [`R/631.BayesFactors.R`](https://github.com/RajeswaranV/proportion/blob/master/R/631.BayesFactors.R), function `hypotestBAF1`

**What the R code does** — Computes the point-null-vs-Beta Bayes factor for each
`x`, bins `BaFa01` on the Jeffreys scale, and attaches the interpretation.

**Python source** — `binomcikit.bayes.bayesfactors.hypotestbaf1`

```python
def _baf1(x, n, th0, a1, b1):
    return (beta_fn(a1, b1) / beta_fn(x + a1, n - x + b1)
            * th0 ** x * (1 - th0) ** (n - x))
```

**What the Python code does** — Evaluates the closed-form factor with
`scipy.special.beta` and maps each value to its interpretation via `_interpret`.

**R → Py changes** — Naming lowercased; pandas `DataFrame`; `beta` →
`scipy.special.beta`. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `hypotestbaf1x`

```{eval-rst}
.. autofunction:: binomcikit.bayes.bayesfactors.hypotestbaf1x
```

**In plain words** — `hypotestbaf1` for a **single observed `x`**.

**The maths** — The BAF1 formula at one `x`.

**Example**

```python
import binomcikit as bk
bk.hypotestbaf1x(3, 5, 0.5, 1, 1)
```

**R source** — [`R/632.BayesFactors_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/632.BayesFactors_x.R), function `hypotestBAF1x`

**What the R code does** — The BAF1 factor and interpretation for one `x`.

**Python source** — `binomcikit.bayes.bayesfactors.hypotestbaf1x`.

**What the Python code does** — One-row BAF1 result.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `hypotestbaf2`

```{eval-rst}
.. autofunction:: binomcikit.bayes.bayesfactors.hypotestbaf2
```

**In plain words** — Bayes factor for a **one-sided upper** alternative
(`H1: p > th0`) with a `Beta(a1, b1)` prior.

**The maths** — With upper-tail masses `t1 = SF_{prior}(th0)`,
`t2 = SF_{post}(th0)`: `BaFa01 = (t1/t2)·th0^x·(1−th0)^{n−x}`.

**Example**

```python
import binomcikit as bk
bk.hypotestbaf2(5, 0.5, 1, 1)
```

**R source** — [`R/631.BayesFactors.R`](https://github.com/RajeswaranV/proportion/blob/master/R/631.BayesFactors.R), function `hypotestBAF2`

**What the R code does** — Integrates the prior and posterior Beta densities
over `(th0, 1)` and forms the factor.

**Python source** — `binomcikit.bayes.bayesfactors.hypotestbaf2` — uses
`scipy.stats.beta.sf` for the upper-tail masses.

**What the Python code does** — The same one-sided-upper factor, analytically.

**R → Py changes** — Naming lowercased; pandas `DataFrame`; `integrate` →
`scipy.stats.beta.sf`. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `hypotestbaf2x`

```{eval-rst}
.. autofunction:: binomcikit.bayes.bayesfactors.hypotestbaf2x
```

**In plain words** — `hypotestbaf2` for a single `x`.

**The maths** — The BAF2 formula at one `x`.

**Example**

```python
import binomcikit as bk
bk.hypotestbaf2x(3, 5, 0.5, 1, 1)
```

**R source** — [`R/632.BayesFactors_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/632.BayesFactors_x.R), function `hypotestBAF2x`

**What the R code does** — The BAF2 factor for one `x`.

**Python source** — `binomcikit.bayes.bayesfactors.hypotestbaf2x`.

**What the Python code does** — One-row BAF2 result.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `hypotestbaf3`

```{eval-rst}
.. autofunction:: binomcikit.bayes.bayesfactors.hypotestbaf3
```

**In plain words** — Bayes factor for a **one-sided lower** alternative
(`H1: p < th0`) with a `Beta(a1, b1)` prior.

**The maths** — With lower-tail masses `t1 = CDF_{prior}(th0)`,
`t2 = CDF_{post}(th0)`: `BaFa01 = (t1/t2)·th0^x·(1−th0)^{n−x}`.

**Example**

```python
import binomcikit as bk
bk.hypotestbaf3(5, 0.5, 1, 1)
```

**R source** — [`R/631.BayesFactors.R`](https://github.com/RajeswaranV/proportion/blob/master/R/631.BayesFactors.R), function `hypotestBAF3`

**What the R code does** — Integrates the prior/posterior densities over
`(0, th0)` and forms the factor.

**Python source** — `binomcikit.bayes.bayesfactors.hypotestbaf3` — uses
`scipy.stats.beta.cdf`.

**What the Python code does** — The one-sided-lower factor, analytically.

**R → Py changes** — Naming lowercased; pandas `DataFrame`; `integrate` →
`scipy.stats.beta.cdf`. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `hypotestbaf3x`

```{eval-rst}
.. autofunction:: binomcikit.bayes.bayesfactors.hypotestbaf3x
```

**In plain words** — `hypotestbaf3` for a single `x`.

**The maths** — The BAF3 formula at one `x`.

**Example**

```python
import binomcikit as bk
bk.hypotestbaf3x(3, 5, 0.5, 1, 1)
```

**R source** — [`R/632.BayesFactors_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/632.BayesFactors_x.R), function `hypotestBAF3x`

**What the R code does** — The BAF3 factor for one `x`.

**Python source** — `binomcikit.bayes.bayesfactors.hypotestbaf3x`.

**What the Python code does** — One-row BAF3 result.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `hypotestbaf4`

```{eval-rst}
.. autofunction:: binomcikit.bayes.bayesfactors.hypotestbaf4
```

**In plain words** — Bayes factor using **separate priors** for null and
alternative: null `Beta(a0, b0)` restricted below `th0`, alternative
`Beta(a1, b1)` restricted above `th0`.

**The maths** — `BaFa01 = t01·t1 / (t0·t11)`, where `t0, t01` are the null
prior/posterior lower-tail masses at `th0` and `t1, t11` the alternative
prior/posterior upper-tail masses.

**Example**

```python
import binomcikit as bk
bk.hypotestbaf4(5, 0.5, 1, 1, 1, 1)
```

**R source** — [`R/631.BayesFactors.R`](https://github.com/RajeswaranV/proportion/blob/master/R/631.BayesFactors.R), function `hypotestBAF4`

**What the R code does** — Integrates the four prior/posterior tail masses and
combines them.

**Python source** — `binomcikit.bayes.bayesfactors.hypotestbaf4` — uses
`scipy.stats.beta.cdf`/`.sf` for the four masses.

**What the Python code does** — The two-prior factor, analytically.

**R → Py changes** — Naming lowercased; pandas `DataFrame`; `integrate` →
`scipy.stats.beta`. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `hypotestbaf4x`

```{eval-rst}
.. autofunction:: binomcikit.bayes.bayesfactors.hypotestbaf4x
```

**In plain words** — `hypotestbaf4` for a single `x`.

**The maths** — The BAF4 formula at one `x`.

**Example**

```python
import binomcikit as bk
bk.hypotestbaf4x(3, 5, 0.5, 1, 1, 1, 1)
```

**R source** — [`R/632.BayesFactors_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/632.BayesFactors_x.R), function `hypotestBAF4x`

**What the R code does** — The BAF4 factor for one `x`.

**Python source** — `binomcikit.bayes.bayesfactors.hypotestbaf4x`.

**What the Python code does** — One-row BAF4 result.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `hypotestbaf5`

```{eval-rst}
.. autofunction:: binomcikit.bayes.bayesfactors.hypotestbaf5
```

**In plain words** — Like `hypotestbaf4` but with the tails swapped: null
`Beta(a0, b0)` restricted **above** `th0`, alternative `Beta(a1, b1)` restricted
**below** `th0`.

**The maths** — `BaFa01 = t01·t1 / (t0·t11)` with the upper/lower tails swapped
relative to BAF4.

**Example**

```python
import binomcikit as bk
bk.hypotestbaf5(5, 0.5, 1, 1, 1, 1)
```

**R source** — [`R/631.BayesFactors.R`](https://github.com/RajeswaranV/proportion/blob/master/R/631.BayesFactors.R), function `hypotestBAF5`

**What the R code does** — Integrates the four tail masses (upper null / lower
alternative) and combines them.

**Python source** — `binomcikit.bayes.bayesfactors.hypotestbaf5` — `scipy.stats.beta`
tails.

**What the Python code does** — The swapped-tail two-prior factor.

**R → Py changes** — Naming lowercased; pandas `DataFrame`; `integrate` →
`scipy.stats.beta`. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `hypotestbaf5x`

```{eval-rst}
.. autofunction:: binomcikit.bayes.bayesfactors.hypotestbaf5x
```

**In plain words** — `hypotestbaf5` for a single `x`.

**The maths** — The BAF5 formula at one `x`.

**Example**

```python
import binomcikit as bk
bk.hypotestbaf5x(3, 5, 0.5, 1, 1, 1, 1)
```

**R source** — [`R/632.BayesFactors_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/632.BayesFactors_x.R), function `hypotestBAF5x`

**What the R code does** — The BAF5 factor for one `x`.

**Python source** — `binomcikit.bayes.bayesfactors.hypotestbaf5x`.

**What the Python code does** — One-row BAF5 result.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `hypotestbaf6`

```{eval-rst}
.. autofunction:: binomcikit.bayes.bayesfactors.hypotestbaf6
```

**In plain words** — Bayes factor for **two interval hypotheses**: `H1: p < th1`
under a `Beta(a1, b1)` posterior versus `H2: p > th2` under a `Beta(a2, b2)`
posterior.

**The maths** — `BaFa01 = t1/t2`, where `t1 = CDF_{post1}(th1)` and
`t2 = SF_{post2}(th2)`.

**Example**

```python
import binomcikit as bk
bk.hypotestbaf6(5, 0.4, 1, 1, 0.6, 1, 1)     # th1=0.4, th2=0.6
```

**R source** — [`R/631.BayesFactors.R`](https://github.com/RajeswaranV/proportion/blob/master/R/631.BayesFactors.R), function `hypotestBAF6`

**What the R code does** — Integrates one posterior over `(0, th1)` and another
over `(th2, 1)` and forms the ratio.

**Python source** — `binomcikit.bayes.bayesfactors.hypotestbaf6` — uses
`scipy.stats.beta.cdf`/`.sf`.

**What the Python code does** — The interval-vs-interval factor, analytically.

**R → Py changes** — Naming lowercased; pandas `DataFrame`; `integrate` →
`scipy.stats.beta`. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `hypotestbaf6x`

```{eval-rst}
.. autofunction:: binomcikit.bayes.bayesfactors.hypotestbaf6x
```

**In plain words** — `hypotestbaf6` for a single `x`.

**The maths** — The BAF6 formula at one `x`.

**Example**

```python
import binomcikit as bk
bk.hypotestbaf6x(3, 5, 0.4, 1, 1, 0.6, 1, 1)
```

**R source** — [`R/632.BayesFactors_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/632.BayesFactors_x.R), function `hypotestBAF6x`

**What the R code does** — The BAF6 factor for one `x`.

**Python source** — `binomcikit.bayes.bayesfactors.hypotestbaf6x`.

**What the Python code does** — One-row BAF6 result.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`
