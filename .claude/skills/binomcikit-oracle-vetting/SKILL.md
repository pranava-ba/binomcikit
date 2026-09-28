---
name: binomcikit-oracle-vetting
description: >-
  Use before writing a test that asserts a new binomcikit function matches an
  external library function (scipy, statsmodels, R) as its oracle — confirm
  both compute the same mathematical convention, not just a plausible answer
  to the same kind of question. Signals: "verify against scipy/statsmodels",
  writing an oracle/golden-value test, a new test comparing bk.<fn> to a
  third-party function with a similar name.
---

# binomcikit — same name does not mean same math

**Why this exists:** `ROADMAP.md` named `scipy.stats.binomtest` as "the
oracle" for binomcikit's planned p-value feature (`pvalue`/`reject`, CI-test
duality). It's the wrong oracle: scipy's default two-sided p-value uses a
different ("minlike", smallest-probability) convention than the equal-tailed
construction dual to binomcikit's own CIs. At `x=3, n=20, theta0=0.05` the two
disagree by exactly **2x** — not close, not a rounding difference. Both
"binomial two-sided p-value" — same name, different math. Caught only by
deriving the closed-form formula independently and comparing, not by trusting
the citation.

## The rule

Before `assert bk.<fn>(...) == external_library.<fn>(...)`:

1. **Derive or state the formula each side actually computes**, in symbols —
   not "does the same kind of test/interval/estimate." If you can't write
   both formulas down, you haven't vetted the oracle yet.
2. **Check the parts that commonly differ:** tail convention (equal-tailed vs.
   minlike vs. likelihood-based), boundary handling at `x=0`/`x=n`, default
   parameterization (which prior, which correction, which `alternative=`).
   These are exactly where "similar function, different answer" hides.
3. **Test the genuinely unambiguous sub-piece first.** One-sided tail
   probabilities agree across every reasonable convention; a full two-sided
   or composite statistic often does not. Verifying the unambiguous piece
   (e.g. `scipy.stats.binomtest(..., alternative="less"/"greater")` against
   the one-sided tail) gives real evidence without assuming the composite
   number is safe to trust too.
4. **If there's a genuine, explainable discrepancy, write a test that locks
   it in** (asserts the *specific* known ratio/difference, with a comment
   explaining why) instead of either forcing equality or silently comparing
   against whichever number happens to be closer.
5. **A discrepancy is itself useful documentation** — it usually means the
   two conventions solve subtly different problems. Say so in the function's
   docstring and in `docs/under_the_hood.md`, the way `pvalue`'s deliberate
   divergence from `scipy.stats.binomtest` is documented, not hidden.

## Common mistakes
- Picking an oracle because the function name matches, without reading what
  it actually computes.
- Trusting a planning doc's "verify against X" note without re-deriving why
  X is the right comparison for *this* construction specifically.
- Silently changing your own function's convention to match the oracle
  "because the test failed," rather than checking which one is actually
  correct for what you're building.
