# ArcSine (variance-stabilising) interval

> **In one line:** a confidence interval for a {term}`proportion` built on a stretched scale where the
> data's wobble is constant. It behaves well in the **interior** (θ away from 0 and 1) but has a
> notorious **boundary failure** — near 0 or 1 it collapses to a point that can *exclude the value you
> actually observed*. Prefer **Wilson** as a default; reach for arcsine for its specific, historical role.

*New here?* Read {doc}`../foundations/index` first — it explains proportions, trials, and what a
confidence interval means, with no maths. Every technical word below is a link to the
{doc}`../glossary`.

This page has two parts: **Use it** (how to call it) and **Understand it** (the maths behind it).

---

## Use it

### Import and call
```python
import binomcikit as bk

# one interval, for x successes in n trials:
bk.ci(x=3, n=20, method="arcsine")   # "arc-sine" is an alias and identical

# the interval for every possible x = 0, 1, ..., n:
bk.ci(n=20, method="arcsine")

# the flat function does the same thing:
bk.cias(20, 0.05)
```

### Parameters
| name | plain English | formal |
|---|---|---|
| `x` | how many successes you saw (optional; omit for all x) | the observed count, 0 ≤ x ≤ n |
| `n` | how many trials in total | the number of {term}`Bernoulli trial`s |
| `alpha` | your error budget; `0.05` gives a 95% interval | {term}`alpha` (α); confidence is 1 − α |

### What you get back
A table (pandas `DataFrame`). For each `x` it gives the lower and upper limits `LAS`, `UAS`, plus
three diagnostic flags:

| column | meaning |
|---|---|
| `LAS`, `UAS` | the lower and upper ends of the **A**rc**S**ine interval (both clamped to lie in [0, 1]) |
| `ZWI` | **{term}`zero-width interval`** — `YES` when the interval collapses to a point (arcsine does this **at the boundary**, x = 0 and x = n) |
| `LABB`, `UABB` | **{term}`aberration`** flags — `YES` when a limit runs past a sensible boundary |

### Examples
The paper's worked example, `n = 5`, `alpha = 0.05` (values match the closed form and the golden
oracle in `tests/cases.py::ARCSINE_N5`):

| x | LAS | UAS | note |
|---:|---:|---:|---|
| 0 | 0.180 | 0.180 | `ZWI` — and it **excludes 0**, the value you observed! |
| 1 | 0.001 | 0.616 | |
| 2 | 0.060 | 0.813 | |
| 3 | 0.188 | 0.941 | well-behaved in the interior |
| 4 | 0.385 | 0.999 | |
| 5 | 0.820 | 0.820 | `ZWI` — and it **excludes 1** |

Look at the `x = 0` row. You observed **zero** successes, yet arcsine reports the interval `[0.18,
0.18]` — it does not even contain 0. Compare the same row across methods: Wald gives the (also useless)
`[0, 0]`, but **Wilson** gives a sensible `[0, 0.43]`. That boundary row is the whole reason arcsine is
not a default.

### Recipes
- **Adjusted form (`h`):** `bk.ci(x=3, n=20, method="arcsine", h=2)` adds `h` pseudo-successes and `h`
  pseudo-failures before transforming — the offset that tames the boundary (the Anscombe / Freeman–Tukey
  idea).
- **With a {term}`continuity correction`:** `bk.ci(n=20, method="arcsine", c=0.5)` widens the interval
  slightly to respect the discreteness of the counts.
- **Compare its {term}`coverage` against other methods:** feed the limits to the `covp*` family
  (see {doc}`../user_guide/index`), or read the figure below.
- **Plot it (interactive, Plotly):** `bk.plot_ci(n=20, method="arcsine")` draws the interval for every
  `x`; `bk.plot_coverage(n=20, methods=["arcsine", "wilson"])` overlays coverage curves. Plotting needs
  `pip install binomcikit[plots]`.

### Gotchas
- **Boundary collapse.** At x = 0 and x = n the interval degenerates to a single point that *excludes*
  the observed {term}`proportion`. This is arcsine's defining weakness — do not use the raw method when
  small counts are likely. The `h`-adjusted form is the standard repair.
- The limits are **not symmetric** around p̂ = x/n; the transform bends the scale near the edges.

---

## Understand it

### The idea, before any symbols
Wald's problem is that a proportion's wobble ({term}`standard error`) changes with θ: it is largest near
½ and shrinks to nothing near 0 and 1. Arcsine plays a clever trick. It re-plots the proportion on a
*stretched* scale — the arcsine-of-the-square-root scale — chosen precisely so that the wobble is the
**same size everywhere**, no matter what θ is. On that flattened scale you can lay down a plain,
symmetric interval; then you bend the two endpoints back onto the ordinary 0-to-1 scale. The interior
behaves beautifully. The catch is at the very edges, where "bend the endpoints back" quietly loses
information.

### The formula
$$\sin^2\!\left(\arcsin\sqrt{\hat p}\;\pm\;\frac{z_{1-\alpha/2}}{2\sqrt{n}}\right)$$

Reading each piece:
- $\hat p = x/n$ — the observed {term}`proportion` (an {term}`estimate` of {term}`theta`).
- $\varphi = \arcsin\sqrt{\hat p}$ — the {term}`variance-stabilising transformation` of p̂.
- $z_{1-\alpha/2}$ — the **{term}`critical value`** (≈ 1.96 for 95%), a {term}`quantile` of the normal curve.
- $\dfrac{1}{2\sqrt{n}}$ — the {term}`standard error` of φ. The whole point of the transform: it does
  **not** depend on θ.
- $\sin^2(\cdot)$ — the {term}`back-transformation` that returns the limits to the 0–1 scale. Note it is
  $\sin^2(\varphi)$ of the **whole** angle, *not* $\sin^2(\varphi/2)$ — a common typo that gives the
  wrong interval.

:::{dropdown} Where it comes from (the derivation)
On a proportion, $\operatorname{Var}(\hat p)=\theta(1-\theta)/n$ depends on θ. Apply the transform
$\varphi=g(\hat p)=\arcsin\sqrt{\hat p}$. By the delta method its variance is
$\operatorname{Var}(\varphi)\approx g'(\theta)^2\,\theta(1-\theta)/n$, and because
$g'(p)=\tfrac{1}{2\sqrt{p(1-p)}}$ the $\theta(1-\theta)$ factors **cancel**, leaving
$\operatorname{Var}(\varphi)\approx 1/(4n)$ — a constant. So on the φ-scale the ordinary Wald recipe
$\varphi\pm z/(2\sqrt n)$ is honest. Undo the transform with $p=\sin^2(\varphi)$ to get the interval
above.

The boundary failure is now visible. At x = 0, φ = arcsin√0 = 0, and the φ-interval is
$[-z/2\sqrt n,\; +z/2\sqrt n]$ — a band straddling 0. But $\sin^2$ is symmetric about 0, so **both**
endpoints map to the same positive number $\sin^2(z/2\sqrt n)$, and the true minimum of $\sin^2$ over
that band (the value 0, at φ = 0) is thrown away. The result is a {term}`zero-width interval` sitting
at ≈ 0.18 that misses p̂ = 0 entirely. Variants that add a small offset before transforming — Anscombe
(1948) using (x+⅜)/(n+¾), Freeman–Tukey (1950) — keep φ away from 0 and largely fix this.
:::

### When it works — and when it doesn't
Arcsine is a solid performer in the **interior**: for θ roughly in 0.2–0.8 its {term}`coverage` tracks
the nominal level about as well as **Wilson**. It fails **at the boundary** — for θ near 0 or 1 the
coverage plunges, and at x = 0 or x = n the interval degenerates as shown above. Its historical
importance is as the archetype of the {term}`variance-stabilising transformation` idea (Bartlett 1936;
Anscombe 1948; Freeman & Tukey 1950), which recurs throughout statistics.

```{figure} ../_static/arcsine_coverage.png
:alt: Coverage probability versus theta for Wald, ArcSine and Wilson at n=20
:width: 100%

**Good in the middle, broken at the edges.** True {term}`coverage` against θ for n = 20, α = 0.05
(produced by binomcikit's own metric engine). ArcSine (orange) hugs the nominal 0.95 line across the
interior — clearly beating Wald (blue) — but **dives** as θ approaches 0 or 1, exactly where **Wilson**
(green) stays stable. Reproduce with `bk.plot_coverage(n=20, methods=["wald", "arcsine", "wilson"])`.
```

### The fixes
- **Offset / adjusted form** (`h=…`, or the Anscombe and Freeman–Tukey variants) — nudge the counts away
  from 0 and n before transforming, which stops the boundary collapse. This is the usual repair.
- **Just use {doc}`Wilson <wilson>`** — for a general default it is simpler to reason about and has
  no boundary blind spot.

### References
The variance-stabilising lineage is Bartlett (1936) [4], Anscombe (1948) [3] and Freeman & Tukey (1950)
[5]; the boundary behaviour and comparisons are discussed in Brown, Cai & DasGupta (2001) [16]. Full
citations: the project's `planning/RESEARCH.md` §11. Deeper maths: {doc}`../theory/index`.

---

:::{admonition} Terms used on this page
:class: seealso
{term}`proportion` · {term}`theta` · {term}`trial` · {term}`Bernoulli trial` · {term}`success` ·
{term}`estimate` · {term}`confidence interval` · {term}`coverage` · {term}`alpha` ·
{term}`standard error` · {term}`critical value` · {term}`quantile` ·
{term}`variance-stabilising transformation` · {term}`back-transformation` ·
{term}`continuity correction` · {term}`zero-width interval` · {term}`aberration`
:::
