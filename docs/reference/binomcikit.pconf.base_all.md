<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `pconf.base_all`

```{eval-rst}
.. module:: binomcikit.pconf.base_all
```

This module computes **p-confidence and p-bias** — deterministic (no-simulation) measures of how well each interval's actual confidence matches its nominal level, for the **base** interval methods. These functions reuse the confidence-interval limits from the 1xx `ci` family and feed them through a shared engine, so only the supplied limits differ between methods. See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `pcopbiall`

```{eval-rst}
.. autofunction:: binomcikit.pconf.base_all.pcopbiall
```

**In plain words** — the **p-confidence and p-bias** of all interval methods — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbiall(20, 0.05)
```

**R source** — [`R/401.p-Confidence_p-Bias_BASE_All.R` (line 684)](https://github.com/RajeswaranV/proportion/blob/master/R/401.p-Confidence_p-Bias_BASE_All.R#L684), function `pCOpBIAll`

```r
pCOpBIAll<-function(n,alp)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")

  #### Calling functions and creating df

  df1 = pCOpBIWD(n,alp)
  df2 = pCOpBISC(n,alp)
  df3 = pCOpBIAS(n,alp)
  df4 = pCOpBILT(n,alp)
  df5 = pCOpBITW(n,alp)
  df6 = pCOpBILR(n,alp)

  df1$method = as.factor("Wald")
  df2$method = as.factor("Score")
  df3$method = as.factor("ArcSine")
  df4$method = as.factor("Logit-Wald")
  df5$method = as.factor("Wald-T")
  df6$method = as.factor("Likelihood")

  Final.df= rbind(df1,df2,df3,df4,df5,df6)

  return(Final.df)
}
```

**What the R code does** — The R function reads the interval limits and evaluates the two tail probabilities for every interior `x`, returning `x1`, `pconf`, `pbias`.

**Python source** — `binomcikit.pconf.base_all.pcopbiall`

```python
def pcopbiall(n, alp):
    """p-confidence and p-bias for all six base methods (R pCOpBIAll)."""
    _validate(n, alp)
    frames = []
    for name in _BASE:
        d = _base(name, n, alp)
        d['method'] = name
        frames.append(d)
    return pd.concat(frames, ignore_index=True)[
        ['method', 'x1', 'pconf', 'pbias']]

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `pcopbias`

```{eval-rst}
.. autofunction:: binomcikit.pconf.base_all.pcopbias
```

**In plain words** — the **p-confidence and p-bias** of the ArcSine (variance-stabilised) interval — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbias(20, 0.05)
```

**R source** — [`R/401.p-Confidence_p-Bias_BASE_All.R` (line 162)](https://github.com/RajeswaranV/proportion/blob/master/R/401.p-Confidence_p-Bias_BASE_All.R#L162), function `pCOpBIAS`

```r
pCOpBIAS<-function(n,alp)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")

  ####INPUT n
  x=0:n
  k=n+1
  ####INITIALIZATIONS
  pA=0
  qA=0
  seA=0
  LA=0
  UA=0
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
    pA[i]=x[i]/n
    qA[i]=1-pA[i]
    seA[i]=cv/sqrt(4*n)
    LA[i]=(sin(asin(sqrt(pA[i]))-seA[i]))^2
    UA[i]=(sin(asin(sqrt(pA[i]))+seA[i]))^2
    if(LA[i]<0) LA[i]=0
    if(UA[i]>1) UA[i]=1
  }

  ####p-confidence and p-bias
  for(i in 2:(k-1))
  {
    pcon[i-1]=2*(stats::pbinom(i-1, n, LA[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LA[i]))
    pconC[i-1]=2*stats::pbinom(i-1, n, UA[i], lower.tail = TRUE, log.p = FALSE)
    pconf[i-1]=1-max(pcon[i-1],pconC[i-1]) 		#p-confidence calculation
    pbia1[i-1]=max(pcon[i-1],pconC[i-1])-min(pcon[i-1],pconC[i-1])
    pbias[i-1]=as.numeric(max(0,pbia1[i-1]))
  }

  x1=1:(n-1)
  p_C_B=data.frame(x1,pconf,pbias)
  # windows()
  # plot(x1,pconf,type="l",xlab="No of successes",ylab="p-Confidence",main="Arc Sine")
  # windows()
  # plot(x1,pbias,type="l",xlab="No of successes",ylab="p-Bias",main="Arc Sine")
  return(p_C_B)
}
```

**What the R code does** — The R function reads the interval limits and evaluates the two tail probabilities for every interior `x`, returning `x1`, `pconf`, `pbias`.

**Python source** — `binomcikit.pconf.base_all.pcopbias`

```python
def pcopbias(n, alp):
    """p-confidence and p-bias of the ArcSine interval (R pCOpBIAS)."""
    _validate(n, alp)
    return _base("ArcSine", n, alp)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `pcopbiex`

```{eval-rst}
.. autofunction:: binomcikit.pconf.base_all.pcopbiex
```

**In plain words** — the **p-confidence and p-bias** of the Exact (Clopper-Pearson / mid-p) interval — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbiex(20, 0.05, 0.5)
```

**R source** — [`R/401.p-Confidence_p-Bias_BASE_All.R` (line 478)](https://github.com/RajeswaranV/proportion/blob/master/R/401.p-Confidence_p-Bias_BASE_All.R#L478), function `pCOpBIEX`

```r
pCOpBIEX<-function(n,alp,e)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(e)) stop("'e' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(e) != "integer") & (class(e) != "numeric") || any(e>1) || any(e<0)) stop("'e' has to be between 0 and 1")
  if (length(e)>10) stop("'e' can have only 10 intervals")

  ####INITIALIZATIONS
  nvar=length(e)

  tdf <- data.frame()

  for(i in 1:nvar)
     {
     slf=slu401(n,alp,e[i])
     tdf <- rbind(tdf,slf)
     }

  res <- data.frame()
  stdf <- data.frame()

  for(i in 1:nvar)
      {
       ep=e[i]
       stdf=subset(tdf, e == ep)
       pcbw=pcb401(n,stdf)
       res <- rbind(res,pcbw)
      }
    return(res)
}
```

**What the R code does** — The R function reads the interval limits and evaluates the two tail probabilities for every interior `x`, returning `x1`, `pconf`, `pbias`.

**Python source** — `binomcikit.pconf.base_all.pcopbiex`

```python
def pcopbiex(n, alp, e):
    """p-confidence and p-bias of the Exact interval (R pCOpBIEX)."""
    _validate(n, alp)
    if e is None:
        raise ValueError("'e' is missing")
    df = ciex(n, alp, [e])
    return _pconf_pbias(n, df['LEX'], df['UEX'])

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `pcopbilr`

```{eval-rst}
.. autofunction:: binomcikit.pconf.base_all.pcopbilr
```

**In plain words** — the **p-confidence and p-bias** of the Likelihood-Ratio interval — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbilr(20, 0.05)
```

**R source** — [`R/401.p-Confidence_p-Bias_BASE_All.R` (line 400)](https://github.com/RajeswaranV/proportion/blob/master/R/401.p-Confidence_p-Bias_BASE_All.R#L400), function `pCOpBILR`

```r
pCOpBILR<-function(n,alp)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")

  ####INPUT n
  y=0:n
  k=n+1
  ####INITIALIZATIONS
  mle=0
  cutoff=0
  LL=0
  UL=0
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
    likelhd = function(p) stats::dbinom(y[i],n,p)
    loglik = function(p) stats::dbinom(y[i],n,p,log=TRUE)
    mle[i]=stats::optimize(likelhd,c(0,1),maximum=TRUE)$maximum
    cutoff[i]=loglik(mle[i])-(cv^2/2)
    loglik.optim=function(p){abs(cutoff[i]-loglik(p))}
    LL[i]=stats::optimize(loglik.optim, c(0,mle[i]))$minimum
    UL[i]=stats::optimize(loglik.optim, c(mle[i],1))$minimum
  }
  ####p-confidence and p-bias
  for(i in 2:(k-1))
  {
    pcon[i-1]=2*(stats::pbinom(i-1, n, LL[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LL[i]))
    pconC[i-1]=2*stats::pbinom(i-1, n, UL[i], lower.tail = TRUE, log.p = FALSE)
    pconf[i-1]=1-max(pcon[i-1],pconC[i-1]) 		#p-confidence calculation
    pbia1[i-1]=max(pcon[i-1],pconC[i-1])-min(pcon[i-1],pconC[i-1])
    pbias[i-1]=as.numeric(max(0,pbia1[i-1]))
  }
  x1=1:(n-1)
  p_C_B=data.frame(x1,pconf,pbias)
  # windows()
  # plot(x1,pconf,type="l",xlab="No of successes",ylab="p-Confidence",main="Likelihood Ratio")
  # windows()
  # plot(x1,pbias,type="l",xlab="No of successes",ylab="p-Bias",main="Likelihood Ratio")
  return(p_C_B)
}
```

**What the R code does** — The R function reads the interval limits and evaluates the two tail probabilities for every interior `x`, returning `x1`, `pconf`, `pbias`.

**Python source** — `binomcikit.pconf.base_all.pcopbilr`

```python
def pcopbilr(n, alp):
    """p-confidence and p-bias of the Likelihood-Ratio interval (R pCOpBILR)."""
    _validate(n, alp)
    return _base("Likelihood", n, alp)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `pcopbilt`

```{eval-rst}
.. autofunction:: binomcikit.pconf.base_all.pcopbilt
```

**In plain words** — the **p-confidence and p-bias** of the Logit-Wald interval — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbilt(20, 0.05)
```

**R source** — [`R/401.p-Confidence_p-Bias_BASE_All.R` (line 234)](https://github.com/RajeswaranV/proportion/blob/master/R/401.p-Confidence_p-Bias_BASE_All.R#L234), function `pCOpBILT`

```r
pCOpBILT<-function(n,alp)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")

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
  pcon=0						#p-confidence
  pconC=0
  pconf=0
  pbia1=0					#p-bias
  pbias=0
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


  ####p-confidence and p-bias
  for(i in 2:(k-1))
  {
    pcon[i-1]=2*(stats::pbinom(i-1, n, LLT[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LLT[i]))
    pconC[i-1]=2*stats::pbinom(i-1, n, ULT[i], lower.tail = TRUE, log.p = FALSE)
    pconf[i-1]=1-max(pcon[i-1],pconC[i-1]) 		#p-confidence calculation
    pbia1[i-1]=max(pcon[i-1],pconC[i-1])-min(pcon[i-1],pconC[i-1])
    pbias[i-1]=as.numeric(max(0,pbia1[i-1]))
  }
  x1=1:(n-1)
  p_C_B=data.frame(x1,pconf,pbias)
  # windows()
  # plot(x1,pconf,type="l",xlab="No of successes",ylab="p-Confidence",main="Logit Wald")
  # windows()
  # plot(x1,pbias,type="l",xlab="No of successes",ylab="p-Bias",main="Logit Wald")
  return(p_C_B)
}
```

**What the R code does** — The R function reads the interval limits and evaluates the two tail probabilities for every interior `x`, returning `x1`, `pconf`, `pbias`.

**Python source** — `binomcikit.pconf.base_all.pcopbilt`

```python
def pcopbilt(n, alp):
    """p-confidence and p-bias of the Logit-Wald interval (R pCOpBILT)."""
    _validate(n, alp)
    return _base("Logit-Wald", n, alp)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `pcopbisc`

```{eval-rst}
.. autofunction:: binomcikit.pconf.base_all.pcopbisc
```

**In plain words** — the **p-confidence and p-bias** of the Score / Wilson interval — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbisc(20, 0.05)
```

**R source** — [`R/401.p-Confidence_p-Bias_BASE_All.R` (line 89)](https://github.com/RajeswaranV/proportion/blob/master/R/401.p-Confidence_p-Bias_BASE_All.R#L89), function `pCOpBISC`

```r
pCOpBISC<-function(n,alp)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")

  ####INPUT n
  x=0:n
  k=n+1
  ####INITIALIZATIONS
  pS=0
  qS=0
  seS=0
  LS=0
  US=0
  pcon=0						#p-confidence
  pconC=0
  pconf=0
  pbia1=0					#p-bias
  pbias=0
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
  }
  ####p-confidence and p-bias
  for(i in 2:(k-1))
  {
    pcon[i-1]=2*(stats::pbinom(i-1, n, LS[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LS[i]))
    pconC[i-1]=2*stats::pbinom(i-1, n, US[i], lower.tail = TRUE, log.p = FALSE)
    pconf[i-1]=1-max(pcon[i-1],pconC[i-1]) 		#p-confidence calculation
    pbia1[i-1]=max(pcon[i-1],pconC[i-1])-min(pcon[i-1],pconC[i-1])
    pbias[i-1]=as.numeric(max(0,pbia1[i-1]))
  }
  x1=1:(n-1)
  p_C_B=data.frame(x1,pconf,pbias)
#   windows()
#   plot(x1,pconf,type="l",xlab="No of successes",ylab="p-Confidence",main="Score")
#   windows()
#   plot(x1,pbias,type="l",xlab="No of successes",ylab="p-Bias",main="Score")
  return(p_C_B)
}
```

**What the R code does** — The R function reads the interval limits and evaluates the two tail probabilities for every interior `x`, returning `x1`, `pconf`, `pbias`.

**Python source** — `binomcikit.pconf.base_all.pcopbisc`

```python
def pcopbisc(n, alp):
    """p-confidence and p-bias of the Score interval (R pCOpBISC)."""
    _validate(n, alp)
    return _base("Score", n, alp)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `pcopbitw`

```{eval-rst}
.. autofunction:: binomcikit.pconf.base_all.pcopbitw
```

**In plain words** — the **p-confidence and p-bias** of the Wald-T interval — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbitw(20, 0.05)
```

**R source** — [`R/401.p-Confidence_p-Bias_BASE_All.R` (line 318)](https://github.com/RajeswaranV/proportion/blob/master/R/401.p-Confidence_p-Bias_BASE_All.R#L318), function `pCOpBITW`

```r
pCOpBITW<-function(n,alp)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")

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
  pcon=0						#p-confidence
  pconC=0
  pconf=0
  pbia1=0					#p-bias
  pbias=0
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
  }
  ####p-confidence and p-bias
  for(i in 2:(k-1))
  {
    pcon[i-1]=2*(stats::pbinom(i-1, n, LTW[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LTW[i]))
    pconC[i-1]=2*stats::pbinom(i-1, n, UTW[i], lower.tail = TRUE, log.p = FALSE)
    pconf[i-1]=1-max(pcon[i-1],pconC[i-1]) 		#p-confidence calculation
    pbia1[i-1]=max(pcon[i-1],pconC[i-1])-min(pcon[i-1],pconC[i-1])
    pbias[i-1]=as.numeric(max(0,pbia1[i-1]))
  }
  x1=1:(n-1)
  p_C_B=data.frame(x1,pconf,pbias)
  # windows()
  # plot(x1,pconf,type="l",xlab="No of successes",ylab="p-Confidence",main="t-Wald")
  # windows()
  # plot(x1,pbias,type="l",,xlab="No of successes",ylab="p-Bias",main="t-Wald")
  return(p_C_B)
}
```

**What the R code does** — The R function reads the interval limits and evaluates the two tail probabilities for every interior `x`, returning `x1`, `pconf`, `pbias`.

**Python source** — `binomcikit.pconf.base_all.pcopbitw`

```python
def pcopbitw(n, alp):
    """p-confidence and p-bias of the Wald-T interval (R pCOpBITW)."""
    _validate(n, alp)
    return _base("Wald-T", n, alp)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `pcopbiwd`

```{eval-rst}
.. autofunction:: binomcikit.pconf.base_all.pcopbiwd
```

**In plain words** — the **p-confidence and p-bias** of the Wald (normal-approximation) interval — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbiwd(20, 0.05)
```

**R source** — [`R/401.p-Confidence_p-Bias_BASE_All.R` (line 19)](https://github.com/RajeswaranV/proportion/blob/master/R/401.p-Confidence_p-Bias_BASE_All.R#L19), function `pCOpBIWD`

```r
pCOpBIWD<-function(n,alp)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")

  ####INPUT n
  x=0:n
  k=n+1
  ####INITIALIZATIONS
  pW=0
  qW=0
  seW=0
  LW=0
  UW=0
  pcon=0						#p-confidence
  pconC=0
  pconf=0
  pbia1=0					#p-bias
  pbias=0
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
  }
  ####p-confidence and p-bias
  for(i in 2:(k-1))
  {
    pcon[i-1]=2*(stats::pbinom(i-1, n, LW[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LW[i]))
    pconC[i-1]=2*stats::pbinom(i-1, n, UW[i], lower.tail = TRUE, log.p = FALSE)
    pconf[i-1]=(1-max(pcon[i-1],pconC[i-1]))*100 		#p-confidence calculation
    pbia1[i-1]=max(pcon[i-1],pconC[i-1])-min(pcon[i-1],pconC[i-1])
    pbias[i-1]=max(0,pbia1[i-1])*100
  }
  x1=1:(n-1)
  p_C_B=data.frame(x1,pconf,pbias)
#   windows()
#   plot(x1,pconf,type="l",xlab="No of successes",ylab="p-Confidence",main="Wald")
#   windows()
#   plot(x1,pbias,type="l",xlab="No of successes",ylab="p-Bias",main="Wald")
  return(p_C_B)
}
```

**What the R code does** — The R function reads the interval limits and evaluates the two tail probabilities for every interior `x`, returning `x1`, `pconf`, `pbias`.

**Python source** — `binomcikit.pconf.base_all.pcopbiwd`

```python
def pcopbiwd(n, alp):
    """p-confidence and p-bias of the Wald interval (R pCOpBIWD)."""
    _validate(n, alp)
    return _base("Wald", n, alp)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

