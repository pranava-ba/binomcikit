#!/usr/bin/env python3
"""Compare two LLM-eval pass/fail results and print a PR-comment-ready summary.

Standalone example, not part of the binomcikit package itself -- copy this file
(and adapt the two counts to however your eval harness reports results) into
your own repo's CI. See README.md in this directory for the GitHub Actions
wiring, and docs/tutorials/llm_eval_benchmark.md in the binomcikit docs for the
statistics behind it (overlapping confidence intervals, and why "5 points
better" isn't automatically real).

Usage
-----
    python compare_eval_results.py \\
        --a-name "baseline" --a-correct 78 --a-total 100 \\
        --b-name "candidate" --b-correct 83 --b-total 100

Exit code is always 0 -- this reports, it doesn't gate the build. Wire an
explicit `--fail-under-power N` check into your own pipeline if you want the
build to fail when a benchmark is too small to trust.
"""

from __future__ import annotations

import argparse
import sys

import binomcikit as bk


def compare(
    a_name: str,
    a_correct: int,
    a_total: int,
    b_name: str,
    b_correct: int,
    b_total: int,
    alpha: float = 0.05,
    method: str = "wilson",
) -> str:
    if a_total != b_total:
        # power() assumes both models see the same n; a genuinely different-n
        # comparison needs the two-proportion methods binomcikit doesn't (yet)
        # ship -- see planning/ROADMAP.md ("two-proportion inference" sequel).
        raise ValueError(
            f"a_total ({a_total}) != b_total ({b_total}) -- this script assumes both "
            "models were run on the same n questions"
        )
    n = a_total

    ci_a = bk.ci(a_correct, n, method=method, alpha=alpha)
    ci_b = bk.ci(b_correct, n, method=method, alpha=alpha)
    lo_col = [c for c in ci_a.columns if c.startswith("L")][0]
    hi_col = [c for c in ci_a.columns if c.startswith("U")][0]
    a_lo, a_hi = float(ci_a[lo_col].iloc[0]), float(ci_a[hi_col].iloc[0])
    b_lo, b_hi = float(ci_b[lo_col].iloc[0]), float(ci_b[hi_col].iloc[0])
    overlap = not (a_hi < b_lo or b_hi < a_lo)

    gap = abs(b_correct - a_correct) / n
    hi_theta0, lo_p_true = (
        (a_correct / n, b_correct / n) if b_correct >= a_correct else (b_correct / n, a_correct / n)
    )
    detected = bk.power(n, hi_theta0, lo_p_true, alpha=alpha, method=method)

    lines = [
        f"### Eval comparison ({method}, {int((1 - alpha) * 100)}% CI, n={n})",
        "",
        f"| | correct/n | score | {int((1 - alpha) * 100)}% CI |",
        "|---|---|---|---|",
        f"| {a_name} | {a_correct}/{n} | {a_correct / n:.1%} | [{a_lo:.1%}, {a_hi:.1%}] |",
        f"| {b_name} | {b_correct}/{n} | {b_correct / n:.1%} | [{b_lo:.1%}, {b_hi:.1%}] |",
        "",
    ]
    if overlap:
        lines.append(
            f"⚠️ **Confidence intervals overlap.** The {gap:.1%} gap between `{a_name}` and "
            f"`{b_name}` may just be noise at this sample size. Power to detect a real gap "
            f"this size at n={n} is **{detected:.0%}**."
        )
    else:
        lines.append(
            f"✅ Confidence intervals do not overlap -- the {gap:.1%} gap is unlikely to be "
            f"noise alone at n={n}."
        )
    lines.append(
        "\n_Computed with [binomcikit](https://github.com/pranava-ba/binomcikit) "
        f'(`bk.ci(..., method="{method}")` / `bk.power(...)`)._'
    )
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--a-name", default="A")
    p.add_argument("--a-correct", type=int, required=True)
    p.add_argument("--a-total", type=int, required=True)
    p.add_argument("--b-name", default="B")
    p.add_argument("--b-correct", type=int, required=True)
    p.add_argument("--b-total", type=int, required=True)
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--method", default="wilson")
    args = p.parse_args()

    # Windows consoles default to a non-UTF-8 codepage that can't print the
    # status emoji below; GitHub Actions runners are already UTF-8, so this
    # is a no-op there and only matters when testing locally on Windows.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print(
        compare(
            args.a_name,
            args.a_correct,
            args.a_total,
            args.b_name,
            args.b_correct,
            args.b_total,
            alpha=args.alpha,
            method=args.method,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
