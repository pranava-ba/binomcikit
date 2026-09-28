# CI eval comparison (example)

A copy-paste template, not a published/installable GitHub Action — two files:

- **`compare_eval_results.py`** — takes two `(correct, total)` pairs, computes a
  confidence interval for each with [binomcikit](https://github.com/pranava-ba/binomcikit),
  checks whether they overlap, and computes the statistical power to detect the
  observed gap. Prints a Markdown summary.
- **`example-workflow.yml`** — a GitHub Actions workflow showing how to wire
  the script into a PR: run your eval on the base and head commits, compare,
  post the result as a PR comment.

## Why

A 5-point gap between two model runs is easy to over-read. See
[`docs/tutorials/llm_eval_benchmark.md`](https://pranava-babinomcikit-rtd.readthedocs.io/en/latest/tutorials/llm_eval_benchmark.html)
in the binomcikit docs for the full worked example this template is built from.

## Using this

1. Copy both files into your own repo (`compare_eval_results.py` anywhere your
   workflow can reach it; `example-workflow.yml` into `.github/workflows/`,
   renamed).
2. `pip install binomcikit` in your CI environment.
3. Replace the two steps marked `ADAPT THIS` in the workflow with however your
   eval harness actually reports `correct`/`total` — this template has no
   opinion on your eval format; it only needs two integers per side.
4. If your two runs don't share the same `n`, this script will refuse (see the
   `ValueError` in `compare()`) — a genuinely different-`n` comparison needs
   two-proportion methods binomcikit doesn't ship yet (see
   `planning/ROADMAP.md`, "two-proportion inference" is scoped as a future
   sequel package). Run both sides on the same question set to use this as-is.

## Try it locally

```bash
pip install binomcikit
python compare_eval_results.py \
  --a-name baseline --a-correct 78 --a-total 100 \
  --b-name candidate --b-correct 83 --b-total 100
```
