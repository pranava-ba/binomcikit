# Papers to download for the primary-source checks

> Prepared 2026-10-03. **Every DOI below was looked up in Crossref (title, authors, journal and volume matched, and the pages quoted are the ones Crossref returned; issue numbers are left out because I did not verify them) on that date; none comes
> from memory.** The exceptions are marked "no DOI found". OpenAlex lists all of them as closed access, and the publishers' sites block
> automated downloads, so I could not read any of them. Please save the PDFs into **`previous-work/`** (it is git-ignored; PDFs must never be
> committed, copyright) using the file names in the last column, and tell me; I will then run each check and update the docs.

## Where the two checks stand without the papers

| Item | What I could establish from other sources | What the paper is still needed for |
|---|---|---|
| **6. Two-proportion methods** (`bk.diff_interval`) | **88 of 88** published intervals reproduced to the 4 printed decimals (Newcombe 1998 Table II as recast in the SAS paper below, plus SAS output), across 12 methods and 9 tables including the boundary tables (0/10 vs 0/20, 10/10 vs 0/10). The PASS and SAS reference documents print the Miettinen–Nurminen cubic, the `N/(N-1)` factor, Mee's `λ = 1` and Newcombe's methods 10 and 11 exactly as implemented. (Those two documents are in DBCI's `references/` folder on GitHub.) | A first-hand read of the formulas, and confirmation that the table in the SAS paper is transcribed correctly from Newcombe's Table II. |
| **7. Pratt** | DBCI's and DescTools' lower limit is off the exact Clopper–Pearson limit by up to 0.13 (n = 20), against < 1e-3 for the *upper* limit of the same formula; replacing `n-x-1` by `n-x+1` restores the upper-limit accuracy. Our mirror construction `L(x) = 1 - U(n-x)` is within 1e-4 of exact. | Pratt's own lower-limit formula, to say "this is what Pratt published" rather than "this is what a normal approximation to the exact limit has to be". |
| **7. Witting** | DBCI's "95%" Witting interval covers 0.90 (simulation, 3 values of θ); ours covers 0.95. | Witting (1985) itself, to cite the construction and check the tail split. |

---

## A. Needed to close items 6 and 7 (do these first)

| # | Paper | DOI | Check I will do with it | Save as |
|--:|---|---|---|---|
| 1 | Pratt, J. W. (1968). *A normal approximation for binomial, F, beta, and other common, related tail probabilities, II.* JASA 63, 1457–1483 | [10.1080/01621459.1968.10480939](https://doi.org/10.1080/01621459.1968.10480939) (same paper on JSTOR: [10.2307/2285896](https://doi.org/10.2307/2285896)) | Find the formula for the binomial limits, check it against `_pratt_upper` (`src/binomcikit/ext/closed_form.py`) and against the lower-limit expression used by DBCI/DescTools; settles upstream reports #6 and #8 | `pratt1968_part2.pdf` |
| 2 | Newcombe, R. G. (1998). *Interval estimation for the difference between independent proportions: comparison of eleven methods.* Stat. Med. 17, 873–890 | [10.1002/(SICI)1097-0258(19980430)17:8<873::AID-SIM779>3.0.CO;2-I](https://doi.org/10.1002/(SICI)1097-0258(19980430)17:8%3C873::AID-SIM779%3E3.0.CO;2-I) | Method definitions (1–11); **Table II** against the 88 values already matched; the continuity-corrected forms | `newcombe1998_difference.pdf` |
| 3 | Newcombe, R. G. (1998). *Two-sided confidence intervals for the single proportion: comparison of seven methods.* Stat. Med. 17, 857–872 | [10.1002/(SICI)1097-0258(19980430)17:8<857::AID-SIM777>3.0.CO;2-E](https://doi.org/10.1002/(SICI)1097-0258(19980430)17:8%3C857::AID-SIM777%3E3.0.CO;2-E) | The Wilson continuity-corrected limits used inside `newcombe-cc` (`twoprop._wilson`, `cc=True`) | `newcombe1998_single.pdf` |
| 4 | Miettinen, O. & Nurminen, M. (1985). *Comparative analysis of two rates.* Stat. Med. 4, 213–226 | [10.1002/sim.4780040211](https://doi.org/10.1002/sim.4780040211) | Score statistic, the `N/(N-1)` factor, the closed-form restricted MLE (the cubic) | `miettinen_nurminen1985.pdf` |
| 5 | Mee, R. W. (1984). *Confidence bounds for the difference between two probabilities.* Biometrics 40, 1175–1176 | **no DOI found** (Crossref and OpenAlex searched; the volume and pages are from memory and from the references of other papers, so please confirm them when you locate it; look under JSTOR, Biometrics 40, no. 4) | That Mee's interval is the score interval with `λ = 1` | `mee1984.pdf` |
| 6 | Agresti, A. & Caffo, B. (2000). *Simple and effective confidence intervals for proportions and differences of proportions result from adding two successes and two failures.* Am. Stat. 54, 280–288 | [10.1080/00031305.2000.10474560](https://doi.org/10.1080/00031305.2000.10474560) | The "add one success and one failure to each sample" form and its variance | `agresti_caffo2000.pdf` |
| 7 | Brown, L. D., Cai, T. T. & DasGupta, A. (2001). *Interval estimation for a binomial proportion.* Stat. Sci. 16 | [10.1214/ss/1009213286](https://doi.org/10.1214/ss/1009213286) | The modified Wilson interval (boundary adjustment near 0 and n): settles upstream report #1 (the missing `1 -`) | `brown_cai_dasgupta2001.pdf` |
| 8 | Witting, H. (1985). *Mathematische Statistik I.* Teubner, Stuttgart (Beispiel 2.106) | **book, no DOI**; borrow it or request the section through a library | The randomised uniformly-most-accurate binomial interval and how the error is split between the tails; our docstring (`ext/exact.py`) cites Beispiel 2.106 | `witting1985_beispiel2_106.pdf` |
| 9 | Fagerland, M. W., Lydersen, S. & Laake, P. (2011). *Recommended confidence intervals for two independent binomial proportions.* Stat. Methods Med. Res. 24, 224–254 | [10.1177/0962280211415469](https://doi.org/10.1177/0962280211415469) | The best single survey: method definitions, which ones they recommend (our default is Newcombe's hybrid score), and a second published table to test against | `fagerland2011.pdf` |

If you can only fetch a few, take **1, 2, 7, 8** (they settle the upstream reports) and then **4, 3**.

## B. Needed only for later items (not blocking)

| Paper | DOI | Used for |
|---|---|---|
| Hauck, W. W. & Anderson, S. (1986). *A comparison of large-sample confidence interval methods for the difference of two binomial probabilities.* Am. Stat. 40, 318–322 | [10.1080/00031305.1986.10475426](https://doi.org/10.1080/00031305.1986.10475426) | `hauck-anderson` (backlog item 9) |
| Brown, L. D. & Li, X. (2005). *Confidence intervals for two sample binomial distribution.* J. Stat. Plan. Inference 130, 359–375 | [10.1016/j.jspi.2003.09.039](https://doi.org/10.1016/j.jspi.2003.09.039) | `brown-li`, `miettinen-nurminen-brown-li` |
| Agresti, A. & Min, Y. (2001). *On small-sample confidence intervals for parameters in discrete distributions.* Biometrics 57, 963–971 | [10.1111/j.0006-341x.2001.00963.x](https://doi.org/10.1111/j.0006-341x.2001.00963.x) | `agresti-min` |
| Santner, T. J. & Snell, M. K. (1980). *Small-sample confidence intervals for p1−p2 and p1/p2 in 2×2 contingency tables.* JASA 75, 386–394 | [10.1080/01621459.1980.10477482](https://doi.org/10.1080/01621459.1980.10477482) (JSTOR [10.2307/2287464](https://doi.org/10.2307/2287464)) | `santner-snell` |
| Chan, I. S. F. & Zhang, Z. (1999). *Test-based exact confidence intervals for the difference of two binomial proportions.* Biometrics 55, 1202–1209 | [10.1111/j.0006-341x.1999.01202.x](https://doi.org/10.1111/j.0006-341x.1999.01202.x) | `chan-zhang` |
| Wang, W. (2010). *On construction of the smallest one-sided confidence interval for the difference of two proportions.* Ann. Stat. 38 | [10.1214/09-AOS744](https://doi.org/10.1214/09-AOS744) | `wang` (exact unconditional); heavy to implement |
| Anscombe, F. J. (1948). *The transformation of Poisson, binomial and negative-binomial data.* Biometrika 35, 246–254 | [10.1093/biomet/35.3-4.246](https://doi.org/10.1093/biomet/35.3-4.246) | DBCI's arcsine variant (3/8-shifted centre), backlog item 10 |
| Vollset, S. E. (1993). *Confidence intervals for a binomial proportion.* Stat. Med. 12, 809–824 | [10.1002/sim.4780120902](https://doi.org/10.1002/sim.4780120902) | How Pratt's formula is used in practice (DescTools cites this lineage) |
| Peizer, D. B. & Pratt, J. W. (1968). *A normal approximation for binomial, F, beta, and other common, related tail probabilities, I.* JASA 63, 1416– | [10.2307/2285895](https://doi.org/10.2307/2285895) | Part I of the Pratt paper; context only |
| Blaker, H. (2000). *Confidence curves and improved exact confidence intervals for discrete distributions.* Can. J. Stat. 28, 783–798 | [10.2307/3315916](https://doi.org/10.2307/3315916) | Re-confirming our Blaker construction |
| Sterne, T. E. (1954). *Some remarks on confidence or fiducial limits.* Biometrika 41, 275–278 | [10.1093/biomet/41.1-2.275](https://doi.org/10.1093/biomet/41.1-2.275) | Sterne's interval |
| Casella, G. (1986). *Refining binomial confidence intervals.* Can. J. Stat. 14, 113–129 | [10.2307/3314658](https://doi.org/10.2307/3314658) | Blyth–Still–Casella |
| Wilson, E. B. (1927). *Probable inference, the law of succession, and statistical inference.* JASA 22, 209–212 | [10.1080/01621459.1927.10502953](https://doi.org/10.1080/01621459.1927.10502953) | The Wilson interval |

## C. Already readable without a download

| Document | Where | Status |
|---|---|---|
| *Constructing Confidence Intervals for the Differences of Binomial Proportions in SAS* (WUSS 2016, paper 127) | [lexjansen.com/wuss/2016/127_Final_Paper_PDF.pdf](https://www.lexjansen.com/wuss/2016/127_Final_Paper_PDF.pdf), and `references/` in DBCI's repository | **Read 2026-10-03**: defines 17 methods with formulas; its Table II recasts Newcombe's. DBCI's README notes it has errors in its descriptions of Wilson-cc, Mee and Miettinen–Nurminen (the code blocks are correct); our numbers match its printed values |
| PASS manual, *Confidence Intervals for the Difference Between Two Proportions* (NCSS) | `references/` in DBCI's repository | **Read 2026-10-03**: prints the Miettinen–Nurminen cubic and score statistic |
| Pires, A. M. & Amado, C. (2008). *Interval estimators for a binomial proportion: comparison of twenty methods.* REVSTAT 6, 165–197 | open access at the journal (INE Portugal) | Read in full in an earlier session; no DOI in Crossref |

## D. What to tell me when a paper is saved

Just the file name. For each paper I will run the check in the table, report a one-line verdict (matches / differs, with the numbers), fix the code
or the docs if it differs, and then (for #1, #7, #8) update the status of the upstream reports in `planning/UPSTREAM_REPORTS_DRAFT.md`.
