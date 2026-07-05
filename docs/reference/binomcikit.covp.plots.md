<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `covp.plots`

```{eval-rst}
.. module:: binomcikit.covp.plots
```

This module computes **coverage probability** — how often each interval actually contains the true proportion, evaluated over hypothetical *p* drawn from a `Beta(a, b)` prior and summarised (mean/min coverage, RMSE, tolerance), for **plots** of the results (returning plotnine `ggplot` objects). See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `plotcovpaall`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpaall
```

**In plain words** — Plots the coverage-probability curve against *p* for all adjusted interval methods — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovpaall(20, 0.05, 2, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/213.CoverageProb_ADJ_All_Graph.R` (line 20)](https://github.com/RajeswaranV/proportion/blob/master/R/213.CoverageProb_ADJ_All_Graph.R#L20), function `PlotcovpAAll`

```r
PlotcovpAAll<-function(n,alp,h,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL


  #### Calling functions and creating df
  df.1    = gcovpAWD(n,alp,h,a,b,t1,t2)
  df.2    = gcovpAAS(n,alp,h,a,b,t1,t2)
  df.3    = gcovpALR(n,alp,h,a,b,t1,t2)
  df.4    = gcovpASC(n,alp,h,a,b,t1,t2)
  df.5    = gcovpALT(n,alp,h,a,b,t1,t2)
  df.6    = gcovpATW(n,alp,h,a,b,t1,t2)

  nndf=  rbind(df.1,df.2,df.3,df.4,df.5,df.6)
  nndf$t1=t1
  nndf$t2=t2
  nndf$alp=alp

  ggplot2::ggplot(nndf, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(title = "Coverage Probability of adjusted methods") +
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)

}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpaall`

```python
def plotcovpaall(n, alp, h, a, b, t1, t2, seed=None):
    """Coverage curves for all six adjusted methods overlaid (R PlotcovpAAll)."""
    import pandas as pd
    curve = pd.concat(
        [_adj_curve(m, n, alp, h, a, b, seed) for m in _ADJ], ignore_index=True)
    return _covp_plot(curve, alp, t1, t2,
                      "Coverage Probability for all adjusted methods")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpaas`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpaas
```

**In plain words** — Plots the coverage-probability curve against *p* for the adjusted ArcSine (variance-stabilised) interval — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovpaas(20, 0.05, 2, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/213.CoverageProb_ADJ_All_Graph.R` (line 147)](https://github.com/RajeswaranV/proportion/blob/master/R/213.CoverageProb_ADJ_All_Graph.R#L147), function `PlotcovpAAS`

```r
PlotcovpAAS<-function(n,alp,h,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL

  #### Calling functions and creating df
  nndf    = gcovpAAS(n,alp,h,a,b,t1,t2)
  ArcSinecovp.df = covpAAS(n,alp,h,a,b,t1,t2)

  nndf$mcp=ArcSinecovp.df$mcpAA
  nndf$micp=ArcSinecovp.df$micpAA
  nndf$t1=t1
  nndf$t2=t2
  nndf$alp=alp

  ggplot2::ggplot(nndf, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(title = "Coverage Probability of the adjusted ArcSine method") +
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=mcp,color="Mean Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::guides(colour = ggplot2::guide_legend("Heading")) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)

}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpaas`

```python
    def _plot(n, alp, h, a, b, t1, t2, seed=None):
        curve = _adj_curve(method, n, alp, h, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpall`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpall
```

**In plain words** — Plots the coverage-probability curve against *p* for all interval methods — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovpall(20, 0.05, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/202.CoverageProb_BASE_All_Graph.R` (line 241)](https://github.com/RajeswaranV/proportion/blob/master/R/202.CoverageProb_BASE_All_Graph.R#L241), function `PlotcovpAll`

```r
PlotcovpAll<-function(n,alp,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL

  ####INPUT n
  df1=gcovpW(n,alp,a,b,t1,t2)
  df2=gcovpS(n,alp,a,b,t1,t2)
  df3=gcovpA(n,alp,a,b,t1,t2)
  df4=gcovpLT(n,alp,a,b,t1,t2)
  df5=gcovpTW(n,alp,a,b,t1,t2)
  df6=gcovpL(n,alp,a,b,t1,t2)

 nndf=  rbind(df1,df2,df3,df4,df5,df6)
 nndf$t1=t1
 nndf$t2=t2
 nndf$alp=alp

  ggplot2::ggplot(nndf, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(title = "Coverage Probability for 6 base methods") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)

}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpall`

```python
def plotcovpall(n, alp, a, b, t1, t2, seed=None):
    """Coverage curves for all six base methods overlaid (R PlotcovpAll)."""
    import pandas as pd
    curve = pd.concat(
        [_base_curve(m, n, alp, a, b, seed) for m in _BASE], ignore_index=True)
    return _covp_plot(curve, alp, t1, t2,
                      "Coverage Probability for all base methods")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpalr`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpalr
```

**In plain words** — Plots the coverage-probability curve against *p* for the adjusted Likelihood-Ratio interval — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovpalr(20, 0.05, 2, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/213.CoverageProb_ADJ_All_Graph.R` (line 210)](https://github.com/RajeswaranV/proportion/blob/master/R/213.CoverageProb_ADJ_All_Graph.R#L210), function `PlotcovpALR`

```r
PlotcovpALR<-function(n,alp,h,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL

  #### Calling functions and creating df
  nndf   = gcovpALR(n,alp,h,a,b,t1,t2)
  LRcovp.df      = covpALR(n,alp,h,a,b,t1,t2)

  nndf$mcp=LRcovp.df$mcpAL
  nndf$micp=LRcovp.df$micpAL
  nndf$t1=t1
  nndf$t2=t2
  nndf$alp=alp

  ggplot2::ggplot(nndf, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(title = "Coverage Probability of the adjusted Likelihood Ratio method") +
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=mcp,color="Mean Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::guides(colour = ggplot2::guide_legend("Heading")) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)

}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpalr`

```python
    def _plot(n, alp, h, a, b, t1, t2, seed=None):
        curve = _adj_curve(method, n, alp, h, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpalt`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpalt
```

**In plain words** — Plots the coverage-probability curve against *p* for the adjusted Logit-Wald interval — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovpalt(20, 0.05, 2, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/213.CoverageProb_ADJ_All_Graph.R` (line 336)](https://github.com/RajeswaranV/proportion/blob/master/R/213.CoverageProb_ADJ_All_Graph.R#L336), function `PlotcovpALT`

```r
PlotcovpALT<-function(n,alp,h,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL

  #### Calling functions and creating df
  nndf    = gcovpALT(n,alp,h,a,b,t1,t2)
  WaldLcovp.df   = covpALT(n,alp,h,a,b,t1,t2)

  nndf$mcp=WaldLcovp.df$mcpALT
  nndf$micp=WaldLcovp.df$micpALT
  nndf$t1=t1
  nndf$t2=t2
  nndf$alp=alp

  ggplot2::ggplot(nndf, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(title = "Coverage Probability of the adjusted Logistic Wald method") +
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=mcp,color="Mean Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::guides(colour = ggplot2::guide_legend("Heading")) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)

}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpalt`

```python
    def _plot(n, alp, h, a, b, t1, t2, seed=None):
        curve = _adj_curve(method, n, alp, h, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpas`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpas
```

**In plain words** — Plots the coverage-probability curve against *p* for the ArcSine (variance-stabilised) interval — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovpas(20, 0.05, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/202.CoverageProb_BASE_All_Graph.R` (line 359)](https://github.com/RajeswaranV/proportion/blob/master/R/202.CoverageProb_BASE_All_Graph.R#L359), function `PlotcovpAS`

```r
PlotcovpAS<-function(n,alp,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL

  ArcSinecovp.df = covpAS(n,alp,a,b,t1,t2)

  nndf=gcovpA(n,alp,a,b,t1,t2)
  nndf$mcp=ArcSinecovp.df$mcpA
  nndf$micp=ArcSinecovp.df$micpA
  nndf$t1=t1
  nndf$t2=t2
  nndf$alp=alp

  ggplot2::ggplot(nndf, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(title = "Coverage Probability for ArcSine method") +
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::geom_hline(ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=mcp,color="Mean Coverage"))+
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::guides(colour = ggplot2::guide_legend("Heading"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)

}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpas`

```python
    def _plot(n, alp, a, b, t1, t2, seed=None):
        curve = _base_curve(method, n, alp, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpasc`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpasc
```

**In plain words** — Plots the coverage-probability curve against *p* for the adjusted Score / Wilson interval — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovpasc(20, 0.05, 2, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/213.CoverageProb_ADJ_All_Graph.R` (line 273)](https://github.com/RajeswaranV/proportion/blob/master/R/213.CoverageProb_ADJ_All_Graph.R#L273), function `PlotcovpASC`

```r
PlotcovpASC<-function(n,alp,h,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL

  #### Calling functions and creating df
  nndf   = gcovpASC(n,alp,h,a,b,t1,t2)
  Scorecovp.df   = covpASC(n,alp,h,a,b,t1,t2)

  nndf$mcp=Scorecovp.df$mcpAS
  nndf$micp=Scorecovp.df$micpAS
  nndf$t1=t1
  nndf$t2=t2
  nndf$alp=alp

  ggplot2::ggplot(nndf, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(title = "Coverage Probability of the adjusted Score method") +
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=mcp,color="Mean Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::guides(colour = ggplot2::guide_legend("Heading")) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)

}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpasc`

```python
    def _plot(n, alp, h, a, b, t1, t2, seed=None):
        curve = _adj_curve(method, n, alp, h, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpatw`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpatw
```

**In plain words** — Plots the coverage-probability curve against *p* for the adjusted Wald-T interval — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovpatw(20, 0.05, 2, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/213.CoverageProb_ADJ_All_Graph.R` (line 399)](https://github.com/RajeswaranV/proportion/blob/master/R/213.CoverageProb_ADJ_All_Graph.R#L399), function `PlotcovpATW`

```r
PlotcovpATW<-function(n,alp,h,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL

  #### Calling functions and creating df
  nndf    = gcovpATW(n,alp,h,a,b,t1,t2)
  AdWaldcovp.df  = covpATW(n,alp,h,a,b,t1,t2)

  nndf$mcp=AdWaldcovp.df$mcpATW
  nndf$micp=AdWaldcovp.df$micpATW
  nndf$t1=t1
  nndf$t2=t2
  nndf$alp=alp

  ggplot2::ggplot(nndf, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(title = "Coverage Probability of the adjusted Wald-T method") +
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=mcp,color="Mean Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::guides(colour = ggplot2::guide_legend("Heading")) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)

}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpatw`

```python
    def _plot(n, alp, h, a, b, t1, t2, seed=None):
        curve = _adj_curve(method, n, alp, h, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpawd`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpawd
```

**In plain words** — Plots the coverage-probability curve against *p* for the adjusted Wald (normal-approximation) interval — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovpawd(20, 0.05, 2, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/213.CoverageProb_ADJ_All_Graph.R` (line 84)](https://github.com/RajeswaranV/proportion/blob/master/R/213.CoverageProb_ADJ_All_Graph.R#L84), function `PlotcovpAWD`

```r
PlotcovpAWD<-function(n,alp,h,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL

  #### Calling functions and creating df
  Waldcovp.df    = covpAWD(n,alp,h,a,b,t1,t2)
  nndf    = gcovpAWD(n,alp,h,a,b,t1,t2)
  nndf$t1=t1
  nndf$t2=t2
  nndf$alp=alp

  nndf$mcp=Waldcovp.df$mcpAW
  nndf$micp=Waldcovp.df$micpAW

  ggplot2::ggplot(nndf, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(title = "Coverage Probability of the adjusted Wald method") +
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=mcp,color="Mean Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::guides(colour = ggplot2::guide_legend("Heading")) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)

}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpawd`

```python
    def _plot(n, alp, h, a, b, t1, t2, seed=None):
        curve = _adj_curve(method, n, alp, h, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpba`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpba
```

**In plain words** — Plots the coverage-probability curve against *p* for the Bayesian credible interval — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovpba(20, 0.05, 1, 1, 0.9, 0.97, 1, 1, seed=0)
```

**R source** — [`R/202.CoverageProb_BASE_All_Graph.R` (line 111)](https://github.com/RajeswaranV/proportion/blob/master/R/202.CoverageProb_BASE_All_Graph.R#L111), function `PlotcovpBA`

```r
PlotcovpBA<-function(n,alp,a,b,t1,t2,a1,a2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if (missing(a1)) stop("'a1' is missing")
  if (missing(a2)) stop("'a2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")
  if ((class(a1) != "integer") & (class(a1) != "numeric") || length(a1)>1 || a1<0  ) stop("'a1' has to be greater than or equal to 0")
  if ((class(a2) != "integer") & (class(a2) != "numeric") || length(a2)>1 || a2<0  ) stop("'a2' has to be greater than or equal to 0")
  ID=method=Value=hp=cp=cpp=mcpBAQ=micpBAQ=mcpBAH=micpBAH=NULL

####INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
LBAQ=0
UBAQ=0
LBAH=0
UBAH=0
s=5000
cpBAQ=matrix(0,k,s)
ctBAQ=matrix(0,k,s)							#Cover Pbty quantity in sum
cppBAQ=0								#Coverage probabilty
ctr=0

cpBAH=matrix(0,k,s)
ctBAH=matrix(0,k,s)							#Cover Pbty quantity in sum
cppBAH=0								#Coverage probabilty
ctrH=0

##############
#library(TeachingDemos)				#To get HPDs
for(i in 1:k)
{
#Quantile Based Intervals
LBAQ[i]=stats::qbeta(alp/2,x[i]+a1,n-x[i]+a2)
UBAQ[i]=stats::qbeta(1-(alp/2),x[i]+a1,n-x[i]+a2)

LBAH[i]=TeachingDemos::hpd(stats::qbeta,shape1=x[i]+a1,shape2=n-x[i]+a2,conf=1-alp)[1]
UBAH[i]=TeachingDemos::hpd(stats::qbeta,shape1=x[i]+a1,shape2=n-x[i]+a2,conf=1-alp)[2]

}
####COVERAGE PROBABILITIES
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
if(hp[j] > LBAQ[i] && hp[j] < UBAQ[i])
{
cpBAQ[i,j]=stats::dbinom(i-1, n,hp[j])
ctBAQ[i,j]=1
}
if(hp[j] > LBAH[i] && hp[j] < UBAH[i])
{
cpBAH[i,j]=stats::dbinom(i-1, n,hp[j])
ctBAH[i,j]=1
}

}
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpba`

```python
def plotcovpba(n, alp, a, b, t1, t2, a1, a2, seed=None):
    """Coverage curves for the Bayesian credible interval, quantile+HPD (R PlotcovpBA)."""
    ba = ciba(n, alp, a1, a2)
    hp = _beta_hp(a, b, seed)
    curve = pd.concat([
        _coverage_curve(n, ba['LBAQ'], ba['UBAQ'], hp, "Quantile"),
        _coverage_curve(n, ba['LBAH'], ba['UBAH'], hp, "HPD"),
    ], ignore_index=True)
    return _covp_plot(curve, alp, t1, t2,
                      "Coverage Probability for Bayesian method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; uses SciPy HPD (`_hpd.hpd_beta`); lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpcall`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpcall
```

**In plain words** — Plots the coverage-probability curve against *p* for all continuity-corrected interval methods — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovpcall(20, 0.05, 0.02, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/222.CoverageProb_CC_All_Graph.R` (line 20)](https://github.com/RajeswaranV/proportion/blob/master/R/222.CoverageProb_CC_All_Graph.R#L20), function `PlotcovpCAll`

```r
PlotcovpCAll<-function(n,alp,c,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL


  #### Calling functions and creating df
  df1    = gcovpCWD(n,alp,c,a,b,t1,t2)
  df2    = gcovpCAS(n,alp,c,a,b,t1,t2)
  df3    = gcovpCSC(n,alp,c,a,b,t1,t2)
  df4    = gcovpCLT(n,alp,c,a,b,t1,t2)
  df5    = gcovpCTW(n,alp,c,a,b,t1,t2)

  g.df= rbind(df1,df2,df3,df4,df5)
  g.df$t1=t1
  g.df$t2=t2
  g.df$alp=alp

  ggplot2::ggplot(g.df, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(title = "Coverage Probability of Continuity corrected methods") +
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)

}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpcall`

```python
def plotcovpcall(n, alp, c, a, b, t1, t2, seed=None):
    """Coverage curves for all five CC methods overlaid (R PlotcovpCAll)."""
    import pandas as pd
    curve = pd.concat(
        [_cc_curve(m, n, alp, c, a, b, seed) for m in _CC], ignore_index=True)
    return _covp_plot(curve, alp, t1, t2,
                      "Coverage Probability for all continuity-corrected methods")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpcas`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpcas
```

**In plain words** — Plots the coverage-probability curve against *p* for the continuity-corrected ArcSine (variance-stabilised) interval — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovpcas(20, 0.05, 0.02, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/222.CoverageProb_CC_All_Graph.R` (line 145)](https://github.com/RajeswaranV/proportion/blob/master/R/222.CoverageProb_CC_All_Graph.R#L145), function `PlotcovpCAS`

```r
PlotcovpCAS<-function(n,alp,c,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL

  #### Calling functions and creating df
  df1    = gcovpCAS(n,alp,c,a,b,t1,t2)
  ArcSinecovpA.df = covpCAS(n,alp,c,a,b,t1,t2)

  df1$mcp=ArcSinecovpA.df$mcpCA
  df1$micp=ArcSinecovpA.df$micpCA
  df1$t1=t1
  df1$t2=t2
  df1$alp=alp

  ggplot2::ggplot(df1, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(title = "Coverage Probability of Continuity corrected ArcSine method") +
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=mcp,color="Mean Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::guides(colour = ggplot2::guide_legend("Heading")) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)

}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpcas`

```python
    def _plot(n, alp, c, a, b, t1, t2, seed=None):
        curve = _cc_curve(method, n, alp, c, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for continuity-corrected {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpclt`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpclt
```

**In plain words** — Plots the coverage-probability curve against *p* for the continuity-corrected Logit-Wald interval — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovpclt(20, 0.05, 0.02, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/222.CoverageProb_CC_All_Graph.R` (line 271)](https://github.com/RajeswaranV/proportion/blob/master/R/222.CoverageProb_CC_All_Graph.R#L271), function `PlotcovpCLT`

```r
PlotcovpCLT<-function(n,alp,c,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL

  #### Calling functions and creating df
  df1    = gcovpCLT(n,alp,c,a,b,t1,t2)
  WaldLcovpA.df   = covpCLT(n,alp,c,a,b,t1,t2)

  df1$mcp=WaldLcovpA.df$mcpCLT
  df1$micp=WaldLcovpA.df$micpCLT
  df1$t1=t1
  df1$t2=t2
  df1$alp=alp

  ggplot2::ggplot(df1, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(title = "Coverage Probability of Continuity corrected Logistic Wald method") +
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=mcp,color="Mean Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::guides(colour = ggplot2::guide_legend("Heading")) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)


}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpclt`

```python
    def _plot(n, alp, c, a, b, t1, t2, seed=None):
        curve = _cc_curve(method, n, alp, c, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for continuity-corrected {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpcsc`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpcsc
```

**In plain words** — Plots the coverage-probability curve against *p* for the continuity-corrected Score / Wilson interval — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovpcsc(20, 0.05, 0.02, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/222.CoverageProb_CC_All_Graph.R` (line 208)](https://github.com/RajeswaranV/proportion/blob/master/R/222.CoverageProb_CC_All_Graph.R#L208), function `PlotcovpCSC`

```r
PlotcovpCSC<-function(n,alp,c,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL

  #### Calling functions and creating df
  df1    = gcovpCSC(n,alp,c,a,b,t1,t2)
  ScorecovpA.df   = covpCSC(n,alp,c,a,b,t1,t2)

  df1$mcp=ScorecovpA.df$mcpCS
  df1$micp=ScorecovpA.df$micpCS
  df1$t1=t1
  df1$t2=t2
  df1$alp=alp

  ggplot2::ggplot(df1, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(title = "Coverage Probability of Continuity corrected Score method") +
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=mcp,color="Mean Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::guides(colour = ggplot2::guide_legend("Heading")) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)

}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpcsc`

```python
    def _plot(n, alp, c, a, b, t1, t2, seed=None):
        curve = _cc_curve(method, n, alp, c, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for continuity-corrected {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpctw`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpctw
```

**In plain words** — Plots the coverage-probability curve against *p* for the continuity-corrected Wald-T interval — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovpctw(20, 0.05, 0.02, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/222.CoverageProb_CC_All_Graph.R` (line 336)](https://github.com/RajeswaranV/proportion/blob/master/R/222.CoverageProb_CC_All_Graph.R#L336), function `PlotcovpCTW`

```r
PlotcovpCTW<-function(n,alp,c,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL

  #### Calling functions and creating df
  df1    = gcovpCTW(n,alp,c,a,b,t1,t2)

  AdWaldcovpA.df  = covpCTW(n,alp,c,a,b,t1,t2)

  df1$mcp=AdWaldcovpA.df$mcpCTW
  df1$micp=AdWaldcovpA.df$micpCTW
  df1$t1=t1
  df1$t2=t2
  df1$alp=alp

ggplot2::ggplot(df1, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(title = "Coverage Probability of Continuity corrected Wald-T method") +
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=mcp,color="Mean Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::guides(colour = ggplot2::guide_legend("Heading")) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)

}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpctw`

```python
    def _plot(n, alp, c, a, b, t1, t2, seed=None):
        curve = _cc_curve(method, n, alp, c, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for continuity-corrected {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpcwd`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpcwd
```

**In plain words** — Plots the coverage-probability curve against *p* for the continuity-corrected Wald (normal-approximation) interval — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovpcwd(20, 0.05, 0.02, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/222.CoverageProb_CC_All_Graph.R` (line 83)](https://github.com/RajeswaranV/proportion/blob/master/R/222.CoverageProb_CC_All_Graph.R#L83), function `PlotcovpCWD`

```r
PlotcovpCWD<-function(n,alp,c,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL

  #### Calling functions and creating df
  df1    = gcovpCWD(n,alp,c,a,b,t1,t2)
  WaldcovpA.df    = covpCWD(n,alp,c,a,b,t1,t2)
  df1$mcp=WaldcovpA.df$mcpCW
  df1$micp=WaldcovpA.df$micpCW
  df1$t1=t1
  df1$t2=t2
  df1$alp=alp

  ggplot2::ggplot(df1, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(title = "Coverage Probability of Continuity corrected Wald method") +
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=mcp,color="Mean Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::guides(colour = ggplot2::guide_legend("Heading")) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)

}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpcwd`

```python
    def _plot(n, alp, c, a, b, t1, t2, seed=None):
        curve = _cc_curve(method, n, alp, c, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for continuity-corrected {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpex`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpex
```

**In plain words** — Plots the coverage-probability curve against *p* for the Exact (Clopper-Pearson / mid-p) interval — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovpex(20, 0.05, 0.5, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/202.CoverageProb_BASE_All_Graph.R` (line 25)](https://github.com/RajeswaranV/proportion/blob/master/R/202.CoverageProb_BASE_All_Graph.R#L25), function `PlotcovpEX`

```r
PlotcovpEX=function(n,alp,e,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(e)) stop("'e' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(e) != "integer") & (class(e) != "numeric") || any(e>1) || any(e<0)) stop("'e' has to be between 0 and 1")
  if (length(e)>10 ) stop("Plot of only 10 intervals of 'e' is possible")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")
  method=Value=hp=cp=cpp=mcp=micp=NULL

  if(length(e)>1){
    dfex=gcovpEX(n,alp,e,a,b,t1,t2)
    exdf=dfex[,c(1,2,5)]
    exdf$e=as.factor(exdf$e)
    exdf$t1=t1
    exdf$t2=t2
    exdf$alp=alp

ggplot2::ggplot(exdf, ggplot2::aes(x=hp, y=cpp))+
  ggplot2::labs(y = "Coverage Probability") +
  ggplot2::labs(title = "Coverage Probability for exact method for multiple e values") +
  ggplot2::labs(x = "p") +
  ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
  ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
  ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
  ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
  ggplot2::geom_line(ggplot2::aes(color=e)) +
  ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)
  }
  else{
    dfex=gcovpEX(n,alp,e,a,b,t1,t2)
dfex1=data.frame(micp=dfex$micpEX[1]	,mcp=dfex$mcpEX[1]	)
dfex1$alp=alp

ggplot2::ggplot(dfex, ggplot2::aes(x=hp, y=cpp))+
  ggplot2::labs(title = "Coverage Probability of exact method") +
  ggplot2::labs(y = "Coverage Probability") +
  ggplot2::labs(x = "p") +
  ggplot2::geom_line(ggplot2::aes(color="Coverage Probability"))+
  ggplot2::geom_point(ggplot2::aes(color="CP Values"))+
  ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp),color="Confidence Level"),linetype = 2)+
  ggplot2::geom_hline(data=dfex1,ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
  ggplot2::geom_hline(data=dfex1,ggplot2::aes(yintercept=mcp,color="Mean Coverage"))+
  ggplot2::scale_colour_manual(name='Heading',
                               values=c('Coverage Probability'='red',
                                        'CP Values'='red',
                                        'Minimum Coverage'='black',
                                        'Mean Coverage'='blue',
                                        'Confidence Level'='brown'),
                               guide='legend') +
  ggplot2::guides(colour = ggplot2::guide_legend(override.aes = list(linetype=c(2,1,1,1,1),
                                                                     shape=c(NA, NA, 16,NA,NA))))


}
}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpex`

```python
def plotcovpex(n, alp, e, a, b, t1, t2, seed=None):
    """Coverage curve for the Exact interval (R PlotcovpEX)."""
    df = ciex(n, alp, [e])
    curve = _coverage_curve(n, df['LEX'], df['UEX'], _beta_hp(a, b, seed), "Exact")
    return _covp_plot(curve, alp, t1, t2,
                      "Coverage Probability for Exact method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpgen`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpgen
```

**In plain words** — Plots the coverage-probability curve against *p* for user-supplied interval limits — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
wd = bk.ciwd(20, 0.05)
bk.plotcovpgen(20, wd["LWD"].values, wd["UWD"].values, 0.05, [0.2, 0.5, 0.8], 0.9, 0.97)
```

**R source** — [`R/224.CoverageProb_GENERAL_GIVEN_p.R` (line 120)](https://github.com/RajeswaranV/proportion/blob/master/R/224.CoverageProb_GENERAL_GIVEN_p.R#L120), function `PlotcovpGEN`

```r
PlotcovpGEN<-function(n,LL,UL,alp,hp,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(LL)) stop("'Lower limit' is missing")
  if (missing(UL)) stop("'Upper Limit' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(hp)) stop("'hp' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if ((class(LL) != "integer") & (class(LL) != "numeric") || any(LL < 0)) stop("'LL' has to be a set of positive numeric vectors")
  if ((class(UL) != "integer") & (class(UL) != "numeric") || any(UL < 0)) stop("'UL' has to be a set of positive numeric vectors")
  if (length(LL) <= n ) stop("Length of vector LL has to be greater than n")
  if (length(UL) <= n ) stop("Length of vector UL has to be greater than n")
  if (any(LL[0:n+1] > UL[0:n+1] )) stop("LL value have to be lower than the corrosponding UL value")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (any(hp>1) || any(hp<0) ) stop("'hp' has to be between 0 and 1")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")
  ID=method=Value=cp=cpp=mcp=micp=NULL

  ####INPUT n
 # x=0:n
  k=n+1
  s=length(hp)
  cp=matrix(0,k,s)
  ct=matrix(0,k,s)							#Cover Pbty quantity in sum
  cpp=0								#Coverage probabilty
  ctr=0
  ###CRITICAL VALUES
  #cv=qnorm(1-(alp/2), mean = 0, sd = 1)
  ####COVERAGE PROBABILITIES
  for (j in 1:s)
  {
    for(i in 1:k)
    {
      if(hp[j] > LL[i] && hp[j] < UL[i])
      {
        cp[i,j]=stats::dbinom(i-1, n,hp[j])
        ct[i,j]=1
      }
    }
    cpp[j]=sum(cp[,j])
    if(t1<cpp[j]&&cpp[j]<t2) ctr=ctr+1		#tolerance for cov prob - user defined
  }
  CP=data.frame(hp,cpp)
  CP$mcp=mean(cpp)
  CP$micp=min(cpp)					#Mean Cov Prob


ggplot2::ggplot(CP, ggplot2::aes(x=hp, y=cpp))+
  ggplot2::labs(y = "Coverage Probability") +
  ggplot2::labs(x = "p") +
  ggplot2::labs(title = "Coverage Probability - General method") +
  ggplot2::geom_line(ggplot2::aes(color="Coverage Probability"))+
  ggplot2::geom_point(ggplot2::aes(color="CP Values"))+
  ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
  ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
  ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
  ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
  ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp),color="Confidence Level"),linetype = 2)+
  ggplot2::geom_hline(ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
  ggplot2::geom_hline(ggplot2::aes(yintercept=mcp,color="Mean Coverage"))+
  ggplot2::scale_colour_manual(name='Heading',
                        values=c('Coverage Probability'='red',
                                 'CP Values'='red',
                                 'Minimum Coverage'='black',
                                 'Mean Coverage'='blue',
                                 'Confidence Level'='brown'),
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpgen`

```python
def plotcovpgen(n, LL, UL, alp, hp, t1, t2):
    """Coverage curve for user-supplied limits over given hp (R PlotcovpGEN)."""
    _check_limits(n, LL, UL, alp, t1, t2)
    hp = np.atleast_1d(np.asarray(hp, dtype=float))
    curve = _coverage_curve(n, LL, UL, hp, "Given")
    return _covp_plot(curve, alp, t1, t2, "Coverage Probability (given p)")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovplr`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovplr
```

**In plain words** — Plots the coverage-probability curve against *p* for the Likelihood-Ratio interval — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovplr(20, 0.05, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/202.CoverageProb_BASE_All_Graph.R` (line 417)](https://github.com/RajeswaranV/proportion/blob/master/R/202.CoverageProb_BASE_All_Graph.R#L417), function `PlotcovpLR`

```r
PlotcovpLR<-function(n,alp,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL

  ####INPUT n
  LRcovp.df      = covpLR(n,alp,a,b,t1,t2)
 # ss1 = data.frame(method = LRcovp.df$method, MeanCP=LRcovp.df$mcpL, MinCP= LRcovp.df$micpL, RMSE_N=LRcovp.df$RMSE_N,RMSE_M=LRcovp.df$RMSE_M,RMSE_MI=LRcovp.df$RMSE_MI,tol=LRcovp.df$tol)

  nndf=gcovpL(n,alp,a,b,t1,t2)
  nndf$mcp=LRcovp.df$mcpL
  nndf$micp=LRcovp.df$micpL
  nndf$t1=t1
  nndf$t2=t2
  nndf$alp=alp

  ggplot2::ggplot(nndf, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(title = "Coverage Probability for Likelihood Ratio method") +
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::geom_hline(ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=mcp,color="Mean Coverage"))+
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::guides(colour = ggplot2::guide_legend("Heading"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)

}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovplr`

```python
    def _plot(n, alp, a, b, t1, t2, seed=None):
        curve = _base_curve(method, n, alp, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovplt`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovplt
```

**In plain words** — Plots the coverage-probability curve against *p* for the Logit-Wald interval — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovplt(20, 0.05, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/202.CoverageProb_BASE_All_Graph.R` (line 537)](https://github.com/RajeswaranV/proportion/blob/master/R/202.CoverageProb_BASE_All_Graph.R#L537), function `PlotcovpLT`

```r
PlotcovpLT<-function(n,alp,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL

  ####INPUT n
  WaldLcovp.df   = covpLT(n,alp,a,b,t1,t2)

  nndf=gcovpLT(n,alp,a,b,t1,t2)
  nndf$mcp=WaldLcovp.df$mcpLT
  nndf$micp=WaldLcovp.df$micpLT
  nndf$t1=t1
  nndf$t2=t2
  nndf$alp=alp

  ggplot2::ggplot(nndf, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(title = "Coverage Probability for Logit Wald method") +
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::geom_hline(ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=mcp,color="Mean Coverage"))+
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::guides(colour = ggplot2::guide_legend("Heading"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)

}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovplt`

```python
    def _plot(n, alp, a, b, t1, t2, seed=None):
        curve = _base_curve(method, n, alp, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpsc`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpsc
```

**In plain words** — Plots the coverage-probability curve against *p* for the Score / Wilson interval — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovpsc(20, 0.05, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/202.CoverageProb_BASE_All_Graph.R` (line 477)](https://github.com/RajeswaranV/proportion/blob/master/R/202.CoverageProb_BASE_All_Graph.R#L477), function `PlotcovpSC`

```r
PlotcovpSC<-function(n,alp,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL

  ####INPUT n
  Scorecovp.df   = covpSC(n,alp,a,b,t1,t2)
  #ss1 = data.frame( MeanCP=Scorecovp.df$mcpS, MinCP= Scorecovp.df$micpS, RMSE_N=Scorecovp.df$RMSE_N,RMSE_M=Scorecovp.df$RMSE_M,RMSE_MI=Scorecovp.df$RMSE_MI,tol=Scorecovp.df$tol)

  nndf=gcovpS(n,alp,a,b,t1,t2)
  nndf$mcp=Scorecovp.df$mcpS
  nndf$micp=Scorecovp.df$micpS
  nndf$t1=t1
  nndf$t2=t2
  nndf$alp=alp

  ggplot2::ggplot(nndf, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(title = "Coverage Probability for Score method") +
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::geom_hline(ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=mcp,color="Mean Coverage"))+
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::guides(colour = ggplot2::guide_legend("Heading"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)

}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpsc`

```python
    def _plot(n, alp, a, b, t1, t2, seed=None):
        curve = _base_curve(method, n, alp, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpsim`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpsim
```

**In plain words** — Plots the coverage-probability curve against *p* for user-supplied limits over simulated p — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
wd = bk.ciwd(20, 0.05)
bk.plotcovpsim(20, wd["LWD"].values, wd["UWD"].values, 0.05, 1000, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/225.CoverageProb_GENERAL_SIMULATEDp.R` (line 123)](https://github.com/RajeswaranV/proportion/blob/master/R/225.CoverageProb_GENERAL_SIMULATEDp.R#L123), function `PlotcovpSIM`

```r
PlotcovpSIM<-function(n,LL,UL,alp,s,a,b,t1,t2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(LL)) stop("'Lower limit' is missing")
  if (missing(UL)) stop("'Upper Limit' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(s)) stop("'s' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(t1)) stop("'t1' is missing")
  if (missing(t2)) stop("'t2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if ((class(LL) != "integer") & (class(LL) != "numeric") || any(LL < 0)) stop("'LL' has to be a set of positive numeric vectors")
  if ((class(UL) != "integer") & (class(UL) != "numeric") || any(UL < 0)) stop("'UL' has to be a set of positive numeric vectors")
  if (length(LL) <= n ) stop("Length of vector LL has to be greater than n")
  if (length(UL) <= n ) stop("Length of vector UL has to be greater than n")
  if (any(LL[0:n+1] > UL[0:n+1] )) stop("LL value have to be lower than the corrosponding UL value")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(s) != "integer") & (class(s) != "numeric") || length(s)>1 || s<1  ) stop("'b' has to be greater than or equal to 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if (t1>t2) stop(" t1 has to be lesser than t2")
  if ((class(t1) != "integer") & (class(t1) != "numeric") || length(t1)>1 || t1<0 || t1>1 ) stop("'t1' has to be between 0 and 1")
  if ((class(t2) != "integer") & (class(t2) != "numeric") || length(t2)>1 || t2<0 || t2>1 ) stop("'t2' has to be between 0 and 1")
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL

  ####INPUT n
  x=0:n
  k=n+1

  cp=matrix(0,k,s)
  ct=matrix(0,k,s)							#Cover Pbty quantity in sum
  cpp=0								#Coverage probabilty
  ctr=0
  ###CRITICAL VALUES
  cv=stats::qnorm(1-(alp/2), mean = 0, sd = 1)
  ####COVERAGE PROBABILITIES
  hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
  for (j in 1:s)
  {
    for(i in 1:k)
    {
      if(hp[j] > LL[i] && hp[j] < UL[i])
      {
        cp[i,j]=stats::dbinom(i-1, n,hp[j])
        ct[i,j]=1
      }
    }
    cpp[j]=sum(cp[,j])
    if(t1<cpp[j]&&cpp[j]<t2) ctr=ctr+1		#tolerance for cov prob - user defined
  }
  CP=data.frame(hp,cpp)
  CP$mcp=mean(cpp)
  CP$micp=min(cpp)					#Mean Cov Prob

ggplot2::ggplot(CP, ggplot2::aes(x=hp,
                                 y=cpp,
                                 color = ggplot2::guide_legend(override.aes = list(linetype=c(2,1,1,1,1),
                                                                  shape=c(NA, NA, 16,NA,NA)))))+
  ggplot2::labs(y = "Coverage Probability") +
  ggplot2::labs(x = "p") +
  ggplot2::labs(title = "Coverage Probability using simulation") +
  ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
  ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
  ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
  ggplot2::geom_text(ggplot2::aes(y=t2, label="\nHigher tolerance(t2)", x=.1), colour="blue") +
  ggplot2::geom_line(ggplot2::aes(color="Coverage Probability"))+
  ggplot2::geom_point(ggplot2::aes(color="CP Values"))+
  ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp),color="Confidence Level"),linetype = 2)+
  ggplot2::geom_hline(ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpsim`

```python
def plotcovpsim(n, LL, UL, alp, s, a, b, t1, t2, seed=None):
    """Coverage curve for user-supplied limits over simulated hp (R PlotcovpSIM)."""
    _check_limits(n, LL, UL, alp, t1, t2)
    hp = np.sort(np.random.default_rng(seed).beta(a, b, int(s)))
    curve = _coverage_curve(n, LL, UL, hp, "Simulated")
    return _covp_plot(curve, alp, t1, t2, "Coverage Probability (simulated p)")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovptw`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovptw
```

**In plain words** — Plots the coverage-probability curve against *p* for the Wald-T interval — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovptw(20, 0.05, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/202.CoverageProb_BASE_All_Graph.R` (line 596)](https://github.com/RajeswaranV/proportion/blob/master/R/202.CoverageProb_BASE_All_Graph.R#L596), function `PlotcovpTW`

```r
PlotcovpTW<-function(n,alp,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL

  ####INPUT n
  AdWaldcovp.df  = covpTW(n,alp,a,b,t1,t2)

  nndf=gcovpTW(n,alp,a,b,t1,t2)
  nndf$mcp=AdWaldcovp.df$mcpTW
  nndf$micp=AdWaldcovp.df$micpTW
  nndf$t1=t1
  nndf$t2=t2
  nndf$alp=alp

  ggplot2::ggplot(nndf, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(title = "Coverage Probability for Wald-T method") +
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::geom_hline(ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=mcp,color="Mean Coverage"))+
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::guides(colour = ggplot2::guide_legend("Heading"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)

}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovptw`

```python
    def _plot(n, alp, a, b, t1, t2, seed=None):
        curve = _base_curve(method, n, alp, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcovpwd`

```{eval-rst}
.. autofunction:: binomcikit.covp.plots.plotcovpwd
```

**In plain words** — Plots the coverage-probability curve against *p* for the Wald (normal-approximation) interval — a visualisation of the corresponding `coverage probability` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotcovpwd(20, 0.05, 1, 1, 0.9, 0.97, seed=0)
```

**R source** — [`R/202.CoverageProb_BASE_All_Graph.R` (line 300)](https://github.com/RajeswaranV/proportion/blob/master/R/202.CoverageProb_BASE_All_Graph.R#L300), function `PlotcovpWD`

```r
PlotcovpWD<-function(n,alp,a,b,t1,t2)
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
  ID=method=Value=hp=cp=cpp=mcp=micp=NULL

  ####INPUT n
  Waldcovp.df    = covpWD(n,alp,a,b,t1,t2)

  nndf=gcovpW(n,alp,a,b,t1,t2)
  nndf$mcp=Waldcovp.df$mcpW
  nndf$micp=Waldcovp.df$micpW
  nndf$t1=t1
  nndf$t2=t2
  nndf$alp=alp

  ggplot2::ggplot(nndf, ggplot2::aes(x=hp, y=cp))+
    ggplot2::labs(title = "Coverage Probability for Wald method") +
    ggplot2::labs(y = "Coverage Probability") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t1), color="red",linetype = 2) +
    ggplot2::geom_hline(ggplot2::aes(yintercept=t2), color="blue",linetype = 2) +
    ggplot2::geom_text(ggplot2::aes(y=t1, label="\nLower tolerance(t1)", x=.1), colour="red") +
    ggplot2::geom_text(ggplot2::aes(y=t2, label="Higher tolerance(t2)", x=.1), colour="blue") +
    ggplot2::geom_hline(ggplot2::aes(yintercept=micp,color="Minimum Coverage"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=mcp,color="Mean Coverage"))+
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::guides(colour = ggplot2::guide_legend("Heading"))+
    ggplot2::geom_hline(ggplot2::aes(yintercept=1-(alp)),linetype = 2)

}
```

**What the R code does** — The R function calls the numeric function and draws the coverage-probability curve against *p* with ggplot2.

**Python source** — `binomcikit.covp.plots.plotcovpwd`

```python
    def _plot(n, alp, a, b, t1, t2, seed=None):
        curve = _base_curve(method, n, alp, a, b, seed)
        return _covp_plot(curve, alp, t1, t2,
                          f"Coverage Probability for {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

