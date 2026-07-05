<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `err.general`

```{eval-rst}
.. module:: binomcikit.err.general
```

This module computes **error and failure** — for a null proportion `phi` and threshold `f`, the increase in nominal error, the long-term power, and a pass/fail verdict for each interval, for **user-supplied** interval limits (given or simulated *p*). These functions reuse the confidence-interval limits from the 1xx `ci` family and feed them through a shared engine, so only the supplied limits differ between methods. See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `errgen`

```{eval-rst}
.. autofunction:: binomcikit.err.general.errgen
```

**In plain words** — the **error and failure** summary of user-supplied interval limits for a null proportion `phi` and threshold `f` — the increase in nominal error (`delalp`), long-term power (`theta`) and a pass/fail verdict

**The maths** — `delalp` $=100(\alpha-\sum_{x:\,\phi\notin[L_x,U_x]}\binom{n}{x}\phi^x(1-\phi)^{n-x})$; `theta` is the % of `x` excluding `phi`; `Fail_Pass` is *failure* iff `delalp < f`.

**Example**

```python
import binomcikit as bk
wd = bk.ciwd(20, 0.05)
bk.errgen(20, wd["LWD"].values, wd["UWD"].values, 0.05, 0.5, -2)
```

**R source** — [`R/523.Error-Failure_LimitBased_GENERAL.R` (line 26)](https://github.com/RajeswaranV/proportion/blob/master/R/523.Error-Failure_LimitBased_GENERAL.R#L26), function `errGEN`

```r
errGEN<-function(n,LL,UL,alp,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(LL)) stop("'Lower limit' is missing")
  if (missing(UL)) stop("'Upper Limit' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")) stop("'f' has to be numeric value")
  if ((class(LL) != "integer") & (class(LL) != "numeric") || any(LL < 0)) stop("'LL' has to be a set of positive numeric vectors")
  if ((class(UL) != "integer") & (class(UL) != "numeric") || any(UL < 0)) stop("'UL' has to be a set of positive numeric vectors")
  if (length(LL) <= n ) stop("Length of vector LL has to be greater than n")
  if (length(UL) <= n ) stop("Length of vector UL has to be greater than n")
  if (any(LL[0:n+1] > UL[0:n+1] )) stop("LL value have to be lower than the corrosponding UL value")

x=0:n
k=n+1
####INITIALIZATION
delalp=0
alpstar=0
thetactr=0

for(m in 1:k)
{
if(phi > UL[m] || phi<LL[m])
{
thetactr=thetactr+1
alpstar[m]=stats::dbinom(x[m],n,phi)
} else alpstar[m] = 0
}
delalp=round((alp-sum(alpstar))*100,2)
theta=round(100*thetactr/(n+1),2)
if(delalp < f)
Fail_Pass="failure" else Fail_Pass="success"
return(data.frame(delalp=delalp,theta,Fail_Pass))
}
```

**What the R code does** — The R function reads the interval limits, sums the binomial mass at the `x` that exclude `phi`, and returns `delalp`, `theta`, `Fail_Pass`.

**Python source** — `binomcikit.err.general.errgen`

```python
def errgen(n, LL, UL, alp, phi, f):
    """Error/failure for given limits (R errGEN)."""
    if n is None:
        raise ValueError("'n' is missing")
    if LL is None:
        raise ValueError("'LL' is missing")
    if UL is None:
        raise ValueError("'UL' is missing")
    if alp is None:
        raise ValueError("'alpha' is missing")
    if phi is None:
        raise ValueError("'phi' is missing")
    if f is None:
        raise ValueError("'f' is missing")
    if not isinstance(n, (int, float)) or n <= 0:
        raise ValueError("'n' has to be greater than 0")
    if not 0 <= alp <= 1:
        raise ValueError("'alpha' has to be between 0 and 1")
    if not isinstance(phi, (int, float)) or not 0 <= phi <= 1:
        raise ValueError("Null hypothesis 'phi' has to be between 0 and 1")
    LL = np.asarray(LL, dtype=float)
    UL = np.asarray(UL, dtype=float)
    if len(LL) < n + 1 or len(UL) < n + 1:
        raise ValueError("'LL' and 'UL' both have to be of length n+1")
    return _error(n, alp, phi, f, LL, UL)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_error` engine; matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

