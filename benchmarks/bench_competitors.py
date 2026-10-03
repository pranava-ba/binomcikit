"""Speed + parity benchmark: binomcikit against the other Python tools for binomial intervals.

    python benchmarks/bench_competitors.py                 # full run -> benchmarks/results.json
    python benchmarks/bench_competitors.py --quick         # small sizes, seconds
    python benchmarks/bench_competitors.py --markdown      # also (re)write benchmarks/RESULTS.md

What is measured
----------------
A. **table**    -- limits for *every* x = 0..n (what ``bk.ci(n=..., method=...)`` returns).
B. **single**   -- one interval, x = 0.3 n.
C. **exotic**   -- Blaker, Mid-P, Pratt, Witting-type, likelihood-ratio vs DBCI (the only other
                   package that ships them).
D. **evaluation** -- the coverage-probability curve of an interval (competitors ship no
                   evaluator, so the reference is the obvious numpy/scipy implementation).
E. **sequence** -- an anytime-valid betting confidence sequence vs ``confseq``.
F. **new**      -- absolute cost of the methods only binomcikit has (Sterne, Blyth-Still-Casella,
                   optimal locally correct, betting ...).

Every row also records **parity**: the largest absolute difference between a competitor's limits
and binomcikit's for the *same* method, so a fast-but-different answer cannot hide.

Timing is best-of-``repeat`` wall time per call (each sample is at least ``min_time`` seconds),
after a warm-up call that absorbs numba JIT compilation. All tools are given the same inputs.
Competitors that are not installed are skipped (and listed under ``missing``).
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import pathlib
import platform
import sys
import time
import warnings

import numpy as np

warnings.filterwarnings("ignore")
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))

import binomcikit as bk  # noqa: E402

ALPHA = 0.05


# ------------------------------------------------------------------------------- timing
def best_time(fn, min_time=0.05, repeat=5, max_total=20.0):
    """Best wall time (seconds) of ``fn()`` over ``repeat`` samples of >= ``min_time`` each."""
    t0 = time.perf_counter()
    fn()  # warm-up (JIT, caches)
    first = time.perf_counter() - t0
    if first > max_total / 3:  # too slow to repeat: one more sample only
        t = time.perf_counter()
        fn()
        return min(first, time.perf_counter() - t)
    number = max(1, int(min_time / max(first, 1e-7)))
    best = float("inf")
    for _ in range(repeat):
        t = time.perf_counter()
        for _ in range(number):
            fn()
        best = min(best, (time.perf_counter() - t) / number)
    return best


def maybe_import(name):
    try:
        return importlib.import_module(name)
    except Exception:
        return None


def version(mod):
    return getattr(mod, "__version__", None) or getattr(mod, "version", None) or "?"


# ------------------------------------------------------------------------ competitor shims
sm = maybe_import("statsmodels")
smp = maybe_import("statsmodels.stats.proportion")
scipy_stats = maybe_import("scipy.stats")
astropy_stats = maybe_import("astropy.stats")
dbci = maybe_import("diff_binom_confint")
pynomial = maybe_import("pynomial")
binoculars = maybe_import("binoculars")
binomial_cis = maybe_import("binomial_cis")


def _bk_table(method, n):
    return lambda: bk.ci(n=n, alpha=ALPHA, method=method)


def _bk_limits(method, n):
    df = bk.ci(n=n, alpha=ALPHA, method=method)
    cols = [c for c in df.columns if c[0] in "LU" and c not in ("LABB", "UABB")]
    return df[cols[0]].to_numpy(float), df[cols[1]].to_numpy(float)


# method name in each library for the five classics
SM = {"wilson": "wilson", "exact": "beta", "jeffreys": "jeffreys", "agresti-coull": "agresti_coull", "wald": "normal"}
AST = {"wilson": "wilson", "jeffreys": "jeffreys", "wald": "wald"}  # astropy has no exact interval
DB = {"wilson": "wilson", "exact": "clopper-pearson", "jeffreys": "jeffreys", "agresti-coull": "agresti-coull", "wald": "wald"}
PY = {"wilson": "wilson", "exact": "clopper_pearson", "agresti-coull": "agresti_coull", "wald": "wald"}
SC = {"wilson": "wilson", "exact": "exact"}


def competitors_table(method, n):
    """name -> (callable producing (lower, upper) arrays for every x, loop?)."""
    k = np.arange(n + 1)
    out = {}
    if smp and method in SM:
        out["statsmodels"] = lambda: smp.proportion_confint(k, n, alpha=ALPHA, method=SM[method])
    if astropy_stats and method in AST:
        out["astropy"] = lambda: astropy_stats.binom_conf_interval(k, n, confidence_level=1 - ALPHA, interval=AST[method])
    if scipy_stats and method in SC:
        def f():
            lo = np.empty(n + 1)
            hi = np.empty(n + 1)
            for i in range(n + 1):
                ci = scipy_stats.binomtest(i, n).proportion_ci(confidence_level=1 - ALPHA, method=SC[method])
                lo[i], hi[i] = ci.low, ci.high
            return lo, hi

        out["scipy (loop)"] = f
    if dbci and method in DB:
        def f():
            lo = np.empty(n + 1)
            hi = np.empty(n + 1)
            for i in range(n + 1):
                c = dbci.compute_confidence_interval(i, n, 1 - ALPHA, DB[method])
                lo[i], hi[i] = c.lower_bound, c.upper_bound
            return lo, hi

        out["DBCI (loop)"] = f
    if pynomial and method in PY:
        fn = getattr(pynomial, PY[method])

        def f():
            lo = np.empty(n + 1)
            hi = np.empty(n + 1)
            for i in range(n + 1):
                c = fn(i, n)
                lo[i], hi[i] = float(c.lower), float(c.upper)
            return lo, hi

        out["pynomial (loop)"] = f
    if binoculars and method in ("wilson", "exact", "jeffreys", "wald"):
        bm = {"wilson": "wilson", "exact": "clopper-pearson", "jeffreys": "jeffrey", "wald": "normal"}[method]

        def f():
            lo = np.empty(n + 1)
            hi = np.empty(n + 1)
            for i in range(n + 1):
                a, b = binoculars.binomial_confidence(i / n, n, method=bm)
                lo[i], hi[i] = a, b
            return lo, hi

        out["binoculars (loop)"] = f
    return out


def parity(method, n, comp_fn):
    try:
        ours = _bk_limits(method, n)
        lo, hi = comp_fn()
        lo, hi = np.asarray(lo, float), np.asarray(hi, float)
        inner = slice(1, n)  # boundary rows follow each package's own documented convention
        return float(max(np.nanmax(np.abs(lo[inner] - ours[0][inner])), np.nanmax(np.abs(hi[inner] - ours[1][inner]))))
    except Exception as e:  # pragma: no cover
        return f"error: {type(e).__name__}"


# ----------------------------------------------------------------------------- the tasks
def task_table(sizes, loop_cap):
    rows = []
    for method in ("wilson", "exact", "jeffreys", "agresti-coull", "wald"):
        for n in sizes:
            entry = {
                "task": "table",
                "method": method,
                "n": n,
                "binomcikit_s": best_time(_bk_table(method, n)),
                "binomcikit_arrays_s": best_time(lambda: bk.limits(n, ALPHA, method)),
            }
            comp = {}
            for name, fn in competitors_table(method, n).items():
                if "loop" in name and n > loop_cap:
                    continue
                comp[name] = {"s": best_time(fn, repeat=3), "parity": parity(method, n, fn)}
            entry["competitors"] = comp
            rows.append(entry)
            print(f"  table {method:14s} n={n:6d}  ci() {entry['binomcikit_s']*1e3:9.2f} ms  limits() "
                  f"{entry['binomcikit_arrays_s']*1e3:9.3f} ms  | "
                  + "  ".join(f"{k} {v['s']*1e3:.2f}" for k, v in comp.items()), flush=True)
    return rows


def task_single(n=1000):
    x = int(0.3 * n)
    rows = []
    for method in ("wilson", "exact", "jeffreys", "wald"):
        entry = {"task": "single", "method": method, "n": n, "binomcikit_s": best_time(lambda: bk.ci(x=x, n=n, alpha=ALPHA, method=method))}
        entry["binomcikit_arrays_s"] = best_time(lambda: bk.interval(x, n, ALPHA, method))
        comp = {}
        if smp and method in SM:
            comp["statsmodels"] = {"s": best_time(lambda: smp.proportion_confint(x, n, alpha=ALPHA, method=SM[method]))}
        if scipy_stats and method in SC:
            comp["scipy"] = {"s": best_time(lambda: scipy_stats.binomtest(x, n).proportion_ci(1 - ALPHA, method=SC[method]))}
        if astropy_stats and method in AST:
            comp["astropy"] = {"s": best_time(lambda: astropy_stats.binom_conf_interval(x, n, 1 - ALPHA, AST[method]))}
        if dbci and method in DB:
            comp["DBCI"] = {"s": best_time(lambda: dbci.compute_confidence_interval(x, n, 1 - ALPHA, DB[method]))}
        if pynomial and method in PY:
            fn = getattr(pynomial, PY[method])
            comp["pynomial"] = {"s": best_time(lambda: fn(x, n))}
        entry["competitors"] = comp
        rows.append(entry)
        print(f"  single {method:10s} n={n}  ci(x=) {entry['binomcikit_s']*1e6:8.1f} us  interval() {entry['binomcikit_arrays_s']*1e6:7.1f} us  | "
              + "  ".join(f"{k} {v['s']*1e6:.1f}" for k, v in comp.items()), flush=True)
    return rows


def task_exotic(n):
    rows = []
    pairs = {
        "blaker": ("blaker", "blaker"),
        "midp": ("midp", "mid-p"),
        "pratt": ("pratt", "pratt"),
        "lr": ("lr", "lik"),
        "modified-wilson": ("modified-wilson", "modified-wilson"),
        "modified-jeffreys": ("modified-jeffreys", "modified-jeffreys"),
    }
    for label, (bkm, dbm) in pairs.items():
        entry = {"task": "exotic", "method": label, "n": n, "binomcikit_s": best_time(_bk_table(bkm, n), repeat=3), "competitors": {}}
        if dbci:
            def f():
                lo = np.empty(n + 1)
                hi = np.empty(n + 1)
                for i in range(n + 1):
                    c = dbci.compute_confidence_interval(i, n, 1 - ALPHA, dbm)
                    lo[i], hi[i] = c.lower_bound, c.upper_bound
                return lo, hi

            entry["competitors"]["DBCI (loop)"] = {"s": best_time(f, repeat=2, max_total=60.0), "parity": parity(bkm, n, f)}
        rows.append(entry)
        print(f"  exotic {label:18s} n={n}  binomcikit {entry['binomcikit_s']*1e3:9.2f} ms  "
              + "  ".join(f"{k} {v['s']*1e3:.1f} (parity {v['parity']})" for k, v in entry["competitors"].items()), flush=True)
    return rows


def _reference_coverage(n, lower, upper, theta):
    """The obvious numpy/scipy coverage computation a user would write by hand."""
    from scipy import stats

    k = np.arange(n + 1)
    pmf = stats.binom.pmf(k[None, :], n, theta[:, None])
    cov = (theta[:, None] > lower[None, :]) & (theta[:, None] < upper[None, :])
    return (pmf * cov).sum(axis=1)


def task_evaluation(sizes, points=2000):
    rows = []
    theta = np.linspace(1e-4, 1 - 1e-4, points)
    for n in sizes:
        lo, hi = _bk_limits("wilson", n)
        ours = best_time(lambda: bk.coverage_curve(n, "wilson", points=points), repeat=3)
        ref = best_time(lambda: _reference_coverage(n, lo, hi, theta), repeat=2, max_total=60.0)
        a = bk.coverage_curve(n, "wilson", points=points).coverage.to_numpy()
        b = _reference_coverage(n, lo, hi, theta)
        rows.append({"task": "evaluation", "method": "wilson coverage curve", "n": n, "points": points,
                     "binomcikit_s": ours, "competitors": {"numpy/scipy reference": {"s": ref, "parity": float(np.abs(a - b).max())}}})
        print(f"  coverage n={n:6d}  binomcikit {ours*1e3:9.2f} ms   reference {ref*1e3:9.2f} ms  parity {np.abs(a - b).max():.1e}", flush=True)
    return rows


def task_sequence(T):
    rows = []
    # confseq needs a C++ toolchain to pip-install; its pure-Python betting module is enough here.
    # Point CONFSEQ_SRC at the sdist's `src/` directory (numpy>=2 users: replace `np.float_` by
    # `np.float64` in its sources) -- or leave unset to skip the confseq comparison.
    cs_path = pathlib.Path(os.environ.get("CONFSEQ_SRC", HERE / "_confseq_src"))
    confseq_betting = None
    if cs_path.exists():
        sys.path.insert(0, str(cs_path))
        confseq_betting = maybe_import("confseq.betting")
    rng = np.random.default_rng(3)
    seq = (rng.random(T) < 0.3).astype(float)
    for breaks in (100, 1000):
        entry = {"task": "sequence", "method": f"hedged betting CS (breaks={breaks})", "n": T,
                 "binomcikit_s": best_time(lambda: bk.cibetseq(seq, ALPHA, "hedged", running_intersection=False, breaks=breaks), repeat=2, max_total=60.0),
                 "competitors": {}}
        if confseq_betting is not None:
            f = lambda: confseq_betting.hedged_cs(seq, alpha=ALPHA, breaks=breaks, running_intersection=False)  # noqa: E731
            l, u = f()
            mine = bk.cibetseq(seq, ALPHA, "hedged", running_intersection=False, breaks=breaks)
            entry["competitors"]["confseq"] = {"s": best_time(f, repeat=2, max_total=120.0),
                                               "parity": float(max(np.abs(mine.lower.to_numpy() - l).max(), np.abs(mine.upper.to_numpy() - u).max()))}
        rows.append(entry)
        print(f"  sequence breaks={breaks:5d} T={T}  binomcikit {entry['binomcikit_s']*1e3:9.2f} ms  "
              + "  ".join(f"{k} {v['s']*1e3:.1f} ms (parity {v['parity']:.1e})" for k, v in entry["competitors"].items()), flush=True)
    return rows


def task_new(sizes):
    rows = []
    for method in ("sterne", "bsc", "olc", "lr-star", "cressie-read", "mixture", "betting", "pratt", "hoeffding", "chernoff"):
        for n in sizes:
            spec = bk.methods.REGISTRY.get(method)
            if spec is not None and spec.max_n is not None and n > spec.max_n:
                continue
            try:
                t = best_time(_bk_table(method, n), repeat=2, max_total=40.0)
            except Exception as e:  # pragma: no cover
                t = float("nan")
                print("   !", method, n, type(e).__name__, e)
            rows.append({"task": "new", "method": method, "n": n, "binomcikit_s": t, "competitors": {}})
            print(f"  new {method:14s} n={n:6d}  {t*1e3:10.2f} ms", flush=True)
    return rows


# ------------------------------------------------------------------------------ report
def environment():
    libs = {"python": platform.python_version(), "platform": platform.platform(), "processor": platform.processor()}
    for name in ("numpy", "scipy", "pandas", "numba", "statsmodels", "astropy", "diff_binom_confint", "pynomial", "binoculars", "binomial_cis"):
        m = maybe_import(name)
        libs[name] = version(m) if m else None
    libs["binomcikit"] = bk.__version__
    return libs


def fmt_time(s):
    if s != s:
        return "n/a"
    if s < 1e-3:
        return f"{s*1e6:,.0f} µs"
    if s < 1:
        return f"{s*1e3:,.1f} ms"
    return f"{s:,.2f} s"


def markdown(res):
    env = res["environment"]
    L = ["# Benchmarks — binomcikit vs the other Python tools\n",
         "> Auto-generated by [`bench_competitors.py`](bench_competitors.py); re-run it to reproduce. "
         "Times are best-of-N wall clock per call; **parity** is the largest absolute difference between "
         "the competitor's limits and binomcikit's for the same method (interior rows; each package's "
         "documented boundary convention aside). Lower time is better; *speed-up* = competitor ÷ binomcikit.\n",
         "## Environment\n", "| | |", "|---|---|"]
    L += [f"| {k} | {v} |" for k, v in env.items()]
    for task, title in (("table", "A. Whole table: limits for every x = 0..n"),
                        ("single", "B. A single interval"),
                        ("exotic", "C. Methods only DBCI also ships (whole table)"),
                        ("evaluation", "D. Coverage-probability curve (2 000 θ points)"),
                        ("sequence", "E. Anytime-valid betting confidence sequence"),
                        ("new", "F. Methods only binomcikit has (absolute cost)")):
        rows = [r for r in res["rows"] if r["task"] == task]
        if not rows:
            continue
        L.append(f"\n## {title}\n")
        if task == "new":
            L += ["| method | n | time |", "|---|---:|---:|"]
            L += [f"| `{r['method']}` | {r['n']:,} | {fmt_time(r['binomcikit_s'])} |" for r in rows]
            continue
        has_arr = any(r.get("binomcikit_arrays_s") for r in rows)
        if has_arr:
            fast = "`bk.interval()` (floats)" if task == "single" else "`bk.limits()` (arrays)"
            L += [f"| method | n | `bk.ci()` (DataFrame) | {fast} | competitor | time | vs `ci()` | vs lean path | parity |",
                  "|---|---:|---:|---:|---|---:|---:|---:|---:|"]
        else:
            L += ["| method | n | binomcikit | competitor | time | speed-up | parity |", "|---|---:|---:|---|---:|---:|---:|"]
        for r in rows:
            comps = r["competitors"] or {"—": {"s": float("nan")}}
            first = True
            for name, c in comps.items():
                sp = c["s"] / r["binomcikit_s"] if c["s"] == c["s"] and r["binomcikit_s"] > 0 else float("nan")
                par = c.get("parity")
                par_s = "" if par is None else (f"{par:.1e}" if isinstance(par, float) else str(par))
                sp_s = '**%.1f×**' % sp if sp == sp else ''
                if has_arr:
                    arr = r.get("binomcikit_arrays_s")
                    spa = c["s"] / arr if arr and c["s"] == c["s"] else float("nan")
                    L.append(f"| {r['method'] if first else ''} | {r['n']:,} | {fmt_time(r['binomcikit_s']) if first else ''} | "
                             f"{fmt_time(arr) if (first and arr) else ''} | {name} | {fmt_time(c['s'])} | {sp_s} | "
                             f"{'**%.1f×**' % spa if spa == spa else ''} | {par_s} |")
                else:
                    L.append(f"| {r['method'] if first else ''} | {r['n']:,} | {fmt_time(r['binomcikit_s']) if first else ''} | "
                             f"{name} | {fmt_time(c['s'])} | {sp_s} | {par_s} |")
                first = False
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--markdown", action="store_true")
    ap.add_argument("--out", default=str(HERE / "results.json"))
    args = ap.parse_args()
    sizes = [50, 200] if args.quick else [100, 1000, 10_000]
    loop_cap = 200 if args.quick else 2000
    exotic_n = 40 if args.quick else 60
    cov_sizes = [100, 1000] if args.quick else [100, 1000, 10_000]
    new_sizes = [50, 200] if args.quick else [50, 200, 1000, 5000]

    bk.ci(n=20, alpha=ALPHA, method="blaker")  # absorb JIT before any timing
    res = {"environment": environment(), "rows": []}
    print("A. table"); res["rows"] += task_table(sizes, loop_cap)
    print("B. single"); res["rows"] += task_single()
    print("C. exotic"); res["rows"] += task_exotic(exotic_n)
    print("D. evaluation"); res["rows"] += task_evaluation(cov_sizes)
    print("E. sequence"); res["rows"] += task_sequence(200 if args.quick else 1000)
    print("F. new methods"); res["rows"] += task_new(new_sizes)
    pathlib.Path(args.out).write_text(json.dumps(res, indent=1, default=str))
    if args.markdown:
        (HERE / "RESULTS.md").write_text(markdown(res), encoding="utf-8")
        print("wrote RESULTS.md")


if __name__ == "__main__":
    main()
