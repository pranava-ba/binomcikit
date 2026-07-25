---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Trials and the binomial

## In words

The count $x$ from the last page does not fall from the sky — it is built up from individual yes/no
events. Each visitor either clicks or not; each part is either defective or not; each coin lands heads or
not. One such event, with two outcomes and a fixed chance of "success," is a **trial**. Line up $n$ of
them, assume they do not influence each other and all share the same success chance $\theta$, and count
the successes. That count is what the **binomial distribution** describes: for a given $\theta$, how
likely is *each* possible total $0, 1, 2, \dots, n$?

The picture to hold in mind: the binomial is a set of bars, one per possible count, whose heights are the
probabilities and which always sum to 1. It is tall in the middle (near $n\theta$ successes) and short in
the tails. Everything the package does is, underneath, a statement about this distribution.

## The symbols

| Symbol | Reads as | Means |
|---|---|---|
| $\theta$ | "theta" | the success chance on a single {term}`trial` (same for all trials) |
| $n$ | "n" | the number of trials |
| $x$ | "x" | a particular number of successes, from 0 to $n$ |
| $X$ | "big X" | the count *before* we see it — a {term}`random variable` |
| $\binom{n}{x}$ | "n choose x" | the number of different orders in which $x$ successes can occur |
| $\Pr(X=x)$ | "P of X equals x" | the probability the count comes out exactly $x$ |

The distinction between little $x$ (a specific value, like 14) and big $X$ (the count as a
{term}`random variable`, before it is observed) is worth keeping: the binomial formula gives the
probability that the random $X$ *equals* a particular $x$.

## Definition

$$\Pr(X = x) \;=\; \binom{n}{x}\,\theta^{x}\,(1-\theta)^{\,n-x}, \qquad x = 0, 1, \dots, n.$$

Read it left to right: $\theta^{x}$ is the chance of $x$ specific successes, $(1-\theta)^{n-x}$ the chance
of the remaining failures, and $\binom{n}{x}$ counts how many arrangements give that many successes. This
is the {term}`binomial` {term}`probability` of the count. The true rate {term}`theta` is the one unknown;
$n$ is known and $x$ is what you observe.

## Examples

A hand-workable case first — $n = 5$, $\theta = 0.4$, and we want exactly $x = 2$ successes.
By hand: $\binom{5}{2} = 10$, so $\Pr(X=2) = 10 \times 0.4^{2} \times 0.6^{3} = 10 \times 0.16 \times
0.216 = 0.3456$. Now check it:

```{code-cell} python
from math import comb

n, theta, x = 5, 0.4, 2
prob = comb(n, x) * theta**x * (1 - theta) ** (n - x)
round(prob, 4)      # matches the 0.3456 we computed by hand
```

The probabilities over *all* possible counts must add to 1 — every experiment produces *some* total:

```{code-cell} python
n, theta = 5, 0.4
pmf = [comb(n, x) * theta**x * (1 - theta) ** (n - x) for x in range(n + 1)]
[round(p, 4) for p in pmf], round(sum(pmf), 6)
```

The list is the full distribution; its sum is exactly 1. Plotting those bars for a fair coin
($n = 10$, $\theta = 0.5$) gives the classic symmetric mound:

```{figure} ../_static/foundations_binomial_pmf.png
:alt: Bar chart of the binomial distribution for n = 10 and theta = 0.5
:width: 90%

The {term}`binomial` distribution for $n = 10$, $\theta = 0.5$. Each bar is the {term}`probability` of
that many successes. It peaks at $x = 5$ (the expected $n\theta$) and is symmetric because $\theta =
0.5$; shift $\theta$ toward 0 or 1 and the mound slides and leans. The bars sum to 1.
```

:::{dropdown} Why the distribution matters for intervals
Every {term}`coverage` statement in these docs is a sum over this distribution. To ask "how often does my
interval trap $\theta$?" you list the counts $x$ whose interval contains $\theta$, look up each one's
$\Pr(X=x)$ from the formula above, and add them. That is literally what {doc}`page 5 <05_coverage>` and
the coverage engine compute. So the binomial is not background trivia — it is the machinery the whole
evaluation half of the package runs on.
:::

## Check yourself

**Q1.** For $n = 3$, $\theta = 0.5$ (three fair coins), what is $\Pr(X = 3)$ — all three heads?

:::{dropdown} Show answer
$\binom{3}{3}\,0.5^3\,0.5^0 = 1 \times 0.125 \times 1 = \mathbf{0.125}$, i.e. 1 in 8.
```python
from math import comb
comb(3, 3) * 0.5**3 * 0.5**0      # -> 0.125
```
:::

**Q2.** Without computing every bar, why must the six probabilities for $n = 5$ add up to exactly 1?

:::{dropdown} Show answer
Because the counts $0, 1, 2, 3, 4, 5$ are **all** the things that can happen and they cannot happen
together — the experiment always yields exactly one of them. The probabilities of a complete set of
mutually exclusive outcomes always sum to 1; the {term}`binomial` formula is built so that
$\sum_{x=0}^{n}\binom{n}{x}\theta^x(1-\theta)^{n-x} = 1$ for any $\theta$.
:::

**Q3.** With $n = 20$ and $\theta = 0.1$, do you expect the tallest bar near $x = 2$ or near $x = 10$?
Why?

:::{dropdown} Show answer
Near $x = 2$. The distribution peaks around the expected count $n\theta = 20 \times 0.1 = 2$, not at the
middle of the range. A small $\theta$ pushes the whole mound toward the low counts.
```python
from math import comb
n, th = 20, 0.1
peak = max(range(n + 1), key=lambda x: comb(n, x) * th**x * (1 - th)**(n - x))
peak      # -> 2
```
:::

---

:::{admonition} Terms used on this page
:class: seealso
{term}`trial` · {term}`Bernoulli trial` · {term}`success` · {term}`binomial` · {term}`theta` ·
{term}`probability` · {term}`random variable` · {term}`coverage`
:::

*New here? Start at {doc}`the proportion <01_proportion>`. Next: {doc}`sampling variability
<03_sampling_variability>` — why two samples disagree. Deeper: {doc}`the estimation problem
<../theory/01_the_problem>`.*
