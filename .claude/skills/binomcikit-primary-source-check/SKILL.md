---
name: binomcikit-primary-source-check
description: >-
  Use before implementing a method or construction that binomcikit ports from
  a cited paper (RESEARCH.md, ROADMAP.md, or any planning-doc summary of an
  external source) — verify the primary source's actual text/equations before
  coding from a paraphrase. Signals: "implement <method> from the paper",
  "RESEARCH.md §9 has the construction", adding a method whose formula comes
  from a citation rather than from code already in this repo.
---

# binomcikit — verify the primary source before coding from a citation

**Why this exists:** two real, confirmed failures from trusting a secondary
summary instead of the primary text.

1. `RESEARCH.md`'s summary of the Wang & Hutson (2013) smooth bootstrap said
   "invert mean(X*) via a cubic B-spline" — true, but missing the actual
   knots and coefficients, which don't exist anywhere derivable from first
   principles; they're numbers printed in the paper. Coding from the summary
   alone would have meant guessing or badly approximating them. Fetching the
   paper's primary text (via PMC) gave the exact spline and confirmed the
   median-unbiased-estimator boundary formulas independently.
2. `ROADMAP.md` named `scipy.stats.binomtest` as the "oracle" for a planned
   p-value feature. It wasn't: scipy's default two-sided p-value uses a
   different mathematical convention than the one the feature's own design
   rationale required. Nobody had checked; the claim just got repeated
   forward across planning docs. See `binomcikit-oracle-vetting`.

## The rule

Before writing code from a paper citation (or from a planning doc's summary
*of* one), get the primary source's actual equations — not a third or fourth
paraphrase of them.

1. **Find the primary source.** Prefer an open-access copy (PMC, arXiv, the
   journal, the authors' own site) over a summary. Use `WebSearch` then
   `WebFetch` with a prompt that asks for the *exact algorithm/equations*,
   quoted, with section/equation numbers — not a plain-English gloss.
2. **Get numbers, not descriptions, for anything that isn't derivable.** A
   fitted constant, a specific spline/table, a numerically-tuned cutoff —
   these exist only in the paper. "Construction reproduces X" is not
   implementable; the actual formula is.
3. **Sanity-check what you got.** Recompute a boundary case or special value
   by hand/independently (e.g. does the formula's stated edge-case behavior
   match a value you can derive a different way?) before trusting it as the
   basis for shipped code — this is what caught that the median-unbiased
   estimator's boundary formulas were an instance of the same incomplete-beta
   identity used elsewhere in the package, not an unrelated special case.
4. **If a planning doc's citation claim doesn't survive the check, fix the
   doc.** Don't silently work around a wrong claim and leave it for the next
   session to repeat.

## Common mistakes
- Treating "the summary mentions the right paper" as equivalent to "the
  summary has the right formula."
- Coding a plausible-looking approximation of a fitted constant instead of
  fetching the real one.
- Trusting an internal doc's citation claim (oracle, formula, convention)
  without independently confirming it once, the first time it's load-bearing.
