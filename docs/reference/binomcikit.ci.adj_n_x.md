# `ci.adj_n_x`

```{eval-rst}
.. module:: binomcikit.ci.adj_n_x
```

The **adjusted, given-*x*** confidence-interval methods: the pseudo-count
adjustment of {doc}`ci.adj_n <binomcikit.ci.adj_n>` (replace `x, n` with
`x + h, n + 2h`), applied to a **single observed `x`** and returned as one row.
See `ci.adj_n` for the adjustment idea and `ci.base_n_x` for the given-`x` form.

```{contents} Functions in this module
:local:
:depth: 1
```

---

## `ciawdx`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n_x.ciawdx
```

**In plain words** — Adjusted **Wald** interval for a single `x`.

**The maths** — `p̃ ± z√(p̃(1−p̃)/ñ)` with `p̃ = (x+h)/(n+2h)`, `ñ = n+2h`.

**Example**

```python
import binomcikit as bk
bk.ciawdx(2, 10, 0.05, 2)
```

**R source** — [`R/113.ConfidenceIntervals_ADJ_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/113.ConfidenceIntervals_ADJ_n_x.R), function `ciAWDx`

**What the R code does** — Adjusted Wald limits for the given `x`.

**Python source** — `binomcikit.ci.adj_n_x.ciawdx` — one-row result.

**What the Python code does** — Single adjusted Wald interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ciascx`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n_x.ciascx
```

**In plain words** — Adjusted **Score** (Wilson) interval for a single `x`.

**The maths** — Wilson formula at `x+h`, `n+2h`.

**Example**

```python
import binomcikit as bk
bk.ciascx(2, 10, 0.05, 2)
```

**R source** — [`R/113.ConfidenceIntervals_ADJ_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/113.ConfidenceIntervals_ADJ_n_x.R), function `ciASCx`

**What the R code does** — Adjusted Wilson interval for the given `x`.

**Python source** — `binomcikit.ci.adj_n_x.ciascx` — one-row result.

**What the Python code does** — Single adjusted Wilson interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ciaasx`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n_x.ciaasx
```

**In plain words** — Adjusted **ArcSine** interval for a single `x`.

**The maths** — $\sin^2(\arcsin\sqrt{\tilde{p}} \pm z/(2\sqrt{\tilde{n}}))$.

**Example**

```python
import binomcikit as bk
bk.ciaasx(2, 10, 0.05, 2)
```

**R source** — [`R/113.ConfidenceIntervals_ADJ_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/113.ConfidenceIntervals_ADJ_n_x.R), function `ciAASx`

**What the R code does** — Adjusted ArcSine interval for the given `x`.

**Python source** — `binomcikit.ci.adj_n_x.ciaasx` — one-row result.

**What the Python code does** — Single adjusted ArcSine interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ciatwx`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n_x.ciatwx
```

**In plain words** — Adjusted **Wald-T** interval for a single `x`.

**The maths** — `p̃ ± t·SE*` on the pseudo-count data.

**Example**

```python
import binomcikit as bk
bk.ciatwx(2, 10, 0.05, 2)
```

**R source** — [`R/113.ConfidenceIntervals_ADJ_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/113.ConfidenceIntervals_ADJ_n_x.R), function `ciATWx`

**What the R code does** — Adjusted Wald-T interval for the given `x`.

**Python source** — `binomcikit.ci.adj_n_x.ciatwx` — one-row result.

**What the Python code does** — Single adjusted Wald-T interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`; `stats::qt` →
`scipy.stats.t.ppf`. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `cialtx`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n_x.cialtx
```

**In plain words** — Adjusted **Logit-Wald** interval for a single `x`.

**The maths** — Logit-scale Wald interval from `p̃`, back-transformed.

**Example**

```python
import binomcikit as bk
bk.cialtx(2, 10, 0.05, 2)
```

**R source** — [`R/113.ConfidenceIntervals_ADJ_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/113.ConfidenceIntervals_ADJ_n_x.R), function `ciALTx`

**What the R code does** — Adjusted Logit-Wald interval for the given `x`.

**Python source** — `binomcikit.ci.adj_n_x.cialtx` — one-row result.

**What the Python code does** — Single adjusted Logit-Wald interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `cialrx`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n_x.cialrx
```

**In plain words** — Adjusted **Likelihood-Ratio** interval for a single `x`.

**The maths** — LR interval from the pseudo-count log-likelihood, solved
numerically.

**Example**

```python
import binomcikit as bk
bk.cialrx(2, 10, 0.05, 2)
```

**R source** — [`R/113.ConfidenceIntervals_ADJ_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/113.ConfidenceIntervals_ADJ_n_x.R), function `ciALRx`

**What the R code does** — Adjusted LR interval for the given `x`.

**Python source** — `binomcikit.ci.adj_n_x.cialrx` — `scipy.optimize`, one-row
result.

**What the Python code does** — Single adjusted LR interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`; numerical solve via
SciPy. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ciaallx`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n_x.ciaallx
```

**In plain words** — Runs **all six adjusted methods** for a single `x` and
stacks them into one long-format table — the given-`x`, adjusted analogue of
{py:func}`ciall <binomcikit.ci.base_n.ciall>`.

**The maths** — None of its own; calls the six adjusted given-`x` methods above.

**Example**

```python
import binomcikit as bk
df = bk.ciaallx(2, 10, 0.05, 2)
set(df["method"])
# {'Wald','ArcSine','Likelihood','Score','Wald-T','Logit-Wald'}
```

**R source** — [`R/113.ConfidenceIntervals_ADJ_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/113.ConfidenceIntervals_ADJ_n_x.R), function `ciAAllx`

**What the R code does** — Calls the six adjusted given-`x` methods, tags each
with a `method` factor, and `rbind`s them.

**Python source** — `binomcikit.ci.adj_n_x.ciaallx` — same, via `pandas.concat`.

**What the Python code does** — Six-row long-format table for the single `x`.

**R → Py changes** — Naming lowercased; `rbind` → `pandas.concat`; pandas
`DataFrame`. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`
