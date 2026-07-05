<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `pconf.adj_all`

```{eval-rst}
.. module:: binomcikit.pconf.adj_all
```

This module computes **p-confidence and p-bias** — deterministic (no-simulation) measures of how well each interval's actual confidence matches its nominal level, for the **adjusted** (pseudo-count `x+h`, `n+2h`) interval methods. These functions reuse the confidence-interval limits from the 1xx `ci` family and feed them through a shared engine, so only the supplied limits differ between methods. See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `pcopbiaall`

```{eval-rst}
.. autofunction:: binomcikit.pconf.adj_all.pcopbiaall
```

**In plain words** — the **p-confidence and p-bias** of all adjusted interval methods — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbiaall(20, 0.05, 2)
```

**R source** — [`R/411.p-Confidence_p-Bias_ADJ_All.R` (line 472)](https://github.com/RajeswaranV/proportion/blob/master/R/411.p-Confidence_p-Bias_ADJ_All.R#L472), function `pCOpBIAAll`

```r
pCOpBIAAll<-function(n,alp,h)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h) >1|| h<0  || !(h%%1 ==0)) stop("'h' has to be an integer greater than or equal to 0")

  #### Calling functions and creating df
  WaldpCB.df    = pCOpBIAWD(n,alp,h)
  ArcSinepCB.df = pCOpBIAAS(n,alp,h)
  LRpCB.df      = pCOpBIALR(n,alp,h)
  ScorepCB.df   = pCOpBIASC(n,alp,h)
  WaldLpCB.df   = pCOpBIALT(n,alp,h)
  AdWaldpCB.df  = pCOpBIATW(n,alp,h)

  WaldpCB.df$method    = as.factor("Adj-Wald")
  ArcSinepCB.df$method = as.factor("Adj-ArcSine")
  LRpCB.df$method      = as.factor("Adj-Likelihood")
  WaldLpCB.df$method   = as.factor("Adj-Logit-Wald")
  ScorepCB.df$method   = as.factor("Adj-Score")
  AdWaldpCB.df$method  = as.factor("Adj-Wald-T")

  Final.df= rbind(WaldpCB.df, ArcSinepCB.df, LRpCB.df,ScorepCB.df,WaldLpCB.df,AdWaldpCB.df)

  return(Final.df)
}
```

**What the R code does** — The R function reads the interval limits and evaluates the two tail probabilities for every interior `x`, returning `x1`, `pconf`, `pbias`.

**Python source** — `binomcikit.pconf.adj_all.pcopbiaall`

```python
def pcopbiaall(n, alp, h):
    """p-confidence and p-bias for all six adjusted methods (R pCOpBIAAll)."""
    _validate_adj(n, alp, h)
    frames = []
    for name in _ADJ:
        d = _adj(name, n, alp, h)
        d['method'] = name
        frames.append(d)
    return pd.concat(frames, ignore_index=True)[
        ['method', 'x1', 'pconf', 'pbias']]

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `pcopbiaas`

```{eval-rst}
.. autofunction:: binomcikit.pconf.adj_all.pcopbiaas
```

**In plain words** — the **p-confidence and p-bias** of the adjusted ArcSine (variance-stabilised) interval — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbiaas(20, 0.05, 2)
```

**R source** — [`R/411.p-Confidence_p-Bias_ADJ_All.R` (line 170)](https://github.com/RajeswaranV/proportion/blob/master/R/411.p-Confidence_p-Bias_ADJ_All.R#L170), function `pCOpBIAAS`

```r
pCOpBIAAS<-function(n,alp,h)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if ((class(h) != "integer") & (class(h) != "numeric") || h<0  ) stop("'h' has to be greater than or equal to 0")

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
pcon=0						#p-confidence
pconC=0
pconf=0
pbia1=0					#p-bias
pbias=0
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
}

####p-confidence and p-bias
for(i in 2:(k-1))
{
pcon[i-1]=2*(stats::pbinom(i-1, n, LAA[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LAA[i]))
pconC[i-1]=2*stats::pbinom(i-1, n, UAA[i], lower.tail = TRUE, log.p = FALSE)
pconf[i-1]=1-max(pcon[i-1],pconC[i-1]) 		#p-confidence calculation
pbia1[i-1]=max(pcon[i-1],pconC[i-1])-min(pcon[i-1],pconC[i-1])
pbias[i-1]=as.numeric(max(0,pbia1[i-1]))
}

x1=1:(n-1)
p_C_B=data.frame(x1,pconf,pbias)
return(p_C_B)
}
```

**What the R code does** — The R function reads the interval limits and evaluates the two tail probabilities for every interior `x`, returning `x1`, `pconf`, `pbias`.

**Python source** — `binomcikit.pconf.adj_all.pcopbiaas`

```python
def pcopbiaas(n, alp, h):
    """p-confidence and p-bias of the adjusted ArcSine interval (R pCOpBIAAS)."""
    _validate_adj(n, alp, h)
    return _adj("ArcSine", n, alp, h)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `pcopbialr`

```{eval-rst}
.. autofunction:: binomcikit.pconf.adj_all.pcopbialr
```

**In plain words** — the **p-confidence and p-bias** of the adjusted Likelihood-Ratio interval — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbialr(20, 0.05, 2)
```

**R source** — [`R/411.p-Confidence_p-Bias_ADJ_All.R` (line 398)](https://github.com/RajeswaranV/proportion/blob/master/R/411.p-Confidence_p-Bias_ADJ_All.R#L398), function `pCOpBIALR`

```r
pCOpBIALR<-function(n,alp,h)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h) >1|| h<0  || !(h%%1 ==0)) stop("'h' has to be an integer greater than or equal to 0")

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

pcon=0						#p-confidence
pconC=0
pconf=0
pbia1=0					#p-bias
pbias=0


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
}
####p-confidence and p-bias
for(i in 2:(k-1))
{
pcon[i-1]=2*(stats::pbinom(i-1, n, LAL[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LAL[i]))
pconC[i-1]=2*stats::pbinom(i-1, n, UAL[i], lower.tail = TRUE, log.p = FALSE)
pconf[i-1]=1-max(pcon[i-1],pconC[i-1]) 		#p-confidence calculation
pbia1[i-1]=max(pcon[i-1],pconC[i-1])-min(pcon[i-1],pconC[i-1])
pbias[i-1]=as.numeric(max(0,pbia1[i-1]))
}
x1=1:(n-1)
p_C_B=data.frame(x1,pconf,pbias)
return(p_C_B)
}
```

**What the R code does** — The R function reads the interval limits and evaluates the two tail probabilities for every interior `x`, returning `x1`, `pconf`, `pbias`.

**Python source** — `binomcikit.pconf.adj_all.pcopbialr`

```python
def pcopbialr(n, alp, h):
    """p-confidence and p-bias of the adjusted Likelihood-Ratio interval (R pCOpBIALR)."""
    _validate_adj(n, alp, h)
    return _adj("Likelihood", n, alp, h)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `pcopbialt`

```{eval-rst}
.. autofunction:: binomcikit.pconf.adj_all.pcopbialt
```

**In plain words** — the **p-confidence and p-bias** of the adjusted Logit-Wald interval — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbialt(20, 0.05, 2)
```

**R source** — [`R/411.p-Confidence_p-Bias_ADJ_All.R` (line 244)](https://github.com/RajeswaranV/proportion/blob/master/R/411.p-Confidence_p-Bias_ADJ_All.R#L244), function `pCOpBIALT`

```r
pCOpBIALT<-function(n,alp,h)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if ((class(h) != "integer") & (class(h) != "numeric") || h<0  ) stop("'h' has to be greater than or equal to 0")

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
pcon=0						#p-confidence
pconC=0
pconf=0
pbia1=0					#p-bias
pbias=0
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
}

####p-confidence and p-bias
for(i in 2:(k-1))
{
pcon[i-1]=2*(stats::pbinom(i-1, n, LALT[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LALT[i]))
pconC[i-1]=2*stats::pbinom(i-1, n, UALT[i], lower.tail = TRUE, log.p = FALSE)
pconf[i-1]=1-max(pcon[i-1],pconC[i-1]) 		#p-confidence calculation
pbia1[i-1]=max(pcon[i-1],pconC[i-1])-min(pcon[i-1],pconC[i-1])
pbias[i-1]=as.numeric(max(0,pbia1[i-1]))
}
x1=1:(n-1)
p_C_B=data.frame(x1,pconf,pbias)
return(p_C_B)
}
```

**What the R code does** — The R function reads the interval limits and evaluates the two tail probabilities for every interior `x`, returning `x1`, `pconf`, `pbias`.

**Python source** — `binomcikit.pconf.adj_all.pcopbialt`

```python
def pcopbialt(n, alp, h):
    """p-confidence and p-bias of the adjusted Logit-Wald interval (R pCOpBIALT)."""
    _validate_adj(n, alp, h)
    return _adj("Logit-Wald", n, alp, h)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `pcopbiasc`

```{eval-rst}
.. autofunction:: binomcikit.pconf.adj_all.pcopbiasc
```

**In plain words** — the **p-confidence and p-bias** of the adjusted Score / Wilson interval — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbiasc(20, 0.05, 2)
```

**R source** — [`R/411.p-Confidence_p-Bias_ADJ_All.R` (line 95)](https://github.com/RajeswaranV/proportion/blob/master/R/411.p-Confidence_p-Bias_ADJ_All.R#L95), function `pCOpBIASC`

```r
pCOpBIASC<-function(n,alp,h)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if ((class(h) != "integer") & (class(h) != "numeric") || h<0  ) stop("'h' has to be greater than or equal to 0")

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
pcon=0						#p-confidence
pconC=0
pconf=0
pbia1=0					#p-bias
pbias=0
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
}
####p-confidence and p-bias
for(i in 2:(k-1))
{
pcon[i-1]=2*(stats::pbinom(i-1, n, LAS[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LAS[i]))
pconC[i-1]=2*stats::pbinom(i-1, n, UAS[i], lower.tail = TRUE, log.p = FALSE)
pconf[i-1]=1-max(pcon[i-1],pconC[i-1]) 		#p-confidence calculation
pbia1[i-1]=max(pcon[i-1],pconC[i-1])-min(pcon[i-1],pconC[i-1])
pbias[i-1]=as.numeric(max(0,pbia1[i-1]))
}
x1=1:(n-1)
p_C_B=data.frame(x1,pconf,pbias)
return(p_C_B)
}
```

**What the R code does** — The R function reads the interval limits and evaluates the two tail probabilities for every interior `x`, returning `x1`, `pconf`, `pbias`.

**Python source** — `binomcikit.pconf.adj_all.pcopbiasc`

```python
def pcopbiasc(n, alp, h):
    """p-confidence and p-bias of the adjusted Score interval (R pCOpBIASC)."""
    _validate_adj(n, alp, h)
    return _adj("Score", n, alp, h)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `pcopbiatw`

```{eval-rst}
.. autofunction:: binomcikit.pconf.adj_all.pcopbiatw
```

**In plain words** — the **p-confidence and p-bias** of the adjusted Wald-T interval — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbiatw(20, 0.05, 2)
```

**R source** — [`R/411.p-Confidence_p-Bias_ADJ_All.R` (line 321)](https://github.com/RajeswaranV/proportion/blob/master/R/411.p-Confidence_p-Bias_ADJ_All.R#L321), function `pCOpBIATW`

```r
pCOpBIATW<-function(n,alp,h)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if ((class(h) != "integer") & (class(h) != "numeric") || h<0  ) stop("'h' has to be greater than or equal to 0")

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
pcon=0						#p-confidence
pconC=0
pconf=0
pbia1=0					#p-bias
pbias=0
#MODIFIED_t-WALD METHOD
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
}
####p-confidence and p-bias
for(i in 2:(k-1))
{
pcon[i-1]=2*(stats::pbinom(i-1, n, LATW[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LATW[i]))
pconC[i-1]=2*stats::pbinom(i-1, n, UATW[i], lower.tail = TRUE, log.p = FALSE)
pconf[i-1]=1-max(pcon[i-1],pconC[i-1]) 		#p-confidence calculation
pbia1[i-1]=max(pcon[i-1],pconC[i-1])-min(pcon[i-1],pconC[i-1])
pbias[i-1]=as.numeric(max(0,pbia1[i-1]))
}
x1=1:(n-1)
p_C_B=data.frame(x1,pconf,pbias)
return(p_C_B)
}
```

**What the R code does** — The R function reads the interval limits and evaluates the two tail probabilities for every interior `x`, returning `x1`, `pconf`, `pbias`.

**Python source** — `binomcikit.pconf.adj_all.pcopbiatw`

```python
def pcopbiatw(n, alp, h):
    """p-confidence and p-bias of the adjusted Wald-T interval (R pCOpBIATW)."""
    _validate_adj(n, alp, h)
    return _adj("Wald-T", n, alp, h)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `pcopbiawd`

```{eval-rst}
.. autofunction:: binomcikit.pconf.adj_all.pcopbiawd
```

**In plain words** — the **p-confidence and p-bias** of the adjusted Wald (normal-approximation) interval — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbiawd(20, 0.05, 2)
```

**R source** — [`R/411.p-Confidence_p-Bias_ADJ_All.R` (line 21)](https://github.com/RajeswaranV/proportion/blob/master/R/411.p-Confidence_p-Bias_ADJ_All.R#L21), function `pCOpBIAWD`

```r
pCOpBIAWD<-function(n,alp,h)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if ((class(h) != "integer") & (class(h) != "numeric") || h<0  ) stop("'h' has to be greater than or equal to 0")


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
pcon=0					#p-confidence
pconC=0
pconf=0
pbia1=0					#p-bias
pbias=0
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
}
####p-confidence and p-bias
for(i in 2:(k-1))
{
pcon[i-1]=2*(stats::pbinom(i-1, n, LAW[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LAW[i]))
pconC[i-1]=2*stats::pbinom(i-1, n, UAW[i], lower.tail = TRUE, log.p = FALSE)
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

**Python source** — `binomcikit.pconf.adj_all.pcopbiawd`

```python
def pcopbiawd(n, alp, h):
    """p-confidence and p-bias of the adjusted Wald interval (R pCOpBIAWD)."""
    _validate_adj(n, alp, h)
    return _adj("Wald", n, alp, h)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

