# The Bayesian toolbox

Most Python packages can give you a confidence interval for a proportion. **binomcikit's Bayesian
toolbox is the part that is hard to find elsewhere** — a unified set of Bayesian tools for a single
binomial proportion, all built on the same {term}`Beta distribution` machinery. This page is a tour of
what is here and when to reach for it.

Everything below assumes the {term}`prior` → {term}`posterior` idea from the {doc}`methods/bayes` page:
with a Beta(a, b) prior and x successes in n trials, the posterior is Beta(x+a, n−x+b), and every tool
here is a different question asked of that posterior.

New to the vocabulary? Each linked term goes to the {doc}`glossary`.

---

## 1. Credible interval — `ciba` / `cibax`
The Bayesian interval itself: the {term}`posterior mean`, the equal-tailed {term}`credible interval`,
and the {term}`highest posterior density interval`. Full treatment on its own page,
{doc}`methods/bayes`.

```python
bk.ci(x=3, n=20, method="jeffreys")   # or method="bayes" for a flat prior
```

## 2. Empirical Bayes — `empiricalba` / `empiricalbax`
What if you do not want to *choose* a {term}`prior`? {term}`empirical Bayes` **estimates it from the
data**, by fitting the Beta-Binomial marginal likelihood, then forms the credible interval from the
resulting posterior. You bound the search with `sL`, `sU`.

```python
bk.empiricalbax(x=3, n=20, alp=0.05, sL=0.1, sU=10)
# -> x, pomean, LEBAQx, UEBAQx (quantile), LEBAHx, UEBAHx (HPD)
```
Use it when a subjective prior is hard to justify but you still want the Bayesian machinery.

## 3. Bayes factors — `hypotestbaf1` … `hypotestbaf6` (+ `…x`)
A {term}`Bayes factor` weighs two hypotheses about {term}`theta` by how well each predicts the data.
Unlike a p-value, it can provide evidence *for* a null, and it comes with a plain-language reading on
the Jeffreys scale ("positive", "strong", "very strong").

```python
bk.hypotestbaf1x(x=3, n=20, th0=0.5, a1=1, b1=1)
# -> x, BaFa01 (the factor), Interpretation (e.g. "Evidence against H0 is strong")
```

The six formulations differ in **how the two hypotheses are framed**:

| variant | null H₀ | alternative H₁ | signature |
|---|---|---|---|
| `baf1` | point θ = θ₀ | one-sided, θ < θ₀ under a Beta(a₁,b₁) prior | `(n, th0, a1, b1)` |
| `baf2` | point θ = θ₀ | one-sided, θ > θ₀ | `(n, th0, a1, b1)` |
| `baf3` | point θ = θ₀ | two-sided, θ ≠ θ₀ | `(n, th0, a1, b1)` |
| `baf4` | Beta(a₀,b₀) prior below θ₀ | Beta(a₁,b₁) prior above θ₀ | `(n, th0, a0, b0, a1, b1)` |
| `baf5` | Beta(a₀,b₀) prior above θ₀ | Beta(a₁,b₁) prior below θ₀ | `(n, th0, a0, b0, a1, b1)` |
| `baf6` | Beta(a₁,b₁) around θ₁ | Beta(a₂,b₂) around θ₂ | `(n, th1, a1, b1, th2, a2, b2)` |

Each has an `…x` twin (`hypotestbaf1x`, …) for a single observed `x`; the bare name returns the factor
for every `x = 0..n`.

## 4. Posterior probability — `probpos` / `probposx`
A direct probability statement: **how likely is θ below a threshold**, given the data?

```python
bk.probposx(x=3, n=20, a=1, b=1, th=0.3)
# -> x, PosProb = P(theta < 0.3 | data)   (the posterior CDF at th)
```
Perfect for questions like "what is the chance the defect rate is under 5%?" — a question a
{term}`confidence interval` cannot answer directly.

## 5. Posterior predictive — `probpre` / `probprex`
Look **forward**, not at θ itself: given what you have seen, how many successes should you expect in
`m` *future* trials? The {term}`posterior predictive` averages the binomial prediction over the whole
posterior, so it carries your remaining uncertainty about θ (it is wider than plugging in a single p̂).

```python
bk.probprex(x=3, n=20, xnew=2, m=10, a1=1, a2=1)
# -> the Beta-Binomial probability of xnew = 2 successes in m = 10 new trials
```
Use it for planning and prediction — the expected outcome of the *next* batch, not the estimate of the
underlying rate.

---

## How this fits together
| you want to… | tool | returns |
|---|---|---|
| estimate θ with an interval | credible interval (`ciba`) | {term}`posterior mean` + quantile/HPD interval |
| …without choosing a prior | empirical Bayes (`empiricalba`) | prior fitted from data, then the interval |
| compare two hypotheses about θ | Bayes factor (`hypotestbaf1…6`) | factor + Jeffreys-scale reading |
| get P(θ below a threshold) | posterior probability (`probpos`) | a single probability |
| predict the next m trials | posterior predictive (`probpre`) | probability over future counts |

All five share one engine — the Beta(x+a, n−x+b) posterior — which is why they live together here and,
in the R original, define the package's contribution. Each function's exact signature and return
columns are on its {doc}`API reference page <r_to_python_mapping>`.

:::{admonition} Terms used on this page
:class: seealso
{term}`theta` · {term}`prior` · {term}`posterior` · {term}`Bayesian` · {term}`Beta distribution` ·
{term}`credible interval` · {term}`posterior mean` · {term}`highest posterior density interval` ·
{term}`empirical Bayes` · {term}`Bayes factor` · {term}`posterior probability` ·
{term}`posterior predictive` · {term}`confidence interval`
:::
