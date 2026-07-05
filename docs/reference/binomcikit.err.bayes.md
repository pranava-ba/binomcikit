<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `err.bayes`

```{eval-rst}
.. module:: binomcikit.err.bayes
```

This module computes **error and failure** — for a null proportion `phi` and threshold `f`, the increase in nominal error, the long-term power, and a pass/fail verdict for each interval, for the **Bayesian** credible interval. These functions reuse the confidence-interval limits from the 1xx `ci` family and feed them through a shared engine, so only the supplied limits differ between methods. See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `errba`

```{eval-rst}
.. autofunction:: binomcikit.err.bayes.errba
```

**In plain words** — the **error and failure** summary of the Bayesian credible interval for a null proportion `phi` and threshold `f` — the increase in nominal error (`delalp`), long-term power (`theta`) and a pass/fail verdict

**The maths** — `delalp` $=100(\alpha-\sum_{x:\,\phi\notin[L_x,U_x]}\binom{n}{x}\phi^x(1-\phi)^{n-x})$; `theta` is the % of `x` excluding `phi`; `Fail_Pass` is *failure* iff `delalp < f`.

**Example**

```python
import binomcikit as bk
bk.errba(20, 0.05, 0.5, -2, 1, 1)
```

**R source** — [`R/501.Error-Failure_LimitBased_BASE_All.R` (line 607)](https://github.com/RajeswaranV/proportion/blob/master/R/501.Error-Failure_LimitBased_BASE_All.R#L607), function `errBA`

```r
errBA<-function(n,alp,phi,f,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0 || length(phi)>1) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")|| length(f)>1) stop("'f' has to be numeric value")
  if ((class(a) != "integer") & (class(a) != "numeric") || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || b<0  ) stop("'b' has to be greater than or equal to 0")

####INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
LBAQ=0
UBAQ=0
LBAH=0
UBAH=0
##############
#library(TeachingDemos)				#To get HPDs
for(i in 1:k)
{
#Quantile Based Intervals
LBAQ[i]=stats::qbeta(alp/2,x[i]+a,n-x[i]+b)
UBAQ[i]=stats::qbeta(1-(alp/2),x[i]+a,n-x[i]+b)

LBAH[i]=TeachingDemos::hpd(stats::qbeta,shape1=x[i]+a,shape2=n-x[i]+b,conf=1-alp)[1]
UBAH[i]=TeachingDemos::hpd(stats::qbeta,shape1=x[i]+a,shape2=n-x[i]+b,conf=1-alp)[2]

}
###DELTA_ALPHA, THETA,F_Quantile Based
alpstarLQ=0
thetactrQ=0
for(m in 1:k)
{
if(phi > UBAQ[m] || phi < LBAQ[m])
{
thetactrQ=thetactrQ+1
alpstarLQ[m]=stats::dbinom(x[m],n,phi)
} else alpstarLQ[m] = 0
}

delalpLQ=round((alp-sum(alpstarLQ))*100,2)
thetaQ=round(100*thetactrQ/(n+1),2)
if(delalpLQ<f)
Fail_PassQ="failure" else Fail_PassQ="success"

###DELTA_ALPHA, THETA,F_HPD Based
alpstarLH=0
thetactrH=0
for(m in 1:k)
{
if(phi > UBAH[m] || phi < LBAH[m])
{
thetactrH=thetactrH+1
alpstarLH[m]=stats::dbinom(x[m],n,phi)
} else alpstarLH[m] = 0
}

delalpLH=round((alp-sum(alpstarLH))*100,2)
thetaH=round(100*thetactrH/(n+1),2)
if(delalpLH<f)
Fail_PassH="failure" else Fail_PassH="success"
qdf=data.frame(delalp=delalpLQ,theta=thetaQ,Fail_Pass=Fail_PassQ,method="Quantile")
hdf=data.frame(delalp=delalpLH,theta=thetaH,Fail_Pass=Fail_PassH,method="HPD")
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function reads the interval limits, sums the binomial mass at the `x` that exclude `phi`, and returns `delalp`, `theta`, `Fail_Pass`.

**Python source** — `binomcikit.err.bayes.errba`

```python
def errba(n, alp, phi, f, a, b):
    """Error/failure of the Bayesian credible interval (R errBA)."""
    _validate(n, alp, phi, f)
    if not isinstance(a, (int, float)) or a < 0:
        raise ValueError("'a' has to be greater than or equal to 0")
    if not isinstance(b, (int, float)) or b < 0:
        raise ValueError("'b' has to be greater than or equal to 0")

    ba = ciba(n, alp, a, b)
    rows = []
    for label, lo, hi in [("Quantile", 'LBAQ', 'UBAQ'), ("HPD", 'LBAH', 'UBAH')]:
        row = _error(n, alp, phi, f, ba[lo], ba[hi]).iloc[0].to_dict()
        row['method'] = label
        rows.append(row)
    out = pd.DataFrame(rows)
    return out[['method', 'delalp', 'theta', 'Fail_Pass']]

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_error` engine; matches R exactly.

**R → Py changes** — uses SciPy HPD (`_hpd.hpd_beta`); lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

