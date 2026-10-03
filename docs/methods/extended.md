---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Extended methods — 35 more intervals

The original port covers the twelve methods of R's `proportion`. These pages document **35 more**, every
one added from a primary source or a reference implementation and verified against an independent oracle —
a published table, a worked example in the paper, an exact property, or another package. Each is available
through the same call, `bk.ci(x, n, method="<name>")`, and — because every method just produces limits —
works unchanged with {doc}`../evaluating_intervals`, `bk.compare`, `bk.recommend` and the plots.

```{code-cell} python
import binomcikit as bk

bk.list_methods()[["method", "family", "guarantee", "cost"]]
```

That table is **generated from the registry** (`binomcikit.methods`), so it cannot drift from the code.
*guarantee* says what the method promises: `exact` = coverage ≥ 1 − α for every θ, `exact-randomized` =
exactly 1 − α but with a random number, `anytime` = valid at every sample size at once, `local` = the
{term}`locally correct` criterion, `approximate` = coverage near, not guaranteed at, nominal.

## Where to start

| You want… | Use | Why |
|---|---|---|
| a guaranteed interval that is **shorter than Clopper–Pearson** | `"bsc"` or `"sterne"` ({doc}`extended_exact`) | exact coverage, minimal acceptance sets |
| the shortest interval with an honest, *checkable* coverage claim | `"olc"` ({doc}`extended_exact`) | proved smallest average length among {term}`locally correct` intervals |
| near-exact coverage with **no** discreteness machinery | `"lr-star"` ({doc}`extended_approx`) | third-order accurate likelihood |
| a strictly conservative approximation in one line | `"arcsine-anscombe"`, `"score-cc"` ({doc}`extended_approx`) | Pires & Amado's "strictly conservative" group |
| **exactly** 1 − α, even at tiny n (and you accept a coin flip) | `"witting"` ({doc}`extended_exact`) | the only interval that is not conservative anywhere |
| to **peek** at a running experiment | `"mixture"`, `bk.cibetseq` ({doc}`betting`) | {term}`anytime-valid`: no inflation from stopping early |
| the tightest guaranteed interval for bounded data | `"betting"` ({doc}`betting`) | variance-adaptive, Waudby-Smith & Ramdas |
| a distribution-free guarantee with no asymptotics | `"chernoff"`, `"bernstein"` ({doc}`extended_exact`) | concentration bounds — wide but unconditional |
| to audit *any* interval | `bk.locally_correct(n, alpha, method)` ({doc}`extended_exact`) | exact check of the 2024 criterion |

## How each one was verified

```{code-cell} python
rows = [
    ("olc", "all 270 limits of Garthwaite et al.'s Table A1 (95%) and 270 of Table A2 (99%), n = 1…30, to 5e-5"),
    ("sterne", "Dümbgen's published example n=20, x=5 → (0.104, 0.475); brute-force p-value hull"),
    ("bsc", "exact coverage touching 1 − α to four decimals; exactly symmetric; nested in Clopper–Pearson"),
    ("coverage-adjusted", "all 30 rows of Thulin's Table 1 and his worked example n=96, x=4"),
    ("betting", "capital process and limits identical to the authors' `confseq` to 1e-16"),
    ("mixture", "each limit satisfies the mixture-capital equation by independent numerical integration"),
    ("cressie-read", "lam=1 equals Wilson (2e-16); lam=0 equals the likelihood-ratio interval (5e-13)"),
    ("arcsine-anscombe", "reproduces Pires & Amado's 'strictly conservative' classification by exact enumeration"),
    ("witting", "coverage integrates to exactly 1 − α at every θ checked"),
    ("pratt / cloglog", "vs DescTools' formula / vs `pynomial` (a port of R `binom`)"),
]
import pandas as pd
pd.DataFrame(rows, columns=["method", "independent oracle"])
```

Full detail, including **what could not be implemented and why** (Andersson–Nerman's 2024 interval, the
Schilling–Doi LCO, Wang's optimal intervals — primary text not accessible) is in the project's
`planning/MISSING_METHODS.md`.

```{toctree}
:hidden:
:maxdepth: 1

extended_approx
extended_exact
betting
```
