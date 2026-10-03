# Methods binomcikit did not have â€” exhaustive catalogue, status and evidence

> Written 2026-10-01. Answers: *"what methods do we not have, and add all of them."*
> Every entry says **where the method comes from**, **where it already exists elsewhere**, **whether it is
> now in binomcikit**, and **how it was verified** (or, if it is not implemented, exactly why not).
> Nothing here was implemented from memory: each construction was transcribed from a primary source or
> from the reference R/Python source code, and checked against an *independent* oracle (a published table,
> a worked example in the paper, an exact property, or another package) before it was accepted.

## 0. How the list was built

The union of every method named by the standard comparative reviews and by the software that implements them:

| Source | What it contributed |
|---|---|
| Vollset (1993), *Stat. Med.* 12 â€” 17 methods | Wald-I and its continuity variants, Pratt, Blythâ€“Still |
| Newcombe (1998), *Stat. Med.* 17 â€” 7 methods | Score-cc (method 4), Wald-cc |
| Agresti & Coull (1998); Brown, Cai & DasGupta (2001) â€” 12 methods | Modified Wilson / Jeffreys, Add-4 |
| **Pires & Amado (2008), *REVSTAT* 6 â€” 20 methods** (read in full, Tables 1â€“2) | Wald-I(+cc), recentred Wald-I(+cc), analytic bootstrap Ã—4, arcsine-cc-Anscombe, Score-cc |
| R: `binom`, `PropCIs`, `DescTools`, `Hmisc`, `binGroup`, `exactci`, `rbscCI`, **`binomCI` (CRAN 2026)** | cloglog, probit, Pratt, Witting, SOC, Sterne (`minlike`), Blythâ€“Stillâ€“Casella |
| Python: `statsmodels`, `scipy`, `astropy`, `pynomial`, `binoculars`, **`DBCI`**, **`binomial_cis`**, `confseq` | what the Python competition covers |
| 2012â€“2025 papers: Thulin (2014), Decrouez & Hall (2014), Howard et al. (2021), Garthwaite et al. (2024), Waudby-Smith & Ramdas (2024), Andersson & Nerman (2024) | the modern methods |

**Baseline.** The original port had 13 named methods (Wald, Wilson, ArcSine, Logit, Wald-T, LR, Clopperâ€“Pearson,
Mid-P, Bayes/Jeffreys, Agrestiâ€“Coull, Blaker, smooth/percentile/BCa bootstrap) with adjusted (`h`) and
continuity-corrected (`c`) variants. **This batch adds 34 interval methods (47 in total), a streaming
confidence-sequence tool, one evaluation criterion and a planning layer.**

Status legend: âœ… implemented and verified Â· â— implemented, with a documented caveat Â· âŒ not implemented (reason given).

---

## 1. Closed-form, transformed and corrected approximations

| # | Method (`method=`) | Source | Already elsewhere | Status | Verification |
|---|---|---|---|---|---|
| 1 | **Pratt** `"pratt"` | Pratt 1968, JASA 63 | R `DescTools`; Py `DBCI` | âœ… | Upper limit = the DescTools formula (transcribed); tracks exact Clopperâ€“Pearson to **â‰¤ 9Â·10â»â´** (n=20), 2Â·10â»â´ (n=100). **Defect found upstream:** `DescTools::BinomCI(method="pratt")` (and `DBCI`, which copies it) has a lower-limit formula that drifts from exact CP by **up to 0.126** at n=20 for x near n, and non-exact boundary rows. binomcikit mirrors the (accurate) upper formula; the discrepancy is pinned by a test. |
| 2 | **Complementary log-log** `"cloglog"` | R `binom` | R `binom`; Py `pynomial` | âœ… | Equals `pynomial.cloglog` (the GitHub port of R `binom`) to 1e-12 for every x. |
| 3 | **Probit** `"probit"` | R `binom` | R `binom` | âœ… | Delta-method derivation test; boundary rows are the exact closed forms. |
| 4 | **Modified Wilson** `"modified-wilson"` | Brownâ€“Caiâ€“DasGupta 2001 | R `DescTools`; Py `DBCI` | âœ… | Semantics transcribed from the DescTools R source (it uses the full Î± in the Ï‡Â² quantile). **`DBCI`'s version has two defects:** it uses Î±/2 in the Ï‡Â² quantile (so it disagrees with DescTools), and its **upper** limit for x â‰¥ nâˆ’3 omits the `1 âˆ’` â€” at n=60, x=59 it returns an upper limit of 0.0004 *below* its own lower limit 0.9114. binomcikit follows the R source. |
| 5 | **Modified Jeffreys** `"modified-jeffreys"` | Brownâ€“Caiâ€“DasGupta 2001 | R `DescTools`; Py `DBCI` | âœ… | Boundary-row rules from the DescTools source. |
| 6 | **Garwood (Poisson)** `"poisson"` | Garwood 1936 | â€” (as a binomial CI) | âœ… | Ï‡Â² formula test; conservative upper limit vs CP verified. |
| 7 | **Freemanâ€“Tukey double-arcsine** `"freeman-tukey"` | Freeman & Tukey 1950; Miller 1978 | R `meta`/`metafor` transforms | â— | Inverted numerically on the count scale (not Miller's closed-form back-transform); round-trip tested. Known to under-cover at x=0. |
| 8 | **Second-order corrected (SOC)** `"soc"` | Cai 2005, JSPI 131 | R `binGroup` | â— | Ported from `binGroup::binSOC`; Cai's primary text not independently re-read. |
| 9 | **Score + continuity (Newcombe 4)** `"score-cc"` | Newcombe 1998; Pires & Amado IV | SAS/PASS (â€œscore with continuity correctionâ€) | âœ… | Equals the Pires Table-1 formula **and** the PASS Chapter-115 formula (two independent transcriptions agree to 1e-12). The original `cicsc` port leaves the boundary rows uncorrected (coverage â†’ 0 as Î¸ â†’ 0); this one fixes them. |
| 10 | **Wald-I** `"wald-i"`, **Wald-I + cc** `"wald-i-cc"` | Vollset 1993; Pires & Amado VII/VIII | â€” | âœ… | Scalar re-transcription of Table 1. |
| 11 | **Recentred Wald-I** `"wald-recentred"`, **+ cc** | Brownâ€“Caiâ€“DasGupta 2002; Pires & Amado IX/X | â€” | âœ… | Scalar re-transcription of Table 1. |
| 12 | **Arcsine-cc-Anscombe** `"arcsine-anscombe"` | Anscombe 1948; Pires & Amado XVII | â€” | âœ… | Table 2 transcribed literally (a `clamp=True` option monotonises the two boundary-adjacent rows). **Reproduces the paper's finding:** strictly conservative (min coverage 0.952â€“0.962 for n â‰¥ 10; their Group 1), at essentially Clopperâ€“Pearson's length. |
| 13 | **Analytic percentile bootstrap** `"analytic-percentile"` (+ `-cc`) | Pires & Amado XI/XII | â€” | âœ… | The bootstrap law is *exactly* Binomial(n, x/n): Monte-Carlo quantiles agree within 1/n. No resampling, no seed. |
| 14 | **Analytic bias-corrected percentile** `"analytic-bcp"` (+ `-cc`) | Pires & Amado XIII/XIV | â€” | âœ… | Scalar re-transcription of eqs. (2.5)â€“(2.6). |
| 15 | **Cressieâ€“Read power-divergence** `"cressie-read"` (`lam=`) | Cressie & Read 1984 | â€” | âœ… | **Identities, not approximations:** `lam=1` equals Wilson (2e-16) and `lam=0` equals the existing LR interval (5e-13); every limit solves its statistic = zÂ². Contains Freemanâ€“Tukey at `lam=-Â½`. |
| 16 | **Higher-order likelihood r\*** `"lr-star"` | Barndorff-Nielsen 1986 | R `likelihood`/`hoa` (not as a binomial CI) | âœ… | Limits solve r\* = Â±z (tested); mean coverage within 0.012 of nominal at n=40 (third-order accuracy). |

## 2. Non-asymptotic (concentration) intervals â€” guaranteed coverage, no asymptotics

| # | Method | Source | Elsewhere | Status | Verification |
|---|---|---|---|---|---|
| 17 | **Hoeffding** `"hoeffding"` | Hoeffding 1963 | folklore | âœ… | Exact enumeration: coverage â‰¥ 1âˆ’Î± for every Î¸ at n = 8, 20, 40. |
| 18 | **Chernoffâ€“KL** `"chernoff"` | Chernoff 1952; Garivier & CappÃ© 2011 | bandit libraries | âœ… | Limits satisfy nÂ·KL = ln(2/Î±); never wider than Hoeffding; coverage guaranteed. |
| 19 | **Bernstein** `"bernstein"` | Bernstein 1924 | â€” | âœ… | Closed form (a convex quadratic); the defining inequality holds with equality at each limit. |
| 20 | **Empirical Bernstein** `"empirical-bernstein"` | Maurer & Pontil 2009, Thm 4 | â€” | â— | Coverage guaranteed (verified); very conservative at small n. Constants taken from the theorem statement; recheck against the COLT paper before citing. |

## 3. Exact and optimal-exact intervals

| # | Method | Source | Elsewhere | Status | Verification |
|---|---|---|---|---|---|
| 21 | **Sterne (minlike)** `"sterne"` | Sterne 1954; DÃ¼mbgen 2021 (arXiv:2111.12937) | R `exactci` (`tsmethod="minlike"`) | âœ… | DÃ¼mbgen's published example n=20, x=5 â†’ **(0.104, 0.475)**: ours (0.1041, 0.4746). Equals a brute-force 60 001-point hull of the p-value for n=8, 11; min coverage 0.95000. |
| 22 | **Blythâ€“Stillâ€“Casella** `"bsc"` | Blyth & Still 1983; Casella 1986 | R `rbscCI`; StatXact | âœ… | Literal port of the `rbscCI` refinement algorithm. Min coverage touches **1âˆ’Î± to 4 decimals** (0.95000), exactly symmetric, âŠ† Clopperâ€“Pearson. No third-party numeric oracle (R is not installed here) â€” verified by its defining property. |
| 23 | **Optimal locally correct (OLC)** `"olc"` | Garthwaite, Moustafa & Elfadaly 2024 | Shiny app only | âœ… | **All 270 limits of the paper's Table A1 (95%) and all 270 of Table A2 (99%), n = 1â€¦30, agree to â‰¤ 5Â·10â»âµ** (their 4-decimal rounding). Per-cycle average coverage equals 1âˆ’Î±/2 exactly (quadrature). |
| 24 | **Witting / Stevens (randomised UMA)** `"witting"` (`"stevens"`) | Witting 1985; Stevens 1950; Blank 1956 | R `DescTools`; Py `DBCI`, `binomial_cis` (UMAU variant) | âœ… | Averaged over the uniform draw the coverage is **exactly 1âˆ’Î±** (0.9500 at Î¸ = 0.3, 0.91 â€¦). **Defect found upstream:** `DescTools::BinomCI(method="witting")` puts Î±, not Î±/2, in each tail, so it returns a 1âˆ’2Î± interval. |
| 25 | **Coverage-adjusted Clopperâ€“Pearson** `"coverage-adjusted"` | Thulin 2014, *Scand. J. Statist.* 41 | R/Excel code from the author | âœ… | Reproduces Thulin's worked example (n=96, x=4: Î±â€² = 0.0698 vs 0.0697 printed; intervals to 3 decimals) and **all 30 rows of his Table 1** to â‰¤ 3Â·10â»â´. The table's own rounding comes from a ~1e-4 bisection tolerance: by direct numerical integration of his definition *our* Î±â€² gives mean coverage 0.95000000, the printed ones 0.95008. |
| 26 | **Randomised noise-Wilson** `"uniform-noise-wilson"`, `"split-wilson"` | Decrouez & Hall 2014; Thulin 2014 (arXiv:1402.6536) | â€” | â— | Reduce to plain Wilson at zero noise; E[pÌƒ \| x] = x/n; seeded. They are *randomised*: two analysts differ. |
| 27 | **Mid-P, Clopperâ€“Pearson, Blaker** | (already present) | | âœ… | **Correctness bug found and fixed in the existing Blaker:** see Â§6. |

## 4. Betting, mixture and anytime-valid intervals (the post-2017 paradigm)

| # | Method | Source | Elsewhere | Status | Verification |
|---|---|---|---|---|---|
| 28 | **Beta-binomial mixture CS** `"mixture"` | Robbins 1970; Howard et al. 2021, *Ann. Statist.* 49 | â€” (not as a binomial CI) | âœ… | Each limit satisfies âˆ« likelihood-ratio Ã— Beta prior = 1/Î± by **independent numerical integration**; anytime validity checked by simulating 400 streams Ã— 120 looks (error rate â‰¤ Î±). |
| 29 | **Sub-Gaussian normal-mixture CS** `"normal-mixture"` | Robbins 1970 | â€” | âœ… | Coverage guaranteed (exact enumeration); anytime-valid by simulation. |
| 30 | **Hedged-capital betting CI** `"betting"` | Waudby-Smith & Ramdas 2024, *JRSS-B* 86 | Py `confseq` (C++; grid) | âœ… | Capital process, predictable plug-in bets and limits **identical to `confseq` to 1e-16** on a fixed sequence (hedged CS and PrPl-EB). Table version derandomises by averaging the capital over B permutations (valid by Markov). |
| 31 | **Streaming `cibetseq`** (`hedged`, `mixture`, `normal`, `preb`) | WSR 2024; Howard 2021 | `confseq` | âœ… | `hedged` and `preb` frozen from `confseq` outputs (1e-6 / 1e-5); `mixture`, `normal` verified by simulation. |
| 32 | Howard et al. **stitched / LIL** boundaries; WSR **aKelly / grid-Kelly / LBOW** bets | Howard 2021; WSR 2024 | `confseq` | âŒ | Variance-adaptive stitching targets *sub-Gaussian / sub-exponential* data; for a Bernoulli the exact mixture (#28) is tighter, and the WSR default bet (#30) is implemented. Not worth the added surface. |
| 33 | BRAVO / ALPHA risk-limiting-audit *tests*; mSPRT / always-valid p-values | Stark; Lindon & Malek | `SHANGRLA`, Arlo, `rilacs` | âŒ | These are *tests*, not intervals; the mixture CS (#28) is the Beta-mixture mSPRT inverted. |

## 5. Evaluation criteria and planning (added alongside the methods)

| Capability | Source | Status | Verification |
|---|---|---|---|
| **Locally-correct criterion** `locally_correct()` | Garthwaite et al. 2024 | âœ… | Reproduces the paper's classification â€” Clopperâ€“Pearson âœ“, Mid-P âœ“ (Î±<0.1), **Wilson âœ—**; OLC equals the target on every cycle. Exact (closed-form integrals). |
| **PASS CI sample size** (`sample_size(plug_in="continuous")`) | NCSS PASS Ch. 115 | âœ… | **All 15 published sample sizes reproduced (before: 7/15)**, plus the printed interval limits and the dropout-inflated enrolment (914 â†’ 1143). |
| **SAS `PROBWIDTH`** `prob_width()` Â· assurance `sample_size_assurance()` Â· `expected_width()` | SAS PROC POWER; binGroup `binWidth` | âœ… | Brute-force enumeration identity; works for *every* registered method. |
| **Exact / z / adjusted-z test power**, `sample_size_test()` | SAS ONESAMPLEFREQ | âœ… | Exact test = SAS's critical values (re-derived independently) = Clopperâ€“Pearson duality to 1e-15. |
| **TOST equivalence** `power_equivalence()`, `sample_size_equivalence()` | SAS ONESAMPLEFREQ | âœ… | Brute-force enumeration; closed form uses SAS's convention that z_Î± is the *negative* Î±-quantile. |
| **Zero-failure / success-run plan** `sample_size_upper_bound()` | reliability, ISO 2859-type plans | âœ… | n = âŒˆln(1âˆ’C)/ln(1âˆ’p)âŒ‰; rule-of-three limit. |
| **Bayesian ALC / WOC** `sample_size_bayes()` | Joseph, Wolfson & du Berger 1995 | âœ… | Brute-force beta-binomial expectation. |
| **Kerman neutral prior** `prior("kerman")` | Kerman 2011 | âœ… | Registered with `(1/3, 1/3)`. |

## 6. A correctness defect found in the *existing* code while adding these

**Blaker's interval returned an interior crossing for a few (n, Î±, x).** The acceptability function
Î³(x, Î¸) is not unimodal, so the original per-row `scipy.optimize.brentq` could converge to an *inner* crossing
and return a limit that was too short. Across n = 2â€¦100 and Î± âˆˆ {0.001, 0.01, 0.05, 0.1, 0.2} that happened for
**24 of â‰ˆ 30 000 limits** (e.g. n=57, Î±=0.05, x=0: upper limit 0.0576 where the true outermost boundary is
0.0626). The coverage guarantee consequently dipped *below nominal* â€” min coverage **0.89932 for n=21, Î±=0.1**
(nominal 0.9000) â€” which the existing coverage test missed because it only tried n â‰¤ 20. The new table kernel walks
inward from the Clopperâ€“Pearson bound to the first acceptable Î¸ (as R's `PropCIs::blakerci` does) and restores the
exact guarantee (0.90002). The 24 disagreements were **all** adjudicated against a brute-force fine scan: in 24 of 24
the new value is the correct one. Regression tests pin it.

## 7. Considered and **not** implemented â€” and why

| Method | Source | Why not |
|---|---|---|
| **Anderssonâ€“Nerman interval** | Andersson & Nerman 2024, *Stat* (doi 10.1002/sta4.70027) | The defining formula is in the paywalled article (HTTP 403 for automated access); the abstract only states coverage â‰¥ Wilson at larger length. Implementing a guessed formula would violate the project's primary-source rule. **Highest-value follow-up if you can supply the PDF.** |
| **Schillingâ€“Doi LCO** (length/coverage optimal, deterministic) | Schilling & Doi 2014, *Amer. Statist.* 68 | Paper not accessible. NB: `binomial_cis` (PyPI) implements the **randomised** UMA/UMAU interval, *not* LCO â€” a different procedure. |
| **Wang (2006, 2007, 2010)** optimal / iterative intervals | Wang | Primary text not accessed. For the shortest equivariant *exact* interval, Blythâ€“Stillâ€“Casella (#22) is the established alternative. |
| **Crow (1956), Clunies-Ross (1958), Reiczigel (2003)** | | Crow and Clunies-Ross build the same minimal-cardinality acceptance sets as Sterne/BSC (Sterne and BSC have **identical total length** at n=20 â€” 7.2411 vs Clopperâ€“Pearson's 7.6874 â€” because both minimise the acceptance-set cardinality at every Î¸); Reiczigel's informal correction is Thulin's Beta(1,1)-prior correction (#25), per Thulin. Not separately implemented; no independent numerics to verify against. |
| **Guan (2012)** modified Wilson | Guan | Paper not accessed. |
| **McGrath & Burke (2024)** relative margin of error for rare events | *Amer. Statist.* | Paper not accessed. `expected_width`/`prob_width` already give absolute widths. |
| **Korn (1987)** / Thulin data-randomised Stevens | | Need the ordered 0/1 *sequence*, not (x, n). Out of scope for the (x, n) table API (`cibetseq` handles sequences). |
| Robust / mixture-of-Betas priors; Bayesian bootstrap | | The Bayesian toolbox is conjugate-Beta by design; a mixture posterior is a natural sequel, not a gap in *interval methods*. |
| Bennett, Bretagnolleâ€“Huberâ€“Carol bounds | | For a Bernoulli, KL-Chernoff (#18) is the exact inversion of the Chernoff bound and dominates them. |
| Two-sample / difference-of-proportions intervals | many | Out of scope (single proportion) â€” a documented sequel. |

## 8. What the Python/R competition covers (for context)

| Package | Binomial CI methods | Evaluation layer | Notes |
|---|---|---|---|
| `statsmodels` | 6 | â€” | the de facto Python default |
| `scipy` | 3 (exact, Wilson, Wilson-cc) | â€” | |
| `astropy` | 4 (Wilson, Jeffreys, Wald, `binom_conf_interval`) | â€” | |
| **`DBCI` (PyPI `diff-binom-confint`)** | **16** incl. Blaker, Pratt, Witting, Mid-P, modified-*; Streamlit app | tests vs SAS/PASS/DescTools | *Not* the "no Python package has these" the earlier novelty report claimed. Its Blaker steps by 1e-5, its Pratt/Witting have the defects above. |
| `binomial_cis` | randomised UMA/UMAU exact (numba) | â€” | Pre-review JOSS submission closed ("uncertain scope") |
| `pynomial` (GitHub; **not** the PyPI package of the same name) | 9 | â€” | port of R `binom` |
| `confseq` | betting / confidence sequences | â€” | C++ build; needs a toolchain (fails on Windows here) |
| `binoculars`, `evalci` | 3â€“4 | â€” | small utilities; `binoculars`' "wilson" does not return Wilson's interval |
| R `binom` | 11 | `binom.coverage`, `binom.length` | |
| R `DescTools::BinomCI` | 16 | â€” | defects above |
| R `binomCI` (CRAN, Feb 2026) | 12 | â€” | no evaluation / sample-size functions |
| R `proportion` | 12 | **full** | archived from CRAN 2022; the original binomcikit ported |
| SAS PROC FREQ | 9 (Wald, exact, AC, Blaker, Jeffreys, mid-P, LR, logit, Wilson) | â€” | commercial |
| NCSS PASS | 5 (+ sample size / width) | sample-size only | commercial |

**No package, in any language, combines the interval methods above with the evaluation layer (coverage, length,
p-confidence/bias, error, local correctness) and the Bayesian toolbox, in one tool.** That claim â€” not "first in
Python", which the earlier report made and which `DBCI` refutes â€” is the defensible one.
