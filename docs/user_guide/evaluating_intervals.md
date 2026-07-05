# Evaluating an interval

An interval method is only as good as its long-run behaviour. `binomcikit`
scores every method against **four criteria**. Each is its own family of
functions, and each reuses the interval limits from the `ci` family — so you can
evaluate any method the same way.

All four families accept the same method codes (`wd`, `sc`, …) and the same
base / adjusted (`a`) / continuity-corrected (`c`) variants.

## 1. Coverage probability — `covp*`

**Does the interval actually contain `p` at the nominal rate?** For each
hypothetical `p` drawn from a `Beta(a, b)` prior, coverage is the binomial mass
of the `x` whose interval contains that `p`. The function summarises this over
5000 draws.

```python
import binomcikit as bk
bk.covpwd(n=20, alp=0.05, a=1, b=1, t1=0.9, t2=0.97, seed=0)
```

Returned columns: `mcp` (mean coverage), `micp` (minimum coverage), three RMSE
measures, and `tol` (the % of `p` whose coverage falls in the tolerance band
`(t1, t2)`). A good method keeps `mcp` close to `1 − α` and `micp` from dropping
too low.

```{note}
These functions simulate, so pass `seed=` for reproducible results. Because
NumPy's RNG differs from R's, results match the R package *in distribution*, not
draw-for-draw.
```

## 2. Expected length — `length*` / `expl*`

**How wide is the interval, on average?** Coverage is easy to inflate by making
intervals huge, so width is the counterweight. `length*` returns a summary
(`sumLen`, `explMean`, `explSD`, `explMax`, and a ±SD band); `expl*` returns the
raw per-`p` curve for plotting.

```python
bk.lengthsc(n=20, alp=0.05, a=1, b=1, seed=0)
```

The art is picking a method with good coverage **and** small expected length.

## 3. p-confidence and p-bias — `pcopbi*`

**How honest is the confidence level, point by point?** For each interior `x`,
two binomial tail probabilities measure how well the interval's *actual*
confidence matches the nominal level (**p-confidence**) and how lop-sided it is
(**p-bias**). Unlike the first two, this is *deterministic* — no simulation, so
it matches the R package exactly.

```python
bk.pcopbiwd(n=20, alp=0.05)
#    x1   pconf   pbias
```

## 4. Error and failure — `err*`

**For a specific null hypothesis `phi`, how much does the true error exceed the
nominal `α`?** Given a threshold `f`, the function reports the increase in
nominal error (`delalp`), the long-term power (`theta`), and a pass/fail verdict.

```python
bk.errwd(n=20, alp=0.05, phi=0.05, f=-2)
#    delalp  theta Fail_Pass
```

## Putting it together

A typical workflow: compute intervals for a few candidate methods, then compare
their coverage and expected length for your `n`:

```python
import binomcikit as bk
common = dict(n=30, alp=0.05, a=1, b=1, t1=0.9, t2=0.97, seed=0)
for name, covp, length in [
    ("Wald",   bk.covpwd, bk.lengthwd),
    ("Wilson", bk.covpsc, bk.lengthsc),
]:
    c = covp(**common)["mcp"][0]
    w = length(n=30, alp=0.05, a=1, b=1, seed=0)["explMean"][0]
    print(f"{name:7s}  mean coverage={c:.3f}  mean length={w:.3f}")
```

Every criterion also has plotting functions (`plotcovp*`, `plotexpl*`,
`plotpcopbi*`, `ploterr*`) — see the {doc}`gallery <../gallery>`.
