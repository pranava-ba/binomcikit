---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# A/B test: comparing two conversion rates

**The situation.** You ran an experiment on your sign-up page. The old design (**A**, the control) was
shown to 500 visitors and 32 signed up. A new design (**B**, the variant) was shown to a different 500
visitors and 45 signed up. B *looks* better — 9.0% versus 6.4% — and someone wants to ship it today.

**The question.** Is B genuinely better, or could that gap be the luck of *which* visitors landed in each
group? This is the {doc}`sampling-variability <../foundations/03_sampling_variability>` question from the
Foundations, now with real money on it.

## Choosing a method

`binomcikit` does **single-proportion** inference: it gives you an honest {term}`confidence interval` for
*one* rate at a time. So the plan is to build an interval for each arm and see how they sit relative to
each other. For a plain conversion rate with a few dozen successes, the {doc}`Wilson <../methods/wilson>`
interval (the default) is the right first choice — well-behaved, never collapses, good {term}`coverage`.

:::{important}
A single-proportion tool cannot, by itself, give you a *p*-value for the **difference** B − A. Comparing
the two intervals is a sound first look, but it is not a formal two-sample test — see "What could go
wrong" below.
:::

## Running it

```{code-cell} python
import binomcikit as bk

A = bk.ci(32, 500)      # control: Wilson 95% interval
B = bk.ci(45, 500)      # variant
A
```

```{code-cell} python
B
```

Pull the two intervals out and check whether they overlap:

```{code-cell} python
Alo, Ahi = float(A.iloc[0, 1]), float(A.iloc[0, 2])
Blo, Bhi = float(B.iloc[0, 1]), float(B.iloc[0, 2])
{"A rate": round(32 / 500, 3), "A 95%": (round(Alo, 3), round(Ahi, 3)),
 "B rate": round(45 / 500, 3), "B 95%": (round(Blo, 3), round(Bhi, 3)),
 "overlap?": Blo <= Ahi}
```

## Reading the result

A's plausible range is about **4.6%–8.9%**; B's is about **6.8%–11.8%**. They **overlap** in the band
6.8%–8.9%: there are true rates (say 8%) that are perfectly consistent with *both* arms' data. So although
B's point estimate is higher, the experiment has **not** cleanly separated the two — the gap could still be
sampling noise. The honest verdict is *promising but not conclusive at n = 500 per arm*.

```{figure} ../_static/tutorial_ab.png
:alt: Wilson 95% intervals for arm A and arm B, with their overlap shaded
:width: 100%

Each arm's Wilson 95% interval, dots at the observed rates. The grey band is where they **overlap** —
rates compatible with both arms. Because the band is non-empty, the two arms are not clearly distinguished
by their individual intervals.
```

## How to report it

> The variant converted 9.0% (45/500; 95% CI 6.8–11.8%) versus the control's 6.4% (32/500; 95% CI
> 4.6–8.9%). The intervals overlap, so this experiment does not establish a difference; a larger sample or
> a formal two-proportion test is needed before shipping.

## What could go wrong

- **The overlap fallacy (both directions).** Overlapping 95% intervals do *not* prove "no difference,"
  and non-overlapping ones are a *stricter* bar than a proper test. Interval overlap is a rough visual, not
  a decision rule. For an actual test of B − A, use a two-proportion method (e.g. a two-sample score test);
  two-proportion inference is a **separate** tool, outside single-proportion `binomcikit`.
- **Peeking.** If you checked results every hour and stopped when B looked good, your error rate is far
  above 5%. Fix the sample size in advance.
- **Different populations.** The method assumes each arm is a clean random sample from the same kind of
  visitor. Weekend-vs-weekday or traffic-source imbalance breaks that.

## Try it yourself

Suppose you rerun with **ten times** the traffic and see the same rates: A = 320/5000, B = 450/5000. Do
the intervals still overlap?

:::{dropdown} Solution
```python
import binomcikit as bk
A = bk.ci(320, 5000); B = bk.ci(450, 5000)
float(A.iloc[0, 2]), float(B.iloc[0, 1])      # A upper vs B lower
```
A's interval is now ≈ 5.8–7.1% and B's ≈ 8.2–9.8% — they **no longer overlap**. With 10× the data the
same 2.6-point gap is resolved: {term}`sampling variability` shrank like 1/√n (Foundations page 3), so the
intervals tightened enough to separate. Same effect size, very different conclusion — which is exactly why
sample size matters.
:::

---

:::{admonition} Terms used on this page
:class: seealso
{term}`confidence interval` · {term}`coverage` · {term}`sampling variability` · {term}`proportion` ·
{term}`alpha`
:::

*See also: {doc}`Choosing a method <choosing_a_method>` · {doc}`the Wilson method <../methods/wilson>` ·
{doc}`What a confidence interval means <../foundations/04_confidence_interval>`.*
