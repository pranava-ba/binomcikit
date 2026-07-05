# `ci.cc_n_x`

```{eval-rst}
.. module:: binomcikit.ci.cc_n_x
```

The **continuity-corrected, given-*x*** confidence-interval methods: the
continuity correction of {doc}`ci.cc_n <binomcikit.ci.cc_n>` (push each limit out
by `c`, with `0 < c ≤ 1/(2n)`), applied to a **single observed `x`** and
returned as one row. Five methods (no Likelihood-Ratio). See `ci.cc_n` for the
correction and `ci.base_n_x` for the given-`x` form.

```{contents} Functions in this module
:local:
:depth: 1
```

---

## `cicwdx`

```{eval-rst}
.. autofunction:: binomcikit.ci.cc_n_x.cicwdx
```

**In plain words** — Continuity-corrected **Wald** interval for a single `x`.

**The maths** — `p̂ ± (z·SE + c)` at `p̂ = x/n`.

**Example**

```python
import binomcikit as bk
bk.cicwdx(2, 20, 0.05, 1/40)
```

**R source** — [`R/123.ConfidenceIntervals_CC_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/123.ConfidenceIntervals_CC_n_x.R), function `ciCWDx`

**What the R code does** — Continuity-corrected Wald limits for the given `x`.

**Python source** — `binomcikit.ci.cc_n_x.cicwdx` — one-row result.

**What the Python code does** — Single continuity-corrected Wald interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `cicscx`

```{eval-rst}
.. autofunction:: binomcikit.ci.cc_n_x.cicscx
```

**In plain words** — Continuity-corrected **Score** (Wilson) interval for a
single `x`.

**The maths** — Wilson formula with the continuity correction, at `p̂ = x/n`.

**Example**

```python
import binomcikit as bk
bk.cicscx(2, 20, 0.05, 1/40)
```

**R source** — [`R/123.ConfidenceIntervals_CC_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/123.ConfidenceIntervals_CC_n_x.R), function `ciCSCx`

**What the R code does** — Continuity-corrected Wilson interval for the given
`x`.

**Python source** — `binomcikit.ci.cc_n_x.cicscx` — one-row result.

**What the Python code does** — Single continuity-corrected Wilson interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `cicasx`

```{eval-rst}
.. autofunction:: binomcikit.ci.cc_n_x.cicasx
```

**In plain words** — Continuity-corrected **ArcSine** interval for a single `x`.

**The maths** — ArcSine interval with the correction on the transformed scale.

**Example**

```python
import binomcikit as bk
bk.cicasx(2, 20, 0.05, 1/40)
```

**R source** — [`R/123.ConfidenceIntervals_CC_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/123.ConfidenceIntervals_CC_n_x.R), function `ciCASx`

**What the R code does** — Continuity-corrected ArcSine interval for the given
`x`.

**Python source** — `binomcikit.ci.cc_n_x.cicasx` — one-row result.

**What the Python code does** — Single continuity-corrected ArcSine interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `cictwx`

```{eval-rst}
.. autofunction:: binomcikit.ci.cc_n_x.cictwx
```

**In plain words** — Continuity-corrected **Wald-T** interval for a single `x`.

**The maths** — `p̂ ± (t·SE* + c)`.

**Example**

```python
import binomcikit as bk
bk.cictwx(2, 20, 0.05, 1/40)
```

**R source** — [`R/123.ConfidenceIntervals_CC_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/123.ConfidenceIntervals_CC_n_x.R), function `ciCTWx`

**What the R code does** — Continuity-corrected Wald-T interval for the given
`x`.

**Python source** — `binomcikit.ci.cc_n_x.cictwx` — one-row result.

**What the Python code does** — Single continuity-corrected Wald-T interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`; `stats::qt` →
`scipy.stats.t.ppf`. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `cicltx`

```{eval-rst}
.. autofunction:: binomcikit.ci.cc_n_x.cicltx
```

**In plain words** — Continuity-corrected **Logit-Wald** interval for a single
`x`.

**The maths** — Logit-scale Wald interval with the correction, back-transformed.

**Example**

```python
import binomcikit as bk
bk.cicltx(2, 20, 0.05, 1/40)
```

**R source** — [`R/123.ConfidenceIntervals_CC_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/123.ConfidenceIntervals_CC_n_x.R), function `ciCLTx`

**What the R code does** — Continuity-corrected Logit-Wald interval for the given
`x`.

**Python source** — `binomcikit.ci.cc_n_x.cicltx` — one-row result.

**What the Python code does** — Single continuity-corrected Logit-Wald interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `cicallx`

```{eval-rst}
.. autofunction:: binomcikit.ci.cc_n_x.cicallx
```

**In plain words** — Runs **all five continuity-corrected methods** for a single
`x` and stacks them into one long-format table — the given-`x`, CC analogue of
{py:func}`ciall <binomcikit.ci.base_n.ciall>` (no Likelihood-Ratio).

**The maths** — None of its own; calls the five CC given-`x` methods above.

**Example**

```python
import binomcikit as bk
df = bk.cicallx(2, 20, 0.05, 1/40)
set(df["method"])
# {'Wald','ArcSine','Score','Wald-T','Logit-Wald'}
```

**R source** — [`R/123.ConfidenceIntervals_CC_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/123.ConfidenceIntervals_CC_n_x.R), function `ciCAllx`

**What the R code does** — Calls the five CC given-`x` methods, tags each with a
`method` factor, and `rbind`s them.

**Python source** — `binomcikit.ci.cc_n_x.cicallx` — same, via `pandas.concat`.

**What the Python code does** — Five-row long-format table for the single `x`.

**R → Py changes** — Naming lowercased; `rbind` → `pandas.concat`; pandas
`DataFrame`. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`
