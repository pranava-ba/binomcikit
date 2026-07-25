---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Exact methods and discreteness

The {doc}`previous page <03_test_inversion>` built intervals by inverting a test — but the tests there
(score, likelihood-ratio) lean on a *large-sample* approximation: their cutoff is the $\chi^2_1$ /
normal quantile, which is only exactly right as $n \to \infty$. This page inverts the **exact** binomial
test instead, using the real {term}`binomial` probabilities and no normal approximation at all. That buys
an ironclad guarantee — coverage never drops below the promised level — but the guarantee collides with a
hard fact from {doc}`page 2 of the foundations <../foundations/02_binomial>`: the count is a whole number.
That collision, **{term}`discreteness`**, is why exact intervals are wider than they "should" be, and why
there is more than one of them.

Every code block here is **executed when the docs are built**.

## Why coverage is a jagged step function

Recall the exact {term}`coverage` formula (foundations {doc}`page 5 <../foundations/05_coverage>`): for a
true rate $\theta$, add up the {term}`binomial` probabilities of exactly those counts whose interval
traps $\theta$. As $\theta$ slides upward, nothing changes *until* it crosses one of an interval's
endpoints — at that instant a whole count's probability lump either joins or leaves the sum, and coverage
**jumps**. Between crossings it drifts smoothly; at each crossing it steps. So $\text{Coverage}(\theta)$
is a sawtooth, not a flat line — a direct fingerprint of the count being discrete.

```{code-cell} python
from math import comb
import binomcikit as bk

def coverage(theta, n, grid, lcol, ucol):
    g = grid.set_index("x")
    return float(sum(
        comb(n, x) * theta**x * (1 - theta) ** (n - x)
        for x in range(n + 1) if g.loc[x, lcol] <= theta <= g.loc[x, ucol]
    ))

cp = bk.ciex(40, 0.05, 1.0)      # Clopper–Pearson grid (e = 1), columns LEX / UEX
# Coverage at four nearby true rates — it hops around, never settling on 0.95:
{t: round(coverage(t, 40, cp, "LEX", "UEX"), 4) for t in [0.28, 0.29, 0.30, 0.31]}
```

Because coverage can only *step*, you cannot pin it to exactly $1-\alpha$ everywhere. A method must
choose: stay **at or above** the line for every $\theta$ (safe, but wide), or weave **through** it (tight,
but occasionally short). Exact methods take the first road.

## Clopper–Pearson: invert the exact test

The {term}`Clopper–Pearson` interval keeps every $\theta_0$ that the exact two-sided binomial test does
not reject — the {doc}`test inversion <03_test_inversion>` idea, but with the real
{term}`tail probability` values instead of a normal approximation. Its limits have a closed form as {term}`Beta distribution`
{term}`quantile`s, and it is the textbook "exact" interval.

```{code-cell} python
bk.ciex(5, 0.05, 1.0)[["x", "LEX", "UEX", "ZWI"]]
```

Two things to notice. Like {doc}`Wilson <../methods/wilson>`, it never collapses (`ZWI` is all `NO`);
`x = 0` gives $[0,\,0.52]$, not $[0,0]$. And — this is the price — its intervals are *wide*. Because it
insists on covering at every $\theta$ despite the sawtooth, it ends up covering **too much** on average:

```{code-cell} python
c = bk.coverage_curve(40, method="exact")["coverage"]
{"mean coverage": round(float(c.mean()), 3), "minimum": round(float(c.min()), 3)}
```

The minimum stays above 0.95 — the guarantee holds — but the **mean is 0.971**, well above nominal. Every
extra percent of coverage over 0.95 is bought with interval width you did not need. That over-coverage is
the definition of **conservative**.

## Mid-P: shave the atom

The conservatism comes from counting the *whole* probability lump at the observed count $x$ in the tail.
The **{term}`Mid-P`** correction counts only **half** of it — as if splitting the discrete atom down the
middle. `binomcikit` exposes this through the same function with the tail fraction `e`: `e = 1` is
Clopper–Pearson, `e = 0.5` is Mid-P.

```{code-cell} python
bk.ciex(5, 0.05, 0.5)[["x", "LEX", "UEX"]]      # e = 0.5 → Mid-P, visibly narrower than CP above
```

Mid-P sits much closer to nominal — but it pays for it by **giving up the guarantee**: its coverage now
dips *below* 0.95 at some $\theta$.

```{code-cell} python
c = bk.coverage_curve(40, method="midp")["coverage"]
{"mean coverage": round(float(c.mean()), 3), "minimum": round(float(c.min()), 3)}
```

Mean 0.957, minimum 0.928 — tighter and better-centred than Clopper–Pearson, but no longer a *guaranteed*
95% procedure. It is the pragmatic compromise: exact-flavoured, near-nominal, not conservative.

## Blaker: the acceptability function

Is there a method that keeps Clopper–Pearson's **guarantee** yet is **narrower**? Yes — Blaker's (2000)
interval. It inverts a smarter exact test built on the **{term}`acceptability function`** $\gamma(x,
\theta)$: take the smaller of the two {term}`tail probability` values at $x$, then add back the opposite tail
*truncated to be no larger than it*. The interval is every $\theta$ with $\gamma(x,\theta) \ge \alpha$.
Its endpoints are exactly where $\gamma = \alpha$ — which we can reproduce from scratch, the same way we
checked the LR deviance on the previous page:

```{code-cell} python
import numpy as np
from scipy.stats import binom

def acceptability(x, theta, n):
    j = np.arange(n + 1)
    h_j = np.minimum(binom.cdf(j, n, theta), binom.sf(j - 1, n, theta))   # min tail at each j
    h_x = min(binom.cdf(x, n, theta), binom.sf(x - 1, n, theta))          # min tail at observed x
    return float(binom.pmf(j, n, theta)[h_j <= h_x + 1e-12].sum())

blaker = bk.ciblaker(5, 0.05).set_index("x")     # columns LBK / UBK
lo, hi = blaker.loc[3, "LBK"], blaker.loc[3, "UBK"]
print("Blaker interval x=3 :", round(lo, 6), round(hi, 6))
print("acceptability at lo :", round(acceptability(3, lo, 5), 4))    # -> 0.05 = alpha
print("acceptability at hi :", round(acceptability(3, hi, 5), 4))    # -> 0.05 = alpha
```

Both endpoints sit on $\gamma = \alpha = 0.05$, by definition. The payoff is a genuine domination of
Clopper–Pearson: Blaker's interval is a **{term}`nested interval`** — never poking outside CP, usually
strictly inside it — at *every* count:

```{code-cell} python
cp5 = bk.ciex(5, 0.05, 1.0).set_index("x")
lower_inside = (blaker["LBK"] >= cp5["LEX"] - 1e-9).all()
upper_inside = (blaker["UBK"] <= cp5["UEX"] + 1e-9).all()
{"Blaker lower ≥ CP lower everywhere": bool(lower_inside),
 "Blaker upper ≤ CP upper everywhere": bool(upper_inside)}
```

And it keeps the guarantee while doing so — its coverage still never drops below 0.95, but its mean is
lower (tighter) than CP's:

```{code-cell} python
c = bk.coverage_curve(40, method="blaker")["coverage"]
{"mean coverage": round(float(c.mean()), 3), "minimum": round(float(c.min()), 3)}
```

## The guarantee-versus-width trade-off, in one table

```{code-cell} python
import pandas as pd
rows = {}
for m, lab in [("exact", "Clopper–Pearson"), ("blaker", "Blaker"),
               ("midp", "Mid-P"), ("wilson", "Wilson")]:
    c = bk.coverage_curve(40, method=m)["coverage"]
    rows[lab] = {"mean": round(float(c.mean()), 3),
                 "min": round(float(c.min()), 3),
                 "share ≥ 0.95": round(float(np.mean(c.to_numpy() >= 0.95)), 2)}
pd.DataFrame(rows).T
```

Read the `share ≥ 0.95` column as "does it keep the promise?" **Clopper–Pearson** and **Blaker** hold it
everywhere (1.00) — they are *guaranteed* — but Blaker does it with a lower mean, i.e. narrower intervals:
it **dominates** Clopper–Pearson. **Mid-P** and **Wilson** trade the guarantee away (0.65 and 0.54) to sit
closer to nominal, so they are tighter still but occasionally short. There is no free lunch — you choose
*where* on the guarantee↔width axis to stand.

```{figure} ../_static/exact_discreteness_coverage.png
:alt: Coverage of Clopper–Pearson, Blaker and Wilson against the true rate at n = 40
:width: 100%

The trade-off drawn out ($n = 40$). **Clopper–Pearson** (orange) rides highest — always above the 95%
line, hence widest. **Blaker** (green) also stays above the line but hugs it more closely — same guarantee,
less waste. **Wilson** (blue) weaves *through* the line, dipping below near the boundaries — tightest, but
not guaranteed. All three are jagged: that sawtooth is {term}`discreteness`, unavoidable for any binomial
interval.
```

## How this connects to the methods

- {doc}`Clopper–Pearson and Mid-P <../methods/exact>` are the `ciex` family (`e = 1` and `e = 0.5`); pick
  CP when you must *never* under-cover (regulatory, safety), Mid-P when you want exact-flavour without the
  conservatism.
- {doc}`Blaker <../methods/blaker>` is the method to prefer when you want the guarantee **and** short
  intervals — it is `binomcikit`'s addition beyond the original R package, precisely because it dominates
  Clopper–Pearson.
- The remaining approximate families — {doc}`arcsine <../methods/arcsine>` and {doc}`logit
  <../methods/logit>` — attack the problem from the other side, by *transforming* to a scale where the
  variance is stable. That is {doc}`the next page <05_transformed_intervals>`.

## Check yourself

**Q1.** Why can no binomial interval have coverage exactly $0.95$ at every $\theta$, no matter how cleverly
it is built?

:::{dropdown} Show answer
Because of {term}`discreteness`. The count $X$ takes only whole values, so as $\theta$ moves, coverage can
only change when $\theta$ crosses an endpoint — a discrete probability lump jumps in or out and coverage
*steps*. A step function that takes finitely many values cannot equal $0.95$ on a whole continuum. Every
method is stuck oscillating around nominal; the only choice is whether to stay above the line (exact) or
weave through it (approximate).
:::

**Q2.** Clopper–Pearson has mean coverage $0.971$ at $n = 40$, comfortably above $0.95$. Why is that a
*criticism*, not praise?

:::{dropdown} Show answer
Because coverage above nominal is bought with **width**. A 0.971 mean means the intervals are wider than a
true 95% procedure needs — you are paying in {term}`expected length` (lost precision) for coverage you were
not asked to provide. The ideal is *close to* 0.95. Being needlessly conservative is a real cost;
{doc}`Blaker <../methods/blaker>` and {term}`Mid-P` exist specifically to reduce it.
:::

**Q3.** Using the `acceptability` function above, show that $\theta = 0.25$ lies **inside** the Blaker
interval for $x = 3$, $n = 5$. What is the rule?

:::{dropdown} Show answer
A value $\theta$ is in the Blaker interval when its {term}`acceptability function` is at least $\alpha =
0.05$.
```python
acceptability(3, 0.25, 5)      # -> 0.1035, which is >= 0.05, so 0.25 is inside
```
$\gamma(3, 0.25) = 0.1035 \ge 0.05$, so the exact test does not reject $\theta = 0.25$ and it is kept.
(The interval's endpoints, $0.189$ and $0.924$, are exactly where $\gamma$ drops to $0.05$.)
:::

---

:::{admonition} Terms used on this page
:class: seealso
{term}`binomial` · {term}`discreteness` · {term}`coverage` · {term}`test inversion` ·
{term}`tail probability` · {term}`Clopper–Pearson` · {term}`Beta distribution` · {term}`quantile` ·
{term}`Mid-P` · {term}`acceptability function` · {term}`nested interval` · {term}`expected length` ·
{term}`alpha` · {term}`confidence level`
:::

*New here? Start at {doc}`the foundations <../foundations/index>`. Previous: {doc}`test inversion
<03_test_inversion>`. Next in the series: variance-stabilising and transformed intervals (arcsine, logit).*
