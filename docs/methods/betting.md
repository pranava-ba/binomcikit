---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Betting and anytime-valid intervals

A fixed-n 95% interval is 95% **only if you chose n in advance.** Peek after every observation and stop when the
interval excludes a value you dislike, and its true error rate balloons — the "peeking problem" of every online A/B
test, dashboard and LLM benchmark. A {term}`confidence sequence` fixes it: a whole sequence of intervals that *all*
contain the truth simultaneously with probability ≥ 1 − α, so you may look as often as you like.

| Tool | What it gives | Depends on |
|---|---|---|
| `"mixture"` | the exact Beta-mixture {term}`confidence sequence` as an ordinary interval table | `(x, n)` only |
| `"normal-mixture"` | Robbins' normal-mixture boundary with a sub-Gaussian variance proxy | `(x, n)` only |
| `"betting"` | the hedged-capital {term}`betting interval` of Waudby-Smith & Ramdas, {term}`derandomisation`-averaged | `(x, n)`; slowest method |
| `bk.cibetseq(data, method=...)` | the genuine streaming sequence on your 0/1 data | the ordered stream |

## Use it

```{code-cell} python
import numpy as np
import binomcikit as bk

# a running experiment: true conversion rate 30%
rng = np.random.default_rng(3)
stream = (rng.random(400) < 0.30).astype(int)

cs = bk.cibetseq(stream, alpha=0.05, method="mixture")
cs.iloc[[9, 49, 99, 199, 399]].round(3)
```

Every row is a valid 95% interval **and all of them hold at once** — you can stop at row 49, or 99, or the first
moment the interval clears your target. Compare with a naive fixed-n Wilson interval recomputed after every
observation:

```{code-cell} python
def peeking_error(method, theta=0.30, T=150, reps=300, seed=1):
    """P(the truth is ever excluded at any of T looks) -- the real error rate under peeking."""
    rng = np.random.default_rng(seed)
    bad = 0
    for _ in range(reps):
        s = (rng.random(T) < theta).astype(int)
        if method == "wilson":
            t = np.arange(1, T + 1)
            x = np.cumsum(s)
            lo = np.array([bk.interval(int(xi), int(ti), 0.05, "wilson")[0] for xi, ti in zip(x, t)])
            hi = np.array([bk.interval(int(xi), int(ti), 0.05, "wilson")[1] for xi, ti in zip(x, t)])
        else:
            cs_ = bk.cibetseq(s, 0.05, method=method, running_intersection=False)
            lo, hi = cs_.lower.to_numpy(), cs_.upper.to_numpy()
        bad += bool(((lo > theta) | (hi < theta)).any())
    return bad / reps

print("Wilson, re-checked after every observation: error rate", round(peeking_error("wilson"), 3), " (nominal 0.05)")
print("Beta-mixture confidence sequence           : error rate", round(peeking_error("mixture"), 3), " (<= 0.05 guaranteed)")
```

Peeking at a Wilson interval multiplies its error rate several times over (about 0.38 against a nominal 0.05 in the run above);
the confidence sequence stays at or below the nominal 5% (0.04 here; with 300 replications the Monte-Carlo error is about ±0.01) —
that is the whole point.

### As an ordinary interval table

```{code-cell} python
bk.compare(3, 20, methods=["wilson", "exact", "mixture", "normal-mixture", "betting", "hoeffding"])
```

The anytime-valid intervals are wider than the fixed-n ones. That is the **price of optional stopping**, not a defect:
they are valid at *every* n simultaneously. Among them, hedged betting adapts to the variance, so it pulls ahead as n
grows — at n = 20 there is little data for it to adapt to.

## Understand it

**Testing by betting.** For each candidate mean $m$ a gambler starts with capital 1 and bets that the true mean is
not $m$. If the data really have mean $m$ the bets are fair, so the capital is a {term}`martingale`. By
{term}`Ville's inequality` the chance it *ever* reaches $1/\alpha$ is at most $\alpha$ — so any $m$ that lets the gambler get
rich is rejected, and the set of un-rejectable $m$ is a $(1-\alpha)$ {term}`confidence sequence`.

**Mixture.** Instead of one bet, average the capital over a Beta($a$, $b$) prior on the alternative. For Bernoulli data this
{term}`mixture martingale` is a closed form,

$$M_n(m)=\frac{B(a+x,\;b+n-x)}{B(a,b)}\;m^{-x}(1-m)^{-(n-x)},$$

so the interval $\{m: M_n(m)<1/\alpha\}$ is cut out by a unimodal function of $m$ and needs two scalar roots. The test-suite checks each
limit by integrating the mixture numerically.

**Hedged betting.** Waudby-Smith & Ramdas run two bets at once — "the mean is above $m$" and "below $m$" — and take
$\max\{\theta K^{+},(1-\theta)K^{-}\}$, with *predictable plug-in* bet sizes that depend only on the data seen so far:
$\lambda_t=\sqrt{2\ln(2/\alpha)/(n\,\hat\sigma^2_{t-1})}$ (truncated at $c/m$). It depends on the **order** of the
observations, so the table version averages the capital over $B$ random orderings — valid by Markov's inequality — giving a
{term}`derandomisation` that depends on $(x,n)$ alone. Our implementation reproduces the authors' reference code (`confseq`)
**to 1e-16** on a fixed sequence, and is roughly eight to ten times faster (see {doc}`../benchmarks`):

```{code-cell} python
import time

seq = (np.random.default_rng(0).random(300) < 0.3).astype(float)
t = time.perf_counter(); out = bk.cibetseq(seq, 0.05, "hedged", breaks=500, running_intersection=False); dt = time.perf_counter() - t
print(f"hedged confidence sequence, 300 observations, 500-point grid: {dt*1e3:.0f} ms")
out.iloc[[19, 99, 299]].round(3)
```

## When to use which

* **Online experiments, dashboards, LLM-eval leaderboards that grow** → `"mixture"` / `cibetseq(method="mixture")` (exact,
  fast, depends only on counts).
* **You have the stream and want the tightest** → `cibetseq(method="hedged")` or `"preb"` (closed form).
* **A one-off, fixed-n study** → use a fixed-n interval ({doc}`wilson`, {doc}`extended_exact`); anytime validity costs width you do not need.

## References

Waudby-Smith & Ramdas (2024), *Estimating means of bounded random variables by betting*, JRSS-B 86 (arXiv:2010.09686) ·
Howard, Ramdas, McAuliffe & Sekhon (2021), *Time-uniform, nonparametric, nonasymptotic confidence sequences*, Ann. Statist. 49 ·
Robbins (1970) · an enterprise deployment on Adobe Experience Platform: arXiv:2302.10108.
