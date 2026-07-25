---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Test inversion — Wilson and the likelihood-ratio interval

The {doc}`previous page <02_normal_approximation>` showed the {doc}`Wald <../methods/wald>` interval
failing in two ways: it evaluates the {term}`standard error` at $\hat p$ instead of at the true
{term}`theta`, and it collapses to a point at the boundary. This page builds two intervals that fix the
first failure by a completely different route — **not** "estimate, then add a margin," but **invert a
hypothesis test**. It is the single most important idea in the whole subject, and it gives us the
{doc}`Wilson <../methods/wilson>` (score) interval and the {doc}`likelihood-ratio <../methods/lr>`
interval in one stroke.

Every code block here is **executed when the docs are built**, so the numbers are the real package's.

## The idea: an interval is a set of tests that passed

Fix a candidate value $\theta_0$ and ask a yes/no question: *are my data consistent with the true rate
being $\theta_0$?* That is a {term}`hypothesis test` of the {term}`null hypothesis` $H_0:\theta=\theta_0$.
Do that for **every** $\theta_0$ in $[0,1]$ and keep the ones you could not reject. The set you keep is a
confidence interval. This move — building an interval as *the values a test does not reject* — is
{term}`test inversion`.

$$\text{CI} \;=\; \{\,\theta_0 : \text{the test of } H_0:\theta=\theta_0 \text{ is not rejected at level } \alpha\,\}.$$

Why does this give the right {term}`coverage`? Because a level-$\alpha$ test rejects the *true*
$\theta$ at most a fraction $\alpha$ of the time — that is the definition of a test's size. So the true
$\theta$ survives (stays in the interval) at least $1-\alpha$ of the time. Coverage is inherited from
the test, for free. The only remaining choice is **which test** — and that choice is exactly what
separates Wilson from the likelihood-ratio interval below.

## Wilson: invert the score test

The {term}`score test` measures the gap between the observed $\hat p$ and the candidate $\theta_0$ in
units of the standard error **computed at $\theta_0$** — the honest one, since under $H_0$ the rate
*is* $\theta_0$:

$$Z(\theta_0) \;=\; \frac{\hat p - \theta_0}{\sqrt{\theta_0(1-\theta_0)/n}}.$$

Compare $Z(\theta_0)^2$ against the {term}`critical value` $z_{1-\alpha/2}^2$ (about $1.96^2$). Keeping
every $\theta_0$ that passes means solving

$$(\hat p - \theta_0)^2 \;\le\; z^2\,\frac{\theta_0(1-\theta_0)}{n},$$

a **quadratic in $\theta_0$**. Its two roots are the Wilson limits. Notice what changed from Wald: the
$\theta_0(1-\theta_0)$ under the root uses the candidate, not $\hat p$, so the standard error can never
collapse to zero at $x=0$ or $x=n$ — the first Wald failure is gone by construction.

```{code-cell} python
import binomcikit as bk

# Wald vs Wilson for every count x = 0..5 at n = 5:
wald = bk.ciwd(5, 0.05)[["x", "LWD", "UWD"]]
wilson = bk.cisc(5, 0.05)[["LSC", "USC"]]
wald.join(wilson)
```

Look at the `x = 0` row: Wald gives `[0, 0]`, Wilson gives a genuine interval `[0, 0.43…]`. The score
inversion never degenerates.

:::{dropdown} Solving the quadratic — where the Wilson centre comes from
Expanding $(\hat p-\theta_0)^2 = z^2\theta_0(1-\theta_0)/n$ and writing $x=n\hat p$ gives, after
collecting terms in $\theta_0$,

$$\left(n+z^2\right)\theta_0^2 \;-\; \left(2x+z^2\right)\theta_0 \;+\; \frac{x^2}{n} \;=\; 0.$$

The two roots are symmetric about

$$\tilde\theta \;=\; \frac{x + z^2/2}{\,n + z^2\,},$$

which is the Wilson **centre** — the observed $\hat p$ pulled a little toward $1/2$ by an amount that
shrinks as $n$ grows. The half-width is $\dfrac{z}{n+z^2}\sqrt{\,n\hat p(1-\hat p) + z^2/4\,}$. This
"shrink toward $1/2$" is the same instinct as {term}`Agresti–Coull`, which just adds $z^2/2 \approx 2$
pseudo-successes and $z^2/2$ pseudo-failures and then runs Wald on the padded counts.
:::

We can check the centre formula by hand for $x=3,\,n=5$ and confirm it reproduces the package's limits:

```{code-cell} python
from scipy.stats import norm
import numpy as np

x, n = 3, 5
z = norm.ppf(0.975)                      # 1.95996…
centre = (x + z**2 / 2) / (n + z**2)
half   = z / (n + z**2) * np.sqrt(n * (x/n) * (1 - x/n) + z**2 / 4)
print("by hand :", round(centre - half, 6), round(centre + half, 6))
print("package :", *bk.ciscx(x, n, 0.05)[["LSCx", "USCx"]].iloc[0].round(6))
```

## The likelihood-ratio interval: invert the LR test

The second test asks how much *worse* the {term}`likelihood` gets when we force $\theta=\theta_0$
instead of using the best-fitting $\hat p$. That penalty is the {term}`likelihood-ratio statistic`, and
for the binomial it is the **deviance**

$$D(\theta_0) \;=\; 2\!\left[\,x\log\frac{\hat p}{\theta_0} \;+\; (n-x)\log\frac{1-\hat p}{1-\theta_0}\,\right].$$

{term}`Wilks' theorem` says that, under $H_0$, $D(\theta_0)$ behaves like a $\chi^2_1$ variable for
large $n$. So we reject when $D(\theta_0)$ exceeds the $\chi^2_1$ {term}`critical value` at level
$\alpha$ — and the interval is every $\theta_0$ with $D(\theta_0)\le \chi^2_{1,\,1-\alpha}$.

Here is the idea worth pausing on: for one degree of freedom, $\chi^2_{1,\,0.95} = z_{0.975}^2$ —
**the exact same cutoff** the score test used. Score and likelihood-ratio are two different measures of
"surprise" compared against the *same* threshold; they disagree only in how they bend near the edges.

```{code-cell} python
from scipy.stats import chi2
z = norm.ppf(0.975)
print("z**2            =", round(z**2, 5))
print("chi2_1 at 0.95  =", round(chi2.ppf(0.95, 1), 5))   # identical
```

The likelihood-ratio limits are the two $\theta_0$ where the deviance *equals* that cutoff. We can
verify the package's endpoints do exactly that — plug them back into $D$ and get $3.8415$:

```{code-cell} python
def deviance(theta, x, n):
    p = x / n
    return 2 * (x * np.log(p / theta) + (n - x) * np.log((1 - p) / (1 - theta)))

lo, hi = bk.cilrx(3, 5, 0.05)[["LLRx", "ULRx"]].iloc[0]
print("LR interval   :", round(lo, 6), round(hi, 6))
print("deviance at lo:", round(deviance(lo, 3, 5), 4))
print("deviance at hi:", round(deviance(hi, 3, 5), 4))
```

Both endpoints sit right on $3.8415$ — they are, by definition, the edge of the acceptance region.

## Both bracket $\hat p$, and both beat Wald

Line the three intervals up for $x=3,\,n=5$ ($\hat p = 0.6$):

```{code-cell} python
import pandas as pd
rows = {
    "Wald":   bk.ciwdx(3, 5, 0.05)[["LWDx", "UWDx"]].iloc[0].values,
    "Wilson": bk.ciscx(3, 5, 0.05)[["LSCx", "USCx"]].iloc[0].values,
    "LR":     bk.cilrx(3, 5, 0.05)[["LLRx", "ULRx"]].iloc[0].values,
}
pd.DataFrame(rows, index=["lower", "upper"]).T.round(4)
```

All three contain $\hat p=0.6$, but Wald is symmetric about it while Wilson and LR lean **inward** — the
asymmetry that keeps them honest when $\hat p$ is near an edge. The payoff is coverage. Averaged over
$\theta$ at $n=40$, the two inverted intervals stay near the promised 95% while Wald sags well below it:

```{code-cell} python
summary = {
    m: bk.coverage_curve(40, method=m)["coverage"].agg(["mean", "min"]).round(3).to_dict()
    for m in ["wald", "wilson", "lr"]
}
pd.DataFrame(summary).T
```

```{figure} ../_static/test_inversion_coverage.png
:alt: Coverage of Wald, Wilson and LR against the true rate at n = 40
:width: 100%

Actual {term}`coverage` at $n=40$. **Wald** (orange) plunges far below the 95% line near the edges;
**Wilson** (blue) and **LR** (green) oscillate tightly around it. Both inverted intervals inherit their
coverage from the level-$\alpha$ test they invert — the jaggedness is {term}`discreteness`, not a bug,
and is the subject of {doc}`the next page <04_exact_and_discreteness>`.
```

## How this connects to the methods

- The {doc}`Wilson interval <../methods/wilson>` is the score inversion above; it is `binomcikit`'s
  **default** because it is closed-form, never degenerates, and covers well.
- The {doc}`likelihood-ratio interval <../methods/lr>` inverts the deviance test. It has no
  {term}`continuity correction` variant — the LR statistic already carries the shape information a
  correction would add.
- Both use the *asymptotic* $\chi^2_1$ cutoff. When even that approximation is too rough — small $n$,
  $\theta$ hard against 0 or 1 — you drop the approximation entirely and go **exact**, which is where
  the {doc}`Clopper–Pearson, Mid-P and Blaker intervals <../methods/exact>` come in.

## Check yourself

**Q1.** In one sentence, why does inverting a level-$\alpha$ test automatically give an interval with
coverage at least $1-\alpha$?

:::{dropdown} Show answer
Because a level-$\alpha$ test rejects the *true* $\theta$ at most a fraction $\alpha$ of the time, the
true $\theta$ is *kept* (falls inside the interval) at least $1-\alpha$ of the time. The interval
inherits its {term}`coverage` directly from the {term}`null hypothesis` test's size — you never argue
about coverage separately.
:::

**Q2.** The Wald standard error uses $\hat p(1-\hat p)$; the score standard error uses
$\theta_0(1-\theta_0)$. Which one can equal zero for $0<\theta_0<1$, and why does that matter at $x=0$?

:::{dropdown} Show answer
Only Wald's can. At $x=0$, $\hat p=0$ so $\hat p(1-\hat p)=0$ and the Wald interval collapses to the
{term}`zero-width interval` $[0,0]$. The score version uses $\theta_0(1-\theta_0)$, which is strictly
positive for every interior candidate $\theta_0$, so the Wilson interval stays a genuine range even when
$x=0$ — as the first code cell showed (`[0, 0.43…]`).
:::

**Q3.** For $x=3,\,n=5$, confirm with code that the likelihood-ratio *upper* limit really sits on the
$\chi^2_1$ cutoff, and state the cutoff.

:::{dropdown} Show answer
The cutoff is $\chi^2_{1,\,0.95} = 3.8415$ (equal to $z_{0.975}^2$).
```python
lo, hi = bk.cilrx(3, 5, 0.05)[["LLRx", "ULRx"]].iloc[0]
deviance(hi, 3, 5)      # -> 3.8415, exactly the cutoff
```
The upper limit is *defined* as the largest $\theta_0$ whose deviance has not yet exceeded $3.8415$, so
plugging it back in must return the cutoff.
:::

---

:::{admonition} Terms used on this page
:class: seealso
{term}`theta` · {term}`standard error` · {term}`coverage` · {term}`hypothesis test` ·
{term}`null hypothesis` · {term}`test inversion` · {term}`score test` · {term}`critical value` ·
{term}`likelihood` · {term}`likelihood-ratio statistic` · {term}`Wilks' theorem` · {term}`Agresti–Coull` ·
{term}`continuity correction` · {term}`Clopper–Pearson` · {term}`Mid-P` · {term}`discreteness` ·
{term}`zero-width interval`
:::
