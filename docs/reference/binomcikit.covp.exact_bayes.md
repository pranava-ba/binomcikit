<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `covp.exact_bayes`

```{eval-rst}
.. module:: binomcikit.covp.exact_bayes
```

This module computes **coverage probability** — how often each interval actually contains the true proportion, evaluated over hypothetical *p* drawn from a `Beta(a, b)` prior and summarised (mean/min coverage, RMSE, tolerance), for the **Exact** and **Bayesian** intervals. These functions reuse the confidence-interval limits from the 1xx `ci` family and feed them through a shared engine, so only the supplied limits differ between methods. See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `covpba`

```{eval-rst}
.. autofunction:: binomcikit.covp.exact_bayes.covpba
```

**In plain words** — the **coverage probability** of the Bayesian credible interval — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covpba(20, 0.05, 1, 1, 0.9, 0.97, 1, 1, seed=0)
```

**R source** — [`R/201.CoverageProb_BASE_All.R` (line 1048)](https://github.com/RajeswaranV/proportion/blob/master/R/201.CoverageProb_BASE_All.R#L1048), function `covpBA`

```r
covpBA<-function(n,alp,a,b,t1,t2,a1,a2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if (missing(a1)) stop("'a1' is missing")
  if (missing(a2)) stop("'a2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")
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
cpBAQ=matrix(0,k,s)
ctBAQ=matrix(0,k,s)							#Cover Pbty quantity in sum
cppBAQ=0								#Coverage probabilty
RMSE_N1=0
RMSE_M1=0
RMSE_Mi1=0
ctr=0

cpBAH=matrix(0,k,s)
ctBAH=matrix(0,k,s)							#Cover Pbty quantity in sum
cppBAH=0								#Coverage probabilty
RMSE_N1H=0
RMSE_M1H=0
RMSE_Mi1H=0
ctrH=0

##############
#library(TeachingDemos)				#To get HPDs
for(i in 1:k)
{
#Quantile Based Intervals
LBAQ[i]=stats::qbeta(alp/2,x[i]+a1,n-x[i]+a2)
UBAQ[i]=stats::qbeta(1-(alp/2),x[i]+a1,n-x[i]+a2)

LBAH[i]=TeachingDemos::hpd(stats::qbeta,shape1=x[i]+a1,shape2=n-x[i]+a2,conf=1-alp)[1]
UBAH[i]=TeachingDemos::hpd(stats::qbeta,shape1=x[i]+a1,shape2=n-x[i]+a2,conf=1-alp)[2]

}
####COVERAGE PROBABILITIES
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
if(hp[j] > LBAQ[i] && hp[j] < UBAQ[i])
{
cpBAQ[i,j]=stats::dbinom(i-1, n,hp[j])
ctBAQ[i,j]=1
}
if(hp[j] > LBAH[i] && hp[j] < UBAH[i])
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.exact_bayes.covpba`

```python
def covpba(n, alp, a, b, t1, t2, a1, a2, seed=None):
    """Coverage probability of the Bayesian credible interval (R covpBA).

    ``a1, a2`` set the credible-interval prior; ``a, b`` the simulation prior.
    Returns coverage for both the quantile-based and HPD credible intervals.
    """
    _validate(n, alp, a, b, t1, t2)
    if not isinstance(a1, (int, float)) or a1 < 0:
        raise ValueError("'a1' has to be greater than or equal to 0")
    if not isinstance(a2, (int, float)) or a2 < 0:
        raise ValueError("'a2' has to be greater than or equal to 0")
    ba = ciba(n, alp, a1, a2)
    rows = []
    for label, lo, hi in [("Quantile", 'LBAQ', 'UBAQ'), ("HPD", 'LBAH', 'UBAH')]:
        row = _coverage(n, alp, a, b, t1, t2, ba[lo], ba[hi], seed).iloc[0].to_dict()
        row['method'] = label
        rows.append(row)
    out = pd.DataFrame(rows)
    return out[['method', 'mcp', 'micp', 'RMSE_N', 'RMSE_M', 'RMSE_MI', 'tol']]

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; uses SciPy HPD (`_hpd.hpd_beta`); lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `covpex`

```{eval-rst}
.. autofunction:: binomcikit.covp.exact_bayes.covpex
```

**In plain words** — the **coverage probability** of the Exact (Clopper-Pearson / mid-p) interval — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covpex(20, 0.05, 0.5, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/201.CoverageProb_BASE_All.R` (line 882)](https://github.com/RajeswaranV/proportion/blob/master/R/201.CoverageProb_BASE_All.R#L882), function `covpEX`

```r
covpEX=function(n,alp,e,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(e)) stop("'e' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(e) != "integer") & (class(e) != "numeric") || any(e>1) || any(e<0)) stop("'e' has to be between 0 and 1")
  if (length(e)>10) stop("'e' can have only 10 intervals")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

  nvar=length(e)

  res <- data.frame()

  for(i in 1:nvar)
  {
    lu=oldEX201(n,alp,e[i],a,b,t1,t2)
    res <- rbind(res,lu)
  }
  return(res)
}
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.exact_bayes.covpex`

```python
def covpex(n, alp, e, a, b, t1, t2, seed=None):
    """Coverage probability of the Exact interval (R covpEX)."""
    _validate(n, alp, a, b, t1, t2)
    if e is None:
        raise ValueError("'e' is missing")
    df = ciex(n, alp, [e])
    return _coverage(n, alp, a, b, t1, t2, df['LEX'], df['UEX'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

