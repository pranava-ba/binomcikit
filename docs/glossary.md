# Glossary

Every technical term used anywhere in these docs is defined here in plain language,
with a tiny example. Terms are hyperlinked throughout the site — click any linked
word to jump here. New terms are added as each method is documented.

:::{glossary}
proportion
  The fraction of {term}`trial`s that turn out to be "successes". Flip a coin 10
  times, get 6 heads → the observed proportion of heads is 6/10 = 0.6. We usually
  want the *true*, unknown proportion, which we call {term}`theta`.

trial
  One repetition of a yes/no experiment — a single coin flip, one patient either
  recovering or not, one manufactured part passing or failing.

Bernoulli trial
  A {term}`trial` with exactly two outcomes, conventionally "success" (1) and
  "failure" (0), where the chance of success is the same every time.

success
  The outcome we are counting. It need not be "good": for a defect rate, a
  "success" is a defective part. What matters is that we count it consistently.

binomial
  The pattern from adding up *n* independent {term}`Bernoulli trial`s: the number
  of successes *x* out of *n*. Written *X* ~ Binomial(*n*, {term}`theta`).

theta
  (θ) The true, unknown {term}`probability` of {term}`success` on one {term}`trial`
  — the number we are trying to estimate. Always between 0 and 1.

probability
  A number between 0 and 1 saying how likely something is: 0 = impossible,
  1 = certain, 0.5 = a fair coin's chance of heads.

random variable
  A quantity whose value depends on chance — e.g. *X*, the number of successes you
  will observe. Uncertain before the experiment, a fixed number after.

estimate
  A single best-guess value for an unknown quantity, computed from data — e.g. the
  observed proportion p̂ = x/n estimates {term}`theta`.

confidence interval
  A *range* of plausible values for {term}`theta`, instead of a single
  {term}`estimate`. A "95% confidence interval" comes from a recipe that, used
  over and over on fresh data, traps the true {term}`theta` about 95% of the time.

confidence level
  The advertised success rate of a {term}`confidence interval` recipe, e.g. 95%.
  Equal to 1 − {term}`alpha`.

alpha
  (α) The allowed error rate of a {term}`confidence interval`: α = 0.05 pairs with
  a 95% {term}`confidence level`. Smaller α → wider, safer intervals.

coverage
  How often a {term}`confidence interval` recipe *actually* traps the true
  {term}`theta`. Ideally this matches the {term}`confidence level`; measuring when
  it does not is a core purpose of this package.

expected length
  The average width (upper minus lower) of a {term}`confidence interval`. Narrower
  is more informative — but not if it costs {term}`coverage`.

quantile
  The value below which a given fraction of a distribution lies. The 0.975 quantile
  of the standard normal (≈ 1.96) is the multiplier behind most 95% intervals.

prior
  In {term}`Bayesian` methods, what you believed about {term}`theta` *before* seeing
  data, written as a distribution (often a {term}`Beta distribution`).

posterior
  Your updated belief about {term}`theta` *after* combining the {term}`prior` with
  the data, via Bayes' rule.

Bayesian
  An approach that treats the unknown {term}`theta` as itself uncertain, described by
  a {term}`prior` that data updates into a {term}`posterior`. The alternative,
  "frequentist", treats {term}`theta` as a fixed unknown constant.

Beta distribution
  A flexible distribution on values between 0 and 1, written Beta(a, b). It is the
  natural {term}`prior` for a {term}`proportion` because the {term}`posterior` is
  again a Beta — which keeps the maths clean.

credible interval
  The {term}`Bayesian` counterpart of a {term}`confidence interval`: a range that holds a stated
  share (say 95%) of the {term}`posterior` probability for {term}`theta`. You read it directly —
  "there is a 95% chance θ is in here, given my data and {term}`prior`" — which is *not* what a
  frequentist confidence interval says.

posterior mean
  The average of the {term}`posterior` distribution — the Bayesian point {term}`estimate` of
  {term}`theta`. For a Beta(x+a, n−x+b) posterior it is (x+a)/(n+a+b), which, unlike p̂ = x/n, is
  pulled slightly toward the {term}`prior` (so it is nonzero even at x = 0).

highest posterior density interval
  (HPD) The **shortest** {term}`credible interval` with the required probability — every point
  inside it is more probable than every point outside. It differs from the equal-tailed (quantile)
  credible interval when the {term}`posterior` is skewed, and near a boundary it can be one-sided.

Bayes factor
  A number weighing how well two hypotheses about {term}`theta` explain the data: the ratio of the
  data's probability under one to its probability under the other. Unlike a p-value it can support
  *either* hypothesis, and is read on an interpretive (Jeffreys) scale from "bare mention" to "strong".

empirical Bayes
  A shortcut that **estimates the {term}`prior` from the data itself** (here by fitting the
  Beta-Binomial marginal likelihood) instead of choosing it up front, then proceeds as usual to a
  {term}`posterior` and a {term}`credible interval`.

posterior probability
  The probability of a statement about {term}`theta` read straight off the {term}`posterior` — for
  example P(θ < 0.05 | data), the posterior area below a threshold. A question a frequentist
  {term}`confidence interval` cannot answer directly.

posterior predictive
  The probability of a **future** result — e.g. how many successes in the next m trials — obtained by
  averaging the ordinary prediction over the whole {term}`posterior` for {term}`theta`, so it honestly
  includes your remaining uncertainty about θ.

continuity correction
  A small ± adjustment applied when approximating discrete {term}`binomial` counts by
  a smooth (normal) curve, to improve accuracy for small *n*.

standard error
  How much an {term}`estimate` typically wobbles from sample to sample. For a
  {term}`proportion` p̂ from *n* trials it is √(p̂(1−p̂)/n) — smaller for larger *n*.

variance-stabilising transformation
  A change of scale chosen so an {term}`estimate`'s wobble ({term}`standard error`) is
  roughly the *same size wherever the truth sits*. For a {term}`proportion` the arcsine
  transform φ = arcsin√p̂ does this: its wobble is about 1/(2√n) for *every* {term}`theta`.
  That lets you build a simple symmetric interval on the φ-scale, then map it back.

back-transformation
  Undoing a {term}`variance-stabilising transformation` to return an interval to the
  original 0–1 {term}`proportion` scale. The arcsine interval is built in φ and mapped
  back with p = sin²(φ). (Mapping only the *endpoints* is what makes arcsine misbehave at
  the boundary — see the {doc}`arcsine <methods/arcsine>` page.)

odds
  The number of successes per failure: odds = p / (1 − p). A {term}`proportion` of p = 0.8
  is odds of 4 (four successes for every failure, "4 to 1"). Odds run from 0 to ∞.

log-odds
  (the **logit**) The natural log of the {term}`odds`: logit(p) = ln(p / (1 − p)). It
  stretches the 0–1 {term}`proportion` scale out to the whole line (−∞ to +∞), so a
  symmetric interval built there can never fall outside 0–1 once mapped back. logit(0.5) = 0.

expit
  (the **logistic function**) The inverse of {term}`log-odds`: expit(u) = 1 / (1 + e^−u).
  It squashes any number on the line back into (0, 1). Used to {term}`back-transformation`
  a logit-scale interval to a {term}`proportion`. expit(0) = 0.5.

tail probability
  The chance, if {term}`theta` were some value, of seeing a result **as or more extreme** than
  the one observed. Adding up binomial probabilities in the tail is how an **exact** interval
  decides which θ are still plausible. Example: with n = 10, θ = 0.5, the chance of ≥ 9 heads is a
  small upper-tail probability.

Clopper–Pearson
  The **exact** {term}`confidence interval`, built by inverting the exact binomial test using
  {term}`tail probability`s rather than a normal approximation. Its {term}`coverage` is guaranteed
  to be at least the nominal level (never below), at the cost of being noticeably wide. It is the
  `e = 1` end of binomcikit's tunable exact family (see the {doc}`exact <methods/exact>` page); the
  logit method borrows its one-sided form at x = 0 and x = n.

Mid-P
  A less-conservative **exact** interval that counts only **half** of the observed outcome's
  probability in the {term}`tail probability`, instead of all of it. This trims {term}`Clopper–Pearson`'s
  excess width and pulls {term}`coverage` closer to nominal (occasionally a hair below). It is the
  `e = 0.5` setting of the exact family.

acceptability function
  In Blaker's method, γ(x, θ): the probability, if θ were true, of seeing an outcome whose *smaller*
  {term}`tail probability` is no larger than the one you observed. The Blaker interval keeps every θ
  with γ(x, θ) ≥ {term}`alpha`. See the {doc}`Blaker <methods/blaker>` page.

nested interval
  An interval that is always **contained inside** another. Blaker's interval is nested inside
  {term}`Clopper–Pearson` — never wider — which is how it keeps the exact coverage guarantee while
  wasting less width.

t-distribution
  (Student's *t*) A bell curve like the normal but with **heavier tails**, used as the
  reference curve when the {term}`standard error` is itself *estimated* from the data rather
  than known. It is controlled by its {term}`degrees of freedom`: few → fat tails (wider
  intervals); many → it becomes the normal curve. Its 0.975 {term}`quantile` is > 1.96.

degrees of freedom
  A number that sets the shape of a {term}`t-distribution` — roughly, how much information the
  data carry about the spread. More trials → more degrees of freedom → tails closer to normal.

Satterthwaite approximation
  A standard recipe for the *effective* {term}`degrees of freedom` to use when a variance is
  estimated: it matches the estimator's mean and variance to a scaled chi-squared. The
  **Wald-T** method uses it to pick the {term}`t-distribution` that best fits each (x, n).

critical value
  The {term}`quantile` of a reference curve (usually the normal) that sets how many
  {term}`standard error`s wide an interval reaches. For 95% it is ≈ 1.96.

null hypothesis
  A specific value we provisionally assume for {term}`theta` — say θ = 0.3 — so we can
  ask whether the observed data look surprising *if that value were true*. Written H₀.

score test
  A hypothesis test for a {term}`null hypothesis` value of {term}`theta` that measures
  the {term}`standard error` *at the value being tested* (under H₀), not at the observed
  {term}`estimate` p̂. This one change is what makes the **Wilson** interval better
  behaved than **Wald**, whose {term}`standard error` uses p̂.

test inversion
  Building a {term}`confidence interval` as the set of all {term}`null hypothesis`
  values a test would *not* reject at level {term}`alpha`. Inverting the {term}`score
  test` gives the Wilson interval; inverting the exact binomial test gives Clopper–Pearson.

likelihood
  How probable the observed data are, read as a function of the unknown {term}`theta`. For x
  successes in n trials it is ∝ θ^x (1−θ)^(n−x). The θ that maximises it is the
  {term}`maximum likelihood estimate`.

maximum likelihood estimate
  (MLE) The parameter value that makes the observed data most probable. For a
  {term}`binomial`, the MLE of {term}`theta` is just the observed {term}`proportion` p̂ = x/n.

likelihood-ratio statistic
  A measure of how much *worse* a candidate {term}`theta` fits than the best fit (the
  {term}`maximum likelihood estimate`): 2·[ln {term}`likelihood`(p̂) − ln likelihood(θ)]. It is 0
  at p̂ and grows as θ moves away. Keeping the θ with a small enough statistic gives a
  {term}`confidence interval`.

Wilks' theorem
  The result that, for large n, the {term}`likelihood-ratio statistic` follows a chi-squared
  distribution with one degree of freedom. That is why the interval's cutoff is z² (≈ 1.96² for
  95%): z² is the matching chi-squared {term}`quantile`.

Agresti–Coull
  A simple repair of the **Wald** interval: add about two successes and two failures to the data
  before applying the Wald formula. It fixes most of Wald's {term}`coverage` problem.

zero-width interval
  (ZWI) A {term}`confidence interval` that has collapsed to a single point — it claims a certainty
  it does not have. Wald produces one at x = 0 and x = n.

aberration
  A confidence limit that behaves badly — e.g. running past a sensible boundary, or moving in the
  wrong direction. binomcikit reports these as the LABB / UABB flags.
:::

---

*This page holds the shared vocabulary; individual method pages add their own terms
and link back here. See the docs convention in {doc}`foundations/index`.*
