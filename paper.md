---
title: "binomcikit: confidence intervals, evaluation metrics and planning for a binomial proportion in Python"
tags:
  - Python
  - statistics
  - binomial proportion
  - confidence intervals
  - coverage probability
authors:
  - name: Vyasa R Rajeswaran
    orcid: 0009-0005-5912-8804
    equal-contrib: true
    affiliation: 1
  - name: Pranava BA
    orcid: 0009-0003-5883-8949
    equal-contrib: true
    affiliation: 1
  - name: Justindhas Y
    orcid: 0000-0003-0296-2206
    equal-contrib: true
    corresponding: true
    affiliation: 2
affiliations:
  - name: Second Year BE CSE (AIML), Easwari Engineering College, Chennai, India
    index: 1
  - name: Head of Department, CSE (AIML), Easwari Engineering College, Chennai, India
    index: 2
date: 3 October 2026
bibliography: paper.bib
---

<!--
DRAFT revised 2026-10-03 for the authors to review; nothing here has been submitted.
To confirm before submission: (1) the AI-usage statement at the end; (2) the version number and archive DOI
(the package has not been released since 0.0.5 on PyPI); (3) that the claims about other packages still hold at submission
(planning/COMPETITOR_REPOS.md has the dated measurements); (4) the primary-source checks still open in
planning/PAPERS_TO_DOWNLOAD.md. The earlier text claimed Python had no dedicated package for this problem; that is not true
(see State of the field) and has been removed.
-->

# Summary

A binomial proportion (a conversion rate, a defect rate, a response rate) is estimated by $\hat p = x/n$, and its uncertainty is reported as an
interval. More than a dozen interval constructions are in use, and they differ most where it matters: small $n$, proportions near 0 or 1, and the
requirement that the stated confidence level actually be achieved. `binomcikit` is a Python package that implements 48 single-proportion interval
methods and 12 methods for the difference of two proportions, and evaluates any of them: coverage probability, expected length, p-confidence and
p-bias, error and failure rates, and a check against the locally-correct criterion [@Garthwaite2024]. It also provides Bayesian tools, anytime-valid
(betting) intervals [@WaudbySmith2024], and sample-size, width and power planning. It began as a port of the R package `proportion` [@Subbiah2017]
and has since been extended well beyond it.

# Statement of need

Choosing an interval is a quantitative question: the classical Wald interval can have true coverage far below its nominal level
[@Brown2001], the exact Clopper–Pearson interval [@Clopper1934] is conservative, and Wilson's score interval [@Wilson1927] sits between them,
with the ranking changing with $n$ and $p$. Analysts need to see those properties for *their* $n$, not take them on trust. In R this has long been
possible; in Python the commonly used tools (SciPy [@Virtanen2020], statsmodels [@Seabold2010]) return an interval and nothing more.
`binomcikit` is for people who need to choose, justify or audit an interval, for example in clinical reporting, quality control, A/B testing and
evaluation of machine-learning systems, where a zero-failure plan or an always-valid interval is the actual question.

# State of the field

Python is not empty here. SciPy's `binomtest(...).proportion_ci` offers 3 intervals and statsmodels' `proportion_confint` 6.
The package DBCI [@DBCI] offers 16 distinct single-proportion methods and 15 for the difference of two proportions, including Blaker's interval
[@Blaker2000] and Pratt's approximation. `binomial_cis` [@binomialcis] computes optimal randomised exact intervals, and `confseq` [@confseq] is
the reference implementation of betting confidence sequences. None of them evaluates an interval (coverage, length, p-confidence, error), and none puts classical, exact, Bayesian and betting methods
under one set of diagnostics; statsmodels has sample-size and power helpers, but for normal-approximation tests and Wald widths only. We built `binomcikit` rather than
contribute to one of them because the evaluation layer is the product, and it needs every method to expose the same table of limits.

# Software design

Every method returns the same table: the lower and upper limit for each possible count $x = 0,\dots,n$, with flags marking limits that left $[0,1]$
before clamping (`LABB`, `UABB`) and zero-width intervals (`ZWI`). Because that table is all the evaluation needs, one metric engine computes
coverage, expected length, p-confidence and p-bias, and error for *any* method, including user-supplied limits. A registry (`list_methods()`) holds
the 35 methods beyond the original 13, and each is reachable through one dispatcher, `ci(method=...)`. A lean path (`limits`, `interval`) returns
bare arrays or floats for loops and simulations. The numerical core is NumPy and SciPy, with vectorised root-finding on the deviance (never the raw
likelihood, which underflows at large $n$); numba is an optional accelerator, and plotting is optional and loaded on first use.

# Verification and performance

Correctness is checked against independent sources, not only against itself (\autoref{tab:verification}); the package's own mistakes found this
way were fixed, for example a single-root search in the Blaker interval that could return an inner crossing and under-cover.

| Check | Result |
|---|---|
| Wilson and Clopper–Pearson against a 30-digit reference (19 cases, $n \le 10^5$) | max error $2.2\times10^{-16}$ |
| Single-proportion methods against R `DescTools::BinomCI` output at 84/101 | agree to $10^{-6}$ ($10^{-4}$ for root-found methods, R's `uniroot` tolerance) |
| Difference of two proportions against Newcombe's Table II and SAS output (12 methods, 9 tables) | 88 of 88 intervals reproduced to the 4 printed decimals |
| Score intervals (Mee, Miettinen–Nurminen) | solve their defining equation to $\sim10^{-15}$ |
| Test suite | 1,465 tests run (516 parametrised cases skipped as not applicable), 84.7% branch coverage; property tests tie `limits`, `interval` and `ci` together |

: Verification against independent sources. {#tab:verification}

For performance we compared whole-table construction (all $n+1$ intervals) with SciPy, statsmodels, astropy and DBCI on one machine
(`benchmarks/`, re-runnable). Against packages that return one interval per call, the speed-up is two to four orders of magnitude (e.g. 28 µs
versus 89 ms for DBCI's Wilson table at $n = 1000$). Against vectorised packages the picture is mixed: the lean path is 2 to 7 times faster than
statsmodels at $n \le 10^4$, equal to slightly slower for Wilson at $n = 10^6$, and about twice as fast for the exact interval at $10^6$; the
`DataFrame`-returning `ci()` is slower than statsmodels for closed-form methods at small $n$. We report this rather than a single headline number.

# Acknowledgements

We acknowledge support from The Principal, Dr Deiva Sundari, the department of CSE(AIML), Dr A Joseph Anburaj, Mr K Kadhiravan and Mrs S Leelavathi
from the Central Library during the genesis of this project.

# AI usage disclosure

<!-- Authors: confirm and edit. The development repository records the use of an AI coding assistant. -->
AI coding assistance (Claude, via Claude Code) was used during development of the code, tests, documentation and this manuscript's revision.
The authors reviewed the results and are responsible for the content; the verification table above compares against independent sources rather
than against AI output.

# References
