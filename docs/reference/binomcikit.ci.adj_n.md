# `ci.adj_n`

```{eval-rst}
.. module:: binomcikit.ci.adj_n
```

The **adjusted** confidence-interval methods — the base methods of
{doc}`ci.base_n <binomcikit.ci.base_n>` applied after **adding pseudo-counts**.

The idea (the same one behind the Agresti–Coull interval): before computing an
interval, replace the raw count `x` with `x + h` and the sample size `n` with
`n + 2h`, so the working proportion is

$$\tilde{p} = \frac{x + h}{n + 2h}.$$

Pushing the estimate away from 0 and 1 fixes the degenerate behaviour of the
raw methods at the extremes and improves small-sample coverage. A common choice
is `h = 2` (with `z ≈ 2`, that is the Agresti–Coull "add two successes and two
failures" rule). All functions here take the extra argument **`h ≥ 0`** and
return the usual `LABB`/`UABB`/`ZWI` flags; column names carry an `A`
(`LAWD`/`UAWD`, `LASC`/`USC`, …).

```{contents} Functions in this module
:local:
:depth: 1
```

---

## `ciawd`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n.ciawd
```

**In plain words** — The **adjusted Wald** interval: Wald applied to the
pseudo-count estimate `p̃`. Far better behaved than plain
{py:func}`ciwd <binomcikit.ci.base_n.ciwd>` near 0 and 1.

**The maths** — With `p̃ = (x+h)/(n+2h)`, `ñ = n+2h`:
$\tilde{p} \pm z\sqrt{\tilde{p}(1-\tilde{p})/\tilde{n}}$, clamped to `[0, 1]`.

**Example**

```python
import binomcikit as bk
bk.ciawd(5, 0.05, 2)      # adjusted Wald, h = 2 (Agresti-Coull-style)
```

**R source** — [`R/111.ConfidenceIntervals_ADJ_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/111.ConfidenceIntervals_ADJ_n.R), function `ciAWD`

**What the R code does** — Forms `y = x + h`, `n1 = n + 2h`, then runs the Wald
computation on `(y, n1)` for every `x`.

**Python source** — `binomcikit.ci.adj_n.ciawd`

```python
def ciawd(n, alp, h):
    y = x + h; n1 = n + 2 * h
    pAW = y / n1
    seAW = np.sqrt(pAW * (1 - pAW) / n1)
    LAWD = pAW - cv * seAW
    UAWD = pAW + cv * seAW
    # ... clamp + flags ...
```

**What the Python code does** — The same pseudo-count Wald computation, columns
`LAWD`/`UAWD`.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ciasc`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n.ciasc
```

**In plain words** — The **adjusted Score** (Wilson) interval; the Wilson method
of {py:func}`cisc <binomcikit.ci.base_n.cisc>` applied to the pseudo-count data.

**The maths** — The Wilson formula evaluated with `x+h`, `n+2h`.

**Example**

```python
import binomcikit as bk
bk.ciasc(5, 0.05, 2)
```

**R source** — [`R/111.ConfidenceIntervals_ADJ_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/111.ConfidenceIntervals_ADJ_n.R), function `ciASC`

**What the R code does** — Runs the Wilson computation on the pseudo-count data.

**Python source** — `binomcikit.ci.adj_n.ciasc` — columns `LASC`/`USC`.

**What the Python code does** — Adjusted Wilson interval for every `x`.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ciaas`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n.ciaas
```

**In plain words** — The **adjusted ArcSine** interval; see
{py:func}`cias <binomcikit.ci.base_n.cias>`.

**The maths** — $\sin^2(\arcsin\sqrt{\tilde{p}} \pm z/(2\sqrt{\tilde{n}}))$.

**Example**

```python
import binomcikit as bk
bk.ciaas(5, 0.05, 2)
```

**R source** — [`R/111.ConfidenceIntervals_ADJ_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/111.ConfidenceIntervals_ADJ_n.R), function `ciAAS`

**What the R code does** — ArcSine transform on the pseudo-count estimate.

**Python source** — `binomcikit.ci.adj_n.ciaas` — columns `LAAS`/`UAAS`.

**What the Python code does** — Adjusted ArcSine interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ciatw`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n.ciatw
```

**In plain words** — The **adjusted Wald-T** interval; see
{py:func}`citw <binomcikit.ci.base_n.citw>`.

**The maths** — `p̃ ± t·SE*` on the pseudo-count data.

**Example**

```python
import binomcikit as bk
bk.ciatw(5, 0.05, 2)
```

**R source** — [`R/111.ConfidenceIntervals_ADJ_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/111.ConfidenceIntervals_ADJ_n.R), function `ciATW`

**What the R code does** — Wald-T computation on `(x+h, n+2h)`.

**Python source** — `binomcikit.ci.adj_n.ciatw` — columns `LATW`/`UATW`.

**What the Python code does** — Adjusted Wald-T interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`; `stats::qt` →
`scipy.stats.t.ppf`. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `cialt`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n.cialt
```

**In plain words** — The **adjusted Logit-Wald** interval; see
{py:func}`cilt <binomcikit.ci.base_n.cilt>`.

**The maths** — Logit-scale Wald interval built from the pseudo-count estimate,
back-transformed.

**Example**

```python
import binomcikit as bk
bk.cialt(5, 0.05, 2)
```

**R source** — [`R/111.ConfidenceIntervals_ADJ_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/111.ConfidenceIntervals_ADJ_n.R), function `ciALT`

**What the R code does** — Logit transform of `p̃`, Wald interval, inverse-logit.

**Python source** — `binomcikit.ci.adj_n.cialt` — columns `LALT`/`UALT`.

**What the Python code does** — Adjusted Logit-Wald interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `cialr`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n.cialr
```

**In plain words** — The **adjusted Likelihood-Ratio** interval; see
{py:func}`cilr <binomcikit.ci.base_n.cilr>`.

**The maths** — The LR interval computed from the pseudo-count log-likelihood,
solved numerically.

**Example**

```python
import binomcikit as bk
bk.cialr(5, 0.05, 2)
```

**R source** — [`R/111.ConfidenceIntervals_ADJ_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/111.ConfidenceIntervals_ADJ_n.R), function `ciALR`

**What the R code does** — Profiles the pseudo-count log-likelihood and solves
for the endpoints.

**Python source** — `binomcikit.ci.adj_n.cialr` — `scipy.optimize`, columns
`LALR`/`UALR`.

**What the Python code does** — Adjusted LR interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`; numerical solve via
SciPy. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ciaall`

```{eval-rst}
.. autofunction:: binomcikit.ci.adj_n.ciaall
```

**In plain words** — Runs **all six adjusted methods** and stacks them into one
long-format table — the adjusted analogue of
{py:func}`ciall <binomcikit.ci.base_n.ciall>`.

**The maths** — None of its own; calls the six adjusted methods above.

**Example**

```python
import binomcikit as bk
df = bk.ciaall(5, 0.05, 2)
set(df["method"])
# {'Wald','ArcSine','Likelihood','Score','Wald-T','Logit-Wald'}
```

**R source** — [`R/111.ConfidenceIntervals_ADJ_n.R`](https://github.com/RajeswaranV/proportion/blob/master/R/111.ConfidenceIntervals_ADJ_n.R), function `ciAAll`

**What the R code does** — Calls the six adjusted methods, tags each with a
`method` factor, and `rbind`s them.

**Python source** — `binomcikit.ci.adj_n.ciaall` — same, via `pandas.concat`.

**What the Python code does** — Long-format table of all six adjusted methods.

**R → Py changes** — Naming lowercased; `rbind` → `pandas.concat`; pandas
`DataFrame`. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`
