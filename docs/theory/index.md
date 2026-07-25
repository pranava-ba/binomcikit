# Methods & Mathematics

A ground-up explanation of the statistics behind `binomcikit`. Where the
{doc}`user guide <../evaluating_intervals>` tells you *which* method to reach for, this
series explains *why each method is built the way it is* — the formula, the idea
behind it, and the way it succeeds or fails.

The material follows the structure of the underlying paper, Subbiah &
Rajeswaran (2017), *"proportion: A comprehensive R package for inference on
single Binomial proportion and Bayesian computations"* (SoftwareX 6, 36–41),
which `binomcikit` ports to Python.

Read it in order — each page builds on the one before — or jump to the topic you
need. The arc runs from the estimation problem, through the four families of
interval (normal-approximation, test-inversion, exact, and transformed), to the
Bayesian view, and closes with a chapter on coverage itself — what all the
oscillating curves really mean.

```{toctree}
:maxdepth: 1

01_the_problem
02_normal_approximation
03_test_inversion
04_exact_and_discreteness
05_transformed_intervals
06_bayesian_view
07_coverage_theory
```
