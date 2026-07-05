---
sd_hide_title: true
---

# binomcikit

<div align="center">

# binomcikit

**Inference on a single binomial proportion — confidence intervals, their evaluation, and Bayesian methods.**

[![PyPI](https://img.shields.io/pypi/v/binomcikit?style=flat-square)](https://pypi.org/project/binomcikit/)
[![CI](https://img.shields.io/github/actions/workflow/status/pranava-ba/binomcikit/ci.yml?branch=main&style=flat-square&label=tests)](https://github.com/pranava-ba/binomcikit/actions)
[![Docs](https://img.shields.io/readthedocs/pranava-babinomcikit-rtd?style=flat-square)](https://pranava-babinomcikit-rtd.readthedocs.io/)
[![License](https://img.shields.io/badge/license-GPLv3-blue?style=flat-square)](https://github.com/pranava-ba/binomcikit/blob/main/LICENSE.txt)

</div>

`binomcikit` estimates the proportion of successes *p* in a binomial process and,
crucially, lets you **evaluate** how good an interval is. It is a complete Python
port of the R package
[`proportion`](https://github.com/RajeswaranV/proportion), covering six families
of methods: confidence intervals, coverage probability, expected length,
p-confidence / p-bias, error & failure, and Bayesian inference.

```python
import binomcikit as bk

bk.ciwd(n=20, alp=0.05)    # Wald 95% intervals for every x = 0..20
bk.cisc(n=20, alp=0.05)    # Wilson (Score) — the recommended default
bk.covpwd(n=20, alp=0.05, a=1, b=1, t1=0.9, t2=0.97)   # how often Wald actually covers p
```

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} {octicon}`rocket` Getting started
:link: getting_started
:link-type: doc
Install the package and compute your first interval in under a minute.
:::

:::{grid-item-card} {octicon}`book` User guide
:link: user_guide/index
:link-type: doc
Concepts, method choice, and worked examples — the narrative walkthrough.
:::

:::{grid-item-card} {octicon}`graph` Gallery
:link: gallery
:link-type: doc
See the plotting functions in action, rendered.
:::

:::{grid-item-card} {octicon}`code` API reference
:link: api/index
:link-type: doc
Every public function, with parameters, returns, and examples.
:::

::::

## Why binomcikit?

- **Comprehensive** — six method families with base, adjusted, continuity-corrected, exact and Bayesian variants.
- **Evaluation built in** — not just "compute an interval" but "how well does it cover, how wide is it, where does it fail?"
- **Validated** — checked against `statsmodels` where an independent reference exists, plus golden-value and property tests.
- **Familiar** — pandas `DataFrame` outputs and `plotnine` figures.

```{toctree}
:hidden:
:caption: Get started

getting_started
```

```{toctree}
:hidden:
:caption: Learn

user_guide/index
gallery
```

```{toctree}
:hidden:
:caption: Reference

api/index
migrating_from_r
```

## Indices

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
