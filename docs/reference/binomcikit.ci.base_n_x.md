# `ci.base_n_x`

```{eval-rst}
.. module:: binomcikit.ci.base_n_x
```

The **given-*x*** counterparts of the base confidence-interval methods in
{doc}`ci.base_n <binomcikit.ci.base_n>`. Where `ci.base_n` returns a whole table
(one row for every `x = 0…n`), these functions take a **single observed number
of successes `x`** and return **one row** — the interval you actually report
once you have data.

The maths of each method is identical to its `ci.base_n` sibling; only the input
and the output size differ. Column names carry an `x` suffix (`LWDx`/`UWDx`,
`LSCx`/`USCx`, …) to signal the single-`x` form.

```{contents} Functions in this module
:local:
:depth: 1
```

---

## `ciwdx`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n_x.ciwdx
```

**In plain words** — The **Wald** interval for a single `x` of `n`. Same
"estimate ± margin" as {py:func}`ciwd <binomcikit.ci.base_n.ciwd>`, reported for
just the value you observed.

**The maths** — With `p̂ = x/n` and `z = Φ⁻¹(1 − α/2)`:
$\hat{p} \pm z\sqrt{\hat{p}\hat{q}/n}$, clamped to `[0, 1]`.

**Example**

```python
import binomcikit as bk
bk.ciwdx(2, 10, 0.05)
#    x  LWDx      UWDx LABB UABB ZWI
# 0  2   0.0  0.447918  YES   NO  NO
```

**R source** — [`R/103.ConfidenceIntervals_BASE_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/103.ConfidenceIntervals_BASE_n_x.R), function `ciWDx`

**What the R code does** — Computes the single Wald interval for the given `x`,
clamps it into `[0, 1]`, and returns a one-row `data.frame`.

**Python source** — `binomcikit.ci.base_n_x.ciwdx`

```python
def ciwdx(x=None, n=None, alp=None):
    cv = stats.norm.ppf(1 - (alp / 2))
    pW = x / n; qW = 1 - x / n
    seW = (pW * qW / n) ** 0.5
    LWDx = max(pW - cv * seW, 0)
    UWDx = min(pW + cv * seW, 1)
    return pd.DataFrame({'x': [x], 'LWDx': [LWDx], 'UWDx': [UWDx], ...})
```

**What the Python code does** — The same one-`x` computation, returning a
single-row pandas `DataFrame`.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ciscx`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n_x.ciscx
```

**In plain words** — The **Score** (Wilson) interval for a single `x`; see
{py:func}`cisc <binomcikit.ci.base_n.cisc>` for the method.

**The maths** — The Wilson formula evaluated at `p̂ = x/n` (see `cisc`).

**Example**

```python
import binomcikit as bk
bk.ciscx(2, 10, 0.05)     # one-row Wilson interval for x = 2 of 10
```

**R source** — [`R/103.ConfidenceIntervals_BASE_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/103.ConfidenceIntervals_BASE_n_x.R), function `ciSCx`

**What the R code does** — Evaluates the Wilson interval for the single `x`.

**Python source** — `binomcikit.ci.base_n_x.ciscx` — the Wilson formula for one
`x`, returning columns `LSCx`/`USCx`.

**What the Python code does** — One-row Wilson interval; matches `cisc` at that
`x`.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ciasx`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n_x.ciasx
```

**In plain words** — The **ArcSine** interval for a single `x`; see
{py:func}`cias <binomcikit.ci.base_n.cias>`.

**The maths** — $\sin^2(\arcsin\sqrt{\hat{p}} \pm z/(2\sqrt{n}))$ at `p̂ = x/n`.

**Example**

```python
import binomcikit as bk
bk.ciasx(2, 10, 0.05)
```

**R source** — [`R/103.ConfidenceIntervals_BASE_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/103.ConfidenceIntervals_BASE_n_x.R), function `ciASx`

**What the R code does** — ArcSine transform, interval, back-transform for the
single `x`.

**Python source** — `binomcikit.ci.base_n_x.ciasx` — columns `LASx`/`UASx`.

**What the Python code does** — One-row ArcSine interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `cilrx`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n_x.cilrx
```

**In plain words** — The **Likelihood-Ratio** interval for a single `x`; see
{py:func}`cilr <binomcikit.ci.base_n.cilr>`.

**The maths** — The endpoints of `{ p : 2[ℓ(p̂) − ℓ(p)] ≤ z²_{α/2} }`, solved
numerically for the one `x`.

**Example**

```python
import binomcikit as bk
bk.cilrx(2, 10, 0.05)
```

**R source** — [`R/103.ConfidenceIntervals_BASE_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/103.ConfidenceIntervals_BASE_n_x.R), function `ciLRx`

**What the R code does** — Profiles the log-likelihood and solves for the two
endpoints at the given `x`.

**Python source** — `binomcikit.ci.base_n_x.cilrx` — `scipy.optimize` solve,
columns `LLRx`/`ULRx`.

**What the Python code does** — One-row LR interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`; numerical solve via
SciPy. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ciltx`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n_x.ciltx
```

**In plain words** — The **Logit-Wald** interval for a single `x`; see
{py:func}`cilt <binomcikit.ci.base_n.cilt>`.

**The maths** — Wald interval on the logit scale, back-transformed, at
`p̂ = x/n`.

**Example**

```python
import binomcikit as bk
bk.ciltx(2, 10, 0.05)
```

**R source** — [`R/103.ConfidenceIntervals_BASE_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/103.ConfidenceIntervals_BASE_n_x.R), function `ciLTx`

**What the R code does** — Logit transform, Wald interval, inverse-logit for the
single `x`.

**Python source** — `binomcikit.ci.base_n_x.ciltx` — columns `LLTx`/`ULTx`.

**What the Python code does** — One-row Logit-Wald interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. Numerically
identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `citwx`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n_x.citwx
```

**In plain words** — The **Wald-T** interval for a single `x`; see
{py:func}`citw <binomcikit.ci.base_n.citw>`.

**The maths** — `p̂ ± t·SE*` at `p̂ = x/n`.

**Example**

```python
import binomcikit as bk
bk.citwx(2, 10, 0.05)
```

**R source** — [`R/103.ConfidenceIntervals_BASE_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/103.ConfidenceIntervals_BASE_n_x.R), function `ciTWx`

**What the R code does** — Adjusted point estimate / SE and a *t* quantile for
the single `x`.

**Python source** — `binomcikit.ci.base_n_x.citwx` — `scipy.stats.t`, columns
`LTWx`/`UTWx`.

**What the Python code does** — One-row Wald-T interval.

**R → Py changes** — Naming lowercased; pandas `DataFrame`; `stats::qt` →
`scipy.stats.t.ppf`. Numerically identical.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ciexx`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n_x.ciexx
```

**In plain words** — The **Exact** (Clopper–Pearson / mid-*p*) interval for a
single `x`, across one or more tail-tuning values `e`; see
{py:func}`ciex <binomcikit.ci.base_n.ciex>`.

**The maths** — Solves the binomial-tail equations `e·P(X=x) + P(X>x) = α/2`
(and its mirror) for the one `x`; `e = 1` → Clopper–Pearson, `e = 0.5` → mid-*p*.

**Example**

```python
import binomcikit as bk
bk.ciexx(2, 10, 0.05, [0.1, 0.5, 1.0])   # three e-values, one row each
```

**R source** — [`R/103.ConfidenceIntervals_BASE_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/103.ConfidenceIntervals_BASE_n_x.R), function `ciEXx` (helpers `lufn103`, `exlim103l`, `exlim103u`)

**What the R code does** — For each `e`, solves the tail equations for the given
`x`.

**Python source** — `binomcikit.ci.base_n_x.ciexx`

```python
def ciexx(x, n, alp, e):
    for ei in e:
        lu = lufn103(x, n, alp, ei)      # LEXx = exlim103l(...), UEXx = exlim103u(...)
        res = pd.concat([res, lu], ignore_index=True)
    return res
```

**What the Python code does** — Loops over the `e` values, solving each endpoint
with `scipy.optimize.brentq`, returning one row per `e` (columns `LEXx`/`UEXx`).

**R → Py changes** — Naming lowercased; pandas `DataFrame`. **Fix:** the earlier
port called `scipy.stats.root_scalar` (which does not exist); this port uses
`scipy.optimize.brentq`, so `ciexx`/`ciex` actually run.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## `ciallx`

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n_x.ciallx
```

**In plain words** — Runs **all six base methods** for a single `x` and stacks
them into one long-format table with a `method` column — the given-`x` analogue
of {py:func}`ciall <binomcikit.ci.base_n.ciall>`.

**The maths** — None of its own; calls the six given-`x` methods above.

**Example**

```python
import binomcikit as bk
bk.ciallx(2, 10, 0.05)
#        method  x  LowerLimit  UpperLimit LowerAbb UpperAbb ZWI
# 1        Wald  2    0.000000    0.447918      YES       NO  NO
# 2     ArcSine  2    0.023453    0.488148       NO       NO  NO
# ...
```

**R source** — [`R/103.ConfidenceIntervals_BASE_n_x.R`](https://github.com/RajeswaranV/proportion/blob/master/R/103.ConfidenceIntervals_BASE_n_x.R), function `ciAllx`

**What the R code does** — Calls the six given-`x` methods, tags each with a
`method` factor, and `rbind`s them.

**Python source** — `binomcikit.ci.base_n_x.ciallx` — same, via `pandas.concat`.

**What the Python code does** — Produces the six-row long-format table for the
single `x`.

**R → Py changes** — Naming lowercased; pandas `DataFrame`. **Newly added** —
`ciallx` was missing from the earlier partial port and was reconstructed from
the R source.

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`

---

## Internal helpers

Exact-method root-finding helpers used by `ciexx`, mirroring the R helpers of
the same name. Documented here only so the mapping table links resolve.

```{eval-rst}
.. autofunction:: binomcikit.ci.base_n_x.lufn103
.. autofunction:: binomcikit.ci.base_n_x.exlim103l
.. autofunction:: binomcikit.ci.base_n_x.exlim103u
```

{doc}`← Back to the R → Python mapping table </r_to_python_mapping>`
