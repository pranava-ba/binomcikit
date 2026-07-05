<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `covp.base_all`

```{eval-rst}
.. module:: binomcikit.covp.base_all
```

This module computes **coverage probability** — how often each interval actually contains the true proportion, evaluated over hypothetical *p* drawn from a `Beta(a, b)` prior and summarised (mean/min coverage, RMSE, tolerance), for the **base** interval methods. These functions reuse the confidence-interval limits from the 1xx `ci` family and feed them through a shared engine, so only the supplied limits differ between methods. See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `covpall`

```{eval-rst}
.. autofunction:: binomcikit.covp.base_all.covpall
```

**In plain words** — the **coverage probability** of all interval methods — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covpall(20, 0.05, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/201.CoverageProb_BASE_All.R` (line 1225)](https://github.com/RajeswaranV/proportion/blob/master/R/201.CoverageProb_BASE_All.R#L1225), function `covpAll`

```r
covpAll<-function(n,alp,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

  #### Calling functions and creating df
  Waldcovp.df    = covpWD(n,alp,a,b,t1,t2)
  ArcSinecovp.df = covpAS(n,alp,a,b,t1,t2)
  LRcovp.df      = covpLR(n,alp,a,b,t1,t2)
  Scorecovp.df   = covpSC(n,alp,a,b,t1,t2)
  WaldLcovp.df   = covpLT(n,alp,a,b,t1,t2)
  AdWaldcovp.df  = covpTW(n,alp,a,b,t1,t2)


  Waldcovp.df$method    = as.factor("Wald")
  ArcSinecovp.df$method = as.factor("ArcSine")
  LRcovp.df$method      = as.factor("Lilelihood")
  WaldLcovp.df$method    = as.factor("WaldLogit")
  Scorecovp.df$method   = as.factor("Score")
  AdWaldcovp.df$method  = as.factor("Wald-T")

  Generic.1 = data.frame(method = Waldcovp.df$method, MeanCP=Waldcovp.df$mcpW, MinCP= Waldcovp.df$micpW, RMSE_N=Waldcovp.df$RMSE_N,RMSE_M=Waldcovp.df$RMSE_M,RMSE_MI=Waldcovp.df$RMSE_MI,tol=Waldcovp.df$tol)
  Generic.2 = data.frame(method = ArcSinecovp.df$method, MeanCP=ArcSinecovp.df$mcpA, MinCP= ArcSinecovp.df$micpA, RMSE_N=ArcSinecovp.df$RMSE_N,RMSE_M=ArcSinecovp.df$RMSE_M,RMSE_MI=ArcSinecovp.df$RMSE_MI,tol=ArcSinecovp.df$tol)
  Generic.3 = data.frame(method = LRcovp.df$method, MeanCP=LRcovp.df$mcpL, MinCP= LRcovp.df$micpL, RMSE_N=LRcovp.df$RMSE_N,RMSE_M=LRcovp.df$RMSE_M,RMSE_MI=LRcovp.df$RMSE_MI,tol=LRcovp.df$tol)
  Generic.4 = data.frame(method = Scorecovp.df$method, MeanCP=Scorecovp.df$mcpS, MinCP= Scorecovp.df$micpS, RMSE_N=Scorecovp.df$RMSE_N,RMSE_M=Scorecovp.df$RMSE_M,RMSE_MI=Scorecovp.df$RMSE_MI,tol=Scorecovp.df$tol)
  Generic.5 = data.frame(method = WaldLcovp.df$method, MeanCP=WaldLcovp.df$mcpLT, MinCP= WaldLcovp.df$micpLT, RMSE_N=WaldLcovp.df$RMSE_N,RMSE_M=WaldLcovp.df$RMSE_M,RMSE_MI=WaldLcovp.df$RMSE_MI,tol=WaldLcovp.df$tol)
  Generic.6 = data.frame(method = AdWaldcovp.df$method, MeanCP=AdWaldcovp.df$mcpTW, MinCP= AdWaldcovp.df$micpTW, RMSE_N=AdWaldcovp.df$RMSE_N,RMSE_M=AdWaldcovp.df$RMSE_M,RMSE_MI=AdWaldcovp.df$RMSE_MI,tol=AdWaldcovp.df$tol)

  Final.df= rbind(Generic.1,Generic.2,Generic.3,Generic.4,Generic.5, Generic.6)

  return(Final.df)
}
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.base_all.covpall`

```python
def covpall(n, alp, a, b, t1, t2, seed=None):
    """Coverage probability summary for all six base methods (R covpAll)."""
    _validate(n, alp, a, b, t1, t2)
    methods = {
        'Wald': covpwd, 'ArcSine': covpas, 'Likelihood': covplr,
        'Score': covpsc, 'Wald-T': covptw, 'Logit-Wald': covplt,
    }
    rows = []
    for name, fn in methods.items():
        row = fn(n, alp, a, b, t1, t2, seed).iloc[0].to_dict()
        row['method'] = name
        rows.append(row)
    out = pd.DataFrame(rows)
    return out[['method', 'mcp', 'micp', 'RMSE_N', 'RMSE_M', 'RMSE_MI', 'tol']]

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `covpas`

```{eval-rst}
.. autofunction:: binomcikit.covp.base_all.covpas
```

**In plain words** — the **coverage probability** of the ArcSine (variance-stabilised) interval — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covpas(20, 0.05, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/201.CoverageProb_BASE_All.R` (line 320)](https://github.com/RajeswaranV/proportion/blob/master/R/201.CoverageProb_BASE_All.R#L320), function `covpAS`

```r
covpAS<-function(n,alp,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

  ####INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
pA=0
qA=0
seA=0
LA=0
UA=0
s=5000								#Simulation run to generate hypothetical p
cpA=matrix(0,k,s)
ctA=matrix(0,k,s)							#Cover Pbty quantity in sum
cppA=0								#Coverage probabilty
RMSE_N1=0
RMSE_M1=0
RMSE_Mi1=0
ctr=0

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
####COVERAGE PROBABILITIES
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
if(hp[j] > LA[i] && hp[j] < UA[i])
{
cpA[i,j]=stats::dbinom(i-1, n,hp[j])
ctA[i,j]=1
}
}
cppA[j]=sum(cpA[,j])						#Coverage Probability
RMSE_N1[j]=(cppA[j]-(1-alp))^2			#Root mean Square from nominal size
if(t1<cppA[j]&&cppA[j]<t2) ctr=ctr+1		#tolerance for cov prob - user defined
}
#CPA=data.frame(hp,cppA)
mcpA=mean(cppA)							#Mean Cov Prob
micpA=min(cppA)
RMSE_N=sqrt(mean(RMSE_N1))

#Root mean Square from min and mean CoPr
for (j in 1:s)
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.base_all.covpas`

```python
def covpas(n, alp, a, b, t1, t2, seed=None):
    """Coverage probability of the ArcSine interval (R covpAS)."""
    _validate(n, alp, a, b, t1, t2)
    df = cias(n, alp)
    return _coverage(n, alp, a, b, t1, t2, df['LAS'], df['UAS'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `covplr`

```{eval-rst}
.. autofunction:: binomcikit.covp.base_all.covplr
```

**In plain words** — the **coverage probability** of the Likelihood-Ratio interval — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covplr(20, 0.05, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/201.CoverageProb_BASE_All.R` (line 738)](https://github.com/RajeswaranV/proportion/blob/master/R/201.CoverageProb_BASE_All.R#L738), function `covpLR`

```r
covpLR<-function(n,alp,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

  ####INPUT n
y=0:n
k=n+1
####INITIALIZATIONS
mle=0
cutoff=0
LL=0
UL=0
s=5000								#Simulation run to generate hypothetical p
cpL=matrix(0,k,s)
ctL=matrix(0,k,s)							#Cover Pbty quantity in sum
cppL=0								#Coverage probabilty
RMSE_N1=0
RMSE_M1=0
RMSE_Mi1=0
ctr=0

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
####COVERAGE PROBABILITIES
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
if(hp[j] > LL[i] && hp[j] < UL[i])
{
cpL[i,j]=stats::dbinom(i-1, n,hp[j])
ctL[i,j]=1
}
}
cppL[j]=sum(cpL[,j])						#Coverage Probability
RMSE_N1[j]=(cppL[j]-(1-alp))^2			#Root mean Square from nominal size
if(t1<cppL[j]&&cppL[j]<t2) ctr=ctr+1		#tolerance for cov prob - user defined
}
#CPL=data.frame(hp,cppL)
mcpL=mean(cppL)
micpL=min(cppL)					#Mean Cov Prob
RMSE_N=sqrt(mean(RMSE_N1))

#Root mean Square from min and mean CoPr
for (j in 1:s)
{
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.base_all.covplr`

```python
def covplr(n, alp, a, b, t1, t2, seed=None):
    """Coverage probability of the Likelihood-Ratio interval (R covpLR)."""
    _validate(n, alp, a, b, t1, t2)
    df = cilr(n, alp)
    return _coverage(n, alp, a, b, t1, t2, df['LLR'], df['ULR'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `covplt`

```{eval-rst}
.. autofunction:: binomcikit.covp.base_all.covplt
```

**In plain words** — the **coverage probability** of the Logit-Wald interval — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covplt(20, 0.05, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/201.CoverageProb_BASE_All.R` (line 451)](https://github.com/RajeswaranV/proportion/blob/master/R/201.CoverageProb_BASE_All.R#L451), function `covpLT`

```r
covpLT<-function(n,alp,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

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
s=5000								#Simulation run to generate hypothetical p
cpLT=matrix(0,k,s)
ctLT=matrix(0,k,s)							#Cover Pbty quantity in sum
cppLT=0								#Coverage probabilty
RMSE_N1=0
RMSE_M1=0
RMSE_Mi1=0
ctr=0

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
####COVERAGE PROBABILITIES
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
if(hp[j] > LLT[i] && hp[j] < ULT[i])
{
cpLT[i,j]=stats::dbinom(i-1, n,hp[j])
ctLT[i,j]=1
}
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.base_all.covplt`

```python
def covplt(n, alp, a, b, t1, t2, seed=None):
    """Coverage probability of the Logit-Wald interval (R covpLT)."""
    _validate(n, alp, a, b, t1, t2)
    df = cilt(n, alp)
    return _coverage(n, alp, a, b, t1, t2, df['LLT'], df['ULT'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `covpsc`

```{eval-rst}
.. autofunction:: binomcikit.covp.base_all.covpsc
```

**In plain words** — the **coverage probability** of the Score / Wilson interval — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covpsc(20, 0.05, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/201.CoverageProb_BASE_All.R` (line 184)](https://github.com/RajeswaranV/proportion/blob/master/R/201.CoverageProb_BASE_All.R#L184), function `covpSC`

```r
covpSC<-function(n,alp,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

  ###INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
pS=0
qS=0
seS=0
LS=0
US=0
s=5000								#Simulation run to generate hypothetical p
cpS=matrix(0,k,s)
ctS=matrix(0,k,s)							#Cover Pbty quantity in sum
cppS=0								#Coverage probabilty
RMSE_N1=0
RMSE_M1=0
RMSE_Mi1=0
ctr=0

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
####COVERAGE PROBABILITIES
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
if(hp[j] > LS[i] && hp[j] < US[i])
{
cpS[i,j]=stats::dbinom(i-1, n,hp[j])
ctS[i,j]=1
}
}
cppS[j]=sum(cpS[,j])						#Coverage Probability
RMSE_N1[j]=(cppS[j]-(1-alp))^2			#Root mean Square from nominal size
if(t1<cppS[j]&&cppS[j]<t2) ctr=ctr+1		#tolerance for cov prob - user defined
}
#CPS=data.frame(hp,cppS)
mcpS=mean(cppS)							#Mean Cov Prob
micpS=min(cppS)							#Mean Cov Prob
RMSE_N=sqrt(mean(RMSE_N1))
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.base_all.covpsc`

```python
def covpsc(n, alp, a, b, t1, t2, seed=None):
    """Coverage probability of the Score (Wilson) interval (R covpSC)."""
    _validate(n, alp, a, b, t1, t2)
    df = cisc(n, alp)
    return _coverage(n, alp, a, b, t1, t2, df['LSC'], df['USC'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `covptw`

```{eval-rst}
.. autofunction:: binomcikit.covp.base_all.covptw
```

**In plain words** — the **coverage probability** of the Wald-T interval — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covptw(20, 0.05, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/201.CoverageProb_BASE_All.R` (line 595)](https://github.com/RajeswaranV/proportion/blob/master/R/201.CoverageProb_BASE_All.R#L595), function `covpTW`

```r
covpTW<-function(n,alp,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

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
s=5000								#Simulation run to generate hypothetical p
cpTW=matrix(0,k,s)
ctTW=matrix(0,k,s)							#Cover Pbty quantity in sum
cppTW=0
RMSE_N1=0
RMSE_M1=0
RMSE_Mi1=0
ctr=0

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
####COVERAGE PROBABILITIES
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
if(hp[j] > LTW[i] && hp[j] < UTW[i])
{
cpTW[i,j]=stats::dbinom(i-1, n,hp[j])
ctTW[i,j]=1
}
}
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.base_all.covptw`

```python
def covptw(n, alp, a, b, t1, t2, seed=None):
    """Coverage probability of the Wald-T interval (R covpTW)."""
    _validate(n, alp, a, b, t1, t2)
    df = citw(n, alp)
    return _coverage(n, alp, a, b, t1, t2, df['LTW'], df['UTW'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `covpwd`

```{eval-rst}
.. autofunction:: binomcikit.covp.base_all.covpwd
```

**In plain words** — the **coverage probability** of the Wald (normal-approximation) interval — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covpwd(20, 0.05, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/201.CoverageProb_BASE_All.R` (line 53)](https://github.com/RajeswaranV/proportion/blob/master/R/201.CoverageProb_BASE_All.R#L53), function `covpWD`

```r
covpWD<-function(n,alp,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

####INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
pW=0
qW=0
seW=0
LW=0
UW=0
s=5000								#Simulation run to generate hypothetical p
cpW=matrix(0,k,s)
ctW=matrix(0,k,s)							#Cover Pbty quantity in sum
cppW=0								#Coverage probabilty
RMSE_N1=0
RMSE_M1=0
RMSE_Mi1=0
ctr=0
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
####COVERAGE PROBABILITIES
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
if(hp[j] > LW[i] && hp[j] < UW[i])
{
cpW[i,j]=stats::dbinom(i-1, n,hp[j])
ctW[i,j]=1
}
}
cppW[j]=sum(cpW[,j])
RMSE_N1[j]=(cppW[j]-(1-alp))^2			#Root mean Square from nominal size
if(t1<cppW[j]&&cppW[j]<t2) ctr=ctr+1		#tolerance for cov prob - user defined
}
#CPW=data.frame(hp,cppW)
mcpW=mean(cppW)
micpW=min(cppW)					#Mean Cov Prob
RMSE_N=sqrt(mean(RMSE_N1))

#Root mean Square from min and mean CoPr
for (j in 1:s)
{
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.base_all.covpwd`

```python
def covpwd(n, alp, a, b, t1, t2, seed=None):
    """Coverage probability of the Wald interval (R covpWD)."""
    _validate(n, alp, a, b, t1, t2)
    df = ciwd(n, alp)
    return _coverage(n, alp, a, b, t1, t2, df['LWD'], df['UWD'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

