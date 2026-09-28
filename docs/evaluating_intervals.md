---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Evaluating an interval

An interval method is only as good as its long-run behaviour. Two methods can hand you the *same*
`[0.05, 0.36]` for one dataset and behave completely differently across all the datasets you *didn't*
see. This page is about that difference — the four lenses `binomcikit` gives you to judge a method,
each explained from first principles and each reproducible from `scipy` so you can see there's no
magic.

*New here?* {doc}`foundations/05_coverage` introduces coverage with no maths; this page assumes you've
met the idea. *Just want to pick a method?* Jump to {doc}`method_selection` or use `recommend` (bottom
of this page).

Every code block below is **executed at build time**, so the numbers are the real package's.

---

## The four questions

| # | Question | Family | Simulated? |
|---|---|---|---|
| 1 | Does the interval actually contain {term}`theta` at the promised rate? | `covp*` | yes (seed it) |
| 2 | How **wide** is it, on average? | `length*` / `expl*` | yes (seed it) |
| 3 | How **honest** is the confidence, count by count? | `pcopbi*` | no — exact |
| 4 | For a specific hypothesis, how much does the real error exceed α? | `err*` | no — exact |

Questions 1–2 average over a `Beta(a, b)` prior of θ values and so **simulate** (pass `seed=` for
reproducibility). Questions 3–4 are pure binomial sums — **deterministic**, and they match the R
`proportion` package to floating point.

---

## 1. Coverage — does it trap θ?

**In words.** Fix a true rate θ. Generate many samples of size `n`, build the interval for each, and
count the fraction that actually contain θ. That fraction is the **{term}`coverage`**. A 95% method
should land near 0.95 *for every* θ — not just on average.

You can watch it happen. Here we simulate 20 000 experiments at θ = 0.1, `n` = 20, and check how often
each interval traps the truth:

```{code-cell} python
import numpy as np
import binomcikit as bk

rng = np.random.default_rng(0)
theta, n = 0.10, 20
xs = rng.binomial(n, theta, size=20_000)          # 20 000 observed counts

def sim_coverage(method, lo_col, up_col):
    tbl = bk.ci(n=n, method=method)
    lo, up = tbl[lo_col].to_numpy(), tbl[up_col].to_numpy()
    return ((lo[xs] <= theta) & (theta <= up[xs])).mean()

print("Wald   coverage at theta=0.1:", round(sim_coverage("wald",   "LWD", "UWD"), 3))
print("Wilson coverage at theta=0.1:", round(sim_coverage("wilson", "LSC", "USC"), 3))
```

Wald lands well under 0.95; Wilson lands on it. `binomcikit` does this for you across the whole range
of θ and summarises it — the `covp*` family:

```{code-cell} python
bk.covpwd(n=20, alp=0.05, a=1, b=1, t1=0.9, t2=0.97, seed=0)[["mcp", "micp"]]
```

- **`mcp`** — mean coverage (averaged over the prior). Should sit near 1 − α.
- **`micp`** — minimum coverage (the worst θ). This is the number that matters for a guarantee, and
  it is where Wald collapses.

The left panel of the figure below shows why summary numbers hide the truth: coverage is a jagged
{term}`discreteness` curve, not a flat line.

## 2. Expected length — how wide?

Coverage alone is a trap: you can hit 100% coverage by returning `[0, 1]` every time. Width is the
counterweight. The **{term}`expected length`** is the average interval width, again averaged over θ.

```{code-cell} python
bk.lengthsc(n=20, alp=0.05, a=1, b=1, seed=0)[["explMean", "explSD", "explMax"]]
```

`explMean` is the average width; `expl*` (e.g. `explsc`) returns the raw per-θ curve for plotting. The
whole game is **good coverage at small length** — the two must be read together:

```{figure} _static/evaluating_tradeoff.png
:alt: Coverage and expected length versus theta for Wald, Wilson and Blaker at n=20
:width: 100%

**Read the two panels together.** Left: true coverage vs θ (`n` = 20). Wald (orange) sinks far below
the nominal 0.95 line, especially near the boundaries; Wilson (blue) tracks it; the exact
{term}`Clopper–Pearson`-style Blaker (green) never drops below 0.95. Right: the price — Blaker's
guaranteed coverage buys slightly *wider* intervals than Wilson almost everywhere. That trade-off,
coverage against length, is the whole decision.
```

## 3. p-confidence & p-bias — honesty, count by count

The first two lenses average over θ. These next two look at the interval **at each observed count `x`**
and ask a sharper, θ-free question. They come from Vos & Hudson's analysis and the R `proportion`
package, and they are *deterministic*.

**In words.** For the interval `[L, U]` returned at count `x`:

- Sitting at the lower limit `L`, how likely is a result *at least as high* as `x`? Double it (two
  tails). Call it the **lower-limit tail**.
- Sitting at the upper limit `U`, how likely is a result *at least as low* as `x`? Double it. Call it
  the **upper-limit tail**.

**p-confidence** is `1 −` the *larger* of those two tails — the realised confidence the interval
actually delivers at `x` (higher is better; aim for ≥ 1 − α). **p-bias** is the *gap* between the two
tails — how lopsided the interval is (lower is better; 0 means the two sides carry equal error).

**The definition.** For interior `x` (1 ≤ x ≤ n−1), with $p_L$ the lower-limit tail and $p_U$ the
upper-limit tail,

$$\text{p-confidence}(x) = 1 - \max(p_L, p_U), \qquad \text{p-bias}(x) = \bigl|\,p_L - p_U\,\bigr|.$$

Nothing is hidden — here is the whole computation from `scipy`, and it reproduces `pcopbiwd` exactly:

```{code-cell} python
import scipy.stats as st

n = 5
wald = bk.ci(n=n, method="wald")
L, U = wald["LWD"].to_numpy(), wald["UWD"].to_numpy()

for x in range(1, n):                                   # interior counts only
    p_L = 2 * (st.binom.sf(x, n, L[x]) + st.binom.pmf(x, n, L[x]))   # doubled tail at L
    p_U = 2 * st.binom.cdf(x, n, U[x])                              # doubled tail at U
    hi, lo = max(p_L, p_U), min(p_L, p_U)
    print(f"x={x}  p-confidence={(1-hi)*100:6.2f}%   p-bias={(hi-lo)*100:6.2f}%")
```

```{code-cell} python
bk.pcopbiwd(n=5, alp=0.05)      # identical to the hand computation above
```

**Reading it.** Now compare Wald with Wilson at `n` = 20. Watch the `pbias` column especially:

```{code-cell} python
summary = {
    "Wald":   bk.pcopbiwd(n=20, alp=0.05),
    "Wilson": bk.pcopbisc(n=20, alp=0.05),
}
import pandas as pd
pd.DataFrame({
    name: {"min p-confidence": d["pconf"].min().round(2),
           "max p-bias":       d["pbias"].max().round(2)}
    for name, d in summary.items()
}).T
```

Both methods' p-confidence dips at the extreme interior counts — that is {term}`discreteness`, not a
bug. But **Wald's p-bias climbs much higher than Wilson's**: Wald's error piles onto one side, while
Wilson stays more balanced. That asymmetry is a big part of what "Wald misbehaves near the boundary"
means in practice.

## 4. Error & long-term power — a specific hypothesis

The last lens fixes a {term}`null hypothesis` value `phi` (say θ = 0.2) and asks: *if that were the
truth, how often would the interval wrongly exclude it, versus the α we promised?*

**In words.** For each count `x`, the interval either contains `phi` or not. Add up the binomial
probability of the counts that *exclude* it — that's the interval's real error rate at `phi`. Compare
it to the nominal α.

**The definition.**

$$\text{delalp} = 100\,\bigl(\alpha - \!\!\sum_{x:\,\phi \notin [L_x, U_x]}\!\! \Pr(x \mid \phi)\bigr),
\qquad \text{theta} = 100 \cdot \frac{\#\{x : \phi \notin [L_x, U_x]\}}{n+1}.$$

- **`delalp`** — nominal minus actual error, in points. **Positive is safe** (the method is
  conservative); **negative means it exceeds α** (anti-conservative — the dangerous direction).
- **`theta`** — the share of the sample space that rejects `phi`: a discrete stand-in for long-run
  power.
- **`Fail_Pass`** — `"failure"` when `delalp` drops below your tolerance `f`.

Again, the whole thing from `scipy`, reproducing `errwd`:

```{code-cell} python
n, phi, alp = 20, 0.2, 0.05
w = bk.ci(n=n, method="wald")
L, U = w["LWD"].to_numpy(), w["UWD"].to_numpy()
x = np.arange(n + 1)

outside = (phi > U) | (phi < L)
actual_error = st.binom.pmf(x, n, phi)[outside].sum()
print("delalp =", round((alp - actual_error) * 100, 2), " theta =", round(100 * outside.sum() / (n + 1), 2))
```

```{code-cell} python
bk.errwd(n=20, alp=0.05, phi=0.2, f=-2)     # same numbers, plus the pass/fail verdict
```

`delalp` is **−2.92** here: at φ = 0.2 the Wald interval's true error is almost 3 points *above* the
5% it promised, so against a tolerance of `f = -2` it is flagged a **failure**. That is the coverage
shortfall of §1, localised to one hypothesis.

---

## Putting it together

The point of all four lenses is to *choose*. `recommend` runs coverage and length across every method
for your `n` and ranks them — here, by expected length among methods with adequate coverage:

```{code-cell} python
bk.recommend(n=30, by="length").head(5)
```

Or drive the families directly to build your own scorecard:

```{code-cell} python
common = dict(n=30, alp=0.05, a=1, b=1, seed=0)
for name, covp, length in [("Wald", bk.covpwd, bk.lengthwd), ("Wilson", bk.covpsc, bk.lengthsc)]:
    c = covp(t1=0.9, t2=0.97, **common)["mcp"][0]
    w = length(**common)["explMean"][0]
    print(f"{name:7s} mean coverage={c:.3f}  mean length={w:.3f}")
```

Every criterion also has plotting functions (`plotcovp*`, `plotexpl*`, `plotpcopbi*`, `ploterr*`) —
see the {doc}`gallery <gallery>`.

---

## Check yourself

**Q1.** A method reports mean coverage `mcp = 0.995` at `n` = 20. Is that good?

:::{dropdown} Show answer
Not necessarily — it is *over*-covering. Mean coverage well above 0.95 means the intervals are wider
than they need to be (conservative), like {term}`Clopper–Pearson`. The target is *close to* 0.95, read
together with {term}`expected length`. The number to fear is a low **`micp`** (minimum coverage), not a
high mean.
:::

**Q2.** In the p-bias definition, what does a value of 0 mean, and why do you want it small?

:::{dropdown} Show answer
`p-bias = |p_L − p_U|` is the gap between the two doubled tail probabilities. **0** means the interval
splits its error exactly evenly between the low and high sides — a perfectly balanced two-sided
interval. A large p-bias means one tail carries most of the error, so the interval systematically
misses on one side. Wald's p-bias grows near the boundary; Wilson's stays smaller (see the table
above).
:::

**Q3.** `errwd(n=20, alp=0.05, phi=0.2, f=-2)` returns `delalp = -2.92`. In one sentence, why is the
sign the whole story? Check it against the code.

:::{dropdown} Show answer
`delalp = nominal − actual` error, so a **negative** value means the *actual* error at φ = 0.2 exceeds
the promised 5% — the interval is anti-conservative exactly where it should be careful. A positive
`delalp` would be safe (conservative). Reproduce with:
```python
import binomcikit as bk
bk.errwd(n=20, alp=0.05, phi=0.2, f=-2)   # delalp -2.92, theta 66.67, "failure"
```
:::

---

:::{admonition} Terms used on this page
:class: seealso
{term}`theta` · {term}`coverage` · {term}`expected length` · {term}`discreteness` ·
{term}`null hypothesis` · {term}`Clopper–Pearson` · {term}`alpha`
:::
