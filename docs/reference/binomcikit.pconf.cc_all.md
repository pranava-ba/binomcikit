<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `pconf.cc_all`

```{eval-rst}
.. module:: binomcikit.pconf.cc_all
```

This module computes **p-confidence and p-bias** — deterministic (no-simulation) measures of how well each interval's actual confidence matches its nominal level, for the **continuity-corrected** interval methods (five methods; no Likelihood-Ratio). These functions reuse the confidence-interval limits from the 1xx `ci` family and feed them through a shared engine, so only the supplied limits differ between methods. See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `pcopbicall`

```{eval-rst}
.. autofunction:: binomcikit.pconf.cc_all.pcopbicall
```

**In plain words** — the **p-confidence and p-bias** of all continuity-corrected interval methods — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbicall(20, 0.05, 0.02)
```

**R source** — [`R/421.p-Confidence_p-Bias_CC_All.R` (line 407)](https://github.com/RajeswaranV/proportion/blob/master/R/421.p-Confidence_p-Bias_CC_All.R#L407), function `pCOpBICAll`

```r
pCOpBICAll<-function(n,alp,c)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if (c<=0 || c>(1/(2*n)) || length(c)>1) stop("'c' has to be positive and less than or equal to 1/(2*n)")

  #### Calling functions and creating df
  WaldpCB.df    = pCOpBICWD(n,alp,c)
  ArcSinepCB.df = pCOpBICAS(n,alp,c)
  ScorepCB.df   = pCOpBICSC(n,alp,c)
  WaldLpCB.df   = pCOpBICLT(n,alp,c)
  AdWaldpCB.df  = pCOpBICTW(n,alp,c)

  WaldpCB.df$method    = as.factor("CC-Wald")
  ArcSinepCB.df$method = as.factor("CC-ArcSine")
  WaldLpCB.df$method   = as.factor("CC-Logit-Wald")
  ScorepCB.df$method   = as.factor("CC-Score")
  AdWaldpCB.df$method  = as.factor("CC-Wald-T")

  Final.df= rbind(WaldpCB.df, ArcSinepCB.df, ScorepCB.df,WaldLpCB.df,AdWaldpCB.df)

  return(Final.df)
}
```

**What the R code does** — The R function reads the interval limits and evaluates the two tail probabilities for every interior `x`, returning `x1`, `pconf`, `pbias`.

**Python source** — `binomcikit.pconf.cc_all.pcopbicall`

```python
def pcopbicall(n, alp, c):
    """p-confidence and p-bias for all five CC methods (R pCOpBICAll)."""
    _validate_cc(n, alp, c)
    frames = []
    for name in _CC:
        d = _cc(name, n, alp, c)
        d['method'] = name
        frames.append(d)
    return pd.concat(frames, ignore_index=True)[
        ['method', 'x1', 'pconf', 'pbias']]

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `pcopbicas`

```{eval-rst}
.. autofunction:: binomcikit.pconf.cc_all.pcopbicas
```

**In plain words** — the **p-confidence and p-bias** of the continuity-corrected ArcSine (variance-stabilised) interval — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbicas(20, 0.05, 0.02)
```

**R source** — [`R/421.p-Confidence_p-Bias_CC_All.R` (line 167)](https://github.com/RajeswaranV/proportion/blob/master/R/421.p-Confidence_p-Bias_CC_All.R#L167), function `pCOpBICAS`

```r
pCOpBICAS<-function(n,alp,c)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")

####INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
pCA=0
qCA=0
seCA=0
LCA=0
UCA=0
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
pCA[i]=x[i]/n
qCA[i]=1-pCA[i]
seCA[i]=cv/sqrt(4*n)
LCA[i]=(sin(asin(sqrt(pCA[i]))-seCA[i]-c))^2
UCA[i]=(sin(asin(sqrt(pCA[i]))+seCA[i]+c))^2
if(LCA[i]<0) LCA[i]=0
if(UCA[i]>1) UCA[i]=1
}

####p-confidence and p-bias
for(i in 2:(k-1))
{
  pcon[i-1]=2*(stats::pbinom(i-1, n, LCA[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LCA[i]))
  pconC[i-1]=2*stats::pbinom(i-1, n, UCA[i], lower.tail = TRUE, log.p = FALSE)
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

**Python source** — `binomcikit.pconf.cc_all.pcopbicas`

```python
def pcopbicas(n, alp, c):
    """p-confidence and p-bias of the continuity-corrected ArcSine interval (R pCOpBICAS)."""
    _validate_cc(n, alp, c)
    return _cc("ArcSine", n, alp, c)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `pcopbiclt`

```{eval-rst}
.. autofunction:: binomcikit.pconf.cc_all.pcopbiclt
```

**In plain words** — the **p-confidence and p-bias** of the continuity-corrected Logit-Wald interval — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbiclt(20, 0.05, 0.02)
```

**R source** — [`R/421.p-Confidence_p-Bias_CC_All.R` (line 240)](https://github.com/RajeswaranV/proportion/blob/master/R/421.p-Confidence_p-Bias_CC_All.R#L240), function `pCOpBICLT`

```r
pCOpBICLT<-function(n,alp,c)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")

####INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
pCLT=0
qCLT=0
seCLT=0
lgit=0
LCLT=0
UCLT=0
pcon=0						#p-confidence
pconC=0
pconf=0
pbia1=0					#p-bias
pbias=0
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
if(LCLT[j+1]<0) LCLT[j+1]=0
if(UCLT[j+1]>1) UCLT[j+1]=1
}

####p-confidence and p-bias
for(i in 2:(k-1))
{
pcon[i-1]=2*(stats::pbinom(i-1, n, LCLT[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LCLT[i]))
pconC[i-1]=2*stats::pbinom(i-1, n, UCLT[i], lower.tail = TRUE, log.p = FALSE)
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

**Python source** — `binomcikit.pconf.cc_all.pcopbiclt`

```python
def pcopbiclt(n, alp, c):
    """p-confidence and p-bias of the continuity-corrected Logit-Wald interval (R pCOpBICLT)."""
    _validate_cc(n, alp, c)
    return _cc("Logit-Wald", n, alp, c)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `pcopbicsc`

```{eval-rst}
.. autofunction:: binomcikit.pconf.cc_all.pcopbicsc
```

**In plain words** — the **p-confidence and p-bias** of the continuity-corrected Score / Wilson interval — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbicsc(20, 0.05, 0.02)
```

**R source** — [`R/421.p-Confidence_p-Bias_CC_All.R` (line 91)](https://github.com/RajeswaranV/proportion/blob/master/R/421.p-Confidence_p-Bias_CC_All.R#L91), function `pCOpBICSC`

```r
pCOpBICSC<-function(n,alp,c)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if (c<=0 || c>(1/(2*n)) || length(c)>1) stop("'c' has to be positive and less than or equal to 1/(2*n)")


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
pcon=0						#p-confidence
pconC=0
pconf=0
pbia1=0					#p-bias
pbias=0
###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
cv1=(cv^2)/(2*n)
cv2=cv/(2*n)

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
}
####p-confidence and p-bias
for(i in 2:(k-1))
{
pcon[i-1]=2*(stats::pbinom(i-1, n, LCS[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LCS[i]))
pconC[i-1]=2*stats::pbinom(i-1, n, UCS[i], lower.tail = TRUE, log.p = FALSE)
pconf[i-1]=1-max(pcon[i-1],pconC[i-1]) 		#p-confidence calculation
pbia1[i-1]=max(pcon[i-1],pconC[i-1])-min(pcon[i-1],pconC[i-1])
pbias[i-1]=max(0,pbia1[i-1])
}
x1=1:(n-1)
p_C_B=data.frame(x1,pconf,pbias)
return(p_C_B)
}
```

**What the R code does** — The R function reads the interval limits and evaluates the two tail probabilities for every interior `x`, returning `x1`, `pconf`, `pbias`.

**Python source** — `binomcikit.pconf.cc_all.pcopbicsc`

```python
def pcopbicsc(n, alp, c):
    """p-confidence and p-bias of the continuity-corrected Score interval (R pCOpBICSC)."""
    _validate_cc(n, alp, c)
    return _cc("Score", n, alp, c)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `pcopbictw`

```{eval-rst}
.. autofunction:: binomcikit.pconf.cc_all.pcopbictw
```

**In plain words** — the **p-confidence and p-bias** of the continuity-corrected Wald-T interval — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbictw(20, 0.05, 0.02)
```

**R source** — [`R/421.p-Confidence_p-Bias_CC_All.R` (line 325)](https://github.com/RajeswaranV/proportion/blob/master/R/421.p-Confidence_p-Bias_CC_All.R#L325), function `pCOpBICTW`

```r
pCOpBICTW<-function(n,alp,c)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")

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
}
####p-confidence and p-bias
for(i in 2:(k-1))
{
pcon[i-1]=2*(stats::pbinom(i-1, n, LCTW[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LCTW[i]))
pconC[i-1]=2*stats::pbinom(i-1, n, UCTW[i], lower.tail = TRUE, log.p = FALSE)
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

**Python source** — `binomcikit.pconf.cc_all.pcopbictw`

```python
def pcopbictw(n, alp, c):
    """p-confidence and p-bias of the continuity-corrected Wald-T interval (R pCOpBICTW)."""
    _validate_cc(n, alp, c)
    return _cc("Wald-T", n, alp, c)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `pcopbicwd`

```{eval-rst}
.. autofunction:: binomcikit.pconf.cc_all.pcopbicwd
```

**In plain words** — the **p-confidence and p-bias** of the continuity-corrected Wald (normal-approximation) interval — deterministic measures (no simulation) of how well the interval's actual confidence matches the nominal level, per interior `x`

**The maths** — For each interior `x`, two binomial tail probabilities give p-confidence $=100(1-\max\text{tail})$ and p-bias $=100\max(0,\text{tail difference})$.

**Example**

```python
import binomcikit as bk
bk.pcopbicwd(20, 0.05, 0.02)
```

**R source** — [`R/421.p-Confidence_p-Bias_CC_All.R` (line 21)](https://github.com/RajeswaranV/proportion/blob/master/R/421.p-Confidence_p-Bias_CC_All.R#L21), function `pCOpBICWD`

```r
pCOpBICWD<-function(n,alp,c)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")

####INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
pCW=0
qCW=0
seCW=0
LCW=0
UCW=0
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
pCW[i]=x[i]/n
qCW[i]=1-pCW[i]
seCW[i]=sqrt(pCW[i]*qCW[i]/n)
LCW[i]=pCW[i]-((cv*seCW[i])+c)
UCW[i]=pCW[i]+((cv*seCW[i])+c)
if(LCW[i]<0) LCW[i]=0
if(UCW[i]>1) UCW[i]=1
}
####p-confidence and p-bias
for(i in 2:(k-1))
{
pcon[i-1]=2*(stats::pbinom(i-1, n, LCW[i], lower.tail = FALSE, log.p = FALSE)+stats::dbinom(i-1, n, LCW[i]))
pconC[i-1]=2*stats::pbinom(i-1, n, UCW[i], lower.tail = TRUE, log.p = FALSE)
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

**Python source** — `binomcikit.pconf.cc_all.pcopbicwd`

```python
def pcopbicwd(n, alp, c):
    """p-confidence and p-bias of the continuity-corrected Wald interval (R pCOpBICWD)."""
    _validate_cc(n, alp, c)
    return _cc("Wald", n, alp, c)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the deterministic `_pconf_pbias` engine (`scipy.stats.binom` tails); matches R exactly.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

