# Day 1 — The problem, the estimate, and why it is hard

This is the first page of the **Methods & Mathematics** series. Everything the
package does hangs off the single problem described here, so it is worth being
precise about it before meeting any particular method.

## The experiment

You run $n$ independent trials, each a success or a failure, each with the same
unknown success probability $\theta$. The number of successes is a random
variable

$$
X \sim \text{Binomial}(n, \theta),
\qquad
\Pr(X = x \mid \theta) = \binom{n}{x}\,\theta^{x}(1-\theta)^{\,n-x},
\quad x = 0, 1, \dots, n .
$$

You observe **one** value $x$ and want to say something about $\theta$.

## The point estimate

The natural estimate is the sample proportion

$$
\hat\theta = \frac{x}{n}.
$$

This is also the **maximum likelihood estimate**: treating the probability above
as a function of $\theta$ for the observed $x$, the log-likelihood

$$
\ell(\theta) = x\log\theta + (n-x)\log(1-\theta) + \text{const}
$$

is maximized by setting $\ell'(\theta) = \tfrac{x}{\theta} - \tfrac{n-x}{1-\theta}
= 0$, which gives $\theta = x/n$. So $\hat\theta$ is not an arbitrary choice —
it is the value that makes the data most probable.

## Why a single number is not enough

$\hat\theta$ tells you nothing about how *sure* you are. Three successes in five
trials and three hundred in five hundred both give $\hat\theta = 0.6$, but the
second is far more informative. A **confidence interval** carries that
information: a data-dependent range $[L(x), U(x)]$ constructed so that, in
repeated experiments, it contains the true $\theta$ a fixed fraction of the time —
the **confidence level** $1 - \alpha$. In the code, $\alpha$ is the argument
`alp`; the usual `alp=0.05` asks for 95% intervals.

The frequentist promise is about the *procedure*, not any one interval: if the
recipe has 95% coverage, then across many datasets 95% of the intervals it
produces will trap the true value. Making that promise hold is the entire game.

## Why the binomial makes it hard

If $X$ were a continuous, unbounded normal variable, one interval would do and
this series would end here. Two features of the binomial break that:

1. **Discreteness.** $X$ takes only the integer values $0, 1, \dots, n$. There is
   no interval you can build that covers $\theta$ *exactly* $1-\alpha$ of the
   time for every $\theta$; coverage as a function of $\theta$ is a jagged step
   function that jumps whenever $\theta$ crosses one of the finitely many
   endpoints. The best you can do is control *how* it deviates from nominal.

2. **Boundedness.** $\theta$ lives in $[0, 1]$, and the data can land on the
   edges: $x = 0$ or $x = n$. A method built on the normal approximation, whose
   spread is driven by $\hat\theta(1-\hat\theta)$, sees that quantity vanish at
   the edges and collapses the interval to a single point — claiming perfect
   certainty exactly where the data are least informative.

These two problems are why there is not one method but many, and why the second
half of this package exists to **evaluate** them.

## The road map

The series follows the shape of the package:

- **Days 2–9 — construction.** Eight ways to build an interval: normal-approximation
  methods (Wald, Score, ArcSine, Logit, Wald-T), the likelihood-ratio method, the
  exact family, and the Bayesian credible interval.
- **Days 10–11 — repair.** Two general fixes — the adjustment factor $h$ and the
  continuity correction $c$ — that rescue the fragile approximate methods at the
  edges.
- **Days 12–17 — evaluation.** How to *score* a method: coverage probability,
  expected length, p-confidence / p-bias, error and long-term power, boundary
  aberrations, and Monte-Carlo evaluation over a Beta-distributed $\theta$.
- **Days 18–20 — the Bayesian toolbox.** Beyond intervals: Bayes factors,
  empirical Bayes, and posterior-predictive computation.

## In code

```python
import binomcikit as bk

bk.ciwd(n=5, alp=0.05)     # Wald 95% intervals for every x = 0..5
bk.ciscx(x=3, n=5, alp=0.05)   # Wilson interval for the single count x = 3 of 5
```

Notice the two shapes: bare names (`ciwd`) return one row per possible $x$ — handy
for studying a method — while the `…x` names (`ciscx`) take the single count you
actually observed.

---

*Next: Day 2 — the Wald interval, the textbook method and its failure modes.*
