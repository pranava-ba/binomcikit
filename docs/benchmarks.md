# Benchmarks: binomcikit vs the other Python tools

Every number here comes from one script, `benchmarks/bench_competitors.py` (output:
`benchmarks/results.json`, full tables in `benchmarks/RESULTS.md`). Re-run it with
`python benchmarks/bench_competitors.py --markdown` (add `--quick` for a minute-long version).

## Method

* **Machine:** AMD64 (Family 25 Model 68), Windows 11, Python 3.13.5, numpy 2.3.2, scipy 1.16.1, pandas 2.3.3, numba 0.65.1,
  statsmodels 0.14.5, astropy 8.0.1, `diff_binom_confint` (DBCI) 0.1.0. Single run on one machine; timings are best-of-N wall
  clock and will differ on yours.
* **Competitors** are called the way their documentation says. For packages that only produce one interval per call
  (scipy, DBCI, pynomial, binoculars) a whole table is built with a Python loop over $x=0..n$; that is the only way those
  packages can produce a table, and it is what a user would have to write, but it is a loop-versus-vectorised comparison, not
  only an algorithm comparison.
* **Parity** (last column of the full tables) is the largest absolute difference between the competitor's limits and
  binomcikit's for the same method. A speed-up with no parity is meaningless, so read the two together.
* **Two binomcikit paths are timed.** `bk.ci()` returns a full DataFrame (limits, boundary flags, zero-width-interval flag,
  ...); `bk.limits()` / `bk.interval()` return bare arrays or floats. Comparing the lean path with a competitor's bare array is
  the fair like-for-like; comparing `ci()` shows what the richer output costs.

## Headline, stated honestly

* **Against loop-based packages the whole-table speed-up is large** (e.g. `n=1000`, Wilson: scipy 781 ms and DBCI 89 ms versus
  binomcikit 28 µs on the lean path, 237 µs through `ci()`). Exact (Clopper–Pearson) at `n=1000`: DBCI 262 ms, pynomial 204 ms,
  binoculars 300 ms, scipy 3.2 s versus 1.4 ms (lean) / 2.2 ms (`ci()`).
* **Against the vectorised packages, `bk.ci()` is *slower* for the closed-form methods.** statsmodels takes 97 µs for a Wilson
  table at `n=100` against our 168 µs; astropy takes ~42 µs. The remaining gap is the DataFrame (about three-quarters of the time
  is pandas building six columns), not the maths: on the lean path we are 1.5–7.6× faster than statsmodels (2.1–5.1× for Wilson),
  and for Clopper–Pearson `ci()` already wins at `n ≥ 1000` (1.4–1.7×). `bk.ci()` is **not** the fastest way to get a bare Wilson
  table; use `bk.limits()` for that. (On 2026-10-03 the `LABB`/`UABB`/`ZWI` columns stopped being built through
  `np.where(...).astype(object)`: `ci()` Wilson at `n=10,000` fell from about 4 ms to 0.5 ms.)
* **Jeffreys through `ci()`** (6.6 ms at `n=100`, 226 ms at `n=10,000`) looks 8–10× slower than statsmodels or astropy, but it is
  not like-for-like: `ci(method="jeffreys")` returns the equal-tailed interval **and** the highest-posterior-density interval (the
  `LBAH`/`UBAH` columns), and the HPD search is most of the time. The equal-tailed limits alone (`bk.limits(..., "jeffreys")`) take
  229 µs at `n=100` (statsmodels: 754 µs).
* **A single interval:** `bk.interval()` costs about 2–9 µs. statsmodels needs 116–223 µs, scipy 1.1–4.0 ms, DBCI 108–299 µs,
  astropy 25–34 µs. `bk.ci(n=…, x=…)` (191–567 µs) is comparable to those packages rather than faster.

## A. Whole table, selected rows (`n` = 1000)

| method | `ci()` | lean | statsmodels | astropy | scipy loop | DBCI loop | pynomial loop |
|---|---:|---:|---:|---:|---:|---:|---:|
| Wilson | 237 µs | 28 µs | 103 µs | 42 µs | 781 ms | 89 ms | 111 ms |
| Clopper–Pearson | 2.2 ms | 1.4 ms | 3.0 ms | n/a | 3.24 s | 262 ms | 204 ms |
| Jeffreys | 28.4 ms | 1.7 ms | 3.8 ms | 3.3 ms | n/a | 293 ms | n/a |
| Agresti–Coull | 490 µs | 31 µs | 157 µs | n/a | n/a | 125 ms | 133 ms |
| Wald | 268 µs | 27 µs | 127 µs | 32 µs | n/a | 118 ms | 142 ms |

Parity with statsmodels, astropy, scipy, DBCI and pynomial is ≤ 5e-13 for these five methods, so those speed-ups compare equal
answers. Two comparisons needed care and were corrected on 2026-10-03: pynomial's `wilson()` is continuity-corrected by default
(the harness now passes `correct_continuity=False`), and the Wald and Agresti–Coull limits of pynomial, astropy and binoculars are
not clamped to [0, 1] (the harness clamps them before comparing). Both had previously shown up as spurious 1e-3–1e-2 "parity"
gaps. binoculars still differs by 1.8e-6 to 5.7e-7 because its `z` defaults to the hard-coded 1.96 rather than the exact
quantile for α = 0.05.

## C. Methods only DBCI also ships (`n` = 60)

| method | binomcikit | DBCI | speed-up | parity |
|---|---:|---:|---:|---:|
| Blaker | 7.3 ms | 18.88 s | 2,587× | 9.9e-6 |
| mid-p | 5.0 ms | 202 ms | 40× | 5.0e-13 |
| likelihood ratio | 2.1 ms | 220 ms | 105× | 3.7e-13 |
| modified Jeffreys | 754 µs | 16.4 ms | 22× | 4.4e-16 |
| Pratt | 352 µs | 5.7 ms | 16× | **5.3e-2** |
| modified Wilson | 729 µs | 6.9 ms | 9.5× | **1.0** |

The two rows with a non-trivial parity are *disagreements about the answer*, so their speed-ups are not like-for-like.
* **Blaker:** DBCI steps the parameter in increments of 1e-5 (a literal `tol = 1e-5` loop in its source), hence the 1e-5
  differences; our value is the exact root.
* **Modified Wilson:** the upper limit in DBCI's code is the *lower*-tail expression without `1 -`, so for `x` near `n` the upper
  limit falls below the lower one (59 of 60: lower 0.9114, upper 0.0004). Verified against both PyPI 0.1.0 and `main`.
* **Pratt:** DBCI's *lower* limit is the problem: against the exact Clopper–Pearson limit it is off by up to 0.13 (n = 20), while
  its upper limit and ours are within 1e-3. The lower-limit expression has `n - x - 1` where `n - x + 1` is needed; DescTools'
  recorded output has the same value. Nothing has been filed upstream (the drafts are in `planning/UPSTREAM_REPORTS_DRAFT.md`).

## D. Coverage-probability curve (2000 θ points)

| `n` | binomcikit | numpy/scipy reference | speed-up |
|---:|---:|---:|---:|
| 100 | 21.8 ms | 35.0 ms | 1.6× |
| 1000 | 5.8 ms | 483 ms | 83× |
| 10,000 | 22.4 ms | 6.44 s | 288× |

The reference is a straightforward vectorised numpy/scipy implementation of the same quantity, not another package's API; we
found no other Python package with a coverage-curve function to compare against. Parity ≤ 9e-12.

## E. Anytime-valid betting confidence sequence

Against `confseq` (the authors' reference implementation) the hedged-capital sequence over 1000 observations takes 4.6 ms
(`breaks=100`) and 49.5 ms (`breaks=1000`) versus 40.2 and 318.2 ms: **6.4–8.7×**, with identical output to 1e-16.
(`confseq` could not be pip-installed on this machine, so the benchmark imports its Python sources directly.)

## F. Methods only binomcikit has: absolute cost, including the slow ones

These have no competitor to compare with, so only the absolute time of the whole table is shown. Not everything is fast:

| method | n=50 | n=200 | n=1000 | n=5000 |
|---|---:|---:|---:|---:|
| Pratt | 538 µs | 486 µs | 627 µs | 1.1 ms |
| Hoeffding | 255 µs | 278 µs | 309 µs | 507 µs |
| Cressie–Read | 5.8 ms | 5.8 ms | 10.2 ms | 31.0 ms |
| higher-order likelihood (r*) | 7.5 ms | 8.6 ms | 12.0 ms | 33.6 ms |
| mixture confidence sequence | 2.0 ms | 2.2 ms | 4.1 ms | 13.3 ms |
| Chernoff / KL | 3.9 ms | 6.2 ms | 17.5 ms | 74.7 ms |
| length-optimal (OLC) | 2.3 ms | 8.5 ms | 59.7 ms | 291 ms |
| Blyth–Still–Casella | 24.9 ms | 95.7 ms | 434 ms | not run |
| **Sterne** | 6.0 ms | 30.1 ms | **403 ms** | **7.79 s** |
| **hedged betting (full table)** | 42.1 ms | 576 ms | **14.7 s** | not run |

Sterne now runs in about 0.4 s at `n=1000` and 7.8 s at `n=5000` (it was 3.3 s and 82 s before the 2026-10-03 pass, which replaced
`scipy.stats` calls in the inner loop with precomputed log-pmfs and `scipy.special` ufuncs; the limits are unchanged to ~1e-14).
The full-table betting interval takes about 15 s at `n=1000` (it was about 80 s; numba now runs chunks of rows in parallel, and the
table is bit-identical for a given seed). Betting is still the slowest method here, at roughly $O(B\,n^2)$ per table, and it needs
numba plus several cores to get that figure. Both are usable to a few hundred trials without waiting; no speed claim is made beyond that.

## What this does and does not show

* It shows large, reproducible gains over every loop-based package and over the old binomcikit code, with equal answers.
* It does **not** show that `bk.ci()` beats statsmodels or astropy for closed-form intervals; it does not. Use `bk.limits()`
  or `bk.interval()` when raw speed on those matters.
* One machine, one run, `n` at most 10,000 for tables. Timings under load vary: two earlier passes on 2026-10-03 looked slow only
  because another process was using the CPU (the first run on 2026-10-01 looked slow for the same reason), so the published numbers
  are from a run with nothing else active. On that idle machine the untouched hedged betting sequence ran in 4.6 ms against 3.8 ms on
  2026-10-01, so absolute times can still drift by ~20% between days; the ratios between packages are the thing to read.
