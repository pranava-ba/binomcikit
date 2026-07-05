<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `expl.adj_all`

```{eval-rst}
.. module:: binomcikit.expl.adj_all
```

This module computes **expected interval length** — the average width of each interval over hypothetical *p* drawn from a `Beta(a, b)` prior, for the **adjusted** (pseudo-count `x+h`, `n+2h`) interval methods. These functions reuse the confidence-interval limits from the 1xx `ci` family and feed them through a shared engine, so only the supplied limits differ between methods. See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `explaall`

```{eval-rst}
.. autofunction:: binomcikit.expl.adj_all.explaall
```

**In plain words** — the per-*p* **expected-length curve** for all adjusted interval methods — the raw `(hp, ew)` values behind the expected-length plots

**The maths** — Same expected-length quantity as `length*`, but returned for every simulated *p* rather than summarised.

**Example**

```python
import binomcikit as bk
bk.explaall(20, 0.05, 2, 1, 1, seed=0)
```

**R source** — [`R/311.Expec_Leng_ADJ_All.R` (line 662)](https://github.com/RajeswaranV/proportion/blob/master/R/311.Expec_Leng_ADJ_All.R#L662), function `explAAll`

```r
explAAll<-function(n,alp,h,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(a)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

  #### Calling functions and creating df
  df.1    = gexplAWD(n,alp,h,a,b)
  df.2    = gexplASC(n,alp,h,a,b)
  df.3    = gexplAAS(n,alp,h,a,b)
  df.4    = gexplALT(n,alp,h,a,b)
  df.5    = gexplATW(n,alp,h,a,b)
  df.6    = gexplALR(n,alp,h,a,b)

  df.new=  rbind(df.1,df.2,df.3,df.4,df.5,df.6)
  return(df.new)
}
```

**What the R code does** — The R function returns the expected length at each simulated *p* (for plotting).

**Python source** — `binomcikit.expl.adj_all.explaall`

```python
def explaall(n, alp, h, a, b, seed=None):
    """Expected-length curves for all six adjusted methods (R explAAll)."""
    _validate_adj(n, alp, h, a, b)
    hp = _beta_hp(a, b, seed)
    curves = []
    for name, (fn, lo, hi) in _ADJ.items():
        df = fn(n, alp, h)
        lengths = df[hi].to_numpy() - df[lo].to_numpy()
        curves.append(_expl_curve(n, lengths, hp, name))
    return pd.concat(curves, ignore_index=True)

```

**What the Python code does** — The Python port reuses the shared `_expl_curve` engine, returning a long `(hp, ew, method)` frame.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthaall`

```{eval-rst}
.. autofunction:: binomcikit.expl.adj_all.lengthaall
```

**In plain words** — the **expected length** of all adjusted interval methods — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthaall(20, 0.05, 2, 1, 1, seed=0)
```

**R source** — [`R/311.Expec_Leng_ADJ_All.R` (line 625)](https://github.com/RajeswaranV/proportion/blob/master/R/311.Expec_Leng_ADJ_All.R#L625), function `lengthAAll`

```r
lengthAAll<-function(n,alp,h,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h) >1|| h<0  || !(h%%1 ==0)) stop("'h' has to be an integer greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

  #### Calling functions and creating df

  df1    = lengthAWD(n,alp,h,a,b)
  df2    = lengthASC(n,alp,h,a,b)
  df3    = lengthAAS(n,alp,h,a,b)
  df4    = lengthALT(n,alp,h,a,b)
  df5    = lengthATW(n,alp,h,a,b)
  df6    = lengthALR(n,alp,h,a,b)

  df1$method = "Adj-Wald"
  df2$method = "Adj-Score"
  df3$method = "Adj-ArcSine"
  df4$method = "Adj-Logit-Wald"
  df5$method = "Adj-Wald-T"
  df6$method = "Adj-Likelihood"

  Final.df= rbind(df1,df2,df3,df4,df5,df6)

  return(Final.df)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.adj_all.lengthaall`

```python
def lengthaall(n, alp, h, a, b, seed=None):
    """Expected-length summary for all six adjusted methods (R lengthAAll)."""
    _validate_adj(n, alp, h, a, b)
    rows = []
    for name in _ADJ:
        row = _adj_length(name, n, alp, h, a, b, seed).iloc[0].to_dict()
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

## `lengthaas`

```{eval-rst}
.. autofunction:: binomcikit.expl.adj_all.lengthaas
```

**In plain words** — the **expected length** of the adjusted ArcSine (variance-stabilised) interval — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthaas(20, 0.05, 2, 1, 1, seed=0)
```

**R source** — [`R/311.Expec_Leng_ADJ_All.R` (line 230)](https://github.com/RajeswaranV/proportion/blob/master/R/311.Expec_Leng_ADJ_All.R#L230), function `lengthAAS`

```r
lengthAAS<-function(n,alp,h,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(a)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

####INPUT n
x=0:n
k=n+1
y=x+h
m=n+(2*h)
####INITIALIZATIONS
pAA=0
qAA=0
seAA=0
LAA=0
UAA=0
s=2000
LEAA=0 								#LENGTH OF INTERVAL

ewiAA=matrix(0,k,s)						#sum of length quantity in sum
ewAA=0									#sum of length
###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#ARC-SINE METHOD
for(i in 1:k)
{
pAA[i]=y[i]/m
qAA[i]=1-pAA[i]
seAA[i]=cv/sqrt(4*m)
LAA[i]=(sin(asin(sqrt(pAA[i]))-seAA[i]))^2
UAA[i]=(sin(asin(sqrt(pAA[i]))+seAA[i]))^2
if(LAA[i]<0) LAA[i]=0
if(UAA[i]>1) UAA[i]=1
LEAA[i]=UAA[i]-LAA[i]
}
#sumLEAA=sum(LEAA)
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
  for(i in 1:k)
  {
    ewiAA[i,j]=LEAA[i]*stats::dbinom(i-1, n,hp[j])
  }
  ewAA[j]=sum(ewiAA[,j])						#Expected Length
}

sumLen=sum(LEAA)
explMean=mean(ewAA)
explSD=stats::sd(ewAA)
explMax=max(ewAA)
explLL=explMean-(explSD)
explUL=explMean+(explSD)
df.Summary=data.frame(sumLen,explMean,explSD,explMax,explLL,explUL)
return(df.Summary)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.adj_all.lengthaas`

```python
def lengthaas(n, alp, h, a, b, seed=None):
    """Expected length of the adjusted ArcSine interval (R lengthAAS)."""
    _validate_adj(n, alp, h, a, b)
    return _adj_length("ArcSine", n, alp, h, a, b, seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthalr`

```{eval-rst}
.. autofunction:: binomcikit.expl.adj_all.lengthalr
```

**In plain words** — the **expected length** of the adjusted Likelihood-Ratio interval — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthalr(20, 0.05, 2, 1, 1, seed=0)
```

**R source** — [`R/311.Expec_Leng_ADJ_All.R` (line 528)](https://github.com/RajeswaranV/proportion/blob/master/R/311.Expec_Leng_ADJ_All.R#L528), function `lengthALR`

```r
lengthALR<-function(n,alp,h,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h) >1|| h<0  || !(h%%1 ==0)) stop("'h' has to be an integer greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

####INPUT n
y=0:n
y1=y+h
k=n+1
n1=n+(2*h)
####INITIALIZATIONS
mle=0
cutoff=0
LAL=0
UAL=0
s=2000
LEAL=0 								#LENGTH OF INTERVAL

ewiAL=matrix(0,k,s)						#sum of length quantity in sum
ewAL=0									#sum of length
###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#LIKELIHOOD-RATIO METHOD
for(i in 1:k)
{
likelhd = function(p) stats::dbinom(y1[i],n1,p)
loglik = function(p) stats::dbinom(y1[i],n1,p,log=TRUE)
mle[i]=stats::optimize(likelhd,c(0,1),maximum=TRUE)$maximum
cutoff[i]=loglik(mle[i])-(cv^2/2)
loglik.optim=function(p){abs(cutoff[i]-loglik(p))}
LAL[i]=stats::optimize(loglik.optim, c(0,mle[i]))$minimum
UAL[i]=stats::optimize(loglik.optim, c(mle[i],1))$minimum
LEAL[i]=UAL[i]-LAL[i]
}
#sumLEAL=sum(LEAL)
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
  for(i in 1:k)
  {
    ewiAL[i,j]=LEAL[i]*stats::dbinom(i-1, n,hp[j])
  }
  ewAL[j]=sum(ewiAL[,j])						#Expected Length
}

sumLen=sum(LEAL)
explMean=mean(ewAL)
explSD=stats::sd(ewAL)
explMax=max(ewAL)
explLL=explMean-(explSD)
explUL=explMean+(explSD)
df.Summary=data.frame(sumLen,explMean,explSD,explMax,explLL,explUL)
return(df.Summary)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.adj_all.lengthalr`

```python
def lengthalr(n, alp, h, a, b, seed=None):
    """Expected length of the adjusted Likelihood-Ratio interval (R lengthALR)."""
    _validate_adj(n, alp, h, a, b)
    return _adj_length("Likelihood", n, alp, h, a, b, seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthalt`

```{eval-rst}
.. autofunction:: binomcikit.expl.adj_all.lengthalt
```

**In plain words** — the **expected length** of the adjusted Logit-Wald interval — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthalt(20, 0.05, 2, 1, 1, seed=0)
```

**R source** — [`R/311.Expec_Leng_ADJ_All.R` (line 327)](https://github.com/RajeswaranV/proportion/blob/master/R/311.Expec_Leng_ADJ_All.R#L327), function `lengthALT`

```r
lengthALT<-function(n,alp,h,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(a)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

####INPUT n
x=0:n
k=n+1
y=x+h
n1=n+(2*h)

####INITIALIZATIONS
pALT=0
qALT=0
seALT=0
lgit=0
LALT=0
UALT=0
s=2000
LEALT=0 								#LENGTH OF INTERVAL

ewiALT=matrix(0,k,s)						#sum of length quantity in sum
ewALT=0									#sum of length
###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#LOGIT-WALD METHOD

for(i in 1:k)
{
pALT[i]=y[i]/n1
qALT[i]=1-pALT[i]
lgit[i]=log(pALT[i]/qALT[i])
seALT[i]=sqrt(pALT[i]*qALT[i]*n1)
LALT[i]=1/(1+exp(-lgit[i]+(cv/seALT[i])))
UALT[i]=1/(1+exp(-lgit[i]-(cv/seALT[i])))
if(LALT[i]<0) LALT[i]=0
if(UALT[i]>1) UALT[i]=1
LEALT[i]=UALT[i]-LALT[i]
}
#sumLEALT=sum(LEALT)
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
  for(i in 1:k)
  {
    ewiALT[i,j]=LEALT[i]*stats::dbinom(i-1, n,hp[j])
  }
  ewALT[j]=sum(ewiALT[,j])						#Expected Length
}
sumLen=sum(LEALT)
explMean=mean(ewALT)
explSD=stats::sd(ewALT)
explMax=max(ewALT)
explLL=explMean-(explSD)
explUL=explMean+(explSD)
df.Summary=data.frame(sumLen,explMean,explSD,explMax,explLL,explUL)
return(df.Summary)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.adj_all.lengthalt`

```python
def lengthalt(n, alp, h, a, b, seed=None):
    """Expected length of the adjusted Logit-Wald interval (R lengthALT)."""
    _validate_adj(n, alp, h, a, b)
    return _adj_length("Logit-Wald", n, alp, h, a, b, seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthasc`

```{eval-rst}
.. autofunction:: binomcikit.expl.adj_all.lengthasc
```

**In plain words** — the **expected length** of the adjusted Score / Wilson interval — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthasc(20, 0.05, 2, 1, 1, seed=0)
```

**R source** — [`R/311.Expec_Leng_ADJ_All.R` (line 130)](https://github.com/RajeswaranV/proportion/blob/master/R/311.Expec_Leng_ADJ_All.R#L130), function `lengthASC`

```r
lengthASC<-function(n,alp,h,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(a)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

####INPUT n
x=0:n
k=n+1
y=x+h
n1=n+(2*h)
####INITIALIZATIONS
pAS=0
qAS=0
seAS=0
LAS=0
UAS=0
s=2000
LEAS=0 								#LENGTH OF INTERVAL

ewiAS=matrix(0,k,s)						#sum of length quantity in sum
ewAS=0									#sum of length
###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
cv1=(cv^2)/(2*n1)
cv2=(cv/(2*n1))^2

#SCORE (WILSON) METHOD
for(i in 1:k)
{
pAS[i]=y[i]/n1
qAS[i]=1-pAS[i]
seAS[i]=sqrt((pAS[i]*qAS[i]/n1)+cv2)
LAS[i]=(n1/(n1+(cv)^2))*((pAS[i]+cv1)-(cv*seAS[i]))
UAS[i]=(n1/(n1+(cv)^2))*((pAS[i]+cv1)+(cv*seAS[i]))
if(LAS[i]<0) LAS[i]=0
if(UAS[i]>1) UAS[i]=1
LEAS[i]=UAS[i]-LAS[i]
}
#sumLEAS=sum(LEAS)
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
  for(i in 1:k)
  {
    ewiAS[i,j]=LEAS[i]*stats::dbinom(i-1, n,hp[j])
  }
  ewAS[j]=sum(ewiAS[,j])						#Expected Length
}

sumLen=sum(LEAS)
explMean=mean(ewAS)
explSD=stats::sd(ewAS)
explMax=max(ewAS)
explLL=explMean-(explSD)
explUL=explMean+(explSD)
df.Summary=data.frame(sumLen,explMean,explSD,explMax,explLL,explUL)
return(df.Summary)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.adj_all.lengthasc`

```python
def lengthasc(n, alp, h, a, b, seed=None):
    """Expected length of the adjusted Score interval (R lengthASC)."""
    _validate_adj(n, alp, h, a, b)
    return _adj_length("Score", n, alp, h, a, b, seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthatw`

```{eval-rst}
.. autofunction:: binomcikit.expl.adj_all.lengthatw
```

**In plain words** — the **expected length** of the adjusted Wald-T interval — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthatw(20, 0.05, 2, 1, 1, seed=0)
```

**R source** — [`R/311.Expec_Leng_ADJ_All.R` (line 426)](https://github.com/RajeswaranV/proportion/blob/master/R/311.Expec_Leng_ADJ_All.R#L426), function `lengthATW`

```r
lengthATW<-function(n,alp,h,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(a)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

####INPUT n
x=0:n
k=n+1
y=x+h
n1=n+(2*h)
####INITIALIZATIONS
pATW=0
qATW=0
seATW=0
LATW=0
UATW=0
DOF=0
cv=0
s=2000
LEATW=0 								#LENGTH OF INTERVAL

ewiATW=matrix(0,k,s)						#sum of length quantity in sum
ewATW=0									#sum of length
#MODIFIED_t-ADJ_WALD METHOD
for(i in 1:k)
{
pATW[i]=y[i]/n1
qATW[i]=1-pATW[i]
f1=function(p,n) p*(1-p)/n
f2=function(p,n) (p*(1-p)/(n^3))+(p+((6*n)-7)*(p^2)+(4*(n-1)*(n-3)*(p^3))-(2*(n-1)*((2*n)-3)*(p^4)))/(n^5)-(2*(p+((2*n)-3)*(p^2)-2*(n-1)*(p^3)))/(n^4)
DOF[i]=2*((f1(pATW[i],n1))^2)/f2(pATW[i],n1)
cv[i]=stats::qt(1-(alp/2), df=DOF[i])
seATW[i]=cv[i]*sqrt(f1(pATW[i],n1))
LATW[i]=pATW[i]-(seATW[i])
UATW[i]=pATW[i]+(seATW[i])
if(LATW[i]<0) LATW[i]=0
if(UATW[i]>1) UATW[i]=1
LEATW[i]=UATW[i]-LATW[i]
}
#sumLEATW=sum(LEATW)
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
  for(i in 1:k)
  {
    ewiATW[i,j]=LEATW[i]*stats::dbinom(i-1, n,hp[j])
  }
  ewATW[j]=sum(ewiATW[,j])						#Expected Length
}

sumLen=sum(LEATW)
explMean=mean(ewATW)
explSD=stats::sd(ewATW)
explMax=max(ewATW)
explLL=explMean-(explSD)
explUL=explMean+(explSD)
df.Summary=data.frame(sumLen,explMean,explSD,explMax,explLL,explUL)
return(df.Summary)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.adj_all.lengthatw`

```python
def lengthatw(n, alp, h, a, b, seed=None):
    """Expected length of the adjusted Wald-T interval (R lengthATW)."""
    _validate_adj(n, alp, h, a, b)
    return _adj_length("Wald-T", n, alp, h, a, b, seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthawd`

```{eval-rst}
.. autofunction:: binomcikit.expl.adj_all.lengthawd
```

**In plain words** — the **expected length** of the adjusted Wald (normal-approximation) interval — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthawd(20, 0.05, 2, 1, 1, seed=0)
```

**R source** — [`R/311.Expec_Leng_ADJ_All.R` (line 33)](https://github.com/RajeswaranV/proportion/blob/master/R/311.Expec_Leng_ADJ_All.R#L33), function `lengthAWD`

```r
lengthAWD<-function(n,alp,h,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(a)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")


####INPUT n
x=0:n
k=n+1
y=x+h
m=n+(2*h)
####INITIALIZATIONS
pAW=0
qAW=0
seAW=0
LAW=0
UAW=0
s=2000
LEAW=0 								#LENGTH OF INTERVAL

ewiAW=matrix(0,k,s)						#sum of length quantity in sum
ewAW=0									#sum of length
###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#WALD METHOD
for(i in 1:k)
{
pAW[i]=y[i]/m
qAW[i]=1-pAW[i]
seAW[i]=sqrt(pAW[i]*qAW[i]/m)
LAW[i]=pAW[i]-(cv*seAW[i])
UAW[i]=pAW[i]+(cv*seAW[i])
if(LAW[i]<0) LAW[i]=0
if(UAW[i]>1) UAW[i]=1
LEAW[i]=UAW[i]-LAW[i]
}
#sumLEAW=sum(LEAW)
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
  for(i in 1:k)
  {
    ewiAW[i,j]=LEAW[i]*stats::dbinom(i-1, n,hp[j])
  }
  ewAW[j]=sum(ewiAW[,j])						#Expected Length
}

sumLen=sum(LEAW)
explMean=mean(ewAW)
explSD=stats::sd(ewAW)
explMax=max(ewAW)
explLL=explMean-(explSD)
explUL=explMean+(explSD)
df.Summary=data.frame(sumLen,explMean,explSD,explMax,explLL,explUL)
return(df.Summary)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.adj_all.lengthawd`

```python
def lengthawd(n, alp, h, a, b, seed=None):
    """Expected length of the adjusted Wald interval (R lengthAWD)."""
    _validate_adj(n, alp, h, a, b)
    return _adj_length("Wald", n, alp, h, a, b, seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

