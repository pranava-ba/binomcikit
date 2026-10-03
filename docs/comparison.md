---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# binomcikit vs statsmodels, scipy & R

If you already reach for `scipy` or `statsmodels`, this page shows exactly where `binomcikit` overlaps
with them (and gives the *same* numbers), and where it does more. The short answer: for a single
binomial proportion, `binomcikit` is the most complete of the four — it is a full port of R's
`proportion` package plus an evaluation layer none of the others has.

*Not sure which method you want at all?* Read {doc}`method_selection` first. This page is about which
*library*.

---

## The short version

| | **scipy** | **statsmodels** | **R `proportion`** | **binomcikit** |
|---|---|---|---|---|
| Confidence-interval methods | 3 | 6 | 12 | **47** ({doc}`methods/index`, {doc}`methods/extended`) |
| Evaluate an interval (coverage, length, p-confidence, error) | — | — | ✅ | ✅ |
| Audit an interval against the *locally correct* criterion (2024) | — | — | — | ✅ |
| Exact **Blaker / Sterne / Blyth–Still–Casella / OLC** | — | — | Blaker ✗ | ✅ |
| Difference of two proportions | — | 4 methods (`confint_proportions_2indep`) | — | 7 methods ({doc}`methods/two_proportions`) |
| Anytime-valid / betting confidence sequences | — | — | — | ✅ |
| PASS / SAS-style sample size, width & power planning | — | partial | — | ✅ ({doc}`planning`) |
| Bayesian toolbox (credible intervals, Bayes factor, prediction) | partial | — | partial | ✅ |
| Lean `(lower, upper)` array / float API | ✅ | ✅ | — | ✅ (`bk.limits`, `bk.interval`) |
| `from_data` / `compare` / `recommend` access layer | — | — | — | ✅ |
| Interactive Plotly figures | — | — | — | ✅ |
| Language | Python | Python | R (archived 2022) | Python |

`scipy.stats.binomtest(...).proportion_ci` offers Clopper–Pearson (`exact`) and Wilson; `statsmodels`'
`proportion_confint` adds Wald, Agresti–Coull and Jeffreys. `binomcikit` covers all of those **and**
{doc}`ArcSine <methods/arcsine>`, {doc}`Logit <methods/logit>`, {doc}`Wald-T <methods/waldt>`,
{doc}`likelihood-ratio <methods/lr>`, {doc}`Mid-P <methods/exact>` and the exact
{doc}`Blaker <methods/exact>` interval — each with base, adjusted and continuity-corrected variants.

---

## Same method, same number

Where the libraries implement the *same* interval, they agree to the printed digits — that is how you
know `binomcikit` is computing the textbook quantity and not a private variant. The cell below runs
`binomcikit` and `scipy` side by side (both ship in the docs build, so these numbers are live):

```{code-cell} python
import binomcikit as bk
from scipy.stats import binomtest

cmp = bk.compare(x=3, n=20).set_index("method")[["lower", "upper"]].round(4)
r = binomtest(3, 20)
scipy_wilson = tuple(float(round(v, 4)) for v in r.proportion_ci(method="wilson"))
scipy_exact  = tuple(float(round(v, 4)) for v in r.proportion_ci(method="exact"))

print("Wilson           binomcikit", tuple(cmp.loc["Wilson"]),          " scipy", scipy_wilson)
print("Clopper–Pearson  binomcikit", tuple(cmp.loc["Clopper-Pearson"]), " scipy", scipy_exact)
```

`statsmodels` is not installed in the docs environment, so its line is shown statically — but the
values were checked and match exactly:

```python
from statsmodels.stats.proportion import proportion_confint

proportion_confint(3, 20, alpha=0.05, method="normal")         # Wald    -> (0.0000, 0.3065)
proportion_confint(3, 20, alpha=0.05, method="wilson")         # Wilson  -> (0.0524, 0.3604)
proportion_confint(3, 20, alpha=0.05, method="beta")           # CP      -> (0.0321, 0.3789)
proportion_confint(3, 20, alpha=0.05, method="jeffreys")       # Jeffreys-> (0.0441, 0.3486)
```

Every one of those matches `binomcikit`'s `ci(x=3, n=20, method=...)` for the corresponding method.

---

## What binomcikit adds

### More intervals, as first-class methods

The methods below are either missing from `scipy`/`statsmodels` or only reachable indirectly.
`binomcikit` exposes each with the same `ci(..., method=...)` call and the same diagnostic flags:

```{code-cell} python
bk.compare(x=3, n=20)[["method", "lower", "upper", "width"]]
```

`ArcSine`, `Logit`, `Wald-T`, `Likelihood-ratio`, `Mid-P` and `Blaker` are the six you won't find as
one-line calls elsewhere in Python. **Blaker** in particular is exact (guaranteed
{term}`coverage`) yet never wider than Clopper–Pearson — see {doc}`theory/04_exact_and_discreteness`.

### An evaluation layer — the real differentiator

`scipy` and `statsmodels` hand you an interval and stop. `binomcikit` also answers *how good is it?* —
the whole {doc}`evaluating_intervals` family. No other Python library computes true coverage,
expected length, p-confidence/p-bias and long-run error for these methods:

```{code-cell} python
bk.recommend(n=30, by="length").head(4)
```

That table ranks every method for `n = 30` by expected length among those with adequate coverage —
something you would otherwise have to simulate by hand.

### A Bayesian toolbox and a modern access layer

`binomcikit` also gives you {term}`credible interval`s, {term}`Bayes factor`s and
{term}`posterior predictive` checks (the {doc}`Bayesian toolbox <bayesian_toolbox>`), and a
`from_data` / `compare` / `recommend` {doc}`access layer <access_layer>` that the R original and the
other Python libraries lack.

---

## Every tool we could find — and what each does

Verified 2026-10-01 against the linked documentation (✓) unless marked ○ (not re-checked). "CI methods" counts distinct
intervals for **one binomial proportion**.

### Python

| Package | CI methods | Evaluation layer | Planning | Notes |
|---|---|---|---|---|
| **binomcikit** | **47** | ✅ coverage, length, p-conf/bias, error, locally-correct | ✅ PASS/SAS-style | all verified against independent oracles |
| [`statsmodels`](https://www.statsmodels.org/dev/generated/statsmodels.stats.proportion.proportion_confint.html) ✓ | 6 (normal, Agresti–Coull, Clopper–Pearson, Wilson, Jeffreys, binom_test) | — | `samplesize_confint_proportion` (Wald) | the de-facto default |
| [`scipy`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html) ✓ | 3 (exact, Wilson, Wilson-cc) | — | — | |
| `astropy.stats.binom_conf_interval` ✓ | 4 (Wilson, Jeffreys, flat, Wald) | — | — | no exact interval |
| [`DBCI`](https://github.com/DeepPSP/DBCI/) ✓ | 16 incl. Blaker, Pratt, Witting, Mid-P, modified-\*; **plus 15 two-proportion methods** (binomcikit has 7) | tests vs SAS/PASS/DescTools | — | Streamlit app; **defects found** ({doc}`methods/extended_approx`) |
| [`binomial_cis`](https://github.com/TRI-ML/binomial_cis) ✓ | randomised UMA/UMAU exact | — | — | JOSS pre-review closed ("uncertain scope") |
| `pynomial` (GitHub; *not* the PyPI package of that name) ✓ | 9 (port of R `binom`) | — | — | |
| [`confseq`](https://pypi.org/project/confseq/) ✓ | betting / confidence sequences | — | — | C++ build; fails to build on Windows here |
| `binoculars`, `evalci`, `ebcic` ✓ | 3–4 each | — | — | small utilities; `binoculars`' "wilson" is not Wilson's interval |

### R

| Package | CI methods | Evaluation | Planning |
|---|---|---|---|
| [`binom`](https://www.rdocumentation.org/packages/binom/versions/1.1-1.1/topics/binom.confint) ✓ | 11 | `binom.coverage`, `binom.length` | — |
| [`DescTools::BinomCI`](https://search.r-project.org/CRAN/refmans/DescTools/html/BinomCI.html) ✓ | 16 | — | — |
| `PropCIs`, `exactci`, `rbscCI` ✓ | Blaker/Mid-P/Add-4; Sterne/Blaker; Blyth–Still–Casella | — | — |
| [`binGroup`](https://search.r-project.org/CRAN/refmans/binGroup/html/binCI.html) ✓ | 6 (CP, Blaker, AC, Score, Wald, SOC) | `binWidth` | `binDesign` |
| [`binomCI`](https://cran.r-universe.dev/binomCI/doc/manual.html) ✓ (CRAN, 2026) | 12 | — | — |
| `proportion` ✓ (archived 2022) | 12 | **full** | — |

### Commercial and desktop

| Product | CI methods for one proportion | Planning |
|---|---|---|
| [SAS `PROC FREQ`](https://documentation.sas.com/doc/en/procstat/9.4/procstat_freq_details37.htm) ✓ | 9 (Wald, exact, Agresti–Coull, Blaker, Jeffreys, mid-P, LR, logit, Wilson) | `PROC POWER ONESAMPLEFREQ`: CI precision (6 CIs, `HALFWIDTH`/`PROBWIDTH`), exact / z / adjusted-z tests, TOST equivalence |
| [NCSS PASS](https://www.ncss.com/software/pass/one-proportion-in-pass/) ✓ | 5 (exact, score, score-cc, Wald, Wald-cc) | sample size & width, dropout |
| [Stata `cii`](https://www.stata.com/manuals13/rci.pdf) ✓ | 5 (exact, Wald, Wilson, Agresti–Coull, Jeffreys) | `power oneproportion` ○ |
| [MATLAB `binofit`](https://www.mathworks.com/matlabcentral/answers/47944-confidence-interval-using-binofit) ✓ | 1 (Clopper–Pearson) | — |
| Minitab *1-Proportion* ✓ | 2 (normal, exact) | power & sample size ○ |
| [GraphPad Prism](https://graphpad.com/guides/prism/latest/statistics/stat_three_methods_for_computing_th.htm) ✓ | 3 (exact, Wilson, Wilson/Brown) | — |
| SPSS `NPTESTS` binomial ✓ | a limited set (Clopper–Pearson, Jeffreys, Wald-type) | — |
| [MedCalc](https://www.medcalc.org/en/manual/diagnostic-test.php) ✓ | exact (sens/spec), logit (predictive values) | sample size for a CI ✓ |
| [OpenEpi](https://en.wikipedia.org/wiki/OpenEpi) ✓ | 6 | — |
| StatXact (Cytel) ○ | exact incl. Blyth–Still–Casella (referenced by `rbscCI`) | — |
| JMP, nQuery, Epi Info ○ | not verified in this pass | |

**What no tool in these tables does** is combine the interval zoo with a measured *evaluation* of each interval, the 2024 locally-correct
criterion, anytime-valid intervals and PASS/SAS-parity planning in one place. That — not any single method — is the contribution.

---

## When to use which

| Your situation | Reach for |
|---|---|
| You just need one Wilson or exact interval, fast, and already import `scipy` | **scipy** — `binomtest(...).proportion_ci` |
| You want Wald / Agresti–Coull / Jeffreys and are already in `statsmodels` | **statsmodels** — `proportion_confint` |
| You need to **choose** a method, or justify one, by its coverage/length behaviour | **binomcikit** — `recommend`, `covp*`, `length*` |
| You need ArcSine, Logit, Wald-T, LR, Mid-P, or exact **Blaker** | **binomcikit** |
| You want frequentist *and* Bayesian answers from one API | **binomcikit** |
| You are porting or reproducing R `proportion` results | **binomcikit** (built for parity — see {doc}`migrating_from_r`) |

The honest summary: use `scipy`/`statsmodels` when you want *one* standard interval with minimal
imports; use `binomcikit` when the *choice* of interval, or its *evaluation*, is part of the job.

---

:::{admonition} Terms used on this page
:class: seealso
{term}`proportion` · {term}`coverage` · {term}`expected length` · {term}`credible interval` ·
{term}`Bayes factor` · {term}`posterior predictive` · {term}`Clopper–Pearson` · {term}`Mid-P`
:::
