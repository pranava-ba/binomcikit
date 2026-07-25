# binomcikit

```{raw} html
<div style="text-align:center; margin-bottom:1.5rem">
  <p style="font-size:1.15rem"><strong>Inference on a single binomial proportion — confidence intervals, their evaluation, and Bayesian methods.</strong></p>
  <p>
    <a href="https://pypi.org/project/binomcikit/"><img alt="PyPI" src="https://img.shields.io/pypi/v/binomcikit?style=flat-square"></a>
    <a href="https://github.com/pranava-ba/binomcikit/actions"><img alt="tests" src="https://img.shields.io/github/actions/workflow/status/pranava-ba/binomcikit/ci.yml?branch=main&amp;style=flat-square&amp;label=tests"></a>
    <a href="https://pranava-babinomcikit-rtd.readthedocs.io/"><img alt="Docs" src="https://img.shields.io/readthedocs/pranava-babinomcikit-rtd?style=flat-square"></a>
    <a href="https://github.com/pranava-ba/binomcikit/blob/main/LICENSE.txt"><img alt="License" src="https://img.shields.io/badge/license-GPL-blue?style=flat-square"></a>
  </p>
</div>
```

`binomcikit` estimates the proportion of successes *p* in a binomial process and — crucially — lets you
**evaluate** how good an interval is. It is a complete Python port of the R package
[`proportion`](https://github.com/RajeswaranV/proportion), extended with the exact **Blaker** interval
and a modern access layer.

```python
import binomcikit as bk

bk.ci(x=3, n=20)                      # Wilson (Score) 95% interval — the default
bk.ci(x=3, n=20, method="blaker")     # exact, never wider than Clopper–Pearson
bk.compare(x=3, n=20)                  # every method's interval, side by side
bk.plot_coverage(n=20, methods=["wald", "wilson", "blaker"])
```

## Where to go next

::::{grid} 1 2 2 3
:gutter: 3

:::{grid-item-card} {octicon}`rocket` Getting started
:link: getting_started
:link-type: doc
Install and compute your first interval in under a minute.
:::

:::{grid-item-card} {octicon}`mortar-board` Foundations
:link: foundations/index
:link-type: doc
Probability from zero — proportions, trials, and coverage, with no maths.
:::

:::{grid-item-card} {octicon}`list-unordered` Choosing a method
:link: method_selection
:link-type: doc
Which of the twelve intervals to use, and why.
:::

:::{grid-item-card} {octicon}`beaker` Methods
:link: methods/index
:link-type: doc
One page per interval — *Use it* and *Understand it*.
:::

:::{grid-item-card} {octicon}`checklist` Tutorials
:link: tutorials/index
:link-type: doc
Worked scenarios: A/B tests, quality control, zero events, choosing a method.
:::

:::{grid-item-card} {octicon}`sync` The Bayesian toolbox
:link: bayesian_toolbox
:link-type: doc
Credible intervals, Bayes factors, empirical Bayes, prediction.
:::

:::{grid-item-card} {octicon}`code` API reference
:link: api/index
:link-type: doc
Every public function, with parameters and returns.
:::

::::

## Why binomcikit?

- **Comprehensive** — twelve interval methods with base, adjusted, continuity-corrected, exact and Bayesian variants.
- **Evaluation built in** — not just "compute an interval" but "how well does it cover, how wide is it, where does it fail?"
- **Validated** — checked against `statsmodels` where an independent reference exists, plus golden-value and property tests; the new Blaker interval is verified against its defining theorems.
- **Modern & familiar** — pandas `DataFrame` outputs, interactive Plotly figures, and a `from_data` / `compare` / `recommend` access layer the R original lacks.

```{toctree}
:hidden:
:caption: Start here

getting_started
foundations/index
```

```{toctree}
:hidden:
:caption: Guides

method_selection
evaluating_intervals
bayesian_toolbox
access_layer
gallery
```

```{toctree}
:hidden:
:caption: Tutorials

tutorials/index
```

```{toctree}
:hidden:
:caption: Methods

methods/index
```

```{toctree}
:hidden:
:caption: The maths

theory/index
```

```{toctree}
:hidden:
:caption: Reference

api/index
glossary
migrating_from_r
under_the_hood
```
