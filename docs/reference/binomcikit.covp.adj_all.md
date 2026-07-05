<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `covp.adj_all`

```{eval-rst}
.. module:: binomcikit.covp.adj_all
```

This module computes **coverage probability** — how often each interval actually contains the true proportion, evaluated over hypothetical *p* drawn from a `Beta(a, b)` prior and summarised (mean/min coverage, RMSE, tolerance), for the **adjusted** (pseudo-count `x+h`, `n+2h`) interval methods. These functions reuse the confidence-interval limits from the 1xx `ci` family and feed them through a shared engine, so only the supplied limits differ between methods. See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `covpaall`

```{eval-rst}
.. autofunction:: binomcikit.covp.adj_all.covpaall
```

**In plain words** — the **coverage probability** of all adjusted interval methods — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covpaall(20, 0.05, 2, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/212.CoverageProb_ADJ_All.R` (line 775)](https://github.com/RajeswaranV/proportion/blob/master/R/212.CoverageProb_ADJ_All.R#L775), function `covpAAll`

```r
covpAAll<-function(n,alp,h,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h) >1|| h<0  || !(h%%1 ==0)) stop("'h' has to be an integer greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

  #### Calling functions and creating df
  Waldcovp.df    = covpAWD(n,alp,h,a,b,t1,t2)
  ArcSinecovp.df = covpAAS(n,alp,h,a,b,t1,t2)
  LRcovp.df      = covpALR(n,alp,h,a,b,t1,t2)
  Scorecovp.df   = covpASC(n,alp,h,a,b,t1,t2)
  WaldLcovp.df   = covpALT(n,alp,h,a,b,t1,t2)
  AdWaldcovp.df  = covpATW(n,alp,h,a,b,t1,t2)


  Waldcovp.df$method    = as.factor("Adj-Wald")
  ArcSinecovp.df$method = as.factor("Adj-ArcSine")
  LRcovp.df$method      = as.factor("Adj-Lilelihood")
  WaldLcovp.df$method    = as.factor("Adj-Logit-Wald")
  Scorecovp.df$method   = as.factor("Adj-Score")
  AdWaldcovp.df$method  = as.factor("Adj-Wald-T")

  Generic.1 = data.frame(method = Waldcovp.df$method, MeanCP=Waldcovp.df$mcpAW, MinCP= Waldcovp.df$micpAW, RMSE_N=Waldcovp.df$RMSE_N,RMSE_M=Waldcovp.df$RMSE_M,RMSE_MI=Waldcovp.df$RMSE_MI,tol=Waldcovp.df$tol)
  Generic.2 = data.frame(method = ArcSinecovp.df$method, MeanCP=ArcSinecovp.df$mcpAA, MinCP= ArcSinecovp.df$micpAA, RMSE_N=ArcSinecovp.df$RMSE_N,RMSE_M=ArcSinecovp.df$RMSE_M,RMSE_MI=ArcSinecovp.df$RMSE_MI,tol=ArcSinecovp.df$tol)
  Generic.3 = data.frame(method = LRcovp.df$method, MeanCP=LRcovp.df$mcpAL, MinCP= LRcovp.df$micpAL, RMSE_N=LRcovp.df$RMSE_N,RMSE_M=LRcovp.df$RMSE_M,RMSE_MI=LRcovp.df$RMSE_MI,tol=LRcovp.df$tol)
  Generic.4 = data.frame(method = Scorecovp.df$method, MeanCP=Scorecovp.df$mcpAS, MinCP= Scorecovp.df$micpAS, RMSE_N=Scorecovp.df$RMSE_N,RMSE_M=Scorecovp.df$RMSE_M,RMSE_MI=Scorecovp.df$RMSE_MI,tol=Scorecovp.df$tol)
  Generic.5 = data.frame(method = WaldLcovp.df$method, MeanCP=WaldLcovp.df$mcpALT, MinCP= WaldLcovp.df$micpALT, RMSE_N=WaldLcovp.df$RMSE_N,RMSE_M=WaldLcovp.df$RMSE_M,RMSE_MI=WaldLcovp.df$RMSE_MI,tol=WaldLcovp.df$tol)
  Generic.6 = data.frame(method = AdWaldcovp.df$method, MeanCP=AdWaldcovp.df$mcpATW, MinCP= AdWaldcovp.df$micpATW, RMSE_N=AdWaldcovp.df$RMSE_N,RMSE_M=AdWaldcovp.df$RMSE_M,RMSE_MI=AdWaldcovp.df$RMSE_MI,tol=AdWaldcovp.df$tol)

  Final.df= rbind(Generic.1,Generic.2,Generic.3,Generic.4,Generic.5, Generic.6)

  return(Final.df)
}
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.adj_all.covpaall`

```python
def covpaall(n, alp, h, a, b, t1, t2, seed=None):
    """Coverage probability summary for all six adjusted methods (R covpAAll)."""
    _validate_adj(n, alp, h, a, b, t1, t2)
    methods = {
        'Wald': covpawd, 'ArcSine': covpaas, 'Likelihood': covpalr,
        'Score': covpasc, 'Wald-T': covpatw, 'Logit-Wald': covpalt,
    }
    import pandas as pd
    rows = []
    for name, fn in methods.items():
        row = fn(n, alp, h, a, b, t1, t2, seed).iloc[0].to_dict()
        row['method'] = name
        rows.append(row)
    out = pd.DataFrame(rows)
    return out[['method', 'mcp', 'micp', 'RMSE_N', 'RMSE_M', 'RMSE_MI', 'tol']]

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `covpaas`

```{eval-rst}
.. autofunction:: binomcikit.covp.adj_all.covpaas
```

**In plain words** — the **coverage probability** of the adjusted ArcSine (variance-stabilised) interval — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covpaas(20, 0.05, 2, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/212.CoverageProb_ADJ_All.R` (line 282)](https://github.com/RajeswaranV/proportion/blob/master/R/212.CoverageProb_ADJ_All.R#L282), function `covpAAS`

```r
covpAAS<-function(n,alp,h,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

####INPUT n
x=0:n
k=n+1
y=x+h
n1=n+(2*h)
####INITIALIZATIONS
pAA=0
qAA=0
seAA=0
LAA=0
UAA=0
s=5000								#Simulation run to generate hypothetical p
cpAA=matrix(0,k,s)
ctAA=matrix(0,k,s)							#Cover Pbty quantity in sum
cppAA=0								#Coverage probabilty
RMSE_N1=0
RMSE_M1=0
RMSE_Mi1=0
ctr=0

###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#ADJUSTED ARC-SINE METHOD
for(i in 1:k)
{
pAA[i]=y[i]/n1
qAA[i]=1-pAA[i]
seAA[i]=cv/sqrt(4*n1)
LAA[i]=(sin(asin(sqrt(pAA[i]))-seAA[i]))^2
UAA[i]=(sin(asin(sqrt(pAA[i]))+seAA[i]))^2
if(LAA[i]<0) LAA[i]=0
if(UAA[i]>1) UAA[i]=1
}
####COVERAGE PROBABILITIES
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
if(hp[j] > LAA[i] && hp[j] < UAA[i])
{
cpAA[i,j]=stats::dbinom(i-1, n,hp[j])
ctAA[i,j]=1
}
}
cppAA[j]=sum(cpAA[,j])						#Coverage Probability
RMSE_N1[j]=(cppAA[j]-(1-alp))^2			#Root mean Square from nominal size
if(t1<cppAA[j]&&cppAA[j]<t2) ctr=ctr+1		#tolerance for cov prob - user defined
}
#CPAA=data.frame(hp,cppAA)
mcpAA=mean(cppAA)							#Mean Cov Prob
micpAA=min(cppAA)
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.adj_all.covpaas`

```python
def covpaas(n, alp, h, a, b, t1, t2, seed=None):
    """Coverage probability of the adjusted ArcSine interval (R covpAAS)."""
    _validate_adj(n, alp, h, a, b, t1, t2)
    df = ciaas(n, alp, h)
    return _coverage(n, alp, a, b, t1, t2, df['LAAS'], df['UAAS'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `covpalr`

```{eval-rst}
.. autofunction:: binomcikit.covp.adj_all.covpalr
```

**In plain words** — the **coverage probability** of the adjusted Likelihood-Ratio interval — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covpalr(20, 0.05, 2, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/212.CoverageProb_ADJ_All.R` (line 652)](https://github.com/RajeswaranV/proportion/blob/master/R/212.CoverageProb_ADJ_All.R#L652), function `covpALR`

```r
covpALR<-function(n,alp,h,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h) >1|| h<0  || !(h%%1 ==0)) stop("'h' has to be an integer greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

####INPUT n
y=0:n
k=n+1
y1=y+h
n1=n+(2*h)
####INITIALIZATIONS
mle=0
cutoff=0
LAL=0
UAL=0
s=5000								#Simulation run to generate hypothetical p
cpAL=matrix(0,k,s)
ctAL=matrix(0,k,s)							#Cover Pbty quantity in sum
cppAL=0								#Coverage probabilty
RMSE_N1=0
RMSE_M1=0
RMSE_Mi1=0
ctr=0

###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#ADJUSTED LIKELIHOOD-RATIO METHOD
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
####COVERAGE PROBABILITIES
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
if(hp[j] > LAL[i] && hp[j] < UAL[i])
{
cpAL[i,j]=stats::dbinom(i-1, n,hp[j])
ctAL[i,j]=1
}
}
cppAL[j]=sum(cpAL[,j])						#Coverage Probability
RMSE_N1[j]=(cppAL[j]-(1-alp))^2			#Root mean Square from nominal size
if(t1<cppAL[j]&&cppAL[j]<t2) ctr=ctr+1		#tolerance for cov prob - user defined
}
#CPAL=data.frame(hp,cppAL)
mcpAL=mean(cppAL)
micpAL=min(cppAL)					#Mean Cov Prob
RMSE_N=sqrt(mean(RMSE_N1))
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.adj_all.covpalr`

```python
def covpalr(n, alp, h, a, b, t1, t2, seed=None):
    """Coverage probability of the adjusted Likelihood-Ratio interval (R covpALR)."""
    _validate_adj(n, alp, h, a, b, t1, t2)
    df = cialr(n, alp, h)
    return _coverage(n, alp, a, b, t1, t2, df['LALR'], df['UALR'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `covpalt`

```{eval-rst}
.. autofunction:: binomcikit.covp.adj_all.covpalt
```

**In plain words** — the **coverage probability** of the adjusted Logit-Wald interval — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covpalt(20, 0.05, 2, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/212.CoverageProb_ADJ_All.R` (line 402)](https://github.com/RajeswaranV/proportion/blob/master/R/212.CoverageProb_ADJ_All.R#L402), function `covpALT`

```r
covpALT<-function(n,alp,h,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

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
s=5000								#Simulation run to generate hypothetical p
cpALT=matrix(0,k,s)
ctALT=matrix(0,k,s)							#Cover Pbty quantity in sum
cppALT=0								#Coverage probabilty
RMSE_N1=0
RMSE_M1=0
RMSE_Mi1=0
ctr=0

###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#ADJUSTED LOGIT-WALD METHOD
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
####COVERAGE PROBABILITIES
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
if(hp[j] > LALT[i] && hp[j] < UALT[i])
{
cpALT[i,j]=stats::dbinom(i-1, n,hp[j])
ctALT[i,j]=1
}
}
cppALT[j]=sum(cpALT[,j])				#Coverage Probability
RMSE_N1[j]=(cppALT[j]-(1-alp))^2			#Root mean Square from nominal size
if(t1<cppALT[j]&&cppALT[j]<t2) ctr=ctr+1		#tolerance for cov prob - user defined

  # ... (truncated - see the linked source)
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.adj_all.covpalt`

```python
def covpalt(n, alp, h, a, b, t1, t2, seed=None):
    """Coverage probability of the adjusted Logit-Wald interval (R covpALT)."""
    _validate_adj(n, alp, h, a, b, t1, t2)
    df = cialt(n, alp, h)
    return _coverage(n, alp, a, b, t1, t2, df['LALT'], df['UALT'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `covpasc`

```{eval-rst}
.. autofunction:: binomcikit.covp.adj_all.covpasc
```

**In plain words** — the **coverage probability** of the adjusted Score / Wilson interval — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covpasc(20, 0.05, 2, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/212.CoverageProb_ADJ_All.R` (line 157)](https://github.com/RajeswaranV/proportion/blob/master/R/212.CoverageProb_ADJ_All.R#L157), function `covpASC`

```r
covpASC<-function(n,alp,h,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

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
s=1000								#Simulation run to generate hypothetical p
cpAS=matrix(0,k,s)
ctAS=matrix(0,k,s)							#Cover Pbty quantity in sum
cppAS=0							#Coverage probabilty
RMSE_N1=0
RMSE_M1=0
RMSE_Mi1=0
ctr=0

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
####COVERAGE PROBABILITIES
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
if(hp[j] > LAS[i] && hp[j] < UAS[i])
{
cpAS[i,j]=stats::dbinom(i-1, n,hp[j])
ctAS[i,j]=1
}
}
cppAS[j]=sum(cpAS[,j])						#Coverage Probability
RMSE_N1[j]=(cppAS[j]-(1-alp))^2			#Root mean Square from nominal size
if(t1<cppAS[j]&&cppAS[j]<t2) ctr=ctr+1		#tolerance for cov prob - user defined
}
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.adj_all.covpasc`

```python
def covpasc(n, alp, h, a, b, t1, t2, seed=None):
    """Coverage probability of the adjusted Score interval (R covpASC)."""
    _validate_adj(n, alp, h, a, b, t1, t2)
    df = ciasc(n, alp, h)
    return _coverage(n, alp, a, b, t1, t2, df['LASC'], df['UASC'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `covpatw`

```{eval-rst}
.. autofunction:: binomcikit.covp.adj_all.covpatw
```

**In plain words** — the **coverage probability** of the adjusted Wald-T interval — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covpatw(20, 0.05, 2, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/212.CoverageProb_ADJ_All.R` (line 526)](https://github.com/RajeswaranV/proportion/blob/master/R/212.CoverageProb_ADJ_All.R#L526), function `covpATW`

```r
covpATW<-function(n,alp,h,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

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
s=5000								#Simulation run to generate hypothetical p
cpATW=matrix(0,k,s)
ctATW=matrix(0,k,s)							#Cover Pbty quantity in sum
cppATW=0
RMSE_N1=0
RMSE_M1=0
RMSE_Mi1=0
ctr=0

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
####COVERAGE PROBABILITIES
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
if(hp[j] > LATW[i] && hp[j] < UATW[i])
{
cpATW[i,j]=stats::dbinom(i-1, n,hp[j])
ctATW[i,j]=1
}
}
cppATW[j]=sum(cpATW[,j])						#Coverage Probability
RMSE_N1[j]=(cppATW[j]-(1-alp))^2			#Root mean Square from nominal size
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.adj_all.covpatw`

```python
def covpatw(n, alp, h, a, b, t1, t2, seed=None):
    """Coverage probability of the adjusted Wald-T interval (R covpATW)."""
    _validate_adj(n, alp, h, a, b, t1, t2)
    df = ciatw(n, alp, h)
    return _coverage(n, alp, a, b, t1, t2, df['LATW'], df['UATW'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `covpawd`

```{eval-rst}
.. autofunction:: binomcikit.covp.adj_all.covpawd
```

**In plain words** — the **coverage probability** of the adjusted Wald (normal-approximation) interval — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covpawd(20, 0.05, 2, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/212.CoverageProb_ADJ_All.R` (line 37)](https://github.com/RajeswaranV/proportion/blob/master/R/212.CoverageProb_ADJ_All.R#L37), function `covpAWD`

```r
covpAWD<-function(n,alp,h,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

####INPUT n
x=0:n
k=n+1
y=x+h
n1=n+(2*h)
####INITIALIZATIONS
pAW=0
qAW=0
seAW=0
LAW=0
UAW=0
s=5000								#Simulation run to generate hypothetical p
cpAW=matrix(0,k,s)
ctAW=matrix(0,k,s)							#Cover Pbty quantity in sum
cppAW=0								#Coverage probabilty
RMSE_N1=0
RMSE_M1=0
RMSE_Mi1=0
ctr=0
###CRITICAL VALUES
cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
#WALD METHOD
for(i in 1:k)
{
pAW[i]=y[i]/n1
qAW[i]=1-pAW[i]
seAW[i]=sqrt(pAW[i]*qAW[i]/n1)
LAW[i]=pAW[i]-(cv*seAW[i])
UAW[i]=pAW[i]+(cv*seAW[i])
if(LAW[i]<0) LAW[i]=0
if(UAW[i]>1) UAW[i]=1
}
####COVERAGE PROBABILITIES
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
if(hp[j] > LAW[i] && hp[j] < UAW[i])
{
cpAW[i,j]=stats::dbinom(i-1, n,hp[j])
ctAW[i,j]=1
}
}
cppAW[j]=sum(cpAW[,j])
RMSE_N1[j]=(cppAW[j]-(1-alp))^2			#Root mean Square from nominal size
if(t1<cppAW[j]&&cppAW[j]<t2) ctr=ctr+1		#tolerance for cov prob - user defined
}
#CPAW=data.frame(hp,cppAW)
mcpAW=mean(cppAW)
micpAW=min(cppAW)					#Mean Cov Prob
RMSE_N=sqrt(mean(RMSE_N1))
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.adj_all.covpawd`

```python
def covpawd(n, alp, h, a, b, t1, t2, seed=None):
    """Coverage probability of the adjusted Wald interval (R covpAWD)."""
    _validate_adj(n, alp, h, a, b, t1, t2)
    df = ciawd(n, alp, h)
    return _coverage(n, alp, a, b, t1, t2, df['LAWD'], df['UAWD'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

