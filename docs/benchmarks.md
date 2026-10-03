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

* **Against loop-based packages the whole-table speed-up is large** (e.g. `n=1000`, Wilson: scipy 622 ms and DBCI 70 ms versus
  binomcikit 25 µs on the lean path, 351 µs through `ci()`). Exact (Clopper–Pearson) at `n=1000`: DBCI 202 ms, pynomial 152 ms,
  binoculars 224 ms, scipy 2.6 s versus 1.1 ms (lean) / 1.8 ms (`ci()`).
* **Against the vectorised packages, `bk.ci()` is *slower* for the closed-form methods.** statsmodels takes 82 µs for a Wilson
  table at `n=100` against our 165 µs; astropy takes 26 µs. The reason is the DataFrame and the flag columns, not the maths: on
  the lean path we are 1.2–6× faster than both, and for Clopper–Pearson `ci()` already wins at `n ≥ 1000` (1.4–1.6×).
  `bk.ci()` is **not** the fastest way to get a bare Wilson table.
* **Jeffreys through `ci()`** (4.4 ms at `n=100`, 180 ms at `n=10,000`) is 7–8× slower than statsmodels or astropy; the lean
  path is ~2× faster than them. That is DataFrame overhead plus the boundary/flag post-processing.
* **A single interval:** `bk.interval()` costs about 2–6 µs. statsmodels needs 71–143 µs, scipy 0.65–2.5 ms, DBCI 69–198 µs,
  astropy 14–22 µs. `bk.ci(n=…, x=…)` (138–350 µs) is comparable to those packages rather than faster.

## A. Whole table, selected rows (`n` = 1000)

| method | `ci()` | lean | statsmodels | astropy | scipy loop | DBCI loop | pynomial loop |
|---|---:|---:|---:|---:|---:|---:|---:|
| Wilson | 351 µs | 25 µs | 105 µs | 34 µs | 622 ms | 70 ms | 90 ms |
| Clopper–Pearson | 1.8 ms | 1.1 ms | 2.5 ms | n/a | 2.60 s | 202 ms | 152 ms |
| Jeffreys | 20.2 ms | 1.2 ms | 2.7 ms | 2.5 ms | n/a | 198 ms | n/a |
| Agresti–Coull | 450 µs | 19 µs | 92 µs | n/a | n/a | 70 ms | 86 ms |
| Wald | 352 µs | 18 µs | 87 µs | 23 µs | n/a | 69 ms | 85 ms |

Parity with statsmodels, scipy and DBCI is ≤ 7e-13 for these five methods, so those speed-ups compare equal answers. astropy's Wald differs from ours by 9.6e-4 at `n=1000` (9.5e-3 at `n=100`), so that one cell is not like-for-like.
pynomial agrees with us only to 4e-4–1e-2 for Wilson/Wald/Agresti–Coull, and binoculars to ~6e-7–2e-6 (its limits differ in
the sixth decimal; its "wilson" is not identical to the standard Wilson interval). We did not investigate why; the time ratios against them
should be read with that in mind.

## C. Methods only DBCI also ships (`n` = 60)

| method | binomcikit | DBCI | speed-up | parity |
|---|---:|---:|---:|---:|
| Blaker | 5.2 ms | 14.17 s | 2724× | 9.9e-6 |
| mid-p | 4.0 ms | 168.6 ms | 42× | 5.0e-13 |
| likelihood ratio | 1.8 ms | 139.1 ms | 75× | 3.7e-13 |
| modified Jeffreys | 631 µs | 12.2 ms | 19× | 4.4e-16 |
| Pratt | 336 µs | 4.7 ms | 14× | **5.3e-2** |
| modified Wilson | 606 µs | 5.3 ms | 8.7× | **1.0** |

The three rows with a non-trivial parity are *disagreements about the answer*, so their speed-ups are not like-for-like.
* **Blaker:** DBCI steps the parameter in increments of 1e-5, hence the 1e-5 differences; our value is the exact root.
* **Pratt, modified Wilson:** DBCI's limits differ from ours materially (modified Wilson: by 1.0, i.e. an upper limit that
  is not mirrored). Our versions are covered by the tests in `tests/test_ext_*`; we have not filed an upstream report. See [comparison](comparison.md) for the DBCI defects found.

## D. Coverage-probability curve (2000 θ points)

| `n` | binomcikit | numpy/scipy reference | speed-up |
|---:|---:|---:|---:|
| 100 | 20.3 ms | 31.0 ms | 1.5× |
| 1000 | 5.5 ms | 425 ms | 78× |
| 10,000 | 21.7 ms | 5.61 s | 258× |

The reference is a straightforward vectorised numpy/scipy implementation of the same quantity, not another package's API; we
found no other Python package with a coverage-curve function to compare against. Parity ≤ 9e-12.

## E. Anytime-valid betting confidence sequence

Against `confseq` (the authors' reference implementation) the hedged-capital sequence over 1000 observations takes 7.1 ms
(`breaks=100`) and 65.3 ms (`breaks=1000`) versus 52.0 and 503.7 ms: **about 7.5×**, with identical output to 1e-16.
(`confseq` could not be pip-installed on this machine, so the benchmark imports its Python sources directly.)

## F. Methods only binomcikit has: absolute cost, including the slow ones

These have no competitor to compare with, so only the absolute time of the whole table is shown. Not everything is fast:

| method | n=50 | n=200 | n=1000 | n=5000 |
|---|---:|---:|---:|---:|
| Pratt | 710 µs | 610 µs | 974 µs | 2.7 ms |
| Hoeffding | 301 µs | 364 µs | 654 µs | 2.1 ms |
| Cressie–Read | 7.8 ms | 8.5 ms | 15.4 ms | 46.9 ms |
| higher-order likelihood (r*) | 7.2 ms | 9.3 ms | 16.1 ms | 49.2 ms |
| mixture confidence sequence | 3.0 ms | 4.1 ms | 7.4 ms | 23.8 ms |
| Chernoff / KL | 4.2 ms | 7.5 ms | 25.4 ms | 112 ms |
| length-optimal (OLC) | 3.6 ms | 13.9 ms | 86.7 ms | 413 ms |
| Blyth–Still–Casella | 37.8 ms | 131 ms | 718 ms | not run |
| **Sterne** | 8.6 ms | 50.8 ms | **548 ms** | **12.5 s** |
| **hedged betting (full table)** | 54.0 ms | 742 ms | **15.5 s** | not run |

Sterne now runs in about 0.5 s at `n=1000` and 12 s at `n=5000` (it was 3.3 s and 82 s before the 2026-10-03 pass, which replaced
`scipy.stats` calls in the inner loop with precomputed log-pmfs and `scipy.special` ufuncs; the limits are unchanged to ~1e-14).
The full-table betting interval takes about 16 s at `n=1000` (it was about 80 s; numba now runs chunks of rows in parallel, and the
table is bit-identical for a given seed). Betting is still the slowest method here, at roughly $O(B\,n^2)$ per table, and it needs
numba plus several cores to get that figure. Both are usable to a few hundred trials without waiting; no speed claim is made beyond that.

## What this does and does not show

* It shows large, reproducible gains over every loop-based package and over the old binomcikit code, with equal answers.
* It does **not** show that `bk.ci()` beats statsmodels or astropy for closed-form intervals; it does not. Use `bk.limits()`
  or `bk.interval()` when raw speed on those matters.
* One machine, one run, `n` at most 10,000 for tables. Timings under load vary (an earlier first pass looked slow only because
  of other processes running). The tables in sections A–E and the headline figures quoted above were measured on 2026-10-01; the
  full re-run on 2026-10-03 (`benchmarks/RESULTS.md`) is about 2× slower in absolute terms for *every* package, including code that
  did not change (e.g. the hedged betting sequence, 3.8 ms then, 7.1 ms now), so the machine was in a slower state; the ratios
  between packages agree between the two runs. Section F and the betting-sequence timings above are from the 2026-10-03 run.
