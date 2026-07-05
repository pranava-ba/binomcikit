<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `err.adj_all`

```{eval-rst}
.. module:: binomcikit.err.adj_all
```

This module computes **error and failure** — for a null proportion `phi` and threshold `f`, the increase in nominal error, the long-term power, and a pass/fail verdict for each interval, for the **adjusted** (pseudo-count `x+h`, `n+2h`) interval methods. These functions reuse the confidence-interval limits from the 1xx `ci` family and feed them through a shared engine, so only the supplied limits differ between methods. See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `erraall`

```{eval-rst}
.. autofunction:: binomcikit.err.adj_all.erraall
```

**In plain words** — the **error and failure** summary of all adjusted interval methods for a null proportion `phi` and threshold `f` — the increase in nominal error (`delalp`), long-term power (`theta`) and a pass/fail verdict

**The maths** — `delalp` $=100(\alpha-\sum_{x:\,\phi\notin[L_x,U_x]}\binom{n}{x}\phi^x(1-\phi)^{n-x})$; `theta` is the % of `x` excluding `phi`; `Fail_Pass` is *failure* iff `delalp < f`.

**Example**

```python
import binomcikit as bk
bk.erraall(20, 0.05, 2, 0.5, -2)
```

**R source** — [`R/511.Error-Failure_LimitBased_ADJ_All.R` (line 487)](https://github.com/RajeswaranV/proportion/blob/master/R/511.Error-Failure_LimitBased_ADJ_All.R#L487), function `errAAll`

```r
errAAll<-function(n,alp,h,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h) >1|| h<0  || !(h%%1 ==0)) stop("'h' has to be an integer greater than or equal to 0")
  if (phi>1 || phi<0) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")) stop("'f' has to be numeric value")
  #### Calling functions and creating df
  df.1    = errAWD(n,alp,h,phi,f)
  df.2    = errASC(n,alp,h,phi,f)
  df.3    = errAAS(n,alp,h,phi,f)
  df.4    = errALT(n,alp,h,phi,f)
  df.5    = errATW(n,alp,h,phi,f)
  df.6    = errALR(n,alp,h,phi,f)

  df.1$method = as.factor("Adj-Wald")
  df.2$method = as.factor("Adj-Score")
  df.3$method = as.factor("Adj-ArcSine")
  df.4$method = as.factor("Adj-Logit-Wald")
  df.5$method = as.factor("Adj-Wald-T")
  df.6$method = as.factor("Adj-Likelihood")

  df.new=  rbind(df.1,df.2,df.3,df.4,df.5,df.6)
  return(df.new)

}
```

**What the R code does** — The R function reads the interval limits, sums the binomial mass at the `x` that exclude `phi`, and returns `delalp`, `theta`, `Fail_Pass`.

**Python source** — `binomcikit.err.adj_all.erraall`

```python
def erraall(n, alp, h, phi, f):
    """Error/failure for all six adjusted methods (R errAAll)."""
    _validate_adj(n, alp, h, phi, f)
    frames = []
    for name in _ADJ:
        d = _adj(name, n, alp, h, phi, f)
        d['method'] = name
        frames.append(d)
    return pd.concat(frames, ignore_index=True)[
        ['method', 'delalp', 'theta', 'Fail_Pass']]

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_error` engine; matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `erraas`

```{eval-rst}
.. autofunction:: binomcikit.err.adj_all.erraas
```

**In plain words** — the **error and failure** summary of the adjusted ArcSine (variance-stabilised) interval for a null proportion `phi` and threshold `f` — the increase in nominal error (`delalp`), long-term power (`theta`) and a pass/fail verdict

**The maths** — `delalp` $=100(\alpha-\sum_{x:\,\phi\notin[L_x,U_x]}\binom{n}{x}\phi^x(1-\phi)^{n-x})$; `theta` is the % of `x` excluding `phi`; `Fail_Pass` is *failure* iff `delalp < f`.

**Example**

```python
import binomcikit as bk
bk.erraas(20, 0.05, 2, 0.5, -2)
```

**R source** — [`R/511.Error-Failure_LimitBased_ADJ_All.R` (line 180)](https://github.com/RajeswaranV/proportion/blob/master/R/511.Error-Failure_LimitBased_ADJ_All.R#L180), function `errAAS`

```r
errAAS<-function(n,alp,h,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || h<0  ) stop("'h' has to be greater than or equal to 0")
  if (phi>1 || phi<0) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")) stop("'f' has to be numeric value")

####INPUT
x=0:n
k=n+1
y=x+h
m=n+(2*h)
####INITIALIZATIONS
pA=0
qA=0
seA=0
LAAS=0
UAAS=0

cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#ARC-SINE METHOD
for(i in 1:k)
{
pA[i]=y[i]/m
qA[i]=1-pA[i]
seA[i]=cv/sqrt(4*m)
LAAS[i]= max((sin(asin(sqrt(pA[i]))-seA[i]))^2,0)
UAAS[i]= min((sin(asin(sqrt(pA[i]))+seA[i]))^2,1)
}
#####Finding Error, Failure
alpstarAAS=0
thetactr=0
for(m in 1:k)
{
if(phi > UAAS[m] || phi<LAAS[m])
{
thetactr=thetactr+1
alpstarAAS[m]=stats::dbinom(x[m],n,phi)
} else alpstarAAS[m] = 0
}
delalpAAS=round((alp-sum(alpstarAAS))*100,2)
theta=round(100*thetactr/(n+1),2)
if(delalpAAS < f)Fail_Pass="failure" else Fail_Pass="success"
return(data.frame(delalp=delalpAAS,theta,Fail_Pass))
}
```

**What the R code does** — The R function reads the interval limits, sums the binomial mass at the `x` that exclude `phi`, and returns `delalp`, `theta`, `Fail_Pass`.

**Python source** — `binomcikit.err.adj_all.erraas`

```python
def erraas(n, alp, h, phi, f):
    """Error/failure of the adjusted ArcSine interval (R errAAS)."""
    _validate_adj(n, alp, h, phi, f)
    return _adj("ArcSine", n, alp, h, phi, f)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_error` engine; matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `erralr`

```{eval-rst}
.. autofunction:: binomcikit.err.adj_all.erralr
```

**In plain words** — the **error and failure** summary of the adjusted Likelihood-Ratio interval for a null proportion `phi` and threshold `f` — the increase in nominal error (`delalp`), long-term power (`theta`) and a pass/fail verdict

**The maths** — `delalp` $=100(\alpha-\sum_{x:\,\phi\notin[L_x,U_x]}\binom{n}{x}\phi^x(1-\phi)^{n-x})$; `theta` is the % of `x` excluding `phi`; `Fail_Pass` is *failure* iff `delalp < f`.

**Example**

```python
import binomcikit as bk
bk.erralr(20, 0.05, 2, 0.5, -2)
```

**R source** — [`R/511.Error-Failure_LimitBased_ADJ_All.R` (line 255)](https://github.com/RajeswaranV/proportion/blob/master/R/511.Error-Failure_LimitBased_ADJ_All.R#L255), function `errALR`

```r
errALR<-function(n,alp,h,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h) >1|| h<0  || !(h%%1 ==0)) stop("'h' has to be an integer greater than or equal to 0")
  if (phi>1 || phi<0) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")) stop("'f' has to be numeric value")

####INPUT n
y=0:n
y1=y+h
k=n+1
n1=n+(2*h)
####INITIALIZATIONS
mle=0
cutoff=0
LALR=0
UALR=0

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
LALR[i]=max(stats::optimize(loglik.optim, c(0,mle[i]))$minimum,0)
UALR[i]=min(stats::optimize(loglik.optim, c(mle[i],1))$minimum,1)
}
#####Finding Error, Failure
alpstarALR=0
thetactr=0
for(m in 1:k)
{
if(phi > UALR[m] || phi<LALR[m])
{
thetactr=thetactr+1
alpstarALR[m]=stats::dbinom(y[m],n,phi)
} else alpstarALR[m] = 0
}
delalpALR=round((alp-sum(alpstarALR))*100,2)
theta=round(100*thetactr/(n+1),2)
if(delalpALR < f)Fail_Pass="failure" else Fail_Pass="success"
return(data.frame(delalp=delalpALR,theta,Fail_Pass))
}
```

**What the R code does** — The R function reads the interval limits, sums the binomial mass at the `x` that exclude `phi`, and returns `delalp`, `theta`, `Fail_Pass`.

**Python source** — `binomcikit.err.adj_all.erralr`

```python
def erralr(n, alp, h, phi, f):
    """Error/failure of the adjusted Likelihood-Ratio interval (R errALR)."""
    _validate_adj(n, alp, h, phi, f)
    return _adj("Likelihood", n, alp, h, phi, f)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_error` engine; matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `erralt`

```{eval-rst}
.. autofunction:: binomcikit.err.adj_all.erralt
```

**In plain words** — the **error and failure** summary of the adjusted Logit-Wald interval for a null proportion `phi` and threshold `f` — the increase in nominal error (`delalp`), long-term power (`theta`) and a pass/fail verdict

**The maths** — `delalp` $=100(\alpha-\sum_{x:\,\phi\notin[L_x,U_x]}\binom{n}{x}\phi^x(1-\phi)^{n-x})$; `theta` is the % of `x` excluding `phi`; `Fail_Pass` is *failure* iff `delalp < f`.

**Example**

```python
import binomcikit as bk
bk.erralt(20, 0.05, 2, 0.5, -2)
```

**R source** — [`R/511.Error-Failure_LimitBased_ADJ_All.R` (line 413)](https://github.com/RajeswaranV/proportion/blob/master/R/511.Error-Failure_LimitBased_ADJ_All.R#L413), function `errALT`

```r
errALT<-function(n,alp,h,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || h<0  ) stop("'h' has to be greater than or equal to 0")
  if (phi>1 || phi<0) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")) stop("'f' has to be numeric value")

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
###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#LOGIT-WALD METHOD
for(i in 1:k)
{
pALT[i]=y[i]/n1
qALT[i]=1-pALT[i]
lgit[i]=log(pALT[i]/qALT[i])
seALT[i]=sqrt(pALT[i]*qALT[i]*n1)
LALT[i]=max(1/(1+exp(-lgit[i]+(cv/seALT[i]))),1)
UALT[i]=min(1/(1+exp(-lgit[i]-(cv/seALT[i]))),1)
}
#####Finding Error, Failure
alpstarALT=0
thetactr=0
for(m in 1:k)
{
if(phi > UALT[m] || phi<LALT[m])
{
thetactr=thetactr+1
alpstarALT[m]=stats::dbinom(x[m],n,phi)
} else alpstarALT[m] = 0
}
delalpALT=round((alp-sum(alpstarALT))*100,2)
theta=round(100*thetactr/(n+1),2)
if(delalpALT < f)Fail_Pass="failure" else Fail_Pass="success"
return(data.frame(delalp=delalpALT,theta,Fail_Pass))
}
```

**What the R code does** — The R function reads the interval limits, sums the binomial mass at the `x` that exclude `phi`, and returns `delalp`, `theta`, `Fail_Pass`.

**Python source** — `binomcikit.err.adj_all.erralt`

```python
def erralt(n, alp, h, phi, f):
    """Error/failure of the adjusted Logit-Wald interval (R errALT)."""
    _validate_adj(n, alp, h, phi, f)
    return _adj("Logit-Wald", n, alp, h, phi, f)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_error` engine; matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `errasc`

```{eval-rst}
.. autofunction:: binomcikit.err.adj_all.errasc
```

**In plain words** — the **error and failure** summary of the adjusted Score / Wilson interval for a null proportion `phi` and threshold `f` — the increase in nominal error (`delalp`), long-term power (`theta`) and a pass/fail verdict

**The maths** — `delalp` $=100(\alpha-\sum_{x:\,\phi\notin[L_x,U_x]}\binom{n}{x}\phi^x(1-\phi)^{n-x})$; `theta` is the % of `x` excluding `phi`; `Fail_Pass` is *failure* iff `delalp < f`.

**Example**

```python
import binomcikit as bk
bk.errasc(20, 0.05, 2, 0.5, -2)
```

**R source** — [`R/511.Error-Failure_LimitBased_ADJ_All.R` (line 101)](https://github.com/RajeswaranV/proportion/blob/master/R/511.Error-Failure_LimitBased_ADJ_All.R#L101), function `errASC`

```r
errASC<-function(n,alp,h,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || h<0  ) stop("'h' has to be greater than or equal to 0")
  if (phi>1 || phi<0) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")) stop("'f' has to be numeric value")

####INPUT n
x=0:n
k=n+1
y=x+h
n1=n+(2*h)
####INITIALIZATIONS
pAS=0
qAS=0
seAS=0
LASC=0
UASC=0

###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
cv1=(cv^2)/(2*n1)
cv2=(cv/(2*n1))^2

#ASCORE (WILSON) METHOD
for(i in 1:k)
{
pAS[i]=y[i]/n1
qAS[i]=1-pAS[i]
seAS[i]=sqrt((pAS[i]*qAS[i]/n1)+cv2)
LASC[i]=max((n1/(n1+(cv)^2))*((pAS[i]+cv1)-(cv*seAS[i])),0)
UASC[i]=min((n1/(n1+(cv)^2))*((pAS[i]+cv1)+(cv*seAS[i])),1)
}
#####Finding Error, Failure
alpstarAS=0
thetactr=0
for(m in 1:k)
{
if(phi > UASC[m] || phi<LASC[m])
{
thetactr=thetactr+1
alpstarAS[m]=stats::dbinom(x[m],n,phi)
} else alpstarAS[m] = 0
}
delalpAS=round((alp-sum(alpstarAS))*100,2)
theta=round(100*thetactr/(n+1),2)
if(delalpAS < f)Fail_Pass="failure" else Fail_Pass="success"
return(data.frame(delalp=delalpAS,theta,Fail_Pass))
}
```

**What the R code does** — The R function reads the interval limits, sums the binomial mass at the `x` that exclude `phi`, and returns `delalp`, `theta`, `Fail_Pass`.

**Python source** — `binomcikit.err.adj_all.errasc`

```python
def errasc(n, alp, h, phi, f):
    """Error/failure of the adjusted Score interval (R errASC)."""
    _validate_adj(n, alp, h, phi, f)
    return _adj("Score", n, alp, h, phi, f)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_error` engine; matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `erratw`

```{eval-rst}
.. autofunction:: binomcikit.err.adj_all.erratw
```

**In plain words** — the **error and failure** summary of the adjusted Wald-T interval for a null proportion `phi` and threshold `f` — the increase in nominal error (`delalp`), long-term power (`theta`) and a pass/fail verdict

**The maths** — `delalp` $=100(\alpha-\sum_{x:\,\phi\notin[L_x,U_x]}\binom{n}{x}\phi^x(1-\phi)^{n-x})$; `theta` is the % of `x` excluding `phi`; `Fail_Pass` is *failure* iff `delalp < f`.

**Example**

```python
import binomcikit as bk
bk.erratw(20, 0.05, 2, 0.5, -2)
```

**R source** — [`R/511.Error-Failure_LimitBased_ADJ_All.R` (line 333)](https://github.com/RajeswaranV/proportion/blob/master/R/511.Error-Failure_LimitBased_ADJ_All.R#L333), function `errATW`

```r
errATW<-function(n,alp,h,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || h<0  ) stop("'h' has to be greater than or equal to 0")
  if (phi>1 || phi<0) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")) stop("'f' has to be numeric value")

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
								#Coverage probabilty
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
LATW[i]=max(pATW[i]-(seATW[i]),0)
UATW[i]=min(pATW[i]+(seATW[i]),1)
}
#####Finding Error, Failure
alpstarATW=0
thetactr=0
for(m in 1:k)
{
if(phi > UATW[m] || phi<LATW[m])
{
thetactr=thetactr+1
alpstarATW[m]=stats::dbinom(x[m],n,phi)
} else alpstarATW[m] = 0
}
delalpATW=round((alp-sum(alpstarATW))*100,2)
theta=round(100*thetactr/(n+1),2)
if(delalpATW < f)Fail_Pass="failure" else Fail_Pass="success"
return(data.frame(delalp=delalpATW,theta,Fail_Pass))
}
```

**What the R code does** — The R function reads the interval limits, sums the binomial mass at the `x` that exclude `phi`, and returns `delalp`, `theta`, `Fail_Pass`.

**Python source** — `binomcikit.err.adj_all.erratw`

```python
def erratw(n, alp, h, phi, f):
    """Error/failure of the adjusted Wald-T interval (R errATW)."""
    _validate_adj(n, alp, h, phi, f)
    return _adj("Wald-T", n, alp, h, phi, f)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_error` engine; matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `errawd`

```{eval-rst}
.. autofunction:: binomcikit.err.adj_all.errawd
```

**In plain words** — the **error and failure** summary of the adjusted Wald (normal-approximation) interval for a null proportion `phi` and threshold `f` — the increase in nominal error (`delalp`), long-term power (`theta`) and a pass/fail verdict

**The maths** — `delalp` $=100(\alpha-\sum_{x:\,\phi\notin[L_x,U_x]}\binom{n}{x}\phi^x(1-\phi)^{n-x})$; `theta` is the % of `x` excluding `phi`; `Fail_Pass` is *failure* iff `delalp < f`.

**Example**

```python
import binomcikit as bk
bk.errawd(20, 0.05, 2, 0.5, -2)
```

**R source** — [`R/511.Error-Failure_LimitBased_ADJ_All.R` (line 23)](https://github.com/RajeswaranV/proportion/blob/master/R/511.Error-Failure_LimitBased_ADJ_All.R#L23), function `errAWD`

```r
errAWD<-function(n,alp,h,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || h<0  ) stop("'h' has to be greater than or equal to 0")
  if (phi>1 || phi<0) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")) stop("'f' has to be numeric value")

####INPUT n
x=0:n
k=n+1
y=x+h
n1=n+(2*h)
####INITIALIZATIONS
pAW=0
qAW=0
seAW=0
LAWD=0
UAWD=0


###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#WALD METHOD
for(i in 1:k)
{
pAW[i]=y[i]/n1
qAW[i]=1-pAW[i]
seAW[i]=sqrt(pAW[i]*qAW[i]/n1)
LAWD[i]=max(pAW[i]-(cv*seAW[i]),0)
UAWD[i]=min(pAW[i]+(cv*seAW[i]),1)
}

#####Finding Error, Failure
alpstarAW=0
thetactr=0
for(m in 1:k)
{
if(phi > UAWD[m] || phi<LAWD[m])
{
thetactr=thetactr+1
alpstarAW[m]=stats::dbinom(x[m],n,phi)
} else alpstarAW[m] = 0
}
delalpAW=round((alp-sum(alpstarAW))*100,2)
theta=round(100*thetactr/(n+1),2)
if(delalpAW < f)Fail_Pass="failure" else Fail_Pass="success"
return(data.frame(delalp=delalpAW,theta,Fail_Pass))
}
```

**What the R code does** — The R function reads the interval limits, sums the binomial mass at the `x` that exclude `phi`, and returns `delalp`, `theta`, `Fail_Pass`.

**Python source** — `binomcikit.err.adj_all.errawd`

```python
def errawd(n, alp, h, phi, f):
    """Error/failure of the adjusted Wald interval (R errAWD)."""
    _validate_adj(n, alp, h, phi, f)
    return _adj("Wald", n, alp, h, phi, f)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_error` engine; matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

