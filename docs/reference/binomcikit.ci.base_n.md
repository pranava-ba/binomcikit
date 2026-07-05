# `ci.base_n`

```{eval-rst}
.. module:: binomcikit.ci.base_n
```

The **base confidence-interval methods** for a single binomial proportion,
computed for *every* possible number of successes `x = 0, 1, …, n` at a given
sample size `n` and error level `alp` (= α). Each function returns a pandas
`DataFrame` with one row per `x`, the lower/upper limits, and three diagnostic
flags:

| flag | meaning |
|---|---|
| `LABB` | `"YES"` if the raw lower limit fell below 0 and was clamped to 0 |
| `UABB` | `"YES"` if the raw upper limit exceeded 1 and was clamped to 1 |
| `ZWI`  | `"YES"` for a **z**ero-**w**idth **i**nterval (lower = upper) |

All six methods estimate the same quantity — the true proportion *p* — but
differ in how they build the interval, and therefore in their coverage and
width. `ciall` runs all six at once; `ciex` is the exact method.

```{contents} Functions in this module
:local:
:depth: 1
```

---

## `ciwd`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n.ciwd
```

**In plain words** — The **Wald** interval, the textbook "estimate ± margin of
error." It centres the interval on the observed proportion `p̂ = x/n` and adds a
symmetric margin from the normal approximation. Simple and familiar, but it
behaves badly near `p = 0` or `p = 1` and for small `n` (it can even produce a
zero-width interval at `x = 0` or `x = n`).

**The maths** — With `q̂ = 1 − p̂`, standard error `SE = √(p̂q̂/n)`, and normal
critical value `z = Φ⁻¹(1 − α/2)`:

$$\hat{p} \pm z_{\alpha/2}\,\sqrt{\frac{\hat{p}\,\hat{q}}{n}}$$

Limits below 0 are clamped to 0 (`LABB`), above 1 to 1 (`UABB`).

**Example**

```python
import binomcikit as bk
bk.ciwd(5, 0.05)
#    x       LWD       UWD LABB UABB  ZWI
# 0  0  0.000000  0.000000   NO   NO  YES   <- zero-width at x=0
# 1  1  0.000000  0.550609  YES   NO   NO   <- lower clamped to 0
# ...
# 5  5  1.000000  1.000000   NO   NO  YES
```

**R source** — [`R/101.Confidence_base_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/101.Confidence_base_n.R#L6), function `ciWD`

```r
ciWD<-function(n,alp)
{
  x=0:n ; k=n+1
  cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
  for(i in 1:k)
  {
    pW[i]=x[i]/n
    qW[i]=1-(x[i]/n)
    seW[i]=sqrt(pW[i]*qW[i]/n)
    LWD[i]=pW[i]-(cv*seW[i])
    UWD[i]=pW[i]+(cv*seW[i])
    LABB[i]=if(LWD[i]<0) "YES" else "NO" ; LWD[i]=max(0,LWD[i])
    UABB[i]=if(UWD[i]>1) "YES" else "NO" ; UWD[i]=min(1,UWD[i])
    ZWI[i] =if(UWD[i]-LWD[i]==0) "YES" else "NO"
  }
  data.frame(x,LWD,UWD,LABB,UABB,ZWI)
}
```

**What the R code does** — Loops over every `x` from 0 to `n`, computes `p̂`,
the standard error and the two Wald limits, clamps them into `[0, 1]` while
recording the aberration flags, and returns a `data.frame`.

**Python source** — `binomcikit.ci.base_n.ciwd`

```python
def ciwd(n, alp):
    cv = stats.norm.ppf(1 - (alp / 2))
    for i in range(k):
        pW[i] = x[i] / n
        qW[i] = 1 - (x[i] / n)
        seW[i] = np.sqrt(pW[i] * qW[i] / n)
        LWD[i] = pW[i] - (cv * seW[i])
        UWD[i] = pW[i] + (cv * seW[i])
        LABB[i] = "YES" if LWD[i] < 0 else "NO"; LWD[i] = max(0, LWD[i])
        UABB[i] = "YES" if UWD[i] > 1 else "NO"; UWD[i] = min(1, UWD[i])
        ZWI[i] = "YES" if UWD[i] - LWD[i] == 0 else "NO"
    return pd.DataFrame({'x': x, 'LWD': LWD, 'UWD': UWD,
                         'LABB': LABB, 'UABB': UABB, 'ZWI': ZWI})
```

**What the Python code does** — Line-for-line the same computation, using
`scipy.stats.norm.ppf` for the normal quantile and NumPy arrays for the
per-`x` vectors, returning a pandas `DataFrame`.

**R → Py changes** — Naming lowercased (`ciWD` → `ciwd`); returns a pandas
`DataFrame`; `stats::qnorm` → `scipy.stats.norm.ppf`. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `cisc`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n.cisc
```

**In plain words** — The **Score** (Wilson) interval. Instead of centring on
`p̂`, it inverts the score test, which shifts the interval toward ½ and keeps it
inside `[0, 1]` automatically. Much better coverage than Wald for small `n` and
extreme `p̂`, and the recommended default in most references.

**The maths** — With `z = Φ⁻¹(1 − α/2)`:

$$\frac{n}{n+z^2}\left[\left(\hat{p}+\frac{z^2}{2n}\right) \pm
z\sqrt{\frac{\hat{p}\hat{q}}{n}+\frac{z^2}{4n^2}}\right]$$

**Example**

```python
import binomcikit as bk
bk.cisc(10, 0.05).iloc[3]     # x = 3 of 10
#   x=3  LSC≈0.1078  USC≈0.6032   (contained in [0,1] without clamping)
```

**R source** — [`R/101.Confidence_base_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/101.Confidence_base_n.R#L58), function `ciSC`

```r
ciSC<-function(n,alp)
{
  cv  = stats::qnorm(1-(alp/2), mean = 0, sd = 1)
  cv1 = (cv^2)/(2*n)
  cv2 = (cv/(2*n))^2
  for(i in 1:k){
    pS[i]=x[i]/n ; qS[i]=1-pS[i]
    seS[i]=sqrt((pS[i]*qS[i]/n)+cv2)
    LSC[i]=(n/(n+cv^2))*((pS[i]+cv1)-(cv*seS[i]))
    USC[i]=(n/(n+cv^2))*((pS[i]+cv1)+(cv*seS[i]))
    # ... clamp + flags ...
  }
  data.frame(x,LSC,USC,LABB,UABB,ZWI)
}
```

**What the R code does** — Precomputes the two Wilson correction terms
(`cv1`, `cv2`), then for each `x` forms the shifted centre and the widened
standard error and applies the `n/(n+z²)` shrinkage factor.

**Python source** — `binomcikit.ci.base_n.cisc`

```python
def cisc(n, alp):
    cv = stats.norm.ppf(1 - (alp / 2))
    cv1 = (cv ** 2) / (2 * n)
    cv2 = (cv / (2 * n)) ** 2
    for i in range(k):
        pS[i] = x[i] / n; qS[i] = 1 - pS[i]
        seS[i] = np.sqrt((pS[i] * qS[i] / n) + cv2)
        LSC[i] = (n / (n + cv ** 2)) * ((pS[i] + cv1) - (cv * seS[i]))
        USC[i] = (n / (n + cv ** 2)) * ((pS[i] + cv1) + (cv * seS[i]))
        # ... clamp + flags ...
    return pd.DataFrame({'x': x, 'LSC': LSC, 'USC': USC, ...})
```

**What the Python code does** — The identical Wilson formula; validated
against `statsmodels.stats.proportion.proportion_confint(method="wilson")` to
1e-9 in the test suite.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical (independently cross-checked against statsmodels).

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `cias`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n.cias
```

**In plain words** — The **ArcSine** interval. It applies the
variance-stabilising transform `arcsin(√p̂)`, builds a symmetric interval on that
scale, and transforms back. Stabilises the variance at the extremes.

**The maths** — Interval on the transformed scale, back-transformed:

$$\sin^2\!\left(\arcsin\sqrt{\hat{p}} \pm \frac{z_{\alpha/2}}{2\sqrt{n}}\right)$$

**Example**

```python
import binomcikit as bk
bk.cias(20, 0.05)     # arcsine limits for every x = 0..20
```

**R source** — [`R/101.Confidence_base_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/101.Confidence_base_n.R#L236), function `ciAS`

```r
ciAS<-function(n,alp)
{
  cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
  for(i in 1:k){
    pA[i]=x[i]/n ; qA[i]=1-pA[i]
    seA[i]=cv/sqrt(4*n)
    LAS[i]=(sin(asin(sqrt(pA[i]))-seA[i]))^2
    UAS[i]=(sin(asin(sqrt(pA[i]))+seA[i]))^2
    # ... clamp + flags ...
  }
  return(data.frame(x,LAS,UAS,LABB,UABB,ZWI))
}
```

**What the R code does** — For each `x`, transforms `p̂` with `arcsin(√·)`, adds
`±z/√(4n)`, then squares the sine of the result to return to the probability
scale, clamping and flagging as usual.

**Python source** — `binomcikit.ci.base_n.cias`

```python
def cias(n, alp):
    cv = stats.norm.ppf(1 - (alp / 2))
    for i in range(k):
        pA[i] = x[i] / n
        seA[i] = cv / np.sqrt(4 * n)
        LAS[i] = (np.sin(np.arcsin(np.sqrt(pA[i])) - seA[i])) ** 2
        UAS[i] = (np.sin(np.arcsin(np.sqrt(pA[i])) + seA[i])) ** 2
        # ... clamp + flags ...
    return pd.DataFrame({'x': x, 'LAS': LAS, 'UAS': UAS, ...})
```

**What the Python code does** — The same transform-and-back computation with
`numpy.arcsin`/`numpy.sin`.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `citw`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n.citw
```

**In plain words** — The **Wald-T** interval: a Wald interval that swaps the
normal critical value for a Student-*t* value and uses a slightly modified
standard error, which widens the interval a little for small `n`.

**The maths** — Uses a *t* quantile with the method's degrees of freedom and an
adjusted standard error `SE*`:

$$\hat{p} \pm t_{\alpha/2}\,\mathrm{SE}^{*}$$

**Example**

```python
import binomcikit as bk
bk.citw(15, 0.05)
```

**R source** — [`R/101.Confidence_base_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/101.Confidence_base_n.R), function `ciTW` *(see linked source for the full body)*

**What the R code does** — Computes an adjusted point estimate and standard
error, derives the effective degrees of freedom, and forms the interval with
`stats::qt`.

**Python source** — `binomcikit.ci.base_n.citw` — mirrors the R computation
using `scipy.stats.t.ppf` for the *t* quantile.

**What the Python code does** — Same formula, `scipy.stats.t` instead of
`stats::qt`.

**R → Py changes** — Naming lowercased; pandas `DataFrame`; `stats::qt` →
`scipy.stats.t.ppf`. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `cilt`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n.cilt
```

**In plain words** — The **Logit-Wald** interval. It builds a Wald interval on
the log-odds (logit) scale, then transforms back to a probability. Because the
logit scale is unbounded, the back-transformed interval always lies strictly
inside `(0, 1)` — helpful for extreme `p̂`.

**The maths** — With logit `L = ln(p̂/q̂)` and its standard error
`SE_L = 1/√(n p̂ q̂)`:

$$\operatorname{logit}^{-1}\!\left(\ln\frac{\hat{p}}{\hat{q}} \pm
z_{\alpha/2}\,\frac{1}{\sqrt{n\,\hat{p}\,\hat{q}}}\right)$$

**Example**

```python
import binomcikit as bk
bk.cilt(20, 0.05)
```

**R source** — [`R/101.Confidence_base_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/101.Confidence_base_n.R), function `ciLT` *(see linked source)*

**What the R code does** — Transforms `p̂` to the logit scale, forms the Wald
interval there, and applies the inverse-logit to both limits.

**Python source** — `binomcikit.ci.base_n.cilt` — same logit/inverse-logit
computation in NumPy.

**What the Python code does** — Identical transform-based interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `cilr`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n.cilr
```

**In plain words** — The **Likelihood-Ratio** interval. It keeps all values of
`p` that are *not rejected* by the likelihood-ratio test — i.e. where twice the
drop in log-likelihood from the maximum stays below the χ²(1) critical value.
There is no closed form, so the two endpoints are found numerically.

**The maths** — The interval is `{ p : 2[ℓ(p̂) − ℓ(p)] ≤ z²_{α/2} }`, where
`ℓ(p) = x·ln p + (n−x)·ln(1−p)`; the boundary is solved for `p` on each side of
`p̂`.

**Example**

```python
import binomcikit as bk
bk.cilr(5, 0.05)     # each row: numerically-solved LR limits
```

**R source** — [`R/101.Confidence_base_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/101.Confidence_base_n.R), function `ciLR` *(see linked source)*

**What the R code does** — For each `x`, maximises the binomial log-likelihood
and then numerically searches below and above the MLE for the two `p` where the
log-likelihood drops by the χ² cutoff.

**Python source** — `binomcikit.ci.base_n.cilr`

```python
def cilr(n, alp):
    for i in range(k):
        # profile the binomial log-likelihood around the MLE
        LLR_res = optimize.minimize_scalar(loglik_optim,
                                           bounds=(0, mle_i), method='bounded')
        ULR_res = optimize.minimize_scalar(loglik_optim,
                                           bounds=(mle_i, 1), method='bounded')
        ...
    return pd.DataFrame({'x': x, 'LLR': LLR, 'ULR': ULR, ...})
```

**What the Python code does** — Uses `scipy.optimize.minimize_scalar` to locate
each endpoint. **Returns `x` as an ordinary column** (see changes).

**R → Py changes** — Naming lowercased; pandas `DataFrame`; numerical solve via
`scipy.optimize.minimize_scalar`. **Fix:** the earlier Python port returned `x`
as a hidden `MultiIndex` (unlike every other method); this port returns `x` as a
plain column so `cilr` composes correctly with the other functions.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ciex`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n.ciex
```

**In plain words** — The **Exact** interval, based on inverting the binomial
tail probabilities rather than a normal approximation. A parameter `e ∈ [0, 1]`
tunes the tail treatment: `e = 1` gives the classic **Clopper–Pearson**
interval, `e = 0.5` gives the **mid-*p*** interval. Guaranteed coverage, at the
cost of being conservative (wider).

**The maths** — The endpoints solve, per `x`, tail equations of the form
`e·P(X = x) + P(X > x) = α/2` (upper) and the mirror for the lower limit; these
are Beta-quantile / root-finding problems.

**Example**

```python
import binomcikit as bk
bk.ciex(10, 0.05, [1])      # Clopper-Pearson (e = 1)
bk.ciex(10, 0.05, [0.5])    # mid-p         (e = 0.5)
```

Note `e` is passed as a **list**, so several `e` values can be evaluated at
once.

**R source** — [`R/101.Confidence_base_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/101.Confidence_base_n.R), function `ciEX` (helpers `lufn101`, `exlim102l`, `exlim102u`)

**What the R code does** — For each `x` and each `e`, solves the two tail
equations for the interval endpoints (special-casing `x = 0` and `x = n`).

**Python source** — `binomcikit.ci.base_n.ciex` (with `lufn101`, `exlim102l`,
`exlim102u`) — same equations solved with SciPy.

**What the Python code does** — Evaluates the Clopper–Pearson/mid-*p* endpoints;
validated against
`statsmodels.stats.proportion.proportion_confint(method="beta")` at `e = 1`.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. `e` accepted as a
list/array. Numerically identical (cross-checked against statsmodels for
Clopper–Pearson).

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ciall`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n.ciall
```

**In plain words** — A convenience wrapper that runs **all six base methods**
(Wald, ArcSine, Likelihood, Score, Wald-T, Logit-Wald) and stacks the results
into one long-format `DataFrame` with a `method` column — ideal for comparing
methods side by side or plotting them together.

**The maths** — None of its own; it just calls the six methods above and
concatenates them.

**Example**

```python
import binomcikit as bk
df = bk.ciall(5, 0.05)
set(df["method"])
# {'Wald','ArcSine','Likelihood','Score','Wald-T','Logit-Wald'}
len(df)   # 6 methods x (n+1) rows = 36
```

**R source** — [`R/101.Confidence_base_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/101.Confidence_base_n.R#L896), function `ciAll`

**What the R code does** — Calls `ciWD`, `ciAS`, `ciLR`, `ciSC`, `ciTW`, `ciLT`,
tags each with a `method` factor, harmonises their column names to
`LowerLimit`/`UpperLimit`, and `rbind`s them.

**Python source** — `binomcikit.ci.base_n.ciall` — the same, using a small
`create_generic_df` helper and `pandas.concat`.

**What the Python code does** — Produces the identical long-format table with
columns `method, x, LowerLimit, UpperLimit, LowerAbb, UpperAbb, ZWI`.

**R → Py changes** — Naming lowercased; `rbind` → `pandas.concat`; returns a
pandas `DataFrame`. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## Internal helpers

These are not part of the public API; they implement the exact-method
root-finding used by `ciex` and mirror the R helpers of the same name. They are
documented here only so the mapping table's links resolve.

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n.lufn101
.. autofunction:: binomcikit.ci.base_n.exlim102l
.. autofunction:: binomcikit.ci.base_n.exlim102u
```

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`
