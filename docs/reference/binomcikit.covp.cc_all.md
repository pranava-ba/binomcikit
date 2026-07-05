<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `covp.cc_all`

```{eval-rst}
.. module:: binomcikit.covp.cc_all
```

This module computes **coverage probability** — how often each interval actually contains the true proportion, evaluated over hypothetical *p* drawn from a `Beta(a, b)` prior and summarised (mean/min coverage, RMSE, tolerance), for the **continuity-corrected** interval methods (five methods; no Likelihood-Ratio). These functions reuse the confidence-interval limits from the 1xx `ci` family and feed them through a shared engine, so only the supplied limits differ between methods. See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `covpcall`

```{eval-rst}
.. autofunction:: binomcikit.covp.cc_all.covpcall
```

**In plain words** — the **coverage probability** of all continuity-corrected interval methods — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covpcall(20, 0.05, 0.02, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/221.CoverageProb_CC_All.R` (line 667)](https://github.com/RajeswaranV/proportion/blob/master/R/221.CoverageProb_CC_All.R#L667), function `covpCAll`

```r
covpCAll<-function(n,alp,c,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if (c<=0 || c>(1/(2*n))) stop("'c' has to be positive and less than or equal to 1/(2*n)")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

  #### Calling functions and creating df
  WaldcovpA.df    = covpCWD(n,alp,c,a,b,t1,t2)
  ArcSinecovpA.df = covpCAS(n,alp,c,a,b,t1,t2)
  ScorecovpA.df   = covpCSC(n,alp,c,a,b,t1,t2)
  WaldLcovpA.df   = covpCLT(n,alp,c,a,b,t1,t2)
  AdWaldcovpA.df  = covpCTW(n,alp,c,a,b,t1,t2)


  WaldcovpA.df$method    = as.factor("CC-Wald")
  ArcSinecovpA.df$method = as.factor("CC-ArcSine")
  WaldLcovpA.df$method    = as.factor("CC-Logit-Wald")
  ScorecovpA.df$method   = as.factor("CC-Score")
  AdWaldcovpA.df$method  = as.factor("CC-Wald-T")

  Generic.1 = data.frame(method = WaldcovpA.df$method, MeanCP=WaldcovpA.df$mcpCW, MinCP= WaldcovpA.df$micpCW, RMSE_N=WaldcovpA.df$RMSE_N,RMSE_M=WaldcovpA.df$RMSE_M,RMSE_MI=WaldcovpA.df$RMSE_MI,tol=WaldcovpA.df$tol)
  Generic.2 = data.frame(method = ArcSinecovpA.df$method, MeanCP=ArcSinecovpA.df$mcpCA, MinCP= ArcSinecovpA.df$micpCA, RMSE_N=ArcSinecovpA.df$RMSE_N,RMSE_M=ArcSinecovpA.df$RMSE_M,RMSE_MI=ArcSinecovpA.df$RMSE_MI,tol=ArcSinecovpA.df$tol)
  Generic.4 = data.frame(method = ScorecovpA.df$method, MeanCP=ScorecovpA.df$mcpCS, MinCP= ScorecovpA.df$micpCS, RMSE_N=ScorecovpA.df$RMSE_N,RMSE_M=ScorecovpA.df$RMSE_M,RMSE_MI=ScorecovpA.df$RMSE_MI,tol=ScorecovpA.df$tol)
  Generic.5 = data.frame(method = WaldLcovpA.df$method, MeanCP=WaldLcovpA.df$mcpCLT, MinCP= WaldLcovpA.df$micpCLT, RMSE_N=WaldLcovpA.df$RMSE_N,RMSE_M=WaldLcovpA.df$RMSE_M,RMSE_MI=WaldLcovpA.df$RMSE_MI,tol=WaldLcovpA.df$tol)
  Generic.6 = data.frame(method = AdWaldcovpA.df$method, MeanCP=AdWaldcovpA.df$mcpCTW, MinCP= AdWaldcovpA.df$micpCTW, RMSE_N=AdWaldcovpA.df$RMSE_N,RMSE_M=AdWaldcovpA.df$RMSE_M,RMSE_MI=AdWaldcovpA.df$RMSE_MI,tol=AdWaldcovpA.df$tol)

  Final.df= rbind(Generic.1,Generic.2,Generic.4,Generic.5, Generic.6)

  return(Final.df)
}
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.cc_all.covpcall`

```python
def covpcall(n, alp, c, a, b, t1, t2, seed=None):
    """Coverage probability summary for all five CC methods (R covpCAll)."""
    _validate_cc(n, alp, c, a, b, t1, t2)
    methods = {
        'Wald': covpcwd, 'ArcSine': covpcas, 'Score': covpcsc,
        'Wald-T': covpctw, 'Logit-Wald': covpclt,
    }
    rows = []
    for name, fn in methods.items():
        row = fn(n, alp, c, a, b, t1, t2, seed).iloc[0].to_dict()
        row['method'] = name
        rows.append(row)
    out = pd.DataFrame(rows)
    return out[['method', 'mcp', 'micp', 'RMSE_N', 'RMSE_M', 'RMSE_MI', 'tol']]

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `covpcas`

```{eval-rst}
.. autofunction:: binomcikit.covp.cc_all.covpcas
```

**In plain words** — the **coverage probability** of the continuity-corrected ArcSine (variance-stabilised) interval — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covpcas(20, 0.05, 0.02, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/221.CoverageProb_CC_All.R` (line 282)](https://github.com/RajeswaranV/proportion/blob/master/R/221.CoverageProb_CC_All.R#L282), function `covpCAS`

```r
covpCAS<-function(n,alp,c,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

####INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
pCA=0
qCA=0
seCA=0
LCA=0
UCA=0
s=5000								#Simulation run to generate hypothetical p
cpCA=matrix(0,k,s)
ctCA=matrix(0,k,s)							#Cover Pbty quantity in sum
cppCA=0									#Coverage probabilty
RMSE_N1=0
RMSE_M1=0
RMSE_Mi1=0
ctr=0

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
####COVERAGE PROBABILITIES
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
if(hp[j] > LCA[i] && hp[j] < UCA[i])
{
cpCA[i,j]=stats::dbinom(i-1, n,hp[j])
ctCA[i,j]=1
}
}
cppCA[j]=sum(cpCA[,j])						#Coverage Probability
RMSE_N1[j]=(cppCA[j]-(1-alp))^2			#Root mean Square from nominal size
if(t1<cppCA[j]&&cppCA[j]<t2) ctr=ctr+1		#tolerance for cov prob - user defined
}
#CPCA=data.frame(hp,cppCA)
mcpCA=mean(cppCA)							#Mean Cov Prob
micpCA=min(cppCA)
RMSE_N=sqrt(mean(RMSE_N1))

  # ... (truncated - see the linked source)
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.cc_all.covpcas`

```python
def covpcas(n, alp, c, a, b, t1, t2, seed=None):
    """Coverage probability of the continuity-corrected ArcSine interval (R covpCAS)."""
    _validate_cc(n, alp, c, a, b, t1, t2)
    df = cicas(n, alp, c)
    return _coverage(n, alp, a, b, t1, t2, df['LCA'], df['UCA'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `covpclt`

```{eval-rst}
.. autofunction:: binomcikit.covp.cc_all.covpclt
```

**In plain words** — the **coverage probability** of the continuity-corrected Logit-Wald interval — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covpclt(20, 0.05, 0.02, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/221.CoverageProb_CC_All.R` (line 400)](https://github.com/RajeswaranV/proportion/blob/master/R/221.CoverageProb_CC_All.R#L400), function `covpCLT`

```r
covpCLT<-function(n,alp,c,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

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
s=5000								#Simulation run to generate hypothetical p
cpCLT=matrix(0,k,s)
ctCLT=matrix(0,k,s)							#Cover Pbty quantity in sum
cppCLT=0								#Coverage probabilty
RMSE_N1=0
RMSE_M1=0
RMSE_Mi1=0
ctr=0

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
}
####COVERAGE PROBABILITIES
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.cc_all.covpclt`

```python
def covpclt(n, alp, c, a, b, t1, t2, seed=None):
    """Coverage probability of the continuity-corrected Logit-Wald interval (R covpCLT)."""
    _validate_cc(n, alp, c, a, b, t1, t2)
    df = ciclt(n, alp, c)
    return _coverage(n, alp, a, b, t1, t2, df['LCLT'], df['UCLT'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `covpcsc`

```{eval-rst}
.. autofunction:: binomcikit.covp.cc_all.covpcsc
```

**In plain words** — the **coverage probability** of the continuity-corrected Score / Wilson interval — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covpcsc(20, 0.05, 0.02, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/221.CoverageProb_CC_All.R` (line 156)](https://github.com/RajeswaranV/proportion/blob/master/R/221.CoverageProb_CC_All.R#L156), function `covpCSC`

```r
covpCSC<-function(n,alp,c,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if (c<=0 || c>(1/(2*n))) stop("'c' has to be positive and less than or equal to 1/(2*n)")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")


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
s=5000								#Simulation run to generate hypothetical p
cpCS=matrix(0,k,s)
ctCS=matrix(0,k,s)							#Cover Pbty quantity in sum
cppCS=0								#Coverage probabilty
RMSE_N1=0
RMSE_M1=0
RMSE_Mi1=0
ctr=0

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
####COVERAGE PROBABILITIES
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
if(hp[j] > LCS[i] && hp[j] < UCS[i])
{
cpCS[i,j]=stats::dbinom(i-1, n,hp[j])
ctCS[i,j]=1
}
}
cppCS[j]=sum(cpCS[,j])						#Coverage Probability
RMSE_N1[j]=(cppCS[j]-(1-alp))^2			#Root mean Square from nominal size
if(t1<cppCS[j]&&cppCS[j]<t2) ctr=ctr+1		#tolerance for cov prob - user defined
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.cc_all.covpcsc`

```python
def covpcsc(n, alp, c, a, b, t1, t2, seed=None):
    """Coverage probability of the continuity-corrected Score interval (R covpCSC)."""
    _validate_cc(n, alp, c, a, b, t1, t2)
    df = cicsc(n, alp, c)
    return _coverage(n, alp, a, b, t1, t2, df['LCS'], df['UCS'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `covpctw`

```{eval-rst}
.. autofunction:: binomcikit.covp.cc_all.covpctw
```

**In plain words** — the **coverage probability** of the continuity-corrected Wald-T interval — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covpctw(20, 0.05, 0.02, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/221.CoverageProb_CC_All.R` (line 536)](https://github.com/RajeswaranV/proportion/blob/master/R/221.CoverageProb_CC_All.R#L536), function `covpCTW`

```r
covpCTW<-function(n,alp,c,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

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
s=5000								#Simulation run to generate hypothetical p
cpCTW=matrix(0,k,s)
ctCTW=matrix(0,k,s)							#Cover Pbty quantity in sum
cppCTW=0
RMSE_N1=0
RMSE_M1=0
RMSE_Mi1=0
ctr=0

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
####COVERAGE PROBABILITIES
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
if(hp[j] > LCTW[i] && hp[j] < UCTW[i])
{
cpCTW[i,j]=stats::dbinom(i-1, n,hp[j])
ctCTW[i,j]=1
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.cc_all.covpctw`

```python
def covpctw(n, alp, c, a, b, t1, t2, seed=None):
    """Coverage probability of the continuity-corrected Wald-T interval (R covpCTW)."""
    _validate_cc(n, alp, c, a, b, t1, t2)
    df = cictw(n, alp, c)
    return _coverage(n, alp, a, b, t1, t2, df['LCTW'], df['UCTW'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `covpcwd`

```{eval-rst}
.. autofunction:: binomcikit.covp.cc_all.covpcwd
```

**In plain words** — the **coverage probability** of the continuity-corrected Wald (normal-approximation) interval — how often the interval actually contains the true proportion, averaged over hypothetical values of *p* drawn from a `Beta(a, b)` prior

**The maths** — For each simulated *p*, coverage $= \sum_{x:\,L_x < p < U_x}\binom{n}{x}p^x(1-p)^{n-x}$; the function reports the mean (`mcp`), minimum (`micp`), RMSE-from-nominal (`RMSE_N`) and tolerance (`tol`).

**Example**

```python
import binomcikit as bk
bk.covpcwd(20, 0.05, 0.02, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/221.CoverageProb_CC_All.R` (line 37)](https://github.com/RajeswaranV/proportion/blob/master/R/221.CoverageProb_CC_All.R#L37), function `covpCWD`

```r
covpCWD<-function(n,alp,c,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")

####INPUT n
x=0:n
k=n+1

####INITIALIZATIONS
pCW=0
qCW=0
seCW=0
LCW=0
UCW=0
s=5000								#Simulation run to generate hypothetical p
cpCW=matrix(0,k,s)
ctCW=matrix(0,k,s)							#Cover Pbty quantity in sum
cppCW=0								#Coverage probabilty
RMSE_N1=0
RMSE_M1=0
RMSE_Mi1=0
ctr=0
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
####COVERAGE PROBABILITIES
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
if(hp[j] > LCW[i] && hp[j] < UCW[i])
{
cpCW[i,j]=stats::dbinom(i-1, n,hp[j])
ctCW[i,j]=1
}
}
cppCW[j]=sum(cpCW[,j])
RMSE_N1[j]=(cppCW[j]-(1-alp))^2			#Root mean Square from nominal size
if(t1<cppCW[j]&&cppCW[j]<t2) ctr=ctr+1		#tolerance for cov prob - user defined
}
#CPCW=data.frame(hp,cppCW)
mcpCW=mean(cppCW)
micpCW=min(cppCW)					#Mean Cov Prob
RMSE_N=sqrt(mean(RMSE_N1))

  # ... (truncated - see the linked source)
```

**What the R code does** — The R function computes the interval limits, simulates 5000 `Beta(a, b)` draws, sums the binomial mass wherever a draw is covered, and returns the summary statistics.

**Python source** — `binomcikit.covp.cc_all.covpcwd`

```python
def covpcwd(n, alp, c, a, b, t1, t2, seed=None):
    """Coverage probability of the continuity-corrected Wald interval (R covpCWD)."""
    _validate_cc(n, alp, c, a, b, t1, t2)
    df = cicwd(n, alp, c)
    return _coverage(n, alp, a, b, t1, t2, df['LCW'], df['UCW'], seed)

```

**What the Python code does** — The Python port reuses the 1xx interval limits and the shared `_coverage` engine (NumPy `default_rng` for the Beta draws), returning the same summary.

**R → Py changes** — `stats::rbeta` → NumPy `default_rng`; adds `seed=`; not draw-for-draw identical to R; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

