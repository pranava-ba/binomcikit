# Choosing a method

No single interval is best in every situation. The choice trades off three
things: **coverage** (does it actually contain `p` at the stated rate?),
**width** (how precise is it?), and **behaviour at the extremes** (`p` near 0 or
1, or small `n`).

## Quick guidance

```{list-table}
:header-rows: 1

* - If you want…
  - Use
  - Why
* - A sensible default
  - **Score / Wilson** (`cisc`)
  - Good coverage across the board, stays in `[0, 1]`, no tuning.
* - Guaranteed (conservative) coverage
  - **Exact** (`ciex`, `e = 1`)
  - Clopper–Pearson never under-covers; it is just wider.
* - Something less conservative than exact but still safe
  - **Exact mid-p** (`ciex`, `e = 0.5`), or **adjusted Wald** (`ciawd`, `h = 2`)
  - Shorter than Clopper–Pearson while keeping coverage near nominal.
* - The familiar textbook interval
  - **Wald** (`ciwd`)
  - Fine for large `n` and `p̂` away from 0/1 — but know its flaws.
* - Well-behaved limits at extreme `p̂`
  - **Logit-Wald** (`cilt`) or **ArcSine** (`cias`)
  - Transform-based; limits stay strictly inside `(0, 1)`.
```

## Why not just always use Wald?

The Wald interval **under-covers** — its true coverage is often well below the
nominal `1 − α`, badly so for small `n` or `p̂` near the boundary — and it
produces a **zero-width interval** at `x = 0` and `x = n`. You can see this
directly:

```python
import binomcikit as bk
bk.ciwd(5, 0.05)
#    x       LWD       UWD LABB UABB  ZWI
# 0  0  0.000000  0.000000   NO   NO  YES   <- zero width!
# 1  1  0.000000  0.550609  YES   NO   NO
```

## Don't guess — measure

The whole point of `binomcikit` is that you don't have to take these claims on
faith. The evaluation families let you *quantify* the trade-off for your own `n`
and prior beliefs about `p`:

```python
import binomcikit as bk
args = dict(n=20, alp=0.05, a=1, b=1, t1=0.9, t2=0.97, seed=0)

bk.covpwd(**args)["mcp"][0]   # mean coverage of Wald
bk.covpsc(**args)["mcp"][0]   # mean coverage of Wilson — noticeably higher
```

The next page explains coverage and the other three evaluation criteria in
detail: {doc}`evaluating an interval <evaluating_intervals>`.
