# `ci.cc_n_graph`

```{eval-rst}
.. module:: binomcikit.ci.cc_n_graph
```

**Plots** for the continuity-corrected confidence-interval methods
({doc}`ci.cc_n <binomcikit.ci.cc_n>`). Each `plotcic*` function calls the
matching CC `cic*` numeric function and draws the intervals as horizontal error
bars across `x = 0…n`, taking the same continuity-correction argument `c`. Five
methods (no Likelihood-Ratio). No new maths; every function returns a plotnine
`ggplot` (R used ggplot2).

```{contents} Functions in this module
:local:
:depth: 1
```

---

## `plotcicwd`

```{eval-rst}
.. autofunction:: binomcikit.ci.cc_n_graph.plotcicwd
```

**In plain words** — Plots the **continuity-corrected Wald** intervals from
{py:func}`cicwd <binomcikit.ci.cc_n.cicwd>`.

**The maths** — None; a visualisation of `cicwd`.

**Example**

```python
import binomcikit as bk
bk.plotcicwd(20, 0.05, 1/40).draw()
```

**R source** — [`R/122.ConfidenceIntervals_CC_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/122.ConfidenceIntervals_CC_n_Graph.R), function `PlotciCWD`

**What the R code does** — Calls `ciCWD` and draws the intervals as error bars.

**Python source** — `binomcikit.ci.cc_n_graph.plotcicwd`.

**What the Python code does** — The equivalent plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcicsc`

```{eval-rst}
.. autofunction:: binomcikit.ci.cc_n_graph.plotcicsc
```

**In plain words** — Plots the **continuity-corrected Score** (Wilson) intervals
from {py:func}`cicsc <binomcikit.ci.cc_n.cicsc>`.

**The maths** — None; a visualisation of `cicsc`.

**Example**

```python
import binomcikit as bk
bk.plotcicsc(20, 0.05, 1/40).draw()
```

**R source** — [`R/122.ConfidenceIntervals_CC_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/122.ConfidenceIntervals_CC_n_Graph.R), function `PlotciCSC`

**What the R code does** — Draws the CC Wilson intervals as error bars.

**Python source** — `binomcikit.ci.cc_n_graph.plotcicsc`.

**What the Python code does** — The equivalent plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcicas`

```{eval-rst}
.. autofunction:: binomcikit.ci.cc_n_graph.plotcicas
```

**In plain words** — Plots the **continuity-corrected ArcSine** intervals from
{py:func}`cicas <binomcikit.ci.cc_n.cicas>`.

**The maths** — None; a visualisation of `cicas`.

**Example**

```python
import binomcikit as bk
bk.plotcicas(20, 0.05, 1/40).draw()
```

**R source** — [`R/122.ConfidenceIntervals_CC_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/122.ConfidenceIntervals_CC_n_Graph.R), function `PlotciCAS`

**What the R code does** — Draws the CC ArcSine intervals as error bars.

**Python source** — `binomcikit.ci.cc_n_graph.plotcicas`.

**What the Python code does** — The equivalent plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotcictw`

```{eval-rst}
.. autofunction:: binomcikit.ci.cc_n_graph.plotcictw
```

**In plain words** — Plots the **continuity-corrected Wald-T** intervals from
{py:func}`cictw <binomcikit.ci.cc_n.cictw>`.

**The maths** — None; a visualisation of `cictw`.

**Example**

```python
import binomcikit as bk
bk.plotcictw(20, 0.05, 1/40).draw()
```

**R source** — [`R/122.ConfidenceIntervals_CC_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/122.ConfidenceIntervals_CC_n_Graph.R), function `PlotciCTW`

**What the R code does** — Draws the CC Wald-T intervals as error bars.

**Python source** — `binomcikit.ci.cc_n_graph.plotcictw`.

**What the Python code does** — The equivalent plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `plotciclt`

```{eval-rst}
.. autofunction:: binomcikit.ci.cc_n_graph.plotciclt
```

**In plain words** — Plots the **continuity-corrected Logit-Wald** intervals from
{py:func}`ciclt <binomcikit.ci.cc_n.ciclt>`.

**The maths** — None; a visualisation of `ciclt`.

**Example**

```python
import binomcikit as bk
bk.plotciclt(20, 0.05, 1/40).draw()
```

**R source** — [`R/122.ConfidenceIntervals_CC_n_Graph.R`](https://github.com/RajeswaranV/proportion/blob/master/R/122.ConfidenceIntervals_CC_n_Graph.R), function `PlotciCLT`

**What the R code does** — Draws the CC Logit-Wald intervals as error bars.

**Python source** — `binomcikit.ci.cc_n_graph.plotciclt`.

**What the Python code does** — The equivalent plotnine figure.

**R → Py changes** — Naming lowercased; ggplot2 → plotnine.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`
