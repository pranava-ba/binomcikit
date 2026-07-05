# `ci.adj_n_graph`

```{eval-rst}
.. module:: binomcikit.ci.adj_n_graph
```

**Plots** for the adjusted confidence-interval methods
({doc}`ci.adj_n <binomcikit.ci.adj_n>`). Each `plotcia*` function calls the
matching adjusted `cia*` numeric function and draws the intervals as horizontal
error bars across `x = 0…n`, taking the same pseudo-count argument `h`. No new
maths — these visualise the adjusted intervals. Every function returns a plotnine
`ggplot` (R used ggplot2).

```{contents} Functions in this module
:local:
:depth: 1
```

---

## `plotciawd`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n_graph.plotciawd
```

**In plain words** — Plots the **adjusted Wald** intervals from
{py:func}`ciawd <binomcikit.ci.adj_n.ciawd>`.

**The maths** — None; a visualisation of `ciawd`.

**Example**

```python
import binomcikit as bk
bk.plotciawd(20, 0.05, 2).draw()
```

**R source** — [`R/112.ConfidenceIntervals_ADJ_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/112.ConfidenceIntervals_ADJ_n_Graph.R), function `PlotciAWD`

**What the R code does** — Calls `ciAWD` and draws the intervals as error bars.

**Python source** — `binomcikit.ci.adj_n_graph.plotciawd`.

**What the Python code does** — The equivalent plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotciasc`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n_graph.plotciasc
```

**In plain words** — Plots the **adjusted Score** (Wilson) intervals from
{py:func}`ciasc <binomcikit.ci.adj_n.ciasc>`.

**The maths** — None; a visualisation of `ciasc`.

**Example**

```python
import binomcikit as bk
bk.plotciasc(20, 0.05, 2).draw()
```

**R source** — [`R/112.ConfidenceIntervals_ADJ_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/112.ConfidenceIntervals_ADJ_n_Graph.R), function `PlotciASC`

**What the R code does** — Draws the adjusted Wilson intervals as error bars.

**Python source** — `binomcikit.ci.adj_n_graph.plotciasc`.

**What the Python code does** — The equivalent plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotciaas`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n_graph.plotciaas
```

**In plain words** — Plots the **adjusted ArcSine** intervals from
{py:func}`ciaas <binomcikit.ci.adj_n.ciaas>`.

**The maths** — None; a visualisation of `ciaas`.

**Example**

```python
import binomcikit as bk
bk.plotciaas(20, 0.05, 2).draw()
```

**R source** — [`R/112.ConfidenceIntervals_ADJ_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/112.ConfidenceIntervals_ADJ_n_Graph.R), function `PlotciAAS`

**What the R code does** — Draws the adjusted ArcSine intervals as error bars.

**Python source** — `binomcikit.ci.adj_n_graph.plotciaas`.

**What the Python code does** — The equivalent plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotciatw`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n_graph.plotciatw
```

**In plain words** — Plots the **adjusted Wald-T** intervals from
{py:func}`ciatw <binomcikit.ci.adj_n.ciatw>`.

**The maths** — None; a visualisation of `ciatw`.

**Example**

```python
import binomcikit as bk
bk.plotciatw(20, 0.05, 2).draw()
```

**R source** — [`R/112.ConfidenceIntervals_ADJ_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/112.ConfidenceIntervals_ADJ_n_Graph.R), function `PlotciATW`

**What the R code does** — Draws the adjusted Wald-T intervals as error bars.

**Python source** — `binomcikit.ci.adj_n_graph.plotciatw`.

**What the Python code does** — The equivalent plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcialt`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n_graph.plotcialt
```

**In plain words** — Plots the **adjusted Logit-Wald** intervals from
{py:func}`cialt <binomcikit.ci.adj_n.cialt>`.

**The maths** — None; a visualisation of `cialt`.

**Example**

```python
import binomcikit as bk
bk.plotcialt(20, 0.05, 2).draw()
```

**R source** — [`R/112.ConfidenceIntervals_ADJ_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/112.ConfidenceIntervals_ADJ_n_Graph.R), function `PlotciALT`

**What the R code does** — Draws the adjusted Logit-Wald intervals as error bars.

**Python source** — `binomcikit.ci.adj_n_graph.plotcialt`.

**What the Python code does** — The equivalent plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcialr`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n_graph.plotcialr
```

**In plain words** — Plots the **adjusted Likelihood-Ratio** intervals from
{py:func}`cialr <binomcikit.ci.adj_n.cialr>`.

**The maths** — None; a visualisation of `cialr`.

**Example**

```python
import binomcikit as bk
bk.plotcialr(20, 0.05, 2).draw()
```

**R source** — [`R/112.ConfidenceIntervals_ADJ_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/112.ConfidenceIntervals_ADJ_n_Graph.R), function `PlotciALR`

**What the R code does** — Draws the adjusted LR intervals as error bars.

**Python source** — `binomcikit.ci.adj_n_graph.plotcialr`.

**What the Python code does** — The equivalent plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`
