<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `pconf.general`

```{eval-rst}
.. module:: binomcikit.pconf.general
```

This module computes **p-confidence and p-bias** — deterministic (no-simulation) measures of how well each interval's actual confidence matches its nominal level, for **user-supplied** interval limits (given or simulated *p*). These functions reuse the confidence-interval limits from the 1xx `ci` family and feed them through a shared engine, so only the supplied limits differ between methods. See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `pcopbigen`

```{eval-rst}
.. autofunction:: binomcikit.pconf.general.pcopbigen
```

**In plain words** — the **p-confidence and p-bias** of user-supplied interval limits — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
wd = bk.ciwd(20, 0.05)
bk.pcopbigen(20, wd["LWD"].values, wd["UWD"].values)
```

**R source** — [`R/423.p-Confidence_p-Bias_GENERAL.R` (line 34)](https://github.com/RajeswaranV/proportion/blob/master/R/423.p-Confidence_p-Bias_GENERAL.R#L34), function `pCOpBIGEN`

```r
pCOpBIGEN<-function(n,LL,UL)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(LL)) stop("'Lower limit' is missing")
  if (missing(UL)) stop("'Upper Limit' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if ((class(LL) != "integer") & (class(LL) != "numeric") || any(LL < 0)) stop("'LL' has to be a set of positive numeric vectors")
  if ((class(UL) != "integer") & (class(UL) != "numeric") || any(UL < 0)) stop("'UL' has to be a set of positive numeric vectors")
  if (length(LL) < n ) stop("Length of vector LL has to be greater than n")
  if (length(UL) < n ) stop("Length of vector UL has to be greater than n")
  if (any(LL[0:n+1] > UL[0:n+1] )) stop("LL value have to be lower than the corrosponding UL value")

####INPUT n
#x=0:n
k=n+1
pcon=0					#p-confidence
pconC=0
pconf=0
pbia1=0					#p-bias
pbias=0
####p-confidence and p-bias
for(i in 2:(k-1))
{
pcon[i-1]=2*(stats::pbinom(i-1, n, LL[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LL[i]))
pconC[i-1]=2*stats::pbinom(i-1, n, UL[i], lower.tail = TRUE, log.p = FALSE)
pconf[i-1]=(1-max(pcon[i-1],pconC[i-1]))*100 		#p-confidence calculation
pbia1[i-1]=max(pcon[i-1],pconC[i-1])-min(pcon[i-1],pconC[i-1])
pbias[i-1]=max(0,pbia1[i-1])*100
}
x1=1:(n-1)
p_C_B=data.frame(x1,pconf,pbias)
return(p_C_B)
}
```

**What the R code does** — The R function reads the interval limits and evaluates the two tail probabilities for every interior `x`, returning `x1`, `pconf`, `pbias`.

**Python source** — `binomcikit.pconf.general.pcopbigen`

```python
def pcopbigen(n, LL, UL):
    """p-confidence and p-bias for given limits (R pCOpBIGEN)."""
    if n is None:
        raise ValueError("'n' is missing")
    if LL is None:
        raise ValueError("'Lower limit' is missing")
    if UL is None:
        raise ValueError("'Upper Limit' is missing")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    LL = np.asarray(LL, dtype=float)
    UL = np.asarray(UL, dtype=float)
    if np.any(LL < 0) or np.any(UL < 0):
        raise ValueError("'LL' and 'UL' have to be positive")
    if len(LL) < n + 1 or len(UL) < n + 1:
        raise ValueError("'LL' and 'UL' both have to be of length n+1")
    if np.any(LL[:n + 1] > UL[:n + 1]):
        raise ValueError("LL values have to be lower than the corresponding UL")
    return _pconf_pbias(n, LL, UL)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

