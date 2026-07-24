# Methods

One page per confidence-interval method. Each page has two parts — **Use it** (how to call it)
and **Understand it** (the maths behind it) — and links every technical term to the
{doc}`../glossary`. New to the topic? Start with {doc}`../foundations/index`; not sure which to use?
see {doc}`../method_selection`.

## At a glance

| Method | `method=` | Type | In one line |
|---|---|---|---|
| {doc}`Wald <wald>` | `"wald"` | approx. | the textbook interval; a teaching baseline that under-covers |
| {doc}`Wilson (Score) <wilson>` | `"wilson"` | approx. | **the recommended default** — good coverage, never collapses |
| {doc}`ArcSine <arcsine>` | `"arcsine"` | approx. | variance-stabilised; good in the interior, fails at the edges |
| {doc}`Logit-Wald <logit>` | `"logit"` | approx. | on the log-odds scale; stays in (0, 1), mildly conservative |
| {doc}`Wald-T <waldt>` | `"waldt"` | approx. | Wald with a Student-*t* small-sample correction |
| {doc}`Likelihood-ratio <lr>` | `"lr"` | approx. | test-inversion; coverage ≈ Wilson, computed numerically |
| {doc}`Clopper–Pearson <exact>` | `"exact"` | exact | guaranteed coverage ≥ 1 − α, but the widest |
| {doc}`Mid-P <exact>` | `"midp"` | exact | a leaner exact interval (less conservative than CP) |
| {doc}`Blaker <blaker>` ⭐ | `"blaker"` | exact | **new** — the guarantee of CP, but never wider |
| {doc}`Bayesian <bayes>` | `"bayes"` | Bayesian | Beta-posterior credible interval (quantile + HPD) |
| {doc}`Jeffreys <bayes>` | `"jeffreys"` | Bayesian | Bayesian with the Beta(½, ½) prior; excellent coverage |

Agresti–Coull is available as `method="agresti-coull"` (adjusted Wald). The wider Bayesian toolbox
(Bayes factors, empirical Bayes, posterior predictive) has its own page: {doc}`../bayesian_toolbox`.

```{toctree}
:hidden:
:maxdepth: 1

wald
wilson
arcsine
logit
waldt
lr
exact
bayes
blaker
```
