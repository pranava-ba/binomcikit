<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `covp.general`

```{eval-rst}
.. module:: binomcikit.covp.general
```

This module computes **coverage probability** — how often each interval actually contains the true proportion, evaluated over hypothetical *p* drawn from a `Beta(a, b)` prior and summarised (mean/min coverage, RMSE, tolerance), for **user-supplied** interval limits (given or simulated *p*). These functions reuse the confidence-interval limits from the 1xx `ci` family and feed them through a shared engine, so only the supplied limits differ between methods. See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `covpgen`

```{eval-rst}
.. autofunction:: binomcikit.covp.general.covpgen
```

**In plain words** — the **coverage probability** of user-supplied interval limits — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
wd = bk.ciwd(20, 0.05)
bk.covpgen(20, wd["LWD"].values, wd["UWD"].values, 0.05, [0.2, 0.5, 0.8], 0.9, 0.97)
```

**R source** — [`R/224.CoverageProb_GENERAL_GIVEN_p.R` (line 32)](https://github.com/RajeswaranV/proportion/blob/master/R/224.CoverageProb_GENERAL_GIVEN_p.R#L32), function `covpGEN`

```r
covpGEN<-function(n,LL,UL,alp,hp,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(LL)) stop("'Lower limit' is missing")
  if (missing(UL)) stop("'Upper Limit' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(hp)) stop("'hp' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if ((class(LL) != "integer") & (class(LL) != "numeric") || any(LL < 0)) stop("'LL' has to be a set of positive numeric vectors")
  if ((class(UL) != "integer") & (class(UL) != "numeric") || any(UL < 0)) stop("'UL' has to be a set of positive numeric vectors")
  if (length(LL) <= n ) stop("Length of vector LL has to be greater than n")
  if (length(UL) <= n ) stop("Length of vector UL has to be greater than n")
  if (any(LL[0:n+1] > UL[0:n+1] )) stop("LL value have to be lower than the corrosponding UL value")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (any(hp>1) || any(hp<0) ) stop("'hp' has to be between 0 and 1")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

####INPUT n
k=n+1
s=length(hp)
cp=matrix(0,k,s)
ct=matrix(0,k,s)							#Cover Pbty quantity in sum
cpp=0								#Coverage probabilty
RMSE_N1=0
RMSE_M1=0
RMSE_Mi1=0
ctr=0
###CRITICAL VALUES
#cv=qnorm(1-(alp/2), mean = 0, sd = 1)
####COVERAGE PROBABILITIES
for (j in 1:s)
{
for(i in 1:k)
{
if(hp[j] > LL[i] && hp[j] < UL[i])
{
cp[i,j]=stats::dbinom(i-1, n,hp[j])
ct[i,j]=1
}
}
cpp[j]=sum(cp[,j])
RMSE_N1[j]=(cpp[j]-(1-alp))^2			#Root mean Square from nominal size
if(t1<cpp[j]&&cpp[j]<t2) ctr=ctr+1		#tolerance for cov prob - user defined
}
#CP=data.frame(hp,cpp)
mcp=mean(cpp)
micp=min(cpp)					#Mean Cov Prob
RMSE_N=sqrt(mean(RMSE_N1))

#Root mean Square from min and mean CoPr
for (j in 1:s)
{
RMSE_M1[j]=(cpp[j]-mcp)^2
RMSE_Mi1[j]=(cpp[j]-micp)^2
}
RMSE_M=sqrt(mean(RMSE_M1))
RMSE_MI=sqrt(mean(RMSE_Mi1))
tol=100*ctr/s
return(data.frame(mcp,micp,RMSE_N,RMSE_M,RMSE_MI,tol))
}
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.general.covpgen`

```python
def covpgen(n, LL, UL, alp, hp, t1, t2):
    """Coverage probability for given limits over a given hp vector (R covpGEN)."""
    _check_limits(n, LL, UL, alp, t1, t2)
    if hp is None:
        raise ValueError("'hp' is missing")
    hp = np.atleast_1d(np.asarray(hp, dtype=float))
    if np.any((hp < 0) | (hp > 1)):
        raise ValueError("'hp' has to be between 0 and 1")
    return _coverage_core(n, alp, LL, UL, hp, t1, t2)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `covpsim`

```{eval-rst}
.. autofunction:: binomcikit.covp.general.covpsim
```

**In plain words** — the **coverage probability** of user-supplied limits over simulated p — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
wd = bk.ciwd(20, 0.05)
bk.covpsim(20, wd["LWD"].values, wd["UWD"].values, 0.05, 1000, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/225.CoverageProb_GENERAL_SIMULATEDp.R` (line 31)](https://github.com/RajeswaranV/proportion/blob/master/R/225.CoverageProb_GENERAL_SIMULATEDp.R#L31), function `covpSIM`

```r
covpSIM<-function(n,LL,UL,alp,s,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(LL)) stop("'Lower limit' is missing")
  if (missing(UL)) stop("'Upper Limit' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(s)) stop("'s' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if ((class(LL) != "integer") & (class(LL) != "numeric") || any(LL < 0)) stop("'LL' has to be a set of positive numeric vectors")
  if ((class(UL) != "integer") & (class(UL) != "numeric") || any(UL < 0)) stop("'UL' has to be a set of positive numeric vectors")
  if (length(LL) <= n ) stop("Length of vector LL has to be greater than n")
  if (length(UL) <= n ) stop("Length of vector UL has to be greater than n")
  if (any(LL[0:n+1] > UL[0:n+1] )) stop("LL value have to be lower than the corrosponding UL value")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(s) != "integer") & (class(s) != "numeric") || length(s)>1 || s<1  ) stop("'b' has to be greater than or equal to 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

  ####INPUT n
  k=n+1

  cp=matrix(0,k,s)
  ct=matrix(0,k,s)							#Cover Pbty quantity in sum
  cpp=0								#Coverage probabilty
  RMSE_N1=0
  RMSE_M1=0
  RMSE_Mi1=0
  ctr=0
  ####COVERAGE PROBABILITIES
  hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
  for (j in 1:s)
  {
    for(i in 1:k)
    {
      if(hp[j] > LL[i] && hp[j] < UL[i])
      {
        cp[i,j]=stats::dbinom(i-1, n,hp[j])
        ct[i,j]=1
      }
    }
    cpp[j]=sum(cp[,j])
    RMSE_N1[j]=(cpp[j]-(1-alp))^2			#Root mean Square from nominal size
    if(t1<cpp[j]&&cpp[j]<t2) ctr=ctr+1		#tolerance for cov prob - user defined
  }

  mcp=mean(cpp)
  micp=min(cpp)					#Mean Cov Prob
  RMSE_N=sqrt(mean(RMSE_N1))

  #Root mean Square from min and mean CoPr
  for (j in 1:s)
  {
    RMSE_M1[j]=(cpp[j]-mcp)^2
    RMSE_Mi1[j]=(cpp[j]-micp)^2
  }
  RMSE_M=sqrt(mean(RMSE_M1))
  RMSE_MI=sqrt(mean(RMSE_Mi1))
  tol=100*ctr/s
  return(data.frame(mcp,micp,RMSE_N,RMSE_M,RMSE_MI,tol))
}
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.general.covpsim`

```python
def covpsim(n, LL, UL, alp, s, a, b, t1, t2, seed=None):
    """Coverage probability for given limits over s Beta(a, b) draws (R covpSIM)."""
    _check_limits(n, LL, UL, alp, t1, t2)
    if s is None:
        raise ValueError("'s' is missing")
    if not isinstance(s, (int, float)) or s <= 0:
        raise ValueError("'s' has to be greater than 0")
    if not isinstance(a, (int, float)) or a < 0:
        raise ValueError("'a' has to be greater than or equal to 0")
    if not isinstance(b, (int, float)) or b < 0:
        raise ValueError("'b' has to be greater than or equal to 0")
    rng = np.random.default_rng(seed)
    hp = np.sort(rng.beta(a, b, int(s)))
    return _coverage_core(n, alp, LL, UL, hp, t1, t2)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

