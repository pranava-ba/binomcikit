# Foundations — probability from zero

**What this is:** a short, self-contained course in the handful of ideas the rest of the docs stand on —
what a proportion is, how a sample wobbles around the truth, what a confidence interval *really* claims,
and the one number (coverage) that tells you whether a method keeps its promise. **What you need first:**
nothing but arithmetic. Every technical word is a link to the {doc}`../glossary`; every example is small
enough to check by hand or is run for you when these pages are built.

:::{note}
Read the five pages below in order — each one builds on the last. By the end you can open any
{doc}`method page <../methods/index>` and follow both halves of it. When you want the *why* behind the
formulas, the {doc}`../theory/index` track takes each idea further.
:::

## The journey

1. **{doc}`A proportion, and its estimate <01_proportion>`** — the quantity we are after ($\theta$) and
   the number we actually see ($\hat p$), and why they are not the same thing.
2. **{doc}`Trials and the binomial <02_binomial>`** — where the count comes from: independent yes/no
   trials, and the distribution that governs how many succeed.
3. **{doc}`Sampling variability <03_sampling_variability>`** — run the same experiment twice and get two
   answers. How much do samples wobble, and how fast does the wobble shrink with more data?
4. **{doc}`What a confidence interval really means <04_confidence_interval>`** — the most misunderstood
   idea in statistics, shown by simulation rather than asserted.
5. **{doc}`Coverage — the promise kept or broken <05_coverage>`** — how we *score* a method, and why
   this package is built around measuring it.

## Why there are so many methods

By the last page you will see the tension the whole library exists to manage. Every interval method
trades off two things:

- **{term}`coverage`** — does it trap the true rate as often as it advertises?
- **{term}`expected length`** — how narrow, and therefore how useful, is it?

No single method wins on both for every $n$ and every $\theta$, especially with small samples or when the
rate sits near 0 or 1. `binomcikit` lets you *measure* that trade-off for your own situation instead of
taking a method on faith — which is exactly what these foundations prepare you to do.

```{toctree}
:hidden:
:maxdepth: 1

01_proportion
02_binomial
03_sampling_variability
04_confidence_interval
05_coverage
```
