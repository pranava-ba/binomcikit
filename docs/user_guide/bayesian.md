# Bayesian methods

The Bayesian view treats `p` as uncertain and updates a prior belief with the
data. With a `Beta(a, b)` prior and `x` successes in `n` trials, the posterior is
`Beta(x + a, n − x + b)`. `binomcikit` provides the credible interval plus a set
of Bayesian decision tools.

## Credible intervals — `ciba` / `cibax`

`ciba` summarises the posterior two ways:

- a **quantile** (equal-tailed) interval `(LBAQ, UBAQ)`, and
- a **highest-posterior-density (HPD)** interval `(LBAH, UBAH)` — the *shortest*
  interval holding `1 − α` of the posterior mass,

plus the posterior mean.

```python
import binomcikit as bk
bk.ciba(20, 0.05, a=1, b=1)     # uniform Beta(1, 1) prior
```

```{note}
The R package computes the HPD interval with `TeachingDemos::hpd`. Since that has
no Python equivalent, `binomcikit` reimplements it in SciPy (a shortest-interval
search over the Beta posterior). The HPD interval is never wider than the
quantile interval — a property the test suite checks.
```

## Empirical Bayes — `empiricalba`

Instead of fixing the prior, estimate it from the data by maximising the
Beta-Binomial marginal likelihood, then report the resulting credible intervals:

```python
bk.empiricalba(n=5, alp=0.05, sL=0.1, sU=10)
```

## Posterior probabilities — `probpos`

The posterior probability that `p` is below a threshold `th`:

```python
bk.probpos(n=10, a=1, b=1, th=0.5)     # P(p < 0.5 | x) for each x
```

## Posterior predictive — `probpre`

The Beta-Binomial predictive probability of `xnew` future successes in `m` new
trials, given `x` past successes:

```python
bk.probpre(n=3, m=2, a1=1, a2=1)
```

## Bayes factors — `hypotestbaf1` … `hypotestbaf6`

Six formulations weigh a null against an alternative hypothesis about `p`, each
returning the Bayes factor per `x` with a Jeffreys-scale interpretation
("positive / strong / very strong evidence"):

```python
bk.hypotestbaf1(n=5, th0=0.5, a1=1, b1=1)
```

| formulation | compares |
|---|---|
| `baf1` | point null `p = th0` vs a `Beta` alternative |
| `baf2` / `baf3` | one-sided (`p > th0` / `p < th0`) |
| `baf4` / `baf5` | separate priors for null and alternative |
| `baf6` | two interval hypotheses |

Each has an `…x` variant for a single observed `x`.
