# Tutorials & cookbook

The rest of the docs explain *what* each method is. These pages show you *doing the job* — real
scenarios, worked start to finish, with the reasoning about which method to reach for and how to report
the answer. Every number is computed live when the docs are built, so you can copy a tutorial and run it
on your own counts.

:::{note}
New to the ideas? The {doc}`Foundations <../foundations/index>` course and the {doc}`method-selection
guide <../method_selection>` are the background these tutorials assume. Each tutorial links back to the
concepts it uses.
:::

## Worked tutorials

1. **{doc}`A/B test: comparing two conversion rates <ab_test>`** — estimate each arm honestly, read the
   overlap, and understand what a single-proportion tool can and cannot tell you about a *difference*.
2. **{doc}`Quality control: is the defect rate below 1%? <quality_control>`** — turn a pass/fail
   question into a posterior probability, and see why a confidence interval and a decision are not the
   same thing.
3. **{doc}`Zero events in n trials: the rule of three <zero_events>`** — what to report when *nothing*
   happened, why Wald gives the useless `[0, 0]`, and where "3/n" comes from.
4. **{doc}`Choosing a method for your own data <choosing_a_method>`** — let `compare` and `recommend` do
   the measuring, and learn to read their tables.

## Cookbook

**{doc}`Copy-paste recipes <cookbook>`** — one-liners for the common tasks: an interval from counts or
from raw data, a posterior probability, a coverage curve, the point estimate, and more.

```{toctree}
:hidden:
:maxdepth: 1

ab_test
quality_control
zero_events
choosing_a_method
cookbook
```
