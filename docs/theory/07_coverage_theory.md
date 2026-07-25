---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Coverage theory — reading the oscillating curves

This is the last page of the series, and its job is to step back. Every method we have built — {doc}`Wald
<02_normal_approximation>`, {doc}`Wilson and LR <03_test_inversion>`, {doc}`the exact family
<04_exact_and_discreteness>`, {doc}`arcsine and logit <05_transformed_intervals>`, {doc}`the Bayesian
credible interval <06_bayesian_view>` — produced the same kind of jagged {term}`coverage` curve. This page
asks what those curves actually *mean*: how to summarise a method in a way that doesn't lie, why the
wiggles never fully disappear, why "95% coverage" hides a one-sided story, and how the two general repairs
— **adjustment** and **continuity correction** — reshape the curve. It ties the whole track together.

Every code block here is **executed when the docs are built**.

## Two numbers, two different questions

You cannot read a whole coverage curve at a glance, so we summarise it. The two summaries that matter
answer *different* questions, and a method can pass one while failing the other:

- **Mean coverage** — averaged over $\theta$: *on average, is the method honest?*
- **Minimum coverage** — the worst $\theta$: *in its worst case, how badly does it under-cover?*

```{code-cell} python
import binomcikit as bk
import pandas as pd

rows = {}
for m in ["wald", "wilson", "exact", "blaker"]:
    c = bk.coverage_curve(40, method=m, points=600)["coverage"]
    rows[m] = {"mean": round(float(c.mean()), 3), "min": round(float(c.min()), 3)}
pd.DataFrame(rows).T
```

Look at **Wald**: its mean coverage (~0.89) looks merely mediocre, but its *minimum* is near **0.004** —
at some $\theta$ it essentially never covers (the {term}`zero-width interval` collapse). The mean *hid*
the disaster. This is the single most important habit in evaluating an interval: **never trust mean
coverage alone** — always look at the minimum. Wilson, Blaker and the exact interval keep both summaries
respectable; Wald only survives the "mean" test.

## Oscillation, and why it never dies

The wiggles are not noise — they are {term}`discreteness` (from {doc}`page 4 <04_exact_and_discreteness>`).
Because the count is an integer, the coverage function is a step function, and stepping means oscillating.
You might hope that with enough data the oscillation smooths away and the minimum climbs to 0.95. It does —
but *painfully slowly*, and the minimum lags far behind the mean the whole way:

```{code-cell} python
rows = {}
for n in [20, 40, 80, 200, 500]:
    c = bk.coverage_curve(n, method="wilson", points=800)["coverage"]
    rows[n] = {"mean coverage": round(float(c.mean()), 3),
               "min coverage": round(float(c.min()), 3)}
pd.DataFrame(rows).T
```

Wilson's **mean** coverage sits on 0.95 at *every* sample size — it looks flawless. But its **minimum**
crawls: still only ~0.90 at $n=200$, and not until $n=500$ does the worst case reach ~0.94. This slow,
uneven approach is a famous result (Brown, Cai & DasGupta, 2001): binomial coverage does not converge to
nominal smoothly, and a larger $n$ is not always luckier than a smaller one. It is *why* the evaluation
tools in this package exist — you genuinely cannot eyeball whether a method is safe at your $n$.

## One-sided vs two-sided: coverage has two tails

"95% coverage" is a *two-sided* statement, but the 5% of misses splits into two very different piles: the
times the interval sits entirely **above** $\theta$ (its lower limit is too high) and the times it sits
entirely **below** (its upper limit is too low). Near the boundary these are wildly unequal. Split Wald's
non-coverage into its left and right pieces:

```{code-cell} python
from math import comb

def noncoverage_split(theta, n, grid, lcol, ucol):
    g = grid.set_index("x")
    left = right = 0.0                      # left: theta below L ; right: theta above U
    for x in range(n + 1):
        w = comb(n, x) * theta**x * (1 - theta) ** (n - x)
        if theta < g.loc[x, lcol]:
            left += w
        elif theta > g.loc[x, ucol]:
            right += w
    return {"miss low (θ<L)": round(left, 4), "miss high (θ>U)": round(right, 4)}

wald = bk.ciwd(40, 0.05)
print("theta = 0.05:", noncoverage_split(0.05, 40, wald, "LWD", "UWD"))
print("theta = 0.50:", noncoverage_split(0.50, 40, wald, "LWD", "UWD"))
```

At $\theta = 0.5$ the two tails are equal (~0.04 each) — a balanced 8% miss. But at $\theta = 0.05$,
almost *all* the ~13% non-coverage is on one side: the upper limit is repeatedly too low. A method can
look tolerable two-sided while being badly skewed one-sided, which matters enormously if your decision is
one-directional ("is the rate *below* the safety threshold?"). binomcikit's p-confidence / p-bias metrics
(see {doc}`../evaluating_intervals`) measure exactly this asymmetry.

## The two repairs: adjustment (h) and continuity (c)

Finally, the two general levers for rescuing a fragile approximate method — both applied here to Wald, both
computable from the exact coverage sum.

**Adjustment ($h$).** Add $h$ pseudo-successes and $h$ pseudo-failures before applying the formula: use
$y = x+h$ out of $n' = n+2h$. This nudges $\hat p$ away from the edges so the {term}`standard error` never
collapses. With $h=2$ it is essentially {term}`Agresti–Coull`.

**Continuity correction ($c$).** Widen the interval by a small amount $c$ to acknowledge that the discrete
count jumps past the smooth normal curve. It makes the interval *more conservative*.

```{code-cell} python
import numpy as np

def coverage(theta, n, grid, lcol, ucol):
    g = grid.set_index("x")
    return float(sum(comb(n, x) * theta**x * (1 - theta) ** (n - x)
                     for x in range(n + 1) if g.loc[x, lcol] <= theta <= g.loc[x, ucol]))

def summarise(n, grid, lcol, ucol, pts=500):
    ts = np.linspace(1e-4, 1 - 1e-4, pts)
    cs = [coverage(t, n, grid, lcol, ucol) for t in ts]
    return {"mean": round(float(np.mean(cs)), 3), "min": round(float(np.min(cs)), 3)}

pd.DataFrame({
    "Wald (raw)":            summarise(40, bk.ciwd(40, 0.05), "LWD", "UWD"),
    "+ adjustment (h=2)":    summarise(40, bk.ciawd(40, 0.05, 2), "LAWD", "UAWD"),
    "+ continuity (c=0.5)":  summarise(40, bk.cicwd(40, 0.05, 0.5), "LCW", "UCW"),
}).T
```

The contrast is the lesson. The **adjustment** re-centres the whole curve: Wald's catastrophic minimum
(~0.004) leaps to ~0.94, close to nominal — a clean repair. The **continuity correction** *over*-corrects:
it pushes coverage to essentially **1.0 everywhere**, so the interval never under-covers but is now far too
wide — you have traded the under-coverage problem for a wasted-{term}`expected length` problem. Neither is
free; each moves you along the same coverage↔width axis this whole series has circled.

```{figure} ../_static/coverage_repairs.png
:alt: Coverage of raw Wald, adjusted Wald, and continuity-corrected Wald at n = 40
:width: 100%

The two repairs at $n=40$. **Raw Wald** (orange) sags and plunges to a {term}`zero-width interval` at the
edges. The **adjustment** $h=2$ (blue) lifts it to oscillate tightly around 95% — the good repair. The
**continuity correction** $c=0.5$ (green) rockets it to ~100% everywhere — safe but wastefully wide. Same
method, three very different coverage stories.
```

## The whole series, in one sentence

Every interval in this library is a different answer to one question: *how do you turn a discrete count
into an honest range for $\theta$?* The normal approximation is fast but sags; test inversion fixes the
centre; exact methods guarantee coverage at the cost of width; transforms stabilise the variance but can
fold at the edge; the Bayesian view adds a prior and, with Jeffreys, lands back near the frequentist
answer; and the two repairs trade coverage against length. There is no universally best interval — which
is exactly why `binomcikit` is built to *measure* coverage and length rather than to crown a winner. With
this track behind you, the {doc}`method-selection guide <../method_selection>` and the
{doc}`evaluation tools <../evaluating_intervals>` are yours to use with full understanding.

## Check yourself

**Q1.** A method reports mean coverage 0.94 at $n=40$. Your colleague says "close enough to 0.95, ship it."
What one number do you insist on seeing first, and why?

:::{dropdown} Show answer
The **minimum** coverage. Mean coverage averages over $\theta$ and can hide a catastrophic dip — Wald's
mean is ~0.89 but its minimum is ~0.004. A respectable mean with a terrible minimum means the method fails
badly for *some* true rates, which may be exactly the rate you have. Never approve an interval on mean
{term}`coverage` alone.
:::

**Q2.** Wilson's mean coverage is ~0.95 at $n=20$ and at $n=500$. Does that mean sample size no longer
matters for its coverage?

:::{dropdown} Show answer
No — the **minimum** tells the real story. Wilson's worst-case coverage is ~0.84 at $n=20$ and only reaches
~0.94 at $n=500$; it climbs slowly and unevenly with $n$ (Brown–Cai–DasGupta). The *mean* is flat, but the
worst case keeps improving, so larger $n$ genuinely helps where it counts. The oscillation from
{term}`discreteness` never fully disappears.
:::

**Q3.** You apply a continuity correction ($c=0.5$) to Wald and its coverage becomes 1.0 for every
$\theta$. Is your interval now perfect?

:::{dropdown} Show answer
No — it is *over*-corrected. Coverage pinned at 1.0 means the interval is far wider than a 95% procedure
needs: you have fixed the under-coverage by paying in {term}`expected length`, losing precision you did not
have to lose. The goal is coverage *close to* 0.95, which the {term}`Agresti–Coull`-style adjustment ($h$)
achieves far more efficiently than a heavy continuity correction.
:::

---

:::{admonition} Terms used on this page
:class: seealso
{term}`coverage` · {term}`discreteness` · {term}`zero-width interval` · {term}`standard error` ·
{term}`continuity correction` · {term}`Agresti–Coull` · {term}`expected length` · {term}`theta` ·
{term}`binomial` · {term}`confidence level`
:::

*New here? Start at {doc}`the foundations <../foundations/index>`. Previous: {doc}`the Bayesian view
<06_bayesian_view>`. This completes the theory series — head to {doc}`../method_selection` to choose a
method, or {doc}`../evaluating_intervals` to measure one yourself.*
