# `ci.base_n_x_graph`

```{eval-rst}
.. module:: binomcikit.ci.base_n_x_graph
```

**Plots** for the base, given-*x* confidence-interval methods
({doc}`ci.base_n_x <binomcikit.ci.base_n_x>`). These draw the intervals for a
single observed `x` — either the Exact interval across several tail values `e`,
or all six methods together — as horizontal error bars. Every function returns a
plotnine `ggplot`.

```{note}
This module corresponds to R file `104.ConfidenceIntervals_BASE_n_x_Graph.R`,
which in the earlier Python port was **broken** (a syntax error that stopped the
whole package importing) and contained the wrong content. It was rewritten from
the R source; see the {doc}`mapping table </r_to_python_mapping>` intro for the
history.
```

```{contents} Functions in this module
:local:
:depth: 1
```

---

## `plotciexx`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n_x_graph.plotciexx
```

**In plain words** — Plots the **Exact** interval for a single `x` across a
vector of tail-tuning values `e`, colouring each `e` differently — so you can
see how the interval tightens from Clopper–Pearson (`e = 1`) toward mid-*p*
(`e = 0.5`).

**The maths** — None; a visualisation of
{py:func}`ciexx <binomcikit.ci.base_n_x.ciexx>`.

**Example**

```python
import binomcikit as bk
bk.plotciexx(2, 10, 0.05, [0.1, 0.5, 1.0]).draw()
```

**R source** — [`R/104.ConfidenceIntervals_BASE_n_x_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/104.ConfidenceIntervals_BASE_n_x_Graph.R), function `PlotciEXx`

**What the R code does** — Calls `ciEXx` and draws one error bar per `e`, with
aberration points overlaid.

**Python source** — `binomcikit.ci.base_n_x_graph.plotciexx` — the same in
plotnine (`geom_errorbarh` coloured by `e`).

**What the Python code does** — Builds the equivalent figure for the vector of
`e` values.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine. Rewritten from the R
source (the original port's `a_104` file was broken).

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotciallx`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n_x_graph.plotciallx
```

**In plain words** — Plots **all six base methods** for a single `x`, overlaid,
so you can compare where each method places its interval for the value you
observed.

**The maths** — None; a visualisation of
{py:func}`ciallx <binomcikit.ci.base_n_x.ciallx>`.

**Example**

```python
import binomcikit as bk
bk.plotciallx(2, 10, 0.05).draw()
```

**R source** — [`R/104.ConfidenceIntervals_BASE_n_x_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/104.ConfidenceIntervals_BASE_n_x_Graph.R), function `PlotciAllx`

**What the R code does** — Calls `ciAllx` and overlays the six intervals,
coloured by method.

**Python source** — `binomcikit.ci.base_n_x_graph.plotciallx`.

**What the Python code does** — The equivalent overlaid plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine. Depends on the
newly-added `ciallx`.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotciallxg`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n_x_graph.plotciallxg
```

**In plain words** — The same as `plotciallx`, but **faceted** — one small panel
per method instead of overlaying them (the `g` = "grid" variant).

**The maths** — None; a visualisation of
{py:func}`ciallx <binomcikit.ci.base_n_x.ciallx>`.

**Example**

```python
import binomcikit as bk
bk.plotciallxg(2, 10, 0.05).draw()
```

**R source** — [`R/104.ConfidenceIntervals_BASE_n_x_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/104.ConfidenceIntervals_BASE_n_x_Graph.R), function `PlotciAllxg`

**What the R code does** — Draws the six intervals faceted by method with
`facet_grid`.

**Python source** — `binomcikit.ci.base_n_x_graph.plotciallxg` — plotnine
`facet_grid('method ~ .')`.

**What the Python code does** — The equivalent faceted plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`
