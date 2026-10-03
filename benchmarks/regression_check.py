"""Performance regression gate: fail when a tracked call gets more than ``--factor`` slower.

    python benchmarks/regression_check.py            # compare with benchmarks/baseline.json
    python benchmarks/regression_check.py --update   # re-record the baseline (do this on purpose)

Absolute times differ between machines (and between runs on a busy one: the 2026-10-03 benchmark
re-run was 2x slower than 2026-10-01 for *every* package), so each timing is divided by a
**calibration workload** timed in the same process (sorting 2M floats + 100k inverse-beta calls).
A regression is a call whose calibrated time rose by more than ``--factor`` (default 2x) over the
baseline's; machine speed cancels out, a slower algorithm does not.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time
import warnings

import numpy as np

warnings.filterwarnings("ignore")
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))

from scipy import special  # noqa: E402

import binomcikit as bk  # noqa: E402

BASELINE = HERE / "baseline.json"
ALPHA = 0.05


def best_time(fn, repeat=5, min_time=0.05):
    """Best per-call wall time over ``repeat`` samples of at least ``min_time`` seconds each."""
    fn()  # warm-up (caches, numba JIT)
    t0 = time.perf_counter()
    fn()
    first = time.perf_counter() - t0
    number = max(1, int(min_time / max(first, 1e-7)))
    best = float("inf")
    for _ in range(repeat):
        t = time.perf_counter()
        for _ in range(number):
            fn()
        best = min(best, (time.perf_counter() - t) / number)
    return best


def _calibration():
    rng = np.random.default_rng(0)
    data = rng.random(2_000_000)
    q = rng.random(100_000)

    def work():
        np.sort(data)
        special.betaincinv(3.0, 7.0, q)

    return best_time(work, repeat=5, min_time=0.2)


# The betting table is deliberately not tracked: its speed scales with the number of cores (numba
# parallel kernel), so a 2-core CI runner would look like a regression against a many-core baseline.
CASES = {
    "ci wilson n=1000": lambda: bk.ci(n=1000, alpha=ALPHA, method="wilson"),
    "ci wilson n=10000": lambda: bk.ci(n=10_000, alpha=ALPHA, method="wilson"),
    "ci exact n=1000": lambda: bk.ci(n=1000, alpha=ALPHA, method="exact"),
    "limits wilson n=10000": lambda: bk.limits(10_000, ALPHA, "wilson"),
    "limits exact n=10000": lambda: bk.limits(10_000, ALPHA, "exact"),
    "interval wilson (single)": lambda: bk.interval(300, 1000, ALPHA, "wilson"),
    "ci lr n=1000": lambda: bk.ci(n=1000, alpha=ALPHA, method="lr"),
    "ci adj-lr n=1000": lambda: bk.ci(n=1000, alpha=ALPHA, method="lr", h=2),
    "ci blaker n=200": lambda: bk.ci(n=200, alpha=ALPHA, method="blaker"),
    "ci sterne n=200": lambda: bk.ci(n=200, alpha=ALPHA, method="sterne"),
    "ci olc n=1000": lambda: bk.ci(n=1000, alpha=ALPHA, method="olc"),
}


def measure():
    cal = _calibration()
    out = {name: best_time(fn, repeat=3) / cal for name, fn in CASES.items()}
    return cal, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--update", action="store_true", help="re-record benchmarks/baseline.json")
    ap.add_argument(
        "--factor", type=float, default=2.0, help="fail above this slowdown (default 2)"
    )
    args = ap.parse_args()
    cal, now = measure()
    print(f"calibration workload: {cal * 1e3:.1f} ms")
    if args.update:
        BASELINE.write_text(
            json.dumps({"calibration_s": cal, "calibrated": now}, indent=1), encoding="utf-8"
        )
        print(f"wrote {BASELINE.name} ({len(now)} cases)")
        return 0
    base = json.loads(BASELINE.read_text(encoding="utf-8"))["calibrated"]
    bad = []
    for name, value in now.items():
        ratio = value / base[name] if name in base else float("nan")
        flag = "REGRESSION" if ratio > args.factor else "ok"
        if flag != "ok":
            bad.append(name)
        print(f"  {name:28s} {ratio:6.2f}x baseline  {flag}")
    missing = sorted(set(base) - set(now))
    if missing:
        print("cases in the baseline but no longer measured:", missing)
    if bad:
        print(f"FAIL: {len(bad)} case(s) more than {args.factor}x slower than the baseline")
        return 1
    print("all cases within the limit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
