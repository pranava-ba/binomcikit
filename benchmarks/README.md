# Performance benchmarks — language & backend decision

> **Question (raised before building out Phase 1):** should binomcikit be a Python package, or
> would a compiled language (Rust / C++ / Haskell) give a materially faster, lighter package?
> **Answer (evidence below): stay Python-core; add *optional* numba acceleration for the hot
> kernels. A full compiled-language rewrite is not justified.** Reproduce with the scripts here.
> Measured 2026-07-23 · Python 3.13.5, numpy 2.3.2, scipy 1.16.1, numba 0.65.1, GHC 9.4.8
> (Rust/Cargo not installed; not needed — see conclusion).

## Method
Two kernels that represent the real workloads:
- **(A) coverage kernel** — `C(θ)` over an *S*-point θ grid (the dominant metric workload; what
  `covp*`/`length*` do). Run as pure-Python loop, vectorized numpy (**the current impl**), numba
  (LLVM-compiled), and — as a compiled-language cross-check — Haskell (GHC ‑O2).
- **(B) root-finding loop** — *n+1* scalar monotone solves (the shape of LR / exact-`e`). Run as a
  `scipy.optimize.brentq` loop vs a numba-compiled bisection.

Timing = best of 7 (Python) / mean of 20 (Haskell), warm caches, JIT compiled before timing.
Scripts: [`bench_kernels.py`](bench_kernels.py), [`bench_coverage.hs`](bench_coverage.hs).

## (A) Coverage kernel — ms per call
| n | S | pure-Python | **numpy (current)** | **numba** | Haskell (GHC ‑O2) |
|---:|---:|---:|---:|---:|---:|
| 20 | 1 000 | 55.4 | 3.0 | 1.5 | – |
| 20 | 5 000 | 512.8 | 28.6 | 7.2 | – |
| 20 | 50 000 | 4 976 | 272 | 74 | – |
| 100 | 1 000 | 103.7 | 26.9 | 4.3 | – |
| 100 | 5 000 | 520.0 | 142.2 | 21.9 | – |
| 100 | 50 000 | 5 284 | 1 357 | 223 | – |
| 500 | 1 000 | 103.9 | 169.4 | 3.5 | – |
| 500 | 5 000 | 567.7 | 764.4 | 17.3 | – |
| 500 | 50 000 | 5 528 | **7 762** | **176** | **380** |

## (B) Root-finding loop — ms for n+1 solves
| roots | scipy.brentq | numba bisect | speedup |
|---:|---:|---:|---:|
| 21 | 0.44 | 0.009 | 47× |
| 101 | 2.07 | 0.034 | 61× |
| 501 | 10.60 | 0.171 | 62× |
| 2 001 | 44.42 | 1.35 | 33× |

## Lightness
- Core import (no plotting): **~2.2 s**, of which **~1.9 s is numpy+scipy+pandas** — i.e. the
  weight is the scientific stack, not our code.
- Install footprint: numpy 33 MB + scipy 120 MB + pandas 65 MB ≈ **218 MB** (again, the stack).

## What the numbers say
1. **Vectorized numpy is excellent for small *n* (the common case)** — 18× over a pure-Python loop
   at n=20. **But it degrades badly at large *n***: it materializes a dense `S×(n+1)` PMF matrix and
   pays scipy's per-element `binom.pmf` cost, so at n=500 it is *slower than pure Python* (0.6–0.7×).
   The shipped engine is the right default for typical binomial-proportion sizes, not a universal win.
2. **numba is 2–48× over numpy on the coverage kernel** (the gap grows with *n*, because it skips
   uncovered `x` and never materializes the matrix) and **33–62× over `scipy.brentq`** for root-finding.
3. **numba reaches compiled-language speed.** At the hardest point it beat idiomatic Haskell
   (176 ms vs 380 ms); optimized Rust/C++/Haskell would all land in the ~100–400 ms band — **within
   ~2–3× of numba, not orders of magnitude.** The algorithm is simple numeric loops, so LLVM (numba)
   and a Rust/C++ compiler produce comparable code.
4. **"Lighter" via a compiled rewrite is illusory** for a *Python* deliverable: the 218 MB / 1.9 s is
   numpy+scipy+pandas, which we keep for DataFrame outputs, `scipy.stats`, and ecosystem integration
   (goals 1–3). A Rust **PyO3** extension is *heavier* (compiled artifact + per-platform wheels +
   `maturin`), not lighter. A pure-Rust binary would be light — but is a different product.

## Decision
- **Python core** (numpy / scipy / pandas) — for correctness, DataFrame outputs, `scipy.stats`, and
  the Streamlit/PyQt/PyPI deliverables.
- **Optional `[fast]` numba acceleration** for the hot kernels — the metric engines at large *n*, the
  LR / exact-`e` root-finding, and the future Monte-Carlo / bootstrap / betting loops. Auto-used when
  installed; pure numpy/scipy fallback otherwise. Prebuilt wheels; no user toolchain.
- **No Rust / C++ / Haskell rewrite, and no need to install Rust.** Revisit *only* if a future
  profiled bottleneck shows numba is insufficient **and** the wheel-matrix cost is acceptable — or if
  the goal changes to a standalone non-Python binary.
- **Also (independent of language):** consider a smarter numpy coverage engine that skips uncovered
  `x` for the large-*n* path even without numba.

_See [`../planning/ROADMAP.md`](../planning/ROADMAP.md) §6 for how this folds into the build plan._
