<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `expl.general`

```{eval-rst}
.. module:: binomcikit.expl.general
```

This module computes **expected interval length** — the average width of each interval over hypothetical *p* drawn from a `Beta(a, b)` prior, for **user-supplied** interval limits (given or simulated *p*). These functions reuse the confidence-interval limits from the 1xx `ci` family and feed them through a shared engine, so only the supplied limits differ between methods. See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `lengthgen`

```{eval-rst}
.. autofunction:: binomcikit.expl.general.lengthgen
```

**In plain words** — the **expected length** of user-supplied interval limits — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
wd = bk.ciwd(20, 0.05)
bk.lengthgen(20, wd["LWD"].values, wd["UWD"].values, [0.2, 0.5, 0.8])
```

**R source** — [`R/328.Sum_Leng_GENERAL_SIM.R` (line 24)](https://github.com/RajeswaranV/proportion/blob/master/R/328.Sum_Leng_GENERAL_SIM.R#L24), function `lengthGEN`

```r
lengthGEN<-function(n,LL,UL,hp)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(LL)) stop("'Lower limit' is missing")
  if (missing(UL)) stop("'Upper Limit' is missing")
  if (missing(hp)) stop("'hp' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if ((class(LL) != "integer") & (class(LL) != "numeric") || any(LL < 0)) stop("'LL' has to be a set of positive numeric vectors")
  if ((class(UL) != "integer") & (class(UL) != "numeric") || any(UL < 0)) stop("'UL' has to be a set of positive numeric vectors")
  if (length(LL) <= n ) stop("Length of vector LL has to be greater than n")
  if (length(UL) <= n ) stop("Length of vector UL has to be greater than n")
  if (any(LL[0:n+1] > UL[0:n+1] )) stop("LL value have to be lower than the corrosponding UL value")
  if (any(hp>1) || any(hp<0)) stop("'hp' has to be between 0 and 1")

  ####INPUT n
  x=0:n
  k=n+1
  s=length(hp)
  ewi=matrix(0,k,s)						#Expected length quantity in sum
  ew=0									#Expected Length
  LE=0

  for(i in 1:k)
  {
    LE[i]=UL[i]-LL[i]
  }
  ####Expected Length

  for (j in 1:s)
  {
    for(i in 1:k)
    {
      ewi[i,j]=LE[i]*stats::dbinom(i-1, n,hp[j])
    }
    ew[j]=sum(ewi[,j])						#Expected Length
  }

  sumLen=sum(LE)
  explMean=mean(ew)
  explSD=stats::sd(ew)
  explMax=max(ew)
  explLL=explMean-(explSD)
  explUL=explMean+(explSD)
  df.Summary=data.frame(sumLen,explMean,explSD,explMax,explLL,explUL)
  return(df.Summary)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.general.lengthgen`

```python
def lengthgen(n, LL, UL, hp):
    """Expected length for given limits over a given hp vector (R lengthGEN)."""
    _check_limits(n, LL, UL)
    if hp is None:
        raise ValueError("'hp' is missing")
    hp = np.atleast_1d(np.asarray(hp, dtype=float))
    if np.any((hp < 0) | (hp > 1)):
        raise ValueError("'hp' has to be between 0 and 1")
    lengths = np.asarray(UL, dtype=float) - np.asarray(LL, dtype=float)
    ew = _expl_series(n, lengths, hp)
    return _expl_summary(lengths, ew)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthsim`

```{eval-rst}
.. autofunction:: binomcikit.expl.general.lengthsim
```

**In plain words** — the **expected length** of user-supplied limits over simulated p — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
wd = bk.ciwd(20, 0.05)
bk.lengthsim(20, wd["LWD"].values, wd["UWD"].values, 1000, 1, 1, seed=0)
```

**R source** — [`R/328.Sum_Leng_GENERAL_SIM.R` (line 141)](https://github.com/RajeswaranV/proportion/blob/master/R/328.Sum_Leng_GENERAL_SIM.R#L141), function `lengthSIM`

```r
lengthSIM<-function(n,LL,UL,s,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(LL)) stop("'Lower limit' is missing")
  if (missing(UL)) stop("'Upper Limit' is missing")
  if (missing(s)) stop("'s' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if ((class(LL) != "integer") & (class(LL) != "numeric") || any(LL < 0)) stop("'LL' has to be a set of positive numeric vectors")
  if ((class(UL) != "integer") & (class(UL) != "numeric") || any(UL < 0)) stop("'UL' has to be a set of positive numeric vectors")
  if (length(LL) <= n ) stop("Length of vector LL has to be greater than n")
  if (length(UL) <= n ) stop("Length of vector UL has to be greater than n")
  if (any(LL[0:n+1] > UL[0:n+1] )) stop("LL value have to be lower than the corrosponding UL value")
  if ((class(s) != "integer") & (class(s) != "numeric") || length(s)>1 || s<1  ) stop("'b' has to be greater than or equal to 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

  ####INPUT n
  k=n+1
  LE=0
  ewi=matrix(0,k,s)						#sum of length quantity in sum
  ew=0

  for(i in 1:k)
  {
    LE[i]=UL[i]-LL[i]
  }
  hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
  for (j in 1:s)
  {
    for(i in 1:k)
    {
      ewi[i,j]=LE[i]*stats::dbinom(i-1, n,hp[j])
    }
    ew[j]=sum(ewi[,j])						#Expected Length
  }
  sumLen=sum(LE)
  explMean=mean(ew)
  explSD=stats::sd(ew)
  explMax=max(ew)
  explLL=explMean-(explSD)
  explUL=explMean+(explSD)
  df.Summary=data.frame(sumLen,explMean,explSD,explMax,explLL,explUL)
  return(df.Summary)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.general.lengthsim`

```python
def lengthsim(n, LL, UL, s, a, b, seed=None):
    """Expected length for given limits over s Beta(a, b) draws (R lengthSIM)."""
    _check_limits(n, LL, UL)
    if s is None:
        raise ValueError("'s' is missing")
    if not isinstance(s, (int, float)) or s <= 0:
        raise ValueError("'s' has to be greater than 0")
    if not isinstance(a, (int, float)) or a < 0:
        raise ValueError("'a' has to be greater than or equal to 0")
    if not isinstance(b, (int, float)) or b < 0:
        raise ValueError("'b' has to be greater than or equal to 0")
    hp = np.sort(np.random.default_rng(seed).beta(a, b, int(s)))
    lengths = np.asarray(UL, dtype=float) - np.asarray(LL, dtype=float)
    ew = _expl_series(n, lengths, hp)
    return _expl_summary(lengths, ew)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

