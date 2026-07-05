# User guide

This guide explains the *ideas* behind `binomcikit` — what each family of
methods computes, when to reach for it, and how to read the results. If you just
want the signature of a specific function, jump to the
{doc}`API reference <../api/index>`.

The package mirrors the structure of the statistical problem:

1. **Estimate** the proportion with a confidence interval.
2. **Evaluate** that interval against four criteria — coverage probability,
   expected length, p-confidence / p-bias, and error.
3. Optionally, take a **Bayesian** view.

```{toctree}
:maxdepth: 1

binomial_proportion
choosing_a_method
evaluating_intervals
bayesian
```
