---
name: binomcikit-numerical-audit
description: >-
  Use when writing new root-finding/optimization code in binomcikit's ci/
  subpackage (a new limit-producer, a new MLE or cutoff search), when
  reviewing an existing one for correctness, or when asked to audit the
  codebase for numerical bugs. Signals: "add a new method that needs
  root-finding", "check for numerical bugs", "audit scipy.optimize usage",
  a CI function behaves correctly at small n but is untested at large n.
---

# binomcikit — numerical robustness for root-finding CI code

**Why this exists:** `cilrx`/`cilr`/`cialr` (the Likelihood-Ratio interval)
silently returned an interval close to `[0, 1]` for any `n` above ~26,000.
Root cause: the code found the MLE by numerically minimizing the *raw*
binomial likelihood (`scipy.stats.binom.pmf`), which underflows to exactly
`0.0` for large `n` away from the true value. With nothing but a flat zero
region to search, `scipy.optimize.minimize_scalar` converged to an arbitrary
wrong point. It shipped with golden-value tests at `n=5` that passed cleanly —
small `n` never triggers the underflow, so nothing caught it. Full writeup:
`docs/under_the_hood.md` "Sample-size / power".

## The rule, in one line

**A binomial-likelihood MLE search is a closed form (`x/n`), not an
optimization problem. A confidence-interval endpoint is a root-find (where
does a monotone function cross zero), not a minimization problem.** If you
catch yourself calling `minimize_scalar` to locate either, stop — you're
solving the right problem with the wrong tool.

## Checklist for new root-finding CI code

1. **Never call `stats.binom.pmf` (raw probability) inside an optimizer's
   objective.** Use `stats.binom.logpmf`. Raw pmf underflows to `0.0` in
   float64 once `n` is large enough that the likelihood at the search point is
   below ~1e-308 — which happens routinely, not just at extreme `n`, for any
   point far from the mode. `logpmf` never underflows this way.
2. **If you need an MLE of a binomial proportion, it's `x / n` — don't search
   for it.** No binomcikit method needs a *numerically* found MLE; the
   binomial's is always closed-form. (An MLE of something else — a
   pseudo-count-adjusted count, a mixture — may still need care, but check for
   a closed form before reaching for `minimize_scalar`.)
3. **For "find where this crosses a threshold," use `brentq` or
   `root_scalar`, not `minimize_scalar` on `abs(f(p) - cutoff)`.** Minimizing
   an absolute difference asks the optimizer to find where a V-shaped curve
   bottoms out; root-finding asks it to find a sign change. The latter is
   provably more robust: a proper bracket with opposite-signed endpoints
   cannot silently converge to the wrong root the way an ill-conditioned
   minimization can when the landscape goes flat almost everywhere. See
   `src/binomcikit/ci/base_n_x.py`'s `cilrx` for the pattern (closed-form MLE
   + `brentq` on the signed log-likelihood-minus-cutoff function), including
   the `x==0`/`x==n` boundary special-cases (no valid bracket there — assign
   the limit directly, don't search).
4. **`bisect`-based `root_scalar` on a properly-signed function is safe by
   construction** (needs only that the two endpoints disagree in sign, not
   smoothness in between) — this is the family used by the exact/Mid-P
   methods and needs no special large-n caution.
5. **Stress-test empirically at large n before trusting a new root-find.**
   Don't reason your way to "this is fine" — run it. A useful smoke test:
   ```python
   import binomcikit as b
   for n in [20, 1000, 26000, 100000, 1000000]:
       x = n // 2
       print(n, b.ci(x=x, n=n, method="<new_method>"))
   ```
   A correct method's interval shrinks steadily toward `x/n` as `n` grows. A
   broken one typically shows a **sharp cliff** at some threshold (not a
   gradual drift) — the signature of an optimizer losing its footing once the
   underflow region gets large enough relative to the search bracket, not of
   accumulating floating-point error.

## Auditing existing code (the technique used to find/confirm this bug)

```bash
grep -rn "optimize\.\|brentq\|minimize_scalar\|fsolve\|root_scalar" src/binomcikit --include="*.py"
```
For each hit: read what the objective function evaluates (raw pmf/likelihood,
or log). If raw, that call is a candidate — **don't assume a sibling function
is equally affected just because it looks similar**: `cilrx`/`cilr` had the
bug, but `cialrx` (same family, same file layout, single-`x` variant) already
used `logpmf` and was fine — confirmed by directly running the isolated
formula, not by inference. Every candidate needs its own empirical large-n
check (the smoke test above); a `bisect`/`root_scalar` hit on a monotone,
correctly-signed function generally doesn't need one (see point 4), but a
`minimize_scalar` hit always does.

## Common mistakes
- Fixing the bug you found and stopping — the same anti-pattern is often
  copy-pasted into a sibling function (the all-`x` and single-`x` variants of
  a method are usually two independent implementations of the same idea).
  Grep for the same pattern elsewhere before considering the fix done.
- Writing a regression test at the *original* n only when that n makes the
  test slow — the all-`x` (`ci*`, not `ci*x`) functions loop over every `x`
  in Python, so a full-table test at `n=26,000`+ can take minutes even fixed.
  Test the fast single-`x` path at the real failure scale, and the full-table
  path at a smaller n that still exercises the same code (cross-check the two
  agree, per `tests/test_golden_paper.py::test_cialr_matches_cialrx`).
