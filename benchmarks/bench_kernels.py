"""Rigorous micro-benchmark for the binomcikit hot paths.

Two representative kernels:
  (A) coverage-probability over an S-point theta grid   -> the dominant workload
  (B) n+1 scalar root solves                             -> LR / exact-e style

Compared across:  pure-Python loop  |  vectorized numpy (current impl)  |  numba (compiled).
"""
import time

import numpy as np
from scipy import stats
from scipy.optimize import brentq

REPS = 7


def best(fn, *a):
    fn(*a)  # warmup (also triggers numba JIT compile)
    ts = []
    for _ in range(REPS):
        t0 = time.perf_counter()
        fn(*a)
        ts.append(time.perf_counter() - t0)
    return min(ts)


# --- (A) coverage kernel --------------------------------------------------
def cov_py(n, lo, hi, hp):
    x = np.arange(n + 1)
    out = np.empty(len(hp))
    for j in range(len(hp)):
        m = (hp[j] > lo) & (hp[j] < hi)
        out[j] = np.sum(stats.binom.pmf(x[m], n, hp[j]))
    return out


def cov_vec(n, lo, hi, hp):
    x = np.arange(n + 1)
    covered = (hp[:, None] > lo[None, :]) & (hp[:, None] < hi[None, :])
    pmf = stats.binom.pmf(x[None, :], n, hp[:, None])
    return (pmf * covered).sum(axis=1)


NUMBA = True
try:
    from math import exp, lgamma, log

    from numba import njit

    @njit(cache=True, fastmath=True)
    def cov_numba(n, lo, hi, hp):
        S = hp.shape[0]
        out = np.empty(S)
        lfn = lgamma(n + 1.0)
        for j in range(S):
            p = hp[j]
            lp = log(p)
            lq = log(1.0 - p)
            s = 0.0
            for k in range(n + 1):
                if lo[k] < p < hi[k]:
                    s += exp(lfn - lgamma(k + 1.0) - lgamma(n - k + 1.0) + k * lp + (n - k) * lq)
            out[j] = s
        return out

    @njit(cache=True)
    def roots_numba(targets):
        out = np.empty(targets.shape[0])
        for i in range(targets.shape[0]):
            lo, hi, t = 0.0, 1.0, targets[i]
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if mid * mid * mid - t > 0.0:
                    hi = mid
                else:
                    lo = mid
            out[i] = 0.5 * (lo + hi)
        return out

except Exception as e:  # noqa: BLE001
    NUMBA = False
    print("numba unavailable:", e)


def limits(n):
    x = np.arange(n + 1)
    p = x / n
    half = 1.96 * np.sqrt(np.maximum(p * (1 - p), 1e-9) / n) + 0.5 / n
    return np.clip(p - half, 0, 1), np.clip(p + half, 0, 1)


# --- (B) root-finding loop ------------------------------------------------
def roots_scipy(targets):
    return np.array([brentq(lambda th, t=t: th**3 - t, 0.0, 1.0) for t in targets])


print("=" * 78)
print("(A) COVERAGE KERNEL   C(theta) over S grid points")
print(f"{'n':>4} {'S':>7} | {'py (ms)':>10} {'numpy (ms)':>11} {'numba (ms)':>11} | "
      f"{'numpy/py':>9} {'numba/numpy':>12}")
for n in (20, 100, 500):
    lo, hi = limits(n)
    for S in (1000, 5000, 50000):
        hp = np.sort(np.random.default_rng(0).beta(1, 1, S))
        tpy = best(cov_py, n, lo, hi, hp)
        tvec = best(cov_vec, n, lo, hi, hp)
        line = f"{n:4d} {S:7d} | {tpy*1e3:10.2f} {tvec*1e3:11.2f} "
        if NUMBA:
            tnb = best(cov_numba, n, lo, hi, hp)
            assert np.allclose(cov_vec(n, lo, hi, hp), cov_numba(n, lo, hi, hp), atol=1e-9)
            line += f"{tnb*1e3:11.2f} | {tpy/tvec:8.1f}x {tvec/tnb:11.1f}x"
        else:
            line += f"{'--':>11} | {tpy/tvec:8.1f}x {'--':>12}"
        print(line)

print("=" * 78)
print("(B) ROOT-FINDING LOOP   n+1 monotone solves (LR / exact-e style)")
print(f"{'roots':>6} | {'scipy.brentq (ms)':>18} {'numba bisect (ms)':>18} | {'speedup':>9}")
for n in (20, 100, 500, 2000):
    targets = np.linspace(0.01, 0.99, n + 1)
    ts = best(roots_scipy, targets)
    if NUMBA:
        tn = best(roots_numba, targets)
        print(f"{n+1:6d} | {ts*1e3:18.3f} {tn*1e3:18.3f} | {ts/tn:8.1f}x")
    else:
        print(f"{n+1:6d} | {ts*1e3:18.3f} {'--':>18} | {'--':>9}")
print("=" * 78)
