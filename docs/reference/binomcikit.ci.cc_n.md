# `ci.cc_n`

```{eval-rst}
.. module:: binomcikit.ci.cc_n
```

The **continuity-corrected** confidence-interval methods — the base methods of
{doc}`ci.base_n <binomcikit.ci.base_n>` with a small **continuity correction
`c`** added to widen the interval.

Because the binomial is discrete but the normal approximation is continuous, the
approximation slightly under-covers. A continuity correction nudges each limit
outward by `c` (lower limit down by `c`, upper limit up by `c`, roughly), which
restores coverage closer to the nominal level. The correction must satisfy
**`0 < c ≤ 1/(2n)`** (the classic choice is `c = 1/(2n)`).

There are **five** continuity-corrected methods — Wald, Score, ArcSine, Wald-T
and Logit-Wald. The Likelihood-Ratio method has no continuity-corrected form.
Column names carry a `C` (`LCW`/`UCW`, `LCS`/`UCS`, …).

```{contents} Functions in this module
:local:
:depth: 1
```

---

## `cicwd`

```{eval-rst}
.. autofunction:: binomcikit.ci.cc_n.cicwd
```

**In plain words** — The **continuity-corrected Wald** interval: plain
{py:func}`ciwd <binomcikit.ci.base_n.ciwd>` with the limits pushed out by `c`.

**The maths** — With `p̂ = x/n` and `SE = √(p̂q̂/n)`:

$$\hat{p} - (z\,\mathrm{SE} + c) \quad\text{and}\quad \hat{p} + (z\,\mathrm{SE} + c),$$

clamped to `[0, 1]`.

**Example**

```python
import binomcikit as bk
bk.cicwd(20, 0.05, 1/40)     # c = 1/(2n) = 1/40 for n = 20
```

**R source** — [`R/121.ConfidenceIntervals_CC_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/121.ConfidenceIntervals_CC_n.R), function `ciCWD`

**What the R code does** — Computes the Wald limits and then subtracts/adds the
continuity correction `c` before clamping.

**Python source** — `binomcikit.ci.cc_n.cicwd`

```python
def cicwd(n, alp, c):
    pCW = x / n; seCW = np.sqrt(pCW * (1 - pCW) / n)
    LCW = pCW - (cv * seCW + c)
    UCW = pCW + (cv * seCW + c)
    # ... clamp + flags ...
```

**What the Python code does** — The same corrected Wald computation, columns
`LCW`/`UCW`.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `cicsc`

```{eval-rst}
.. autofunction:: binomcikit.ci.cc_n.cicsc
```

**In plain words** — The **continuity-corrected Score** (Wilson) interval; see
{py:func}`cisc <binomcikit.ci.base_n.cisc>`.

**The maths** — The Wilson formula with the continuity correction `c` folded
into the numerator terms.

**Example**

```python
import binomcikit as bk
bk.cicsc(20, 0.05, 1/40)
```

**R source** — [`R/121.ConfidenceIntervals_CC_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/121.ConfidenceIntervals_CC_n.R), function `ciCSC`

**What the R code does** — Wilson interval with the continuity correction.

**Python source** — `binomcikit.ci.cc_n.cicsc` — columns `LCS`/`UCS`.

**What the Python code does** — Continuity-corrected Wilson interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `cicas`

```{eval-rst}
.. autofunction:: binomcikit.ci.cc_n.cicas
```

**In plain words** — The **continuity-corrected ArcSine** interval; see
{py:func}`cias <binomcikit.ci.base_n.cias>`.

**The maths** — The ArcSine interval with the correction applied on the
transformed scale.

**Example**

```python
import binomcikit as bk
bk.cicas(20, 0.05, 1/40)
```

**R source** — [`R/121.ConfidenceIntervals_CC_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/121.ConfidenceIntervals_CC_n.R), function `ciCAS`

**What the R code does** — ArcSine interval with the continuity correction.

**Python source** — `binomcikit.ci.cc_n.cicas` — columns `LCA`/`UCA`.

**What the Python code does** — Continuity-corrected ArcSine interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `cictw`

```{eval-rst}
.. autofunction:: binomcikit.ci.cc_n.cictw
```

**In plain words** — The **continuity-corrected Wald-T** interval; see
{py:func}`citw <binomcikit.ci.base_n.citw>`.

**The maths** — `p̂ ± (t·SE* + c)`.

**Example**

```python
import binomcikit as bk
bk.cictw(20, 0.05, 1/40)
```

**R source** — [`R/121.ConfidenceIntervals_CC_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/121.ConfidenceIntervals_CC_n.R), function `ciCTW`

**What the R code does** — Wald-T limits with the continuity correction.

**Python source** — `binomcikit.ci.cc_n.cictw` — columns `LCTW`/`UCTW`.

**What the Python code does** — Continuity-corrected Wald-T interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`; `stats::qt` →
`scipy.stats.t.ppf`. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ciclt`

```{eval-rst}
.. autofunction:: binomcikit.ci.cc_n.ciclt
```

**In plain words** — The **continuity-corrected Logit-Wald** interval; see
{py:func}`cilt <binomcikit.ci.base_n.cilt>`.

**The maths** — Logit-scale Wald interval with the continuity correction,
back-transformed.

**Example**

```python
import binomcikit as bk
bk.ciclt(20, 0.05, 1/40)
```

**R source** — [`R/121.ConfidenceIntervals_CC_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/121.ConfidenceIntervals_CC_n.R), function `ciCLT`

**What the R code does** — Logit-Wald interval with the continuity correction.

**Python source** — `binomcikit.ci.cc_n.ciclt` — columns `LCLT`/`UCLT`.

**What the Python code does** — Continuity-corrected Logit-Wald interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `cicall`

```{eval-rst}
.. autofunction:: binomcikit.ci.cc_n.cicall
```

**In plain words** — Runs **all five continuity-corrected methods** and stacks
them into one long-format table — the CC analogue of
{py:func}`ciall <binomcikit.ci.base_n.ciall>` (no Likelihood-Ratio).

**The maths** — None of its own; calls the five CC methods above.

**Example**

```python
import binomcikit as bk
df = bk.cicall(20, 0.05, 1/40)
set(df["method"])
# {'Wald','ArcSine','Score','Wald-T','Logit-Wald'}   (no 'Likelihood')
```

**R source** — [`R/121.ConfidenceIntervals_CC_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/121.ConfidenceIntervals_CC_n.R), function `ciCAll`

**What the R code does** — Calls the five CC methods, tags each with a `method`
factor, and `rbind`s them.

**Python source** — `binomcikit.ci.cc_n.cicall` — same, via `pandas.concat`.

**What the Python code does** — Long-format table of all five CC methods.

**R → Py changes** — Naming lowercased; `rbind` → `pandas.concat`; pandas
`DataFrame`. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`
