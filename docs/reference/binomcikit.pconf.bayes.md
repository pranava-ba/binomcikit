<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `pconf.bayes`

```{eval-rst}
.. module:: binomcikit.pconf.bayes
```

This module computes **p-confidence and p-bias** — deterministic (no-simulation) measures of how well each interval's actual confidence matches its nominal level, for the **Bayesian** credible interval. These functions reuse the confidence-interval limits from the 1xx `ci` family and feed them through a shared engine, so only the supplied limits differ between methods. See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `pcopbiba`

```{eval-rst}
.. autofunction:: binomcikit.pconf.bayes.pcopbiba
```

**In plain words** — the **p-confidence and p-bias** of the Bayesian credible interval — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbiba(20, 0.05, 1, 1)
```

**R source** — [`R/401.p-Confidence_p-Bias_BASE_All.R` (line 602)](https://github.com/RajeswaranV/proportion/blob/master/R/401.p-Confidence_p-Bias_BASE_All.R#L602), function `pCOpBIBA`

```r
pCOpBIBA<-function(n,alp,a1,a2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a1)) stop("'a1' is missing")
  if (missing(a2)) stop("'a2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
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
  pconQ=0
  pconCQ=0
  pconfQ=0
  pbia1Q=0
  pbiasQ=0
  pconH=0
  pconCH=0
  pconfH=0
  pbia1H=0
  pbiasH=0

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

  for(i in 2:(k-1))
  {
    pconQ[i-1]=2*(stats::pbinom(i-1, n, LBAQ[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LBAQ[i]))
    pconCQ[i-1]=2*stats::pbinom(i-1, n, UBAQ[i], lower.tail = TRUE, log.p = FALSE)
    pconfQ[i-1]=(1-max(pconQ[i-1],pconCQ[i-1]))*100 		#p-confidence calculation
    pbia1Q[i-1]=max(pconQ[i-1],pconCQ[i-1])-min(pconQ[i-1],pconCQ[i-1])
    pbiasQ[i-1]=max(0,pbia1Q[i-1])*100

    pconH[i-1]=2*(stats::pbinom(i-1, n, LBAH[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LBAH[i]))
    pconCH[i-1]=2*stats::pbinom(i-1, n, UBAH[i], lower.tail = TRUE, log.p = FALSE)
    pconfH[i-1]=(1-max(pconH[i-1],pconCH[i-1]))*100 		#p-confidence calculation
    pbia1H[i-1]=max(pconH[i-1],pconCH[i-1])-min(pconH[i-1],pconCH[i-1])
    pbiasH[i-1]=max(0,pbia1H[i-1])*100

  }
  x1=1:(n-1)

  return(data.frame(x1,pconfQ,pbiasQ,pconfH,pbiasH))
}
```

**What the R code does** — The R function reads the interval limits and evaluates the two tail probabilities for every interior `x`, returning `x1`, `pconf`, `pbias`.

**Python source** — `binomcikit.pconf.bayes.pcopbiba`

```python
def pcopbiba(n, alp, a1, a2):
    """p-confidence and p-bias of the Bayesian credible interval (R pCOpBIBA)."""
    _validate(n, alp)
    if not isinstance(a1, (int, float)) or a1 < 0:
        raise ValueError("'a1' has to be greater than or equal to 0")
    if not isinstance(a2, (int, float)) or a2 < 0:
        raise ValueError("'a2' has to be greater than or equal to 0")

    ba = ciba(n, alp, a1, a2)
    q = _pconf_pbias(n, ba['LBAQ'], ba['UBAQ'])
    h = _pconf_pbias(n, ba['LBAH'], ba['UBAH'])
    return pd.DataFrame({
        'x1': q['x1'],
        'pconfQ': q['pconf'], 'pbiasQ': q['pbias'],
        'pconfH': h['pconf'], 'pbiasH': h['pbias'],
    })

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — uses SciPy HPD (`_hpd.hpd_beta`); lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

