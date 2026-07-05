<!-- GENERATED-STUB: safe to regenerate; delete this line once hand-written -->

# `expl.plots`

```{eval-rst}
.. module:: binomcikit.expl.plots
```

This module computes **expected interval length** — the average width of each interval over hypothetical *p* drawn from a `Beta(a, b)` prior, for **plots** of the results (returning plotnine `ggplot` objects). See the {doc}`mapping table </r_to_python_mapping>` for the full family overview.

```{contents} Functions in this module
:local:
:depth: 1
```

## `plotexplaall`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplaall
```

**In plain words** — Plots the expected-length curve against *p* for all adjusted interval methods — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexplaall(20, 0.05, ..., seed=0)
```

**R source** — [`R/312.Expec_Leng_ADJ_All_Graph.R` (line 17)](https://github.com/RajeswaranV/proportion/blob/master/R/312.Expec_Leng_ADJ_All_Graph.R#L17), function `PlotexplAAll`

```r
PlotexplAAll<-function(n,alp,h,a,b)
{

  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h) >1|| h<0  || !(h%%1 ==0)) stop("'h' has to be an integer greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  df.new=  explAAll(n,alp,h,a,b)

  ggplot2::ggplot(df.new, ggplot2::aes(x=hp, y=ew))+
    ggplot2::labs(title = "Expected length of 6 adjusted methods") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::geom_vline(ggplot2::aes(xintercept=0.5),linetype = 1)

}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplaall`

```python
    def _plot(n, alp, *rest, seed=None):
        if need_param:
            param, a, b = rest
        else:
            a, b = rest
        hp = _beta_hp(a, b, seed)
        curves = []
        for name, (fn, lo, hi) in reg.items():
            args = (n, alp, param) if need_param else (n, alp)
            curves.append(_expl_curve(n, _lengths_from(fn, lo, hi, *args), hp, name))
        curve = pd.concat(curves, ignore_index=True)
        return _expl_plot(curve, f"Expected length - all {kind} methods")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplaas`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplaas
```

**In plain words** — Plots the expected-length curve against *p* for the adjusted ArcSine (variance-stabilised) interval — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexplaas(20, 0.05, 2, 1, 1, seed=0)
```

**R source** — [`R/312.Expec_Leng_ADJ_All_Graph.R` (line 286)](https://github.com/RajeswaranV/proportion/blob/master/R/312.Expec_Leng_ADJ_All_Graph.R#L286), function `PlotexplAAS`

```r
PlotexplAAS<-function(n,alp,h,a,b)
{

  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  df.aas=  gexplAAS(n,alp,h,a,b)
  ddf.aas = lengthAAS(n,alp,h,a,b)
  df.aas$gMean=ddf.aas$explMean
  df.aas$gMax=ddf.aas$explMax
  df.aas$gUL=ddf.aas$explMean+ddf.aas$explSD
  df.aas$gLL=ddf.aas$explMean-ddf.aas$explSD

  ggplot2::ggplot(data=df.aas, mapping=ggplot2::aes(x=hp, y=ew)) +
    ggplot2::labs(title = "Expected length of adjusted Logit Wald method") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(mapping=ggplot2::aes(colour=method), show_guide = TRUE) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMean, fill="Mean"),color="orange"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMax, fill="Max"),color="blue"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gLL, fill="Lower Limit"),color="cyan4"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gUL, fill="Upper Limit"),color="brown"  ) +
    ggplot2::scale_color_hue("Method") +
    ggplot2::scale_fill_manual(
      "Metric lines", values=c(1,1,1,1),
      guide=ggplot2::guide_legend(override.aes = list(colour=c("orange", "blue", "cyan4","brown"))),
      labels=c("Mean", "Max", "Lower Limit(Mean- 1SD)", "Upper Limit(Mean + 1SD)"))

}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplaas`

```python
    def _plot(n, alp, h, a, b, seed=None):
        fn, lo, hi = _ADJ[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp, h),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve, f"Expected length - adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplall`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplall
```

**In plain words** — Plots the expected-length curve against *p* for all interval methods — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexplall(20, 0.05, ..., seed=0)
```

**R source** — [`R/302.Expec_Leng_BASE_All_Graph.R` (line 236)](https://github.com/RajeswaranV/proportion/blob/master/R/302.Expec_Leng_BASE_All_Graph.R#L236), function `PlotexplAll`

```r
PlotexplAll<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=NULL

  #### Calling functions and creating df
  df.eall=  explAll(n,alp,a,b)

  ggplot2::ggplot(df.eall, ggplot2::aes(x=hp, y=ew))+
    ggplot2::labs(title = "Expected length of 6 base methods") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::geom_vline(ggplot2::aes(xintercept=0.5),linetype = 1)

}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplall`

```python
    def _plot(n, alp, *rest, seed=None):
        if need_param:
            param, a, b = rest
        else:
            a, b = rest
        hp = _beta_hp(a, b, seed)
        curves = []
        for name, (fn, lo, hi) in reg.items():
            args = (n, alp, param) if need_param else (n, alp)
            curves.append(_expl_curve(n, _lengths_from(fn, lo, hi, *args), hp, name))
        curve = pd.concat(curves, ignore_index=True)
        return _expl_plot(curve, f"Expected length - all {kind} methods")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplalr`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplalr
```

**In plain words** — Plots the expected-length curve against *p* for the adjusted Likelihood-Ratio interval — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexplalr(20, 0.05, 2, 1, 1, seed=0)
```

**R source** — [`R/312.Expec_Leng_ADJ_All_Graph.R` (line 342)](https://github.com/RajeswaranV/proportion/blob/master/R/312.Expec_Leng_ADJ_All_Graph.R#L342), function `PlotexplALR`

```r
PlotexplALR<-function(n,alp,h,a,b)
{

  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h) >1|| h<0  || !(h%%1 ==0)) stop("'h' has to be an integer greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  df.alr=  gexplALR(n,alp,h,a,b)
  ddf.alr = lengthALR(n,alp,h,a,b)
  df.alr$gMean=ddf.alr$explMean
  df.alr$gMax=ddf.alr$explMax
  df.alr$gUL=ddf.alr$explMean+ddf.alr$explSD
  df.alr$gLL=ddf.alr$explMean-ddf.alr$explSD

  ggplot2::ggplot(data=df.alr, mapping=ggplot2::aes(x=hp, y=ew)) +
    ggplot2::labs(title = "Expected length of adjusted Likelihood Ratio method") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(mapping=ggplot2::aes(colour=method), show_guide = TRUE) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMean, fill="Mean"),color="orange"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMax, fill="Max"),color="blue"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gLL, fill="Lower Limit"),color="cyan4"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gUL, fill="Upper Limit"),color="brown"  ) +
    ggplot2::scale_color_hue("Method") +
    ggplot2::scale_fill_manual(
      "Metric lines", values=c(1,1,1,1),
      guide=ggplot2::guide_legend(override.aes = list(colour=c("orange", "blue", "cyan4","brown"))),
      labels=c("Mean", "Max", "Lower Limit(Mean- 1SD)", "Upper Limit(Mean + 1SD)"))

}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplalr`

```python
    def _plot(n, alp, h, a, b, seed=None):
        fn, lo, hi = _ADJ[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp, h),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve, f"Expected length - adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplalt`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplalt
```

**In plain words** — Plots the expected-length curve against *p* for the adjusted Logit-Wald interval — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexplalt(20, 0.05, 2, 1, 1, seed=0)
```

**R source** — [`R/312.Expec_Leng_ADJ_All_Graph.R` (line 230)](https://github.com/RajeswaranV/proportion/blob/master/R/312.Expec_Leng_ADJ_All_Graph.R#L230), function `PlotexplALT`

```r
PlotexplALT<-function(n,alp,h,a,b)
{

  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  df.alt=  gexplALT(n,alp,h,a,b)
  ddf.alt = lengthALT(n,alp,h,a,b)
  df.alt$gMean=ddf.alt$explMean
  df.alt$gMax=ddf.alt$explMax
  df.alt$gUL=ddf.alt$explMean+ddf.alt$explSD
  df.alt$gLL=ddf.alt$explMean-ddf.alt$explSD

  ggplot2::ggplot(data=df.alt, mapping=ggplot2::aes(x=hp, y=ew)) +
    ggplot2::labs(title = "Expected length of adjusted Logit Wald method") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(mapping=ggplot2::aes(colour=method), show_guide = TRUE) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMean, fill="Mean"),color="orange"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMax, fill="Max"),color="blue"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gLL, fill="Lower Limit"),color="cyan4"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gUL, fill="Upper Limit"),color="brown"  ) +
    ggplot2::scale_color_hue("Method") +
    ggplot2::scale_fill_manual(
      "Metric lines", values=c(1,1,1,1),
      guide=ggplot2::guide_legend(override.aes = list(colour=c("orange", "blue", "cyan4","brown"))),
      labels=c("Mean", "Max", "Lower Limit(Mean- 1SD)", "Upper Limit(Mean + 1SD)"))

}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplalt`

```python
    def _plot(n, alp, h, a, b, seed=None):
        fn, lo, hi = _ADJ[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp, h),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve, f"Expected length - adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplas`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplas
```

**In plain words** — Plots the expected-length curve against *p* for the ArcSine (variance-stabilised) interval — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexplas(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/302.Expec_Leng_BASE_All_Graph.R` (line 381)](https://github.com/RajeswaranV/proportion/blob/master/R/302.Expec_Leng_BASE_All_Graph.R#L381), function `PlotexplAS`

```r
PlotexplAS<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=NULL

  df.as=  gexplAS(n,alp,a,b)

  ddf.as = lengthAS(n,alp,a,b)
  df.as$gMean=ddf.as$explMean
  df.as$gMax=ddf.as$explMax
  df.as$gUL=ddf.as$explMean+ddf.as$explSD
  df.as$gLL=ddf.as$explMean-ddf.as$explSD

  ggplot2::ggplot(data=df.as, mapping=ggplot2::aes(x=hp, y=ew)) +
    ggplot2::labs(title = "Expected length of ArcSine method") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(mapping=ggplot2::aes(colour=method), show_guide = TRUE) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMean, fill="Mean"),color="orange"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMax, fill="Max"),color="blue"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gLL, fill="Lower Limit"),color="cyan4"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gUL, fill="Upper Limit"),color="brown"  ) +
    ggplot2::scale_color_hue("Method") +
    ggplot2::scale_fill_manual(
      "Metric lines", values=c(1,1,1,1),
      guide=ggplot2::guide_legend(override.aes = list(colour=c("orange", "blue", "cyan4","brown"))),
      labels=c("Mean", "Max", "Lower Limit(Mean- 1SD)", "Upper Limit(Mean + 1SD)"))

}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplas`

```python
    def base_variant(n, alp, a, b, seed=None):
        fn, lo, hi = reg[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve, f"Expected length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplasc`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplasc
```

**In plain words** — Plots the expected-length curve against *p* for the adjusted Score / Wilson interval — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexplasc(20, 0.05, 2, 1, 1, seed=0)
```

**R source** — [`R/312.Expec_Leng_ADJ_All_Graph.R` (line 117)](https://github.com/RajeswaranV/proportion/blob/master/R/312.Expec_Leng_ADJ_All_Graph.R#L117), function `PlotexplASC`

```r
PlotexplASC<-function(n,alp,h,a,b)
{

  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  df.asc=  gexplASC(n,alp,h,a,b)
  ddf.asc = lengthASC(n,alp,h,a,b)
  df.asc$gMean=ddf.asc$explMean
  df.asc$gMax=ddf.asc$explMax
  df.asc$gUL=ddf.asc$explMean+ddf.asc$explSD
  df.asc$gLL=ddf.asc$explMean-ddf.asc$explSD

  ggplot2::ggplot(data=df.asc, mapping=ggplot2::aes(x=hp, y=ew)) +
    ggplot2::labs(title = "Expected length of adjusted Score method") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(mapping=ggplot2::aes(colour=method), show_guide = TRUE) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMean, fill="Mean"),color="orange"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMax, fill="Max"),color="blue"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gLL, fill="Lower Limit"),color="cyan4"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gUL, fill="Upper Limit"),color="brown"  ) +
    ggplot2::scale_color_hue("Method") +
    ggplot2::scale_fill_manual(
      "Metric lines", values=c(1,1,1,1),
      guide=ggplot2::guide_legend(override.aes = list(colour=c("orange", "blue", "cyan4","brown"))),
      labels=c("Mean", "Max", "Lower Limit(Mean- 1SD)", "Upper Limit(Mean + 1SD)"))

}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplasc`

```python
    def _plot(n, alp, h, a, b, seed=None):
        fn, lo, hi = _ADJ[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp, h),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve, f"Expected length - adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplatw`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplatw
```

**In plain words** — Plots the expected-length curve against *p* for the adjusted Wald-T interval — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexplatw(20, 0.05, 2, 1, 1, seed=0)
```

**R source** — [`R/312.Expec_Leng_ADJ_All_Graph.R` (line 173)](https://github.com/RajeswaranV/proportion/blob/master/R/312.Expec_Leng_ADJ_All_Graph.R#L173), function `PlotexplATW`

```r
PlotexplATW<-function(n,alp,h,a,b)
{

  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  df.atw=  gexplATW(n,alp,h,a,b)
  ddf.atw = lengthATW(n,alp,h,a,b)
  df.atw$gMean=ddf.atw$explMean
  df.atw$gMax=ddf.atw$explMax
  df.atw$gUL=ddf.atw$explMean+ddf.atw$explSD
  df.atw$gLL=ddf.atw$explMean-ddf.atw$explSD

  ggplot2::ggplot(data=df.atw, mapping=ggplot2::aes(x=hp, y=ew)) +
    ggplot2::labs(title = "Expected length of adjusted Wald-T method") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(mapping=ggplot2::aes(colour=method), show_guide = TRUE) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMean, fill="Mean"),color="orange"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMax, fill="Max"),color="blue"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gLL, fill="Lower Limit"),color="cyan4"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gUL, fill="Upper Limit"),color="brown"  ) +
    ggplot2::scale_color_hue("Method") +
    ggplot2::scale_fill_manual(
      "Metric lines", values=c(1,1,1,1),
      guide=ggplot2::guide_legend(override.aes = list(colour=c("orange", "blue", "cyan4","brown"))),
      labels=c("Mean", "Max", "Lower Limit(Mean- 1SD)", "Upper Limit(Mean + 1SD)"))


}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplatw`

```python
    def _plot(n, alp, h, a, b, seed=None):
        fn, lo, hi = _ADJ[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp, h),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve, f"Expected length - adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplawd`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplawd
```

**In plain words** — Plots the expected-length curve against *p* for the adjusted Wald (normal-approximation) interval — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexplawd(20, 0.05, 2, 1, 1, seed=0)
```

**R source** — [`R/312.Expec_Leng_ADJ_All_Graph.R` (line 60)](https://github.com/RajeswaranV/proportion/blob/master/R/312.Expec_Leng_ADJ_All_Graph.R#L60), function `PlotexplAWD`

```r
PlotexplAWD<-function(n,alp,h,a,b)
{

  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  df.awd=  gexplAWD(n,alp,h,a,b)
  ddf.awd = lengthAWD(n,alp,h,a,b)
  df.awd$gMean=ddf.awd$explMean
  df.awd$gMax=ddf.awd$explMax
  df.awd$gUL=ddf.awd$explMean+ddf.awd$explSD
  df.awd$gLL=ddf.awd$explMean-ddf.awd$explSD

  ggplot2::ggplot(data=df.awd, mapping=ggplot2::aes(x=hp, y=ew)) +
    ggplot2::labs(title = "Expected length of adjusted Wald method") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(mapping=ggplot2::aes(colour=method), show_guide = TRUE) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMean, fill="Mean"),color="orange"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMax, fill="Max"),color="blue"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gLL, fill="Lower Limit"),color="cyan4"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gUL, fill="Upper Limit"),color="brown"  ) +
    ggplot2::scale_color_hue("Method") +
    ggplot2::scale_fill_manual(
      "Metric lines", values=c(1,1,1,1),
      guide=ggplot2::guide_legend(override.aes = list(colour=c("orange", "blue", "cyan4","brown"))),
      labels=c("Mean", "Max", "Lower Limit(Mean- 1SD)", "Upper Limit(Mean + 1SD)"))


}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplawd`

```python
    def _plot(n, alp, h, a, b, seed=None):
        fn, lo, hi = _ADJ[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp, h),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve, f"Expected length - adjusted {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplba`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplba
```

**In plain words** — Plots the expected-length curve against *p* for the Bayesian credible interval — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexplba(20, 0.05, 1, 1, 1, 1, seed=0)
```

**R source** — [`R/302.Expec_Leng_BASE_All_Graph.R` (line 142)](https://github.com/RajeswaranV/proportion/blob/master/R/302.Expec_Leng_BASE_All_Graph.R#L142), function `PlotexplBA`

```r
PlotexplBA<-function(n,alp,a,b,a1,a2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(a1)) stop("'a1' is missing")
  if (missing(a2)) stop("'a2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if ((class(a1) != "integer") & (class(a1) != "numeric") || length(a1)>1 || a1<0 ) stop("'a1' has to be greater than or equal to 0")
  if ((class(a2) != "integer") & (class(a2) != "numeric") || length(a2)>1 || a2<0 ) stop("'a2' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=NULL

####INPUT n
x=0:n
k=n+1
####INITIALIZATIONS
LBAQ=0
UBAQ=0
LBAH=0
UBAH=0
s=5000
LEBAQ=0 								#LENGTH OF INTERVAL
LEBAH=0
ewiBAQ=matrix(0,k,s)						#Expected length quantity in sum
ewBAQ=0
ewiBAH=matrix(0,k,s)						#Expected length quantity in sum
ewBAH=0									#Expected Length

#library(TeachingDemos)				#To get HPDs
for(i in 1:k)
{
#Quantile Based Intervals
LBAQ[i]=stats::qbeta(alp/2,x[i]+a1,n-x[i]+a2)
UBAQ[i]=stats::qbeta(1-(alp/2),x[i]+a1,n-x[i]+a2)

LBAH[i]=TeachingDemos::hpd(stats::qbeta,shape1=x[i]+a1,shape2=n-x[i]+a2,conf=1-alp)[1]
UBAH[i]=TeachingDemos::hpd(stats::qbeta,shape1=x[i]+a1,shape2=n-x[i]+a2,conf=1-alp)[2]

LEBAQ[i]=UBAQ[i]-LBAQ[i]
LEBAH[i]=UBAH[i]-LBAH[i]
}
#sumLEBAQ=sum(LEBAQ)
#sumLEBAH=sum(LEBAH)
####Expected Length
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
ewiBAQ[i,j]=LEBAQ[i]*stats::dbinom(i-1, n,hp[j])
ewiBAH[i,j]=LEBAH[i]*stats::dbinom(i-1, n,hp[j])

}
ewBAQ[j]=sum(ewiBAQ[,j])
ewBAH[j]=sum(ewiBAH[,j])						#Expected Length
}
ELBAQ=data.frame(hp,ew=ewBAQ,method="Quantile")
ELBAH=data.frame(hp,ew=ewBAH,method="HPD")

df.ba=rbind(ELBAQ,ELBAH)

ggplot2::ggplot(df.ba, ggplot2::aes(x=hp, y=ew))+
  ggplot2::labs(title = "Expected length of Bayesian Quantile & HPD based methods") +
  ggplot2::labs(y = "Expected Length") +
  ggplot2::labs(x = "p") +
  ggplot2::geom_line(ggplot2::aes(color=method)) +
  # ... (truncated - see the linked source)
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplba`

```python
def plotexplba(n, alp, a, b, a1, a2, seed=None):
    """Expected-length curves for the Bayesian interval, quantile+HPD (R PlotexplBA)."""
    ba = ciba(n, alp, a1, a2)
    hp = _beta_hp(a, b, seed)
    curve = pd.concat([
        _expl_curve(n, ba['UBAQ'].to_numpy() - ba['LBAQ'].to_numpy(), hp, "Quantile"),
        _expl_curve(n, ba['UBAH'].to_numpy() - ba['LBAH'].to_numpy(), hp, "HPD"),
    ], ignore_index=True)
    return _expl_plot(curve, "Expected length - Bayesian method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; uses SciPy HPD (`_hpd.hpd_beta`); lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplcall`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplcall
```

**In plain words** — Plots the expected-length curve against *p* for all continuity-corrected interval methods — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexplcall(20, 0.05, ..., seed=0)
```

**R source** — [`R/322.Expec_Leng_CC_All_Graph.R` (line 17)](https://github.com/RajeswaranV/proportion/blob/master/R/322.Expec_Leng_CC_All_Graph.R#L17), function `PlotexplCAll`

```r
PlotexplCAll<-function(n,alp,c,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  df.new    = explCAll(n,alp,c,a,b)

  ggplot2::ggplot(df.new, ggplot2::aes(x=hp, y=ew))+
    ggplot2::labs(title = "Expected length of continuity corrected methods") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(ggplot2::aes(color=method)) +
    ggplot2::geom_vline(ggplot2::aes(xintercept=0.5),linetype = 1)

}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplcall`

```python
    def _plot(n, alp, *rest, seed=None):
        if need_param:
            param, a, b = rest
        else:
            a, b = rest
        hp = _beta_hp(a, b, seed)
        curves = []
        for name, (fn, lo, hi) in reg.items():
            args = (n, alp, param) if need_param else (n, alp)
            curves.append(_expl_curve(n, _lengths_from(fn, lo, hi, *args), hp, name))
        curve = pd.concat(curves, ignore_index=True)
        return _expl_plot(curve, f"Expected length - all {kind} methods")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplcas`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplcas
```

**In plain words** — Plots the expected-length curve against *p* for the continuity-corrected ArcSine (variance-stabilised) interval — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexplcas(20, 0.05, 0.02, 1, 1, seed=0)
```

**R source** — [`R/322.Expec_Leng_CC_All_Graph.R` (line 170)](https://github.com/RajeswaranV/proportion/blob/master/R/322.Expec_Leng_CC_All_Graph.R#L170), function `PlotexplCAS`

```r
PlotexplCAS<-function(n,alp,c,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  df.cas    = gexplCAS(n,alp,c,a,b)
  ddf.cas = lengthCAS(n,alp,c,a,b)
  df.cas$gMean=ddf.cas$explMean
  df.cas$gMax=ddf.cas$explMax
  df.cas$gUL=ddf.cas$explMean+ddf.cas$explSD
  df.cas$gLL=ddf.cas$explMean-ddf.cas$explSD

  ggplot2::ggplot(data=df.cas, mapping=ggplot2::aes(x=hp, y=ew)) +
    ggplot2::labs(title = "Expected length of continuity corrected ArcSine") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(mapping=ggplot2::aes(colour=method), show_guide = TRUE) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMean, fill="Mean"),color="orange"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMax, fill="Max"),color="blue"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gLL, fill="Lower Limit"),color="cyan4"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gUL, fill="Upper Limit"),color="brown"  ) +
    ggplot2::scale_color_hue("Method") +
    ggplot2::scale_fill_manual(
      "Metric lines", values=c(1,1,1,1),
      guide=ggplot2::guide_legend(override.aes = list(colour=c("orange", "blue", "cyan4","brown"))),
      labels=c("Mean", "Max", "Lower Limit(Mean- 1SD)", "Upper Limit(Mean + 1SD)"))

}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplcas`

```python
    def _plot(n, alp, c, a, b, seed=None):
        fn, lo, hi = _CC[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp, c),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve,
                          f"Expected length - continuity-corrected {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplclt`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplclt
```

**In plain words** — Plots the expected-length curve against *p* for the continuity-corrected Logit-Wald interval — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexplclt(20, 0.05, 0.02, 1, 1, seed=0)
```

**R source** — [`R/322.Expec_Leng_CC_All_Graph.R` (line 225)](https://github.com/RajeswaranV/proportion/blob/master/R/322.Expec_Leng_CC_All_Graph.R#L225), function `PlotexplCLT`

```r
PlotexplCLT<-function(n,alp,c,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  df.clt    = gexplCLT(n,alp,c,a,b)
  ddf.clt = lengthCLT(n,alp,c,a,b)
  df.clt$gMean=ddf.clt$explMean
  df.clt$gMax=ddf.clt$explMax
  df.clt$gUL=ddf.clt$explMean+ddf.clt$explSD
  df.clt$gLL=ddf.clt$explMean-ddf.clt$explSD

  ggplot2::ggplot(data=df.clt, mapping=ggplot2::aes(x=hp, y=ew)) +
    ggplot2::labs(title = "Expected length of continuity corrected Logit Wald") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(mapping=ggplot2::aes(colour=method), show_guide = TRUE) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMean, fill="Mean"),color="orange"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMax, fill="Max"),color="blue"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gLL, fill="Lower Limit"),color="cyan4"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gUL, fill="Upper Limit"),color="brown"  ) +
    ggplot2::scale_color_hue("Method") +
    ggplot2::scale_fill_manual(
      "Metric lines", values=c(1,1,1,1),
      guide=ggplot2::guide_legend(override.aes = list(colour=c("orange", "blue", "cyan4","brown"))),
      labels=c("Mean", "Max", "Lower Limit(Mean- 1SD)", "Upper Limit(Mean + 1SD)"))


}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplclt`

```python
    def _plot(n, alp, c, a, b, seed=None):
        fn, lo, hi = _CC[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp, c),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve,
                          f"Expected length - continuity-corrected {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplcsc`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplcsc
```

**In plain words** — Plots the expected-length curve against *p* for the continuity-corrected Score / Wilson interval — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexplcsc(20, 0.05, 0.02, 1, 1, seed=0)
```

**R source** — [`R/322.Expec_Leng_CC_All_Graph.R` (line 115)](https://github.com/RajeswaranV/proportion/blob/master/R/322.Expec_Leng_CC_All_Graph.R#L115), function `PlotexplCSC`

```r
PlotexplCSC<-function(n,alp,c,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if (c<=0 || c>(1/(2*n)) || length(c)>1) stop("'c' has to be positive and less than or equal to 1/(2*n)")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  df.csc    = gexplCSC(n,alp,c,a,b)
  ddf.csc = lengthCSC(n,alp,c,a,b)
  df.csc$gMean=ddf.csc$explMean
  df.csc$gMax=ddf.csc$explMax
  df.csc$gUL=ddf.csc$explMean+ddf.csc$explSD
  df.csc$gLL=ddf.csc$explMean-ddf.csc$explSD

  ggplot2::ggplot(data=df.csc, mapping=ggplot2::aes(x=hp, y=ew)) +
    ggplot2::labs(title = "Expected length of continuity corrected Score") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(mapping=ggplot2::aes(colour=method), show_guide = TRUE) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMean, fill="Mean"),color="orange"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMax, fill="Max"),color="blue"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gLL, fill="Lower Limit"),color="cyan4"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gUL, fill="Upper Limit"),color="brown"  ) +
    ggplot2::scale_color_hue("Method") +
    ggplot2::scale_fill_manual(
      "Metric lines", values=c(1,1,1,1),
      guide=ggplot2::guide_legend(override.aes = list(colour=c("orange", "blue", "cyan4","brown"))),
      labels=c("Mean", "Max", "Lower Limit(Mean- 1SD)", "Upper Limit(Mean + 1SD)"))

}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplcsc`

```python
    def _plot(n, alp, c, a, b, seed=None):
        fn, lo, hi = _CC[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp, c),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve,
                          f"Expected length - continuity-corrected {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplctw`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplctw
```

**In plain words** — Plots the expected-length curve against *p* for the continuity-corrected Wald-T interval — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexplctw(20, 0.05, 0.02, 1, 1, seed=0)
```

**R source** — [`R/322.Expec_Leng_CC_All_Graph.R` (line 281)](https://github.com/RajeswaranV/proportion/blob/master/R/322.Expec_Leng_CC_All_Graph.R#L281), function `PlotexplCTW`

```r
PlotexplCTW<-function(n,alp,c,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  df.ctw    = gexplCTW(n,alp,c,a,b)
  ddf.ctw = lengthCTW(n,alp,c,a,b)
  df.ctw$gMean=ddf.ctw$explMean
  df.ctw$gMax=ddf.ctw$explMax
  df.ctw$gUL=ddf.ctw$explMean+ddf.ctw$explSD
  df.ctw$gLL=ddf.ctw$explMean-ddf.ctw$explSD

  ggplot2::ggplot(data=df.ctw, mapping=ggplot2::aes(x=hp, y=ew)) +
    ggplot2::labs(title = "Expected length of continuity corrected Wald-T") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(mapping=ggplot2::aes(colour=method), show_guide = TRUE) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMean, fill="Mean"),color="orange"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMax, fill="Max"),color="blue"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gLL, fill="Lower Limit"),color="cyan4"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gUL, fill="Upper Limit"),color="brown"  ) +
    ggplot2::scale_color_hue("Method") +
    ggplot2::scale_fill_manual(
      "Metric lines", values=c(1,1,1,1),
      guide=ggplot2::guide_legend(override.aes = list(colour=c("orange", "blue", "cyan4","brown"))),
      labels=c("Mean", "Max", "Lower Limit(Mean- 1SD)", "Upper Limit(Mean + 1SD)"))

}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplctw`

```python
    def _plot(n, alp, c, a, b, seed=None):
        fn, lo, hi = _CC[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp, c),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve,
                          f"Expected length - continuity-corrected {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplcwd`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplcwd
```

**In plain words** — Plots the expected-length curve against *p* for the continuity-corrected Wald (normal-approximation) interval — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexplcwd(20, 0.05, 0.02, 1, 1, seed=0)
```

**R source** — [`R/322.Expec_Leng_CC_All_Graph.R` (line 59)](https://github.com/RajeswaranV/proportion/blob/master/R/322.Expec_Leng_CC_All_Graph.R#L59), function `PlotexplCWD`

```r
PlotexplCWD<-function(n,alp,c,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  df.cwd    = gexplCWD(n,alp,c,a,b)
  ddf.cwd = lengthCWD(n,alp,c,a,b)
  df.cwd$gMean=ddf.cwd$explMean
  df.cwd$gMax=ddf.cwd$explMax
  df.cwd$gUL=ddf.cwd$explMean+ddf.cwd$explSD
  df.cwd$gLL=ddf.cwd$explMean-ddf.cwd$explSD

  ggplot2::ggplot(data=df.cwd, mapping=ggplot2::aes(x=hp, y=ew)) +
    ggplot2::labs(title = "Expected length of continuity corrected Wald") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(mapping=ggplot2::aes(colour=method), show_guide = TRUE) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMean, fill="Mean"),color="orange"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMax, fill="Max"),color="blue"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gLL, fill="Lower Limit"),color="cyan4"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gUL, fill="Upper Limit"),color="brown"  ) +
    ggplot2::scale_color_hue("Method") +
    ggplot2::scale_fill_manual(
      "Metric lines", values=c(1,1,1,1),
      guide=ggplot2::guide_legend(override.aes = list(colour=c("orange", "blue", "cyan4","brown"))),
      labels=c("Mean", "Max", "Lower Limit(Mean- 1SD)", "Upper Limit(Mean + 1SD)"))


}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplcwd`

```python
    def _plot(n, alp, c, a, b, seed=None):
        fn, lo, hi = _CC[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp, c),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve,
                          f"Expected length - continuity-corrected {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplex`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplex
```

**In plain words** — Plots the expected-length curve against *p* for the Exact (Clopper-Pearson / mid-p) interval — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexplex(20, 0.05, 0.5, 1, 1, seed=0)
```

**R source** — [`R/302.Expec_Leng_BASE_All_Graph.R` (line 23)](https://github.com/RajeswaranV/proportion/blob/master/R/302.Expec_Leng_BASE_All_Graph.R#L23), function `PlotexplEX`

```r
PlotexplEX<-function(n,alp,e,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(e)) stop("'e' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (any(e>1) || any(e<0)) stop("'e' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ewEX=NULL

  ELEX2=gexplEX(n,alp,e,a,b)
  ELEX2$e=as.factor(ELEX2$e)

  ggplot2::ggplot(ELEX2, ggplot2::aes(x=hp, y=ewEX, color=e))+
    ggplot2::labs(title = "Expected length of Exact method") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::geom_vline(ggplot2::aes(xintercept=0.5),linetype = 2)+
    ggplot2::labs(x = "p") +
    ggplot2::geom_line()

}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplex`

```python
def plotexplex(n, alp, e, a, b, seed=None):
    """Expected-length curve for the Exact method (R PlotexplEX)."""
    df = ciex(n, alp, [e])
    lengths = df['UEX'].to_numpy() - df['LEX'].to_numpy()
    curve = _expl_curve(n, lengths, _beta_hp(a, b, seed), "Exact")
    return _expl_plot(curve, "Expected length - Exact method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplgen`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplgen
```

**In plain words** — Plots the expected-length curve against *p* for user-supplied interval limits — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
wd = bk.ciwd(20, 0.05)
bk.plotexplgen(20, wd["LWD"].values, wd["UWD"].values, [0.2, 0.5, 0.8])
```

**R source** — [`R/327.Expec_Leng_GENERAL_GIVENp.R` (line 16)](https://github.com/RajeswaranV/proportion/blob/master/R/327.Expec_Leng_GENERAL_GIVENp.R#L16), function `PlotexplGEN`

```r
PlotexplGEN<-function(n,LL,UL,hp)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(LL)) stop("'Lower limit' is missing")
  if (missing(UL)) stop("'Upper Limit' is missing")
  if (missing(hp)) stop("'hp' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if ((class(LL) != "integer") & (class(LL) != "numeric") || any(LL < 0)) stop("'LL' has to be a set of positive numeric vectors")
  if ((class(UL) != "integer") & (class(UL) != "numeric") || any(UL < 0)) stop("'UL' has to be a set of positive numeric vectors")
  if (length(LL) <= n ) stop("Length of vector LL has to be greater than n")
  if (length(UL) <= n ) stop("Length of vector UL has to be greater than n")
  if (any(LL[0:n+1] > UL[0:n+1] )) stop("LL value have to be lower than the corrosponding UL value")
  if (any(hp>1) || any(hp<0)) stop("'hp' has to be between 0 and 1")
  ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

####INPUT n
x=0:n
k=n+1
s=length(hp)
ewi=matrix(0,k,s)						#Expected length quantity in sum
ew=0									#Expected Length
LE=0

for(i in 1:k)
{
LE[i]=UL[i]-LL[i]
}

####Expected Length

for (j in 1:s)
{
for(i in 1:k)
{
ewi[i,j]=LE[i]*stats::dbinom(i-1, n,hp[j])
}
ew[j]=sum(ewi[,j])						#Expected Length
}
explMean=mean(ew)
explSD=stats::sd(ew)
explMax=max(ew)
explLL=explMean-(explSD)
explUL=explMean+(explSD)
EL=data.frame(hp,ew,method="General",explMean,explMax,explLL,explUL)

ggplot2::ggplot(data=EL, mapping=ggplot2::aes(x=hp, y=ew)) +
  ggplot2::labs(title = "Expected length given hypothetical 'p'") +
  ggplot2::labs(y = "Expected length") +
  ggplot2::labs(x = "p") +
  ggplot2::geom_line(mapping=ggplot2::aes(colour=method), show.legend = TRUE)  +
  ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=explMean, fill="Mean"),color="orange"  ) +
  ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=explMax, fill="Max"),color="blue"  ) +
  ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=explLL, fill="Lower Limit"),color="cyan4"  ) +
  ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=explUL, fill="Upper Limit"),color="brown"  ) +
  ggplot2::scale_color_hue("Method") +
  ggplot2::scale_fill_manual(
    "Metric lines", values=c(1,1,1,1),
    guide=ggplot2::guide_legend(override.aes = list(colour=c("orange", "blue", "cyan4","brown"))),
    labels=c("Mean", "Max", "Lower Limit(Mean- 1SD)", "Upper Limit(Mean + 1SD)"))

}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplgen`

```python
def plotexplgen(n, LL, UL, hp):
    """Expected-length curve for user-supplied limits over given hp (R PlotexplGEN)."""
    hp = np.atleast_1d(np.asarray(hp, dtype=float))
    lengths = np.asarray(UL, dtype=float) - np.asarray(LL, dtype=float)
    curve = _expl_curve(n, lengths, hp, "Given")
    return _expl_plot(curve, "Expected length (given p)")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexpllr`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexpllr
```

**In plain words** — Plots the expected-length curve against *p* for the Likelihood-Ratio interval — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexpllr(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/302.Expec_Leng_BASE_All_Graph.R` (line 538)](https://github.com/RajeswaranV/proportion/blob/master/R/302.Expec_Leng_BASE_All_Graph.R#L538), function `PlotexplLR`

```r
PlotexplLR<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=NULL

  df.lr=  gexplLR(n,alp,a,b)
  ddf.lr = lengthLR(n,alp,a,b)
  df.lr$gMean=ddf.lr$explMean
  df.lr$gMax=ddf.lr$explMax
  df.lr$gUL=ddf.lr$explMean+ddf.lr$explSD
  df.lr$gLL=ddf.lr$explMean-ddf.lr$explSD

  ggplot2::ggplot(data=df.lr, mapping=ggplot2::aes(x=hp, y=ew)) +
    ggplot2::labs(title = "Expected length of Likelihood Ratio method") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(mapping=ggplot2::aes(colour=method), show_guide = TRUE) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMean, fill="Mean"),color="orange"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMax, fill="Max"),color="blue"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gLL, fill="Lower Limit"),color="cyan4"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gUL, fill="Upper Limit"),color="brown"  ) +
    ggplot2::scale_color_hue("Method") +
    ggplot2::scale_fill_manual(
      "Metric lines", values=c(1,1,1,1),
      guide=ggplot2::guide_legend(override.aes = list(colour=c("orange", "blue", "cyan4","brown"))),
      labels=c("Mean", "Max", "Lower Limit(Mean- 1SD)", "Upper Limit(Mean + 1SD)"))

}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexpllr`

```python
    def base_variant(n, alp, a, b, seed=None):
        fn, lo, hi = reg[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve, f"Expected length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexpllt`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexpllt
```

**In plain words** — Plots the expected-length curve against *p* for the Logit-Wald interval — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexpllt(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/302.Expec_Leng_BASE_All_Graph.R` (line 434)](https://github.com/RajeswaranV/proportion/blob/master/R/302.Expec_Leng_BASE_All_Graph.R#L434), function `PlotexplLT`

```r
PlotexplLT<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=NULL

  df.lt=  gexplLT(n,alp,a,b)
  ddf.lt = lengthLT(n,alp,a,b)
  df.lt$gMean=ddf.lt$explMean
  df.lt$gMax=ddf.lt$explMax
  df.lt$gUL=ddf.lt$explMean+ddf.lt$explSD
  df.lt$gLL=ddf.lt$explMean-ddf.lt$explSD

  ggplot2::ggplot(data=df.lt, mapping=ggplot2::aes(x=hp, y=ew)) +
    ggplot2::labs(title = "Expected length of Logit Wald method") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(mapping=ggplot2::aes(colour=method), show_guide = TRUE) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMean, fill="Mean"),color="orange"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMax, fill="Max"),color="blue"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gLL, fill="Lower Limit"),color="cyan4"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gUL, fill="Upper Limit"),color="brown"  ) +
    ggplot2::scale_color_hue("Method") +
    ggplot2::scale_fill_manual(
      "Metric lines", values=c(1,1,1,1),
      guide=ggplot2::guide_legend(override.aes = list(colour=c("orange", "blue", "cyan4","brown"))),
      labels=c("Mean", "Max", "Lower Limit(Mean- 1SD)", "Upper Limit(Mean + 1SD)"))

}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexpllt`

```python
    def base_variant(n, alp, a, b, seed=None):
        fn, lo, hi = reg[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve, f"Expected length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplsc`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplsc
```

**In plain words** — Plots the expected-length curve against *p* for the Score / Wilson interval — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexplsc(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/302.Expec_Leng_BASE_All_Graph.R` (line 329)](https://github.com/RajeswaranV/proportion/blob/master/R/302.Expec_Leng_BASE_All_Graph.R#L329), function `PlotexplSC`

```r
PlotexplSC<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=NULL

  df.sc=  gexplSC(n,alp,a,b)
  ddf.sc = lengthSC(n,alp,a,b)
  df.sc$gMean=ddf.sc$explMean
  df.sc$gMax=ddf.sc$explMax
  df.sc$gUL=ddf.sc$explMean+ddf.sc$explSD
  df.sc$gLL=ddf.sc$explMean-ddf.sc$explSD

  ggplot2::ggplot(data=df.sc, mapping=ggplot2::aes(x=hp, y=ew)) +
    ggplot2::labs(title = "Expected length of Score method") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(mapping=ggplot2::aes(colour=method), show_guide = TRUE) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMean, fill="Mean"),color="orange"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMax, fill="Max"),color="blue"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gLL, fill="Lower Limit"),color="cyan4"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gUL, fill="Upper Limit"),color="brown"  ) +
    ggplot2::scale_color_hue("Method") +
    ggplot2::scale_fill_manual(
      "Metric lines", values=c(1,1,1,1),
      guide=ggplot2::guide_legend(override.aes = list(colour=c("orange", "blue", "cyan4","brown"))),
      labels=c("Mean", "Max", "Lower Limit(Mean- 1SD)", "Upper Limit(Mean + 1SD)"))

  }
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplsc`

```python
    def base_variant(n, alp, a, b, seed=None):
        fn, lo, hi = reg[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve, f"Expected length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplsim`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplsim
```

**In plain words** — Plots the expected-length curve against *p* for user-supplied limits over simulated p — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
wd = bk.ciwd(20, 0.05)
bk.plotexplsim(20, wd["LWD"].values, wd["UWD"].values, 1000, 1, 1, seed=0)
```

**R source** — [`R/326.Expec_Leng_GENERAL_SIMULATEDp.R` (line 18)](https://github.com/RajeswaranV/proportion/blob/master/R/326.Expec_Leng_GENERAL_SIMULATEDp.R#L18), function `PlotexplSIM`

```r
PlotexplSIM<-function(n,LL,UL,s,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(LL)) stop("'Lower limit' is missing")
  if (missing(UL)) stop("'Upper Limit' is missing")
  if (missing(s)) stop("'s' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if ((class(LL) != "integer") & (class(LL) != "numeric") || any(LL < 0)) stop("'LL' has to be a set of positive numeric vectors")
  if ((class(UL) != "integer") & (class(UL) != "numeric") || any(UL < 0)) stop("'UL' has to be a set of positive numeric vectors")
  if (length(LL) <= n ) stop("Length of vector LL has to be greater than n")
  if (length(UL) <= n ) stop("Length of vector UL has to be greater than n")
  if (any(LL[0:n+1] > UL[0:n+1] )) stop("LL value have to be lower than the corrosponding UL value")
  if ((class(s) != "integer") & (class(s) != "numeric") || length(s)>1 || s<1  ) stop("'b' has to be greater than or equal to 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=explMean=explMax=explLL=explUL=NULL

    ####INPUT n
x=0:n
k=n+1
ewi=matrix(0,k,s)						#Expected length quantity in sum
ew=0									#Expected Length
LE=0

for(i in 1:k)
{
LE[i]=UL[i]-LL[i]
}
####Expected Length
hp=sort(stats::rbeta(s,a,b),decreasing = FALSE)	#HYPOTHETICAL "p"
for (j in 1:s)
{
for(i in 1:k)
{
ewi[i,j]=LE[i]*stats::dbinom(i-1, n,hp[j])
}
ew[j]=sum(ewi[,j])						#Expected Length
}
explMean=mean(ew)
explSD=stats::sd(ew)
explMax=max(ew)
explLL=explMean-(explSD)
explUL=explMean+(explSD)
EL=data.frame(hp,ew,method="Simulation",explMean,explMax,explLL,explUL)

ggplot2::ggplot(data=EL, mapping=ggplot2::aes(x=hp, y=ew)) +
  ggplot2::labs(title = "Expected length of Simulation method") +
  ggplot2::labs(y = "Expected length") +
  ggplot2::labs(x = "p") +
  ggplot2::geom_line(mapping=ggplot2::aes(colour=method), show.legend  = TRUE)  +
  ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=explMean, fill="Mean"),color="orange"  ) +
  ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=explMax, fill="Max"),color="blue"  ) +
  ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=explLL, fill="Lower Limit"),color="cyan4"  ) +
  ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=explUL, fill="Upper Limit"),color="brown"  ) +
  ggplot2::scale_color_hue("Method") +
  ggplot2::scale_fill_manual(
    "Metric lines", values=c(1,1,1,1),
    guide=ggplot2::guide_legend(override.aes = list(colour=c("orange", "blue", "cyan4","brown"))),
    labels=c("Mean", "Max", "Lower Limit(Mean- 1SD)", "Upper Limit(Mean + 1SD)"))

}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplsim`

```python
def plotexplsim(n, LL, UL, s, a, b, seed=None):
    """Expected-length curve for user-supplied limits over simulated hp (R PlotexplSIM)."""
    hp = np.sort(np.random.default_rng(seed).beta(a, b, int(s)))
    lengths = np.asarray(UL, dtype=float) - np.asarray(LL, dtype=float)
    curve = _expl_curve(n, lengths, hp, "Simulated")
    return _expl_plot(curve, "Expected length (simulated p)")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexpltw`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexpltw
```

**In plain words** — Plots the expected-length curve against *p* for the Wald-T interval — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexpltw(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/302.Expec_Leng_BASE_All_Graph.R` (line 486)](https://github.com/RajeswaranV/proportion/blob/master/R/302.Expec_Leng_BASE_All_Graph.R#L486), function `PlotexplTW`

```r
PlotexplTW<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=NULL

  df.tw=  gexplTW(n,alp,a,b)
  ddf.tw = lengthTW(n,alp,a,b)
  df.tw$gMean=ddf.tw$explMean
  df.tw$gMax=ddf.tw$explMax
  df.tw$gUL=ddf.tw$explMean+ddf.tw$explSD
  df.tw$gLL=ddf.tw$explMean-ddf.tw$explSD

  ggplot2::ggplot(data=df.tw, mapping=ggplot2::aes(x=hp, y=ew)) +
    ggplot2::labs(title = "Expected length of Wald-T method") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(mapping=ggplot2::aes(colour=method), show_guide = TRUE) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMean, fill="Mean"),color="orange"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMax, fill="Max"),color="blue"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gLL, fill="Lower Limit"),color="cyan4"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gUL, fill="Upper Limit"),color="brown"  ) +
    ggplot2::scale_color_hue("Method") +
    ggplot2::scale_fill_manual(
      "Metric lines", values=c(1,1,1,1),
      guide=ggplot2::guide_legend(override.aes = list(colour=c("orange", "blue", "cyan4","brown"))),
      labels=c("Mean", "Max", "Lower Limit(Mean- 1SD)", "Upper Limit(Mean + 1SD)"))


}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexpltw`

```python
    def base_variant(n, alp, a, b, seed=None):
        fn, lo, hi = reg[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve, f"Expected length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotexplwd`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotexplwd
```

**In plain words** — Plots the expected-length curve against *p* for the Wald (normal-approximation) interval — a visualisation of the corresponding `expected-length curve` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotexplwd(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/302.Expec_Leng_BASE_All_Graph.R` (line 276)](https://github.com/RajeswaranV/proportion/blob/master/R/302.Expec_Leng_BASE_All_Graph.R#L276), function `PlotexplWD`

```r
PlotexplWD<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=NULL

  df.wd=  gexplWD(n,alp,a,b)
  ddf.wd = lengthWD(n,alp,a,b)
  df.wd$gMean=ddf.wd$explMean
  df.wd$gMax=ddf.wd$explMax
  df.wd$gUL=ddf.wd$explMean+ddf.wd$explSD
  df.wd$gLL=ddf.wd$explMean-ddf.wd$explSD


  ggplot2::ggplot(data=df.wd, mapping=ggplot2::aes(x=hp, y=ew)) +
    ggplot2::labs(title = "Expected length of Wald method") +
    ggplot2::labs(y = "Expected length") +
    ggplot2::labs(x = "p") +
    ggplot2::geom_line(mapping=ggplot2::aes(colour=method), show_guide = TRUE)  +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMean, fill="Mean"),color="orange"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gMax, fill="Max"),color="blue"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gLL, fill="Lower Limit"),color="cyan4"  ) +
    ggplot2::geom_hline(mapping=ggplot2::aes(yintercept=gUL, fill="Upper Limit"),color="brown"  ) +
    ggplot2::scale_color_hue("Method") +
    ggplot2::scale_fill_manual(
      "Metric lines", values=c(1,1,1,1),
      guide=ggplot2::guide_legend(override.aes = list(colour=c("orange", "blue", "cyan4","brown"))),
      labels=c("Mean", "Max", "Lower Limit(Mean- 1SD)", "Upper Limit(Mean + 1SD)"))


}
```

**What the R code does** — The R function calls the numeric function and draws the expected-length curve against *p* with ggplot2.

**Python source** — `binomcikit.expl.plots.plotexplwd`

```python
    def base_variant(n, alp, a, b, seed=None):
        fn, lo, hi = reg[name]
        curve = _expl_curve(n, _lengths_from(fn, lo, hi, n, alp),
                            _beta_hp(a, b, seed), name)
        return _expl_plot(curve, f"Expected length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthaall`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthaall
```

**In plain words** — Plots the sum-length bar chart for all adjusted interval methods — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthaall(20, 0.05, 2, 1, 1, seed=0)
```

**R source** — [`R/313.Sum_Leng_ADJ_All_Graph.R` (line 17)](https://github.com/RajeswaranV/proportion/blob/master/R/313.Sum_Leng_ADJ_All_Graph.R#L17), function `PlotlengthAAll`

```r
PlotlengthAAll<-function(n,alp,h,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h) >1|| h<0  || !(h%%1 ==0)) stop("'h' has to be an integer greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  full.df= lengthAAll(n,alp,h,a,b)

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("gray", "red", "#56B4E9", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length - Adjusted methods") +
    ggplot2::labs(x = "Method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthaall`

```python
def plotlengthaall(n, alp, h, a, b, seed=None):
    """Sum-length bars for all six adjusted methods (R PlotlengthAAll)."""
    return _length_plot(adj_all.lengthaall(n, alp, h, a, b, seed),
                        "Sum length - all adjusted methods")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthaas`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthaas
```

**In plain words** — Plots the sum-length bar chart for the adjusted ArcSine (variance-stabilised) interval — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthaas(20, 0.05, ..., 1, 1, seed=0)
```

**R source** — [`R/313.Sum_Leng_ADJ_All_Graph.R` (line 258)](https://github.com/RajeswaranV/proportion/blob/master/R/313.Sum_Leng_ADJ_All_Graph.R#L258), function `PlotlengthAAS`

```r
PlotlengthAAS<-function(n,alp,h,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  full.df= lengthAAS(n,alp,h,a,b)
  full.df$method="Adj-ArcSine"

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("orange", "red", "#56B4E9", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length - Adjusted ArcSine") +
    ggplot2::labs(x = "Method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthaas`

```python
    def _plot(n, alp, param, a, b, seed=None):
        summary = length_fn(n, alp, param, a, b, seed).copy()
        summary['method'] = label
        return _length_plot(summary, f"Sum length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthall`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthall
```

**In plain words** — Plots the sum-length bar chart for all interval methods — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthall(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/303.Sum_Leng_BASE_All_Graph.R` (line 16)](https://github.com/RajeswaranV/proportion/blob/master/R/303.Sum_Leng_BASE_All_Graph.R#L16), function `PlotlengthAll`

```r
PlotlengthAll<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  full.df= lengthAll(n,alp,a,b)

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("gray", "red", "#56B4E9", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity") +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length -6 Base methods") +
    ggplot2::labs(x = "Method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthall`

```python
def plotlengthall(n, alp, a, b, seed=None):
    """Sum-length bars for all six base methods (R PlotlengthAll)."""
    return _length_plot(base_all.lengthall(n, alp, a, b, seed),
                        "Sum length - all base methods")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthalr`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthalr
```

**In plain words** — Plots the sum-length bar chart for the adjusted Likelihood-Ratio interval — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthalr(20, 0.05, ..., 1, 1, seed=0)
```

**R source** — [`R/313.Sum_Leng_ADJ_All_Graph.R` (line 306)](https://github.com/RajeswaranV/proportion/blob/master/R/313.Sum_Leng_ADJ_All_Graph.R#L306), function `PlotlengthALR`

```r
PlotlengthALR<-function(n,alp,h,a,b)
{

  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h) >1|| h<0  || !(h%%1 ==0)) stop("'h' has to be an integer greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  full.df= lengthALR(n,alp,h,a,b)
  full.df$method="Adj-Likelihood Ratio"

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("orange", "red", "#56B4E9", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length - Adjusted Likelihood Ratio") +
    ggplot2::labs(x = "Method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthalr`

```python
    def _plot(n, alp, param, a, b, seed=None):
        summary = length_fn(n, alp, param, a, b, seed).copy()
        summary['method'] = label
        return _length_plot(summary, f"Sum length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthalt`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthalt
```

**In plain words** — Plots the sum-length bar chart for the adjusted Logit-Wald interval — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthalt(20, 0.05, ..., 1, 1, seed=0)
```

**R source** — [`R/313.Sum_Leng_ADJ_All_Graph.R` (line 210)](https://github.com/RajeswaranV/proportion/blob/master/R/313.Sum_Leng_ADJ_All_Graph.R#L210), function `PlotlengthALT`

```r
PlotlengthALT<-function(n,alp,h,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  full.df= lengthALT(n,alp,h,a,b)
  full.df$method="Adj-Logit Wald"

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("orange", "red", "#56B4E9", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length - Adjusted Logit Wald") +
    ggplot2::labs(x = "Method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthalt`

```python
    def _plot(n, alp, param, a, b, seed=None):
        summary = length_fn(n, alp, param, a, b, seed).copy()
        summary['method'] = label
        return _length_plot(summary, f"Sum length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthas`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthas
```

**In plain words** — Plots the sum-length bar chart for the ArcSine (variance-stabilised) interval — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthas(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/303.Sum_Leng_BASE_All_Graph.R` (line 259)](https://github.com/RajeswaranV/proportion/blob/master/R/303.Sum_Leng_BASE_All_Graph.R#L259), function `PlotlengthAS`

```r
PlotlengthAS<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  full.df= lengthAS(n,alp,a,b)
  full.df$method="ArcSine"

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("orange", "green", "#56B4E9", "orange","#F0E442", "#CC79A7",
                 "cyan4", "pink", "cyan", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length - ArcSine method") +
    ggplot2::labs(x = "method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthas`

```python
    def _plot(n, alp, a, b, seed=None):
        summary = length_fn(n, alp, a, b, seed).copy()
        summary['method'] = label
        return _length_plot(summary, f"Sum length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthasc`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthasc
```

**In plain words** — Plots the sum-length bar chart for the adjusted Score / Wilson interval — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthasc(20, 0.05, ..., 1, 1, seed=0)
```

**R source** — [`R/313.Sum_Leng_ADJ_All_Graph.R` (line 112)](https://github.com/RajeswaranV/proportion/blob/master/R/313.Sum_Leng_ADJ_All_Graph.R#L112), function `PlotlengthASC`

```r
PlotlengthASC<-function(n,alp,h,a,b)
{

  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  full.df= lengthAAS(n,alp,h,a,b)
  full.df$method="Adj-Score"

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("orange", "red", "#56B4E9", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length - Adjusted Score") +
    ggplot2::labs(x = "Method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthasc`

```python
    def _plot(n, alp, param, a, b, seed=None):
        summary = length_fn(n, alp, param, a, b, seed).copy()
        summary['method'] = label
        return _length_plot(summary, f"Sum length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthatw`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthatw
```

**In plain words** — Plots the sum-length bar chart for the adjusted Wald-T interval — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthatw(20, 0.05, ..., 1, 1, seed=0)
```

**R source** — [`R/313.Sum_Leng_ADJ_All_Graph.R` (line 161)](https://github.com/RajeswaranV/proportion/blob/master/R/313.Sum_Leng_ADJ_All_Graph.R#L161), function `PlotlengthATW`

```r
PlotlengthATW<-function(n,alp,h,a,b)
{

  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  full.df= lengthATW(n,alp,h,a,b)
  full.df$method="Adj-Wald-T"

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("orange", "red", "#56B4E9", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length - Adjusted Wald-T") +
    ggplot2::labs(x = "Method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthatw`

```python
    def _plot(n, alp, param, a, b, seed=None):
        summary = length_fn(n, alp, param, a, b, seed).copy()
        summary['method'] = label
        return _length_plot(summary, f"Sum length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthawd`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthawd
```

**In plain words** — Plots the sum-length bar chart for the adjusted Wald (normal-approximation) interval — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthawd(20, 0.05, ..., 1, 1, seed=0)
```

**R source** — [`R/313.Sum_Leng_ADJ_All_Graph.R` (line 63)](https://github.com/RajeswaranV/proportion/blob/master/R/313.Sum_Leng_ADJ_All_Graph.R#L63), function `PlotlengthAWD`

```r
PlotlengthAWD<-function(n,alp,h,a,b)
{

  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(h)) stop("'h' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(h) != "integer") & (class(h) != "numeric") || length(h)>1 || h<0  ) stop("'h' has to be greater than or equal to 0")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  full.df= lengthAWD(n,alp,h,a,b)
  full.df$method="Adj-Wald"

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("orange", "red", "#56B4E9", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length - Adjusted Wald") +
    ggplot2::labs(x = "Method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthawd`

```python
    def _plot(n, alp, param, a, b, seed=None):
        summary = length_fn(n, alp, param, a, b, seed).copy()
        summary['method'] = label
        return _length_plot(summary, f"Sum length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthba`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthba
```

**In plain words** — Plots the sum-length bar chart for the Bayesian credible interval — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthba(20, 0.05, 1, 1, 1, 1, seed=0)
```

**R source** — [`R/303.Sum_Leng_BASE_All_Graph.R` (line 120)](https://github.com/RajeswaranV/proportion/blob/master/R/303.Sum_Leng_BASE_All_Graph.R#L120), function `PlotlengthBA`

```r
PlotlengthBA<-function(n,alp,a,b,a1,a2)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if (missing(a1)) stop("'a1' is missing")
  if (missing(a2)) stop("'a2' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  if ((class(a1) != "integer") & (class(a1) != "numeric") || length(a1)>1 || a1<0 ) stop("'a1' has to be greater than or equal to 0")
  if ((class(a2) != "integer") & (class(a2) != "numeric") || length(a2)>1 || a2<0 ) stop("'a2' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  full.df= lengthBA(n,alp,a,b,a1,a2)

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c(  "#56B4E9", "orange")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=0.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length - Quantile & HPD of Bayesian method") +
    ggplot2::labs(x = "Method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthba`

```python
def plotlengthba(n, alp, a, b, a1, a2, seed=None):
    """Sum-length bars for the Bayesian interval, quantile+HPD (R PlotlengthBA)."""
    from .bayes import lengthba
    summary = lengthba(n, alp, a, b, a1, a2, seed)
    return _length_plot(summary, "Sum length - Bayesian method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; uses SciPy HPD (`_hpd.hpd_beta`); lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthcall`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthcall
```

**In plain words** — Plots the sum-length bar chart for all continuity-corrected interval methods — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthcall(20, 0.05, 0.02, 1, 1, seed=0)
```

**R source** — [`R/323.Sum_Leng_CC_All_Graph.R` (line 17)](https://github.com/RajeswaranV/proportion/blob/master/R/323.Sum_Leng_CC_All_Graph.R#L17), function `PlotlengthCAll`

```r
PlotlengthCAll<-function(n,alp,c,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if (c<=0 || c>(1/(2*n)) || length(c)>1) stop("'c' has to be positive and less than or equal to 1/(2*n)")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  full.df= lengthCAll(n,alp,c,a,b)

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("gray", "red", "#56B4E9", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=0.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length  - Continuity corrected methods") +
    ggplot2::labs(x = "Method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthcall`

```python
def plotlengthcall(n, alp, c, a, b, seed=None):
    """Sum-length bars for all five CC methods (R PlotlengthCAll)."""
    return _length_plot(cc_all.lengthcall(n, alp, c, a, b, seed),
                        "Sum length - all continuity-corrected methods")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthcas`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthcas
```

**In plain words** — Plots the sum-length bar chart for the continuity-corrected ArcSine (variance-stabilised) interval — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthcas(20, 0.05, ..., 1, 1, seed=0)
```

**R source** — [`R/323.Sum_Leng_CC_All_Graph.R` (line 159)](https://github.com/RajeswaranV/proportion/blob/master/R/323.Sum_Leng_CC_All_Graph.R#L159), function `PlotlengthCAS`

```r
PlotlengthCAS<-function(n,alp,c,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  full.df= lengthCAS(n,alp,c,a,b)
  full.df$method="Continuity corrected ArcSine"

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("orange", "red", "#56B4E9", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=0.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length  - Continuity corrected ArcSine") +
    ggplot2::labs(x = "Method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthcas`

```python
    def _plot(n, alp, param, a, b, seed=None):
        summary = length_fn(n, alp, param, a, b, seed).copy()
        summary['method'] = label
        return _length_plot(summary, f"Sum length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthclt`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthclt
```

**In plain words** — Plots the sum-length bar chart for the continuity-corrected Logit-Wald interval — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthclt(20, 0.05, ..., 1, 1, seed=0)
```

**R source** — [`R/323.Sum_Leng_CC_All_Graph.R` (line 207)](https://github.com/RajeswaranV/proportion/blob/master/R/323.Sum_Leng_CC_All_Graph.R#L207), function `PlotlengthCLT`

```r
PlotlengthCLT<-function(n,alp,c,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  full.df= lengthCLT(n,alp,c,a,b)
  full.df$method="Continuity corrected Logit Wald"

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("orange", "red", "#56B4E9", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=0.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length  - Continuity corrected Logit Wald") +
    ggplot2::labs(x = "Method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthclt`

```python
    def _plot(n, alp, param, a, b, seed=None):
        summary = length_fn(n, alp, param, a, b, seed).copy()
        summary['method'] = label
        return _length_plot(summary, f"Sum length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthcsc`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthcsc
```

**In plain words** — Plots the sum-length bar chart for the continuity-corrected Score / Wilson interval — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthcsc(20, 0.05, ..., 1, 1, seed=0)
```

**R source** — [`R/323.Sum_Leng_CC_All_Graph.R` (line 111)](https://github.com/RajeswaranV/proportion/blob/master/R/323.Sum_Leng_CC_All_Graph.R#L111), function `PlotlengthCSC`

```r
PlotlengthCSC<-function(n,alp,c,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if (c<=0 || c>(1/(2*n)) || length(c)>1) stop("'c' has to be positive and less than or equal to 1/(2*n)")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  full.df= lengthCSC(n,alp,c,a,b)
  full.df$method="Continuity corrected Score"

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("orange", "red", "#56B4E9", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=0.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length  - Continuity corrected Score") +
    ggplot2::labs(x = "Method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthcsc`

```python
    def _plot(n, alp, param, a, b, seed=None):
        summary = length_fn(n, alp, param, a, b, seed).copy()
        summary['method'] = label
        return _length_plot(summary, f"Sum length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthctw`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthctw
```

**In plain words** — Plots the sum-length bar chart for the continuity-corrected Wald-T interval — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthctw(20, 0.05, ..., 1, 1, seed=0)
```

**R source** — [`R/323.Sum_Leng_CC_All_Graph.R` (line 255)](https://github.com/RajeswaranV/proportion/blob/master/R/323.Sum_Leng_CC_All_Graph.R#L255), function `PlotlengthCTW`

```r
PlotlengthCTW<-function(n,alp,c,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  full.df= lengthCTW(n,alp,c,a,b)
  full.df$method="Continuity corrected Wald-T"

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("orange", "red", "#56B4E9", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=0.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length  - Continuity corrected Wald-T") +
    ggplot2::labs(x = "Method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthctw`

```python
    def _plot(n, alp, param, a, b, seed=None):
        summary = length_fn(n, alp, param, a, b, seed).copy()
        summary['method'] = label
        return _length_plot(summary, f"Sum length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthcwd`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthcwd
```

**In plain words** — Plots the sum-length bar chart for the continuity-corrected Wald (normal-approximation) interval — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthcwd(20, 0.05, ..., 1, 1, seed=0)
```

**R source** — [`R/323.Sum_Leng_CC_All_Graph.R` (line 63)](https://github.com/RajeswaranV/proportion/blob/master/R/323.Sum_Leng_CC_All_Graph.R#L63), function `PlotlengthCWD`

```r
PlotlengthCWD<-function(n,alp,c,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(c)) stop("'c' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(c) != "integer") & (class(c) != "numeric") || length(c) >1 || c<0 ) stop("'c' has to be positive")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  #### Calling functions and creating df
  full.df= lengthCWD(n,alp,c,a,b)
  full.df$method="Continuity corrected Wald"

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("orange", "red", "#56B4E9", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=0.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length  - Continuity corrected Wald") +
    ggplot2::labs(x = "Method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthcwd`

```python
    def _plot(n, alp, param, a, b, seed=None):
        summary = length_fn(n, alp, param, a, b, seed).copy()
        summary['method'] = label
        return _length_plot(summary, f"Sum length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthex`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthex
```

**In plain words** — Plots the sum-length bar chart for the Exact (Clopper-Pearson / mid-p) interval — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthex(20, 0.05, 0.5, 1, 1, seed=0)
```

**R source** — [`R/303.Sum_Leng_BASE_All_Graph.R` (line 68)](https://github.com/RajeswaranV/proportion/blob/master/R/303.Sum_Leng_BASE_All_Graph.R#L68), function `PlotlengthEX`

```r
PlotlengthEX<-function(n,alp,e,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(e)) stop("'e' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp)>1) stop("'alpha' has to be between 0 and 1")
  if (any(e>1) || any(e<0)) stop("'e' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  full.df= lengthEX(n,alp,e,a,b)
  full.df$e=as.factor(full.df$e)

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("green", "#56B4E9", "orange","#F0E442", "#CC79A7",
                 "cyan4", "pink", "cyan", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = e, y = sumLen,  fill=e)) +
    ggplot2::geom_bar(stat="identity",width=0.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length - Exact method") +
    ggplot2::labs(x = "e") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthex`

```python
def plotlengthex(n, alp, e, a, b, seed=None):
    """Sum-length bar for the Exact method (R PlotlengthEX)."""
    summary = base_all.lengthex(n, alp, e, a, b, seed).copy()
    summary['method'] = "Exact"
    return _length_plot(summary, "Sum length - Exact method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthgen`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthgen
```

**In plain words** — Plots the sum-length bar chart for user-supplied interval limits — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
wd = bk.ciwd(20, 0.05)
bk.plotlengthgen(20, wd["LWD"].values, wd["UWD"].values, [0.2, 0.5, 0.8])
```

**R source** — [`R/328.Sum_Leng_GENERAL_SIM.R` (line 88)](https://github.com/RajeswaranV/proportion/blob/master/R/328.Sum_Leng_GENERAL_SIM.R#L88), function `PlotlengthGEN`

```r
PlotlengthGEN<-function(n,LL,UL,hp)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(LL)) stop("'Lower limit' is missing")
  if (missing(UL)) stop("'Upper Limit' is missing")
  if (missing(hp)) stop("'hp' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if ((class(LL) != "integer") & (class(LL) != "numeric") || any(LL < 0)) stop("'LL' has to be a set of positive numeric vectors")
  if ((class(UL) != "integer") & (class(UL) != "numeric") || any(UL < 0)) stop("'UL' has to be a set of positive numeric vectors")
  if (length(LL) <= n ) stop("Length of vector LL has to be greater than n")
  if (length(UL) <= n ) stop("Length of vector UL has to be greater than n")
  if (any(LL[0:n+1] > UL[0:n+1] )) stop("LL value have to be lower than the corrosponding UL value")
  if (any(hp>1) || any(hp<0)) stop("'hp' has to be between 0 and 1")
  method=sumLen=NULL

  full.df=lengthGEN(n,LL,UL,hp)
  full.df$method="General"

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=.5) +
    ggplot2::scale_fill_manual(values="orange") +
    ggplot2::labs(title = "Sum Length - General method") +
    ggplot2::labs(x = "method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthgen`

```python
def plotlengthgen(n, LL, UL, hp):
    """Sum-length bar for user-supplied limits over given hp (R PlotlengthGEN)."""
    summary = lengthgen(n, LL, UL, hp).copy()
    summary['method'] = "Given"
    return _length_plot(summary, "Sum length (given p)")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthlr`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthlr
```

**In plain words** — Plots the sum-length bar chart for the Likelihood-Ratio interval — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthlr(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/303.Sum_Leng_BASE_All_Graph.R` (line 396)](https://github.com/RajeswaranV/proportion/blob/master/R/303.Sum_Leng_BASE_All_Graph.R#L396), function `PlotlengthLR`

```r
PlotlengthLR<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  full.df= lengthLR(n,alp,a,b)
  full.df$method="Likelihood Ratio"

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("orange", "green", "#56B4E9", "orange","#F0E442", "#CC79A7",
                 "cyan4", "pink", "cyan", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length - Likelihood Ratio method") +
    ggplot2::labs(x = "method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthlr`

```python
    def _plot(n, alp, a, b, seed=None):
        summary = length_fn(n, alp, a, b, seed).copy()
        summary['method'] = label
        return _length_plot(summary, f"Sum length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthlt`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthlt
```

**In plain words** — Plots the sum-length bar chart for the Logit-Wald interval — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthlt(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/303.Sum_Leng_BASE_All_Graph.R` (line 305)](https://github.com/RajeswaranV/proportion/blob/master/R/303.Sum_Leng_BASE_All_Graph.R#L305), function `PlotlengthLT`

```r
PlotlengthLT<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  full.df= lengthLT(n,alp,a,b)
  full.df$method="Logit Wald"

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("orange", "green", "#56B4E9", "orange","#F0E442", "#CC79A7",
                 "cyan4", "pink", "cyan", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length - Logit Wald method") +
    ggplot2::labs(x = "method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthlt`

```python
    def _plot(n, alp, a, b, seed=None):
        summary = length_fn(n, alp, a, b, seed).copy()
        summary['method'] = label
        return _length_plot(summary, f"Sum length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthsc`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthsc
```

**In plain words** — Plots the sum-length bar chart for the Score / Wilson interval — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthsc(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/303.Sum_Leng_BASE_All_Graph.R` (line 213)](https://github.com/RajeswaranV/proportion/blob/master/R/303.Sum_Leng_BASE_All_Graph.R#L213), function `PlotlengthSC`

```r
PlotlengthSC<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  full.df= lengthSC(n,alp,a,b)
  full.df$method="Score"

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("orange", "green", "#56B4E9", "orange","#F0E442", "#CC79A7",
                 "cyan4", "pink", "cyan", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length - Score method") +
    ggplot2::labs(x = "method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthsc`

```python
    def _plot(n, alp, a, b, seed=None):
        summary = length_fn(n, alp, a, b, seed).copy()
        summary['method'] = label
        return _length_plot(summary, f"Sum length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthsim`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthsim
```

**In plain words** — Plots the sum-length bar chart for user-supplied limits over simulated p — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
wd = bk.ciwd(20, 0.05)
bk.plotlengthsim(20, wd["LWD"].values, wd["UWD"].values, 1000, 1, 1, seed=0)
```

**R source** — [`R/328.Sum_Leng_GENERAL_SIM.R` (line 205)](https://github.com/RajeswaranV/proportion/blob/master/R/328.Sum_Leng_GENERAL_SIM.R#L205), function `PlotlengthSIM`

```r
PlotlengthSIM<-function(n,LL,UL,s,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(LL)) stop("'Lower limit' is missing")
  if (missing(UL)) stop("'Upper Limit' is missing")
  if (missing(s)) stop("'s' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if ((class(LL) != "integer") & (class(LL) != "numeric") || any(LL < 0)) stop("'LL' has to be a set of positive numeric vectors")
  if ((class(UL) != "integer") & (class(UL) != "numeric") || any(UL < 0)) stop("'UL' has to be a set of positive numeric vectors")
  if (length(LL) <= n ) stop("Length of vector LL has to be greater than n")
  if (length(UL) <= n ) stop("Length of vector UL has to be greater than n")
  if (any(LL[0:n+1] > UL[0:n+1] )) stop("LL value have to be lower than the corrosponding UL value")
  if ((class(s) != "integer") & (class(s) != "numeric") || length(s)>1 || s<1  ) stop("'b' has to be greater than or equal to 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  sumLen=method=NULL

  ####INPUT n
  x=0:n
  k=n+1
  ewi=matrix(0,k,s)						#Expected length quantity in sum
  ew=0									#Expected Length
  LE=0

  for(i in 1:k)
  {
    LE[i]=UL[i]-LL[i]
  }
  sumLen=sum(LE)
  EL=data.frame(sumLen,method="Simulation")

  ggplot2::ggplot(EL, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=.5) +
    ggplot2::scale_fill_manual(values="orange") +
    ggplot2::labs(title = "Sum Length - Simulation method") +
    ggplot2::labs(x = "method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthsim`

```python
def plotlengthsim(n, LL, UL, s, a, b, seed=None):
    """Sum-length bar for user-supplied limits over simulated hp (R PlotlengthSIM)."""
    summary = lengthsim(n, LL, UL, s, a, b, seed).copy()
    summary['method'] = "Simulated"
    return _length_plot(summary, "Sum length (simulated p)")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthtw`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthtw
```

**In plain words** — Plots the sum-length bar chart for the Wald-T interval — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthtw(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/303.Sum_Leng_BASE_All_Graph.R` (line 351)](https://github.com/RajeswaranV/proportion/blob/master/R/303.Sum_Leng_BASE_All_Graph.R#L351), function `PlotlengthTW`

```r
PlotlengthTW<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  full.df= lengthTW(n,alp,a,b)
  full.df$method="Wald-T"

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("orange", "green", "#56B4E9", "orange","#F0E442", "#CC79A7",
                 "cyan4", "pink", "cyan", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length - Wald-T method") +
    ggplot2::labs(x = "method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthtw`

```python
    def _plot(n, alp, a, b, seed=None):
        summary = length_fn(n, alp, a, b, seed).copy()
        summary['method'] = label
        return _length_plot(summary, f"Sum length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotlengthwd`

```{eval-rst}
.. autofunction:: binomcikit.expl.plots.plotlengthwd
```

**In plain words** — Plots the sum-length bar chart for the Wald (normal-approximation) interval — a visualisation of the corresponding `expected length` numbers.

**The maths** — None; a visualisation of the numeric result.

**Example**

```python
import binomcikit as bk
bk.plotlengthwd(20, 0.05, 1, 1, seed=0)
```

**R source** — [`R/303.Sum_Leng_BASE_All_Graph.R` (line 168)](https://github.com/RajeswaranV/proportion/blob/master/R/303.Sum_Leng_BASE_All_Graph.R#L168), function `PlotlengthWD`

```r
PlotlengthWD<-function(n,alp,a,b)
{
  if (missing(n)) stop("'n' is missing")
  if (missing(alp)) stop("'alpha' is missing")
  if (missing(a)) stop("'a' is missing")
  if (missing(b)) stop("'b' is missing")
  if ((class(n) != "integer") & (class(n) != "numeric") || length(n) >1|| n<=0 ) stop("'n' has to be greater than 0")
  if (alp>1 || alp<0 || length(alp) >1) stop("'alpha' has to be between 0 and 1")
  if ((class(a) != "integer") & (class(a) != "numeric") || length(a)>1 || a<0  ) stop("'a' has to be greater than or equal to 0")
  if ((class(b) != "integer") & (class(b) != "numeric") || length(b)>1 || b<0  ) stop("'b' has to be greater than or equal to 0")
  hp=ew=method=gMean=gMax=gLL=gUL=explUL=explLL=sumLen=NULL

  full.df= lengthWD(n,alp,a,b)
  full.df$method="Wald"

  g <- ggplot2::guide_legend("Mean")
  limits <- ggplot2::aes(ymax =explUL, ymin=explLL)
  cbPalette <- c("orange", "green", "#56B4E9", "orange","#F0E442", "#CC79A7",
                 "cyan4", "pink", "cyan", "orange","#F0E442", "#CC79A7")

  ggplot2::ggplot(full.df, ggplot2::aes(x = method, y = sumLen,  fill=method)) +
    ggplot2::geom_bar(stat="identity",width=.5) +
    ggplot2::scale_fill_manual(values=cbPalette) +
    ggplot2::labs(title = "Sum Length - Wald method") +
    ggplot2::labs(x = "method") +
    ggplot2::labs(y = "Sum of Length") +
    ggplot2::guides(colour = g, size = g, shape = g) +
    ggplot2::theme(legend.title = ggplot2::element_text(colour="black", size=11, face="bold"))+
    ggplot2::theme_classic()

}
```

**What the R code does** — The R function calls the numeric function and draws the sum-length bar chart with ggplot2.

**Python source** — `binomcikit.expl.plots.plotlengthwd`

```python
    def _plot(n, alp, a, b, seed=None):
        summary = length_fn(n, alp, a, b, seed).copy()
        summary['method'] = label
        return _length_plot(summary, f"Sum length - {label} method")

```

**What the Python code does** — The Python port builds the equivalent plotnine figure and returns a `ggplot`.

**R → Py changes** — ggplot2 → plotnine; returns a plotnine `ggplot`; lowercased name; pandas `DataFrame`

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

