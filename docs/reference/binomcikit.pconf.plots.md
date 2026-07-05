<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `pconf.plots`

```{eval-rst}
.. module:: binomcikit.pconf.plots
```

This module computes **p-confidence and p-bias** — deterministic (no-simulation) measures of how well each interval's actual confidence matches its nominal level, for **plots** of the results (returning plotnine `ggplot` objects). See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `plotpcopbiaall`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbiaall
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for all adjusted interval methods — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbiaall(20, 0.05, 2)
```

**R source** — [`R/412.p-Confidence_p-Bias_ADJ_All_Graph.R` (line 17)](https://github.com/RajeswaranV/proportion/blob/master/R/412.p-Confidence_p-Bias_ADJ_All_Graph.R#L17), function `PlotpCOpBIAAll`

```r
PlotpCOpBIAAll<-function(n,alp,h)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h) >1|| h<0  || !(h%%1 ==0)) stop("'h' has to be an integer greater than or equal to 0")
  x=Value=Heading=val=mark=NULL

  nAll = pCOpBIAAll(n,alp,h)
  pc=data.frame(x=nAll$x1, val=nAll$pconf, Heading=nAll$method, mark="pconf",minmax=min(nAll$pbias, nAll$pconf))
  pb=data.frame(x=nAll$x1, val=nAll$pbias, Heading=nAll$method, mark="pbias",minmax=max(nAll$pbias, nAll$pconf))
  nndf=rbind(pc,pb)
  cdfWDc = subset(nndf, Heading == "Adj-Wald" & mark== "pconf")
  cdfWDb = subset(nndf, Heading == "Adj-Wald" & mark== "pbias")
  cdfSCc = subset(nndf, Heading == "Adj-Score" & mark== "pconf")
  cdfSCb = subset(nndf, Heading == "Adj-Score" & mark== "pbias")
  cdfASc = subset(nndf, Heading == "Adj-ArcSine" & mark== "pconf")
  cdfASb = subset(nndf, Heading == "Adj-ArcSine" & mark== "pbias")
  cdfLTc = subset(nndf, Heading == "Adj-Logit-Wald" & mark== "pconf")
  cdfLTb = subset(nndf, Heading == "Adj-Logit-Wald" & mark== "pbias")
  cdfLRc = subset(nndf, Heading == "Adj-Likelihood" & mark== "pconf")
  cdfLRb = subset(nndf, Heading == "Adj-Likelihood" & mark== "pbias")
  cdfTWc = subset(nndf, Heading == "Adj-Wald-T" & mark== "pconf")
  cdfTWb = subset(nndf, Heading == "Adj-Wald-T" & mark== "pbias")

  ggplot2::ggplot(nndf, ggplot2::aes(x=x, y=val))+
    ggplot2::labs(title = "p-Confidence & p-Bias - Adjusted methods") +
    ggplot2::facet_wrap(Heading ~ mark,scales="free_y",ncol=2) +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=cdfWDc,ggplot2::aes(color="pConf Adj-Wald"))+
    ggplot2::geom_point(data=cdfWDc, ggplot2::aes(color="pConf Adj-Wald Values"),shape=22)+
    ggplot2::geom_line(data=cdfWDb,ggplot2::aes(color="pbias Adj-Wald"))+
    ggplot2::geom_point(data=cdfWDb,ggplot2::aes(color="pbias Adj-Wald Values"),shape=23)+
    ggplot2::geom_line(data=cdfSCc,ggplot2::aes(color="pConf Adj-Score"))+
    ggplot2::geom_point(data=cdfSCc, ggplot2::aes(color="pConf Adj-Score Values"),shape=21)+
    ggplot2::geom_line(data=cdfSCb,ggplot2::aes(color="pbias Adj-Score"))+
    ggplot2::geom_point(data=cdfSCb,ggplot2::aes(color="pbias Adj-Score Values"),shape=16)+
    ggplot2::geom_line(data=cdfASc,ggplot2::aes(color="pConf Adj-ArcSine"))+
    ggplot2::geom_point(data=cdfASc, ggplot2::aes(color="pConf Adj-ArcSine Values"),shape=22)+
    ggplot2::geom_line(data=cdfASb,ggplot2::aes(color="pbias Adj-ArcSine"))+
    ggplot2::geom_point(data=cdfASb,ggplot2::aes(color="pbias Adj-ArcSine Values"),shape=23)+
    ggplot2::geom_line(data=cdfTWc,ggplot2::aes(color="pConf Adj-Wald-T"))+
    ggplot2::geom_point(data=cdfTWc, ggplot2::aes(color="pConf Adj-Wald-T Values"),shape=21)+
    ggplot2::geom_line(data=cdfTWb,ggplot2::aes(color="pbias Adj-Wald-T"))+
    ggplot2::geom_point(data=cdfTWb,ggplot2::aes(color="pbias Adj-Wald-T Values"),shape=16)+
    ggplot2::geom_line(data=cdfLRc,ggplot2::aes(color="pConf Adj-Likelihood"))+
    ggplot2::geom_point(data=cdfLRc, ggplot2::aes(color="pConf Adj-Likelihood Values"),shape=22)+
    ggplot2::geom_line(data=cdfLRb,ggplot2::aes(color="pbias Adj-Likelihood"))+
    ggplot2::geom_point(data=cdfLRb,ggplot2::aes(color="pbias Adj-Likelihood Values"),shape=23)+
    ggplot2::geom_line(data=cdfLTc,ggplot2::aes(color="pConf Adj-Logit-Wald"))+
    ggplot2::geom_point(data=cdfLTc, ggplot2::aes(color="pConf Adj-Logit-Wald Values"),shape=21)+
    ggplot2::geom_line(data=cdfLTb,ggplot2::aes(color="pbias Adj-Logit-Wald"))+
    ggplot2::geom_point(data=cdfLTb,ggplot2::aes(color="pbias Adj-Logit-Wald Values"),shape=16)+
    ggplot2::scale_colour_manual(name='Heading',
                                 values=c(
                                   'pConf Adj-Wald'='red',
                                   'pConf Adj-Wald Values'='red',
                                   'pbias Adj-Wald'='black',
                                   'pbias Adj-Wald Values'='black',
                                   'pConf Adj-Score'='red',
                                   'pConf Adj-Score Values'='red',
                                   'pbias Adj-Score'='black',
                                   'pbias Adj-Score Values'='black',
                                   'pConf Adj-ArcSine'='red',
                                   'pConf Adj-ArcSine Values'='red',
                                   'pbias Adj-ArcSine'='black',
                                   'pbias Adj-ArcSine Values'='black',
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbiaall`

```python
def plotpcopbiaall(n, alp, h):
    """p-confidence & p-bias plot for all six adjusted methods (R PlotpCOpBIAAll)."""
    return _pconf_plot(adj_all.pcopbiaall(n, alp, h),
                       "p-Confidence & p-Bias - all adjusted methods")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbiaas`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbiaas
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for the adjusted ArcSine (variance-stabilised) interval — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbiaas(20, 0.05, 2)
```

**R source** — [`R/412.p-Confidence_p-Bias_ADJ_All_Graph.R` (line 293)](https://github.com/RajeswaranV/proportion/blob/master/R/412.p-Confidence_p-Bias_ADJ_All_Graph.R#L293), function `PlotpCOpBIAAS`

```r
PlotpCOpBIAAS<-function(n,alp,h)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n)>1 || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  x=Value=Heading=mark=NULL

  CBEX = pCOpBIAAS(n,alp,h)

  W1 = data.frame(x=CBEX$x1, Value=CBEX$pconf, Heading="pconf")
  W2 = data.frame(x=CBEX$x1, Value=CBEX$pbias, Heading="pbias")
  gdf=rbind(W1,W2)

  ggplot2::ggplot(gdf, ggplot2::aes(x=x, y=Value)) +
    ggplot2::facet_grid(Heading~.,scales="free_y") +
    ggplot2::labs(title = "p-Confidence & p-Bias - Adjusted ArcSine method") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=gdf,ggplot2::aes(x=x, y=Value))

}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbiaas`

```python
    def _plot(n, alp, h):
        return _pconf_plot(fn(n, alp, h),
                           f"p-Confidence & p-Bias - adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbiall`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbiall
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for all interval methods — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbiall(20, 0.05)
```

**R source** — [`R/402.p-Confidence_p-Bias_BASE_All_Graph.R` (line 149)](https://github.com/RajeswaranV/proportion/blob/master/R/402.p-Confidence_p-Bias_BASE_All_Graph.R#L149), function `PlotpCOpBIAll`

```r
PlotpCOpBIAll<-function(n,alp)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  x=Value=Heading=mark=val=NULL

  nAll = pCOpBIAll(n,alp)
  pc=data.frame(x=nAll$x1, val=nAll$pconf, Heading=nAll$method, mark="pconf",minmax=min(nAll$pbias, nAll$pconf))
  pb=data.frame(x=nAll$x1, val=nAll$pbias, Heading=nAll$method, mark="pbias",minmax=max(nAll$pbias, nAll$pconf))
  nndf=rbind(pc,pb)
  cdfWDc = subset(nndf, Heading == "Wald" & mark== "pconf")
  cdfWDb = subset(nndf, Heading == "Wald" & mark== "pbias")
  cdfSCc = subset(nndf, Heading == "Score" & mark== "pconf")
  cdfSCb = subset(nndf, Heading == "Score" & mark== "pbias")
  cdfASc = subset(nndf, Heading == "ArcSine" & mark== "pconf")
  cdfASb = subset(nndf, Heading == "ArcSine" & mark== "pbias")
  cdfLTc = subset(nndf, Heading == "Logit-Wald" & mark== "pconf")
  cdfLTb = subset(nndf, Heading == "Logit-Wald" & mark== "pbias")
  cdfLRc = subset(nndf, Heading == "Likelihood" & mark== "pconf")
  cdfLRb = subset(nndf, Heading == "Likelihood" & mark== "pbias")
  cdfTWc = subset(nndf, Heading == "Wald-T" & mark== "pconf")
  cdfTWb = subset(nndf, Heading == "Wald-T" & mark== "pbias")

  ggplot2::ggplot(nndf, ggplot2::aes(x=x, y=val))+
    ggplot2::labs(title = "p-Confidence & p-Bias - All methods") +
    ggplot2::facet_wrap(Heading ~ mark,scales="free_y",ncol=2) +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=cdfWDc,ggplot2::aes(color="pConf Wald"))+
    ggplot2::geom_point(data=cdfWDc, ggplot2::aes(color="pConf Wald Values"),shape=22)+
    ggplot2::geom_line(data=cdfWDb,ggplot2::aes(color="pbias Wald"))+
    ggplot2::geom_point(data=cdfWDb,ggplot2::aes(color="pbias Wald Values"),shape=23)+
       ggplot2::geom_line(data=cdfSCc,ggplot2::aes(color="pConf Score"))+
    ggplot2::geom_point(data=cdfSCc, ggplot2::aes(color="pConf Score Values"),shape=21)+
    ggplot2::geom_line(data=cdfSCb,ggplot2::aes(color="pbias Score"))+
    ggplot2::geom_point(data=cdfSCb,ggplot2::aes(color="pbias Score Values"),shape=16)+
       ggplot2::geom_line(data=cdfASc,ggplot2::aes(color="pConf ArcSine"))+
    ggplot2::geom_point(data=cdfASc, ggplot2::aes(color="pConf ArcSine Values"),shape=22)+
    ggplot2::geom_line(data=cdfASb,ggplot2::aes(color="pbias ArcSine"))+
    ggplot2::geom_point(data=cdfASb,ggplot2::aes(color="pbias ArcSine Values"),shape=23)+
       ggplot2::geom_line(data=cdfTWc,ggplot2::aes(color="pConf Wald-T"))+
    ggplot2::geom_point(data=cdfTWc, ggplot2::aes(color="pConf Wald-T Values"),shape=21)+
    ggplot2::geom_line(data=cdfTWb,ggplot2::aes(color="pbias Wald-T"))+
    ggplot2::geom_point(data=cdfTWb,ggplot2::aes(color="pbias Wald-T Values"),shape=16)+
       ggplot2::geom_line(data=cdfLRc,ggplot2::aes(color="pConf Likelihood"))+
    ggplot2::geom_point(data=cdfLRc, ggplot2::aes(color="pConf Likelihood Values"),shape=22)+
    ggplot2::geom_line(data=cdfLRb,ggplot2::aes(color="pbias Likelihood"))+
    ggplot2::geom_point(data=cdfLRb,ggplot2::aes(color="pbias Likelihood Values"),shape=23)+
       ggplot2::geom_line(data=cdfLTc,ggplot2::aes(color="pConf Logit-Wald"))+
    ggplot2::geom_point(data=cdfLTc, ggplot2::aes(color="pConf Logit-Wald Values"),shape=21)+
    ggplot2::geom_line(data=cdfLTb,ggplot2::aes(color="pbias Logit-Wald"))+
    ggplot2::geom_point(data=cdfLTb,ggplot2::aes(color="pbias Logit-Wald Values"),shape=16)+
    ggplot2::scale_colour_manual(name='Heading',
                                 values=c(
                                    'pConf Wald'='red',
                                   'pConf Wald Values'='red',
                                   'pbias Wald'='black',
                                   'pbias Wald Values'='black',
                                    'pConf Score'='red',
                                   'pConf Score Values'='red',
                                   'pbias Score'='black',
                                   'pbias Score Values'='black',
                                    'pConf ArcSine'='red',
                                   'pConf ArcSine Values'='red',
                                   'pbias ArcSine'='black',
                                   'pbias ArcSine Values'='black',
                                    'pConf Logit-Wald'='red',
                                   'pConf Logit-Wald Values'='red',
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbiall`

```python
def plotpcopbiall(n, alp):
    """p-confidence & p-bias plot for all six base methods (R PlotpCOpBIAll)."""
    return _pconf_plot(base_all.pcopbiall(n, alp),
                       "p-Confidence & p-Bias - all base methods")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbialr`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbialr
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for the adjusted Likelihood-Ratio interval — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbialr(20, 0.05, 2)
```

**R source** — [`R/412.p-Confidence_p-Bias_ADJ_All_Graph.R` (line 149)](https://github.com/RajeswaranV/proportion/blob/master/R/412.p-Confidence_p-Bias_ADJ_All_Graph.R#L149), function `PlotpCOpBIALR`

```r
PlotpCOpBIALR<-function(n,alp,h)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n)>1 || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h) >1|| h<0  || !(h%%1 ==0)) stop("'h' has to be an integer greater than or equal to 0")
  x=Value=Heading=mark=NULL

  CBEX = pCOpBIALR(n,alp,h)

  W1 = data.frame(x=CBEX$x1, Value=CBEX$pconf, Heading="pconf")
  W2 = data.frame(x=CBEX$x1, Value=CBEX$pbias, Heading="pbias")
  gdf=rbind(W1,W2)

  ggplot2::ggplot(gdf, ggplot2::aes(x=x, y=Value)) +
    ggplot2::facet_grid(Heading~.,scales="free_y") +
    ggplot2::labs(title = "p-Confidence & p-Bias - Adjusted Likelihood Ratio method") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=gdf,ggplot2::aes(x=x, y=Value))

}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbialr`

```python
    def _plot(n, alp, h):
        return _pconf_plot(fn(n, alp, h),
                           f"p-Confidence & p-Bias - adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbialt`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbialt
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for the adjusted Logit-Wald interval — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbialt(20, 0.05, 2)
```

**R source** — [`R/412.p-Confidence_p-Bias_ADJ_All_Graph.R` (line 221)](https://github.com/RajeswaranV/proportion/blob/master/R/412.p-Confidence_p-Bias_ADJ_All_Graph.R#L221), function `PlotpCOpBIALT`

```r
PlotpCOpBIALT<-function(n,alp,h)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n)>1 || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  x=Value=Heading=mark=NULL

  CBEX = pCOpBIALT(n,alp,h)

  W1 = data.frame(x=CBEX$x1, Value=CBEX$pconf, Heading="pconf")
  W2 = data.frame(x=CBEX$x1, Value=CBEX$pbias, Heading="pbias")
  gdf=rbind(W1,W2)

  ggplot2::ggplot(gdf, ggplot2::aes(x=x, y=Value)) +
    ggplot2::facet_grid(Heading~.,scales="free_y") +
    ggplot2::labs(title = "p-Confidence & p-Bias - Adjusted Logit Wald method") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=gdf,ggplot2::aes(x=x, y=Value))

}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbialt`

```python
    def _plot(n, alp, h):
        return _pconf_plot(fn(n, alp, h),
                           f"p-Confidence & p-Bias - adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbias`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbias
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for the ArcSine (variance-stabilised) interval — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbias(20, 0.05)
```

**R source** — [`R/402.p-Confidence_p-Bias_BASE_All_Graph.R` (line 320)](https://github.com/RajeswaranV/proportion/blob/master/R/402.p-Confidence_p-Bias_BASE_All_Graph.R#L320), function `PlotpCOpBIAS`

```r
PlotpCOpBIAS<-function(n,alp)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  x=Value=Heading=mark=NULL

  CBEX = pCOpBIAS(n,alp)

  W1 = data.frame(x=CBEX$x1, Value=CBEX$pconf, Heading="pconf")
  W2 = data.frame(x=CBEX$x1, Value=CBEX$pbias, Heading="pbias")
  gdf=rbind(W1,W2)

  ggplot2::ggplot(gdf, ggplot2::aes(x=x, y=Value)) +
    ggplot2::facet_grid(Heading~.,scales="free_y") +
    ggplot2::labs(title = "p-Confidence & p-Bias - ArcSine method") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=gdf,ggplot2::aes(x=x, y=Value))

}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbias`

```python
    def _plot(n, alp):
        return _pconf_plot(fn(n, alp), f"p-Confidence & p-Bias - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbiasc`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbiasc
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for the adjusted Score / Wilson interval — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbiasc(20, 0.05, 2)
```

**R source** — [`R/412.p-Confidence_p-Bias_ADJ_All_Graph.R` (line 257)](https://github.com/RajeswaranV/proportion/blob/master/R/412.p-Confidence_p-Bias_ADJ_All_Graph.R#L257), function `PlotpCOpBIASC`

```r
PlotpCOpBIASC<-function(n,alp,h)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n)>1 || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  x=Value=Heading=mark=NULL

  CBEX = pCOpBIASC(n,alp,h)

  W1 = data.frame(x=CBEX$x1, Value=CBEX$pconf, Heading="pconf")
  W2 = data.frame(x=CBEX$x1, Value=CBEX$pbias, Heading="pbias")
  gdf=rbind(W1,W2)

  ggplot2::ggplot(gdf, ggplot2::aes(x=x, y=Value)) +
    ggplot2::facet_grid(Heading~.,scales="free_y") +
    ggplot2::labs(title = "p-Confidence & p-Bias - Adjusted Score method") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=gdf,ggplot2::aes(x=x, y=Value))

}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbiasc`

```python
    def _plot(n, alp, h):
        return _pconf_plot(fn(n, alp, h),
                           f"p-Confidence & p-Bias - adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbiatw`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbiatw
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for the adjusted Wald-T interval — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbiatw(20, 0.05, 2)
```

**R source** — [`R/412.p-Confidence_p-Bias_ADJ_All_Graph.R` (line 185)](https://github.com/RajeswaranV/proportion/blob/master/R/412.p-Confidence_p-Bias_ADJ_All_Graph.R#L185), function `PlotpCOpBIATW`

```r
PlotpCOpBIATW<-function(n,alp,h)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n)>1 || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  x=Value=Heading=mark=NULL

  CBEX = pCOpBIATW(n,alp,h)

  W1 = data.frame(x=CBEX$x1, Value=CBEX$pconf, Heading="pconf")
  W2 = data.frame(x=CBEX$x1, Value=CBEX$pbias, Heading="pbias")
  gdf=rbind(W1,W2)

  ggplot2::ggplot(gdf, ggplot2::aes(x=x, y=Value)) +
    ggplot2::facet_grid(Heading~.,scales="free_y") +
    ggplot2::labs(title = "p-Confidence & p-Bias - Adjusted Wald-T method") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=gdf,ggplot2::aes(x=x, y=Value))

}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbiatw`

```python
    def _plot(n, alp, h):
        return _pconf_plot(fn(n, alp, h),
                           f"p-Confidence & p-Bias - adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbiawd`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbiawd
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for the adjusted Wald (normal-approximation) interval — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbiawd(20, 0.05, 2)
```

**R source** — [`R/412.p-Confidence_p-Bias_ADJ_All_Graph.R` (line 113)](https://github.com/RajeswaranV/proportion/blob/master/R/412.p-Confidence_p-Bias_ADJ_All_Graph.R#L113), function `PlotpCOpBIAWD`

```r
PlotpCOpBIAWD<-function(n,alp,h)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n)>1 || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  x=Value=Heading=mark=NULL

  CBEX = pCOpBIAWD(n,alp,h)

  W1 = data.frame(x=CBEX$x1, Value=CBEX$pconf, Heading="pconf")
  W2 = data.frame(x=CBEX$x1, Value=CBEX$pbias, Heading="pbias")
  gdf=rbind(W1,W2)

  ggplot2::ggplot(gdf, ggplot2::aes(x=x, y=Value)) +
    ggplot2::facet_grid(Heading~.,scales="free_y") +
    ggplot2::labs(title = "p-Confidence & p-Bias - Adjusted Wald method") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=gdf,ggplot2::aes(x=x, y=Value))

}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbiawd`

```python
    def _plot(n, alp, h):
        return _pconf_plot(fn(n, alp, h),
                           f"p-Confidence & p-Bias - adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbiba`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbiba
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for the Bayesian credible interval — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbiba(20, 0.05, 1, 1)
```

**R source** — [`R/402.p-Confidence_p-Bias_BASE_All_Graph.R` (line 83)](https://github.com/RajeswaranV/proportion/blob/master/R/402.p-Confidence_p-Bias_BASE_All_Graph.R#L83), function `PlotpCOpBIBA`

```r
PlotpCOpBIBA<-function(n,alp,a1,a2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a1)) stop("'a1' is missing")
  if (missing(a2)) stop("'a2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a1) != "integer") & (class(a1) != "numeric") || length(a1)>1 || a1<0  ) stop("'a1' has to be greater than or equal to 0")
  if ((class(a2) != "integer") & (class(a2) != "numeric") || length(a2)>1 || a2<0  ) stop("'a2' has to be greater than or equal to 0")
  x=Value=Heading=mark=NULL

  ndf=pCOpBIBA(n,alp,a1,a2)
  W1 = data.frame(x=ndf$x1, Value=ndf$pconfQ, Heading="pconfQ")
  W2 = data.frame(x=ndf$x1, Value=ndf$pbiasQ, Heading="pbiasQ")
  W3 = data.frame(x=ndf$x1, Value=ndf$pconfH, Heading="pconfH")
  W4 = data.frame(x=ndf$x1, Value=ndf$pbiasH, Heading="pbiasH")
  nBA=rbind(W1,W2,W3,W4)

  ggplot2::ggplot(nBA, ggplot2::aes(x=x, y=Value))+
    ggplot2::labs(title = "p-Confidence & p-Bias - Bayesian methods") +
    ggplot2::facet_grid(Heading ~ .,scales="free_y") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=W1,ggplot2::aes(color="pConf Quantile"))+
    ggplot2::geom_point(data=W1, ggplot2::aes(color="pconfQ Values"),shape=22)+
    ggplot2::geom_line(data=W2,ggplot2::aes(color="pbias Quantile"))+
    ggplot2::geom_point(data=W2,ggplot2::aes(color="pbiasQ Values"),shape=23)+
    ggplot2::geom_line(data=W3,ggplot2::aes(color="pConf HPD"))+
    ggplot2::geom_point(data=W3, ggplot2::aes(color="pconfHPD Values"),shape=21)+
    ggplot2::geom_line(data=W4,ggplot2::aes(color="pbias HPD"))+
    ggplot2::geom_point(data=W4,ggplot2::aes(color="pbiasHPD Values"),shape=16)+
    ggplot2::scale_colour_manual(name='Heading',
                                 values=c('pConf Quantile'='red',
                                          'pconfQ Values'='red',
                                          'pbias Quantile'='blue',
                                          'pbiasQ Values'='blue',
                                          'pConf HPD'='orange',
                                          'pconfHPD Values'='orange',
                                          'pbias HPD'='black',
                                          'pbiasHPD Values'='black'),
                                 guide='Title') +
    ggplot2::guides(colour = ggplot2::guide_legend(override.aes = list(linetype=c(1,1,1,1,1,1,1,1),
                                                                       shape=c(NA, NA,16,23,NA,NA,21,22))))


}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbiba`

```python
def plotpcopbiba(n, alp, a1, a2):
    """p-confidence & p-bias plot for the Bayesian interval, quantile+HPD (R PlotpCOpBIBA)."""
    from .bayes import pcopbiba
    ba = pcopbiba(n, alp, a1, a2)
    # reshape the wide Q/H output into the (x1, pconf, pbias, method) form
    q = ba[['x1', 'pconfQ', 'pbiasQ']].rename(
        columns={'pconfQ': 'pconf', 'pbiasQ': 'pbias'})
    q['method'] = "Quantile"
    h = ba[['x1', 'pconfH', 'pbiasH']].rename(
        columns={'pconfH': 'pconf', 'pbiasH': 'pbias'})
    h['method'] = "HPD"
    return _pconf_plot(pd.concat([q, h], ignore_index=True),
                       "p-Confidence & p-Bias - Bayesian method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; uses SciPy HPD (`_hpd.hpd_beta`); lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbicall`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbicall
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for all continuity-corrected interval methods — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbicall(20, 0.05, 0.02)
```

**R source** — [`R/422.p-Confidence_p-Bias_CC_All_Graph.R` (line 15)](https://github.com/RajeswaranV/proportion/blob/master/R/422.p-Confidence_p-Bias_CC_All_Graph.R#L15), function `PlotpCOpBICAll`

```r
PlotpCOpBICAll<-function(n,alp,c)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if (c<=0 || c>(1/(2*n)) || length(c)>1) stop("'c' has to be positive and less than or equal to 1/(2*n)")
  x=Value=Heading=mark=val=NULL

  nAll = pCOpBICAll(n,alp,c)
  pc=data.frame(x=nAll$x1, val=nAll$pconf, Heading=nAll$method, mark="pconf",minmax=min(nAll$pbias, nAll$pconf))
  pb=data.frame(x=nAll$x1, val=nAll$pbias, Heading=nAll$method, mark="pbias",minmax=max(nAll$pbias, nAll$pconf))
  nndf=rbind(pc,pb)
  cdfWDc = subset(nndf, Heading == "CC-Wald" & mark== "pconf")
  cdfWDb = subset(nndf, Heading == "CC-Wald" & mark== "pbias")
  cdfSCc = subset(nndf, Heading == "CC-Score" & mark== "pconf")
  cdfSCb = subset(nndf, Heading == "CC-Score" & mark== "pbias")
  cdfASc = subset(nndf, Heading == "CC-ArcSine" & mark== "pconf")
  cdfASb = subset(nndf, Heading == "CC-ArcSine" & mark== "pbias")
  cdfLTc = subset(nndf, Heading == "CC-Logit-Wald" & mark== "pconf")
  cdfLTb = subset(nndf, Heading == "CC-Logit-Wald" & mark== "pbias")
  cdfTWc = subset(nndf, Heading == "CC-Wald-T" & mark== "pconf")
  cdfTWb = subset(nndf, Heading == "CC-Wald-T" & mark== "pbias")

  ggplot2::ggplot(nndf, ggplot2::aes(x=x, y=val))+
    ggplot2::labs(title = "p-Confidence & p-Bias - Continuity corrected methods") +
    ggplot2::facet_wrap(Heading ~ mark,scales="free_y",ncol=2) +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=cdfWDc,ggplot2::aes(color="pConf CC-Wald"))+
    ggplot2::geom_point(data=cdfWDc, ggplot2::aes(color="pConf CC-Wald Values"),shape=22)+
    ggplot2::geom_line(data=cdfWDb,ggplot2::aes(color="pbias CC-Wald"))+
    ggplot2::geom_point(data=cdfWDb,ggplot2::aes(color="pbias CC-Wald Values"),shape=23)+
    ggplot2::geom_line(data=cdfSCc,ggplot2::aes(color="pConf CC-Score"))+
    ggplot2::geom_point(data=cdfSCc, ggplot2::aes(color="pConf CC-Score Values"),shape=21)+
    ggplot2::geom_line(data=cdfSCb,ggplot2::aes(color="pbias CC-Score"))+
    ggplot2::geom_point(data=cdfSCb,ggplot2::aes(color="pbias CC-Score Values"),shape=16)+
    ggplot2::geom_line(data=cdfASc,ggplot2::aes(color="pConf CC-ArcSine"))+
    ggplot2::geom_point(data=cdfASc, ggplot2::aes(color="pConf CC-ArcSine Values"),shape=22)+
    ggplot2::geom_line(data=cdfASb,ggplot2::aes(color="pbias CC-ArcSine"))+
    ggplot2::geom_point(data=cdfASb,ggplot2::aes(color="pbias CC-ArcSine Values"),shape=23)+
    ggplot2::geom_line(data=cdfTWc,ggplot2::aes(color="pConf CC-Wald-T"))+
    ggplot2::geom_point(data=cdfTWc, ggplot2::aes(color="pConf CC-Wald-T Values"),shape=21)+
    ggplot2::geom_line(data=cdfTWb,ggplot2::aes(color="pbias CC-Wald-T"))+
    ggplot2::geom_point(data=cdfTWb,ggplot2::aes(color="pbias CC-Wald-T Values"),shape=16)+
    ggplot2::geom_line(data=cdfLTc,ggplot2::aes(color="pConf CC-Logit-Wald"))+
    ggplot2::geom_point(data=cdfLTc, ggplot2::aes(color="pConf CC-Logit-Wald Values"),shape=21)+
    ggplot2::geom_line(data=cdfLTb,ggplot2::aes(color="pbias CC-Logit-Wald"))+
    ggplot2::geom_point(data=cdfLTb,ggplot2::aes(color="pbias CC-Logit-Wald Values"),shape=16)+
    ggplot2::scale_colour_manual(name='Heading',
                                 values=c(
                                   'pConf CC-Wald'='red',
                                   'pConf CC-Wald Values'='red',
                                   'pbias CC-Wald'='black',
                                   'pbias CC-Wald Values'='black',
                                   'pConf CC-Score'='red',
                                   'pConf CC-Score Values'='red',
                                   'pbias CC-Score'='black',
                                   'pbias CC-Score Values'='black',
                                   'pConf CC-ArcSine'='red',
                                   'pConf CC-ArcSine Values'='red',
                                   'pbias CC-ArcSine'='black',
                                   'pbias CC-ArcSine Values'='black',
                                   'pConf CC-Logit-Wald'='red',
                                   'pConf CC-Logit-Wald Values'='red',
                                   'pbias CC-Logit-Wald'='black',
                                   'pbias CC-Logit-Wald Values'='black',
                                   'pConf CC-Wald-T'='red',
                                   'pConf CC-Wald-T Values'='red',
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbicall`

```python
def plotpcopbicall(n, alp, c):
    """p-confidence & p-bias plot for all five CC methods (R PlotpCOpBICAll)."""
    return _pconf_plot(cc_all.pcopbicall(n, alp, c),
                       "p-Confidence & p-Bias - all continuity-corrected methods")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbicas`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbicas
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for the continuity-corrected ArcSine (variance-stabilised) interval — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbicas(20, 0.05, 0.02)
```

**R source** — [`R/422.p-Confidence_p-Bias_CC_All_Graph.R` (line 137)](https://github.com/RajeswaranV/proportion/blob/master/R/422.p-Confidence_p-Bias_CC_All_Graph.R#L137), function `PlotpCOpBICAS`

```r
PlotpCOpBICAS<-function(n,alp,c)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  x=Value=Heading=mark=NULL

  CBEX = pCOpBICAS(n,alp,c)

  W1 = data.frame(x=CBEX$x1, Value=CBEX$pconf, Heading="pconf")
  W2 = data.frame(x=CBEX$x1, Value=CBEX$pbias, Heading="pbias")
  gdf=rbind(W1,W2)

  ggplot2::ggplot(gdf, ggplot2::aes(x=x, y=Value)) +
    ggplot2::facet_grid(Heading~.,scales="free_y") +
    ggplot2::labs(title = "p-Confidence & p-Bias - continuity corrected ArcSine method") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=gdf,ggplot2::aes(x=x, y=Value))

}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbicas`

```python
    def _plot(n, alp, c):
        return _pconf_plot(
            fn(n, alp, c),
            f"p-Confidence & p-Bias - continuity-corrected {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbiclt`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbiclt
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for the continuity-corrected Logit-Wald interval — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbiclt(20, 0.05, 0.02)
```

**R source** — [`R/422.p-Confidence_p-Bias_CC_All_Graph.R` (line 209)](https://github.com/RajeswaranV/proportion/blob/master/R/422.p-Confidence_p-Bias_CC_All_Graph.R#L209), function `PlotpCOpBICLT`

```r
PlotpCOpBICLT<-function(n,alp,c)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  x=Value=Heading=mark=NULL

  CBEX = pCOpBICLT(n,alp,c)

  W1 = data.frame(x=CBEX$x1, Value=CBEX$pconf, Heading="pconf")
  W2 = data.frame(x=CBEX$x1, Value=CBEX$pbias, Heading="pbias")
  gdf=rbind(W1,W2)

  ggplot2::ggplot(gdf, ggplot2::aes(x=x, y=Value)) +
    ggplot2::facet_grid(Heading~.,scales="free_y") +
    ggplot2::labs(title = "p-Confidence & p-Bias - continuity corrected Logit Wald method") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=gdf,ggplot2::aes(x=x, y=Value))

}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbiclt`

```python
    def _plot(n, alp, c):
        return _pconf_plot(
            fn(n, alp, c),
            f"p-Confidence & p-Bias - continuity-corrected {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbicsc`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbicsc
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for the continuity-corrected Score / Wilson interval — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbicsc(20, 0.05, 0.02)
```

**R source** — [`R/422.p-Confidence_p-Bias_CC_All_Graph.R` (line 245)](https://github.com/RajeswaranV/proportion/blob/master/R/422.p-Confidence_p-Bias_CC_All_Graph.R#L245), function `PlotpCOpBICSC`

```r
PlotpCOpBICSC<-function(n,alp,c)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if (c<=0 || c>(1/(2*n)) || length(c)>1) stop("'c' has to be positive and less than or equal to 1/(2*n)")
  x=Value=Heading=mark=NULL

  CBEX = pCOpBICSC(n,alp,c)

  W1 = data.frame(x=CBEX$x1, Value=CBEX$pconf, Heading="pconf")
  W2 = data.frame(x=CBEX$x1, Value=CBEX$pbias, Heading="pbias")
  gdf=rbind(W1,W2)

  ggplot2::ggplot(gdf, ggplot2::aes(x=x, y=Value)) +
    ggplot2::facet_grid(Heading~.,scales="free_y") +
    ggplot2::labs(title = "p-Confidence & p-Bias - continuity corrected Score method") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=gdf,ggplot2::aes(x=x, y=Value))

}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbicsc`

```python
    def _plot(n, alp, c):
        return _pconf_plot(
            fn(n, alp, c),
            f"p-Confidence & p-Bias - continuity-corrected {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbictw`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbictw
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for the continuity-corrected Wald-T interval — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbictw(20, 0.05, 0.02)
```

**R source** — [`R/422.p-Confidence_p-Bias_CC_All_Graph.R` (line 173)](https://github.com/RajeswaranV/proportion/blob/master/R/422.p-Confidence_p-Bias_CC_All_Graph.R#L173), function `PlotpCOpBICTW`

```r
PlotpCOpBICTW<-function(n,alp,c)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  x=Value=Heading=mark=NULL

  CBEX = pCOpBICTW(n,alp,c)

  W1 = data.frame(x=CBEX$x1, Value=CBEX$pconf, Heading="pconf")
  W2 = data.frame(x=CBEX$x1, Value=CBEX$pbias, Heading="pbias")
  gdf=rbind(W1,W2)

  ggplot2::ggplot(gdf, ggplot2::aes(x=x, y=Value)) +
    ggplot2::facet_grid(Heading~.,scales="free_y") +
    ggplot2::labs(title = "p-Confidence & p-Bias - continuity corrected Wald-T method") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=gdf,ggplot2::aes(x=x, y=Value))

}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbictw`

```python
    def _plot(n, alp, c):
        return _pconf_plot(
            fn(n, alp, c),
            f"p-Confidence & p-Bias - continuity-corrected {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbicwd`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbicwd
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for the continuity-corrected Wald (normal-approximation) interval — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbicwd(20, 0.05, 0.02)
```

**R source** — [`R/422.p-Confidence_p-Bias_CC_All_Graph.R` (line 101)](https://github.com/RajeswaranV/proportion/blob/master/R/422.p-Confidence_p-Bias_CC_All_Graph.R#L101), function `PlotpCOpBICWD`

```r
PlotpCOpBICWD<-function(n,alp,c)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  x=Value=Heading=mark=NULL

  CBEX = pCOpBICWD(n,alp,c)

  W1 = data.frame(x=CBEX$x1, Value=CBEX$pconf, Heading="pconf")
  W2 = data.frame(x=CBEX$x1, Value=CBEX$pbias, Heading="pbias")
  gdf=rbind(W1,W2)

  ggplot2::ggplot(gdf, ggplot2::aes(x=x, y=Value)) +
    ggplot2::facet_grid(Heading~.,scales="free_y") +
    ggplot2::labs(title = "p-Confidence & p-Bias - continuity corrected Wald method") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=gdf,ggplot2::aes(x=x, y=Value))

}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbicwd`

```python
    def _plot(n, alp, c):
        return _pconf_plot(
            fn(n, alp, c),
            f"p-Confidence & p-Bias - continuity-corrected {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbiex`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbiex
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for the Exact (Clopper-Pearson / mid-p) interval — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbiex(20, 0.05, 0.5)
```

**R source** — [`R/402.p-Confidence_p-Bias_BASE_All_Graph.R` (line 30)](https://github.com/RajeswaranV/proportion/blob/master/R/402.p-Confidence_p-Bias_BASE_All_Graph.R#L30), function `PlotpCOpBIEX`

```r
PlotpCOpBIEX<-function(n,alp,e)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(e)) stop("'e' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(e) != "integer") & (class(e) != "numeric") || any(e>1) || any(e<0)) stop("'e' has to be between 0 and 1")
  if (length(e)>10 ) stop("Plot of only 10 intervals of 'e' is possible")
  x=Value=Heading=mark=NULL

  CBEX = pCOpBIEX(n,alp,e)

  W1 = data.frame(x=CBEX$x1, Value=CBEX$pconf, Heading="pconf")
  W2 = data.frame(x=CBEX$x1, Value=CBEX$pbias, Heading="pbias")
  b1=data.frame(e=CBEX$e)
  b2=data.frame(e=CBEX$e)
  bjoin=rbind(b1,b2)
  fg=rbind(W1,W2)
  gdf=cbind(fg,bjoin)
  gdf$e=as.factor(gdf$e)

  ggplot2::ggplot(gdf, ggplot2::aes(x=x, y=Value, colour = e)) +
    ggplot2::facet_grid(Heading~.,scales="free_y") +
    ggplot2::labs(title = "p-Confidence & p-Bias - Exact method") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
      ggplot2::scale_colour_manual(values=c("blue", "red", "black", "cyan4", "deeppink",
                                            "orange","chartreuse4",
                                            "blueviolet" , "grey", "darksalmon", "tan1")) +
      ggplot2::geom_line(data=gdf,ggplot2::aes(color=e))

}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbiex`

```python
def plotpcopbiex(n, alp, e):
    """p-confidence & p-bias plot for the Exact method (R PlotpCOpBIEX)."""
    return _pconf_plot(base_all.pcopbiex(n, alp, e),
                       "p-Confidence & p-Bias - Exact method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbigen`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbigen
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for user-supplied interval limits — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
wd = bk.ciwd(20, 0.05)
bk.plotpcopbigen(20, wd["LWD"].values, wd["UWD"].values)
```

**R source** — [`R/423.p-Confidence_p-Bias_GENERAL.R` (line 82)](https://github.com/RajeswaranV/proportion/blob/master/R/423.p-Confidence_p-Bias_GENERAL.R#L82), function `PlotpCOpBIGEN`

```r
PlotpCOpBIGEN<-function(n,LL,UL)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(LL)) stop("'Lower limit' is missing")
  if (missing(UL)) stop("'Upper Limit' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if ((class(LL) != "integer") & (class(LL) != "numeric") || any(LL < 0)) stop("'LL' has to be a set of positive numeric vectors")
  if ((class(UL) != "integer") & (class(UL) != "numeric") || any(UL < 0)) stop("'UL' has to be a set of positive numeric vectors")
  if (length(LL) < n ) stop("Length of vector LL has to be greater than n")
  if (length(UL) < n ) stop("Length of vector UL has to be greater than n")
  if (any(LL[0:n+1] > UL[0:n+1] )) stop("LL value have to be lower than the corrosponding UL value")
  x=Value=Heading=mark=NULL

  gdf=pCOpBIGEN(n,LL,UL)
  W1 = data.frame(x=gdf$x1, Value=gdf$pconf, Heading="pconf")
  W2 = data.frame(x=gdf$x1, Value=gdf$pbias, Heading="pbias")
  ndf=rbind(W1,W2)

  ggplot2::ggplot(ndf, ggplot2::aes(x=x, y=Value))+
    ggplot2::labs(title = "p-Confidence & p-Bias - General method") +
    ggplot2::facet_grid(Heading ~ .,scales="free_y") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=W1,ggplot2::aes(color="pConfidence "))+
    ggplot2::geom_point(data=W1, ggplot2::aes(color="pconf Values"))+
    ggplot2::geom_line(data=W2,ggplot2::aes(color="pbias"))+
    ggplot2::geom_point(data=W2,ggplot2::aes(color="pbias Values"))+
    ggplot2::scale_colour_manual(name='Heading',
                                 values=c('pConfidence '='red',
                                          'pconf Values'='red',
                                          'pbias'='blue',
                                          'pbias Values'='blue'),
                                 guide='Title') +
    ggplot2::guides(colour = ggplot2::guide_legend(override.aes = list(linetype=c(1,1,1,1),
                                                                       shape=c(NA, 16,16,NA))))

}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbigen`

```python
def plotpcopbigen(n, LL, UL):
    """p-confidence & p-bias plot for user-supplied limits (R PlotpCOpBIGEN)."""
    return _pconf_plot(pcopbigen(n, LL, UL),
                       "p-Confidence & p-Bias (given limits)")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbilr`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbilr
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for the Likelihood-Ratio interval — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbilr(20, 0.05)
```

**R source** — [`R/402.p-Confidence_p-Bias_BASE_All_Graph.R` (line 431)](https://github.com/RajeswaranV/proportion/blob/master/R/402.p-Confidence_p-Bias_BASE_All_Graph.R#L431), function `PlotpCOpBILR`

```r
PlotpCOpBILR<-function(n,alp)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  x=Value=Heading=mark=NULL

  CBEX = pCOpBILR(n,alp)

  W1 = data.frame(x=CBEX$x1, Value=CBEX$pconf, Heading="pconf")
  W2 = data.frame(x=CBEX$x1, Value=CBEX$pbias, Heading="pbias")
  gdf=rbind(W1,W2)

  ggplot2::ggplot(gdf, ggplot2::aes(x=x, y=Value)) +
    ggplot2::facet_grid(Heading~.,scales="free_y") +
    ggplot2::labs(title = "p-Confidence & p-Bias - Likelihood Ratio method") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=gdf,ggplot2::aes(x=x, y=Value))

}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbilr`

```python
    def _plot(n, alp):
        return _pconf_plot(fn(n, alp), f"p-Confidence & p-Bias - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbilt`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbilt
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for the Logit-Wald interval — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbilt(20, 0.05)
```

**R source** — [`R/402.p-Confidence_p-Bias_BASE_All_Graph.R` (line 357)](https://github.com/RajeswaranV/proportion/blob/master/R/402.p-Confidence_p-Bias_BASE_All_Graph.R#L357), function `PlotpCOpBILT`

```r
PlotpCOpBILT<-function(n,alp)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  x=Value=Heading=mark=NULL

  CBEX = pCOpBILT(n,alp)

  W1 = data.frame(x=CBEX$x1, Value=CBEX$pconf, Heading="pconf")
  W2 = data.frame(x=CBEX$x1, Value=CBEX$pbias, Heading="pbias")
  gdf=rbind(W1,W2)

  ggplot2::ggplot(gdf, ggplot2::aes(x=x, y=Value)) +
    ggplot2::facet_grid(Heading~.,scales="free_y") +
    ggplot2::labs(title = "p-Confidence & p-Bias - Logit Wald method") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=gdf,ggplot2::aes(x=x, y=Value))

}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbilt`

```python
    def _plot(n, alp):
        return _pconf_plot(fn(n, alp), f"p-Confidence & p-Bias - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbisc`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbisc
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for the Score / Wilson interval — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbisc(20, 0.05)
```

**R source** — [`R/402.p-Confidence_p-Bias_BASE_All_Graph.R` (line 283)](https://github.com/RajeswaranV/proportion/blob/master/R/402.p-Confidence_p-Bias_BASE_All_Graph.R#L283), function `PlotpCOpBISC`

```r
PlotpCOpBISC<-function(n,alp)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  x=Value=Heading=mark=NULL

  CBEX = pCOpBISC(n,alp)

  W1 = data.frame(x=CBEX$x1, Value=CBEX$pconf, Heading="pconf")
  W2 = data.frame(x=CBEX$x1, Value=CBEX$pbias, Heading="pbias")
  gdf=rbind(W1,W2)

  ggplot2::ggplot(gdf, ggplot2::aes(x=x, y=Value)) +
    ggplot2::facet_grid(Heading~.,scales="free_y") +
    ggplot2::labs(title = "p-Confidence & p-Bias - Score method") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=gdf,ggplot2::aes(x=x, y=Value))

}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbisc`

```python
    def _plot(n, alp):
        return _pconf_plot(fn(n, alp), f"p-Confidence & p-Bias - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbitw`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbitw
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for the Wald-T interval — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbitw(20, 0.05)
```

**R source** — [`R/402.p-Confidence_p-Bias_BASE_All_Graph.R` (line 394)](https://github.com/RajeswaranV/proportion/blob/master/R/402.p-Confidence_p-Bias_BASE_All_Graph.R#L394), function `PlotpCOpBITW`

```r
PlotpCOpBITW<-function(n,alp)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  x=Value=Heading=mark=NULL

  CBEX = pCOpBITW(n,alp)

  W1 = data.frame(x=CBEX$x1, Value=CBEX$pconf, Heading="pconf")
  W2 = data.frame(x=CBEX$x1, Value=CBEX$pbias, Heading="pbias")
  gdf=rbind(W1,W2)

  ggplot2::ggplot(gdf, ggplot2::aes(x=x, y=Value)) +
    ggplot2::facet_grid(Heading~.,scales="free_y") +
    ggplot2::labs(title = "p-Confidence & p-Bias - Wald-T method") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=gdf,ggplot2::aes(x=x, y=Value))

}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbitw`

```python
    def _plot(n, alp):
        return _pconf_plot(fn(n, alp), f"p-Confidence & p-Bias - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotpcopbiwd`

```{eval-rst}
.. autofunction:: binomcikit.pconf.plots.plotpcopbiwd
```

**In plain words** — Plots p-confidence and p-bias against the number of successes for the Wald (normal-approximation) interval — a visualisation of the corresponding `p-confidence and p-bias` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotpcopbiwd(20, 0.05)
```

**R source** — [`R/402.p-Confidence_p-Bias_BASE_All_Graph.R` (line 246)](https://github.com/RajeswaranV/proportion/blob/master/R/402.p-Confidence_p-Bias_BASE_All_Graph.R#L246), function `PlotpCOpBIWD`

```r
PlotpCOpBIWD<-function(n,alp)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  x=Value=Heading=mark=NULL

  CBEX = pCOpBIWD(n,alp)

  W1 = data.frame(x=CBEX$x1, Value=CBEX$pconf, Heading="pconf")
  W2 = data.frame(x=CBEX$x1, Value=CBEX$pbias, Heading="pbias")
  gdf=rbind(W1,W2)

  ggplot2::ggplot(gdf, ggplot2::aes(x=x, y=Value)) +
    ggplot2::facet_grid(Heading~.,scales="free_y") +
    ggplot2::labs(title = "p-Confidence & p-Bias - Wald method") +
    ggplot2::labs(y = "Confidence ") +
    ggplot2::labs(x = "No of successes") +
    ggplot2::geom_line(data=gdf,ggplot2::aes(x=x, y=Value))

}
```

**What the R code does** — The R function calls the numeric function and draws p-confidence and p-bias against the number of successes with ggplot2.

**Python source** — `binomcikit.pconf.plots.plotpcopbiwd`

```python
    def _plot(n, alp):
        return _pconf_plot(fn(n, alp), f"p-Confidence & p-Bias - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

