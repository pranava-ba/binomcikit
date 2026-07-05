<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `expl.cc_all`

```{eval-rst}
.. module:: binomcikit.expl.cc_all
```

This module computes **expected interval length** — the average width of each interval over hypothetical *p* drawn from a `Beta(a, b)` prior, for the **continuity-corrected** interval methods (five methods; no Likelihood-Ratio). These functions reuse the confidence-interval limits from the 1xx `ci` family and feed them through a shared engine, so only the supplied limits differ between methods. See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `explcall`

```{eval-rst}
.. autofunction:: binomcikit.expl.cc_all.explcall
```

**In plain words** — the per-*p* **expected-length curve** for all continuity-corrected interval methods — the raw `(hp, ew)` values behind the expected-length plots

**The maths** — Same expected-length quantity as `length*`, but returned for every simulated *p* rather than summarised.

**Example**

```python
import binomcikit as bk
bk.explcall(20, 0.05, 0.02, 1, 1, seed=0)
```

**R source** — [`R/321.Expec_Leng_CC_All.R` (line 578)](https://github.com/RajeswaranV/proportion/blob/master/R/321.Expec_Leng_CC_All.R#L578), function `explCAll`

```r
explCAll<-function(n,alp,c,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if (c<=0 || c>(1/(2*n)) || length(c)>1) stop("'c' has to be positive and less than or equal to 1/(2*n)")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

  #### Calling functions and creating df
  df.1    = gexplCWD(n,alp,c,a,b)
  df.2    = gexplCSC(n,alp,c,a,b)
  df.3    = gexplCAS(n,alp,c,a,b)
  df.4    = gexplCLT(n,alp,c,a,b)
  df.5    = gexplCTW(n,alp,c,a,b)

  df.new=  rbind(df.1,df.2,df.3,df.4,df.5)
  return(df.new)
}
```

**What the R code does** — The R function returns the expected length at each simulated *p* (for plotting).

**Python source** — `binomcikit.expl.cc_all.explcall`

```python
def explcall(n, alp, c, a, b, seed=None):
    """Expected-length curves for all five CC methods (R explCAll)."""
    _validate_cc(n, alp, c, a, b)
    hp = _beta_hp(a, b, seed)
    curves = []
    for name, (fn, lo, hi) in _CC.items():
        df = fn(n, alp, c)
        lengths = df[hi].to_numpy() - df[lo].to_numpy()
        curves.append(_expl_curve(n, lengths, hp, name))
    return pd.concat(curves, ignore_index=True)

```

**What the Python code does** — The Python port reuses the shared `_expl_curve` engine, returning a long `(hp, ew, method)` frame.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthcall`

```{eval-rst}
.. autofunction:: binomcikit.expl.cc_all.lengthcall
```

**In plain words** — the **expected length** of all continuity-corrected interval methods — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthcall(20, 0.05, 0.02, 1, 1, seed=0)
```

**R source** — [`R/321.Expec_Leng_CC_All.R` (line 543)](https://github.com/RajeswaranV/proportion/blob/master/R/321.Expec_Leng_CC_All.R#L543), function `lengthCAll`

```r
lengthCAll<-function(n,alp,c,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if (c<=0 || c>(1/(2*n)) || length(c)>1) stop("'c' has to be positive and less than or equal to 1/(2*n)")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

  #### Calling functions and creating df

  df1    = lengthCWD(n,alp,c,a,b)
  df2    = lengthCSC(n,alp,c,a,b)
  df3    = lengthCAS(n,alp,c,a,b)
  df4    = lengthCLT(n,alp,c,a,b)
  df5    = lengthCTW(n,alp,c,a,b)

  df1$method = "CC-Wald"
  df2$method = "CC-Score"
  df3$method = "CC-ArcSine"
  df4$method = "CC-Logit-Wald"
  df5$method = "CC-Wald-T"

  Final.df= rbind(df1,df2,df3,df4,df5)

  return(Final.df)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.cc_all.lengthcall`

```python
def lengthcall(n, alp, c, a, b, seed=None):
    """Expected-length summary for all five CC methods (R lengthCAll)."""
    _validate_cc(n, alp, c, a, b)
    rows = []
    for name in _CC:
        row = _cc_length(name, n, alp, c, a, b, seed).iloc[0].to_dict()
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

## `lengthcas`

```{eval-rst}
.. autofunction:: binomcikit.expl.cc_all.lengthcas
```

**In plain words** — the **expected length** of the continuity-corrected ArcSine (variance-stabilised) interval — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthcas(20, 0.05, 0.02, 1, 1, seed=0)
```

**R source** — [`R/321.Expec_Leng_CC_All.R` (line 226)](https://github.com/RajeswaranV/proportion/blob/master/R/321.Expec_Leng_CC_All.R#L226), function `lengthCAS`

```r
lengthCAS<-function(n,alp,c,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

####INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
pCA=0
qCA=0
seCA=0
LCA=0
UCA=0
s=5000
LECA=0 								#LENGTH OF INTERVAL

ewiCA=matrix(0,k,s)						#sum of length quantity in sum
ewCA=0									#sum of length
###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#ARC-SINE METHOD
for(i in 1:k)
{
pCA[i]=x[i]/n
qCA[i]=1-pCA[i]
seCA[i]=cv/sqrt(4*n)
LCA[i]=(sin(asin(sqrt(pCA[i]))-seCA[i]-c))^2
UCA[i]=(sin(asin(sqrt(pCA[i]))+seCA[i]+c))^2
if(LCA[i]<0) LCA[i]=0
if(UCA[i]>1) UCA[i]=1
LECA[i]=UCA[i]-LCA[i]
}
#sumLECA=sum(LECA)
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
  for(i in 1:k)
  {
    ewiCA[i,j]=LECA[i]*stats::dbinom(i-1, n,hp[j])
  }
  ewCA[j]=sum(ewiCA[,j])						#Expected Length
}

sumLen=sum(LECA)
explMean=mean(ewCA)
explSD=stats::sd(ewCA)
explMax=max(ewCA)
explLL=explMean-(explSD)
explUL=explMean+(explSD)
df.length=data.frame(sumLen,explMean,explSD,explMax,explLL,explUL)
return(df.length)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.cc_all.lengthcas`

```python
def lengthcas(n, alp, c, a, b, seed=None):
    """Expected length of the continuity-corrected ArcSine interval (R lengthCAS)."""
    _validate_cc(n, alp, c, a, b)
    return _cc_length("ArcSine", n, alp, c, a, b, seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthclt`

```{eval-rst}
.. autofunction:: binomcikit.expl.cc_all.lengthclt
```

**In plain words** — the **expected length** of the continuity-corrected Logit-Wald interval — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthclt(20, 0.05, 0.02, 1, 1, seed=0)
```

**R source** — [`R/321.Expec_Leng_CC_All.R` (line 321)](https://github.com/RajeswaranV/proportion/blob/master/R/321.Expec_Leng_CC_All.R#L321), function `lengthCLT`

```r
lengthCLT<-function(n,alp,c,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

####INPUT n
x=0:n
k=n+1
								#sum of length
#INITIALIZATIONS
pCLT=0
qCLT=0
seCLT=0
lgit=0
LCLT=0
UCLT=0
s=5000
LECLT=0 								#LENGTH OF INTERVAL

ewiCLT=matrix(0,k,s)						#sum of length quantity in sum
ewCLT=0									#sum of length
###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#LOGIT-WALD METHOD
pCLT[1]=0
qCLT[1]=1
LCLT[1] = 0
UCLT[1] = 1-((alp/2)^(1/n))

pCLT[k]=1
qCLT[k]=0
LCLT[k]= (alp/2)^(1/n)
UCLT[k]=1

lgiti=function(t) exp(t)/(1+exp(t))	#LOGIT INVERSE
for(j in 1:(k-2))
{
pCLT[j+1]=x[j+1]/n
qCLT[j+1]=1-pCLT[j+1]
lgit[j+1]=log(pCLT[j+1]/qCLT[j+1])
seCLT[j+1]=sqrt(pCLT[j+1]*qCLT[j+1]*n)
LCLT[j+1]=lgiti(lgit[j+1]-(cv/seCLT[j+1])-c)
UCLT[j+1]=lgiti(lgit[j+1]+(cv/seCLT[j+1])+c)
}
for(i in 1:k)
{
if(LCLT[i]<0) LCLT[i]=0
if(UCLT[i]>1) UCLT[i]=1
LECLT[i]=UCLT[i]-LCLT[i]
}
#sumLECLT=sum(LECLT)
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
  for(i in 1:k)
  {
    ewiCLT[i,j]=LECLT[i]*stats::dbinom(i-1, n,hp[j])
  }
  ewCLT[j]=sum(ewiCLT[,j])						#Expected Length
}

sumLen=sum(LECLT)
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.cc_all.lengthclt`

```python
def lengthclt(n, alp, c, a, b, seed=None):
    """Expected length of the continuity-corrected Logit-Wald interval (R lengthCLT)."""
    _validate_cc(n, alp, c, a, b)
    return _cc_length("Logit-Wald", n, alp, c, a, b, seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthcsc`

```{eval-rst}
.. autofunction:: binomcikit.expl.cc_all.lengthcsc
```

**In plain words** — the **expected length** of the continuity-corrected Score / Wilson interval — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthcsc(20, 0.05, 0.02, 1, 1, seed=0)
```

**R source** — [`R/321.Expec_Leng_CC_All.R` (line 127)](https://github.com/RajeswaranV/proportion/blob/master/R/321.Expec_Leng_CC_All.R#L127), function `lengthCSC`

```r
lengthCSC<-function(n,alp,c,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

####INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
pCS=0
qCS=0
seCS_L=0
seCS_U=0
LCS=0
UCS=0
s=5000
LECS=0 								#LENGTH OF INTERVAL

ewiCS=matrix(0,k,s)						#sum of length quantity in sum
ewCS=0									#sum of length
###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
cv1=(cv^2)/(2*n)
cv2= cv/(2*n)

#SCORE (WILSON) METHOD
for(i in 1:k)
{
pCS[i]=x[i]/n
qCS[i]=1-pCS[i]
seCS_L[i]=sqrt((cv^2)-(4*n*(c+c^2))+(4*n*pCS[i]*(1-pCS[i]+(2*c))))	#Sq. root term of LL
seCS_U[i]=sqrt((cv^2)+(4*n*(c-c^2))+(4*n*pCS[i]*(1-pCS[i]-(2*c))))	#Sq. root term of LL
LCS[i]=(n/(n+(cv)^2))*((pCS[i]-c+cv1)-(cv2*seCS_L[i]))
UCS[i]=(n/(n+(cv)^2))*((pCS[i]+c+cv1)+(cv2*seCS_U[i]))
if(LCS[i]<0) LCS[i]=0
if(UCS[i]>1) UCS[i]=1
LECS[i]=UCS[i]-LCS[i]
}
#sumLECS=sum(LECS)
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
  for(i in 1:k)
  {
    ewiCS[i,j]=LECS[i]*stats::dbinom(i-1, n,hp[j])
  }
  ewCS[j]=sum(ewiCS[,j])						#Expected Length
}

sumLen=sum(LECS)
explMean=mean(ewCS)
explSD=stats::sd(ewCS)
explMax=max(ewCS)
explLL=explMean-(explSD)
explUL=explMean+(explSD)
df.length=data.frame(sumLen,explMean,explSD,explMax,explLL,explUL)
return(df.length)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.cc_all.lengthcsc`

```python
def lengthcsc(n, alp, c, a, b, seed=None):
    """Expected length of the continuity-corrected Score interval (R lengthCSC)."""
    _validate_cc(n, alp, c, a, b)
    return _cc_length("Score", n, alp, c, a, b, seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthctw`

```{eval-rst}
.. autofunction:: binomcikit.expl.cc_all.lengthctw
```

**In plain words** — the **expected length** of the continuity-corrected Wald-T interval — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthctw(20, 0.05, 0.02, 1, 1, seed=0)
```

**R source** — [`R/321.Expec_Leng_CC_All.R` (line 435)](https://github.com/RajeswaranV/proportion/blob/master/R/321.Expec_Leng_CC_All.R#L435), function `lengthCTW`

```r
lengthCTW<-function(n,alp,c,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

####INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
pCTW=0
qCTW=0
seCTW=0
LCTW=0
UCTW=0
DOF=0
cv=0
s=5000
LECTW=0 								#LENGTH OF INTERVAL

ewiCTW=matrix(0,k,s)						#sum of length quantity in sum
ewCTW=0									#sum of length
#MODIFIED_t-WALD METHOD
for(i in 1:k)
{
if(x[i]==0||x[i]==n)
{
pCTW[i]=(x[i]+2)/(n+4)
qCTW[i]=1-pCTW[i]
}else
{
pCTW[i]=x[i]/n
qCTW[i]=1-pCTW[i]
}
f1=function(p,n) p*(1-p)/n
f2=function(p,n) (p*(1-p)/(n^3))+(p+((6*n)-7)*(p^2)+(4*(n-1)*(n-3)*(p^3))-(2*(n-1)*((2*n)-3)*(p^4)))/(n^5)-(2*(p+((2*n)-3)*(p^2)-2*(n-1)*(p^3)))/(n^4)
DOF[i]=2*((f1(pCTW[i],n))^2)/f2(pCTW[i],n)
cv[i]=stats::qt(1-(alp/2), df=DOF[i])
seCTW[i]=cv[i]*sqrt(f1(pCTW[i],n))
LCTW[i]=pCTW[i]-(seCTW[i]+c)
UCTW[i]=pCTW[i]+(seCTW[i]+c)
if(LCTW[i]<0) LCTW[i]=0
if(UCTW[i]>1) UCTW[i]=1
LECTW[i]=UCTW[i]-LCTW[i]
}
#sumLECTW=sum(LECTW)
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
  for(i in 1:k)
  {
    ewiCTW[i,j]=LECTW[i]*stats::dbinom(i-1, n,hp[j])
  }
  ewCTW[j]=sum(ewiCTW[,j])						#Expected Length
}

sumLen=sum(LECTW)
explMean=mean(ewCTW)
explSD=stats::sd(ewCTW)
explMax=max(ewCTW)
explLL=explMean-(explSD)
explUL=explMean+(explSD)
df.length=data.frame(sumLen,explMean,explSD,explMax,explLL,explUL)
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.cc_all.lengthctw`

```python
def lengthctw(n, alp, c, a, b, seed=None):
    """Expected length of the continuity-corrected Wald-T interval (R lengthCTW)."""
    _validate_cc(n, alp, c, a, b)
    return _cc_length("Wald-T", n, alp, c, a, b, seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `lengthcwd`

```{eval-rst}
.. autofunction:: binomcikit.expl.cc_all.lengthcwd
```

**In plain words** — the **expected length** of the continuity-corrected Wald (normal-approximation) interval — the average interval width, over hypothetical *p* drawn from a `Beta(a, b)` prior

**The maths** — Expected length $= \sum_x (U_x-L_x)\binom{n}{x}p^x(1-p)^{n-x}$, summarised by `sumLen`, `explMean`, `explSD`, `explMax` and the $\pm\text{SD}$ band `explLL`/`explUL`.

**Example**

```python
import binomcikit as bk
bk.lengthcwd(20, 0.05, 0.02, 1, 1, seed=0)
```

**R source** — [`R/321.Expec_Leng_CC_All.R` (line 33)](https://github.com/RajeswaranV/proportion/blob/master/R/321.Expec_Leng_CC_All.R#L33), function `lengthCWD`

```r
lengthCWD<-function(n,alp,c,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")

####INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
pCW=0
qCW=0
seCW=0
LCW=0
UCW=0
s=5000
LECW=0 								#LENGTH OF INTERVAL

ewiCW=matrix(0,k,s)						#sum of length quantity in sum
ewCW=0									#sum of length
###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#WALD METHOD
for(i in 1:k)
{
pCW[i]=x[i]/n
qCW[i]=1-pCW[i]
seCW[i]=sqrt(pCW[i]*qCW[i]/n)
LCW[i]=pCW[i]-((cv*seCW[i])+c)
UCW[i]=pCW[i]+((cv*seCW[i])+c)
if(LCW[i]<0) LCW[i]=0
if(UCW[i]>1) UCW[i]=1
LECW[i]=UCW[i]-LCW[i]
}
#sumLECW=sum(LECW)
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
  for(i in 1:k)
  {
    ewiCW[i,j]=LECW[i]*stats::dbinom(i-1, n,hp[j])
  }
  ewCW[j]=sum(ewiCW[,j])						#Expected Length
}

sumLen=sum(LECW)
explMean=mean(ewCW)
explSD=stats::sd(ewCW)
explMax=max(ewCW)
explLL=explMean-(explSD)
explUL=explMean+(explSD)
df.length=data.frame(sumLen,explMean,explSD,explMax,explLL,explUL)
return(df.length)
}
```

**What the R code does** — The R function forms the per-`x` interval widths, averages them over 5000 `Beta(a, b)` draws, and returns the length summary.

**Python source** — `binomcikit.expl.cc_all.lengthcwd`

```python
def lengthcwd(n, alp, c, a, b, seed=None):
    """Expected length of the continuity-corrected Wald interval (R lengthCWD)."""
    _validate_cc(n, alp, c, a, b)
    return _cc_length("Wald", n, alp, c, a, b, seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_expl_series` engine, returning the same summary (`explSD` uses `ddof=1` to match R's `sd`).

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

