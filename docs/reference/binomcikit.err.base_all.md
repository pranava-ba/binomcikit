<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `err.base_all`

```{eval-rst}
.. module:: binomcikit.err.base_all
```

This module computes **error and failure** — for a null proportion `phi` and threshold `f`, the increase in nominal error, the long-term power, and a pass/fail verdict for each interval, for the **base** interval methods. These functions reuse the confidence-interval limits from the 1xx `ci` family and feed them through a shared engine, so only the supplied limits differ between methods. See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `errall`

```{eval-rst}
.. autofunction:: binomcikit.err.base_all.errall
```

**In plain words** — the **error and failure** summary of all interval methods for a null proportion `phi` and threshold `f` — the increase in nominal error (`delalp`), long-term power (`theta`) and a pass/fail verdict

**The maths** — `delalp` $=100(\alpha-\sum_{x:\,\phi\notin[L_x,U_x]}\binom{n}{x}\phi^x(1-\phi)^{n-x})$; `theta` is the % of `x` excluding `phi`; `Fail_Pass` is *failure* iff `delalp < f`.

**Example**

```python
import binomcikit as bk
bk.errall(20, 0.05, 0.5, -2)
```

**R source** — [`R/501.Error-Failure_LimitBased_BASE_All.R` (line 704)](https://github.com/RajeswaranV/proportion/blob/master/R/501.Error-Failure_LimitBased_BASE_All.R#L704), function `errAll`

```r
errAll<-function(n,alp,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0 || length(phi)>1) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")|| length(f)>1) stop("'f' has to be numeric value")

  #### Calling functions and creating df
  df.1    = errWD(n,alp,phi,f)
  df.2    = errSC(n,alp,phi,f)
  df.3    = errAS(n,alp,phi,f)
  df.4    = errLT(n,alp,phi,f)
  df.5    = errTW(n,alp,phi,f)
  df.6    = errLR(n,alp,phi,f)

  df.1$method = as.factor("Wald")
  df.2$method = as.factor("Score")
  df.3$method = as.factor("ArcSine")
  df.4$method = as.factor("Logit-Wald")
  df.5$method = as.factor("Wald-T")
  df.6$method = as.factor("Likelihood")

  df.new=  rbind(df.1,df.2,df.3,df.4,df.5,df.6)
  return(df.new)
}
```

**What the R code does** — The R function reads the interval limits, sums the binomial mass at the `x` that exclude `phi`, and returns `delalp`, `theta`, `Fail_Pass`.

**Python source** — `binomcikit.err.base_all.errall`

```python
def errall(n, alp, phi, f):
    """Error/failure for all six base methods (R errAll)."""
    _validate(n, alp, phi, f)
    frames = []
    for name in _BASE:
        d = _base(name, n, alp, phi, f)
        d['method'] = name
        frames.append(d)
    return pd.concat(frames, ignore_index=True)[
        ['method', 'delalp', 'theta', 'Fail_Pass']]

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_error` engine; matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `erras`

```{eval-rst}
.. autofunction:: binomcikit.err.base_all.erras
```

**In plain words** — the **error and failure** summary of the ArcSine (variance-stabilised) interval for a null proportion `phi` and threshold `f` — the increase in nominal error (`delalp`), long-term power (`theta`) and a pass/fail verdict

**The maths** — `delalp` $=100(\alpha-\sum_{x:\,\phi\notin[L_x,U_x]}\binom{n}{x}\phi^x(1-\phi)^{n-x})$; `theta` is the % of `x` excluding `phi`; `Fail_Pass` is *failure* iff `delalp < f`.

**Example**

```python
import binomcikit as bk
bk.erras(20, 0.05, 0.5, -2)
```

**R source** — [`R/501.Error-Failure_LimitBased_BASE_All.R` (line 170)](https://github.com/RajeswaranV/proportion/blob/master/R/501.Error-Failure_LimitBased_BASE_All.R#L170), function `errAS`

```r
errAS<-function(n,alp,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0 || length(phi)>1) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")|| length(f)>1) stop("'f' has to be numeric value")

####DATA
x=0:n
k=n+1
####INITIALIZATIONS
pA=0
qA=0
seA=0
LAS=0
UAS=0
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#ARC-SINE METHOD
for(i in 1:k)
{
pA[i]=x[i]/n
qA[i]=1-pA[i]
seA[i]=cv/sqrt(4*n)
LAS[i]=max((sin(asin(sqrt(pA[i]))-seA[i]))^2,0)
UAS[i]=min((sin(asin(sqrt(pA[i]))+seA[i]))^2,1)
}
###DELTA_ALPHA, THETA,F
alpstarA=0
thetactr=0
for(m in 1:k)
{
if(phi > UAS[m] || phi<LAS[m])
{
thetactr=thetactr+1
alpstarA[m]=stats::dbinom(x[m],n,phi)
} else alpstarA[m] = 0
}
delalpA=round((alp-sum(alpstarA))*100,2)
theta=round(100*thetactr/(n+1),2)
if(delalpA<f)
Fail_Pass="failure" else Fail_Pass="success"
return(data.frame(delalp=delalpA,theta,Fail_Pass))
}
```

**What the R code does** — The R function reads the interval limits, sums the binomial mass at the `x` that exclude `phi`, and returns `delalp`, `theta`, `Fail_Pass`.

**Python source** — `binomcikit.err.base_all.erras`

```python
def erras(n, alp, phi, f):
    """Error/failure of the ArcSine interval (R errAS)."""
    _validate(n, alp, phi, f)
    return _base("ArcSine", n, alp, phi, f)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_error` engine; matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `errex`

```{eval-rst}
.. autofunction:: binomcikit.err.base_all.errex
```

**In plain words** — the **error and failure** summary of the Exact (Clopper-Pearson / mid-p) interval for a null proportion `phi` and threshold `f` — the increase in nominal error (`delalp`), long-term power (`theta`) and a pass/fail verdict

**The maths** — `delalp` $=100(\alpha-\sum_{x:\,\phi\notin[L_x,U_x]}\binom{n}{x}\phi^x(1-\phi)^{n-x})$; `theta` is the % of `x` excluding `phi`; `Fail_Pass` is *failure* iff `delalp < f`.

**Example**

```python
import binomcikit as bk
bk.errex(20, 0.05, 0.5, -2, 0.5)
```

**R source** — [`R/501.Error-Failure_LimitBased_BASE_All.R` (line 489)](https://github.com/RajeswaranV/proportion/blob/master/R/501.Error-Failure_LimitBased_BASE_All.R#L489), function `errEX`

```r
errEX<-function(n,alp,phi,f,e)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if (missing(e)) stop("'e' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0 || length(phi)>1) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")|| length(f)>1) stop("'f' has to be numeric value")
  if ((class(e) != "integer") & (class(e) != "numeric") || any(e>1) || any(e<0)) stop("'e' has to be between 0 and 1")
  if (length(e)>10) stop("'e' can have only 10 intervals")

  nvar=length(e)

  res <- data.frame()

  for(i in 1:nvar)
  {
    lu=gerrEX501(n,alp,phi,f,e[i])
    res <- rbind(res,lu)
  }
  return(res)
}
```

**What the R code does** — The R function reads the interval limits, sums the binomial mass at the `x` that exclude `phi`, and returns `delalp`, `theta`, `Fail_Pass`.

**Python source** — `binomcikit.err.base_all.errex`

```python
def errex(n, alp, phi, f, e):
    """Error/failure of the Exact interval (R errEX)."""
    _validate(n, alp, phi, f)
    if e is None:
        raise ValueError("'e' is missing")
    df = ciex(n, alp, [e])
    return _error(n, alp, phi, f, df['LEX'], df['UEX'])

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_error` engine; matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `errlr`

```{eval-rst}
.. autofunction:: binomcikit.err.base_all.errlr
```

**In plain words** — the **error and failure** summary of the Likelihood-Ratio interval for a null proportion `phi` and threshold `f` — the increase in nominal error (`delalp`), long-term power (`theta`) and a pass/fail verdict

**The maths** — `delalp` $=100(\alpha-\sum_{x:\,\phi\notin[L_x,U_x]}\binom{n}{x}\phi^x(1-\phi)^{n-x})$; `theta` is the % of `x` excluding `phi`; `Fail_Pass` is *failure* iff `delalp < f`.

**Example**

```python
import binomcikit as bk
bk.errlr(20, 0.05, 0.5, -2)
```

**R source** — [`R/501.Error-Failure_LimitBased_BASE_All.R` (line 408)](https://github.com/RajeswaranV/proportion/blob/master/R/501.Error-Failure_LimitBased_BASE_All.R#L408), function `errLR`

```r
errLR<-function(n,alp,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0 || length(phi)>1) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")|| length(f)>1) stop("'f' has to be numeric value")

####DATA
y=0:n
k=n+1
####INITIALIZATIONS
mle=0
cutoff=0
LLR=0
ULR=0

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
LLR[i]=stats::optimize(loglik.optim, c(0,mle[i]))$minimum
ULR[i]=stats::optimize(loglik.optim, c(mle[i],1))$minimum
}
###DELTA_ALPHA, THETA,F
alpstarL=0
thetactr=0
for(m in 1:k)
{
if(phi > ULR[m] || phi < LLR[m])
{
thetactr=thetactr+1
alpstarL[m]=stats::dbinom(y[m],n,phi)
} else alpstarL[m] = 0
}

delalpL=round((alp-sum(alpstarL))*100,2)
theta=round(100*thetactr/(n+1),2)
if(delalpL<f)
Fail_Pass="failure" else Fail_Pass="success"
return(data.frame(delalp=delalpL,theta,Fail_Pass))
}
```

**What the R code does** — The R function reads the interval limits, sums the binomial mass at the `x` that exclude `phi`, and returns `delalp`, `theta`, `Fail_Pass`.

**Python source** — `binomcikit.err.base_all.errlr`

```python
def errlr(n, alp, phi, f):
    """Error/failure of the Likelihood-Ratio interval (R errLR)."""
    _validate(n, alp, phi, f)
    return _base("Likelihood", n, alp, phi, f)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_error` engine; matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `errlt`

```{eval-rst}
.. autofunction:: binomcikit.err.base_all.errlt
```

**In plain words** — the **error and failure** summary of the Logit-Wald interval for a null proportion `phi` and threshold `f` — the increase in nominal error (`delalp`), long-term power (`theta`) and a pass/fail verdict

**The maths** — `delalp` $=100(\alpha-\sum_{x:\,\phi\notin[L_x,U_x]}\binom{n}{x}\phi^x(1-\phi)^{n-x})$; `theta` is the % of `x` excluding `phi`; `Fail_Pass` is *failure* iff `delalp < f`.

**Example**

```python
import binomcikit as bk
bk.errlt(20, 0.05, 0.5, -2)
```

**R source** — [`R/501.Error-Failure_LimitBased_BASE_All.R` (line 240)](https://github.com/RajeswaranV/proportion/blob/master/R/501.Error-Failure_LimitBased_BASE_All.R#L240), function `errLT`

```r
errLT<-function(n,alp,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0 || length(phi)>1) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")|| length(f)>1) stop("'f' has to be numeric value")

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
}
###DELTA_ALPHA, THETA,F
alpstarLT=0
thetactr=0
for(m in 1:k)
{
if(phi > ULT[m] || phi<LLT[m])
{
thetactr=thetactr+1
alpstarLT[m]=stats::dbinom(x[m],n,phi)
} else alpstarLT[m] = 0
}

delalpLT=round((alp-sum(alpstarLT))*100,2)
theta=round(100*thetactr/(n+1),2)
if(delalpLT<f)
Fail_Pass="failure" else Fail_Pass="success"
return(data.frame(delalp=delalpLT,theta,Fail_Pass))
}
```

**What the R code does** — The R function reads the interval limits, sums the binomial mass at the `x` that exclude `phi`, and returns `delalp`, `theta`, `Fail_Pass`.

**Python source** — `binomcikit.err.base_all.errlt`

```python
def errlt(n, alp, phi, f):
    """Error/failure of the Logit-Wald interval (R errLT)."""
    _validate(n, alp, phi, f)
    return _base("Logit-Wald", n, alp, phi, f)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_error` engine; matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `errsc`

```{eval-rst}
.. autofunction:: binomcikit.err.base_all.errsc
```

**In plain words** — the **error and failure** summary of the Score / Wilson interval for a null proportion `phi` and threshold `f` — the increase in nominal error (`delalp`), long-term power (`theta`) and a pass/fail verdict

**The maths** — `delalp` $=100(\alpha-\sum_{x:\,\phi\notin[L_x,U_x]}\binom{n}{x}\phi^x(1-\phi)^{n-x})$; `theta` is the % of `x` excluding `phi`; `Fail_Pass` is *failure* iff `delalp < f`.

**Example**

```python
import binomcikit as bk
bk.errsc(20, 0.05, 0.5, -2)
```

**R source** — [`R/501.Error-Failure_LimitBased_BASE_All.R` (line 93)](https://github.com/RajeswaranV/proportion/blob/master/R/501.Error-Failure_LimitBased_BASE_All.R#L93), function `errSC`

```r
errSC<-function(n,alp,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0 || length(phi)>1) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")|| length(f)>1) stop("'f' has to be numeric value")

####DATA
x=0:n
k=n+1
####INITIALIZATIONS
pS=0
qS=0
seS=0
LSC=0
USC=0

#SCORE (WILSON) METHOD
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
LSC[i]=max((n/(n+(cv)^2))*((pS[i]+cv1)-(cv*seS[i])),0)
USC[i]=min((n/(n+(cv)^2))*((pS[i]+cv1)+(cv*seS[i])),1)
}
###DELTA_ALPHA, THETA,F
alpstarS=0
thetactr=0
for(m in 1:k)
{
if(phi > USC[m] || phi<LSC[m])
{
thetactr=thetactr+1
alpstarS[m]=stats::dbinom(x[m],n,phi)
} else alpstarS[m] = 0
}

delalpS=round((alp-sum(alpstarS))*100,2)
theta=round(100*thetactr/(n+1),2)
if(delalpS<f)
Fail_Pass="failure" else Fail_Pass="success"
return(data.frame(delalp=delalpS,theta,Fail_Pass))
}
```

**What the R code does** — The R function reads the interval limits, sums the binomial mass at the `x` that exclude `phi`, and returns `delalp`, `theta`, `Fail_Pass`.

**Python source** — `binomcikit.err.base_all.errsc`

```python
def errsc(n, alp, phi, f):
    """Error/failure of the Score interval (R errSC)."""
    _validate(n, alp, phi, f)
    return _base("Score", n, alp, phi, f)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_error` engine; matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `errtw`

```{eval-rst}
.. autofunction:: binomcikit.err.base_all.errtw
```

**In plain words** — the **error and failure** summary of the Wald-T interval for a null proportion `phi` and threshold `f` — the increase in nominal error (`delalp`), long-term power (`theta`) and a pass/fail verdict

**The maths** — `delalp` $=100(\alpha-\sum_{x:\,\phi\notin[L_x,U_x]}\binom{n}{x}\phi^x(1-\phi)^{n-x})$; `theta` is the % of `x` excluding `phi`; `Fail_Pass` is *failure* iff `delalp < f`.

**Example**

```python
import binomcikit as bk
bk.errtw(20, 0.05, 0.5, -2)
```

**R source** — [`R/501.Error-Failure_LimitBased_BASE_All.R` (line 325)](https://github.com/RajeswaranV/proportion/blob/master/R/501.Error-Failure_LimitBased_BASE_All.R#L325), function `errTW`

```r
errTW<-function(n,alp,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0 || length(phi)>1) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")|| length(f)>1) stop("'f' has to be numeric value")

####DATA
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
LTW[i]=max(pTW[i]-(seTW[i]),0)
UTW[i]=min(pTW[i]+(seTW[i]),1)
}
###DELTA_ALPHA, THETA,F
alpstarTW=0
thetactr=0
for(m in 1:k)
{
if(phi > UTW[m] || phi<LTW[m])
{
thetactr=thetactr+1
alpstarTW[m]=stats::dbinom(x[m],n,phi)
} else alpstarTW[m] = 0
}

delalpTW=round((alp-sum(alpstarTW))*100,2)
theta=round(100*thetactr/(n+1),2)
if(delalpTW<f)
Fail_Pass="failure" else Fail_Pass="success"
return(data.frame(delalp=delalpTW,theta,Fail_Pass))
}
```

**What the R code does** — The R function reads the interval limits, sums the binomial mass at the `x` that exclude `phi`, and returns `delalp`, `theta`, `Fail_Pass`.

**Python source** — `binomcikit.err.base_all.errtw`

```python
def errtw(n, alp, phi, f):
    """Error/failure of the Wald-T interval (R errTW)."""
    _validate(n, alp, phi, f)
    return _base("Wald-T", n, alp, phi, f)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_error` engine; matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `errwd`

```{eval-rst}
.. autofunction:: binomcikit.err.base_all.errwd
```

**In plain words** — the **error and failure** summary of the Wald (normal-approximation) interval for a null proportion `phi` and threshold `f` — the increase in nominal error (`delalp`), long-term power (`theta`) and a pass/fail verdict

**The maths** — `delalp` $=100(\alpha-\sum_{x:\,\phi\notin[L_x,U_x]}\binom{n}{x}\phi^x(1-\phi)^{n-x})$; `theta` is the % of `x` excluding `phi`; `Fail_Pass` is *failure* iff `delalp < f`.

**Example**

```python
import binomcikit as bk
bk.errwd(20, 0.05, 0.5, -2)
```

**R source** — [`R/501.Error-Failure_LimitBased_BASE_All.R` (line 22)](https://github.com/RajeswaranV/proportion/blob/master/R/501.Error-Failure_LimitBased_BASE_All.R#L22), function `errWD`

```r
errWD<-function(n,alp,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0 || length(phi)>1) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")|| length(f)>1) stop("'f' has to be numeric value")

####DATA
x=0:n
k=n+1
####INITIALIZATIONS
pW=0
qW=0
seW=0
LWD=0
UWD=0
alpstarW=0
thetactr=0

###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#WALD METHOD
for(i in 1:k)
{
pW[i]=x[i]/n
qW[i]=1-(x[i]/n)
seW[i]=sqrt(pW[i]*qW[i]/n)
LWD[i]=max(pW[i]-(cv*seW[i]),0)
UWD[i]=min(pW[i]+(cv*seW[i]),1)
}
for(m in 1:k)
{
if(phi > UWD[m] || phi<LWD[m])
{
thetactr=thetactr+1
alpstarW[m]=stats::dbinom(x[m],n,phi)
} else alpstarW[m] = 0
}
delalpW=round((alp-sum(alpstarW))*100,2)
theta=round(100*thetactr/(n+1),2)
if(delalpW<f)
Fail_Pass="failure" else Fail_Pass="success"
data.frame(delalp=delalpW,theta,Fail_Pass)
}
```

**What the R code does** — The R function reads the interval limits, sums the binomial mass at the `x` that exclude `phi`, and returns `delalp`, `theta`, `Fail_Pass`.

**Python source** — `binomcikit.err.base_all.errwd`

```python
def errwd(n, alp, phi, f):
    """Error/failure of the Wald interval (R errWD)."""
    _validate(n, alp, phi, f)
    return _base("Wald", n, alp, phi, f)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_error` engine; matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

