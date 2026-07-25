---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Zero events in n trials: the rule of three

**The situation.** You tested a safety mechanism **100** times and it failed **0** times. Or 100 patients
took a drug and **none** had the rare side effect. The observed rate is 0/100 = 0. But "we saw zero" is
not the same as "it can never happen" — so what rate can you actually *claim*?

**The question.** With zero events, what is a defensible **upper bound** on the true rate θ?

## Choosing a method

This is the case that breaks the naive method. The observed {term}`proportion` is 0, and the
{doc}`Wald <../methods/wald>` interval's width is driven by $\sqrt{\hat p(1-\hat p)/n}$, which is **0** when
$\hat p = 0$. So Wald returns the {term}`zero-width interval` $[0, 0]$ — a claim of *perfect certainty*
that the rate is exactly zero, from data that is perfectly consistent with a small positive rate. Useless.

You need a method that stays sensible at the boundary: {doc}`Wilson <../methods/wilson>` or an
{doc}`exact <../methods/exact>` interval. And there is a famous shortcut, the **rule of three**.

## Running it

Watch Wald fail, then get a real bound:

```{code-cell} python
import binomcikit as bk

wald   = bk.ci(0, 100, method="wald")     # the trap
wilson = bk.ci(0, 100, method="wilson")   # a real interval
{"Wald":   (round(float(wald.iloc[0, 1]), 3),   round(float(wald.iloc[0, 2]), 3)),
 "Wilson": (round(float(wilson.iloc[0, 1]), 3), round(float(wilson.iloc[0, 2]), 3))}
```

Wald gives `(0.0, 0.0)`; Wilson gives `(0.0, 0.037)` — a genuine upper bound of about **3.7%**. Now the
rule of three. Because you only care about the *upper* side, the natural summary is a **one-sided 95%**
bound, and there is a beautifully simple approximation for it: **3 / n**.

```{code-cell} python
n = 100
rule_of_three = 3 / n

# The exact one-sided 95% upper bound = the upper limit of a 90% two-sided exact interval:
exact_one_sided = float(bk.ci(0, n, alpha=0.10, method="exact", e=1.0).iloc[0, 2])

{"rule of three (3/n)": round(rule_of_three, 4),
 "exact one-sided 95%": round(exact_one_sided, 4)}
```

3/100 = 0.030 versus the exact 0.0295 — the rule of three is accurate to a fraction of a percent, and it
needs no software at all.

## Reading the result

With 0 events in 100 trials you can say, with 95% one-sided confidence, that the true rate is **below about
3%** (3/n). It is *not* zero — you simply have not run enough trials to distinguish "rare" from "never." To
push the ceiling down to 1% you would need roughly 300 trials (3/300 = 0.01), and the shortcut keeps
tracking the exact bound as n grows:

```{figure} ../_static/tutorial_zero.png
:alt: Upper bound on theta versus n for the rule of three, exact, and Wilson
:width: 100%

With 0 events, the upper bound on θ against the number of trials. The **rule of three** (orange dashed)
sits almost exactly on the **exact one-sided 95%** bound (blue) across the whole range; the two-sided
**Wilson** upper (green) is a touch higher because it splits the 5% over *two* tails. Whatever you use, the
bound falls like 1/n — halving it takes twice the trials.
```

## How to report it

> No failures were observed in 100 trials. By the rule of three, the true failure rate is below
> approximately 3% with 95% (one-sided) confidence (exact one-sided upper bound 2.95%). Zero observed
> events do not establish a zero rate.

## What could go wrong

- **Claiming the rate is zero.** 0/100 does not mean θ = 0; it means θ is *probably small*. The
  {term}`zero-width interval` from Wald is exactly this mistake encoded in an interval — never report it.
- **One-sided vs two-sided confusion.** "3/n" is the *one-sided* 95% bound. The default two-sided 95%
  interval is a bit wider on top (it spends 2.5% on the upper tail, giving ≈ 3.7/n). State which you mean.
- **Rare-event assumptions.** The rule of three assumes independent trials with a constant rate. Clustered
  failures (a bad batch) violate that and the bound will be too optimistic.

## Try it yourself

A lab reports **0** contaminations in **60** samples. Give a quick 95% upper bound by hand, then check it.

:::{dropdown} Solution
Rule of three: $3/60 = \mathbf{0.05}$, i.e. below about **5%**.
```python
import binomcikit as bk
float(bk.ci(0, 60, alpha=0.10, method="exact", e=1.0).iloc[0, 2])   # -> about 0.0487
```
The exact one-sided bound is 4.87%, so "under 5%" is a fair, slightly conservative summary — with only 60
samples you cannot promise anything tighter.
:::

---

:::{admonition} Terms used on this page
:class: seealso
{term}`proportion` · {term}`zero-width interval` · {term}`confidence interval` · {term}`Clopper–Pearson` ·
{term}`confidence level`
:::

*See also: {doc}`the Wald failure modes (theory) <../theory/02_normal_approximation>` · {doc}`exact methods
<../methods/exact>` · {doc}`Quality control <quality_control>`.*
