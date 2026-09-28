---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Sizing and comparing an LLM eval benchmark

**The situation.** You ran two models on a **100-question** benchmark — pass/fail per question, the
same setup as almost every LLM eval. Model A got **78/100**; Model B got **83/100**. B looks better by
5 points. Is it?

**The question.** Pass/fail on n questions is a {term}`proportion` — exactly what this whole package is
for. Two things practitioners routinely skip: is the apparent gap real, and how many questions would
you actually need to trust an answer either way?

:::{admonition} Why this matters right now
:class: note
This is not a hypothetical. A widely-discussed 2026 finding: a model scoring 80% on a 100-question
benchmark has a 95% {term}`confidence interval` of roughly **71–87%** — wide enough that leaderboard
models are routinely reported as different while their intervals overlap. Most eval pipelines report
the bare percentage and stop there.
:::

## Choosing a method

Model A's {doc}`Wald <../methods/wald>` interval and its {doc}`Wilson <../methods/wilson>` interval
won't differ much at 78–83% (Wald only breaks down near 0% or 100%) — but reach for Wilson by default
anyway, the same {doc}`recommendation <../method_selection>` as everywhere else in this package.

## Running it

Each model's interval, side by side:

```{code-cell} python
import binomcikit as bk

n = 100
a, b = 78, 83

ci_a = bk.ci(a, n, method="wilson")
ci_b = bk.ci(b, n, method="wilson")
{"Model A (78/100)": (round(float(ci_a.iloc[0, 1]), 3), round(float(ci_a.iloc[0, 2]), 3)),
 "Model B (83/100)": (round(float(ci_b.iloc[0, 1]), 3), round(float(ci_b.iloc[0, 2]), 3))}
```

Model A's interval reaches up to about **0.850**; Model B's reaches down to about **0.745**. They
**overlap** by a wide margin — a 5-point gap on 100 questions is well within noise.

Overlapping intervals don't *prove* there's no real difference — `bk.power` answers the sharper
question directly: *if* B is genuinely 5 points better, what's the chance this 100-question benchmark
would have caught it?

```{code-cell} python
detected = bk.power(n, theta0=a / n, p_true=b / n, method="wilson")
round(detected, 3)
```

**About 1 in 5.** Even if B is truly better by this much, a 100-question benchmark has roughly an 80%
chance of *missing* it entirely. That's the number that should give you pause, not the raw 78 vs. 83.

## Reading the result

So how many questions *would* catch a real 5-point gap reliably? `bk.power` again, at a few sizes:

```{code-cell} python
[(n_try, round(bk.power(n_try, a / 100, b / 100, method="wilson"), 3))
 for n_try in [100, 200, 400, 800]]
```

Power climbs from 18% at n=100 to 95% at n=800 — roughly **eight times** the questions to go from
"probably missed it" to "reliably caught it," for the *same* 5-point gap.

```{figure} ../_static/llm_eval_power.png
:alt: Power to detect a 5-point gap (78% vs 83%) versus benchmark size
:width: 100%

Power to detect B's 5-point edge over A, against benchmark size n (Wilson, α = 0.05). The
conventional 80%-power line (dashed) is crossed at **n ≈ 506** — well past the 100-question benchmark
this scenario started from.
```

## How to report it

> Model B scored 5 points higher than Model A (83% vs. 78%, n=100), but the 95% confidence intervals
> overlap substantially (71–89% vs. 69–85%). At this sample size, power to detect a true 5-point gap is
> only ~18% — this benchmark cannot distinguish the models. A benchmark of roughly 500+ questions would
> be needed to detect a gap this size reliably.

**Automating this in CI:** if you run this comparison on every pull request, a copy-paste
GitHub Actions template that posts exactly this table as a PR comment lives in
[`examples/ci-eval-check/`](https://github.com/pranava-ba/binomcikit/tree/main/examples/ci-eval-check)
in the binomcikit repository.

## What could go wrong

- **Reporting the raw percentage and stopping.** 78% vs. 83% reads like a real difference; the
  interval and the power number both say otherwise at n=100.
- **Treating overlapping intervals as proof of "no difference."** They mean the data *can't
  distinguish* the models — not that the models are equal. `bk.power` quantifies exactly how much the
  test could have missed.
- **Using Wald instinctively.** Fine away from the boundary (as here), but the moment a model scores
  near 0% or 100% on a sub-task — common for "trick question" or safety-refusal splits — Wald collapses
  to a {term}`zero-width interval`; see {doc}`zero_events`.
- **Picking a benchmark size after seeing the result** ("we ran 100, it looked significant, we
  stopped") inflates false positives — decide the size with `bk.sample_size`/`bk.power` *before*
  collecting results, not after.

## Try it yourself

A team reports Model C at **91/100** against a baseline at **85/100** — a 6-point gap, on the same
100-question benchmark. Do the intervals overlap? What's the power to detect a true 6-point gap at
n=100?

:::{dropdown} Solution
```python
c_ci = bk.ci(91, 100, method="wilson")          # -> (0.838, 0.952)
base_ci = bk.ci(85, 100, method="wilson")        # -> (0.767, 0.907)
bk.power(100, 0.85, 0.91, method="wilson")       # -> 0.449
```
The intervals still overlap (baseline reaches 0.907, C reaches down to 0.838), and power is still only
about **45%** — near the boundary (91%, 85%) the interval is *narrower* than at 78/83%, but the gap
alone still isn't enough at n=100 for confidence either way. The lesson holds even for "obviously
better" scores near the ceiling.
:::

---

:::{admonition} Terms used on this page
:class: seealso
{term}`proportion` · {term}`confidence interval` · {term}`coverage` · {term}`statistical power` ·
{term}`sample size` · {term}`effect size` · {term}`zero-width interval`
:::

*See also: {doc}`Choosing a method for your own data <choosing_a_method>` · {doc}`Zero events
<zero_events>` · {doc}`sample_size / power in the access layer <../access_layer>`.*
