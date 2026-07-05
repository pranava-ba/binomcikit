<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `err.plots`

```{eval-rst}
.. module:: binomcikit.err.plots
```

This module computes **error and failure** — for a null proportion `phi` and threshold `f`, the increase in nominal error, the long-term power, and a pass/fail verdict for each interval, for **plots** of the results (returning plotnine `ggplot` objects). See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `ploterraall`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterraall
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for all adjusted interval methods — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterraall(20, 0.05, 2, 0.5, -2)
```

**R source** — [`R/512.Error-Failure_LimitBased_ADJ_All_Graph.R` (line 293)](https://github.com/RajeswaranV/proportion/blob/master/R/512.Error-Failure_LimitBased_ADJ_All_Graph.R#L293), function `PloterrAAll`

```r
PloterrAAll<-function(n,alp,h,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h) >1|| h<0 || !(h%%1 ==0)) stop("'h' has to be an integer greater than or equal to 0")
  if (phi>1 || phi<0) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")) stop("'f' has to be numeric value")
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errAAll(n,alp,h,phi,f)
  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for adjusted methods") +
    ggplot2::labs(x = "Method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity")

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterraall`

```python
def ploterraall(n, alp, h, phi, f):
    """Error/failure plot for all six adjusted methods (R PloterrAAll)."""
    return _err_plot(
        adj_all.erraall(n, alp, h, phi, f),
        "Error, long term power and pass/fail - all adjusted methods")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterraas`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterraas
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for the adjusted ArcSine (variance-stabilised) interval — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterraas(20, 0.05, 2, 0.5, -2)
```

**R source** — [`R/512.Error-Failure_LimitBased_ADJ_All_Graph.R` (line 108)](https://github.com/RajeswaranV/proportion/blob/master/R/512.Error-Failure_LimitBased_ADJ_All_Graph.R#L108), function `PloterrAAS`

```r
PloterrAAS<-function(n,alp,h,phi,f)
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
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errAAS(n,alp,h,phi,f)
  errdf$method = as.factor("Adjusted ArcSine")

  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for adjusted ArcSine method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity",width=0.5)

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterraas`

```python
    def _plot(n, alp, h, phi, f):
        return _err_plot(
            fn(n, alp, h, phi, f),
            f"Error, long term power and pass/fail - adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterrall`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterrall
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for all interval methods — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterrall(20, 0.05, 0.5, -2)
```

**R source** — [`R/502.Error-Failure_LimitBased_BASE_All_Graph.R` (line 15)](https://github.com/RajeswaranV/proportion/blob/master/R/502.Error-Failure_LimitBased_BASE_All_Graph.R#L15), function `PloterrAll`

```r
PloterrAll<-function(n,alp,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0 || length(phi)>1) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")|| length(f)>1) stop("'f' has to be numeric value")
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errAll(n,alp,phi,f)
  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for base methods") +
    ggplot2::labs(x = "Method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity")

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterrall`

```python
def ploterrall(n, alp, phi, f):
    """Error/failure plot for all six base methods (R PloterrAll)."""
    return _err_plot(base_all.errall(n, alp, phi, f),
                     "Error, long term power and pass/fail - all base methods")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterralr`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterralr
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for the adjusted Likelihood-Ratio interval — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterralr(20, 0.05, 2, 0.5, -2)
```

**R source** — [`R/512.Error-Failure_LimitBased_ADJ_All_Graph.R` (line 246)](https://github.com/RajeswaranV/proportion/blob/master/R/512.Error-Failure_LimitBased_ADJ_All_Graph.R#L246), function `PloterrALR`

```r
PloterrALR<-function(n,alp,h,phi,f)
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
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errALR(n,alp,h,phi,f)
  errdf$method = as.factor("Adjusted Likelihood Ratio")

  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for adjusted Likelihood Ratio method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity",width=0.5)

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterralr`

```python
    def _plot(n, alp, h, phi, f):
        return _err_plot(
            fn(n, alp, h, phi, f),
            f"Error, long term power and pass/fail - adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterralt`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterralt
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for the adjusted Logit-Wald interval — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterralt(20, 0.05, 2, 0.5, -2)
```

**R source** — [`R/512.Error-Failure_LimitBased_ADJ_All_Graph.R` (line 154)](https://github.com/RajeswaranV/proportion/blob/master/R/512.Error-Failure_LimitBased_ADJ_All_Graph.R#L154), function `PloterrALT`

```r
PloterrALT<-function(n,alp,h,phi,f)
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
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errALT(n,alp,h,phi,f)
  errdf$method = as.factor("Adjusted Logit Wald")

  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for adjusted Logit Wald method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity",width=0.5)

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterralt`

```python
    def _plot(n, alp, h, phi, f):
        return _err_plot(
            fn(n, alp, h, phi, f),
            f"Error, long term power and pass/fail - adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterras`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterras
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for the ArcSine (variance-stabilised) interval — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterras(20, 0.05, 0.5, -2)
```

**R source** — [`R/502.Error-Failure_LimitBased_BASE_All_Graph.R` (line 143)](https://github.com/RajeswaranV/proportion/blob/master/R/502.Error-Failure_LimitBased_BASE_All_Graph.R#L143), function `PloterrAS`

```r
PloterrAS<-function(n,alp,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0 || length(phi)>1) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")|| length(f)>1) stop("'f' has to be numeric value")
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errAS(n,alp,phi,f)
  errdf$method = as.factor("ArcSine")

  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for ArcSine method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity",width=0.5)

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterras`

```python
    def _plot(n, alp, phi, f):
        return _err_plot(fn(n, alp, phi, f),
                         f"Error, long term power and pass/fail - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterrasc`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterrasc
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for the adjusted Score / Wilson interval — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterrasc(20, 0.05, 2, 0.5, -2)
```

**R source** — [`R/512.Error-Failure_LimitBased_ADJ_All_Graph.R` (line 62)](https://github.com/RajeswaranV/proportion/blob/master/R/512.Error-Failure_LimitBased_ADJ_All_Graph.R#L62), function `PloterrASC`

```r
PloterrASC<-function(n,alp,h,phi,f)
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
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errASC(n,alp,h,phi,f)
  errdf$method = as.factor("Adjusted Score")

  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for adjusted Score method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity",width=0.5)

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterrasc`

```python
    def _plot(n, alp, h, phi, f):
        return _err_plot(
            fn(n, alp, h, phi, f),
            f"Error, long term power and pass/fail - adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterratw`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterratw
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for the adjusted Wald-T interval — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterratw(20, 0.05, 2, 0.5, -2)
```

**R source** — [`R/512.Error-Failure_LimitBased_ADJ_All_Graph.R` (line 200)](https://github.com/RajeswaranV/proportion/blob/master/R/512.Error-Failure_LimitBased_ADJ_All_Graph.R#L200), function `PloterrATW`

```r
PloterrATW<-function(n,alp,h,phi,f)
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
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errATW(n,alp,h,phi,f)
  errdf$method = as.factor("Adjusted Wald-T")

  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for adjusted Wald-T method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity",width=0.5)

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterratw`

```python
    def _plot(n, alp, h, phi, f):
        return _err_plot(
            fn(n, alp, h, phi, f),
            f"Error, long term power and pass/fail - adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterrawd`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterrawd
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for the adjusted Wald (normal-approximation) interval — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterrawd(20, 0.05, 2, 0.5, -2)
```

**R source** — [`R/512.Error-Failure_LimitBased_ADJ_All_Graph.R` (line 16)](https://github.com/RajeswaranV/proportion/blob/master/R/512.Error-Failure_LimitBased_ADJ_All_Graph.R#L16), function `PloterrAWD`

```r
PloterrAWD<-function(n,alp,h,phi,f)
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
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errAWD(n,alp,h,phi,f)
  errdf$method = as.factor("Adjusted Wald")

  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for adjusted Wald method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity",width=0.5)

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterrawd`

```python
    def _plot(n, alp, h, phi, f):
        return _err_plot(
            fn(n, alp, h, phi, f),
            f"Error, long term power and pass/fail - adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterrba`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterrba
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for the Bayesian credible interval — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterrba(20, 0.05, 0.5, -2, 1, 1)
```

**R source** — [`R/502.Error-Failure_LimitBased_BASE_All_Graph.R` (line 320)](https://github.com/RajeswaranV/proportion/blob/master/R/502.Error-Failure_LimitBased_BASE_All_Graph.R#L320), function `PloterrBA`

```r
PloterrBA<-function(n,alp,phi,f,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0 || length(phi)>1) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")|| length(f)>1) stop("'f' has to be numeric value")
  if ((class(a) != "integer") & (class(a) != "numeric") || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || b<0  ) stop("'b' has to be greater than or equal to 0")
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errBA(n,alp,phi,f,a,b)

  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for Bayesian method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity",width=0.5)

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterrba`

```python
def ploterrba(n, alp, phi, f, a, b):
    """Error/failure plot for the Bayesian interval, quantile+HPD (R PloterrBA)."""
    from .bayes import errba
    return _err_plot(errba(n, alp, phi, f, a, b),
                     "Error, long term power and pass/fail - Bayesian method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; uses SciPy HPD (`_hpd.hpd_beta`); lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterrcall`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterrcall
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for all continuity-corrected interval methods — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterrcall(20, 0.05, 0.5, 0.02, -2)
```

**R source** — [`R/522.Error-Failure_Limitbased_CC_All_Graph.R` (line 17)](https://github.com/RajeswaranV/proportion/blob/master/R/522.Error-Failure_Limitbased_CC_All_Graph.R#L17), function `PloterrCAll`

```r
PloterrCAll<-function(n,alp,phi,c,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if (c<=0 || c>(1/(2*n))) stop("'c' has to be positive and less than or equal to 1/(2*n)")
  if ((class(f) != "integer") & (class(f) != "numeric")) stop("'f' has to be numeric value")
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errCAll(n,alp,phi,c,f)
  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for continuity corrected methods") +
    ggplot2::labs(x = "Method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity")

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterrcall`

```python
def ploterrcall(n, alp, phi, c, f):
    """Error/failure plot for all five CC methods (R PloterrCAll)."""
    return _err_plot(
        cc_all.errcall(n, alp, phi, c, f),
        "Error, long term power and pass/fail - all CC methods")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterrcas`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterrcas
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for the continuity-corrected ArcSine (variance-stabilised) interval — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterrcas(20, 0.05, 0.5, 0.02, -2)
```

**R source** — [`R/522.Error-Failure_Limitbased_CC_All_Graph.R` (line 110)](https://github.com/RajeswaranV/proportion/blob/master/R/522.Error-Failure_Limitbased_CC_All_Graph.R#L110), function `PloterrCAS`

```r
PloterrCAS<-function(n,alp,phi,c,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if (c<=0 || c>(1/(2*n))) stop("'c' has to be positive and less than or equal to 1/(2*n)")
  if ((class(f) != "integer") & (class(f) != "numeric")) stop("'f' has to be numeric value")
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errCAS(n,alp,phi,c,f)
  errdf$method = as.factor("Continuity corrected ArcSine")

  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for continuity corrected ArcSine") +
    ggplot2::labs(x = "Method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity",width=0.5)

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterrcas`

```python
    def _plot(n, alp, phi, c, f):
        return _err_plot(
            fn(n, alp, phi, c, f),
            f"Error, long term power and pass/fail - CC {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterrclt`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterrclt
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for the continuity-corrected Logit-Wald interval — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterrclt(20, 0.05, 0.5, 0.02, -2)
```

**R source** — [`R/522.Error-Failure_Limitbased_CC_All_Graph.R` (line 157)](https://github.com/RajeswaranV/proportion/blob/master/R/522.Error-Failure_Limitbased_CC_All_Graph.R#L157), function `PloterrCLT`

```r
PloterrCLT<-function(n,alp,phi,c,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if (c<=0 || c>(1/(2*n))) stop("'c' has to be positive and less than or equal to 1/(2*n)")
  if ((class(f) != "integer") & (class(f) != "numeric")) stop("'f' has to be numeric value")
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errCLT(n,alp,phi,c,f)
  errdf$method = as.factor("Continuity corrected Logit Wald")

  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for continuity corrected Logit Wald") +
    ggplot2::labs(x = "Method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity",width=0.5)

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterrclt`

```python
    def _plot(n, alp, phi, c, f):
        return _err_plot(
            fn(n, alp, phi, c, f),
            f"Error, long term power and pass/fail - CC {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterrcsc`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterrcsc
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for the continuity-corrected Score / Wilson interval — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterrcsc(20, 0.05, 0.5, 0.02, -2)
```

**R source** — [`R/522.Error-Failure_Limitbased_CC_All_Graph.R` (line 251)](https://github.com/RajeswaranV/proportion/blob/master/R/522.Error-Failure_Limitbased_CC_All_Graph.R#L251), function `PloterrCSC`

```r
PloterrCSC<-function(n,alp,phi,c,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if (c<=0 || c>(1/(2*n))) stop("'c' has to be positive and less than or equal to 1/(2*n)")
  if ((class(f) != "integer") & (class(f) != "numeric")) stop("'f' has to be numeric value")
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errCSC(n,alp,phi,c,f)
  errdf$method = as.factor("Continuity corrected Score")

  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for continuity corrected Score") +
    ggplot2::labs(x = "Method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity",width=0.5)

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterrcsc`

```python
    def _plot(n, alp, phi, c, f):
        return _err_plot(
            fn(n, alp, phi, c, f),
            f"Error, long term power and pass/fail - CC {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterrctw`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterrctw
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for the continuity-corrected Wald-T interval — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterrctw(20, 0.05, 0.5, 0.02, -2)
```

**R source** — [`R/522.Error-Failure_Limitbased_CC_All_Graph.R` (line 204)](https://github.com/RajeswaranV/proportion/blob/master/R/522.Error-Failure_Limitbased_CC_All_Graph.R#L204), function `PloterrCTW`

```r
PloterrCTW<-function(n,alp,phi,c,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if (c<=0 || c>(1/(2*n))) stop("'c' has to be positive and less than or equal to 1/(2*n)")
  if ((class(f) != "integer") & (class(f) != "numeric")) stop("'f' has to be numeric value")
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errCTW(n,alp,phi,c,f)
  errdf$method = as.factor("Continuity corrected Wald-t")

  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for continuity corrected Wald-t") +
    ggplot2::labs(x = "Method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity",width=0.5)

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterrctw`

```python
    def _plot(n, alp, phi, c, f):
        return _err_plot(
            fn(n, alp, phi, c, f),
            f"Error, long term power and pass/fail - CC {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterrcwd`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterrcwd
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for the continuity-corrected Wald (normal-approximation) interval — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterrcwd(20, 0.05, 0.5, 0.02, -2)
```

**R source** — [`R/522.Error-Failure_Limitbased_CC_All_Graph.R` (line 62)](https://github.com/RajeswaranV/proportion/blob/master/R/522.Error-Failure_Limitbased_CC_All_Graph.R#L62), function `PloterrCWD`

```r
PloterrCWD<-function(n,alp,phi,c,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if (c<=0 || c>(1/(2*n))) stop("'c' has to be positive and less than or equal to 1/(2*n)")
  if ((class(f) != "integer") & (class(f) != "numeric")) stop("'f' has to be numeric value")
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errCWD(n,alp,phi,c,f)
  errdf$method = as.factor("Continuity corrected Wald")

  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for continuity corrected Wald") +
    ggplot2::labs(x = "Method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity",width=0.5)

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterrcwd`

```python
    def _plot(n, alp, phi, c, f):
        return _err_plot(
            fn(n, alp, phi, c, f),
            f"Error, long term power and pass/fail - CC {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterrex`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterrex
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for the Exact (Clopper-Pearson / mid-p) interval — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterrex(20, 0.05, 0.5, -2, 0.5)
```

**R source** — [`R/502.Error-Failure_LimitBased_BASE_All_Graph.R` (line 373)](https://github.com/RajeswaranV/proportion/blob/master/R/502.Error-Failure_LimitBased_BASE_All_Graph.R#L373), function `PloterrEX`

```r
PloterrEX<-function(n,alp,phi,f,e)
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
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errEX(n,alp,phi,f,e)
  errdf$e = as.factor(errdf$e)

  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,e=alpdf$e)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, e=thetadf$e)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = e, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for Exact method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity",width=0.5)

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterrex`

```python
def ploterrex(n, alp, phi, f, e):
    """Error/failure plot for the Exact method (R PloterrEX)."""
    return _err_plot(base_all.errex(n, alp, phi, f, e),
                     "Error, long term power and pass/fail - Exact method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterrgen`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterrgen
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for user-supplied interval limits — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
wd = bk.ciwd(20, 0.05)
bk.ploterrgen(20, wd["LWD"].values, wd["UWD"].values, 0.05, 0.5, -2)
```

**Python source** — `binomcikit.err.plots.ploterrgen`

```python
def ploterrgen(n, LL, UL, alp, phi, f):
    """Error/failure plot for user-supplied limits (R PloterrGEN)."""
    return _err_plot(errgen(n, LL, UL, alp, phi, f),
                     "Error, long term power and pass/fail (given limits)")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterrlr`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterrlr
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for the Likelihood-Ratio interval — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterrlr(20, 0.05, 0.5, -2)
```

**R source** — [`R/502.Error-Failure_LimitBased_BASE_All_Graph.R` (line 273)](https://github.com/RajeswaranV/proportion/blob/master/R/502.Error-Failure_LimitBased_BASE_All_Graph.R#L273), function `PloterrLR`

```r
PloterrLR<-function(n,alp,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0 || length(phi)>1) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")|| length(f)>1) stop("'f' has to be numeric value")
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errLR(n,alp,phi,f)
  errdf$method = as.factor("Likelihood Ratio")

  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for Likelihood Ratio method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity",width=0.5)

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterrlr`

```python
    def _plot(n, alp, phi, f):
        return _err_plot(fn(n, alp, phi, f),
                         f"Error, long term power and pass/fail - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterrlt`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterrlt
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for the Logit-Wald interval — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterrlt(20, 0.05, 0.5, -2)
```

**R source** — [`R/502.Error-Failure_LimitBased_BASE_All_Graph.R` (line 229)](https://github.com/RajeswaranV/proportion/blob/master/R/502.Error-Failure_LimitBased_BASE_All_Graph.R#L229), function `PloterrLT`

```r
PloterrLT<-function(n,alp,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0 || length(phi)>1) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")|| length(f)>1) stop("'f' has to be numeric value")
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errLT(n,alp,phi,f)
  errdf$method = as.factor("Logit Wald")

  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for Logit Wald method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity",width=0.5)

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterrlt`

```python
    def _plot(n, alp, phi, f):
        return _err_plot(fn(n, alp, phi, f),
                         f"Error, long term power and pass/fail - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterrsc`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterrsc
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for the Score / Wilson interval — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterrsc(20, 0.05, 0.5, -2)
```

**R source** — [`R/502.Error-Failure_LimitBased_BASE_All_Graph.R` (line 100)](https://github.com/RajeswaranV/proportion/blob/master/R/502.Error-Failure_LimitBased_BASE_All_Graph.R#L100), function `PloterrSC`

```r
PloterrSC<-function(n,alp,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0 || length(phi)>1) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")|| length(f)>1) stop("'f' has to be numeric value")
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errSC(n,alp,phi,f)
  errdf$method = as.factor("Score")

  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for Score method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity",width=0.5)

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterrsc`

```python
    def _plot(n, alp, phi, f):
        return _err_plot(fn(n, alp, phi, f),
                         f"Error, long term power and pass/fail - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterrtw`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterrtw
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for the Wald-T interval — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterrtw(20, 0.05, 0.5, -2)
```

**R source** — [`R/502.Error-Failure_LimitBased_BASE_All_Graph.R` (line 186)](https://github.com/RajeswaranV/proportion/blob/master/R/502.Error-Failure_LimitBased_BASE_All_Graph.R#L186), function `PloterrTW`

```r
PloterrTW<-function(n,alp,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0 || length(phi)>1) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")|| length(f)>1) stop("'f' has to be numeric value")
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errTW(n,alp,phi,f)
  errdf$method = as.factor("Wald-T")

  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for Wald-T method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity",width=0.5)

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterrtw`

```python
    def _plot(n, alp, phi, f):
        return _err_plot(fn(n, alp, phi, f),
                         f"Error, long term power and pass/fail - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ploterrwd`

```{eval-rst}
.. autofunction:: binomcikit.err.plots.ploterrwd
```

**In plain words** — Plots the error / long-term-power bars, coloured by pass/fail for the Wald (normal-approximation) interval — a visualisation of the corresponding `error and failure` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.ploterrwd(20, 0.05, 0.5, -2)
```

**R source** — [`R/502.Error-Failure_LimitBased_BASE_All_Graph.R` (line 57)](https://github.com/RajeswaranV/proportion/blob/master/R/502.Error-Failure_LimitBased_BASE_All_Graph.R#L57), function `PloterrWD`

```r
PloterrWD<-function(n,alp,phi,f)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(phi)) stop("'phi' is missing")
  if (missing(f)) stop("'f' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (phi>1 || phi<0 || length(phi)>1) stop("Null hypothesis 'phi' has to be between 0 and 1")
  if ((class(f) != "integer") & (class(f) != "numeric")|| length(f)>1) stop("'f' has to be numeric value")
  method=value=Fail_Pass=NULL

  #### Calling functions and creating df
  errdf=  errWD(n,alp,phi,f)
  errdf$method = as.factor("Wald")

  alpdf=  errdf[,c(1,3,4)]
  thetadf=errdf[,c(2,3,4)]
  vdfa=data.frame(value=alpdf$delalp ,mark="Increase in nominal error" ,Fail_Pass=alpdf$Fail_Pass ,method=alpdf$method)
  vdft=data.frame(value=thetadf$theta ,mark="Long term power of test",Fail_Pass=thetadf$Fail_Pass, method=thetadf$method)
  full.df=rbind(vdfa,vdft)

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = value, fill = Fail_Pass)) +
    ggplot2::labs(title = "Error, long term power and pass/fail for Wald method") +
    ggplot2::facet_grid(mark ~ .,scales="free_y") +
    ggplot2::geom_bar(stat="identity",position = "identity",width=0.5)

}
```

**What the R code does** — The R function calls the numeric function and draws the error / long-term-power bars, coloured by pass/fail with ggplot2.

**Python source** — `binomcikit.err.plots.ploterrwd`

```python
    def _plot(n, alp, phi, f):
        return _err_plot(fn(n, alp, phi, f),
                         f"Error, long term power and pass/fail - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

