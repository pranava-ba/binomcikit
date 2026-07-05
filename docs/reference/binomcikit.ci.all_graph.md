# `ci.all_graph`

```{eval-rst}
.. module:: binomcikit.ci.all_graph
```

**Combined "all-methods" plots** — visualisations of the `ci*all*` numeric
functions, which stack several interval methods into one long-format table.
Each method's intervals are drawn as horizontal error bars; two layouts are
offered per family:

- the plain name (e.g. `plotciall`) **overlays** all methods, coloured by
  method;
- the `g` suffix (e.g. `plotciallg`) **facets** — one small panel per method.

`x`-suffixed variants (`plotciaallx`, `plotcicallx`, …) do the same for a single
observed `x`. `plotciba` draws the Bayesian credible interval. No new maths;
every function returns a plotnine `ggplot` (R used ggplot2).

```{contents} Functions in this module
:local:
:depth: 1
```

---

## `plotciall`

```{eval-rst}
.. autofunction:: binomcikit.ci.all_graph.plotciall
```

**In plain words** — Overlays **all six base methods**
({py:func}`ciall <binomcikit.ci.base_n.ciall>`) as error bars, coloured by
method.

**The maths** — None; a visualisation of `ciall`.

**Example**

```python
import binomcikit as bk
bk.plotciall(10, 0.05).draw()
```

**R source** — [`R/102.Confidence_base_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/102.Confidence_base_n_Graph.R), function `PlotciAll`

**What the R code does** — Calls `ciAll` and overlays the six methods' intervals.

**Python source** — `binomcikit.ci.all_graph.plotciall`.

**What the Python code does** — The equivalent overlaid plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotciallg`

```{eval-rst}
.. autofunction:: binomcikit.ci.all_graph.plotciallg
```

**In plain words** — The faceted version of `plotciall` — one panel per base
method.

**The maths** — None; a visualisation of `ciall`.

**Example**

```python
import binomcikit as bk
bk.plotciallg(10, 0.05).draw()
```

**R source** — [`R/102.Confidence_base_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/102.Confidence_base_n_Graph.R), function `PlotciAllg`

**What the R code does** — Facets the six base methods with `facet_grid`.

**Python source** — `binomcikit.ci.all_graph.plotciallg`.

**What the Python code does** — The equivalent faceted plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotciaall`

```{eval-rst}
.. autofunction:: binomcikit.ci.all_graph.plotciaall
```

**In plain words** — Overlays **all six adjusted methods**
({py:func}`ciaall <binomcikit.ci.adj_n.ciaall>`); takes the pseudo-count `h`.

**The maths** — None; a visualisation of `ciaall`.

**Example**

```python
import binomcikit as bk
bk.plotciaall(10, 0.05, 2).draw()
```

**R source** — [`R/112.ConfidenceIntervals_ADJ_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/112.ConfidenceIntervals_ADJ_n_Graph.R), function `PlotciAAll`

**What the R code does** — Overlays the six adjusted methods' intervals.

**Python source** — `binomcikit.ci.all_graph.plotciaall`.

**What the Python code does** — The equivalent overlaid plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotciaallg`

```{eval-rst}
.. autofunction:: binomcikit.ci.all_graph.plotciaallg
```

**In plain words** — Faceted version of `plotciaall` — one panel per adjusted
method.

**The maths** — None; a visualisation of `ciaall`.

**Example**

```python
import binomcikit as bk
bk.plotciaallg(10, 0.05, 2).draw()
```

**R source** — [`R/112.ConfidenceIntervals_ADJ_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/112.ConfidenceIntervals_ADJ_n_Graph.R), function `PlotciAAllg`

**What the R code does** — Facets the six adjusted methods.

**Python source** — `binomcikit.ci.all_graph.plotciaallg`.

**What the Python code does** — The equivalent faceted plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotciaallx`

```{eval-rst}
.. autofunction:: binomcikit.ci.all_graph.plotciaallx
```

**In plain words** — Overlays all six adjusted methods for a **single `x`**
({py:func}`ciaallx <binomcikit.ci.adj_n_x.ciaallx>`).

**The maths** — None; a visualisation of `ciaallx`.

**Example**

```python
import binomcikit as bk
bk.plotciaallx(2, 10, 0.05, 2).draw()
```

**R source** — [`R/104.ConfidenceIntervals_BASE_n_x_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/104.ConfidenceIntervals_BASE_n_x_Graph.R), function `PlotciAAllx`

**What the R code does** — Overlays the six adjusted intervals for the given `x`.

**Python source** — `binomcikit.ci.all_graph.plotciaallx`.

**What the Python code does** — The equivalent overlaid plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotciaallxg`

```{eval-rst}
.. autofunction:: binomcikit.ci.all_graph.plotciaallxg
```

**In plain words** — Faceted version of `plotciaallx` for a single `x`.

**The maths** — None; a visualisation of `ciaallx`.

**Example**

```python
import binomcikit as bk
bk.plotciaallxg(2, 10, 0.05, 2).draw()
```

**R source** — [`R/104.ConfidenceIntervals_BASE_n_x_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/104.ConfidenceIntervals_BASE_n_x_Graph.R), function `PlotciAAllxg`

**What the R code does** — Facets the six adjusted intervals for the given `x`.

**Python source** — `binomcikit.ci.all_graph.plotciaallxg`.

**What the Python code does** — The equivalent faceted plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcicall`

```{eval-rst}
.. autofunction:: binomcikit.ci.all_graph.plotcicall
```

**In plain words** — Overlays **all five continuity-corrected methods**
({py:func}`cicall <binomcikit.ci.cc_n.cicall>`); takes the correction `c`.

**The maths** — None; a visualisation of `cicall`.

**Example**

```python
import binomcikit as bk
bk.plotcicall(20, 0.05, 1/40).draw()
```

**R source** — [`R/122.ConfidenceIntervals_CC_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/122.ConfidenceIntervals_CC_n_Graph.R), function `PlotciCAll`

**What the R code does** — Overlays the five CC methods' intervals.

**Python source** — `binomcikit.ci.all_graph.plotcicall`.

**What the Python code does** — The equivalent overlaid plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcicallg`

```{eval-rst}
.. autofunction:: binomcikit.ci.all_graph.plotcicallg
```

**In plain words** — Faceted version of `plotcicall` — one panel per CC method.

**The maths** — None; a visualisation of `cicall`.

**Example**

```python
import binomcikit as bk
bk.plotcicallg(20, 0.05, 1/40).draw()
```

**R source** — [`R/122.ConfidenceIntervals_CC_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/122.ConfidenceIntervals_CC_n_Graph.R), function `PlotciCAllg`

**What the R code does** — Facets the five CC methods.

**Python source** — `binomcikit.ci.all_graph.plotcicallg`.

**What the Python code does** — The equivalent faceted plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcicallx`

```{eval-rst}
.. autofunction:: binomcikit.ci.all_graph.plotcicallx
```

**In plain words** — Overlays all five CC methods for a **single `x`**
({py:func}`cicallx <binomcikit.ci.cc_n_x.cicallx>`).

**The maths** — None; a visualisation of `cicallx`.

**Example**

```python
import binomcikit as bk
bk.plotcicallx(2, 20, 0.05, 1/40).draw()
```

**R source** — [`R/104.ConfidenceIntervals_BASE_n_x_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/104.ConfidenceIntervals_BASE_n_x_Graph.R), function `PlotciCAllx`

**What the R code does** — Overlays the five CC intervals for the given `x`.

**Python source** — `binomcikit.ci.all_graph.plotcicallx`.

**What the Python code does** — The equivalent overlaid plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcicallxg`

```{eval-rst}
.. autofunction:: binomcikit.ci.all_graph.plotcicallxg
```

**In plain words** — Faceted version of `plotcicallx` for a single `x`.

**The maths** — None; a visualisation of `cicallx`.

**Example**

```python
import binomcikit as bk
bk.plotcicallxg(2, 20, 0.05, 1/40).draw()
```

**R source** — [`R/104.ConfidenceIntervals_BASE_n_x_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/104.ConfidenceIntervals_BASE_n_x_Graph.R), function `PlotciCAllxg`

**What the R code does** — Facets the five CC intervals for the given `x`.

**Python source** — `binomcikit.ci.all_graph.plotcicallxg`.

**What the Python code does** — The equivalent faceted plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotciba`

```{eval-rst}
.. autofunction:: binomcikit.ci.all_graph.plotciba
```

**In plain words** — Draws the **Bayesian credible intervals**
({py:func}`ciba <binomcikit.ci.bayes_n.ciba>`) as error bars, showing both the
quantile-based and HPD intervals so their widths can be compared.

**The maths** — None; a visualisation of `ciba` (posterior `Beta(x+a, n−x+b)`).

**Example**

```python
import binomcikit as bk
bk.plotciba(10, 0.05, 1, 1).draw()      # uniform prior Beta(1, 1)
```

**R source** — [`R/102.Confidence_base_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/102.Confidence_base_n_Graph.R), function `PlotciBA`

**What the R code does** — Calls `ciBA` and draws the quantile and HPD intervals
as error bars.

**Python source** — `binomcikit.ci.all_graph.plotciba` — reshapes the quantile
and HPD limits into a long frame and draws them coloured by interval type.

**What the Python code does** — The equivalent plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine; the HPD limits come
from the SciPy HPD reimplementation (`_hpd.hpd_beta`).

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`
