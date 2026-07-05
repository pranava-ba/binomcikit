<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `expl.bayes`

```{eval-rst}
.. module:: binomcikit.expl.bayes
```

This module computes **expected interval length** — the average width of each interval over hypothetical *p* drawn from a `Beta(a, b)` prior, for the **Bayesian** credible interval. These functions reuse the confidence-interval limits from the 1xx `ci` family and feed them through a shared engine, so only the supplied limits differ between methods. See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `lengthba`

```{eval-rst}
.. autofunction:: binomcikit.expl.bayes.lengthba
```

**In plain words** — the **expected length** of the Bayesian credible interval — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthba(20, 0.05, 1, 1, 1, 1, seed=0)
```

**R source** — [`R/301.Expec_Leng_BASE_All.R` (line 883)](https://github.com/RajeswaranV/proportion/blob/master/R/301.Expec_Leng_BASE_All.R#L883), function `lengthBA`

```r
lengthBA<-function(n,alp,a,b,a1,a2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(a1)) stop("'a1' is missing")
  if (missing(a2)) stop("'a2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if ((class(a1) != "integer") & (class(a1) != "numeric") || length(a1)>1 || a1<0  ) stop("'a1' has to be greater than or equal to 0")
  if ((class(a2) != "integer") & (class(a2) != "numeric") || length(a2)>1 || a2<0  ) stop("'a2' has to be greater than or equal to 0")


####INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
LBAQ=0
UBAQ=0
LBAH=0
UBAH=0
s=5000
LEBAQ=0 								#LENGTH OF INTERVAL
LEBAH=0
ewiBAQ=matrix(0,k,s)						#sum of length quantity in sum
ewBAQ=0
ewiBAH=matrix(0,k,s)						#sum of length quantity in sum
ewBAH=0									#sum of length

#library(TeachingDemos)				#To get HPDs
for(i in 1:k)
{
#Quantile Based Intervals
LBAQ[i]=stats::qbeta(alp/2,x[i]+a1,n-x[i]+a2)
UBAQ[i]=stats::qbeta(1-(alp/2),x[i]+a1,n-x[i]+a2)

LBAH[i]=TeachingDemos::hpd(stats::qbeta,shape1=x[i]+a1,shape2=n-x[i]+a2,conf=1-alp)[1]
UBAH[i]=TeachingDemos::hpd(stats::qbeta,shape1=x[i]+a1,shape2=n-x[i]+a2,conf=1-alp)[2]

LEBAQ[i]=UBAQ[i]-LBAQ[i]
LEBAH[i]=UBAH[i]-LBAH[i]
}
# sumLEBAQ=sum(LEBAQ)
# sumLEBAH=sum(LEBAH)
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
  for(i in 1:k)
  {
    ewiBAQ[i,j]=LEBAQ[i]*stats::dbinom(i-1, n,hp[j])
    ewiBAH[i,j]=LEBAH[i]*stats::dbinom(i-1, n,hp[j])

  }
  ewBAQ[j]=sum(ewiBAQ[,j])
  ewBAH[j]=sum(ewiBAH[,j])						#Expected Length
}
sumLenBAQ=sum(LEBAQ)
explMeanBAQ=mean(ewBAQ)
explSDBAQ=stats::sd(ewBAQ)
explMaxBAQ=max(ewBAQ)
explLLBAQ=explMeanBAQ-(explSDBAQ)
explULBAQ=explMeanBAQ+(explSDBAQ)
df.SummaryBAQ=data.frame(sumLen=sumLenBAQ,explMean=explMeanBAQ,
                          explSD=explSDBAQ,explMax=explMaxBAQ,
                          explLL=explLLBAQ,explUL=explULBAQ,method="Quantile")

sumLenBAH=sum(LEBAH)
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.bayes.lengthba`

```python
def lengthba(n, alp, a, b, a1, a2, seed=None):
    """Expected length of the Bayesian credible interval (R lengthBA)."""
    _validate(n, alp, a, b)
    if not isinstance(a1, (int, float)) or a1 < 0:
        raise ValueError("'a1' has to be greater than or equal to 0")
    if not isinstance(a2, (int, float)) or a2 < 0:
        raise ValueError("'a2' has to be greater than or equal to 0")

    ba = ciba(n, alp, a1, a2)
    hp = _beta_hp(a, b, seed)
    rows = []
    for label, lo, hi in [("Quantile", 'LBAQ', 'UBAQ'), ("HPD", 'LBAH', 'UBAH')]:
        lengths = ba[hi].to_numpy() - ba[lo].to_numpy()
        ew = _expl_series(n, lengths, hp)
        row = _expl_summary(lengths, ew).iloc[0].to_dict()
        row['method'] = label
        rows.append(row)
    out = pd.DataFrame(rows)
    return out[['method', 'sumLen', 'explMean', 'explSD', 'explMax',
                'explLL', 'explUL']]

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; uses SciPy HPD (`_hpd.hpd_beta`); lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

