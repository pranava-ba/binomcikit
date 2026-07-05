# `ci.base_n_graph`

```{eval-rst}
.. module:: binomcikit.ci.base_n_graph
```

**Plots** for the base confidence-interval methods of
{doc}`ci.base_n <binomcikit.ci.base_n>`. Each `plotci*` function calls the
matching `ci*` numeric function and draws the intervals as **horizontal error
bars** — one bar per `x = 0…n` — so you can see how the interval width and any
clamping (`LABB`/`UABB`) or zero-width (`ZWI`) points vary across `x`.

There is no new maths here: these are visualisations of the numbers computed by
`ci.base_n`. Every function returns a **plotnine `ggplot`** object (the R
package used **ggplot2**); call `.draw()` or `print()` to render it, or `+` more
layers onto it.

```{contents} Functions in this module
:local:
:depth: 1
```

---

## `plotciwd`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n_graph.plotciwd
```

**In plain words** — Plots the **Wald** intervals from
{py:func}`ciwd <binomcikit.ci.base_n.ciwd>` as horizontal error bars, with
aberration points marked.

**The maths** — None; a visualisation of `ciwd`.

**Example**

```python
import binomcikit as bk
p = bk.plotciwd(20, 0.05)
p.draw()      # or print(p)
```

**R source** — [`R/102.Confidence_base_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/102.Confidence_base_n_Graph.R), function `PlotciWD`

**What the R code does** — Calls `ciWD`, reshapes the aberration flags, and
draws `ggplot2::geom_errorbarh` plus points for the clamped/zero-width cases.

**Python source** — `binomcikit.ci.base_n_graph.plotciwd` — the same, using
plotnine's `geom_errorbarh`/`geom_point`.

**What the Python code does** — Builds the equivalent plotnine figure and
returns the `ggplot` object.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine; returns a plotnine
`ggplot`.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcisc`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n_graph.plotcisc
```

**In plain words** — Plots the **Score** (Wilson) intervals from
{py:func}`cisc <binomcikit.ci.base_n.cisc>`.

**The maths** — None; a visualisation of `cisc`.

**Example**

```python
import binomcikit as bk
bk.plotcisc(20, 0.05).draw()
```

**R source** — [`R/102.Confidence_base_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/102.Confidence_base_n_Graph.R), function `PlotciSC`

**What the R code does** — Draws the Wilson intervals as error bars.

**Python source** — `binomcikit.ci.base_n_graph.plotcisc`.

**What the Python code does** — The equivalent plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcias`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n_graph.plotcias
```

**In plain words** — Plots the **ArcSine** intervals from
{py:func}`cias <binomcikit.ci.base_n.cias>`.

**The maths** — None; a visualisation of `cias`.

**Example**

```python
import binomcikit as bk
bk.plotcias(20, 0.05).draw()
```

**R source** — [`R/102.Confidence_base_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/102.Confidence_base_n_Graph.R), function `PlotciAS`

**What the R code does** — Draws the ArcSine intervals as error bars.

**Python source** — `binomcikit.ci.base_n_graph.plotcias`.

**What the Python code does** — The equivalent plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcitw`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n_graph.plotcitw
```

**In plain words** — Plots the **Wald-T** intervals from
{py:func}`citw <binomcikit.ci.base_n.citw>`.

**The maths** — None; a visualisation of `citw`.

**Example**

```python
import binomcikit as bk
bk.plotcitw(20, 0.05).draw()
```

**R source** — [`R/102.Confidence_base_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/102.Confidence_base_n_Graph.R), function `PlotciTW`

**What the R code does** — Draws the Wald-T intervals as error bars.

**Python source** — `binomcikit.ci.base_n_graph.plotcitw`.

**What the Python code does** — The equivalent plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcilt`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n_graph.plotcilt
```

**In plain words** — Plots the **Logit-Wald** intervals from
{py:func}`cilt <binomcikit.ci.base_n.cilt>`.

**The maths** — None; a visualisation of `cilt`.

**Example**

```python
import binomcikit as bk
bk.plotcilt(20, 0.05).draw()
```

**R source** — [`R/102.Confidence_base_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/102.Confidence_base_n_Graph.R), function `PlotciLT`

**What the R code does** — Draws the Logit-Wald intervals as error bars.

**Python source** — `binomcikit.ci.base_n_graph.plotcilt`.

**What the Python code does** — The equivalent plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcilr`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n_graph.plotcilr
```

**In plain words** — Plots the **Likelihood-Ratio** intervals from
{py:func}`cilr <binomcikit.ci.base_n.cilr>`.

**The maths** — None; a visualisation of `cilr`.

**Example**

```python
import binomcikit as bk
bk.plotcilr(20, 0.05).draw()
```

**R source** — [`R/102.Confidence_base_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/102.Confidence_base_n_Graph.R), function `PlotciLR`

**What the R code does** — Draws the LR intervals as error bars.

**Python source** — `binomcikit.ci.base_n_graph.plotcilr`.

**What the Python code does** — The equivalent plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotciex`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n_graph.plotciex
```

**In plain words** — Plots the **Exact** intervals from
{py:func}`ciex <binomcikit.ci.base_n.ciex>` for a given tail parameter `e`.

**The maths** — None; a visualisation of `ciex`.

**Example**

```python
import binomcikit as bk
bk.plotciex(20, 0.05, 1).draw()     # Clopper-Pearson (e = 1)
```

**R source** — [`R/102.Confidence_base_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/102.Confidence_base_n_Graph.R), function `PlotciEX`

**What the R code does** — Draws the exact intervals as error bars.

**Python source** — `binomcikit.ci.base_n_graph.plotciex`.

**What the Python code does** — The equivalent plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`
