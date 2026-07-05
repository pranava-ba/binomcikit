# Getting started

## Installation

```bash
pip install binomcikit
```

`binomcikit` requires Python ≥ 3.9 and depends on `numpy`, `pandas`, `scipy`, and
`plotnine` (for the plotting functions).

## Your first interval

Suppose you ran 20 trials and want confidence intervals for the true proportion
*p* at every possible number of successes:

```python
import binomcikit as bk

bk.ciwd(20, 0.05)      # Wald 95% intervals, one row per x = 0..20
```

Each function returns a pandas `DataFrame`. For the confidence-interval methods
the columns are the lower/upper limits plus three diagnostic flags:

| column | meaning |
|---|---|
| `LWD`, `UWD` | lower / upper interval limits (column names vary by method) |
| `LABB` | `"YES"` if the lower limit was clamped up to 0 |
| `UABB` | `"YES"` if the upper limit was clamped down to 1 |
| `ZWI` | `"YES"` for a zero-width interval |

To report the interval for a **single** observed count, use the `…x` variant:

```python
bk.ciwdx(2, 20, 0.05)      # just x = 2 of 20
```

## Evaluating a method

The real power of the package is evaluation. For example, how often does the
Wald interval actually contain the true proportion (its *coverage*)?

```python
bk.covpwd(n=20, alp=0.05, a=1, b=1, t1=0.9, t2=0.97, seed=0)
#    mcp    micp   RMSE_N ...   <- mean / minimum coverage, etc.
```

Compare that to the Wilson (Score) interval — you'll see Wald under-covers:

```python
bk.covpsc(n=20, alp=0.05, a=1, b=1, t1=0.9, t2=0.97, seed=0)
```

## The naming convention

With ~300 functions, the names follow a strict scheme so you can guess them.

**Confidence intervals** start with `ci`, then a method code:

| code | method |
|---|---|
| `wd` | Wald |
| `sc` | Score (Wilson) |
| `as` | ArcSine |
| `lr` | Likelihood-Ratio |
| `lt` | Logit-Wald |
| `tw` | Wald-T |
| `ex` | Exact (Clopper–Pearson / mid-p) |
| `ba` | Bayesian |
| `all` | all methods at once |

**Modifiers** attach around the method code:

| modifier | where | example |
|---|---|---|
| adjusted (add pseudo-counts) | `a` after `ci` | `ciawd` |
| continuity-corrected | `c` after `ci` | `cicwd` |
| single given `x` | `x` suffix | `ciwdx`, `ciawdx` |
| plot it | `plot` prefix | `plotciwd` |

The **evaluation families** reuse the same method codes with a different prefix:
`covp*` (coverage), `length*` / `expl*` (expected length), `pcopbi*`
(p-confidence & p-bias), `err*` (error & failure), and the Bayesian tools live in
`binomcikit.bayes`.

See the {doc}`user guide <user_guide/index>` for what these mean and when to use
each, or the {doc}`API reference <api/index>` for every function.
