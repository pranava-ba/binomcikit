# Wilson (Score) interval

> **In one line:** the recommended default confidence interval for a {term}`proportion`. It keeps its
> promised {term}`coverage` far better than **Wald**, works for small samples, and never collapses to
> a point — at the small cost of being slightly lopsided (which is the honest thing to be near 0 and 1).

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
bk.ci(x=3, n=20, method="wilson")   # "score" is an alias and identical

# the interval for every possible x = 0, 1, ..., n:
bk.ci(n=20, method="wilson")

# the flat function does the same thing:
bk.cisc(20, 0.05)
```

Wilson is the **default**, so `bk.ci(x=3, n=20)` (no `method=`) already gives you this interval.

### Parameters
| name | plain English | formal |
|---|---|---|
| `x` | how many successes you saw (optional; omit for all x) | the observed count, 0 ≤ x ≤ n |
| `n` | how many trials in total | the number of {term}`Bernoulli trial`s |
| `alpha` | your error budget; `0.05` gives a 95% interval | {term}`alpha` (α); confidence is 1 − α |

### What you get back
A table (pandas `DataFrame`). For each `x` it gives the lower and upper limits `LSC`, `USC`, plus
three diagnostic flags:

| column | meaning |
|---|---|
| `LSC`, `USC` | the lower and upper ends of the **S**core interval (both inside [0, 1] by construction) |
| `ZWI` | **{term}`zero-width interval`** — `YES` if the interval ever collapses to a point (Wilson essentially never does) |
| `LABB`, `UABB` | **{term}`aberration`** flags — `YES` when a limit runs past a sensible boundary |

### Examples
The paper's worked example, `n = 5`, `alpha = 0.05` (values match
`statsmodels` `proportion_confint(method="wilson")`):

| x | LSC | USC | note |
|---:|---:|---:|---|
| 0 | 0.000 | 0.434 | a **real** interval at the boundary — not a point |
| 1 | 0.036 | 0.624 | |
| 2 | 0.118 | 0.769 | |
| 3 | 0.231 | 0.882 | pulled inward, toward ½ |
| 4 | 0.376 | 0.964 | |
| 5 | 0.566 | 1.000 | again a real interval, not a point |

Compare the boundary rows with Wald's on the {doc}`wald` page: where Wald gives the useless `[0, 0]`
and `[1, 1]`, Wilson still reports a sensible range. That is the single clearest reason to prefer it.

### Recipes
- **Adjusted form (`h`):** `bk.ci(x=3, n=20, method="wilson", h=2)` adds `h` pseudo-successes and `h`
  pseudo-failures before scoring (an {term}`Agresti–Coull`-style nudge).
- **With a {term}`continuity correction`:** `bk.ci(n=20, method="wilson", c=0.5)` widens the interval
  slightly to respect the discreteness of the counts.
- **Compare its {term}`coverage` against other methods:** feed the limits to the `covp*` family
  (see {doc}`../user_guide/index`), or just eyeball the figure below.
- **Plot it (interactive, Plotly):** `bk.plot_ci(n=20, method="wilson")` draws the interval for every
  `x`; `bk.plot_coverage(n=20, methods=["wald", "wilson"])` overlays coverage curves. Plotting needs
  `pip install binomcikit[plots]`.

### Gotchas
- The interval is **not symmetric** around p̂ = x/n — it leans toward ½. That is a feature, not a bug:
  it is exactly the correction that fixes Wald's coverage.
- The midpoint is a *shrunken* estimate `(x + z²/2)/(n + z²)`, not the raw p̂. If you need the interval
  centred on p̂, you want Wald or {term}`Agresti–Coull`, not Wilson.

---

## Understand it

### The idea, before any symbols
Wald asks: "given the proportion I *observed*, how far could the truth wander?" Wilson turns the
question around: "for which true rates θ would a result like mine be *unsurprising*?" You test each
candidate θ, and keep every θ that your data do not clearly rule out. That set of survivors **is** the
interval. Because each θ is judged using the wobble expected *at that θ* — not the wobble at your
single observed p̂ — the answer stays honest even when p̂ sits at 0 or 1.

### The formula
$$\frac{n}{n+z^2}\left[\left(\hat p + \frac{z^2}{2n}\right)\pm z\sqrt{\frac{\hat p\,\hat q}{n} + \frac{z^2}{4n^2}}\right]$$

Reading each piece:
- $\hat p = x/n$, $\hat q = 1-\hat p$ — the observed {term}`proportion` and its complement.
- $z = z_{1-\alpha/2}$ — the **{term}`critical value`**, a {term}`quantile` of the normal curve
  (≈ 1.96 for 95%).
- $\hat p + z^2/2n$ — the **shrunken centre**: the interval is built around a point nudged toward ½,
  which is why it is not symmetric about p̂.
- The $\dfrac{n}{n+z^2}$ factor and the $z^2/4n^2$ inside the root are what keep the whole interval
  inside [0, 1] and stop it collapsing at the boundary.

:::{dropdown} Where it comes from (the derivation)
Wilson is a {term}`test inversion`. Start from the {term}`score test`: to test a {term}`null
hypothesis` θ = θ₀, standardise the estimate using the {term}`standard error` **evaluated at θ₀**,
$(\hat p - \theta_0)\big/\sqrt{\theta_0(1-\theta_0)/n}$, and reject when its square exceeds $z^2$.
The interval is every θ₀ that survives — i.e. the solutions of

$$(\hat p - \theta_0)^2 = z^2\,\frac{\theta_0(1-\theta_0)}{n}.$$

This is a **quadratic in θ₀**; solving it gives the two limits in the formula above. Contrast Wald,
which evaluates the same {term}`standard error` at $\hat p$ instead of at θ₀ — the shortcut that makes
Wald a one-line formula but wrecks its coverage near the boundary. Wilson pays a quadratic solve and
gets reliability in return (Brown, Cai & DasGupta 2001 [16]).
:::

### When it works — and when it doesn't
Wilson is a sound default across essentially the whole range of `n` and {term}`theta`: its true
{term}`coverage` oscillates *around* the nominal level instead of sagging below it, and it is defined
and sensible at x = 0 and x = n. Its one honest weakness is that coverage can still spike *above*
nominal in narrow zones (making it a touch conservative there), and for guaranteed-≥-nominal coverage
you would reach for the continuity-corrected Wilson (`c=0.5`) or an exact method. It has been
repeatedly recommended as the practical default (Agresti & Coull 1998 [13]; Newcombe 1998 [14];
Brown, Cai & DasGupta 2001 [16]).

```{figure} ../_static/wilson_coverage.png
:alt: Coverage probability versus theta for Wald and Wilson at n=20
:width: 100%

**Wilson tracks the target; Wald sags.** True {term}`coverage` against θ for n = 20, α = 0.05
(produced by binomcikit's own metric engine). The Wilson curve (orange) oscillates around the nominal
0.95 line across the whole range, while Wald (blue) sits well below it almost everywhere and dives at
the boundaries. Reproduce with `bk.plot_coverage(n=20, methods=["wald", "wilson"])`.
```

### Relatives
- **{term}`Agresti–Coull`** — a deliberately simpler cousin: it approximates Wilson's shrunken centre
  ("add ~2 successes and 2 failures") but then reverts to a *symmetric* Wald-style width. Easier to
  explain, almost as good. *(Its own page in a later sub-phase.)*
- **Continuity-corrected Wilson** (`c=0.5`) — nudges the limits outward so coverage stays at or above
  nominal, at the cost of slightly wider intervals.

### References
Wilson (1927) [1] introduced the score interval; its status as a recommended default is argued in
Agresti & Coull (1998) [13], Newcombe (1998) [14] and Brown, Cai & DasGupta (2001) [16]. Full
citations: the project's `planning/RESEARCH.md` §11. Deeper maths: {doc}`../theory/index`.

---

:::{admonition} Terms used on this page
:class: seealso
{term}`proportion` · {term}`theta` · {term}`trial` · {term}`Bernoulli trial` · {term}`success` ·
{term}`estimate` · {term}`confidence interval` · {term}`coverage` · {term}`alpha` ·
{term}`standard error` · {term}`critical value` · {term}`quantile` · {term}`null hypothesis` ·
{term}`score test` · {term}`test inversion` · {term}`Agresti–Coull` · {term}`continuity correction` ·
{term}`zero-width interval` · {term}`aberration`
:::
