# Estimating a single binomial proportion

## The problem

You observe `x` successes in `n` independent yes/no trials and want to say
something about the *true* success probability `p`. The point estimate is
obvious — `p̂ = x/n` — but a single number hides its uncertainty. A **confidence
interval** gives a range of plausible values for `p` at a stated confidence
level `1 − α` (α is the argument `alp`).

This sounds simple, but the binomial is discrete and bounded to `[0, 1]`, so the
usual normal-approximation interval misbehaves near the edges and for small `n`.
That is exactly why there are many methods — and why *evaluating* them matters.

## The methods

`binomcikit` implements six interval methods, each with a two-letter code.

```{list-table}
:header-rows: 1

* - Method
  - Code
  - Idea
* - **Wald**
  - `wd`
  - `p̂ ± z·√(p̂q̂/n)` — the textbook interval. Simple, but under-covers and can
    give zero-width intervals at `x = 0` or `x = n`.
* - **Score (Wilson)**
  - `sc`
  - Invert the score test. Stays inside `[0, 1]`, good coverage even for small
    `n`. The usual recommended default.
* - **ArcSine**
  - `as`
  - Build the interval on the variance-stabilising `arcsin(√p̂)` scale, then
    transform back.
* - **Likelihood-Ratio**
  - `lr`
  - Keep the values of `p` not rejected by the likelihood-ratio test. No closed
    form — solved numerically.
* - **Logit-Wald**
  - `lt`
  - A Wald interval on the log-odds scale; always strictly inside `(0, 1)`.
* - **Wald-T**
  - `tw`
  - Wald with a Student-*t* critical value and an adjusted standard error;
    slightly wider for small `n`.
* - **Exact**
  - `ex`
  - Invert the binomial tails. `e = 1` gives Clopper–Pearson, `e = 0.5` gives
    mid-*p*. Guaranteed coverage, at the cost of width.
```

## Base, adjusted, and continuity-corrected

Every method comes in three flavours:

- **Base** — the method as stated above (`ciwd`, `cisc`, …).
- **Adjusted** (`cia…`, takes `h`) — first replace `x, n` with `x + h, n + 2h`
  (pseudo-counts). With `h = 2` this is the well-known Agresti–Coull idea; it
  fixes the degenerate behaviour at the extremes.
- **Continuity-corrected** (`cic…`, takes `c`) — widen each limit by a small
  correction `c ≤ 1/(2n)` to compensate for the discreteness of the binomial.

## All-x versus given-x

Most functions compute the interval for **every** possible `x = 0…n` (handy for
studying a method), returning one row per `x`:

```python
import binomcikit as bk
bk.cisc(20, 0.05)          # Wilson interval for x = 0, 1, ..., 20
```

Append `x` to the name for the **single** count you actually observed:

```python
bk.ciscx(7, 20, 0.05)      # just x = 7 of 20
```

## Running all methods at once

`ciall` (and `ciaall`, `cicall`) stacks every method into one long-format table
with a `method` column — ideal for a side-by-side comparison or a plot:

```python
df = bk.ciall(20, 0.05)
df["method"].unique()
# ['Wald' 'ArcSine' 'Likelihood' 'Score' 'Wald-T' 'Logit-Wald']
```

Next: {doc}`which method should you actually use? <choosing_a_method>`
