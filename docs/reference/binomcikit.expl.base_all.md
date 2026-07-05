<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `expl.base_all`

```{eval-rst}
.. module:: binomcikit.expl.base_all
```

This module computes **expected interval length** — the average width of each interval over hypothetical *p* drawn from a `Beta(a, b)` prior, for the **base** interval methods. These functions reuse the confidence-interval limits from the 1xx `ci` family and feed them through a shared engine, so only the supplied limits differ between methods. See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `explall`

```{eval-rst}
.. autofunction:: binomcikit.expl.base_all.explall
```

**In plain words** — the per-*p* **expected-length curve** for all interval methods — the raw `(hp, ew)` values behind the expected-length plots

**The maths** — Same expected-length quantity as `length*`, but returned for every simulated *p* rather than summarised.

**Example**

```python
import binomcikit as bk
bk.explall(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/301.Expec_Leng_BASE_All.R` (line 1052)](https://github.com/RajeswaranV/proportion/blob/master/R/301.Expec_Leng_BASE_All.R#L1052), function `explAll`

```r
explAll<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

  #### Calling functions and creating df
  df.1    = gexplWD(n,alp,a,b)
  df.2    = gexplSC(n,alp,a,b)
  df.3    = gexplAS(n,alp,a,b)
  df.4    = gexplLT(n,alp,a,b)
  df.5    = gexplTW(n,alp,a,b)
  df.6    = gexplLR(n,alp,a,b)

  df.new=  rbind(df.1,df.2,df.3,df.4,df.5,df.6)
  return(df.new)
}
```

**What the R code does** — The R function returns the expected length at each simulated *p* (for plotting).

**Python source** — `binomcikit.expl.base_all.explall`

```python
def explall(n, alp, a, b, seed=None):
    """Expected-length curves for all six base methods (R explAll)."""
    _validate(n, alp, a, b)
    hp = _beta_hp(a, b, seed)
    return pd.concat(
        [_expl_curve(n, _base_lengths(m, n, alp), hp, m) for m in _BASE],
        ignore_index=True)

```

**What the Python code does** — The Python port reuses the shared `_expl_curve` engine, returning a long `(hp, ew, method)` frame.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthall`

```{eval-rst}
.. autofunction:: binomcikit.expl.base_all.lengthall
```

**In plain words** — the **expected length** of all interval methods — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthall(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/301.Expec_Leng_BASE_All.R` (line 1015)](https://github.com/RajeswaranV/proportion/blob/master/R/301.Expec_Leng_BASE_All.R#L1015), function `lengthAll`

```r
lengthAll<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")


  #### Calling functions and creating df

  df1    = lengthWD(n,alp,a,b)
  df2    = lengthSC(n,alp,a,b)
  df3    = lengthAS(n,alp,a,b)
  df4    = lengthLT(n,alp,a,b)
  df5    = lengthTW(n,alp,a,b)
  df6    = lengthLR(n,alp,a,b)

  df1$method = "Wald"
  df2$method = "Score"
  df3$method = "ArcSine"
  df4$method = "Logit-Wald"
  df5$method = "Wald-T"
  df6$method = "Likelihood"

  Final.df= rbind(df1,df2,df3,df4,df5,df6)

  return(Final.df)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.base_all.lengthall`

```python
def lengthall(n, alp, a, b, seed=None):
    """Expected-length summary for all six base methods (R lengthAll)."""
    _validate(n, alp, a, b)
    rows = []
    for name in _BASE:
        row = _length(n, alp, a, b,
                      *(_split_limits(name, n, alp)), seed).iloc[0].to_dict()
        row['method'] = name
        rows.append(row)
    out = pd.DataFrame(rows)
    return out[['method', 'sumLen', 'explMean', 'explSD', 'explMax',
                'explLL', 'explUL']]

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthas`

```{eval-rst}
.. autofunction:: binomcikit.expl.base_all.lengthas
```

**In plain words** — the **expected length** of the ArcSine (variance-stabilised) interval — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthas(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/301.Expec_Leng_BASE_All.R` (line 269)](https://github.com/RajeswaranV/proportion/blob/master/R/301.Expec_Leng_BASE_All.R#L269), function `lengthAS`

```r
lengthAS<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

####INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
pA=0
qA=0
seA=0
LA=0
UA=0
s=5000
LEA=0 								#LENGTH OF INTERVAL

ewiA=matrix(0,k,s)						#sum of length quantity in sum
ewA=0									#sum of length
###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#WALD METHOD
#ARC-SINE METHOD
for(i in 1:k)
{
pA[i]=x[i]/n
qA[i]=1-pA[i]
seA[i]=cv/sqrt(4*n)
LA[i]=(sin(asin(sqrt(pA[i]))-seA[i]))^2
UA[i]=(sin(asin(sqrt(pA[i]))+seA[i]))^2
if(LA[i]<0) LA[i]=0
if(UA[i]>1) UA[i]=1
LEA[i]=UA[i]-LA[i]
}
#sumLEA=sum(LEA)
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
  for(i in 1:k)
  {
    ewiA[i,j]=LEA[i]*stats::dbinom(i-1, n,hp[j])
  }
  ewA[j]=sum(ewiA[,j])						#Expected Length
}

sumLen=sum(LEA)
explMean=mean(ewA)
explSD=stats::sd(ewA)
explMax=max(ewA)
explLL=explMean-(explSD)
explUL=explMean+(explSD)
df.Summary=data.frame(sumLen,explMean,explSD,explMax,explLL,explUL)
return(df.Summary)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.base_all.lengthas`

```python
def lengthas(n, alp, a, b, seed=None):
    """Expected length of the ArcSine interval (R lengthAS)."""
    _validate(n, alp, a, b)
    df = cias(n, alp)
    return _length(n, alp, a, b, df['LAS'], df['UAS'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthex`

```{eval-rst}
.. autofunction:: binomcikit.expl.base_all.lengthex
```

**In plain words** — the **expected length** of the Exact (Clopper-Pearson / mid-p) interval — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthex(20, 0.05, 0.5, 1, 1, seed=0)
```

**R source** — [`R/301.Expec_Leng_BASE_All.R` (line 738)](https://github.com/RajeswaranV/proportion/blob/master/R/301.Expec_Leng_BASE_All.R#L738), function `lengthEX`

```r
lengthEX<-function(n,alp,e,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(e)) stop("'e' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(e) != "integer") & (class(e) != "numeric") || any(e>1) || any(e<0)) stop("'e' has to be between 0 and 1")
  if (length(e)>10) stop("'e' can have only 10 intervals")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

  nvar=length(e)

  res <- data.frame()

  for(i in 1:nvar)
  {
    lu=glengthEX301(n,alp,e[i],a,b)
    res <- rbind(res,lu)
  }
  return(res)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.base_all.lengthex`

```python
def lengthex(n, alp, e, a, b, seed=None):
    """Expected length of the Exact interval (R lengthEX)."""
    _validate(n, alp, a, b)
    if e is None:
        raise ValueError("'e' is missing")
    df = ciex(n, alp, [e])
    return _length(n, alp, a, b, df['LEX'], df['UEX'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthlr`

```{eval-rst}
.. autofunction:: binomcikit.expl.base_all.lengthlr
```

**In plain words** — the **expected length** of the Likelihood-Ratio interval — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthlr(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/301.Expec_Leng_BASE_All.R` (line 623)](https://github.com/RajeswaranV/proportion/blob/master/R/301.Expec_Leng_BASE_All.R#L623), function `lengthLR`

```r
lengthLR<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

####INPUT n
y=0:n
k=n+1
####INITIALIZATIONS
mle=0
cutoff=0
LL=0
UL=0
s=5000
LEL=0 								#LENGTH OF INTERVAL

ewiL=matrix(0,k,s)						#sum of length quantity in sum
ewL=0										#Simulation run to generate hypothetical p
###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#LIKELIHOOD-RATIO METHOD
for(i in 1:k)
{
likelhd = function(p) stats::dbinom(y[i],n,p)
loglik = function(p) stats::dbinom(y[i],n,p,log=TRUE)
mle[i]=stats::optimize(likelhd,c(0,1),maximum=TRUE)$maximum
cutoff[i]=loglik(mle[i])-(cv^2/2)
loglik.optim=function(p){abs(cutoff[i]-loglik(p))}
LL[i]=stats::optimize(loglik.optim, c(0,mle[i]))$minimum
UL[i]=stats::optimize(loglik.optim, c(mle[i],1))$minimum
LEL[i]=UL[i]-LL[i]
}
#sumLEL=sum(LEL)
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
  for(i in 1:k)
  {
    ewiL[i,j]=LEL[i]*stats::dbinom(i-1, n,hp[j])
  }
  ewL[j]=sum(ewiL[,j])						#Expected Length
}

sumLen=sum(LEL)
explMean=mean(ewL)
explSD=stats::sd(ewL)
explMax=max(ewL)
explLL=explMean-(explSD)
explUL=explMean+(explSD)
df.Summary=data.frame(sumLen,explMean,explSD,explMax,explLL,explUL)
return(df.Summary)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.base_all.lengthlr`

```python
def lengthlr(n, alp, a, b, seed=None):
    """Expected length of the Likelihood-Ratio interval (R lengthLR)."""
    _validate(n, alp, a, b)
    df = cilr(n, alp)
    return _length(n, alp, a, b, df['LLR'], df['ULR'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthlt`

```{eval-rst}
.. autofunction:: binomcikit.expl.base_all.lengthlt
```

**In plain words** — the **expected length** of the Logit-Wald interval — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthlt(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/301.Expec_Leng_BASE_All.R` (line 379)](https://github.com/RajeswaranV/proportion/blob/master/R/301.Expec_Leng_BASE_All.R#L379), function `lengthLT`

```r
lengthLT<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

####INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
pLT=0
qLT=0
seLT=0
lgit=0
LLT=0
ULT=0
s=5000
LELT=0 								#LENGTH OF INTERVAL

ewiLT=matrix(0,k,s)						#sum of length quantity in sum
ewLT=0									#sum of length
###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#LOGIT-WALD METHOD

pLT[1]=0
qLT[1]=1
LLT[1] = 0
ULT[1] = 1-((alp/2)^(1/n))

pLT[k]=1
qLT[k]=0
LLT[k]= (alp/2)^(1/n)
ULT[k]=1

for(j in 1:(k-2))
{
pLT[j+1]=x[j+1]/n
qLT[j+1]=1-pLT[j+1]
lgit[j+1]=log(pLT[j+1]/qLT[j+1])
seLT[j+1]=sqrt(pLT[j+1]*qLT[j+1]*n)
LLT[j+1]=1/(1+exp(-lgit[j+1]+(cv/seLT[j+1])))
ULT[j+1]=1/(1+exp(-lgit[j+1]-(cv/seLT[j+1])))
if(LLT[j+1]<0) LLT[j+1]=0
if(ULT[j+1]>1) ULT[j+1]=1
}
for(i in 1:k)
{
LELT[i]=ULT[i]-LLT[i]
}
#sumLET=sum(LELT)
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
  for(i in 1:k)
  {
    ewiLT[i,j]=LELT[i]*stats::dbinom(i-1, n,hp[j])
  }
  ewLT[j]=sum(ewiLT[,j])						#Expected Length
}

sumLen=sum(LELT)
explMean=mean(ewLT)
explSD=stats::sd(ewLT)
explMax=max(ewLT)
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.base_all.lengthlt`

```python
def lengthlt(n, alp, a, b, seed=None):
    """Expected length of the Logit-Wald interval (R lengthLT)."""
    _validate(n, alp, a, b)
    df = cilt(n, alp)
    return _length(n, alp, a, b, df['LLT'], df['ULT'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthsc`

```{eval-rst}
.. autofunction:: binomcikit.expl.base_all.lengthsc
```

**In plain words** — the **expected length** of the Score / Wilson interval — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthsc(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/301.Expec_Leng_BASE_All.R` (line 157)](https://github.com/RajeswaranV/proportion/blob/master/R/301.Expec_Leng_BASE_All.R#L157), function `lengthSC`

```r
lengthSC<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

####INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
pS=0
qS=0
seS=0
LS=0
US=0
s=5000
LES=0 								#LENGTH OF INTERVAL
ewiS=matrix(0,k,s)						#sum of length quantity in sum
ewS=0									#sum of length
###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
cv1=(cv^2)/(2*n)
cv2=(cv/(2*n))^2

#SCORE (WILSON) METHOD
for(i in 1:k)
{
pS[i]=x[i]/n
qS[i]=1-(x[i]/n)
seS[i]=sqrt((pS[i]*qS[i]/n)+cv2)
LS[i]=(n/(n+(cv)^2))*((pS[i]+cv1)-(cv*seS[i]))
US[i]=(n/(n+(cv)^2))*((pS[i]+cv1)+(cv*seS[i]))
if(LS[i]<0) LS[i]=0
if(US[i]>1) US[i]=1
LES[i]=US[i]-LS[i]
}
#sumLES=sum(LES)

####sum of length
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
ewiS[i,j]=LES[i]*stats::dbinom(i-1, n,hp[j])
}
ewS[j]=sum(ewiS[,j])						#sum of length
}
#ELS=data.frame(hp,ewS)
sumLen=sum(LES)
explMean=mean(ewS)
explSD=stats::sd(ewS)
explMax=max(ewS)
explLL=explMean-(explSD)
explUL=explMean+(explSD)
df.Summary=data.frame(sumLen,explMean,explSD,explMax,explLL,explUL)
return(df.Summary)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.base_all.lengthsc`

```python
def lengthsc(n, alp, a, b, seed=None):
    """Expected length of the Score interval (R lengthSC)."""
    _validate(n, alp, a, b)
    df = cisc(n, alp)
    return _length(n, alp, a, b, df['LSC'], df['USC'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthtw`

```{eval-rst}
.. autofunction:: binomcikit.expl.base_all.lengthtw
```

**In plain words** — the **expected length** of the Wald-T interval — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthtw(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/301.Expec_Leng_BASE_All.R` (line 504)](https://github.com/RajeswaranV/proportion/blob/master/R/301.Expec_Leng_BASE_All.R#L504), function `lengthTW`

```r
lengthTW<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

####INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
pTW=0
qTW=0
seTW=0
LTW=0
UTW=0
DOF=0
cv=0
s=5000
LETW=0 								#LENGTH OF INTERVAL

ewiTW=matrix(0,k,s)						#sum of length quantity in sum
ewTW=0									#sum of length
#MODIFIED_t-WALD METHOD
for(i in 1:k)
{
if(x[i]==0||x[i]==n)
{
pTW[i]=(x[i]+2)/(n+4)
qTW[i]=1-pTW[i]
}else
{
pTW[i]=x[i]/n
qTW[i]=1-pTW[i]
}
f1=function(p,n) p*(1-p)/n
f2=function(p,n) (p*(1-p)/(n^3))+(p+((6*n)-7)*(p^2)+(4*(n-1)*(n-3)*(p^3))-(2*(n-1)*((2*n)-3)*(p^4)))/(n^5)-(2*(p+((2*n)-3)*(p^2)-2*(n-1)*(p^3)))/(n^4)
DOF[i]=2*((f1(pTW[i],n))^2)/f2(pTW[i],n)
cv[i]=stats::qt(1-(alp/2), df=DOF[i])
seTW[i]=cv[i]*sqrt(f1(pTW[i],n))
LTW[i]=pTW[i]-(seTW[i])
UTW[i]=pTW[i]+(seTW[i])
if(LTW[i]<0) LTW[i]=0
if(UTW[i]>1) UTW[i]=1
LETW[i]=UTW[i]-LTW[i]
}
#sumLETW=sum(LETW)
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
  for(i in 1:k)
  {
    ewiTW[i,j]=LETW[i]*stats::dbinom(i-1, n,hp[j])
  }
  ewTW[j]=sum(ewiTW[,j])						#Expected Length
}

sumLen=sum(LETW)
explMean=mean(ewTW)
explSD=stats::sd(ewTW)
explMax=max(ewTW)
explLL=explMean-(explSD)
explUL=explMean+(explSD)
df.Summary=data.frame(sumLen,explMean,explSD,explMax,explLL,explUL)
return(df.Summary)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.base_all.lengthtw`

```python
def lengthtw(n, alp, a, b, seed=None):
    """Expected length of the Wald-T interval (R lengthTW)."""
    _validate(n, alp, a, b)
    df = citw(n, alp)
    return _length(n, alp, a, b, df['LTW'], df['UTW'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthwd`

```{eval-rst}
.. autofunction:: binomcikit.expl.base_all.lengthwd
```

**In plain words** — the **expected length** of the Wald (normal-approximation) interval — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthwd(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/301.Expec_Leng_BASE_All.R` (line 49)](https://github.com/RajeswaranV/proportion/blob/master/R/301.Expec_Leng_BASE_All.R#L49), function `lengthWD`

```r
lengthWD<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

####INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
pW=0
qW=0
seW=0
LW=0
UW=0
s=5000
LEW=0 								#LENGTH OF INTERVAL

ewiW=matrix(0,k,s)						#sum of length quantity in sum
ewW=0									#sum of length
###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#WALD METHOD
for(i in 1:k)
{
pW[i]=x[i]/n
qW[i]=1-(x[i]/n)
seW[i]=sqrt(pW[i]*qW[i]/n)
LW[i]=pW[i]-(cv*seW[i])
UW[i]=pW[i]+(cv*seW[i])
if(LW[i]<0) LW[i]=0
if(UW[i]>1) UW[i]=1
LEW[i]=UW[i]-LW[i]
}
#sumLEW=sum(LEW)
####sum of length
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
ewiW[i,j]=LEW[i]*stats::dbinom(i-1, n,hp[j])
}
ewW[j]=sum(ewiW[,j])						#sum of length
}
#ELW=data.frame(hp,ewW)
sumLen=sum(LEW)
explMean=mean(ewW)
explSD=stats::sd(ewW)
explMax=max(ewW)
explLL=explMean-(explSD)
explUL=explMean+(explSD)
df.Summary=data.frame(sumLen,explMean,explSD,explMax,explLL,explUL)
return(df.Summary)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.base_all.lengthwd`

```python
def lengthwd(n, alp, a, b, seed=None):
    """Expected length of the Wald interval (R lengthWD)."""
    _validate(n, alp, a, b)
    df = ciwd(n, alp)
    return _length(n, alp, a, b, df['LWD'], df['UWD'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

